from collections.abc import Callable
from dataclasses import dataclass
from time import monotonic
from typing import Literal

from farmer_helper.schemas.answering import LLMGenerateRequest, LLMGenerateResponse
from farmer_helper.services.answering.provider import LLMProvider, LLMProviderError

CircuitState = Literal["closed", "open", "half_open"]


@dataclass(frozen=True)
class LLMCircuitBreakerPolicy:
    failure_threshold: int = 3
    recovery_timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        """Post init for answer-generation workflows.

        Initialize LLMCircuitBreakerPolicy for answer-generation workflows. This operation does
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


class CircuitBreakerLLMProvider(LLMProvider):
    def __init__(
        self,
        provider: LLMProvider,
        policy: LLMCircuitBreakerPolicy | None = None,
        fallback_provider: LLMProvider | None = None,
        now_fn: Callable[[], float] | None = None,
    ) -> None:
        """Init for answer-generation workflows.

        Initialize CircuitBreakerLLMProvider for answer-generation workflows. Inputs are
        provider, policy, fallback_provider, now_fn. It runs synchronously and returns when
        local processing is complete. The operation is executed for its side effects and does
        not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._provider = provider
        self._policy = policy or LLMCircuitBreakerPolicy()
        self._fallback_provider = fallback_provider
        self._now_fn = now_fn or monotonic

        self._state: CircuitState = "closed"
        self._opened_at: float | None = None
        self._consecutive_failures = 0

    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        """Generate for answer-generation workflows.

        This CircuitBreakerLLMProvider method belongs to the answer-generation service layer.
        Inputs are request. It runs synchronously and returns when local processing is complete.
        Returns a LLMGenerateResponse value that downstream API or orchestration layers can
        consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if self._state == "open":
            if self._should_stay_open():
                return self._fallback_or_error(request)
            self._state = "half_open"

        try:
            response = self._provider.generate(request)
        except LLMProviderError:
            if self._record_failure():
                return self._fallback_or_error(request)
            raise

        self._record_success()
        return response

    def _should_stay_open(self) -> bool:
        """Determine whether should stay open for answer-generation workflows.

        This private helper belongs to the answer-generation service layer. This operation does
        not require explicit caller-supplied arguments. It runs synchronously and returns when
        local processing is complete. Returns a bool value that downstream API or orchestration
        layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if self._opened_at is None:
            self._opened_at = self._now_fn()
        return (self._now_fn() - self._opened_at) < self._policy.recovery_timeout_seconds

    def _record_failure(self) -> bool:
        """Record failure for answer-generation workflows.

        This private helper belongs to the answer-generation service layer. This operation does
        not require explicit caller-supplied arguments. It runs synchronously and returns when
        local processing is complete. Returns a bool value that downstream API or orchestration
        layers can consume.

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
        """Record success for answer-generation workflows.

        This private helper belongs to the answer-generation service layer. This operation does
        not require explicit caller-supplied arguments. It runs synchronously and returns when
        local processing is complete. The operation is executed for its side effects and does
        not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._consecutive_failures = 0
        self._state = "closed"
        self._opened_at = None

    def _trip_open(self) -> None:
        """Trip open for answer-generation workflows.

        This private helper belongs to the answer-generation service layer. This operation does
        not require explicit caller-supplied arguments. It runs synchronously and returns when
        local processing is complete. The operation is executed for its side effects and does
        not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._state = "open"
        self._opened_at = self._now_fn()
        self._consecutive_failures = 0

    def _fallback_or_error(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        """Fallback or error for answer-generation workflows.

        This private helper belongs to the answer-generation service layer. Inputs are request.
        It runs synchronously and returns when local processing is complete. Returns a
        LLMGenerateResponse value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if self._fallback_provider is not None:
            return self._fallback_provider.generate(request)
        raise LLMProviderError(
            code="LLM_CIRCUIT_OPEN",
            message="LLM circuit breaker is open",
            retryable=True,
        )
