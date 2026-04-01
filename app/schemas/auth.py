"""Pydantic schemas for authentication payloads."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Validation model for login credentials before authentication runs."""

    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    """JWT response payload returned after a successful login."""

    access_token: str
    token_type: str = "bearer"


class CurrentUserResponse(BaseModel):
    """Response model for authenticated user profile."""

    user_id: int
    email: EmailStr
    role: str
    stall_id: int | None = None
