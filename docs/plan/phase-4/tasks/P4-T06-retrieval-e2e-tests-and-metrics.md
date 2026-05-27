# P4-T06 - Add end-to-end retrieval tests and metrics

## Sub-issue description
### Objective
Add integration/smoke coverage for retrieval endpoint behavior and basic measurable retrieval metrics outputs.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add end-to-end retrieval integration test that verifies deterministic merged ordering.
2. Add retrieval smoke test for API contract and citation metadata fields.
3. Add basic retrieval metrics schema/values in endpoint response metadata.

## Decisions made
- Metrics for this step should be lightweight and deterministic, suitable for CI assertions.
- End-to-end tests should seed data through existing embedding trigger path when practical.
