"""Redis sorted-set sliding-window rate limiter."""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable

from fastapi import Depends, HTTPException, Request, status
from redis.asyncio import Redis

from src.config import Settings, get_settings
from src.core.redis import get_redis
from src.core.security import AuthError

__all__ = ["RateLimitExceeded", "RateLimiter", "rate_limit"]


class RateLimitExceeded(AuthError):
    def __init__(self, *, retry_after_seconds: int = 60) -> None:
        super().__init__("rate limit exceeded")
        self.retry_after_seconds = retry_after_seconds


class RateLimiter:
    def __init__(self, redis: Redis, *, max_per_minute: int, key_prefix: str) -> None:
        self._redis = redis
        self._max = max_per_minute
        self._prefix = key_prefix

    async def check(self, identifier: str) -> None:
        now_ms = int(time.time() * 1000)
        window_start = now_ms - 60_000
        key = f"ratelimit:{self._prefix}:{identifier}"
        member = f"{now_ms}-{id(identifier)}"

        async with self._redis.pipeline(transaction=True) as pipe:
            pipe.zremrangebyscore(key, 0, window_start)
            pipe.zadd(key, {member: now_ms})
            pipe.zcard(key)
            pipe.expire(key, 60)
            _, _, count, _ = await pipe.execute()

        if int(count) > self._max:
            raise RateLimitExceeded()


def rate_limit(prefix: str) -> Callable[..., Awaitable[None]]:
    async def _dep(
        request: Request,
        redis: Redis = Depends(get_redis),
        settings: Settings = Depends(get_settings),
    ) -> None:
        if not settings.rate_limit_enabled:
            return
        identifier = request.client.host if request.client else "unknown"
        limiter = RateLimiter(
            redis,
            max_per_minute=settings.auth_rate_limit_per_minute,
            key_prefix=prefix,
        )
        try:
            await limiter.check(identifier)
        except RateLimitExceeded as exc:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="rate limit exceeded",
                headers={"Retry-After": str(exc.retry_after_seconds)},
            ) from exc

    return _dep
