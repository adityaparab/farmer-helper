# P4-T01 - Implement vector retrieval

## Sub-issue description
### Objective
Implement baseline vector retrieval over persisted embedding records with top-k scoring and deterministic ordering.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add retrieval request/response schemas for vector search.
2. Add repository-level vector retrieval query path.
3. Add service-level ranking and top-k selection behavior.

## Decisions made
- Start with deterministic distance scoring over stored vectors.
- Keep retrieval interfaces provider-agnostic.
