from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

from farmer_helper.core.config import get_settings


def _build_engine(url: str) -> Engine:
    """Construct engine for database workflows.

    This module-level function documents a stable application boundary used by API handlers,
    service orchestration, validation, persistence, or runtime setup. Inputs are url. It
    runs synchronously and returns after local processing is complete. It returns Engine for
    downstream callers.

    The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
    the source self-describing for future MCP server generation.
    """
    settings = get_settings()
    max_overflow = max(0, settings.database_pool_max - settings.database_pool_min)

    if url.startswith("sqlite"):
        return create_engine(
            url,
            future=True,
            connect_args={"check_same_thread": False},
            pool_pre_ping=True,
        )

    return create_engine(
        url,
        future=True,
        poolclass=QueuePool,
        pool_size=settings.database_pool_min,
        max_overflow=max_overflow,
        pool_timeout=settings.database_pool_timeout_seconds,
        pool_pre_ping=True,
    )


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Retrieve engine for database workflows.

    This module-level function documents a stable application boundary used by API handlers,
    service orchestration, validation, persistence, or runtime setup. The function does not
    require explicit caller-supplied arguments. It runs synchronously and returns after
    local processing is complete. It returns Engine for downstream callers.

    The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
    the source self-describing for future MCP server generation.
    """
    settings = get_settings()
    return _build_engine(settings.database_url)


SessionLocal = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False, class_=Session)


def get_db_session() -> Iterator[Session]:
    """Retrieve db session for database workflows.

    This module-level function documents a stable application boundary used by API handlers,
    service orchestration, validation, persistence, or runtime setup. The function does not
    require explicit caller-supplied arguments. It runs synchronously and returns after
    local processing is complete. It returns Iterator[Session] for downstream callers.

    The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
    the source self-describing for future MCP server generation.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
