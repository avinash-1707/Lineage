"""GitHub App installation token minting for Celery tasks.

Tokens cached in Redis with TTL safely under GitHub's 60-min validity.
Cache-miss falls through to fresh mint via JWT-signed request.
"""

from __future__ import annotations

import httpx
from redis.asyncio import Redis

from src.config import Settings, get_settings
from src.integrations.github.app import (
    build_app_jwt,
    fetch_installation_token,
    load_private_key,
)
from src.observability.logging import get_logger

log = get_logger(__name__)

CACHE_KEY_PREFIX = "gh:install_token"

__all__ = ["get_installation_token", "get_installation_token_cached"]


def _cache_key(installation_id: int) -> str:
    return f"{CACHE_KEY_PREFIX}:{installation_id}"


async def get_installation_token(
    installation_id: int,
    *,
    redis: Redis | None = None,
    settings: Settings | None = None,
    http: httpx.AsyncClient | None = None,
) -> str:
    cfg = settings or get_settings()
    key = _cache_key(installation_id)

    if redis is not None:
        cached = await redis.get(key)
        if cached:
            log.debug("github.install_token_cache_hit", installation_id=installation_id)
            return cached

    if not cfg.github_app_client_id:
        raise RuntimeError("github_app_client_id is required to mint installation tokens")

    pem = load_private_key(cfg)
    app_jwt = build_app_jwt(app_client_id=cfg.github_app_client_id, private_key_pem=pem)

    owns_http = http is None
    client = http or httpx.AsyncClient(timeout=10.0)
    try:
        resp = await fetch_installation_token(
            app_jwt=app_jwt,
            installation_id=installation_id,
            http=client,
            api_base_url=cfg.github_api_base_url,
        )
    finally:
        if owns_http:
            await client.aclose()

    if redis is not None:
        await redis.setex(key, cfg.install_token_cache_ttl_seconds, resp.token)
        log.info(
            "github.install_token_minted",
            installation_id=installation_id,
            cached_for_seconds=cfg.install_token_cache_ttl_seconds,
        )
    else:
        log.info("github.install_token_minted_no_cache", installation_id=installation_id)

    return resp.token


async def get_installation_token_cached(installation_id: int) -> str:
    """One-shot helper for Celery tasks: opens a Redis connection per call."""
    cfg = get_settings()
    redis = Redis.from_url(cfg.redis_url, decode_responses=True)
    try:
        return await get_installation_token(installation_id, redis=redis, settings=cfg)
    finally:
        await redis.aclose()
