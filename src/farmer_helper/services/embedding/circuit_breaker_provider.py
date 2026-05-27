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
        """Post init for embedding workflows.

        Initialize EmbeddingCircuitBreakerPolicy for embedding workflows. This operation does
        not require explicit caller-supplied arguments. It runs synchronously and returns when
        local processing is complete. The operation is executed for its side effects and does
        not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
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
        """Init for embedding workflows.

        Initialize CircuitBreakerEmbeddingProvider for embedding workflows. Inputs are provider,
        policy, fallback_provider, now_fn. It runs synchronously and returns when local
        processing is complete. The operation is executed for its side effects and does not
        return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._provider = provider
        self._policy = policy or EmbeddingCircuitBreakerPolicy()
        self._fallback_provider = fallback_provider
        self._now_fn = now_fn or monotonic

        self._state: CircuitState = "closed"
        self._opened_at: float | None = None
        self._consecutive_failures = 0

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Embed for embedding workflows.

        This CircuitBreakerEmbeddingProvider method belongs to the embedding service layer.
        Inputs are request. It runs synchronously and returns when local processing is complete.
        Returns a EmbeddingResponse value that downstream API or orchestration layers can
        consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
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
        """Determine whether should stay open for embedding workflows.

        This private helper belongs to the embedding service layer. This operation does not
        require explicit caller-supplied arguments. It runs synchronously and returns when local
        processing is complete. Returns a bool value that downstream API or orchestration layers
        can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if self._opened_at is None:
            self._opened_at = self._now_fn()
        return (self._now_fn() - self._opened_at) < self._policy.recovery_timeout_seconds

    def _record_failure(self) -> bool:
        """Record failure for embedding workflows.

        This private helper belongs to the embedding service layer. This operation does not
        require explicit caller-supplied arguments. It runs synchronously and returns when local
        processing is complete. Returns a bool value that downstream API or orchestration layers
        can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if self._state == "half_open":
            self._trip_open()
            return True

        self._consecutive_failures += 1
        if self._consecutive_failures >= self._policy.failure_threshold:
            self._trip_open()
            return True
        return False

    def _record_success(self) -> None:
        """Record success for embedding workflows.

        This private helper belongs to the embedding service layer. This operation does not
        require explicit caller-supplied arguments. It runs synchronously and returns when local
        processing is complete. The operation is executed for its side effects and does not
        return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._consecutive_failures = 0
        self._state = "closed"
        self._opened_at = None

    def _trip_open(self) -> None:
        """Trip open for embedding workflows.

        This private helper belongs to the embedding service layer. This operation does not
        require explicit caller-supplied arguments. It runs synchronously and returns when local
        processing is complete. The operation is executed for its side effects and does not
        return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._state = "open"
        self._opened_at = self._now_fn()
        self._consecutive_failures = 0

    def _fallback_or_error(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Fallback or error for embedding workflows.

        This private helper belongs to the embedding service layer. Inputs are request. It runs
        synchronously and returns when local processing is complete. Returns a EmbeddingResponse
        value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if self._fallback_provider is not None:
            return self._fallback_provider.embed(request)
        raise EmbeddingProviderError(
            code="EMBEDDING_CIRCUIT_OPEN",
            message="Embedding circuit breaker is open",
            retryable=True,
        )
