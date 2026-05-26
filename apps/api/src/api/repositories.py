from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.models.repository import Repository

router = APIRouter()


class RepositoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    github_id: int
    full_name: str
    default_branch: str | None


@router.get("/", response_model=list[RepositoryOut])
async def list_repositories(db: AsyncSession = Depends(get_session)) -> list[RepositoryOut]:
    rows = (await db.execute(select(Repository).order_by(Repository.full_name))).scalars().all()
    return [RepositoryOut.model_validate(r) for r in rows]


@router.get("/{repo_id}", response_model=RepositoryOut)
async def get_repository(repo_id: int, db: AsyncSession = Depends(get_session)) -> RepositoryOut:
    row = (await db.execute(select(Repository).where(Repository.id == repo_id))).scalar_one_or_none()
    if row is None:
        raise HTTPException(404, "repository not found")
    return RepositoryOut.model_validate(row)
