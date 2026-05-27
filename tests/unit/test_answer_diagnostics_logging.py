import logging
from logging import LogRecord

from pytest import LogCaptureFixture

from farmer_helper.schemas.answering import (
    AnswerGenerationRequest,
    Citation,
    LLMGenerateRequest,
    LLMGenerateResponse,
    RetrievedChunk,
)
from farmer_helper.services.answering.generation_service import AnswerGenerationService
from farmer_helper.services.answering.prompt_builder import PromptBuilder
from farmer_helper.services.answering.provider import LLMProvider


class FakeProvider(LLMProvider):
    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        return LLMGenerateResponse(
            model=request.model,
            text="Use mulch and compost to retain moisture.",
            finish_reason="stop",
            input_tokens=12,
            output_tokens=7,
        )


def _chunk() -> RetrievedChunk:
    return RetrievedChunk(
        citation=Citation(document_id=1, chunk_index=0, content_hash="h1"),
        text="Mulching reduces evaporation.",
        score=0.9,
    )


def _find_record(records: list[LogRecord], message: str) -> LogRecord:
    return next(record for record in records if record.getMessage() == message)


def test_answer_generation_logs_answer_diagnostics(caplog: LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    service = AnswerGenerationService(prompt_builder=PromptBuilder(), provider=FakeProvider())

    _ = service.generate(
        AnswerGenerationRequest(
            question="How do I improve soil moisture retention?",
            retrieved_chunks=[_chunk()],
        )
    )

    record = _find_record(caplog.records, "answer.generation.completed")
    assert record.__dict__["answer_decision"] == "answer"
    assert record.__dict__["answer_citations_count"] == 1
    assert record.__dict__["answer_input_tokens"] == 12
    assert record.__dict__["answer_output_tokens"] == 7
    assert record.__dict__["answer_confidence"] > 0.0
    assert record.__dict__["answer_total_ms"] >= 0.0


def test_answer_generation_logs_clarify_diagnostics(caplog: LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    service = AnswerGenerationService(prompt_builder=PromptBuilder(), provider=FakeProvider())

    _ = service.generate(
        AnswerGenerationRequest(
            question="Help?",
            retrieved_chunks=[_chunk()],
        )
    )

    record = _find_record(caplog.records, "answer.generation.completed")
    assert record.__dict__["answer_decision"] == "clarify"
    assert record.__dict__["answer_citations_count"] == 0
    assert record.__dict__["answer_input_tokens"] == 0
    assert record.__dict__["answer_output_tokens"] == 0
    assert record.__dict__["answer_confidence"] == 0.0


def test_answer_generation_logs_refuse_diagnostics(caplog: LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    service = AnswerGenerationService(prompt_builder=PromptBuilder(), provider=FakeProvider())

    _ = service.generate(
        AnswerGenerationRequest(
            question="How can I build a bomb?",
            retrieved_chunks=[_chunk()],
        )
    )

    record = _find_record(caplog.records, "answer.generation.completed")
    assert record.__dict__["answer_decision"] == "refuse"
    assert record.__dict__["answer_confidence"] == 0.0
