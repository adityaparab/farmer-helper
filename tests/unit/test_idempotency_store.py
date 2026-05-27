import pytest

from farmer_helper.services.reliability.idempotency import (
    IdempotencyConflictError,
    InMemoryIdempotencyStore,
    compute_request_hash,
)


def test_idempotency_store_replays_saved_payload() -> None:
    store = InMemoryIdempotencyStore()
    request_payload = {"a": 1, "b": "soil"}
    request_hash = compute_request_hash(request_payload)

    store.save(
        operation="answers.generate",
        key="id-1",
        request_hash=request_hash,
        response_payload={"decision": "answer", "answer": "ok"},
    )

    replay = store.replay_or_raise(
        operation="answers.generate",
        key="id-1",
        request_hash=request_hash,
    )

    assert replay == {"decision": "answer", "answer": "ok"}


def test_idempotency_store_raises_for_hash_mismatch() -> None:
    store = InMemoryIdempotencyStore()
    hash_a = compute_request_hash({"question": "soil"})
    hash_b = compute_request_hash({"question": "water"})

    store.save(
        operation="answers.generate",
        key="id-2",
        request_hash=hash_a,
        response_payload={"decision": "answer", "answer": "ok"},
    )

    with pytest.raises(IdempotencyConflictError):
        store.replay_or_raise(
            operation="answers.generate",
            key="id-2",
            request_hash=hash_b,
        )


def test_compute_request_hash_is_stable_for_key_order() -> None:
    left = compute_request_hash({"a": 1, "b": 2})
    right = compute_request_hash({"b": 2, "a": 1})

    assert left == right
