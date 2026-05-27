# P7-T05 - Normalize internal-to-user error responses

## Sub-issue description
### Objective
Normalize reliability-related error and degradation contracts so user-facing API responses are stable, explicit, and consistent across routes.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Define canonical reliability error/degradation response shape.
2. Align answers and embeddings route reliability responses to the canonical shape.
3. Add regression tests for normalized response fields.
4. Ensure compatibility with idempotency conflict handling and existing route contracts.

## Decisions made
- Normalization should preserve deterministic behavior and existing success payload compatibility.
- Error/degradation semantics should be route-consistent.
