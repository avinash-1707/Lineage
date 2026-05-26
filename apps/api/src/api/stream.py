from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator

from fastapi import APIRouter, Request
from redis.asyncio import Redis
from sse_starlette.sse import EventSourceResponse

from src.config import get_settings

router = APIRouter()


def _redis() -> Redis:
    return Redis.from_url(get_settings().redis_url, decode_responses=True)


@router.get("/reviews/{pr_id}")
async def stream_review(pr_id: int, request: Request) -> EventSourceResponse:
    channel = f"review:events:{pr_id}"
    redis = _redis()

    async def event_gen() -> AsyncIterator[dict[str, str]]:
        pubsub = redis.pubsub()
        await pubsub.subscribe(channel)
        try:
            yield {"event": "open", "data": json.dumps({"pr_id": pr_id})}
            while True:
                if await request.is_disconnected():
                    break
                msg = await pubsub.get_message(ignore_subscribe_messages=True, timeout=15.0)
                if msg is None:
                    yield {"event": "ping", "data": "{}"}
                    continue
                yield {"event": "message", "data": msg["data"]}
                await asyncio.sleep(0)
        finally:
            await pubsub.unsubscribe(channel)
            await pubsub.close()
            await redis.close()

    return EventSourceResponse(event_gen())
