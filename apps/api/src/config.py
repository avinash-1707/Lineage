from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["dev", "staging", "prod", "test"]


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
    github_app_private_key: SecretStr | None = None
    github_webhook_secret: SecretStr = Field(default=SecretStr("changeme"))

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


@lru_cache
def get_settings() -> Settings:
    return Settings()
