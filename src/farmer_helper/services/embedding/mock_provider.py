import hashlib

from farmer_helper.schemas.embedding import EmbeddingItem, EmbeddingRequest, EmbeddingResponse
from farmer_helper.services.embedding.provider import EmbeddingProvider


class MockEmbeddingProvider(EmbeddingProvider):
    def __init__(self, dimensions: int = 8) -> None:
        """Init for embedding workflows.

        Initialize MockEmbeddingProvider for embedding workflows. Inputs are dimensions. It runs
        synchronously and returns when local processing is complete. The operation is executed
        for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if dimensions <= 0:
            raise ValueError("dimensions must be positive")
        self._dimensions = dimensions

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Embed for embedding workflows.

        This MockEmbeddingProvider method belongs to the embedding service layer. Inputs are
        request. It runs synchronously and returns when local processing is complete. Returns a
        EmbeddingResponse value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        items = [
            EmbeddingItem(index=index, vector=self._vector_for_text(text))
            for index, text in enumerate(request.texts)
        ]
        return EmbeddingResponse(model=request.model, items=items, dimensions=self._dimensions)

    def _vector_for_text(self, text: str) -> list[float]:
        """Vector for text for embedding workflows.

        This private helper belongs to the embedding service layer. Inputs are text. It runs
        synchronously and returns when local processing is complete. Returns a list[float] value
        that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        vector: list[float] = []
        for i in range(self._dimensions):
            byte_value = digest[i % len(digest)]
            vector.append(byte_value / 255.0)
        return vector
