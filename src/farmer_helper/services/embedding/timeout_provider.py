from concurrent.futures import ThreadPoolExecutor, TimeoutError
from dataclasses import dataclass

from farmer_helper.schemas.embedding import EmbeddingRequest, EmbeddingResponse
from farmer_helper.services.embedding.provider import EmbeddingProvider, EmbeddingProviderError


@dataclass(frozen=True)
class EmbeddingTimeoutPolicy:
    timeout_seconds: float = 2.0

    def __post_init__(self) -> None:
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")


class TimeoutEmbeddingProvider(EmbeddingProvider):
    def __init__(
        self,
        provider: EmbeddingProvider,
        policy: EmbeddingTimeoutPolicy | None = None,
    ) -> None:
        self._provider = provider
        self._policy = policy or EmbeddingTimeoutPolicy()

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self._provider.embed, request)
            try:
                return future.result(timeout=self._policy.timeout_seconds)
            except TimeoutError as exc:
                raise EmbeddingProviderError(
                    code="EMBEDDING_PROVIDER_TIMEOUT",
                    message=(
                        "Embedding provider call exceeded timeout "
                        f"({self._policy.timeout_seconds:.3f}s)"
                    ),
                    retryable=True,
                ) from exc
