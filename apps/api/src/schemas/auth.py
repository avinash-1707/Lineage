"""Pydantic I/O contracts for auth. No SQLAlchemy imports."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "AccountObject",
    "InstallationEventPayload",
    "InstallationObject",
    "InstallationRepository",
    "SenderObject",
    "UserMe",
]


class UserMe(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    name: str | None
    avatar_url: str | None
    role: str
    plan: str
    created_at: datetime


class AccountObject(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    login: str
    type: str


class InstallationRepository(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    name: str
    full_name: str
    private: bool = False


class InstallationObject(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    account: AccountObject
    target_type: str
    repository_selection: str | None = None


class SenderObject(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    login: str
    type: str | None = None


class InstallationEventPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")

    action: Literal[
        "created",
        "deleted",
        "suspend",
        "unsuspend",
        "new_permissions_accepted",
    ]
    installation: InstallationObject
    repositories: list[InstallationRepository] = Field(default_factory=list)
    sender: SenderObject | None = None
