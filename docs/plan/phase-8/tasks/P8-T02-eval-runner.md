# P8-T02 - Build eval runner

## Sub-issue description
### Objective
Implement an offline deterministic eval runner that executes retrieval/answer checks against dataset items and produces typed result records for reporting.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Define eval runner request/result schemas.
2. Build deterministic runner service over loaded dataset items.
3. Add tests for aggregation and stable ordering.
4. Keep output contract suitable for reporting and CI integration.

## Decisions made
- Runner should consume typed dataset loader outputs from P8-T01.
- Result records should include enough detail for future reporting metrics.
