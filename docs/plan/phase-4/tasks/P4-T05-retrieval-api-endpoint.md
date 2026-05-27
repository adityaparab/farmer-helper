# P4-T05 - Add retrieval API endpoint with score and citation metadata

## Sub-issue description
### Objective
Expose a retrieval API endpoint that returns fused and optionally reranked results with explicit score and citation metadata.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add retrieval API request/response contracts.
2. Compose vector retrieval, keyword retrieval, fusion, and reranking in route/service wiring.
3. Add endpoint tests for success and validation behavior.

## Decisions made
- Retrieval endpoint output must include deterministic score fields and citation identity.
- Endpoint composition should reuse existing retrieval services without duplicating logic.
