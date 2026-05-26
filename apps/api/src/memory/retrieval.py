from __future__ import annotations

from typing import Any

from qdrant_client.http import models as qmodels

from src.agent.state import MemoryHit
from src.config import get_settings
from src.memory.client import get_qdrant
from src.memory.embeddings import embed_texts


async def retrieve_relevant_memory(
    repo_full_name: str,
    query_chunks: list[str],
    top_k: int = 10,
) -> list[MemoryHit]:
    if not query_chunks:
        return []

    settings = get_settings()
    client = get_qdrant()
    vectors = await embed_texts(query_chunks, task_type="RETRIEVAL_QUERY")

    flt = qmodels.Filter(
        must=[
            qmodels.FieldCondition(
                key="repo_full_name",
                match=qmodels.MatchValue(value=repo_full_name),
            )
        ]
    )

    seen: dict[str, MemoryHit] = {}
    for vec in vectors:
        results = await client.search(
            collection_name=settings.qdrant_collection,
            query_vector=vec,
            query_filter=flt,
            limit=top_k,
            with_payload=True,
        )
        for r in results:
            hit_id = str(r.id)
            payload: dict[str, Any] = r.payload or {}
            existing = seen.get(hit_id)
            if existing is None or r.score > existing["score"]:
                seen[hit_id] = {"id": hit_id, "score": r.score, "payload": payload}

    return sorted(seen.values(), key=lambda h: h["score"], reverse=True)[:top_k]


async def upsert_memory(
    point_id: str,
    vector: list[float],
    payload: dict[str, Any],
) -> None:
    settings = get_settings()
    client = get_qdrant()
    await client.upsert(
        collection_name=settings.qdrant_collection,
        points=[qmodels.PointStruct(id=point_id, vector=vector, payload=payload)],
    )
