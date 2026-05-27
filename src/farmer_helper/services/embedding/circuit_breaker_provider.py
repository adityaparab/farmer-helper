from collections.abc import Callable
from dataclasses import dataclass
from time import monotonic
from typing import Literal

from farmer_helper.schemas.embedding import EmbeddingRequest, EmbeddingResponse
from farmer_helper.services.embedding.provider import EmbeddingProvider, EmbeddingProviderError

CircuitState = Literal["closed", "open", "half_open"]


@dataclass(frozen=True)
class EmbeddingCircuitBreakerPolicy:
    failure_threshold: int = 3
    recovery_timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        if self.failure_threshold <= 0:
            raise ValueError("failure_threshold must be positive")
        if self.recovery_timeout_seconds <= 0:
            raise ValueError("recovery_timeout_seconds must be positive")


class CircuitBreakerEmbeddingProvider(EmbeddingProvider):
    def __init__(
        self,
        provider: EmbeddingProvider,
        policy: EmbeddingCircuitBreakerPolicy | None = None,
        fallback_provider: EmbeddingProvider | None = None,
        now_fn: Callable[[], float] | None = None,
    ) -> None:
        self._provider = provider
        self._policy = policy or EmbeddingCircuitBreakerPolicy()
        self._fallback_provider = fallback_provider
        self._now_fn = now_fn or monotonic

        self._state: CircuitState = "closed"
        self._opened_at: float | None = None
        self._consecutive_failures = 0

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        if self._state == "open":
            if self._should_stay_open():
                return self._fallback_or_error(request)
            self._state = "half_open"

        try:
            response = self._provider.embed(request)
        except EmbeddingProviderError:
            if self._record_failure():
                return self._fallback_or_error(request)
            raise

        self._record_success()
        return response

    def _should_stay_open(self) -> bool:
        if self._opened_at is None:
            self._opened_at = self._now_fn()
        return (self._now_fn() - self._opened_at) < self._policy.recovery_timeout_seconds

    def _record_failure(self) -> bool:
        if self._state == "half_open":
            self._trip_open()
            return True

        self._consecutive_failures += 1
        if self._consecutive_failures >= self._policy.failure_threshold:
            self._trip_open()
            return True
        return False

    def _record_success(self) -> None:
        self._consecutive_failures = 0
        self._state = "closed"
        self._opened_at = None

    def _trip_open(self) -> None:
        self._state = "open"
        self._opened_at = self._now_fn()
        self._consecutive_failures = 0

    def _fallback_or_error(self, request: EmbeddingRequest) -> EmbeddingResponse:
        if self._fallback_provider is not None:
            return self._fallback_provider.embed(request)
        raise EmbeddingProviderError(
            code="EMBEDDING_CIRCUIT_OPEN",
            message="Embedding circuit breaker is open",
            retryable=True,
        )
