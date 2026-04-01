"""Authentication-related dependency providers."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.core.security import TokenValidationError, decode_access_token


# Swagger and protected routes share the same bearer-token definition.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class CurrentUser(BaseModel):
    """Normalized authenticated user context extracted from access token."""

    user_id: int
    role: str
    stall_id: int | None = None


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> CurrentUser:
    """Resolve current user from bearer token and enforce basic token validity."""
    try:
        payload = decode_access_token(token)
    except TokenValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return CurrentUser(
        user_id=int(payload["user_id"]),
        role=str(payload["role"]),
        stall_id=payload.get("stall_id"),
    )
