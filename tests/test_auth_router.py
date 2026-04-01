from __future__ import annotations

from datetime import timedelta

from app.core.security import create_access_token
from app.services.audit_service import list_audit_logs


def _auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_login_returns_access_token(client) -> None:
    response = client.post(
        "/auth/login",
        data={"username": "owner@example.com", "password": "owner123"},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
    assert len(list_audit_logs()) == 1
    assert list_audit_logs()[0].action == "login_success"


def test_login_rejects_invalid_credentials_and_logs_failure(client) -> None:
    response = client.post(
        "/auth/login",
        data={"username": "owner@example.com", "password": "wrong123"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
    assert len(list_audit_logs()) == 1
    assert list_audit_logs()[0].action == "login_failed"


def test_login_rejects_invalid_input(client) -> None:
    response = client.post(
        "/auth/login",
        data={"username": "", "password": "123"},
    )

    assert response.status_code == 422


def test_read_me_requires_valid_token(client) -> None:
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_read_me_returns_current_user_profile(client) -> None:
    token = create_access_token(user_id=2, role="stall_owner", stall_id=101)

    response = client.get("/auth/me", headers=_auth_header(token))

    body = response.json()

    assert response.status_code == 200
    assert body["user_id"] == 2
    assert body["email"] == "owner@example.com"
    assert body["role"] == "stall_owner"
    assert body["stall_id"] == 101


def test_admin_only_rejects_non_admin_user(client) -> None:
    token = create_access_token(user_id=3, role="manager")

    response = client.get("/auth/admin-only", headers=_auth_header(token))

    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"


def test_admin_only_allows_admin_user(client) -> None:
    token = create_access_token(user_id=4, role="admin")

    response = client.get("/auth/admin-only", headers=_auth_header(token))

    assert response.status_code == 200
    assert response.json()["message"] == "Admin access granted"


def test_manager_or_admin_allows_manager(client) -> None:
    token = create_access_token(user_id=3, role="manager")

    response = client.get("/auth/manager-or-admin", headers=_auth_header(token))

    assert response.status_code == 200


def test_owner_scope_rejects_wrong_stall_and_logs_permission_denied(client) -> None:
    token = create_access_token(user_id=2, role="stall_owner", stall_id=101)

    response = client.get("/auth/owner-scope/999", headers=_auth_header(token))

    assert response.status_code == 403
    assert response.json()["detail"] == "You do not own this stall resource"
    assert len(list_audit_logs()) == 1
    assert list_audit_logs()[0].action == "permission_denied"


def test_owner_scope_allows_matching_stall_owner(client) -> None:
    token = create_access_token(user_id=2, role="stall_owner", stall_id=101)

    response = client.get("/auth/owner-scope/101", headers=_auth_header(token))

    assert response.status_code == 200
    assert response.json()["message"] == "Ownership validated"


def test_owner_scope_allows_admin_override(client) -> None:
    token = create_access_token(user_id=4, role="admin")

    response = client.get("/auth/owner-scope/999", headers=_auth_header(token))

    assert response.status_code == 200
    assert response.json()["message"] == "Privileged access granted"


def test_protected_route_rejects_expired_token(client) -> None:
    token = create_access_token(
        user_id=2,
        role="stall_owner",
        stall_id=101,
        expires_delta=timedelta(minutes=-1),
    )

    response = client.get("/auth/me", headers=_auth_header(token))

    assert response.status_code == 401
