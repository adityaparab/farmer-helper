# P7-T05 - Normalize internal-to-user error responses

## Sub-issue description
### Objective
Normalize reliability-related error and degradation contracts so user-facing API responses are stable, explicit, and consistent across routes.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added normalized reliability status/code/retryable fields in answer and embedding response schemas.
2. Added shared reliability error-detail helper in `src/farmer_helper/services/reliability/response_contracts.py`.
3. Applied shared error-detail contract to idempotency conflict responses in answers and embeddings routes.
4. Updated degraded response paths to include normalized reliability fields.
5. Extended route tests to assert normalized degraded and error-detail fields.

## Decisions made
- Normalization should preserve deterministic behavior and existing success payload compatibility.
- Error/degradation semantics should be route-consistent.
