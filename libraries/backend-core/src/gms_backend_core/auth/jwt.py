from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from ..config import GmsBackendSettings


def create_access_token(
    data: dict[str, Any], settings: GmsBackendSettings, expires_delta: timedelta | None = None
):
    """Create a new JWT token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_access_token(token: str, settings: GmsBackendSettings) -> dict[str, Any]:
    """Decode and validate a JWT token."""
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])


def is_internal_staff(email: str, allowed_domain: str) -> bool:
    """Checks if an email belongs to the authorized domain."""
    return email.endswith(f"@{allowed_domain}")
