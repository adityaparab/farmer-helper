# P7-T03 - Add idempotency protections

## Sub-issue description
### Objective
Introduce deterministic idempotency protections for reliability-sensitive operations to prevent duplicate side effects under retries and transient failures.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Identify operations requiring idempotency guards in current external-call workflows.
2. Add idempotency key strategy and persistence/replay behavior.
3. Add unit and integration tests for duplicate-request scenarios.
4. Ensure compatibility with existing timeout/retry/circuit-breaker wrappers.

## Decisions made
- Idempotency behavior must be deterministic and explicit across retries.
- Error and replay semantics should preserve current API contracts.
