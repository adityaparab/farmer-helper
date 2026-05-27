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
        """Init for reliability workflows.

        Initialize InMemoryIdempotencyStore for reliability workflows. This operation does not
        require explicit caller-supplied arguments. It runs synchronously and returns when local
        processing is complete. The operation is executed for its side effects and does not
        return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._records: dict[tuple[str, str], IdempotencyRecord] = {}
        self._lock = Lock()

    def replay_or_raise(
        self,
        operation: str,
        key: str,
        request_hash: str,
    ) -> dict[str, Any] | None:
        """Replay or raise for reliability workflows.

        This InMemoryIdempotencyStore method belongs to the reliability service layer. Inputs
        are operation, key, request_hash. It runs synchronously and returns when local
        processing is complete. Returns a dict[str, Any] | None value that downstream API or
        orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
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
        """Persist for reliability workflows.

        This InMemoryIdempotencyStore method belongs to the reliability service layer. Inputs
        are operation, key, request_hash, response_payload. It runs synchronously and returns
        when local processing is complete. The operation is executed for its side effects and
        does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        with self._lock:
            self._records[(operation, key)] = IdempotencyRecord(
                request_hash=request_hash,
                response_payload=response_payload,
            )

    def clear(self) -> None:
        """Clear for reliability workflows.

        This InMemoryIdempotencyStore method belongs to the reliability service layer. This
        operation does not require explicit caller-supplied arguments. It runs synchronously and
        returns when local processing is complete. The operation is executed for its side
        effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        with self._lock:
            self._records.clear()


def compute_request_hash(payload: dict[str, Any]) -> str:
    """Compute request hash for reliability workflows.

    This module-level service helper belongs to the reliability service layer. Inputs are
    payload. It runs synchronously and returns when local processing is complete. Returns a
    str value that downstream API or orchestration layers can consume.

    The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
    outputs, and orchestration boundaries from the source code.
    """
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@lru_cache(maxsize=1)
def get_idempotency_store() -> InMemoryIdempotencyStore:
    """Retrieve idempotency store for reliability workflows.

    This module-level service helper belongs to the reliability service layer. This
    operation does not require explicit caller-supplied arguments. It runs synchronously and
    returns when local processing is complete. Returns a InMemoryIdempotencyStore value that
    downstream API or orchestration layers can consume.

    The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
    outputs, and orchestration boundaries from the source code.
    """
    return InMemoryIdempotencyStore()


def reset_idempotency_store() -> None:
    """Reset idempotency store for reliability workflows.

    This module-level service helper belongs to the reliability service layer. This
    operation does not require explicit caller-supplied arguments. It runs synchronously and
    returns when local processing is complete. The operation is executed for its side
    effects and does not return a payload.

    The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
    outputs, and orchestration boundaries from the source code.
    """
    get_idempotency_store().clear()
