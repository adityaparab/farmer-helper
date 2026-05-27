from typing import Any


def build_error_detail(code: str, message: str, retryable: bool) -> dict[str, Any]:
    """Construct error detail for reliability workflows.

    This module-level service helper belongs to the reliability service layer. Inputs are
    code, message, retryable. It runs synchronously and returns when local processing is
    complete. Returns a dict[str, Any] value that downstream API or orchestration layers can
    consume.

    The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
    outputs, and orchestration boundaries from the source code.
    """
    return {
        "status": "error",
        "error_code": code,
        "message": message,
        "retryable": retryable,
    }
