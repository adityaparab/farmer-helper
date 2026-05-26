from farmer_helper.schemas.embedding import EmbeddingItem, EmbeddingRequest, EmbeddingResponse
from farmer_helper.services.embedding.provider import EmbeddingProvider, EmbeddingProviderError


class EmbeddingBatchService:
    def __init__(self, provider: EmbeddingProvider, batch_size: int = 32) -> None:
        if batch_size <= 0:
            raise ValueError("batch_size must be positive")
        self._provider = provider
        self._batch_size = batch_size

    def embed_texts(self, texts: list[str], model: str) -> EmbeddingResponse:
        request = EmbeddingRequest(texts=texts, model=model)

        aggregated_items: list[EmbeddingItem] = []
        expected_dimensions: int | None = None

        for start in range(0, len(request.texts), self._batch_size):
            batch_texts = request.texts[start : start + self._batch_size]
            batch_request = EmbeddingRequest(texts=batch_texts, model=request.model)

            response = self._provider.embed(batch_request)
            self._validate_batch_response(
                response=response, expected_count=len(batch_texts), model=model
            )

            if expected_dimensions is None:
                expected_dimensions = response.dimensions
            elif response.dimensions != expected_dimensions:
                raise EmbeddingProviderError(
                    code="EMBEDDING_PROVIDER_INCONSISTENT_DIMENSIONS",
                    message="Provider returned inconsistent dimensions across batches",
                    retryable=False,
                )

            index_to_item = {item.index: item for item in response.items}
            for local_index in range(len(batch_texts)):
                item = index_to_item[local_index]
                aggregated_items.append(
                    EmbeddingItem(
                        index=start + local_index,
                        vector=item.vector,
                    )
                )

        if expected_dimensions is None:
            raise EmbeddingProviderError(
                code="EMBEDDING_PROVIDER_EMPTY_RESPONSE",
                message="Provider returned no embeddings",
                retryable=False,
            )

        return EmbeddingResponse(
            model=model,
            items=aggregated_items,
            dimensions=expected_dimensions,
        )

    @staticmethod
    def _validate_batch_response(
        response: EmbeddingResponse,
        expected_count: int,
        model: str,
    ) -> None:
        if response.model != model:
            raise EmbeddingProviderError(
                code="EMBEDDING_PROVIDER_MODEL_MISMATCH",
                message="Provider response model does not match request model",
                retryable=False,
            )

        if len(response.items) != expected_count:
            raise EmbeddingProviderError(
                code="EMBEDDING_PROVIDER_INVALID_COUNT",
                message="Provider returned unexpected number of embeddings",
                retryable=False,
            )

        expected_indices = set(range(expected_count))
        returned_indices = {item.index for item in response.items}
        if returned_indices != expected_indices:
            raise EmbeddingProviderError(
                code="EMBEDDING_PROVIDER_INVALID_INDEXES",
                message="Provider returned invalid local embedding indexes",
                retryable=False,
            )
