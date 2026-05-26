from __future__ import annotations

import asyncio
from typing import Any

from src.observability.logging import get_logger
from src.workers.celery_app import celery_app

log = get_logger(__name__)


def enqueue_review(repo_full_name: str, pr_number: int, head_sha: str) -> str:
    result = run_review.delay(repo_full_name, pr_number, head_sha)
    log.info("review.enqueued", task_id=result.id, repo=repo_full_name, pr=pr_number)
    return result.id


@celery_app.task(
    name="reviews.run_review",
    bind=True,
    max_retries=3,
    default_retry_delay=30,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
)
def run_review(self, repo_full_name: str, pr_number: int, head_sha: str) -> dict[str, Any]:
    from src.agent.graph import build_graph
    from src.agent.state import ReviewState

    log.info("review.start", repo=repo_full_name, pr=pr_number, sha=head_sha)
    graph = build_graph()
    initial: ReviewState = {
        "repo_full_name": repo_full_name,
        "pr_number": pr_number,
        "head_sha": head_sha,
        "diff": None,
        "files": [],
        "memory_hits": [],
        "patterns": [],
        "feedback": [],
        "published": False,
        "errors": [],
    }
    final = asyncio.run(graph.ainvoke(initial))
    log.info("review.done", repo=repo_full_name, pr=pr_number, comments=len(final.get("feedback", [])))
    return {"published": final.get("published", False), "comments": len(final.get("feedback", []))}
