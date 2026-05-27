# P8-T04 - Integrate evals into CI

## Sub-issue description
### Objective
Integrate deterministic offline evaluation execution into CI so material quality regressions fail the pipeline.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added eval execution script `scripts/run-evals.py` for loader, runner, report generation, and threshold gating.
2. Added seeded eval dataset file `docs/evaluation/EVAL_DATASET_SEED.jsonl`.
3. Integrated eval gate and report artifact upload in `.github/workflows/ci.yml`.
4. Added CI gate unit tests in `tests/unit/test_eval_ci_gate.py`.

## Decisions made
- CI integration should consume existing typed loader/runner/reporting contracts.
- Failure criteria should be explicit and stable.
