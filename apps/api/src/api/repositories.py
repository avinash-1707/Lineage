from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.models.auth import Repository

router = APIRouter()


class RepositoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    github_repo_id: int
    owner: str
    name: str
    full_name: str
    default_branch: str | None
    private: bool
    active: bool


@router.get("/", response_model=list[RepositoryOut])
async def list_repositories(db: AsyncSession = Depends(get_session)) -> list[RepositoryOut]:
    rows = (
        await db.execute(
            select(Repository).where(Repository.deleted_at.is_(None)).order_by(Repository.full_name)
        )
    ).scalars().all()
    return [RepositoryOut.model_validate(r) for r in rows]


@router.get("/{repo_id}", response_model=RepositoryOut)
async def get_repository(repo_id: uuid.UUID, db: AsyncSession = Depends(get_session)) -> RepositoryOut:
    row = (
        await db.execute(select(Repository).where(Repository.id == repo_id))
    ).scalar_one_or_none()
    if row is None:
        raise HTTPException(404, "repository not found")
    return RepositoryOut.model_validate(row)
