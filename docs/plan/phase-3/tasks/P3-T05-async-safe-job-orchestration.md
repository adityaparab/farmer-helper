# P3-T05 - Add async-safe job orchestration

## Sub-issue description
### Objective
Provide async-safe embedding orchestration that supports predictable execution boundaries and robust error propagation.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add async embedding orchestration service over batching and retry provider layers.
2. Preserve deterministic mapping between input chunks and persisted embeddings.
3. Add async unit tests for success and failure path behavior.

## Decisions made
- Keep orchestration logic separate from API trigger entrypoints.
- Reuse existing sync services through thread-safe async adapters.
