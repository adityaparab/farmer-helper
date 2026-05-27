import logging


class AnswerDiagnosticsLogger:
    def __init__(self) -> None:
        """Init for answer-generation workflows.

        Initialize AnswerDiagnosticsLogger for answer-generation workflows. This operation does
        not require explicit caller-supplied arguments. It runs synchronously and returns when
        local processing is complete. The operation is executed for its side effects and does
        not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._logger = logging.getLogger(__name__)

    def generation_completed(
        self,
        *,
        decision: str,
        model: str,
        citations_count: int,
        input_tokens: int,
        output_tokens: int,
        confidence: float,
        total_ms: float,
    ) -> None:
        """Generation completed for answer-generation workflows.

        This AnswerDiagnosticsLogger method belongs to the answer-generation service layer.
        Inputs are decision, model, citations_count, input_tokens, output_tokens, confidence,
        total_ms. It runs synchronously and returns when local processing is complete. The
        operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._logger.info(
            "answer.generation.completed",
            extra={
                "answer_decision": decision,
                "answer_model": model,
                "answer_citations_count": citations_count,
                "answer_input_tokens": input_tokens,
                "answer_output_tokens": output_tokens,
                "answer_confidence": round(confidence, 4),
                "answer_total_ms": round(total_ms, 4),
            },
        )
