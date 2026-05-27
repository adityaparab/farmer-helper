from concurrent.futures import ThreadPoolExecutor, TimeoutError
from dataclasses import dataclass

from farmer_helper.schemas.answering import LLMGenerateRequest, LLMGenerateResponse
from farmer_helper.services.answering.provider import LLMProvider, LLMProviderError


@dataclass(frozen=True)
class LLMTimeoutPolicy:
    timeout_seconds: float = 2.0

    def __post_init__(self) -> None:
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")


class TimeoutLLMProvider(LLMProvider):
    def __init__(
        self,
        provider: LLMProvider,
        policy: LLMTimeoutPolicy | None = None,
    ) -> None:
        self._provider = provider
        self._policy = policy or LLMTimeoutPolicy()

    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self._provider.generate, request)
            try:
                return future.result(timeout=self._policy.timeout_seconds)
            except TimeoutError as exc:
                raise LLMProviderError(
                    code="LLM_PROVIDER_TIMEOUT",
                    message=(
                        "LLM provider call exceeded timeout "
                        f"({self._policy.timeout_seconds:.3f}s)"
                    ),
                    retryable=True,
                ) from exc
