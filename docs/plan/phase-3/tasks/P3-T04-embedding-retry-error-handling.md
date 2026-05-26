# P3-T04 - Add retry and error handling for embedding jobs

## Sub-issue description
### Objective
Add deterministic retry handling and explicit error semantics for embedding provider failures.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added retry policy and wrapper provider in `src/farmer_helper/services/embedding/retrying_provider.py`.
2. Implemented bounded deterministic retry execution for provider calls.
3. Added tests in `tests/unit/test_retrying_embedding_provider.py` for retry success, fail-fast, and exhaustion behavior.

## Decisions made
- Retry behavior must be deterministic and bounded.
- Non-retryable errors should fail fast with clear error codes.
