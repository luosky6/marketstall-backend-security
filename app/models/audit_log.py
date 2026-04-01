"""Database model for audit logs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class AuditLog:
    """Lightweight audit log model used before ORM integration."""

    id: int
    user_id: int | None
    action: str
    target_type: str | None
    target_id: int | str | None
    status: str
    message: str | None
    created_at: datetime

    @staticmethod
    def now_utc() -> datetime:
        """Return a timezone-aware UTC timestamp for consistent audit records."""
        return datetime.now(timezone.utc)
