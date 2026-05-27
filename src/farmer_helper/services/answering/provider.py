from abc import ABC, abstractmethod

from farmer_helper.schemas.answering import LLMGenerateRequest, LLMGenerateResponse


class LLMProviderError(Exception):
    def __init__(self, code: str, message: str, retryable: bool) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        raise NotImplementedError
