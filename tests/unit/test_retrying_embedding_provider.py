import pytest

from farmer_helper.schemas.embedding import EmbeddingItem, EmbeddingRequest, EmbeddingResponse
from farmer_helper.services.embedding.provider import EmbeddingProvider, EmbeddingProviderError
from farmer_helper.services.embedding.retrying_provider import (
    EmbeddingRetryPolicy,
    RetryingEmbeddingProvider,
)


class FlakyRetryableProvider(EmbeddingProvider):
    def __init__(self, fail_attempts: int) -> None:
        self._fail_attempts = fail_attempts
        self.calls = 0

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        self.calls += 1
        if self.calls <= self._fail_attempts:
            raise EmbeddingProviderError(
                code="EMBEDDING_PROVIDER_RATE_LIMIT",
                message="rate limited",
                retryable=True,
            )
        items = [
            EmbeddingItem(index=index, vector=[float(index), float(len(text))])
            for index, text in enumerate(request.texts)
        ]
        return EmbeddingResponse(model=request.model, items=items, dimensions=2)


class NonRetryableProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self.calls = 0

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        self.calls += 1
        raise EmbeddingProviderError(
            code="EMBEDDING_PROVIDER_INVALID_REQUEST",
            message="invalid request",
            retryable=False,
        )


def test_retrying_provider_retries_and_succeeds() -> None:
    provider = FlakyRetryableProvider(fail_attempts=2)
    retrying = RetryingEmbeddingProvider(provider, policy=EmbeddingRetryPolicy(max_attempts=3))

    response = retrying.embed(EmbeddingRequest(texts=["soil"], model="test-model"))

    assert provider.calls == 3
    assert response.model == "test-model"
    assert len(response.items) == 1


def test_retrying_provider_fails_fast_for_non_retryable_error() -> None:
    provider = NonRetryableProvider()
    retrying = RetryingEmbeddingProvider(provider, policy=EmbeddingRetryPolicy(max_attempts=5))

    with pytest.raises(EmbeddingProviderError) as exc:
        retrying.embed(EmbeddingRequest(texts=["soil"], model="test-model"))

    assert provider.calls == 1
    assert exc.value.code == "EMBEDDING_PROVIDER_INVALID_REQUEST"


def test_retrying_provider_raises_retries_exhausted() -> None:
    provider = FlakyRetryableProvider(fail_attempts=5)
    retrying = RetryingEmbeddingProvider(provider, policy=EmbeddingRetryPolicy(max_attempts=3))

    with pytest.raises(EmbeddingProviderError) as exc:
        retrying.embed(EmbeddingRequest(texts=["soil"], model="test-model"))

    assert provider.calls == 3
    assert exc.value.code == "EMBEDDING_RETRIES_EXHAUSTED"
    assert exc.value.retryable is False


def test_retry_policy_rejects_non_positive_attempts() -> None:
    with pytest.raises(ValueError):
        EmbeddingRetryPolicy(max_attempts=0)
