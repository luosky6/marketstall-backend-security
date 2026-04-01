"""Custom exception definitions for the application."""

from __future__ import annotations


class SecurityError(Exception):
    """Base class for all security-related application errors."""


class AuthenticationError(SecurityError):
    """Raised when user authentication fails."""


class AuthorizationError(SecurityError):
    """Raised when user lacks required permissions."""


class OwnershipError(SecurityError):
    """Raised when user tries to access a resource they do not own."""
