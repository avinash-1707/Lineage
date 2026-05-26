"""Idempotent upserts for repository + PR rows.

Webhook handlers and the review pipeline both need to write through this
layer so that callers never construct ORM rows directly.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.pull_request import PullRequest
from src.models.repository import Repository


async def upsert_repository(
    db: AsyncSession,
    *,
    github_id: int,
    full_name: str,
    default_branch: str | None,
    installation_id: int | None = None,
) -> Repository:
    row = (
        await db.execute(select(Repository).where(Repository.github_id == github_id))
    ).scalar_one_or_none()

    if row is None:
        row = Repository(
            github_id=github_id,
            full_name=full_name,
            default_branch=default_branch,
            installation_id=installation_id,
        )
        db.add(row)
    else:
        row.full_name = full_name
        row.default_branch = default_branch
        if installation_id is not None:
            row.installation_id = installation_id

    await db.flush()
    return row


async def upsert_pull_request(
    db: AsyncSession,
    *,
    repository_id: int,
    number: int,
    title: str,
    state: str,
    head_sha: str,
    base_ref: str,
    author_login: str | None,
) -> PullRequest:
    row = (
        await db.execute(
            select(PullRequest).where(
                PullRequest.repository_id == repository_id,
                PullRequest.number == number,
            )
        )
    ).scalar_one_or_none()

    if row is None:
        row = PullRequest(
            repository_id=repository_id,
            number=number,
            title=title,
            state=state,
            head_sha=head_sha,
            base_ref=base_ref,
            author_login=author_login,
        )
        db.add(row)
    else:
        row.title = title
        row.state = state
        row.head_sha = head_sha
        row.base_ref = base_ref
        row.author_login = author_login

    await db.flush()
    return row
