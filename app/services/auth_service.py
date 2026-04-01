"""Authentication service logic."""

from __future__ import annotations

from dataclasses import dataclass

from app.core.constants import (
    ROLE_ADMIN,
    ROLE_CUSTOMER,
    ROLE_MANAGER,
    ROLE_STALL_OWNER,
)
from app.core.exceptions import AuthenticationError
from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.auth import CurrentUserResponse, TokenResponse


@dataclass(frozen=True)
class UserRecord:
    """Simple in-memory user structure used before DB integration."""

    id: int
    email: str
    password_hash: str
    role: str
    stall_id: int | None = None


# This in-memory store keeps the module self-contained for demos and tests.
_USER_STORE: dict[str, UserRecord] = {
    "customer@example.com": UserRecord(
        id=1,
        email="customer@example.com",
        password_hash=hash_password("customer123"),
        role=ROLE_CUSTOMER,
        stall_id=None,
    ),
    "owner@example.com": UserRecord(
        id=2,
        email="owner@example.com",
        password_hash=hash_password("owner123"),
        role=ROLE_STALL_OWNER,
        stall_id=101,
    ),
    "manager@example.com": UserRecord(
        id=3,
        email="manager@example.com",
        password_hash=hash_password("manager123"),
        role=ROLE_MANAGER,
        stall_id=None,
    ),
    "admin@example.com": UserRecord(
        id=4,
        email="admin@example.com",
        password_hash=hash_password("admin123"),
        role=ROLE_ADMIN,
        stall_id=None,
    ),
}


def get_user_by_email(email: str) -> UserRecord | None:
    """Fetch user from local store by email."""
    return _USER_STORE.get(email.lower())


def get_user_by_id(user_id: int) -> UserRecord | None:
    """Fetch user from local store by internal user id."""
    for user in _USER_STORE.values():
        if user.id == user_id:
            return user
    return None


def authenticate_user(email: str, password: str) -> UserRecord:
    """Validate user credentials and return user record."""
    user = get_user_by_email(email)
    if user is None or not verify_password(password, user.password_hash):
        raise AuthenticationError("Invalid email or password")
    return user


def create_login_token(user: UserRecord) -> TokenResponse:
    """Issue an access token for an authenticated user."""
    access_token = create_access_token(
        user_id=user.id,
        role=user.role,
        stall_id=user.stall_id,
    )
    return TokenResponse(access_token=access_token)


def to_current_user_response(user: UserRecord) -> CurrentUserResponse:
    """Map internal user record to API-safe user response."""
    return CurrentUserResponse(
        user_id=user.id,
        email=user.email,
        role=user.role,
        stall_id=user.stall_id,
    )
