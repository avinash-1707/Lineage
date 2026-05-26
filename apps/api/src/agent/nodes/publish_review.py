from __future__ import annotations

from src.agent.state import ReviewState
from src.github.client import GitHubClient
from src.observability.logging import get_logger

log = get_logger(__name__)


async def publish_review(state: ReviewState) -> ReviewState:
    async with GitHubClient() as client:
        await client.publish_review(
            repo_full_name=state["repo_full_name"],
            pr_number=state["pr_number"],
            commit_sha=state["head_sha"],
            comments=state["feedback"],
        )
    log.info("agent.publish_review", pr=state["pr_number"], n=len(state["feedback"]))
    return {**state, "published": True}
