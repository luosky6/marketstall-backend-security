"""Permission service logic."""

from __future__ import annotations

from typing import Annotated, Iterable

from fastapi import Depends, HTTPException, status

from app.dependencies.auth import CurrentUser, get_current_user


def enforce_role(user_role: str, allowed_roles: Iterable[str]) -> None:
    """Raise 403 when the user role is not in the allowed role set."""
    role_set = {role.lower() for role in allowed_roles}
    if user_role.lower() not in role_set:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )


def require_roles(*allowed_roles: str):
    """FastAPI dependency factory to protect endpoints by roles."""
    if not allowed_roles:
        raise ValueError("At least one role is required")

    def dependency(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
    ) -> CurrentUser:
        # The dependency keeps role checks declarative at the router layer.
        enforce_role(current_user.role, allowed_roles)
        return current_user

    return dependency


def enforce_stall_ownership(
    *,
    current_user: CurrentUser,
    resource_stall_id: int | None,
    allow_manager: bool = True,
    allow_admin: bool = True,
) -> None:
    """Ensure user can access a stall-owned resource.

    Manager/admin bypass is enabled by default.
    """
    role = current_user.role.lower()
    if allow_admin and role == "admin":
        return
    if allow_manager and role == "manager":
        return

    if resource_stall_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Resource ownership is undefined",
        )
    if current_user.stall_id != resource_stall_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this resource",
        )
