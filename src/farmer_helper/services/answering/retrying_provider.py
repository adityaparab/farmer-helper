from dataclasses import dataclass

from farmer_helper.schemas.answering import LLMGenerateRequest, LLMGenerateResponse
from farmer_helper.services.answering.provider import LLMProvider, LLMProviderError


@dataclass(frozen=True)
class LLMRetryPolicy:
    max_attempts: int = 3

    def __post_init__(self) -> None:
        """Post init for answer-generation workflows.

        Initialize LLMRetryPolicy for answer-generation workflows. This operation does not
        require explicit caller-supplied arguments. It runs synchronously and returns when local
        processing is complete. The operation is executed for its side effects and does not
        return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if self.max_attempts <= 0:
            raise ValueError("max_attempts must be positive")


class RetryingLLMProvider(LLMProvider):
    def __init__(
        self,
        provider: LLMProvider,
        policy: LLMRetryPolicy | None = None,
    ) -> None:
        """Init for answer-generation workflows.

        Initialize RetryingLLMProvider for answer-generation workflows. Inputs are provider,
        policy. It runs synchronously and returns when local processing is complete. The
        operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._provider = provider
        self._policy = policy or LLMRetryPolicy()

    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        """Generate for answer-generation workflows.

        This RetryingLLMProvider method belongs to the answer-generation service layer. Inputs
        are request. It runs synchronously and returns when local processing is complete.
        Returns a LLMGenerateResponse value that downstream API or orchestration layers can
        consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        last_error: LLMProviderError | None = None

        for attempt in range(1, self._policy.max_attempts + 1):
            try:
                return self._provider.generate(request)
            except LLMProviderError as exc:
                if not exc.retryable:
                    raise
                last_error = exc
                if attempt == self._policy.max_attempts:
                    break

        if last_error is None:
            raise RuntimeError("Retry loop exhausted without provider error")
        raise LLMProviderError(
            code="LLM_RETRIES_EXHAUSTED",
            message=(
                f"Retries exhausted after {self._policy.max_attempts} attempts: "
                f"{last_error.code}"
            ),
            retryable=False,
        )
