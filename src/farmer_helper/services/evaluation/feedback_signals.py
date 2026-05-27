import logging

from farmer_helper.schemas.answering import AnswerFeedbackRequest


class OnlineFeedbackSignalLogger:
    def __init__(self, logger_instance: logging.Logger | None = None) -> None:
        self._logger = logger_instance or logging.getLogger(__name__)

    def log_answer_feedback(self, request: AnswerFeedbackRequest) -> None:
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
