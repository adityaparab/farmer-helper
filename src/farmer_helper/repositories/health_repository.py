from sqlalchemy import text
from sqlalchemy.orm import Session


class HealthRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def check_database(self) -> bool:
        self._session.execute(text("SELECT 1"))
        return True
