from __future__ import annotations

import base64
import hashlib
import hmac
import secrets

PASSWORD_HASH_ALGORITHM = "pbkdf2_sha256"
DEFAULT_PASSWORD_ITERATIONS = 310_000
DEFAULT_ADMIN_PASSWORD_HASH = (
    "pbkdf2_sha256$310000$ZmFybWVyLWhlbHBlci1kZWZhdWx0LWFkbWluLXYx$"
    "sVHLdCuNSngooVlVDdkAn-oN0aLSL7uWBzJBQ_8tuvk"
)


def _b64_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _b64_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(f"{value}{padding}".encode("ascii"))


def hash_password(password: str, *, salt: bytes | None = None) -> str:
    salt_value = secrets.token_bytes(24) if salt is None else salt
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt_value,
        DEFAULT_PASSWORD_ITERATIONS,
    )
    return (
        f"{PASSWORD_HASH_ALGORITHM}${DEFAULT_PASSWORD_ITERATIONS}$"
        f"{_b64_encode(salt_value)}${_b64_encode(digest)}"
    )


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations_raw, salt_raw, digest_raw = password_hash.split("$", 3)
        iterations = int(iterations_raw)
    except ValueError:
        return False

    if algorithm != PASSWORD_HASH_ALGORITHM:
        return False

    salt = _b64_decode(salt_raw)
    expected_digest = _b64_decode(digest_raw)
    actual_digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    return hmac.compare_digest(actual_digest, expected_digest)
