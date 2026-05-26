# P4-T01 - Implement vector retrieval

## Sub-issue description
### Objective
Implement baseline vector retrieval over persisted embedding records with top-k scoring and deterministic ordering.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added retrieval schemas in `src/farmer_helper/schemas/retrieval.py`.
2. Added repository retrieval candidate query in `src/farmer_helper/repositories/chunk_embedding_repository.py`.
3. Added vector retrieval scoring service in `src/farmer_helper/services/retrieval/vector_retrieval_service.py`.
4. Added unit tests in `tests/unit/test_vector_retrieval_service.py`.

## Decisions made
- Start with deterministic distance scoring over stored vectors.
- Keep retrieval interfaces provider-agnostic.
