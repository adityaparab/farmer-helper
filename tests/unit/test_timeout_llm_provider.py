import time

import pytest

from farmer_helper.schemas.answering import LLMGenerateRequest, LLMGenerateResponse, LLMMessage
from farmer_helper.services.answering.provider import LLMProvider, LLMProviderError
from farmer_helper.services.answering.timeout_provider import LLMTimeoutPolicy, TimeoutLLMProvider


class SlowLLMProvider(LLMProvider):
    def __init__(self, delay_seconds: float) -> None:
        self._delay_seconds = delay_seconds

    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        time.sleep(self._delay_seconds)
        return LLMGenerateResponse(
            model=request.model,
            text="done",
            finish_reason="stop",
            input_tokens=1,
            output_tokens=1,
        )


class FastLLMProvider(LLMProvider):
    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        return LLMGenerateResponse(
            model=request.model,
            text="ok",
            finish_reason="stop",
            input_tokens=1,
            output_tokens=1,
        )


def _request() -> LLMGenerateRequest:
    return LLMGenerateRequest(
        model="mock-chat-v1",
        messages=[LLMMessage(role="user", content="hello")],
    )


def test_timeout_llm_provider_returns_response_before_timeout() -> None:
    provider = TimeoutLLMProvider(
        provider=FastLLMProvider(),
        policy=LLMTimeoutPolicy(timeout_seconds=0.05),
    )

    response = provider.generate(_request())

    assert response.text == "ok"


def test_timeout_llm_provider_raises_retryable_timeout_error() -> None:
    provider = TimeoutLLMProvider(
        provider=SlowLLMProvider(delay_seconds=0.03),
        policy=LLMTimeoutPolicy(timeout_seconds=0.005),
    )

    with pytest.raises(LLMProviderError) as exc:
        provider.generate(_request())

    assert exc.value.code == "LLM_PROVIDER_TIMEOUT"
    assert exc.value.retryable is True


def test_llm_timeout_policy_rejects_non_positive_timeout() -> None:
    with pytest.raises(ValueError):
        LLMTimeoutPolicy(timeout_seconds=0)
