from __future__ import annotations

from collections.abc import AsyncIterator

from redis.asyncio import ConnectionPool, Redis

from src.config import Settings, get_settings

_pool: ConnectionPool | None = None


def get_redis_pool(settings: Settings | None = None) -> ConnectionPool:
    global _pool
    if _pool is None:
        cfg = settings or get_settings()
        _pool = ConnectionPool.from_url(
            cfg.redis_url,
            decode_responses=True,
            max_connections=64,
        )
    return _pool


async def get_redis() -> AsyncIterator[Redis]:
    pool = get_redis_pool()
    client = Redis(connection_pool=pool)
    try:
        yield client
    finally:
        await client.aclose()


async def close_redis() -> None:
    global _pool
    if _pool is not None:
        await _pool.aclose()
        _pool = None
