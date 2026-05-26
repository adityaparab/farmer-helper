# P3-T02 - Add batch embedding logic

## Sub-issue description
### Objective
Implement batch embedding orchestration over provider contracts with deterministic request/response handling.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add batch embedding service that chunks input texts into provider requests.
2. Preserve stable index mapping between source chunks and returned embeddings.
3. Add unit tests for batching boundaries and ordering guarantees.

## Decisions made
- Keep batching logic separate from provider implementation details.
- Preserve deterministic ordering for downstream storage/upsert operations.
