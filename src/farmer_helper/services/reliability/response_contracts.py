from typing import Any


def build_error_detail(code: str, message: str, retryable: bool) -> dict[str, Any]:
    return {
        "status": "error",
        "error_code": code,
        "message": message,
        "retryable": retryable,
    }
