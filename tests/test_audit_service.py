from __future__ import annotations

from app.services.audit_service import (
    list_audit_logs,
    log_inventory_update,
    log_login_failed,
    log_login_success,
    log_permission_denied,
    log_transfer_action,
)


def test_log_login_success_appends_success_event() -> None:
    log = log_login_success(4)

    logs = list_audit_logs()

    assert log.id == 1
    assert len(logs) == 1
    assert logs[0].action == "login_success"
    assert logs[0].status == "success"


def test_log_login_failed_records_email_in_message() -> None:
    log = log_login_failed("owner@example.com")

    assert log.status == "failed"
    assert "owner@example.com" in (log.message or "")


def test_log_permission_denied_records_target_metadata() -> None:
    log = log_permission_denied(
        user_id=2,
        action="owner_scope",
        target_type="stall",
        target_id=999,
    )

    assert log.action == "permission_denied"
    assert log.target_type == "stall"
    assert log.target_id == 999


def test_log_inventory_update_uses_inventory_target_type() -> None:
    log = log_inventory_update(user_id=2, inventory_id=12)

    assert log.action == "inventory_updated"
    assert log.target_type == "inventory"
    assert log.target_id == 12


def test_log_transfer_action_uses_success_status_when_approved() -> None:
    approved_log = log_transfer_action(user_id=3, transfer_id=88, approved=True)
    rejected_log = log_transfer_action(user_id=3, transfer_id=89, approved=False)

    assert approved_log.status == "success"
    assert rejected_log.status == "failed"
    assert rejected_log.id == approved_log.id + 1


def test_list_audit_logs_returns_copy() -> None:
    log_login_success(1)

    logs = list_audit_logs()
    logs.clear()

    assert len(list_audit_logs()) == 1
