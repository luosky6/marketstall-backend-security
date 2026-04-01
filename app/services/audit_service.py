"""Audit service logic."""

from __future__ import annotations

from threading import Lock

from app.core.constants import (
    AUDIT_ACTION_INVENTORY_UPDATED,
    AUDIT_ACTION_LOGIN_FAILED,
    AUDIT_ACTION_LOGIN_SUCCESS,
    AUDIT_ACTION_PERMISSION_DENIED,
    AUDIT_ACTION_TRANSFER_ACTION,
    AUDIT_STATUS_FAILED,
    AUDIT_STATUS_SUCCESS,
)
from app.models.audit_log import AuditLog


# The in-memory store is intentionally simple until a real database table is wired in.
_AUDIT_LOGS: list[AuditLog] = []
_AUDIT_LOCK = Lock()
_NEXT_ID = 1


def _append_log(
    *,
    user_id: int | None,
    action: str,
    status: str,
    message: str | None = None,
    target_type: str | None = None,
    target_id: int | str | None = None,
) -> AuditLog:
    global _NEXT_ID
    with _AUDIT_LOCK:
        log = AuditLog(
            id=_NEXT_ID,
            user_id=user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            status=status,
            message=message,
            created_at=AuditLog.now_utc(),
        )
        _AUDIT_LOGS.append(log)
        _NEXT_ID += 1
        return log


def list_audit_logs() -> list[AuditLog]:
    """Return a snapshot of audit logs."""
    with _AUDIT_LOCK:
        return list(_AUDIT_LOGS)


def log_login_success(user_id: int, message: str = "Login successful") -> AuditLog:
    """Record a successful login event."""
    return _append_log(
        user_id=user_id,
        action=AUDIT_ACTION_LOGIN_SUCCESS,
        status=AUDIT_STATUS_SUCCESS,
        message=message,
        target_type="auth",
    )


def log_login_failed(email: str, message: str = "Invalid credentials") -> AuditLog:
    """Record a failed login attempt without exposing password data."""
    return _append_log(
        user_id=None,
        action=AUDIT_ACTION_LOGIN_FAILED,
        status=AUDIT_STATUS_FAILED,
        message=f"{message} | email={email}",
        target_type="auth",
    )


def log_permission_denied(
    *,
    user_id: int | None,
    action: str,
    target_type: str | None = None,
    target_id: int | str | None = None,
    message: str = "Permission denied",
) -> AuditLog:
    """Record an authorization failure for traceability and later review."""
    return _append_log(
        user_id=user_id,
        action=AUDIT_ACTION_PERMISSION_DENIED,
        status=AUDIT_STATUS_FAILED,
        message=f"{message} | attempted_action={action}",
        target_type=target_type,
        target_id=target_id,
    )


def log_inventory_update(
    *,
    user_id: int,
    inventory_id: int | str,
    message: str = "Inventory updated",
) -> AuditLog:
    """Record a successful inventory update event."""
    return _append_log(
        user_id=user_id,
        action=AUDIT_ACTION_INVENTORY_UPDATED,
        status=AUDIT_STATUS_SUCCESS,
        message=message,
        target_type="inventory",
        target_id=inventory_id,
    )


def log_transfer_action(
    *,
    user_id: int,
    transfer_id: int | str,
    approved: bool,
    message: str | None = None,
) -> AuditLog:
    """Record a transfer approval or rejection event."""
    status = AUDIT_STATUS_SUCCESS if approved else AUDIT_STATUS_FAILED
    default_message = "Transfer approved" if approved else "Transfer rejected"
    return _append_log(
        user_id=user_id,
        action=AUDIT_ACTION_TRANSFER_ACTION,
        status=status,
        message=message or default_message,
        target_type="transfer",
        target_id=transfer_id,
    )
