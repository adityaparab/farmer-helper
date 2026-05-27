from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AccessTokenClaims:
    subject: str
    username: str
    role: str
    token_type: str
    expires_at: int


def _b64_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _b64_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(f"{value}{padding}".encode("ascii"))


def _json_dumps(value: dict[str, Any]) -> bytes:
    return json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")


def create_access_token(
    *,
    user_id: int,
    username: str,
    role: str,
    secret: str,
    ttl_seconds: int,
    now: int | None = None,
) -> str:
    issued_at = int(time.time()) if now is None else now
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "type": "access",
        "iat": issued_at,
        "exp": issued_at + ttl_seconds,
    }
    encoded_header = _b64_encode(_json_dumps(header))
    encoded_payload = _b64_encode(_json_dumps(payload))
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    return f"{encoded_header}.{encoded_payload}.{_b64_encode(signature)}"


def decode_access_token(token: str, *, secret: str, now: int | None = None) -> AccessTokenClaims:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Malformed token")

    encoded_header, encoded_payload, encoded_signature = parts
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    expected_signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    actual_signature = _b64_decode(encoded_signature)
    if not hmac.compare_digest(actual_signature, expected_signature):
        raise ValueError("Invalid token signature")

    payload = json.loads(_b64_decode(encoded_payload).decode("utf-8"))
    expires_at = int(payload["exp"])
    now_value = int(time.time()) if now is None else now
    if expires_at <= now_value:
        raise ValueError("Token expired")
    if payload.get("type") != "access":
        raise ValueError("Invalid token type")

    return AccessTokenClaims(
        subject=str(payload["sub"]),
        username=str(payload["username"]),
        role=str(payload["role"]),
        token_type=str(payload["type"]),
        expires_at=expires_at,
    )


def create_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
