from __future__ import annotations

from typing import Any

from src.observability.logging import get_logger
from src.workers.celery_app import celery_app

log = get_logger(__name__)


def enqueue_signal(
    repo_full_name: str, pr_number: int, payload: dict[str, Any], event_type: str
) -> str:
    result = ingest_signal.delay(repo_full_name, pr_number, payload, event_type)
    log.info("signal.enqueued", task_id=result.id, repo=repo_full_name, pr=pr_number)
    return result.id


@celery_app.task(
    name="signals.ingest_signal",
    bind=True,
    max_retries=3,
    default_retry_delay=15,
    autoretry_for=(Exception,),
    retry_backoff=True,
)
def ingest_signal(
    self,
    repo_full_name: str,
    pr_number: int,
    payload: dict[str, Any],
    event_type: str,
) -> dict[str, Any]:
    log.info("signal.ingest", repo=repo_full_name, pr=pr_number, event=event_type)
    # TODO: persist signal, derive embedding, upsert into Qdrant memory.
    return {"stored": True, "event": event_type}
