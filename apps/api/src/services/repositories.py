"""Idempotent upserts for repository + PR rows.

Webhook handlers and the review pipeline both need to write through this
layer so that callers never construct ORM rows directly.
"""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.auth import Repository
from src.models.pull_request import PullRequest


async def upsert_repository(
    db: AsyncSession,
    *,
    github_repo_id: int,
    owner: str,
    name: str,
    full_name: str,
    default_branch: str | None = None,
    private: bool = False,
    installation_id: uuid.UUID | None = None,
) -> Repository:
    row = (
        await db.execute(select(Repository).where(Repository.github_repo_id == github_repo_id))
    ).scalar_one_or_none()

    if row is None:
        row = Repository(
            github_repo_id=github_repo_id,
            owner=owner,
            name=name,
            full_name=full_name,
            default_branch=default_branch,
            private=private,
            installation_id=installation_id,
        )
        db.add(row)
    else:
        row.owner = owner
        row.name = name
        row.full_name = full_name
        row.private = private
        if default_branch is not None:
            row.default_branch = default_branch
        if installation_id is not None:
            row.installation_id = installation_id

    await db.flush()
    return row


async def upsert_pull_request(
    db: AsyncSession,
    *,
    repository_id: uuid.UUID,
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
