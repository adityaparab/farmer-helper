import pytest

from farmer_helper.schemas.answering import LLMGenerateRequest, LLMGenerateResponse, LLMMessage
from farmer_helper.services.answering.circuit_breaker_provider import (
    CircuitBreakerLLMProvider,
    LLMCircuitBreakerPolicy,
)
from farmer_helper.services.answering.provider import LLMProvider, LLMProviderError


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0

    def advance(self, seconds: float) -> None:
        self.now += seconds

    def __call__(self) -> float:
        return self.now


class AlwaysFailProvider(LLMProvider):
    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        raise LLMProviderError(
            code="LLM_PROVIDER_UNAVAILABLE",
            message="provider unavailable",
            retryable=True,
        )


class SwitchableProvider(LLMProvider):
    def __init__(self) -> None:
        self.fail = True

    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        if self.fail:
            raise LLMProviderError(
                code="LLM_PROVIDER_UNAVAILABLE",
                message="provider unavailable",
                retryable=True,
            )
        return LLMGenerateResponse(
            model=request.model,
            text="primary-ok",
            finish_reason="stop",
            input_tokens=1,
            output_tokens=1,
        )


class FallbackProvider(LLMProvider):
    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        return LLMGenerateResponse(
            model=request.model,
            text="fallback-ok",
            finish_reason="stop",
            input_tokens=1,
            output_tokens=1,
        )


def _request() -> LLMGenerateRequest:
    return LLMGenerateRequest(
        model="mock-chat-v1",
        messages=[LLMMessage(role="user", content="hello")],
    )


def test_llm_circuit_breaker_opens_and_uses_fallback() -> None:
    clock = FakeClock()
    provider = CircuitBreakerLLMProvider(
        provider=AlwaysFailProvider(),
        policy=LLMCircuitBreakerPolicy(failure_threshold=2, recovery_timeout_seconds=10.0),
        fallback_provider=FallbackProvider(),
        now_fn=clock,
    )

    with pytest.raises(LLMProviderError):
        provider.generate(_request())

    response = provider.generate(_request())
    assert response.text == "fallback-ok"


def test_llm_circuit_breaker_half_open_recovery_closes_on_success() -> None:
    clock = FakeClock()
    primary = SwitchableProvider()
    provider = CircuitBreakerLLMProvider(
        provider=primary,
        policy=LLMCircuitBreakerPolicy(failure_threshold=1, recovery_timeout_seconds=5.0),
        fallback_provider=FallbackProvider(),
        now_fn=clock,
    )

    fallback_response = provider.generate(_request())
    assert fallback_response.text == "fallback-ok"

    clock.advance(5.1)
    primary.fail = False

    recovered = provider.generate(_request())
    assert recovered.text == "primary-ok"


def test_llm_circuit_breaker_raises_when_open_and_no_fallback() -> None:
    clock = FakeClock()
    provider = CircuitBreakerLLMProvider(
        provider=AlwaysFailProvider(),
        policy=LLMCircuitBreakerPolicy(failure_threshold=1, recovery_timeout_seconds=10.0),
        fallback_provider=None,
        now_fn=clock,
    )

    with pytest.raises(LLMProviderError) as first_error:
        provider.generate(_request())
    assert first_error.value.code == "LLM_CIRCUIT_OPEN"

    with pytest.raises(LLMProviderError) as open_error:
        provider.generate(_request())
    assert open_error.value.code == "LLM_CIRCUIT_OPEN"


def test_llm_circuit_breaker_policy_validates_values() -> None:
    with pytest.raises(ValueError):
        LLMCircuitBreakerPolicy(failure_threshold=0)

    with pytest.raises(ValueError):
        LLMCircuitBreakerPolicy(recovery_timeout_seconds=0)
