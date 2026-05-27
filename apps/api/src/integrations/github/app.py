"""GitHub App auth: JWT signing + installation access token exchange.

Pure GitHub I/O. No DB. No auth logic.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import httpx
import jwt
from pydantic import BaseModel, ConfigDict

from src.config import Settings

__all__ = [
    "GitHubAppError",
    "InstallationTokenResponse",
    "build_app_jwt",
    "fetch_installation_token",
    "load_private_key",
]


class GitHubAppError(Exception):
    def __init__(self, message: str, *, status_code: int | None = None, body: str | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class InstallationTokenResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    token: str
    expires_at: datetime
    permissions: dict[str, str] | None = None
    repository_selection: str | None = None


def load_private_key(settings: Settings) -> bytes:
    if settings.github_app_private_key_path:
        path = Path(settings.github_app_private_key_path)
        if not path.exists():
            raise GitHubAppError(f"github app private key file missing: {path}")
        return path.read_bytes()
    if settings.github_app_private_key is not None:
        return settings.github_app_private_key.get_secret_value().encode("utf-8")
    raise GitHubAppError("github_app_private_key or github_app_private_key_path must be configured")


def build_app_jwt(*, app_client_id: str, private_key_pem: bytes) -> str:
    now = int(datetime.now(UTC).timestamp())
    payload = {
        "iat": now - 60,
        "exp": now + 540,
        "iss": app_client_id,
    }
    return jwt.encode(payload, private_key_pem, algorithm="RS256")


async def fetch_installation_token(
    *,
    app_jwt: str,
    installation_id: int,
    http: httpx.AsyncClient,
    api_base_url: str = "https://api.github.com",
) -> InstallationTokenResponse:
    url = f"{api_base_url.rstrip('/')}/app/installations/{installation_id}/access_tokens"
    headers = {
        "Authorization": f"Bearer {app_jwt}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    resp = await http.post(url, headers=headers, timeout=10.0)
    if resp.status_code != 201:
        raise GitHubAppError(
            f"installation token request failed for installation {installation_id}",
            status_code=resp.status_code,
            body=resp.text,
        )
    return InstallationTokenResponse.model_validate(resp.json())
