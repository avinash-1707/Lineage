from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_retrieve_empty_returns_empty_list() -> None:
    from src.memory.retrieval import retrieve_relevant_memory

    out = await retrieve_relevant_memory("x/y", [], top_k=5)
    assert out == []
