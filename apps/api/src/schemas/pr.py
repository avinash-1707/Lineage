from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PullRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: int
    title: str
    state: str
    head_sha: str
    base_ref: str
    author_login: str | None
    created_at: datetime
    updated_at: datetime


class PullRequestList(BaseModel):
    items: list[PullRequestOut]
    total: int
