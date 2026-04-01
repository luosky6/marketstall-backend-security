from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import app.services.audit_service as audit_service
from main import app


@pytest.fixture(autouse=True)
def reset_audit_logs() -> None:
    audit_service._AUDIT_LOGS.clear()
    audit_service._NEXT_ID = 1


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
