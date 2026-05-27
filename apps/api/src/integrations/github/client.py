"""Thin GitHub REST client.

Scope is intentionally narrow: fetch a PR's unified diff, post a review.
Auth is pluggable via `token_provider` so the LangGraph nodes don't need to
know about GitHub App installation tokens, PATs, or test fixtures.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from types import TracebackType
from typing import Any

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.config import Settings, get_settings
from src.observability.logging import get_logger

log = get_logger(__name__)

GITHUB_API = "https://api.github.com"

TokenProvider = Callable[[str], Awaitable[str | None]]


async def _no_token(_repo_full_name: str) -> str | None:
    return None


class GitHubError(RuntimeError):
    """Wraps a non-2xx GitHub API response."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(f"GitHub API {status}: {message}")
        self.status = status


def _retryable(exc: BaseException) -> bool:
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in {429, 500, 502, 503, 504}
    return isinstance(exc, httpx.TransportError)


class GitHubClient:
    """Async GitHub API client. Use as `async with GitHubClient() as gh: ...`."""

    def __init__(
        self,
        *,
        token_provider: TokenProvider = _no_token,
        settings: Settings | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._settings = settings or get_settings()
        self._token_provider = token_provider
        self._client = client or httpx.AsyncClient(
            base_url=GITHUB_API,
            timeout=httpx.Timeout(20.0, connect=5.0),
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": f"{self._settings.service_name}/0.1",
            },
        )
        self._owns_client = client is None

    async def __aenter__(self) -> "GitHubClient":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def _headers(self, repo_full_name: str, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers: dict[str, str] = {}
        token = await self._token_provider(repo_full_name)
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if extra:
            headers.update(extra)
        return headers

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=10),
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TransportError)),
    )
    async def fetch_pr_diff(self, repo_full_name: str, pr_number: int) -> str:
        headers = await self._headers(repo_full_name, {"Accept": "application/vnd.github.v3.diff"})
        r = await self._client.get(f"/repos/{repo_full_name}/pulls/{pr_number}", headers=headers)
        if not _retryable_or_ok(r):
            raise GitHubError(r.status_code, r.text)
        r.raise_for_status()
        return r.text

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=10),
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TransportError)),
    )
    async def publish_review(
        self,
        repo_full_name: str,
        pr_number: int,
        commit_sha: str,
        comments: list[dict[str, Any]],
        body: str = "Lineage review",
    ) -> dict[str, Any]:
        if not comments:
            log.info("github.publish_review.skip", reason="no_comments")
            return {"skipped": True}

        payload = {
            "commit_id": commit_sha,
            "body": body,
            "event": "COMMENT",
            "comments": [
                {
                    "path": c["path"],
                    "line": int(c["line"]),
                    "side": c.get("side", "RIGHT"),
                    "body": c["body"],
                }
                for c in comments
            ],
        }
        headers = await self._headers(repo_full_name)
        r = await self._client.post(
            f"/repos/{repo_full_name}/pulls/{pr_number}/reviews",
            headers=headers,
            json=payload,
        )
        if not _retryable_or_ok(r):
            raise GitHubError(r.status_code, r.text)
        r.raise_for_status()
        return r.json()


def _retryable_or_ok(r: httpx.Response) -> bool:
    """Treat non-retryable 4xx as fatal — don't waste retry budget on them."""
    if r.is_success:
        return True
    if r.status_code in {429, 500, 502, 503, 504}:
        return True
    return False
