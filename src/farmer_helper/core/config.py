from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="farmer-helper", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_log_level: str = Field(default="INFO", alias="APP_LOG_LEVEL")

    api_host: str = Field(default="127.0.0.1", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")

    database_url: str = Field(default="sqlite:///./farmer_helper.db", alias="DATABASE_URL")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
