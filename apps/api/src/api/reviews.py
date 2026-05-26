from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.models.pull_request import PullRequest
from src.models.review_comment import ReviewComment
from src.schemas.review import ReviewCommentOut, ReviewSummary

router = APIRouter()


@router.get("/{pr_id}", response_model=ReviewSummary)
async def get_review(pr_id: int, db: AsyncSession = Depends(get_session)) -> ReviewSummary:
    pr = (await db.execute(select(PullRequest).where(PullRequest.id == pr_id))).scalar_one_or_none()
    if pr is None:
        raise HTTPException(404, "pull request not found")

    rows = (
        await db.execute(
            select(ReviewComment)
            .where(ReviewComment.pull_request_id == pr_id)
            .order_by(ReviewComment.created_at.desc())
        )
    ).scalars().all()

    return ReviewSummary(
        pr_id=pr.id,
        head_sha=pr.head_sha,
        comments=[ReviewCommentOut.model_validate(r) for r in rows],
        published=any(r.github_comment_id is not None for r in rows),
    )


@router.get("/", response_model=list[ReviewCommentOut])
async def list_review_comments(
    pr_id: int = Query(...),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_session),
) -> list[ReviewCommentOut]:
    rows = (
        await db.execute(
            select(ReviewComment)
            .where(ReviewComment.pull_request_id == pr_id)
            .order_by(ReviewComment.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
    ).scalars().all()
    return [ReviewCommentOut.model_validate(r) for r in rows]
