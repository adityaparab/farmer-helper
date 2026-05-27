import pytest

from farmer_helper.schemas.embedding import EmbeddingItem, EmbeddingRequest, EmbeddingResponse
from farmer_helper.services.embedding.circuit_breaker_provider import (
    CircuitBreakerEmbeddingProvider,
    EmbeddingCircuitBreakerPolicy,
)
from farmer_helper.services.embedding.provider import EmbeddingProvider, EmbeddingProviderError


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0

    def advance(self, seconds: float) -> None:
        self.now += seconds

    def __call__(self) -> float:
        return self.now


class AlwaysFailProvider(EmbeddingProvider):
    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        raise EmbeddingProviderError(
            code="EMBEDDING_PROVIDER_UNAVAILABLE",
            message="provider unavailable",
            retryable=True,
        )


class SwitchableProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self.fail = True

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        if self.fail:
            raise EmbeddingProviderError(
                code="EMBEDDING_PROVIDER_UNAVAILABLE",
                message="provider unavailable",
                retryable=True,
            )
        return EmbeddingResponse(
            model=request.model,
            items=[EmbeddingItem(index=0, vector=[0.1, 0.2])],
            dimensions=2,
        )


class FallbackProvider(EmbeddingProvider):
    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        return EmbeddingResponse(
            model=request.model,
            items=[EmbeddingItem(index=0, vector=[0.3, 0.4])],
            dimensions=2,
        )


def _request() -> EmbeddingRequest:
    return EmbeddingRequest(texts=["soil"], model="embed-v1")


def test_embedding_circuit_breaker_opens_and_uses_fallback() -> None:
    clock = FakeClock()
    provider = CircuitBreakerEmbeddingProvider(
        provider=AlwaysFailProvider(),
        policy=EmbeddingCircuitBreakerPolicy(failure_threshold=2, recovery_timeout_seconds=10.0),
        fallback_provider=FallbackProvider(),
        now_fn=clock,
    )

    with pytest.raises(EmbeddingProviderError):
        provider.embed(_request())

    response = provider.embed(_request())
    assert response.items[0].vector == [0.3, 0.4]


def test_embedding_circuit_breaker_half_open_recovery_closes_on_success() -> None:
    clock = FakeClock()
    primary = SwitchableProvider()
    provider = CircuitBreakerEmbeddingProvider(
        provider=primary,
        policy=EmbeddingCircuitBreakerPolicy(failure_threshold=1, recovery_timeout_seconds=5.0),
        fallback_provider=FallbackProvider(),
        now_fn=clock,
    )

    fallback_response = provider.embed(_request())
    assert fallback_response.items[0].vector == [0.3, 0.4]

    clock.advance(5.1)
    primary.fail = False

    recovered = provider.embed(_request())
    assert recovered.items[0].vector == [0.1, 0.2]


def test_embedding_circuit_breaker_raises_when_open_and_no_fallback() -> None:
    clock = FakeClock()
    provider = CircuitBreakerEmbeddingProvider(
        provider=AlwaysFailProvider(),
        policy=EmbeddingCircuitBreakerPolicy(failure_threshold=1, recovery_timeout_seconds=10.0),
        fallback_provider=None,
        now_fn=clock,
    )

    with pytest.raises(EmbeddingProviderError) as first_error:
        provider.embed(_request())
    assert first_error.value.code == "EMBEDDING_CIRCUIT_OPEN"

    with pytest.raises(EmbeddingProviderError) as open_error:
        provider.embed(_request())
    assert open_error.value.code == "EMBEDDING_CIRCUIT_OPEN"


def test_embedding_circuit_breaker_policy_validates_values() -> None:
    with pytest.raises(ValueError):
        EmbeddingCircuitBreakerPolicy(failure_threshold=0)

    with pytest.raises(ValueError):
        EmbeddingCircuitBreakerPolicy(recovery_timeout_seconds=0)
