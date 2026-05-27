from sqlalchemy import text
from sqlalchemy.orm import Session


class HealthRepository:
    def __init__(self, session: Session) -> None:
        """Initialize the object for health-repository repository persistence workflows.

        This HealthRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. Inputs are
        session. It runs synchronously and returns after local processing is complete. It
        performs its work through side effects and returns no payload.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        self._session = session

    def check_database(self) -> bool:
        """Check database for health-repository repository persistence workflows.

        This HealthRepository method documents a stable application boundary used by API
        handlers, service orchestration, validation, persistence, or runtime setup. The function
        does not require explicit caller-supplied arguments. It runs synchronously and returns
        after local processing is complete. It returns bool for downstream callers.

        The explicit docstring supports Swagger/OpenAPI inspection where applicable and keeps
        the source self-describing for future MCP server generation.
        """
        self._session.execute(text("SELECT 1"))
        return True
