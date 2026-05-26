from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

Severity = Literal["info", "warn", "block"]
Signal = Literal["accepted", "dismissed", "resolved", "none"]


class ReviewCommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pull_request_id: int
    path: str
    line: int
    side: str
    severity: Severity
    body: str
    pattern_label: str | None
    feedback_signal: Signal | None
    created_at: datetime


class ReviewSummary(BaseModel):
    pr_id: int
    head_sha: str
    comments: list[ReviewCommentOut]
    published: bool
