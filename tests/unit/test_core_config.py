import pytest

from farmer_helper.core.config import get_settings


def test_security_api_key_empty_string_is_treated_as_unset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SECURITY_API_KEY", "")
    get_settings.cache_clear()

    try:
        assert get_settings().security_api_key is None
    finally:
        get_settings.cache_clear()
