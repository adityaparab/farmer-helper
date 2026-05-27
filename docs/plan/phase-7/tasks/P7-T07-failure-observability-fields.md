# P7-T07 - Add failure observability fields

## Sub-issue description
### Objective
Add structured observability fields for reliability failures and degraded outcomes so operational analysis can distinguish retry, timeout, circuit-open, and idempotency conflict paths.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add structured reliability observability fields to relevant logs.
2. Ensure degraded and conflict outcomes emit stable, queryable identifiers.
3. Add tests for observability payload field presence/values.
4. Keep observability fields low-cardinality and deterministic.

## Decisions made
- Observability fields should align with normalized reliability contract codes.
- Logging additions must preserve request correlation context.
