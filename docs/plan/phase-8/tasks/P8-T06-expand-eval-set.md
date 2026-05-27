# P8-T06 - Expand eval set incrementally

## Sub-issue description
### Objective
Grow the evaluation dataset coverage safely over time to improve regression sensitivity while preserving determinism.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add new dataset entries for underrepresented failure/refusal and ambiguity scenarios.
2. Keep IDs stable and enforce deterministic ordering.
3. Add tests validating expanded dataset integrity and unique IDs.
4. Update eval maintenance docs with expansion rules.

## Decisions made
- Expansion should be incremental with reviewable diffs.
- New samples must keep low ambiguity in expected topic scoring.
