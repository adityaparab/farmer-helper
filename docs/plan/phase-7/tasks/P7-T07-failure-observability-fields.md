# P7-T07 - Add failure observability fields

## Sub-issue description
### Objective
Add structured observability fields for reliability failures and degraded outcomes so operational analysis can distinguish retry, timeout, circuit-open, and idempotency conflict paths.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added structured reliability log events for degraded outcomes and idempotency conflicts in answers and embeddings routes.
2. Added stable observability fields: route, reliability_status, reliability_code, reliability_retryable.
3. Added route-level tests that assert observability log emission and field values.
4. Kept observability identifiers low-cardinality and deterministic.

## Decisions made
- Observability fields should align with normalized reliability contract codes.
- Logging additions must preserve request correlation context.
