from farmer_helper.core.config import Settings


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.app_name == "farmer-helper"
    assert settings.api_port == 8000
    assert settings.database_url.startswith("sqlite")
