from abc import ABC, abstractmethod

from farmer_helper.schemas.embedding import EmbeddingRequest, EmbeddingResponse


class EmbeddingProviderError(Exception):
    def __init__(self, code: str, message: str, retryable: bool) -> None:
        """Init for embedding workflows.

        Initialize EmbeddingProviderError for embedding workflows. Inputs are code, message,
        retryable. It runs synchronously and returns when local processing is complete. The
        operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Embed for embedding workflows.

        This EmbeddingProvider method belongs to the embedding service layer. Inputs are
        request. It runs synchronously and returns when local processing is complete. Returns a
        EmbeddingResponse value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        raise NotImplementedError
