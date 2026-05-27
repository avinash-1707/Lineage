"""Pure crypto + token primitives. No DB, no HTTP, no FastAPI deps."""

from __future__ import annotations

import base64
import hashlib
import secrets
import uuid
from datetime import UTC, datetime

import jwt
from pydantic import BaseModel, Field

__all__ = [
    "AccessTokenClaims",
    "AuthError",
    "RoleDeniedError",
    "TokenExpiredError",
    "TokenInvalidError",
    "TokenReplayError",
    "create_access_token",
    "decode_access_token",
    "generate_oauth_state",
    "generate_pkce_pair",
    "generate_refresh_token",
    "hash_refresh_token",
]


class AuthError(Exception):
    pass


class TokenReplayError(AuthError):
    pass


class TokenExpiredError(AuthError):
    pass


class TokenInvalidError(AuthError):
    pass


class RoleDeniedError(AuthError):
    pass


class AccessTokenClaims(BaseModel):
    sub: uuid.UUID = Field(..., description="user id")
    gh: int = Field(..., description="github user id")
    exp: int
    iat: int
    type: str = "access"


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def generate_oauth_state() -> str:
    return secrets.token_urlsafe(32)


def generate_pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)[:128]
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return verifier, challenge


def create_access_token(
    *,
    user_id: uuid.UUID,
    github_id: int,
    ttl_seconds: int,
    secret: str,
    algorithm: str = "HS256",
) -> str:
    now = int(datetime.now(UTC).timestamp())
    payload = {
        "sub": str(user_id),
        "gh": github_id,
        "iat": now,
        "exp": now + ttl_seconds,
        "type": "access",
    }
    return jwt.encode(payload, secret, algorithm=algorithm)


def decode_access_token(
    token: str,
    *,
    secret: str,
    algorithm: str = "HS256",
) -> AccessTokenClaims:
    try:
        raw = jwt.decode(token, secret, algorithms=[algorithm])
    except jwt.ExpiredSignatureError as exc:
        raise TokenExpiredError(str(exc)) from exc
    except jwt.InvalidTokenError as exc:
        raise TokenInvalidError(str(exc)) from exc

    if raw.get("type") != "access":
        raise TokenInvalidError("wrong token type")
    return AccessTokenClaims.model_validate(raw)
