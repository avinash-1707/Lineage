"""FastAPI dependency wiring: get_db, get_current_user, require_role."""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import Settings, get_settings
from src.core.security import (
    TokenExpiredError,
    TokenInvalidError,
    decode_access_token,
)
from src.database import get_session
from src.models.auth import User, UserRole
from src.services import auth_service

__all__ = [
    "get_current_user",
    "get_db",
    "get_optional_user",
    "require_role",
]

get_db = get_session


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> User:
    token = request.cookies.get(settings.access_cookie_name)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated")
    try:
        claims = decode_access_token(
            token,
            secret=settings.jwt_secret.get_secret_value(),
            algorithm=settings.jwt_algorithm,
        )
    except TokenExpiredError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired") from exc
    except TokenInvalidError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token") from exc

    user = await auth_service.get_user_by_id(db, claims.sub)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user inactive")
    return user


async def get_optional_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> User | None:
    token = request.cookies.get(settings.access_cookie_name)
    if not token:
        return None
    try:
        claims = decode_access_token(
            token,
            secret=settings.jwt_secret.get_secret_value(),
            algorithm=settings.jwt_algorithm,
        )
    except (TokenExpiredError, TokenInvalidError):
        return None
    return await auth_service.get_user_by_id(db, claims.sub)


def require_role(*allowed: UserRole) -> Callable[..., Awaitable[User]]:
    allowed_values = frozenset(r.value for r in allowed)

    async def _check(user: User = Depends(get_current_user)) -> User:
        if user.role.value not in allowed_values:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="forbidden")
        return user

    return _check
