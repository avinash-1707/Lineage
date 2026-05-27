"""Auth endpoints. Thin — delegates to auth_service."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import Settings, get_settings
from src.core.dependencies import get_current_user, get_db
from src.core.rate_limit import rate_limit
from src.core.redis import get_redis
from src.core.security import (
    TokenExpiredError,
    TokenInvalidError,
    TokenReplayError,
    generate_oauth_state,
    generate_pkce_pair,
)
from src.integrations.github.oauth import GitHubOAuthClient, GitHubOAuthError
from src.models.auth import AuthEventType, User
from src.observability.logging import get_logger
from src.schemas.auth import UserMe
from src.services import audit_service, auth_service
from src.services.auth_service import SessionTokens

router = APIRouter()
log = get_logger(__name__)

PKCE_KEY_PREFIX = "oauth:pkce"


def _oauth_client(settings: Settings) -> GitHubOAuthClient:
    if not settings.github_oauth_client_id or settings.github_oauth_client_secret is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="github oauth not configured",
        )
    return GitHubOAuthClient(
        client_id=settings.github_oauth_client_id,
        client_secret=settings.github_oauth_client_secret.get_secret_value(),
        redirect_uri=settings.github_oauth_redirect_uri,
        scopes=settings.github_oauth_scopes,
        authorize_url=settings.github_oauth_authorize_url,
        token_url=settings.github_oauth_token_url,
        api_base_url=settings.github_api_base_url,
    )


def _set_session_cookies(
    response: Response,
    tokens: SessionTokens,
    settings: Settings,
) -> None:
    response.set_cookie(
        key=settings.access_cookie_name,
        value=tokens.access_token,
        max_age=settings.access_token_ttl_seconds,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain,
        path="/",
    )
    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=tokens.refresh_token,
        max_age=settings.refresh_token_ttl_seconds,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain,
        path="/",
    )


def _clear_session_cookies(response: Response, settings: Settings) -> None:
    response.delete_cookie(
        settings.access_cookie_name,
        domain=settings.cookie_domain,
        path="/",
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        httponly=True,
    )
    response.delete_cookie(
        settings.refresh_cookie_name,
        domain=settings.cookie_domain,
        path="/",
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        httponly=True,
    )


def _client_ip(request: Request) -> str | None:
    if request.client is None:
        return None
    return request.client.host


@router.get(
    "/github/login",
    dependencies=[Depends(rate_limit("auth_login"))],
)
async def github_login(
    redis: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
) -> RedirectResponse:
    client = _oauth_client(settings)
    state = generate_oauth_state()
    verifier, challenge = generate_pkce_pair()
    await redis.setex(
        f"{PKCE_KEY_PREFIX}:{state}",
        settings.pkce_state_ttl_seconds,
        verifier,
    )
    url = client.build_authorize_url(state=state, code_challenge=challenge)
    return RedirectResponse(url=url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@router.get("/github/callback")
async def github_callback(
    request: Request,
    code: str,
    state: str,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> RedirectResponse:
    verifier = await redis.getdel(f"{PKCE_KEY_PREFIX}:{state}")
    if not verifier:
        await audit_service.record(
            db,
            event_type=AuthEventType.login_failed,
            ip=_client_ip(request),
            user_agent=request.headers.get("user-agent"),
            metadata={"reason": "pkce_state_missing_or_expired"},
        )
        await db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid or expired state")

    client = _oauth_client(settings)
    try:
        token_resp = await client.exchange_code(code=code, code_verifier=verifier)
        profile = await client.fetch_user_profile(token_resp.access_token)
        primary_email = profile.email or await client.fetch_primary_email(token_resp.access_token)
    except GitHubOAuthError as exc:
        await audit_service.record(
            db,
            event_type=AuthEventType.login_failed,
            ip=_client_ip(request),
            user_agent=request.headers.get("user-agent"),
            metadata={"reason": "github_oauth_error", "status": exc.status_code},
        )
        await db.commit()
        log.warning("auth.oauth_error", status=exc.status_code, body=exc.body)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="github oauth failed") from exc

    user = await auth_service.upsert_user_from_github(
        db,
        profile=profile,
        primary_email=primary_email,
        scope=token_resp.scope,
    )
    tokens = await auth_service.issue_session(
        db,
        user=user,
        settings=settings,
        ip=_client_ip(request),
        user_agent=request.headers.get("user-agent"),
    )
    await db.commit()

    redirect_url = settings.frontend_origin.rstrip("/") + settings.post_login_redirect_path
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    _set_session_cookies(response, tokens, settings)
    return response


@router.post(
    "/refresh",
    dependencies=[Depends(rate_limit("auth_refresh"))],
)
async def refresh(
    request: Request,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> Response:
    token = request.cookies.get(settings.refresh_cookie_name)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="no refresh token")

    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    try:
        tokens = await auth_service.rotate_refresh(
            db,
            refresh_token=token,
            settings=settings,
            ip=_client_ip(request),
            user_agent=request.headers.get("user-agent"),
        )
        await db.commit()
    except TokenReplayError as exc:
        await db.commit()
        _clear_session_cookies(response, settings)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="replay detected") from exc
    except TokenExpiredError as exc:
        await db.commit()
        _clear_session_cookies(response, settings)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh expired") from exc
    except TokenInvalidError as exc:
        await db.commit()
        _clear_session_cookies(response, settings)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid refresh") from exc

    _set_session_cookies(response, tokens, settings)
    return response


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> Response:
    token = request.cookies.get(settings.refresh_cookie_name)
    if token:
        await auth_service.revoke_session(
            db,
            refresh_token=token,
            ip=_client_ip(request),
            user_agent=request.headers.get("user-agent"),
        )
        await db.commit()
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    _clear_session_cookies(response, settings)
    return response


@router.get("/me", response_model=UserMe)
async def me(user: User = Depends(get_current_user)) -> UserMe:
    return UserMe.model_validate(user)
