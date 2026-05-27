from __future__ import annotations

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, SoftDeleteMixin, TimestampMixin, UUIDPKMixin

if TYPE_CHECKING:
    from src.models.pull_request import PullRequest


class UserRole(str, enum.Enum):
    member = "member"
    admin = "admin"


class UserPlan(str, enum.Enum):
    free = "free"
    pro = "pro"


class AccountType(str, enum.Enum):
    user = "user"
    org = "org"


class TargetType(str, enum.Enum):
    user = "user"
    organization = "organization"


class AuthEventType(str, enum.Enum):
    login_success = "login_success"
    login_failed = "login_failed"
    logout = "logout"
    refresh_success = "refresh_success"
    refresh_replay = "refresh_replay"
    install_created = "install_created"
    install_deleted = "install_deleted"
    install_suspended = "install_suspended"
    install_unsuspended = "install_unsuspended"


def _enum_values(cls: type[enum.Enum]) -> list[str]:
    return [e.value for e in cls]


class User(UUIDPKMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role", native_enum=False, length=32, validate_strings=True),
        default=UserRole.member,
        server_default=UserRole.member.value,
        nullable=False,
    )
    plan: Mapped[UserPlan] = mapped_column(
        SQLEnum(UserPlan, name="user_plan", native_enum=False, length=32, validate_strings=True),
        default=UserPlan.free,
        server_default=UserPlan.free.value,
        nullable=False,
    )

    identities: Mapped[list[GitHubIdentity]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    refresh_sessions: Mapped[list[RefreshSession]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(f"role IN ({', '.join(repr(v) for v in _enum_values(UserRole))})", name="ck_users_role"),
        CheckConstraint(f"plan IN ({', '.join(repr(v) for v in _enum_values(UserPlan))})", name="ck_users_plan"),
    )


class GitHubIdentity(UUIDPKMixin, Base):
    __tablename__ = "github_identities"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    github_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    github_login: Mapped[str] = mapped_column(String(255), nullable=False)
    primary_email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    scope: Mapped[str | None] = mapped_column(String(255), nullable=True)
    linked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped[User] = relationship(back_populates="identities")

    __table_args__ = (
        UniqueConstraint("user_id", "github_id", name="uq_github_identity_user_github"),
    )


class RefreshSession(UUIDPKMixin, Base):
    __tablename__ = "refresh_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    revoked_reason: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped[User] = relationship(back_populates="refresh_sessions")

    __table_args__ = (
        Index("ix_refresh_user_active", "user_id", "revoked", "expires_at"),
    )


class GitHubAppInstallation(UUIDPKMixin, Base):
    __tablename__ = "github_app_installations"

    installation_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    account_login: Mapped[str] = mapped_column(String(255), nullable=False)
    account_type: Mapped[AccountType] = mapped_column(
        SQLEnum(AccountType, name="account_type", native_enum=False, length=32, validate_strings=True),
        nullable=False,
    )
    target_type: Mapped[TargetType] = mapped_column(
        SQLEnum(TargetType, name="target_type", native_enum=False, length=32, validate_strings=True),
        nullable=False,
    )
    installed_by: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    suspended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    installed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    repositories: Mapped[list[Repository]] = relationship(
        back_populates="installation", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_install_account_login", "account_login"),
        CheckConstraint(
            f"account_type IN ({', '.join(repr(v) for v in _enum_values(AccountType))})",
            name="ck_install_account_type",
        ),
        CheckConstraint(
            f"target_type IN ({', '.join(repr(v) for v in _enum_values(TargetType))})",
            name="ck_install_target_type",
        ),
    )


class Repository(UUIDPKMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "repositories"

    installation_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("github_app_installations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    github_repo_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(512), unique=True, index=True, nullable=False)
    default_branch: Mapped[str | None] = mapped_column(String(255), nullable=True)
    private: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False)
    org_id: Mapped[uuid.UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True, index=True)

    installation: Mapped[GitHubAppInstallation | None] = relationship(back_populates="repositories")
    pull_requests: Mapped[list[PullRequest]] = relationship(
        back_populates="repository", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_repo_installation_active", "installation_id", "active"),
    )


class AuthEvent(UUIDPKMixin, Base):
    __tablename__ = "auth_events"

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    event_type: Mapped[AuthEventType] = mapped_column(
        SQLEnum(AuthEventType, name="auth_event_type", native_enum=False, length=32, validate_strings=True),
        nullable=False,
    )
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    event_metadata: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index("ix_authevent_user_time", "user_id", "created_at"),
        CheckConstraint(
            f"event_type IN ({', '.join(repr(v) for v in _enum_values(AuthEventType))})",
            name="ck_authevent_type",
        ),
    )
