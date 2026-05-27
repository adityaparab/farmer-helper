import logging
from logging import LogRecord

from pytest import LogCaptureFixture

from farmer_helper.schemas.answering import AnswerFeedbackRequest
from farmer_helper.services.evaluation.feedback_signals import OnlineFeedbackSignalLogger


def _find_record(records: list[LogRecord], message: str) -> LogRecord:
    return next(record for record in records if record.getMessage() == message)


def test_online_feedback_signal_logger_emits_expected_fields(caplog: LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    logger = OnlineFeedbackSignalLogger()

    logger.log_answer_feedback(
        AnswerFeedbackRequest(
            session_key="session-1",
            question="How can I reduce fungal outbreak risk?",
            decision="answer",
            sentiment="not_helpful",
            reliability_status="degraded",
            had_citations=True,
            degraded=True,
            reason="unclear",
            model="mock-chat-v1",
        )
    )

    record = _find_record(caplog.records, "evaluation.feedback.signal")
    assert record.__dict__["feedback_sentiment"] == "not_helpful"
    assert record.__dict__["feedback_reason"] == "unclear"
    assert record.__dict__["feedback_decision"] == "answer"
    assert record.__dict__["feedback_reliability_status"] == "degraded"
    assert record.__dict__["feedback_had_citations"] is True
    assert record.__dict__["feedback_degraded"] is True
    assert record.__dict__["feedback_model"] == "mock-chat-v1"
    assert record.__dict__["feedback_session_present"] is True
    assert record.__dict__["feedback_question_length"] > 0
