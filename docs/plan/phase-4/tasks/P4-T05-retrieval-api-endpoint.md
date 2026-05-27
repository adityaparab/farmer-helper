# P4-T05 - Add retrieval API endpoint with score and citation metadata

## Sub-issue description
### Objective
Expose a retrieval API endpoint that returns fused and optionally reranked results with explicit score and citation metadata.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added retrieval API request/response contracts with score and citation metadata in `src/farmer_helper/schemas/retrieval.py`.
2. Added retrieval orchestration service in `src/farmer_helper/services/retrieval/query_service.py`.
3. Added retrieval API route in `src/farmer_helper/api/routes/retrieval.py` and registered it in `src/farmer_helper/main.py`.
4. Added endpoint and orchestration unit tests in `tests/unit/test_retrieval_route.py` and `tests/unit/test_retrieval_query_service.py`.

## Decisions made
- Retrieval endpoint output must include deterministic score fields and citation identity.
- Endpoint composition should reuse existing retrieval services without duplicating logic.
