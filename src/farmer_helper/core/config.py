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
    database_pool_min: int = Field(default=2, alias="DATABASE_POOL_MIN")
    database_pool_max: int = Field(default=10, alias="DATABASE_POOL_MAX")
    database_pool_timeout_seconds: int = Field(default=30, alias="DATABASE_POOL_TIMEOUT_SECONDS")

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
    sentry_dsn: str | None = Field(default=None, alias="SENTRY_DSN")
    sentry_traces_sample_rate: float = Field(default=0.0, alias="SENTRY_TRACES_SAMPLE_RATE")
    sentry_environment: str | None = Field(default=None, alias="SENTRY_ENVIRONMENT")
    security_api_key: str | None = Field(default=None, alias="SECURITY_API_KEY")
    security_rate_limit_requests: int = Field(default=0, alias="SECURITY_RATE_LIMIT_REQUESTS")
    security_rate_limit_window_seconds: int = Field(
        default=60,
        alias="SECURITY_RATE_LIMIT_WINDOW_SECONDS",
    )
    performance_cache_max_entries: int = Field(default=512, alias="PERFORMANCE_CACHE_MAX_ENTRIES")
    retrieval_cache_ttl_seconds: int = Field(default=0, alias="RETRIEVAL_CACHE_TTL_SECONDS")
    answer_cache_ttl_seconds: int = Field(default=0, alias="ANSWER_CACHE_TTL_SECONDS")
    llm_model_low_cost: str = Field(default="mock-chat-v1", alias="LLM_MODEL_LOW_COST")
    llm_model_high_quality: str = Field(default="mock-chat-v1", alias="LLM_MODEL_HIGH_QUALITY")
    llm_model_router_question_length_threshold: int = Field(
        default=120,
        alias="LLM_MODEL_ROUTER_QUESTION_LENGTH_THRESHOLD",
    )
    session_context_max_chars_per_message: int = Field(
        default=300,
        alias="SESSION_CONTEXT_MAX_CHARS_PER_MESSAGE",
    )
    embedding_worker_count: int = Field(default=2, alias="EMBEDDING_WORKER_COUNT")
    embedding_job_queue_max_size: int = Field(default=100, alias="EMBEDDING_JOB_QUEUE_MAX_SIZE")
    frontend_dist_dir: str = Field(default="frontend/dist", alias="FRONTEND_DIST_DIR")
    frontend_serve_enabled: bool = Field(default=True, alias="FRONTEND_SERVE_ENABLED")
    admin_upload_dir: str = Field(default="data/uploads/admin", alias="ADMIN_UPLOAD_DIR")
    admin_upload_max_size_bytes: int = Field(
        default=25 * 1024 * 1024,
        alias="ADMIN_UPLOAD_MAX_SIZE_BYTES",
    )
    auth_jwt_secret: str = Field(
        default="development-only-change-me",
        alias="AUTH_JWT_SECRET",
    )
    auth_access_token_ttl_minutes: int = Field(default=30, alias="AUTH_ACCESS_TOKEN_TTL_MINUTES")
    auth_refresh_token_ttl_days: int = Field(default=14, alias="AUTH_REFRESH_TOKEN_TTL_DAYS")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Retrieve settings for core runtime workflows.

    This module-level function documents a stable application boundary used by API handlers,
    service orchestration, validation, persistence, or runtime setup. The function does not
    require explicit caller-supplied arguments. It runs synchronously and returns after
    local processing is complete. It returns Settings for downstream callers.

    The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
    the source self-describing for future MCP server generation.
    """
    return Settings()
