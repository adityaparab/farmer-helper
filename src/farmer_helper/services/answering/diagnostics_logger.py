import logging


class AnswerDiagnosticsLogger:
    def __init__(self) -> None:
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
