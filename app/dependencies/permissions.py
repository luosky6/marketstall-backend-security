"""Permission-related dependency providers."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from app.core.constants import ROLE_ADMIN, ROLE_MANAGER, ROLE_STALL_OWNER
from app.dependencies.auth import CurrentUser, get_current_user
from app.services.permission_service import enforce_stall_ownership, require_roles


def require_stall_owner(
    current_user: Annotated[CurrentUser, Depends(require_roles(ROLE_STALL_OWNER))],
) -> CurrentUser:
    """Dependency ensuring current user is stall owner."""
    return current_user


def require_manager_or_admin(
    current_user: Annotated[
        CurrentUser,
        Depends(require_roles(ROLE_MANAGER, ROLE_ADMIN)),
    ],
) -> CurrentUser:
    """Dependency ensuring current user is manager or admin."""
    return current_user


def require_admin(
    current_user: Annotated[CurrentUser, Depends(require_roles(ROLE_ADMIN))],
) -> CurrentUser:
    """Dependency ensuring current user is admin."""
    return current_user


def validate_stall_ownership(
    *,
    current_user: CurrentUser,
    resource_stall_id: int | None,
    allow_manager: bool = True,
    allow_admin: bool = True,
) -> None:
    """Wrapper for ownership validation used by routers/services."""
    enforce_stall_ownership(
        current_user=current_user,
        resource_stall_id=resource_stall_id,
        allow_manager=allow_manager,
        allow_admin=allow_admin,
    )


def get_authenticated_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> CurrentUser:
    """Explicit dependency for authenticated user context."""
    return current_user
