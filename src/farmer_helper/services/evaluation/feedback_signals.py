import logging

from farmer_helper.schemas.answering import AnswerFeedbackRequest


class OnlineFeedbackSignalLogger:
    def __init__(self, logger_instance: logging.Logger | None = None) -> None:
        """Init for evaluation workflows.

        Initialize OnlineFeedbackSignalLogger for evaluation workflows. Inputs are
        logger_instance. It runs synchronously and returns when local processing is complete.
        The operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._logger = logger_instance or logging.getLogger(__name__)

    def log_answer_feedback(self, request: AnswerFeedbackRequest) -> None:
        """Log answer feedback for evaluation workflows.

        This OnlineFeedbackSignalLogger method belongs to the evaluation service layer. Inputs
        are request. It runs synchronously and returns when local processing is complete. The
        operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._logger.info(
            "evaluation.feedback.signal",
            extra={
                "feedback_sentiment": request.sentiment,
                "feedback_reason": request.reason,
                "feedback_decision": request.decision,
                "feedback_reliability_status": request.reliability_status,
                "feedback_had_citations": request.had_citations,
                "feedback_degraded": request.degraded,
                "feedback_model": request.model or "unknown",
                "feedback_session_present": request.session_key is not None,
                "feedback_question_length": len(request.question.strip()),
            },
        )
