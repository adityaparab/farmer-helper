# P3-T03 - Extend schema for vector persistence/upsert

## Sub-issue description
### Objective
Extend persistence models and migration path for storing embedding vectors with idempotent upsert semantics.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add embedding vector persistence model and relation to documents/chunks.
2. Add migration changes for vector storage and upsert keys.
3. Add repository operations for insert/upsert retrieval paths.

## Decisions made
- Keep persistence schema compatible with pgvector target integration.
- Design upsert semantics around stable chunk/document identity.
