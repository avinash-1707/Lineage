from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Repository(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    name: str
    full_name: str
    default_branch: str | None = None


class User(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    login: str


class PullRequestRef(BaseModel):
    model_config = ConfigDict(extra="ignore")

    sha: str
    ref: str


class PullRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    number: int
    state: str
    title: str
    body: str | None = None
    user: User
    head: PullRequestRef
    base: PullRequestRef
    draft: bool = False


class PullRequestEvent(BaseModel):
    model_config = ConfigDict(extra="ignore")

    action: str
    number: int
    pull_request: PullRequest
    repository: Repository


class ReviewCommentEvent(BaseModel):
    model_config = ConfigDict(extra="ignore")

    action: str
    repository: Repository
    pull_request: PullRequest
    comment: dict = Field(default_factory=dict)


class IssueCommentEvent(BaseModel):
    model_config = ConfigDict(extra="ignore")

    action: str
    repository: Repository
    issue: dict
    comment: dict
