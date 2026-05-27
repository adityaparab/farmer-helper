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

    external_call_timeout_seconds: float = Field(
        default=2.0,
        alias="EXTERNAL_CALL_TIMEOUT_SECONDS",
    )
    embedding_retry_max_attempts: int = Field(
        default=3,
        alias="EMBEDDING_RETRY_MAX_ATTEMPTS",
    )
    llm_retry_max_attempts: int = Field(
        default=3,
        alias="LLM_RETRY_MAX_ATTEMPTS",
    )
    embedding_circuit_breaker_failure_threshold: int = Field(
        default=3,
        alias="EMBEDDING_CIRCUIT_BREAKER_FAILURE_THRESHOLD",
    )
    embedding_circuit_breaker_recovery_timeout_seconds: float = Field(
        default=30.0,
        alias="EMBEDDING_CIRCUIT_BREAKER_RECOVERY_TIMEOUT_SECONDS",
    )
    llm_circuit_breaker_failure_threshold: int = Field(
        default=3,
        alias="LLM_CIRCUIT_BREAKER_FAILURE_THRESHOLD",
    )
    llm_circuit_breaker_recovery_timeout_seconds: float = Field(
        default=30.0,
        alias="LLM_CIRCUIT_BREAKER_RECOVERY_TIMEOUT_SECONDS",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
