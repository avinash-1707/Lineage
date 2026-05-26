from __future__ import annotations

from src.agent.state import ReviewState
from src.memory.retrieval import retrieve_relevant_memory
from src.observability.logging import get_logger

log = get_logger(__name__)


async def retrieve_memory(state: ReviewState) -> ReviewState:
    query_chunks = [f["patch"] for f in state["files"] if f.get("patch")]
    hits = await retrieve_relevant_memory(
        repo_full_name=state["repo_full_name"],
        query_chunks=query_chunks,
        top_k=10,
    )
    log.info("agent.retrieve_memory", hits=len(hits))
    return {**state, "memory_hits": hits}
