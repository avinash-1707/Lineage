from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models.pull_request import PullRequest


class ReviewComment(Base):
    __tablename__ = "review_comments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    pull_request_id: Mapped[int] = mapped_column(
        ForeignKey("pull_requests.id", ondelete="CASCADE"), index=True
    )
    github_comment_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, nullable=True)
    path: Mapped[str] = mapped_column(String(1024))
    line: Mapped[int] = mapped_column(Integer)
    side: Mapped[str] = mapped_column(String(8), default="RIGHT")
    severity: Mapped[str] = mapped_column(String(16), default="info")
    body: Mapped[str] = mapped_column(Text)
    pattern_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    feedback_signal: Mapped[str | None] = mapped_column(
        String(32), nullable=True
    )  # accepted | dismissed | resolved | none
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    pull_request: Mapped["PullRequest"] = relationship(back_populates="review_comments")
