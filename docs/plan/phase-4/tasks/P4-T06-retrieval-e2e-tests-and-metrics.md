# P4-T06 - Add end-to-end retrieval tests and metrics

## Sub-issue description
### Objective
Add integration/smoke coverage for retrieval endpoint behavior and basic measurable retrieval metrics outputs.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added retrieval metrics schema and response fields in `src/farmer_helper/schemas/retrieval.py`.
2. Added metrics population in `src/farmer_helper/services/retrieval/query_service.py`.
3. Added end-to-end retrieval integration test in `tests/integration/test_retrieval_query_integration.py`.
4. Added retrieval smoke test in `tests/smoke/test_retrieval_query.py`.

## Decisions made
- Metrics for this step should be lightweight and deterministic, suitable for CI assertions.
- End-to-end tests should seed data through existing embedding trigger path when practical.
