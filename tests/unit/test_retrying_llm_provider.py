import pytest

from farmer_helper.schemas.answering import LLMGenerateRequest, LLMGenerateResponse, LLMMessage
from farmer_helper.services.answering.provider import LLMProvider, LLMProviderError
from farmer_helper.services.answering.retrying_provider import LLMRetryPolicy, RetryingLLMProvider


class FlakyRetryableProvider(LLMProvider):
    def __init__(self, fail_attempts: int) -> None:
        self._fail_attempts = fail_attempts
        self.calls = 0

    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        self.calls += 1
        if self.calls <= self._fail_attempts:
            raise LLMProviderError(
                code="LLM_PROVIDER_RATE_LIMIT",
                message="rate limited",
                retryable=True,
            )
        return LLMGenerateResponse(
            model=request.model,
            text="grounded answer",
            finish_reason="stop",
            input_tokens=2,
            output_tokens=2,
        )


class NonRetryableProvider(LLMProvider):
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        self.calls += 1
        raise LLMProviderError(
            code="LLM_PROVIDER_INVALID_REQUEST",
            message="invalid request",
            retryable=False,
        )


def _request() -> LLMGenerateRequest:
    return LLMGenerateRequest(
        model="mock-chat-v1",
        messages=[LLMMessage(role="user", content="hello")],
    )


def test_retrying_llm_provider_retries_and_succeeds() -> None:
    provider = FlakyRetryableProvider(fail_attempts=2)
    retrying = RetryingLLMProvider(provider, policy=LLMRetryPolicy(max_attempts=3))

    response = retrying.generate(_request())

    assert provider.calls == 3
    assert response.text == "grounded answer"


def test_retrying_llm_provider_fails_fast_for_non_retryable_error() -> None:
    provider = NonRetryableProvider()
    retrying = RetryingLLMProvider(provider, policy=LLMRetryPolicy(max_attempts=5))

    with pytest.raises(LLMProviderError) as exc:
        retrying.generate(_request())

    assert provider.calls == 1
    assert exc.value.code == "LLM_PROVIDER_INVALID_REQUEST"


def test_retrying_llm_provider_raises_retries_exhausted() -> None:
    provider = FlakyRetryableProvider(fail_attempts=5)
    retrying = RetryingLLMProvider(provider, policy=LLMRetryPolicy(max_attempts=3))

    with pytest.raises(LLMProviderError) as exc:
        retrying.generate(_request())

    assert provider.calls == 3
    assert exc.value.code == "LLM_RETRIES_EXHAUSTED"
    assert exc.value.retryable is False


def test_llm_retry_policy_rejects_non_positive_attempts() -> None:
    with pytest.raises(ValueError):
        LLMRetryPolicy(max_attempts=0)
