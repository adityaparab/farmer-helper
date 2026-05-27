import hashlib
import json
from dataclasses import dataclass
from functools import lru_cache
from threading import Lock
from typing import Any


@dataclass(frozen=True)
class IdempotencyRecord:
    request_hash: str
    response_payload: dict[str, Any]


class IdempotencyConflictError(Exception):
    pass


class InMemoryIdempotencyStore:
    def __init__(self) -> None:
        self._records: dict[tuple[str, str], IdempotencyRecord] = {}
        self._lock = Lock()

    def replay_or_raise(
        self,
        operation: str,
        key: str,
        request_hash: str,
    ) -> dict[str, Any] | None:
        with self._lock:
            record = self._records.get((operation, key))
            if record is None:
                return None
            if record.request_hash != request_hash:
                raise IdempotencyConflictError(
                    "idempotency key is already used with a different request payload"
                )
            return record.response_payload

    def save(
        self,
        operation: str,
        key: str,
        request_hash: str,
        response_payload: dict[str, Any],
    ) -> None:
        with self._lock:
            self._records[(operation, key)] = IdempotencyRecord(
                request_hash=request_hash,
                response_payload=response_payload,
            )

    def clear(self) -> None:
        with self._lock:
            self._records.clear()


def compute_request_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@lru_cache(maxsize=1)
def get_idempotency_store() -> InMemoryIdempotencyStore:
    return InMemoryIdempotencyStore()


def reset_idempotency_store() -> None:
    get_idempotency_store().clear()
