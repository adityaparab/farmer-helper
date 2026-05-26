from dataclasses import dataclass

from farmer_helper.schemas.embedding import EmbeddingRequest, EmbeddingResponse
from farmer_helper.services.embedding.provider import EmbeddingProvider, EmbeddingProviderError


@dataclass(frozen=True)
class EmbeddingRetryPolicy:
    max_attempts: int = 3

    def __post_init__(self) -> None:
        if self.max_attempts <= 0:
            raise ValueError("max_attempts must be positive")


class RetryingEmbeddingProvider(EmbeddingProvider):
    def __init__(
        self,
        provider: EmbeddingProvider,
        policy: EmbeddingRetryPolicy | None = None,
    ) -> None:
        self._provider = provider
        self._policy = policy or EmbeddingRetryPolicy()

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
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
