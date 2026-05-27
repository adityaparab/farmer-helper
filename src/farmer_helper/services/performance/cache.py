from __future__ import annotations

import time
from collections import OrderedDict
from dataclasses import dataclass
from threading import Lock


@dataclass
class _Entry[V]:
    expires_at: float
    value: V


class TTLCache[K, V]:
    def __init__(self, max_entries: int) -> None:
        """Init for performance workflows.

        Initialize TTLCache for performance workflows. Inputs are max_entries. It runs
        synchronously and returns when local processing is complete. The operation is executed
        for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if max_entries < 1:
            raise ValueError("max_entries must be >= 1")
        self._max_entries = max_entries
        self._items: OrderedDict[K, _Entry[V]] = OrderedDict()
        self._lock = Lock()

    def get(self, key: K) -> V | None:
        """Retrieve for performance workflows.

        This TTLCache method belongs to the performance service layer. Inputs are key. It runs
        synchronously and returns when local processing is complete. Returns a V | None value
        that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        now = time.time()
        with self._lock:
            entry = self._items.get(key)
            if entry is None:
                return None
            if entry.expires_at <= now:
                self._items.pop(key, None)
                return None
            self._items.move_to_end(key)
            return entry.value

    def set(self, key: K, value: V, ttl_seconds: int) -> None:
        """Set for performance workflows.

        This TTLCache method belongs to the performance service layer. Inputs are key, value,
        ttl_seconds. It runs synchronously and returns when local processing is complete. The
        operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if ttl_seconds <= 0:
            return

        expires_at = time.time() + float(ttl_seconds)
        with self._lock:
            self._items[key] = _Entry(expires_at=expires_at, value=value)
            self._items.move_to_end(key)
            while len(self._items) > self._max_entries:
                self._items.popitem(last=False)
