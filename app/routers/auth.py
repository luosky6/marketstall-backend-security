"""Authentication API router definitions."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from app.core.exceptions import AuthenticationError
from app.dependencies.auth import CurrentUser, get_current_user
from app.schemas.auth import CurrentUserResponse, LoginRequest, TokenResponse
from app.services.audit_service import (
    log_login_failed,
    log_login_success,
    log_permission_denied,
)
from app.services.auth_service import (
    authenticate_user,
    create_login_token,
    get_user_by_id,
    to_current_user_response,
)
from app.services.permission_service import require_roles


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    """Authenticate user and return JWT access token."""
    # OAuth2PasswordRequestForm uses the standard field name `username`.
    email = form_data.username
    try:
        LoginRequest(email=email, password=form_data.password)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.errors(),
        ) from exc

    try:
        user = authenticate_user(email, form_data.password)
    except AuthenticationError as exc:
        log_login_failed(email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        ) from exc

    log_login_success(user.id)
    return create_login_token(user)


@router.get("/me", response_model=CurrentUserResponse)
def read_me(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> CurrentUserResponse:
    """Return current user profile from token context."""
    user = get_user_by_id(current_user.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return to_current_user_response(user)


@router.get("/admin-only")
def admin_only(
    current_user: Annotated[CurrentUser, Depends(require_roles("admin"))],
) -> dict[str, str | int]:
    """Example endpoint protected by admin role."""
    return {
        "message": "Admin access granted",
        "user_id": current_user.user_id,
    }


@router.get("/manager-or-admin")
def manager_or_admin(
    current_user: Annotated[
        CurrentUser,
        Depends(require_roles("manager", "admin")),
    ],
) -> dict[str, str | int]:
    """Example endpoint protected by manager/admin roles."""
    return {
        "message": "Manager/Admin access granted",
        "user_id": current_user.user_id,
    }


@router.get("/owner-scope/{stall_id}")
def owner_scope(
    stall_id: int,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> dict[str, str | int]:
    """Example ownership check endpoint."""
    # Managers and admins can inspect any stall-scoped resource.
    if current_user.role.lower() in {"manager", "admin"}:
        return {"message": "Privileged access granted", "stall_id": stall_id}

    if current_user.stall_id != stall_id:
        log_permission_denied(
            user_id=current_user.user_id,
            action="owner_scope",
            target_type="stall",
            target_id=stall_id,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this stall resource",
        )

    return {
        "message": "Ownership validated",
        "stall_id": stall_id,
        "user_id": current_user.user_id,
    }
