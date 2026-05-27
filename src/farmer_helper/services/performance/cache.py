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
        if max_entries < 1:
            raise ValueError("max_entries must be >= 1")
        self._max_entries = max_entries
        self._items: OrderedDict[K, _Entry[V]] = OrderedDict()
        self._lock = Lock()

    def get(self, key: K) -> V | None:
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
        if ttl_seconds <= 0:
            return

        expires_at = time.time() + float(ttl_seconds)
        with self._lock:
            self._items[key] = _Entry(expires_at=expires_at, value=value)
            self._items.move_to_end(key)
            while len(self._items) > self._max_entries:
                self._items.popitem(last=False)
