from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["dev", "staging", "prod", "test"]
CookieSameSite = Literal["lax", "strict", "none"]


class Settings(BaseSettings):
    """Application settings sourced from env vars and optional `.env` file.

    All secret values use `SecretStr` so they never appear in logs or repr output.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- core ---
    environment: Environment = "dev"
    log_level: str = "INFO"
    service_name: str = "lineage-api"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # --- postgres ---
    database_url: str = "postgresql+asyncpg://lineage:lineage@localhost:5432/lineage"
    database_pool_size: int = 10
    database_max_overflow: int = 20

    # --- redis / celery ---
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # --- qdrant ---
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: SecretStr | None = None
    qdrant_collection: str = "lineage_memory"

    # --- github app ---
    github_app_id: str | None = None
    github_app_client_id: str | None = None
    github_app_private_key: SecretStr | None = None
    github_app_private_key_path: str | None = None
    github_webhook_secret: SecretStr = Field(default=SecretStr("changeme"))

    # --- github oauth (user identity) ---
    github_oauth_client_id: str | None = None
    github_oauth_client_secret: SecretStr | None = None
    github_oauth_redirect_uri: str = "http://localhost:8000/auth/github/callback"
    github_oauth_scopes: str = "read:user user:email"
    github_oauth_authorize_url: str = "https://github.com/login/oauth/authorize"
    github_oauth_token_url: str = "https://github.com/login/oauth/access_token"
    github_api_base_url: str = "https://api.github.com"

    # --- jwt / sessions ---
    jwt_secret: SecretStr = Field(default=SecretStr("dev-insecure-secret-change-me-please-32+"))
    jwt_algorithm: Literal["HS256"] = "HS256"
    access_token_ttl_seconds: int = 15 * 60
    refresh_token_ttl_seconds: int = 30 * 24 * 3600

    # --- cookies ---
    cookie_domain: str | None = None
    cookie_secure: bool = True
    cookie_samesite: CookieSameSite = "lax"
    access_cookie_name: str = "access_token"
    refresh_cookie_name: str = "refresh_token"
    frontend_origin: str = "http://localhost:3000"
    post_login_redirect_path: str = "/"

    # --- cache ttls ---
    install_token_cache_ttl_seconds: int = 55 * 60
    pkce_state_ttl_seconds: int = 600

    # --- rate limit ---
    rate_limit_enabled: bool = True
    auth_rate_limit_per_minute: int = 30

    # --- google gemini ---
    google_api_key: SecretStr | None = None
    gemini_model: str = "gemini-2.5-flash-lite"
    embedding_model: str = "text-embedding-004"
    embedding_dim: int = 768
    gemini_request_timeout_s: float = 30.0
    gemini_max_output_tokens: int = 2048
    gemini_temperature: float = 0.2

    # --- observability ---
    sentry_dsn: str | None = None
    prometheus_enabled: bool = True

    @field_validator("log_level")
    @classmethod
    def _upper_log_level(cls, v: str) -> str:
        return v.upper()

    @field_validator("jwt_secret")
    @classmethod
    def _validate_jwt_secret(cls, v: SecretStr, info: ValidationInfo) -> SecretStr:
        env = info.data.get("environment", "dev")
        if env != "dev" and len(v.get_secret_value()) < 32:
            raise ValueError("jwt_secret must be at least 32 characters outside dev environment")
        return v

    @field_validator("cookie_samesite")
    @classmethod
    def _validate_samesite(cls, v: str, info: ValidationInfo) -> str:
        if v == "none" and not info.data.get("cookie_secure", True):
            raise ValueError("cookie_samesite='none' requires cookie_secure=True")
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
