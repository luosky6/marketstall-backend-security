from __future__ import annotations

import pytest
from fastapi import HTTPException

from app.dependencies.auth import CurrentUser
from app.services.permission_service import (
    enforce_role,
    enforce_stall_ownership,
    require_roles,
)


def test_enforce_role_allows_expected_role() -> None:
    enforce_role("admin", ["admin", "manager"])


def test_enforce_role_rejects_unauthorized_role() -> None:
    with pytest.raises(HTTPException) as exc_info:
        enforce_role("customer", ["admin", "manager"])

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Insufficient permissions"


def test_require_roles_requires_at_least_one_role() -> None:
    with pytest.raises(ValueError, match="At least one role is required"):
        require_roles()


def test_enforce_stall_ownership_allows_matching_owner() -> None:
    current_user = CurrentUser(user_id=2, role="stall_owner", stall_id=101)

    enforce_stall_ownership(current_user=current_user, resource_stall_id=101)


def test_enforce_stall_ownership_rejects_wrong_owner() -> None:
    current_user = CurrentUser(user_id=2, role="stall_owner", stall_id=101)

    with pytest.raises(HTTPException) as exc_info:
        enforce_stall_ownership(current_user=current_user, resource_stall_id=202)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You do not own this resource"


def test_enforce_stall_ownership_rejects_missing_resource_owner() -> None:
    current_user = CurrentUser(user_id=2, role="stall_owner", stall_id=101)

    with pytest.raises(HTTPException) as exc_info:
        enforce_stall_ownership(current_user=current_user, resource_stall_id=None)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Resource ownership is undefined"


def test_enforce_stall_ownership_allows_manager_by_default() -> None:
    current_user = CurrentUser(user_id=3, role="manager", stall_id=None)

    enforce_stall_ownership(current_user=current_user, resource_stall_id=999)


def test_enforce_stall_ownership_respects_manager_override_flag() -> None:
    current_user = CurrentUser(user_id=3, role="manager", stall_id=None)

    with pytest.raises(HTTPException) as exc_info:
        enforce_stall_ownership(
            current_user=current_user,
            resource_stall_id=999,
            allow_manager=False,
        )

    assert exc_info.value.status_code == 403
