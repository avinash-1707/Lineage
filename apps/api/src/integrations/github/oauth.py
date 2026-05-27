"""GitHub OAuth identity flow. Only network I/O — no DB, no auth logic."""

from __future__ import annotations

from urllib.parse import urlencode

import httpx
from pydantic import BaseModel, ConfigDict

__all__ = [
    "GitHubOAuthClient",
    "GitHubOAuthError",
    "GitHubUserEmail",
    "GitHubUserProfile",
    "OAuthTokenResponse",
]


class GitHubOAuthError(Exception):
    def __init__(self, message: str, *, status_code: int | None = None, body: str | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class OAuthTokenResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    access_token: str
    token_type: str
    scope: str | None = None


class GitHubUserProfile(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    login: str
    name: str | None = None
    avatar_url: str | None = None
    email: str | None = None


class GitHubUserEmail(BaseModel):
    model_config = ConfigDict(extra="ignore")

    email: str
    primary: bool
    verified: bool
    visibility: str | None = None


class GitHubOAuthClient:
    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: str,
        authorize_url: str,
        token_url: str,
        api_base_url: str,
        http: httpx.AsyncClient | None = None,
    ) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._scopes = scopes
        self._authorize_url = authorize_url
        self._token_url = token_url
        self._api_base_url = api_base_url.rstrip("/")
        self._http = http

    def build_authorize_url(self, *, state: str, code_challenge: str) -> str:
        params = {
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "scope": self._scopes,
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "allow_signup": "true",
        }
        return f"{self._authorize_url}?{urlencode(params)}"

    async def exchange_code(self, *, code: str, code_verifier: str) -> OAuthTokenResponse:
        payload = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "code": code,
            "redirect_uri": self._redirect_uri,
            "code_verifier": code_verifier,
        }
        async with self._client() as http:
            resp = await http.post(
                self._token_url,
                data=payload,
                headers={"Accept": "application/json"},
                timeout=10.0,
            )
        if resp.status_code != 200:
            raise GitHubOAuthError(
                "token exchange failed",
                status_code=resp.status_code,
                body=resp.text,
            )
        data = resp.json()
        if "error" in data:
            raise GitHubOAuthError(
                f"token exchange error: {data.get('error')}",
                status_code=resp.status_code,
                body=resp.text,
            )
        return OAuthTokenResponse.model_validate(data)

    async def fetch_user_profile(self, access_token: str) -> GitHubUserProfile:
        async with self._client() as http:
            resp = await http.get(
                f"{self._api_base_url}/user",
                headers=self._user_headers(access_token),
                timeout=10.0,
            )
        if resp.status_code != 200:
            raise GitHubOAuthError(
                "user profile fetch failed",
                status_code=resp.status_code,
                body=resp.text,
            )
        return GitHubUserProfile.model_validate(resp.json())

    async def fetch_primary_email(self, access_token: str) -> str:
        async with self._client() as http:
            resp = await http.get(
                f"{self._api_base_url}/user/emails",
                headers=self._user_headers(access_token),
                timeout=10.0,
            )
        if resp.status_code != 200:
            raise GitHubOAuthError(
                "user emails fetch failed",
                status_code=resp.status_code,
                body=resp.text,
            )
        emails = [GitHubUserEmail.model_validate(e) for e in resp.json()]
        for e in emails:
            if e.primary and e.verified:
                return e.email
        for e in emails:
            if e.verified:
                return e.email
        raise GitHubOAuthError("no verified email available")

    @staticmethod
    def _user_headers(access_token: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _client(self) -> httpx.AsyncClient:
        if self._http is not None:
            return _BorrowedClient(self._http)
        return httpx.AsyncClient()


class _BorrowedClient:
    """Async context wrapper that yields a shared httpx client without closing it."""

    def __init__(self, http: httpx.AsyncClient) -> None:
        self._http = http

    async def __aenter__(self) -> httpx.AsyncClient:
        return self._http

    async def __aexit__(self, *args: object) -> None:
        return None
