import pytest
from pydantic import ValidationError

from farmer_helper.schemas.answering import (
    LLMGenerateRequest,
    LLMGenerateResponse,
    LLMMessage,
)
from farmer_helper.services.answering.provider import LLMProvider, LLMProviderError


class FakeLLMProvider(LLMProvider):
    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        prompt_tokens = sum(len(message.content.split()) for message in request.messages)
        return LLMGenerateResponse(
            model=request.model,
            text="Use mulch and organic matter to improve moisture retention.",
            finish_reason="stop",
            input_tokens=prompt_tokens,
            output_tokens=10,
        )


class FailingLLMProvider(LLMProvider):
    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        raise LLMProviderError(
            code="LLM_PROVIDER_RATE_LIMIT",
            message=f"Rate limited for model {request.model}",
            retryable=True,
        )


def test_llm_message_rejects_blank_content() -> None:
    with pytest.raises(ValidationError):
        LLMMessage(role="user", content="   ")


def test_llm_generate_request_requires_messages() -> None:
    with pytest.raises(ValidationError):
        LLMGenerateRequest(model="mock-chat", messages=[])


def test_llm_generate_response_rejects_invalid_finish_reason() -> None:
    with pytest.raises(ValidationError):
        LLMGenerateResponse(
            model="mock-chat",
            text="answer",
            finish_reason="other",  # type: ignore[arg-type]
            input_tokens=1,
            output_tokens=1,
        )


def test_llm_provider_contract_success() -> None:
    provider = FakeLLMProvider()
    request = LLMGenerateRequest(
        model="mock-chat",
        messages=[
            LLMMessage(role="system", content="You are a grounded agronomy assistant."),
            LLMMessage(role="user", content="How do I reduce evaporation?"),
        ],
    )

    response = provider.generate(request)

    assert response.model == "mock-chat"
    assert response.finish_reason == "stop"
    assert response.input_tokens > 0
    assert response.output_tokens == 10


def test_llm_provider_error_semantics() -> None:
    provider = FailingLLMProvider()
    request = LLMGenerateRequest(
        model="mock-chat",
        messages=[LLMMessage(role="user", content="When should I irrigate?")],
    )

    with pytest.raises(LLMProviderError) as exc:
        provider.generate(request)

    assert exc.value.code == "LLM_PROVIDER_RATE_LIMIT"
    assert exc.value.retryable is True
    assert "Rate limited" in exc.value.message
