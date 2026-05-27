from farmer_helper.repositories.health_repository import HealthRepository


class HealthService:
    def __init__(self, repository: HealthRepository) -> None:
        """Init for application workflows.

        Initialize HealthService for application workflows. Inputs are repository. It runs
        synchronously and returns when local processing is complete. The operation is executed
        for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._repository = repository

    def is_ready(self) -> bool:
        """Determine whether is ready for application workflows.

        This HealthService method belongs to the application service layer. This operation does
        not require explicit caller-supplied arguments. It runs synchronously and returns when
        local processing is complete. Returns a bool value that downstream API or orchestration
        layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        return self._repository.check_database()
