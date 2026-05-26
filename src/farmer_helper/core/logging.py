import logging
from typing import Any

from pythonjsonlogger.json import JsonFormatter


def configure_logging(level: str) -> None:
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level.upper())

    handler = logging.StreamHandler()
    formatter = JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)


class RequestContextFilter(logging.Filter):
    def __init__(self, request_id_provider: Any) -> None:
        super().__init__()
        self._request_id_provider = request_id_provider

    def filter(self, record: logging.LogRecord) -> bool:
        request_id = self._request_id_provider()
        record.request_id = request_id or "-"
        return True
