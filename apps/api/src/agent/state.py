from __future__ import annotations

from typing import Any, TypedDict


class FileDiff(TypedDict):
    path: str
    patch: str
    added: int
    removed: int
    language: str | None


class MemoryHit(TypedDict):
    id: str
    score: float
    payload: dict[str, Any]


class Pattern(TypedDict):
    name: str
    description: str
    confidence: float
    source_ids: list[str]


class FeedbackComment(TypedDict):
    path: str
    line: int
    side: str  # "LEFT" | "RIGHT"
    body: str
    severity: str  # "info" | "warn" | "block"


class ReviewState(TypedDict):
    repo_full_name: str
    pr_number: int
    head_sha: str
    diff: str | None
    files: list[FileDiff]
    memory_hits: list[MemoryHit]
    patterns: list[Pattern]
    feedback: list[FeedbackComment]
    published: bool
    errors: list[str]
