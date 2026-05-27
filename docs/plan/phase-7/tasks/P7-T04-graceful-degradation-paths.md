# P7-T04 - Implement graceful degradation paths

## Sub-issue description
### Objective
Implement explicit degraded-response behavior for reliability failures so user-facing APIs remain deterministic and useful when upstream dependencies fail.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added explicit degraded markers to answer and embedding response schemas.
2. Implemented deterministic degraded response behavior in answers route for provider failures.
3. Implemented deterministic degraded response behavior in embeddings route for provider failures.
4. Updated route unit tests to validate degraded behavior.

## Decisions made
- Graceful degradation should build on existing timeout/retry/circuit-breaker/idempotency controls.
- Degradation outputs should remain explicit and testable.
