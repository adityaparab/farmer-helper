import gc
from collections.abc import Generator

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import close_all_sessions

from farmer_helper.db.base import get_engine


@pytest.fixture(autouse=True)
def cleanup_sqlalchemy_state() -> Generator[None, None, None]:
    yield
    close_all_sessions()
    for obj in gc.get_objects():
        if isinstance(obj, Engine):
            obj.dispose()


@pytest.fixture(scope="session", autouse=True)
def dispose_global_engine() -> Generator[None, None, None]:
    yield
    get_engine().dispose()
    get_engine.cache_clear()
