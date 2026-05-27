import time

import pytest

from farmer_helper.schemas.embedding import EmbeddingItem, EmbeddingRequest, EmbeddingResponse
from farmer_helper.services.embedding.provider import EmbeddingProvider, EmbeddingProviderError
from farmer_helper.services.embedding.timeout_provider import (
    EmbeddingTimeoutPolicy,
    TimeoutEmbeddingProvider,
)


class SlowEmbeddingProvider(EmbeddingProvider):
    def __init__(self, delay_seconds: float) -> None:
        self._delay_seconds = delay_seconds

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        time.sleep(self._delay_seconds)
        return EmbeddingResponse(
            model=request.model,
            items=[EmbeddingItem(index=0, vector=[0.1, 0.2])],
            dimensions=2,
        )


class FastEmbeddingProvider(EmbeddingProvider):
    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        return EmbeddingResponse(
            model=request.model,
            items=[EmbeddingItem(index=0, vector=[0.1, 0.2])],
            dimensions=2,
        )


def test_timeout_embedding_provider_returns_response_before_timeout() -> None:
    provider = TimeoutEmbeddingProvider(
        provider=FastEmbeddingProvider(),
        policy=EmbeddingTimeoutPolicy(timeout_seconds=0.05),
    )

    response = provider.embed(EmbeddingRequest(texts=["soil"], model="test-model"))

    assert response.model == "test-model"


def test_timeout_embedding_provider_raises_retryable_timeout_error() -> None:
    provider = TimeoutEmbeddingProvider(
        provider=SlowEmbeddingProvider(delay_seconds=0.03),
        policy=EmbeddingTimeoutPolicy(timeout_seconds=0.005),
    )

    with pytest.raises(EmbeddingProviderError) as exc:
        provider.embed(EmbeddingRequest(texts=["soil"], model="test-model"))

    assert exc.value.code == "EMBEDDING_PROVIDER_TIMEOUT"
    assert exc.value.retryable is True


def test_embedding_timeout_policy_rejects_non_positive_timeout() -> None:
    with pytest.raises(ValueError):
        EmbeddingTimeoutPolicy(timeout_seconds=0)
