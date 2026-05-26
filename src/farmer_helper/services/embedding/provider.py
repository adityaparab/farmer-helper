from abc import ABC, abstractmethod

from farmer_helper.schemas.embedding import EmbeddingRequest, EmbeddingResponse


class EmbeddingProviderError(Exception):
    def __init__(self, code: str, message: str, retryable: bool) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        raise NotImplementedError
