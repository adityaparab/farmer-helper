# P3-T05 - Add async-safe job orchestration

## Sub-issue description
### Objective
Provide async-safe embedding orchestration that supports predictable execution boundaries and robust error propagation.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added async-safe orchestration service in `src/farmer_helper/services/embedding/orchestration_service.py`.
2. Added orchestration models in `src/farmer_helper/schemas/embedding.py`.
3. Added unit tests in `tests/unit/test_embedding_orchestration_service.py`.

## Decisions made
- Keep orchestration logic separate from API trigger entrypoints.
- Reuse existing sync services through thread-safe async adapters.
