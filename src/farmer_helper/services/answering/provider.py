from abc import ABC, abstractmethod

from farmer_helper.schemas.answering import LLMGenerateRequest, LLMGenerateResponse


class LLMProviderError(Exception):
    def __init__(self, code: str, message: str, retryable: bool) -> None:
        """Init for answer-generation workflows.

        Initialize LLMProviderError for answer-generation workflows. Inputs are code, message,
        retryable. It runs synchronously and returns when local processing is complete. The
        operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        """Generate for answer-generation workflows.

        This LLMProvider method belongs to the answer-generation service layer. Inputs are
        request. It runs synchronously and returns when local processing is complete. Returns a
        LLMGenerateResponse value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        raise NotImplementedError
