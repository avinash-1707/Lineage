"""Append-only audit log for auth events."""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.auth import AuthEvent, AuthEventType
from src.observability.logging import get_logger

log = get_logger(__name__)


async def record(
    db: AsyncSession,
    *,
    event_type: AuthEventType,
    user_id: uuid.UUID | None = None,
    ip: str | None = None,
    user_agent: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> AuthEvent:
    row = AuthEvent(
        user_id=user_id,
        event_type=event_type,
        ip_address=ip,
        user_agent=user_agent,
        event_metadata=metadata,
    )
    db.add(row)
    await db.flush()
    log.info(
        "auth.event",
        event_type=event_type.value,
        user_id=str(user_id) if user_id else None,
        ip=ip,
        metadata=metadata,
    )
    return row
