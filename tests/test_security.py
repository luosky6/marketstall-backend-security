from __future__ import annotations

from datetime import timedelta

import pytest
from jose import jwt

from app.core.security import (
    ALGORITHM,
    JWT_SECRET_KEY,
    TokenValidationError,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_returns_hash_not_plaintext() -> None:
    hashed = hash_password("owner123")

    assert hashed != "owner123"
    assert verify_password("owner123", hashed) is True


def test_verify_password_rejects_wrong_password() -> None:
    hashed = hash_password("owner123")

    assert verify_password("wrong-password", hashed) is False


def test_create_and_decode_access_token_round_trip() -> None:
    token = create_access_token(user_id=2, role="stall_owner", stall_id=101)

    payload = decode_access_token(token)

    assert payload["user_id"] == 2
    assert payload["role"] == "stall_owner"
    assert payload["stall_id"] == 101
    assert payload["type"] == "access"


def test_decode_access_token_rejects_expired_token() -> None:
    token = create_access_token(
        user_id=2,
        role="stall_owner",
        stall_id=101,
        expires_delta=timedelta(minutes=-1),
    )

    with pytest.raises(TokenValidationError, match="Invalid or expired token"):
        decode_access_token(token)


def test_decode_access_token_rejects_missing_claims() -> None:
    token = jwt.encode({"type": "access"}, JWT_SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(TokenValidationError, match="missing required claims"):
        decode_access_token(token)


def test_decode_access_token_rejects_wrong_token_type() -> None:
    token = jwt.encode(
        {"user_id": 2, "role": "stall_owner", "type": "refresh"},
        JWT_SECRET_KEY,
        algorithm=ALGORITHM,
    )

    with pytest.raises(TokenValidationError, match="Invalid token type"):
        decode_access_token(token)
