from typing import Any

from sqlalchemy.pool import QueuePool

from farmer_helper.db import base as db_base


class _FakeSettings:
    database_pool_min = 3
    database_pool_max = 9
    database_pool_timeout_seconds = 45


def test_build_engine_non_sqlite_uses_queue_pool(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    captured: dict[str, Any] = {}

    def _fake_create_engine(url: str, **kwargs: Any) -> object:
        captured["url"] = url
        captured["kwargs"] = kwargs
        return object()

    monkeypatch.setattr(db_base, "create_engine", _fake_create_engine)
    monkeypatch.setattr(db_base, "get_settings", lambda: _FakeSettings())

    engine = db_base._build_engine("postgresql+psycopg://example")

    assert engine is not None
    assert captured["url"] == "postgresql+psycopg://example"
    assert captured["kwargs"]["poolclass"] is QueuePool
    assert captured["kwargs"]["pool_size"] == 3
    assert captured["kwargs"]["max_overflow"] == 6
    assert captured["kwargs"]["pool_timeout"] == 45
    assert captured["kwargs"]["pool_pre_ping"] is True


def test_build_engine_sqlite_uses_check_same_thread_false(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    captured: dict[str, Any] = {}

    def _fake_create_engine(url: str, **kwargs: Any) -> object:
        captured["url"] = url
        captured["kwargs"] = kwargs
        return object()

    monkeypatch.setattr(db_base, "create_engine", _fake_create_engine)
    monkeypatch.setattr(db_base, "get_settings", lambda: _FakeSettings())

    engine = db_base._build_engine("sqlite:///./farmer_helper.db")

    assert engine is not None
    assert captured["url"] == "sqlite:///./farmer_helper.db"
    assert captured["kwargs"]["connect_args"] == {"check_same_thread": False}
    assert captured["kwargs"]["pool_pre_ping"] is True
    assert "poolclass" not in captured["kwargs"]
