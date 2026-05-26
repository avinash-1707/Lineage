"""Persist Lineage-generated review comments."""

from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from src.agent.state import FeedbackComment
from src.models.review_comment import ReviewComment


async def record_review_comments(
    db: AsyncSession,
    *,
    pull_request_id: int,
    comments: Iterable[FeedbackComment],
    pattern_label_by_path: dict[str, str] | None = None,
) -> list[ReviewComment]:
    pattern_label_by_path = pattern_label_by_path or {}
    rows = [
        ReviewComment(
            pull_request_id=pull_request_id,
            path=c["path"],
            line=c["line"],
            side=c.get("side", "RIGHT"),
            severity=c.get("severity", "info"),
            body=c["body"],
            pattern_label=pattern_label_by_path.get(c["path"]),
        )
        for c in comments
    ]
    db.add_all(rows)
    await db.flush()
    return rows
