from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.models.pull_request import PullRequest
from src.models.review_comment import ReviewComment

router = APIRouter()


class Overview(BaseModel):
    total_repositories: int
    total_pull_requests: int
    total_comments: int
    accepted: int
    dismissed: int
    resolved: int


@router.get("/overview", response_model=Overview)
async def overview(db: AsyncSession = Depends(get_session)) -> Overview:
    total_prs = (await db.execute(select(func.count(PullRequest.id)))).scalar_one()
    total_comments = (await db.execute(select(func.count(ReviewComment.id)))).scalar_one()

    by_signal = dict(
        (row[0], row[1])
        for row in (
            await db.execute(
                select(ReviewComment.feedback_signal, func.count(ReviewComment.id)).group_by(
                    ReviewComment.feedback_signal
                )
            )
        ).all()
    )

    from src.models.repository import Repository as Repo

    total_repos = (await db.execute(select(func.count(Repo.id)))).scalar_one()

    return Overview(
        total_repositories=int(total_repos or 0),
        total_pull_requests=int(total_prs or 0),
        total_comments=int(total_comments or 0),
        accepted=int(by_signal.get("accepted", 0)),
        dismissed=int(by_signal.get("dismissed", 0)),
        resolved=int(by_signal.get("resolved", 0)),
    )
