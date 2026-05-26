from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request, status

from src.config import get_settings
from src.observability.logging import get_logger
from src.webhooks.schemas import PullRequestEvent, ReviewCommentEvent
from src.webhooks.signature import verify_signature
from src.workers.tasks.review import enqueue_review
from src.workers.tasks.signals import enqueue_signal

router = APIRouter()
log = get_logger(__name__)

SUPPORTED_PR_ACTIONS = {"opened", "synchronize", "reopened", "ready_for_review"}


@router.post("/github", status_code=status.HTTP_202_ACCEPTED)
async def github_webhook(
    request: Request,
    background: BackgroundTasks,
    x_github_event: str = Header(..., alias="X-GitHub-Event"),
    x_hub_signature_256: str | None = Header(None, alias="X-Hub-Signature-256"),
    x_github_delivery: str | None = Header(None, alias="X-GitHub-Delivery"),
) -> dict[str, str]:
    settings = get_settings()
    body = await request.body()

    if not verify_signature(
        body, x_hub_signature_256, settings.github_webhook_secret.get_secret_value()
    ):
        log.warning("webhook.signature_invalid", delivery=x_github_delivery)
        raise HTTPException(status_code=401, detail="invalid signature")

    payload = await request.json()
    log.info("webhook.received", event=x_github_event, delivery=x_github_delivery)

    if x_github_event == "pull_request":
        evt = PullRequestEvent.model_validate(payload)
        if evt.action in SUPPORTED_PR_ACTIONS and not evt.pull_request.draft:
            background.add_task(
                enqueue_review,
                repo_full_name=evt.repository.full_name,
                pr_number=evt.number,
                head_sha=evt.pull_request.head.sha,
            )
        return {"status": "queued", "event": x_github_event}

    if x_github_event in {"pull_request_review", "pull_request_review_comment", "issue_comment"}:
        evt = ReviewCommentEvent.model_validate(payload)
        background.add_task(
            enqueue_signal,
            repo_full_name=evt.repository.full_name,
            pr_number=evt.pull_request.number,
            payload=payload,
            event_type=x_github_event,
        )
        return {"status": "queued", "event": x_github_event}

    return {"status": "ignored", "event": x_github_event}
