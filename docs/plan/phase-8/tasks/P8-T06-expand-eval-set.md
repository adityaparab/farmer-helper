# P8-T06 - Expand eval set incrementally

## Sub-issue description
### Objective
Grow the evaluation dataset coverage safely over time to improve regression sensitivity while preserving determinism.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Expanded `docs/evaluation/EVAL_DATASET_SEED.jsonl` from 10 to 15 deterministic scenarios.
2. Added additional ambiguity/refusal and operational agronomy cases for broader eval coverage.
3. Preserved stable, lexicographically sorted IDs (`Q001`..`Q015`).
4. Added dataset integrity test coverage in `tests/unit/test_eval_seed_dataset.py`.

## Decisions made
- Expansion should be incremental with reviewable diffs.
- New samples must keep low ambiguity in expected topic scoring.
