from concurrent.futures import ThreadPoolExecutor, TimeoutError
from dataclasses import dataclass

from farmer_helper.schemas.answering import LLMGenerateRequest, LLMGenerateResponse
from farmer_helper.services.answering.provider import LLMProvider, LLMProviderError


@dataclass(frozen=True)
class LLMTimeoutPolicy:
    timeout_seconds: float = 2.0

    def __post_init__(self) -> None:
        """Post init for answer-generation workflows.

        Initialize LLMTimeoutPolicy for answer-generation workflows. This operation does not
        require explicit caller-supplied arguments. It runs synchronously and returns when local
        processing is complete. The operation is executed for its side effects and does not
        return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")


class TimeoutLLMProvider(LLMProvider):
    def __init__(
        self,
        provider: LLMProvider,
        policy: LLMTimeoutPolicy | None = None,
    ) -> None:
        """Init for answer-generation workflows.

        Initialize TimeoutLLMProvider for answer-generation workflows. Inputs are provider,
        policy. It runs synchronously and returns when local processing is complete. The
        operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._provider = provider
        self._policy = policy or LLMTimeoutPolicy()

    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        """Generate for answer-generation workflows.

        This TimeoutLLMProvider method belongs to the answer-generation service layer. Inputs
        are request. It runs synchronously and returns when local processing is complete.
        Returns a LLMGenerateResponse value that downstream API or orchestration layers can
        consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
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
