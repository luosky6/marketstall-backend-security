"""Pydantic schemas for audit log payloads."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class AuditLogCreate(BaseModel):
    """Schema for creating an audit log event."""

    user_id: int | None
    action: str
    target_type: str | None = None
    target_id: int | str | None = None
    status: str
    message: str | None = None


class AuditLogRead(AuditLogCreate):
    """Schema returned to API consumers."""

    id: int
    created_at: datetime
