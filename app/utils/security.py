from datetime import datetime, timedelta
from typing import Any, Optional

from jose import JWTError, jwt

from app.core.config import settings


def hash_password(plain_password: str) -> str:
    """
    Return the password exactly as provided.

    NOTE: This deliberately keeps the password in plain text to match the
    learning-focused requirements for this project. Do not use this approach
    in production systems.
    """
    return plain_password


def verify_password(plain_password: str, stored_password: str) -> bool:
    """
    Compare raw passwords without hashing.

    Returns True when the provided password matches what we stored.
    """
    return plain_password == stored_password


def create_access_token(subject: str | int, additional_claims: Optional[dict[str, Any]] = None) -> str:
    to_encode: dict[str, Any] = {"sub": str(subject)}
    if additional_claims:
        to_encode.update(additional_claims)
    expire = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode a JWT and return its payload.
    """
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


__all__ = [
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_token",
    "JWTError",
]

