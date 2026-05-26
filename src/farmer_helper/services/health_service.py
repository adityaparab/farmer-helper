from farmer_helper.repositories.health_repository import HealthRepository


class HealthService:
    def __init__(self, repository: HealthRepository) -> None:
        self._repository = repository

    def is_ready(self) -> bool:
        return self._repository.check_database()
