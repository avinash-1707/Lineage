from __future__ import annotations

from functools import lru_cache

from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models as qmodels

from src.config import get_settings


@lru_cache
def get_qdrant() -> AsyncQdrantClient:
    settings = get_settings()
    api_key = settings.qdrant_api_key.get_secret_value() if settings.qdrant_api_key else None
    return AsyncQdrantClient(url=settings.qdrant_url, api_key=api_key)


async def ensure_collection() -> None:
    settings = get_settings()
    client = get_qdrant()
    existing = await client.get_collections()
    names = {c.name for c in existing.collections}
    if settings.qdrant_collection in names:
        return
    await client.create_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=qmodels.VectorParams(
            size=settings.embedding_dim,
            distance=qmodels.Distance.COSINE,
        ),
    )
