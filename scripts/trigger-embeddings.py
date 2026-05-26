import argparse
import json
from pathlib import Path

from farmer_helper.db.base import SessionLocal
from farmer_helper.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from farmer_helper.schemas.embedding import EmbeddingSourceChunk
from farmer_helper.services.embedding.batch_service import EmbeddingBatchService
from farmer_helper.services.embedding.mock_provider import MockEmbeddingProvider
from farmer_helper.services.embedding.orchestration_service import EmbeddingOrchestrationService
from farmer_helper.services.embedding.retrying_provider import (
    EmbeddingRetryPolicy,
    RetryingEmbeddingProvider,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trigger embedding orchestration from CLI")
    parser.add_argument("--document-id", type=int, required=True)
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--provider", type=str, default="mock-provider")
    parser.add_argument("--version", type=str, default="v1")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--dimensions", type=int, default=8)
    parser.add_argument("--chunks-json", type=Path, required=True)
    return parser.parse_args()


def load_chunks(path: Path) -> list[EmbeddingSourceChunk]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("chunks-json must contain a JSON array")
    return [EmbeddingSourceChunk.model_validate(item) for item in payload]


async def run() -> None:
    args = parse_args()
    chunks = load_chunks(args.chunks_json)

    provider = RetryingEmbeddingProvider(
        provider=MockEmbeddingProvider(dimensions=args.dimensions),
        policy=EmbeddingRetryPolicy(max_attempts=3),
    )
    batch_service = EmbeddingBatchService(provider=provider, batch_size=args.batch_size)

    db = SessionLocal()
    try:
        service = EmbeddingOrchestrationService(
            batch_service=batch_service,
            embedding_repository=ChunkEmbeddingRepository(db),
            provider=args.provider,
            version=args.version,
        )
        result = await service.embed_and_persist(
            document_id=args.document_id,
            model=args.model,
            chunks=chunks,
        )
    finally:
        db.close()

    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
