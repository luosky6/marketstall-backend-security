"""Security utilities: password hashing and JWT token handling.

This module provides the foundation for authentication in the backend.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from os import getenv
from typing import Any

import bcrypt
from jose import JWTError, jwt


ALGORITHM = "HS256"
JWT_SECRET_KEY = getenv("JWT_SECRET_KEY", "change-me-in-production")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


class TokenValidationError(ValueError):
    """Raised when an access token cannot be decoded or validated."""


def hash_password(password: str) -> str:
    """Hash a plaintext password with bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(
    *,
    user_id: int,
    role: str,
    stall_id: int | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT access token with standard and custom claims."""
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # The token embeds only the context needed by downstream authorization checks.
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "user_id": user_id,
        "role": role,
        "stall_id": stall_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate an access token.

    Raises:
        TokenValidationError: If token is expired, malformed, or missing claims.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as exc:
        raise TokenValidationError("Invalid or expired token") from exc

    user_id = payload.get("user_id")
    role = payload.get("role")
    token_type = payload.get("type")

    # These claims are the minimum contract expected by permission checks.
    if user_id is None or role is None:
        raise TokenValidationError("Token missing required claims: user_id/role")
    if token_type != "access":
        raise TokenValidationError("Invalid token type")

    return payload
