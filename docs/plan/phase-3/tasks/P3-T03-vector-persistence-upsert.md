# P3-T03 - Extend schema for vector persistence/upsert

## Sub-issue description
### Objective
Extend persistence models and migration path for storing embedding vectors with idempotent upsert semantics.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added embedding persistence model `ChunkEmbedding` in `src/farmer_helper/db/models/foundation.py`.
2. Added migration `alembic/versions/20260527_0002_embedding_vector_schema.py`.
3. Added upsert/list repository operations in `src/farmer_helper/repositories/chunk_embedding_repository.py`.
4. Added unit tests in `tests/unit/test_chunk_embedding_repository.py`.

## Decisions made
- Keep persistence schema compatible with pgvector target integration.
- Design upsert semantics around stable chunk/document identity.
