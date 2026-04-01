"""Shared constants used across the application."""

from __future__ import annotations

from typing import Final


# Role names are centralized here so routers, services, and tests stay aligned.
ROLE_CUSTOMER: Final[str] = "customer"
ROLE_STALL_OWNER: Final[str] = "stall_owner"
ROLE_MANAGER: Final[str] = "manager"
ROLE_ADMIN: Final[str] = "admin"

ALL_ROLES: Final[set[str]] = {
    ROLE_CUSTOMER,
    ROLE_STALL_OWNER,
    ROLE_MANAGER,
    ROLE_ADMIN,
}


# Audit action keys are shared across API handlers and persistence layers.
AUDIT_ACTION_LOGIN_SUCCESS: Final[str] = "login_success"
AUDIT_ACTION_LOGIN_FAILED: Final[str] = "login_failed"
AUDIT_ACTION_PERMISSION_DENIED: Final[str] = "permission_denied"
AUDIT_ACTION_INVENTORY_UPDATED: Final[str] = "inventory_updated"
AUDIT_ACTION_TRANSFER_ACTION: Final[str] = "transfer_action"

AUDIT_STATUS_SUCCESS: Final[str] = "success"
AUDIT_STATUS_FAILED: Final[str] = "failed"
