from dataclasses import dataclass

from farmer_helper.schemas.embedding import EmbeddingRequest, EmbeddingResponse
from farmer_helper.services.embedding.provider import EmbeddingProvider, EmbeddingProviderError


@dataclass(frozen=True)
class EmbeddingRetryPolicy:
    max_attempts: int = 3

    def __post_init__(self) -> None:
        """Post init for embedding workflows.

        Initialize EmbeddingRetryPolicy for embedding workflows. This operation does not require
        explicit caller-supplied arguments. It runs synchronously and returns when local
        processing is complete. The operation is executed for its side effects and does not
        return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if self.max_attempts <= 0:
            raise ValueError("max_attempts must be positive")


class RetryingEmbeddingProvider(EmbeddingProvider):
    def __init__(
        self,
        provider: EmbeddingProvider,
        policy: EmbeddingRetryPolicy | None = None,
    ) -> None:
        """Init for embedding workflows.

        Initialize RetryingEmbeddingProvider for embedding workflows. Inputs are provider,
        policy. It runs synchronously and returns when local processing is complete. The
        operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._provider = provider
        self._policy = policy or EmbeddingRetryPolicy()

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Embed for embedding workflows.

        This RetryingEmbeddingProvider method belongs to the embedding service layer. Inputs are
        request. It runs synchronously and returns when local processing is complete. Returns a
        EmbeddingResponse value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        last_error: EmbeddingProviderError | None = None

        for attempt in range(1, self._policy.max_attempts + 1):
            try:
                return self._provider.embed(request)
            except EmbeddingProviderError as exc:
                if not exc.retryable:
                    raise
                last_error = exc
                if attempt == self._policy.max_attempts:
                    break

        if last_error is None:
            raise RuntimeError("Retry loop exhausted without provider error")
        raise EmbeddingProviderError(
            code="EMBEDDING_RETRIES_EXHAUSTED",
            message=(
                f"Retries exhausted after {self._policy.max_attempts} attempts: "
                f"{last_error.code}"
            ),
            retryable=False,
        )
