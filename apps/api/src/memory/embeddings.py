"""Embedding helpers built on top of the Gemini client.

Keeps memory/retrieval code decoupled from the concrete LLM provider — anything
that needs a vector should depend on these functions, not the SDK directly.
"""

from __future__ import annotations

from src.llm.gemini import get_gemini_client


async def embed_texts(texts: list[str], *, task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    if not texts:
        return []
    return await get_gemini_client().embed(texts, task_type=task_type)


async def embed_one(text: str, *, task_type: str = "RETRIEVAL_QUERY") -> list[float]:
    return await get_gemini_client().embed_one(text, task_type=task_type)
