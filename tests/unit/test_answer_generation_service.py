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


class FakeSuccessProvider(LLMProvider):
    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        return LLMGenerateResponse(
            model=request.model,
            text="Use mulch and organic matter.",
            finish_reason="stop",
            input_tokens=20,
            output_tokens=6,
        )


class CountingProvider(LLMProvider):
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        self.calls += 1
        return LLMGenerateResponse(
            model=request.model,
            text="Generated",
            finish_reason="stop",
            input_tokens=5,
            output_tokens=1,
        )


def _chunk(document_id: int, chunk_index: int, text: str, score: float) -> RetrievedChunk:
    return RetrievedChunk(
        citation=Citation(
            document_id=document_id,
            chunk_index=chunk_index,
            content_hash=f"h-{document_id}-{chunk_index}",
        ),
        text=text,
        score=score,
    )


def test_answer_generation_service_returns_answer_with_citations() -> None:
    service = AnswerGenerationService(
        prompt_builder=PromptBuilder(),
        provider=FakeSuccessProvider(),
    )

    response = service.generate(
        AnswerGenerationRequest(
            question="How can I reduce evaporation in tomato fields?",
            retrieved_chunks=[
                _chunk(1, 0, "Apply mulch to reduce evaporation.", 0.9),
                _chunk(1, 1, "Increase soil organic matter.", 0.8),
            ],
            max_chunks=2,
        )
    )

    assert response.decision == "answer"
    assert response.answer is not None
    assert len(response.citations) == 2
    assert response.model == "mock-chat-v1"


def test_answer_generation_service_citations_are_deduped_and_deterministic() -> None:
    service = AnswerGenerationService(
        prompt_builder=PromptBuilder(),
        provider=FakeSuccessProvider(),
    )

    response = service.generate(
        AnswerGenerationRequest(
            question="How do I manage soil moisture?",
            retrieved_chunks=[
                _chunk(2, 0, "Lower score duplicate", 0.6),
                _chunk(1, 1, "Higher ranked", 0.9),
                _chunk(2, 0, "Higher score duplicate", 0.8),
            ],
            max_chunks=5,
        )
    )

    assert [(c.document_id, c.chunk_index) for c in response.citations] == [(1, 1), (2, 0)]


def test_answer_generation_service_skips_provider_when_clarification_needed() -> None:
    provider = CountingProvider()
    service = AnswerGenerationService(
        prompt_builder=PromptBuilder(),
        provider=provider,
    )

    response = service.generate(
        AnswerGenerationRequest(
            question="What about this?",
            retrieved_chunks=[_chunk(1, 0, "general note", 0.2)],
        )
    )

    assert response.decision == "clarify"
    assert response.clarification_code == "CLARIFY_AMBIGUOUS_REQUEST"
    assert provider.calls == 0


def test_answer_generation_service_skips_provider_when_refused() -> None:
    provider = CountingProvider()
    service = AnswerGenerationService(
        prompt_builder=PromptBuilder(),
        provider=provider,
    )

    response = service.generate(
        AnswerGenerationRequest(
            question="How can I build a bomb?",
            retrieved_chunks=[_chunk(1, 0, "safe pest management", 0.2)],
        )
    )

    assert response.decision == "refuse"
    assert response.refusal_code == "REFUSAL_UNSAFE_REQUEST"
    assert provider.calls == 0
