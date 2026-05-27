from datetime import datetime

from farmer_helper.services.session.lifecycle_service import SessionLifecycleService


class FakeRepository:
    def __init__(self) -> None:
        self.archived_session_key: str | None = None
        self.expire_before: datetime | None = None

    def archive_session(self, session_key: str) -> None:
        self.archived_session_key = session_key

    def expire_active_sessions(self, updated_before: datetime) -> int:
        self.expire_before = updated_before
        return 3


def test_session_lifecycle_service_archive_delegates_to_repository() -> None:
    repository = FakeRepository()
    service = SessionLifecycleService(repository=repository)  # type: ignore[arg-type]

    service.archive("session-1")

    assert repository.archived_session_key == "session-1"


def test_session_lifecycle_service_expire_delegates_to_repository() -> None:
    repository = FakeRepository()
    service = SessionLifecycleService(repository=repository)  # type: ignore[arg-type]

    cutoff = datetime(2026, 5, 27, 0, 0, 0)
    count = service.expire_stale_sessions(updated_before=cutoff)

    assert repository.expire_before == cutoff
    assert count == 3
