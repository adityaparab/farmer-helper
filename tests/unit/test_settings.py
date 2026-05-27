import pytest

from farmer_helper.core.config import Settings


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.app_name == "farmer-helper"
    assert settings.api_port == 8000
    assert settings.database_url.startswith("sqlite")


def test_settings_requires_openai_api_key_for_openai_providers() -> None:
    with pytest.raises(ValueError, match="OPENAI_API_KEY must be set"):
        Settings(LLM_PROVIDER="openai", OPENAI_API_KEY="")


def test_settings_allows_openai_provider_with_api_key() -> None:
    settings = Settings(LLM_PROVIDER="openai", OPENAI_API_KEY="test-key")
    assert settings.llm_provider == "openai"
