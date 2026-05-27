# P8-T01 - Build eval dataset loader

## Sub-issue description
### Objective
Implement deterministic loading and strict validation of evaluation dataset records for subsequent evaluation and regression workflows.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added typed evaluation dataset schemas in `src/farmer_helper/schemas/evaluation.py`.
2. Added deterministic file loader service in `src/farmer_helper/services/evaluation/dataset_loader.py`.
3. Added strict validation for JSON/JSONL parsing, empty datasets, and duplicate IDs.
4. Added focused unit tests in `tests/unit/test_eval_dataset_loader.py`.

## Decisions made
- Loader supports `.json` and `.jsonl` only for predictable parsing behavior.
- Duplicate eval IDs fail fast to preserve deterministic runner behavior.
