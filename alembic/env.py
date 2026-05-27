from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from farmer_helper.core.config import get_settings
from farmer_helper.db.models.base import Base
from farmer_helper.db.models.foundation import (
    ApiRequestLog,
    ChunkEmbedding,
    Document,
    IngestionJob,
)

# Keep imports for metadata registration.
_ = (Document, IngestionJob, ApiRequestLog, ChunkEmbedding)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    section = config.get_section(config.config_ini_section, {})
    engine_kwargs: dict[str, object] = {
        "prefix": "sqlalchemy.",
    }

    if settings.database_url.startswith("sqlite"):
        engine_kwargs["poolclass"] = pool.NullPool
    else:
        engine_kwargs["poolclass"] = pool.QueuePool
        engine_kwargs["pool_size"] = settings.database_pool_min
        engine_kwargs["max_overflow"] = max(
            0, settings.database_pool_max - settings.database_pool_min
        )
        engine_kwargs["pool_timeout"] = settings.database_pool_timeout_seconds
        engine_kwargs["pool_pre_ping"] = True

    connectable = engine_from_config(section, **engine_kwargs)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
