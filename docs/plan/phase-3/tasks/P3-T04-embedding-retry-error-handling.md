# P3-T04 - Add retry and error handling for embedding jobs

## Sub-issue description
### Objective
Add deterministic retry handling and explicit error semantics for embedding provider failures.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add retry policy abstraction for embedding calls.
2. Implement retry-aware embedding execution service.
3. Add tests for retryable vs non-retryable provider errors and exhaustion behavior.

## Decisions made
- Retry behavior must be deterministic and bounded.
- Non-retryable errors should fail fast with clear error codes.
