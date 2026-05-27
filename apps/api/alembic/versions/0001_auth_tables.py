"""Initial schema: auth + repositories + review pipeline.

Revision ID: 0001_auth_tables
Revises:
Create Date: 2026-05-27
"""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "0001_auth_tables"
down_revision = None
branch_labels = None
depends_on = None


USER_ROLE_VALUES = ("member", "admin")
USER_PLAN_VALUES = ("free", "pro")
ACCOUNT_TYPE_VALUES = ("user", "org")
TARGET_TYPE_VALUES = ("user", "organization")
AUTH_EVENT_VALUES = (
    "login_success",
    "login_failed",
    "logout",
    "refresh_success",
    "refresh_replay",
    "install_created",
    "install_deleted",
    "install_suspended",
    "install_unsuspended",
)


def _in_clause(col: str, values: tuple[str, ...]) -> str:
    rendered = ", ".join(f"'{v}'" for v in values)
    return f"{col} IN ({rendered})"


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    # --- users ---
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("name", sa.String(255), nullable=True),
        sa.Column("avatar_url", sa.String(1024), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("role", sa.String(32), nullable=False, server_default="member"),
        sa.Column("plan", sa.String(32), nullable=False, server_default="free"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(_in_clause("role", USER_ROLE_VALUES), name="ck_users_role"),
        sa.CheckConstraint(_in_clause("plan", USER_PLAN_VALUES), name="ck_users_plan"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # --- github_identities ---
    op.create_table(
        "github_identities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("github_id", sa.BigInteger, nullable=False),
        sa.Column("github_login", sa.String(255), nullable=False),
        sa.Column("primary_email", sa.String(320), nullable=True),
        sa.Column("scope", sa.String(255), nullable=True),
        sa.Column("linked_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "github_id", name="uq_github_identity_user_github"),
    )
    op.create_index("ix_github_identities_user_id", "github_identities", ["user_id"])
    op.create_index("ix_github_identities_github_id", "github_identities", ["github_id"], unique=True)

    # --- refresh_sessions ---
    op.create_table(
        "refresh_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("revoked_reason", sa.String(64), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("token_hash", name="uq_refresh_sessions_token_hash"),
    )
    op.create_index("ix_refresh_sessions_user_id", "refresh_sessions", ["user_id"])
    op.create_index("ix_refresh_user_active", "refresh_sessions", ["user_id", "revoked", "expires_at"])

    # --- github_app_installations ---
    op.create_table(
        "github_app_installations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("installation_id", sa.BigInteger, nullable=False),
        sa.Column("account_login", sa.String(255), nullable=False),
        sa.Column("account_type", sa.String(32), nullable=False),
        sa.Column("target_type", sa.String(32), nullable=False),
        sa.Column(
            "installed_by",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("suspended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("installed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(_in_clause("account_type", ACCOUNT_TYPE_VALUES), name="ck_install_account_type"),
        sa.CheckConstraint(_in_clause("target_type", TARGET_TYPE_VALUES), name="ck_install_target_type"),
    )
    op.create_index("ix_github_app_installations_installation_id", "github_app_installations", ["installation_id"], unique=True)
    op.create_index("ix_github_app_installations_installed_by", "github_app_installations", ["installed_by"])
    op.create_index("ix_install_account_login", "github_app_installations", ["account_login"])

    # --- repositories (replaces legacy) ---
    op.create_table(
        "repositories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column(
            "installation_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("github_app_installations.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("github_repo_id", sa.BigInteger, nullable=False),
        sa.Column("owner", sa.String(255), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(512), nullable=False),
        sa.Column("default_branch", sa.String(255), nullable=True),
        sa.Column("private", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("org_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_repositories_installation_id", "repositories", ["installation_id"])
    op.create_index("ix_repositories_github_repo_id", "repositories", ["github_repo_id"], unique=True)
    op.create_index("ix_repositories_full_name", "repositories", ["full_name"], unique=True)
    op.create_index("ix_repositories_org_id", "repositories", ["org_id"])
    op.create_index("ix_repo_installation_active", "repositories", ["installation_id", "active"])

    # --- pull_requests (FK to repositories now UUID) ---
    op.create_table(
        "pull_requests",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(
            "repository_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("repositories.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("number", sa.Integer, nullable=False),
        sa.Column("title", sa.String(512), nullable=False),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("head_sha", sa.String(64), nullable=False),
        sa.Column("base_ref", sa.String(255), nullable=False),
        sa.Column("author_login", sa.String(255), nullable=True),
        sa.Column("last_reviewed_sha", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_pull_requests_repository_id", "pull_requests", ["repository_id"])
    op.create_index("ix_pull_requests_number", "pull_requests", ["number"])
    op.create_index("ix_pull_requests_state", "pull_requests", ["state"])
    op.create_index("ix_pull_requests_head_sha", "pull_requests", ["head_sha"])

    # --- review_comments (unchanged from prior design) ---
    op.create_table(
        "review_comments",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(
            "pull_request_id",
            sa.BigInteger,
            sa.ForeignKey("pull_requests.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("github_comment_id", sa.BigInteger, nullable=True),
        sa.Column("path", sa.String(1024), nullable=False),
        sa.Column("line", sa.Integer, nullable=False),
        sa.Column("side", sa.String(8), nullable=False, server_default="RIGHT"),
        sa.Column("severity", sa.String(16), nullable=False, server_default="info"),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("pattern_label", sa.String(255), nullable=True),
        sa.Column("feedback_signal", sa.String(32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("github_comment_id", name="uq_review_comments_github_comment_id"),
    )
    op.create_index("ix_review_comments_pull_request_id", "review_comments", ["pull_request_id"])

    # --- auth_events ---
    op.create_table(
        "auth_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("event_type", sa.String(32), nullable=False),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.Text, nullable=True),
        sa.Column("event_metadata", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(_in_clause("event_type", AUTH_EVENT_VALUES), name="ck_authevent_type"),
    )
    op.create_index("ix_authevent_user_time", "auth_events", ["user_id", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_authevent_user_time", table_name="auth_events")
    op.drop_table("auth_events")

    op.drop_index("ix_review_comments_pull_request_id", table_name="review_comments")
    op.drop_table("review_comments")

    op.drop_index("ix_pull_requests_head_sha", table_name="pull_requests")
    op.drop_index("ix_pull_requests_state", table_name="pull_requests")
    op.drop_index("ix_pull_requests_number", table_name="pull_requests")
    op.drop_index("ix_pull_requests_repository_id", table_name="pull_requests")
    op.drop_table("pull_requests")

    op.drop_index("ix_repo_installation_active", table_name="repositories")
    op.drop_index("ix_repositories_org_id", table_name="repositories")
    op.drop_index("ix_repositories_full_name", table_name="repositories")
    op.drop_index("ix_repositories_github_repo_id", table_name="repositories")
    op.drop_index("ix_repositories_installation_id", table_name="repositories")
    op.drop_table("repositories")

    op.drop_index("ix_install_account_login", table_name="github_app_installations")
    op.drop_index("ix_github_app_installations_installed_by", table_name="github_app_installations")
    op.drop_index("ix_github_app_installations_installation_id", table_name="github_app_installations")
    op.drop_table("github_app_installations")

    op.drop_index("ix_refresh_user_active", table_name="refresh_sessions")
    op.drop_index("ix_refresh_sessions_user_id", table_name="refresh_sessions")
    op.drop_table("refresh_sessions")

    op.drop_index("ix_github_identities_github_id", table_name="github_identities")
    op.drop_index("ix_github_identities_user_id", table_name="github_identities")
    op.drop_table("github_identities")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
