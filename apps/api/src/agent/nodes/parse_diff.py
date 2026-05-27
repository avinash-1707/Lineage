from __future__ import annotations

from src.agent.state import ReviewState
from src.integrations.github.client import GitHubClient
from src.integrations.github.diff_parser import parse_unified_diff
from src.observability.logging import get_logger

log = get_logger(__name__)


async def parse_diff(state: ReviewState) -> ReviewState:
    async with GitHubClient() as client:
        diff = await client.fetch_pr_diff(state["repo_full_name"], state["pr_number"])
    files = parse_unified_diff(diff)
    log.info("agent.parse_diff", files=len(files), pr=state["pr_number"])
    return {**state, "diff": diff, "files": files}
