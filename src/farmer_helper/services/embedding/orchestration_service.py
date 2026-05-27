import asyncio

from farmer_helper.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from farmer_helper.schemas.embedding import EmbeddingOrchestrationResult, EmbeddingSourceChunk
from farmer_helper.services.embedding.batch_service import EmbeddingBatchService


class EmbeddingOrchestrationService:
    def __init__(
        self,
        batch_service: EmbeddingBatchService,
        embedding_repository: ChunkEmbeddingRepository,
        provider: str,
        version: str = "v1",
    ) -> None:
        """Init for embedding workflows.

        Initialize EmbeddingOrchestrationService for embedding workflows. Inputs are
        batch_service, embedding_repository, provider, version. It runs synchronously and
        returns when local processing is complete. The operation is executed for its side
        effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._batch_service = batch_service
        self._embedding_repository = embedding_repository
        self._provider = provider
        self._version = version
        self._lock = asyncio.Lock()

    async def embed_and_persist(
        self,
        document_id: int,
        model: str,
        chunks: list[EmbeddingSourceChunk],
    ) -> EmbeddingOrchestrationResult:
        """Embed and persist for embedding workflows.

        This EmbeddingOrchestrationService method belongs to the embedding service layer. Inputs
        are document_id, model, chunks. It may await provider, database, or orchestration work
        before returning. Returns a EmbeddingOrchestrationResult value that downstream API or
        orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if not chunks:
            raise ValueError("chunks must not be empty")

        ordered_chunks = sorted(chunks, key=lambda item: item.chunk_index)

        async with self._lock:
            response = self._batch_service.embed_texts(
                texts=[chunk.text for chunk in ordered_chunks],
                model=model,
            )

            for item in response.items:
                source_chunk = ordered_chunks[item.index]
                self._embedding_repository.upsert(
                    document_id=document_id,
                    chunk_index=source_chunk.chunk_index,
                    provider=self._provider,
                    model=model,
                    version=self._version,
                    dimensions=response.dimensions,
                    vector=item.vector,
                    content_hash=source_chunk.content_hash,
                    chunk_text=source_chunk.text,
                )

            return EmbeddingOrchestrationResult(
                document_id=document_id,
                model=model,
                provider=self._provider,
                version=self._version,
                dimensions=response.dimensions,
                persisted_count=len(response.items),
            )
