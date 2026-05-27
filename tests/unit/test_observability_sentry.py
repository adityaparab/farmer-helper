from types import ModuleType

import pytest

from farmer_helper.core.config import Settings
from farmer_helper.core.observability import configure_sentry


class _FakeSentryModule(ModuleType):
    def __init__(self) -> None:
        super().__init__("sentry_sdk")
        self.called = False
        self.kwargs: dict[str, object] = {}

    def init(self, **kwargs: object) -> None:
        self.called = True
        self.kwargs = kwargs


def test_configure_sentry_returns_false_when_dsn_empty() -> None:
    settings = Settings(SENTRY_DSN="")
    assert configure_sentry(settings) is False


def test_configure_sentry_initializes_sdk_when_available(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_sentry = _FakeSentryModule()
    monkeypatch.setitem(__import__("sys").modules, "sentry_sdk", fake_sentry)

    settings = Settings(
        SENTRY_DSN="https://examplePublicKey@o0.ingest.sentry.io/0",
        SENTRY_ENVIRONMENT="staging",
        SENTRY_TRACES_SAMPLE_RATE=0.2,
    )

    assert configure_sentry(settings) is True
    assert fake_sentry.called is True
    assert fake_sentry.kwargs["dsn"] == "https://examplePublicKey@o0.ingest.sentry.io/0"
    assert fake_sentry.kwargs["environment"] == "staging"
    assert fake_sentry.kwargs["traces_sample_rate"] == 0.2
