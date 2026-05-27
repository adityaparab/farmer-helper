from dataclasses import dataclass

from farmer_helper.schemas.answering import LLMGenerateRequest, LLMGenerateResponse
from farmer_helper.services.answering.provider import LLMProvider, LLMProviderError


@dataclass(frozen=True)
class LLMRetryPolicy:
    max_attempts: int = 3

    def __post_init__(self) -> None:
        if self.max_attempts <= 0:
            raise ValueError("max_attempts must be positive")


class RetryingLLMProvider(LLMProvider):
    def __init__(
        self,
        provider: LLMProvider,
        policy: LLMRetryPolicy | None = None,
    ) -> None:
        self._provider = provider
        self._policy = policy or LLMRetryPolicy()

    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
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
