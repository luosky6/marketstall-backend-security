from __future__ import annotations

import pytest

from app.core.exceptions import AuthenticationError
from app.services.auth_service import (
    authenticate_user,
    create_login_token,
    get_user_by_email,
    get_user_by_id,
    to_current_user_response,
)


def test_get_user_by_email_is_case_insensitive() -> None:
    user = get_user_by_email("OWNER@EXAMPLE.COM")

    assert user is not None
    assert user.email == "owner@example.com"


def test_get_user_by_id_returns_expected_user() -> None:
    user = get_user_by_id(4)

    assert user is not None
    assert user.role == "admin"


def test_authenticate_user_accepts_valid_credentials() -> None:
    user = authenticate_user("owner@example.com", "owner123")

    assert user.id == 2
    assert user.role == "stall_owner"
    assert user.stall_id == 101


def test_authenticate_user_rejects_invalid_password() -> None:
    with pytest.raises(AuthenticationError, match="Invalid email or password"):
        authenticate_user("owner@example.com", "wrong-password")


def test_authenticate_user_rejects_unknown_email() -> None:
    with pytest.raises(AuthenticationError, match="Invalid email or password"):
        authenticate_user("missing@example.com", "owner123")


def test_create_login_token_returns_bearer_token() -> None:
    user = authenticate_user("manager@example.com", "manager123")

    token = create_login_token(user)

    assert token.token_type == "bearer"
    assert isinstance(token.access_token, str)
    assert token.access_token


def test_to_current_user_response_excludes_password_hash() -> None:
    user = authenticate_user("admin@example.com", "admin123")

    response = to_current_user_response(user)

    assert response.user_id == 4
    assert response.email == "admin@example.com"
    assert not hasattr(response, "password_hash")
