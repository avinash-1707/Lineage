"""All auth business logic. No HTTP objects; takes AsyncSession + plain args."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import Settings
from src.core.security import (
    TokenExpiredError,
    TokenInvalidError,
    TokenReplayError,
    create_access_token,
    generate_refresh_token,
    hash_refresh_token,
)
from src.integrations.github.oauth import GitHubUserProfile
from src.models.auth import (
    AccountType,
    AuthEventType,
    GitHubAppInstallation,
    GitHubIdentity,
    RefreshSession,
    Repository,
    TargetType,
    User,
)
from src.observability.logging import get_logger
from src.schemas.auth import InstallationEventPayload
from src.services import audit_service

log = get_logger(__name__)

__all__ = [
    "SessionTokens",
    "get_user_by_id",
    "handle_installation_event",
    "issue_session",
    "revoke_all_user_sessions",
    "revoke_session",
    "rotate_refresh",
    "upsert_user_from_github",
]


class SessionTokens(BaseModel):
    access_token: str
    refresh_token: str
    access_expires_at: datetime
    refresh_expires_at: datetime
    user: User

    model_config = {"arbitrary_types_allowed": True}


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    row = (
        await db.execute(
            select(User).where(User.id == user_id, User.deleted_at.is_(None), User.is_active.is_(True))
        )
    ).scalar_one_or_none()
    return row


async def upsert_user_from_github(
    db: AsyncSession,
    *,
    profile: GitHubUserProfile,
    primary_email: str,
    scope: str | None = None,
) -> User:
    identity = (
        await db.execute(
            select(GitHubIdentity).where(GitHubIdentity.github_id == profile.id)
        )
    ).scalar_one_or_none()

    if identity is not None:
        user = (
            await db.execute(select(User).where(User.id == identity.user_id))
        ).scalar_one()
        user.name = profile.name or user.name
        user.avatar_url = profile.avatar_url or user.avatar_url
        user.email = primary_email
        if user.deleted_at is not None:
            user.deleted_at = None
        if not user.is_active:
            user.is_active = True
        identity.github_login = profile.login
        identity.primary_email = primary_email
        if scope is not None:
            identity.scope = scope
        await db.flush()
        return user

    existing_by_email = (
        await db.execute(select(User).where(User.email == primary_email))
    ).scalar_one_or_none()
    if existing_by_email is not None:
        user = existing_by_email
        user.name = profile.name or user.name
        user.avatar_url = profile.avatar_url or user.avatar_url
        if user.deleted_at is not None:
            user.deleted_at = None
        if not user.is_active:
            user.is_active = True
    else:
        user = User(
            email=primary_email,
            name=profile.name,
            avatar_url=profile.avatar_url,
        )
        db.add(user)
        await db.flush()

    db.add(
        GitHubIdentity(
            user_id=user.id,
            github_id=profile.id,
            github_login=profile.login,
            primary_email=primary_email,
            scope=scope,
        )
    )
    await db.flush()
    return user


async def issue_session(
    db: AsyncSession,
    *,
    user: User,
    settings: Settings,
    ip: str | None,
    user_agent: str | None,
) -> SessionTokens:
    refresh_token = generate_refresh_token()
    token_hash = hash_refresh_token(refresh_token)
    now = datetime.now(UTC)
    refresh_expires = now + timedelta(seconds=settings.refresh_token_ttl_seconds)
    access_expires = now + timedelta(seconds=settings.access_token_ttl_seconds)

    identity_row = (
        await db.execute(
            select(GitHubIdentity)
            .where(GitHubIdentity.user_id == user.id)
            .order_by(GitHubIdentity.linked_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
    github_id = identity_row.github_id if identity_row is not None else 0

    session = RefreshSession(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=refresh_expires,
        ip_address=ip,
        user_agent=user_agent,
    )
    db.add(session)
    await db.flush()

    access_token = create_access_token(
        user_id=user.id,
        github_id=github_id,
        ttl_seconds=settings.access_token_ttl_seconds,
        secret=settings.jwt_secret.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )

    await audit_service.record(
        db,
        event_type=AuthEventType.login_success,
        user_id=user.id,
        ip=ip,
        user_agent=user_agent,
        metadata={"session_id": str(session.id)},
    )

    return SessionTokens(
        access_token=access_token,
        refresh_token=refresh_token,
        access_expires_at=access_expires,
        refresh_expires_at=refresh_expires,
        user=user,
    )


async def revoke_all_user_sessions(
    db: AsyncSession,
    *,
    user_id: uuid.UUID,
    reason: str,
) -> int:
    result = await db.execute(
        update(RefreshSession)
        .where(
            RefreshSession.user_id == user_id,
            RefreshSession.revoked.is_(False),
        )
        .values(revoked=True, revoked_reason=reason)
    )
    return int(result.rowcount or 0)


async def rotate_refresh(
    db: AsyncSession,
    *,
    refresh_token: str,
    settings: Settings,
    ip: str | None,
    user_agent: str | None,
) -> SessionTokens:
    token_hash = hash_refresh_token(refresh_token)
    session = (
        await db.execute(select(RefreshSession).where(RefreshSession.token_hash == token_hash))
    ).scalar_one_or_none()

    if session is None:
        raise TokenInvalidError("refresh token not found")

    now = datetime.now(UTC)

    if session.used_at is not None:
        revoked_count = await revoke_all_user_sessions(
            db, user_id=session.user_id, reason="replay_detected"
        )
        await audit_service.record(
            db,
            event_type=AuthEventType.refresh_replay,
            user_id=session.user_id,
            ip=ip,
            user_agent=user_agent,
            metadata={"revoked_session_count": revoked_count},
        )
        raise TokenReplayError("refresh token replay detected")

    if session.revoked:
        raise TokenInvalidError("refresh token revoked")

    if session.expires_at <= now:
        raise TokenExpiredError("refresh token expired")

    session.used_at = now
    session.revoked = True
    session.revoked_reason = "rotated"
    await db.flush()

    user = (
        await db.execute(
            select(User).where(
                User.id == session.user_id,
                User.deleted_at.is_(None),
                User.is_active.is_(True),
            )
        )
    ).scalar_one_or_none()
    if user is None:
        raise TokenInvalidError("user inactive or deleted")

    tokens = await issue_session(
        db, user=user, settings=settings, ip=ip, user_agent=user_agent
    )
    await audit_service.record(
        db,
        event_type=AuthEventType.refresh_success,
        user_id=user.id,
        ip=ip,
        user_agent=user_agent,
        metadata={"rotated_from": str(session.id)},
    )
    return tokens


async def revoke_session(
    db: AsyncSession,
    *,
    refresh_token: str,
    ip: str | None = None,
    user_agent: str | None = None,
) -> None:
    token_hash = hash_refresh_token(refresh_token)
    session = (
        await db.execute(select(RefreshSession).where(RefreshSession.token_hash == token_hash))
    ).scalar_one_or_none()
    if session is None:
        return
    if not session.revoked:
        session.revoked = True
        session.revoked_reason = "logout"
        await db.flush()
    await audit_service.record(
        db,
        event_type=AuthEventType.logout,
        user_id=session.user_id,
        ip=ip,
        user_agent=user_agent,
    )


def _map_account_type(value: str) -> AccountType:
    return AccountType.org if value.lower() == "organization" else AccountType.user


def _map_target_type(value: str) -> TargetType:
    return TargetType.organization if value.lower() == "organization" else TargetType.user


async def _sync_installation_repositories(
    db: AsyncSession,
    *,
    installation: GitHubAppInstallation,
    payload: InstallationEventPayload,
) -> None:
    for repo in payload.repositories:
        owner_login, _, repo_name = repo.full_name.partition("/")
        existing = (
            await db.execute(
                select(Repository).where(Repository.github_repo_id == repo.id)
            )
        ).scalar_one_or_none()
        if existing is None:
            db.add(
                Repository(
                    installation_id=installation.id,
                    github_repo_id=repo.id,
                    owner=owner_login or payload.installation.account.login,
                    name=repo_name or repo.name,
                    full_name=repo.full_name,
                    private=repo.private,
                    active=True,
                )
            )
        else:
            existing.installation_id = installation.id
            existing.owner = owner_login or existing.owner
            existing.name = repo_name or existing.name
            existing.full_name = repo.full_name
            existing.private = repo.private
            existing.active = True
            existing.deleted_at = None
    await db.flush()


async def handle_installation_event(
    db: AsyncSession,
    payload: InstallationEventPayload,
    *,
    actor_user_id: uuid.UUID | None = None,
) -> None:
    inst_row = (
        await db.execute(
            select(GitHubAppInstallation).where(
                GitHubAppInstallation.installation_id == payload.installation.id
            )
        )
    ).scalar_one_or_none()

    now = datetime.now(UTC)
    account_type = _map_account_type(payload.installation.account.type)
    target_type = _map_target_type(payload.installation.target_type)

    if payload.action == "created":
        if inst_row is None:
            inst_row = GitHubAppInstallation(
                installation_id=payload.installation.id,
                account_login=payload.installation.account.login,
                account_type=account_type,
                target_type=target_type,
                installed_by=actor_user_id,
            )
            db.add(inst_row)
            await db.flush()
        else:
            inst_row.account_login = payload.installation.account.login
            inst_row.account_type = account_type
            inst_row.target_type = target_type
            inst_row.revoked_at = None
            inst_row.suspended_at = None
            await db.flush()
        await _sync_installation_repositories(db, installation=inst_row, payload=payload)
        await audit_service.record(
            db,
            event_type=AuthEventType.install_created,
            user_id=inst_row.installed_by,
            metadata={"installation_id": payload.installation.id, "account": payload.installation.account.login},
        )
        return

    if inst_row is None:
        log.warning(
            "auth.installation_event_unknown",
            action=payload.action,
            installation_id=payload.installation.id,
        )
        return

    if payload.action == "deleted":
        inst_row.revoked_at = now
        await db.flush()
        if inst_row.installed_by is not None:
            await revoke_all_user_sessions(
                db, user_id=inst_row.installed_by, reason="installation_deleted"
            )
        await audit_service.record(
            db,
            event_type=AuthEventType.install_deleted,
            user_id=inst_row.installed_by,
            metadata={"installation_id": payload.installation.id},
        )
        return

    if payload.action == "suspend":
        inst_row.suspended_at = now
        await db.flush()
        if inst_row.installed_by is not None:
            await revoke_all_user_sessions(
                db, user_id=inst_row.installed_by, reason="installation_suspended"
            )
        await audit_service.record(
            db,
            event_type=AuthEventType.install_suspended,
            user_id=inst_row.installed_by,
            metadata={"installation_id": payload.installation.id},
        )
        return

    if payload.action == "unsuspend":
        inst_row.suspended_at = None
        await db.flush()
        await audit_service.record(
            db,
            event_type=AuthEventType.install_unsuspended,
            user_id=inst_row.installed_by,
            metadata={"installation_id": payload.installation.id},
        )
        return

    log.info(
        "auth.installation_event_noop",
        action=payload.action,
        installation_id=payload.installation.id,
    )
