# Evaluation Maintenance and Interpretation Runbook

## Purpose
This runbook explains how to run, interpret, and maintain Phase 8 evaluation workflows.

## Core workflow
1. Load the deterministic seed dataset.
2. Run per-item and aggregate scoring.
3. Build a deterministic JSON report.
4. Apply CI threshold gating.
5. Inspect failures and decide whether to tune behavior or adjust the dataset.

## Local commands
### Run complete quality + eval flow
1. `ruff check src tests`
2. `black --check src tests`
3. `mypy src`
4. `pytest -q`
5. `python scripts/run-evals.py --dataset docs/evaluation/EVAL_DATASET_SEED.jsonl --min-average-score 6.0 --report-out artifacts/eval-report.local.json`

### Run eval only
- `python scripts/run-evals.py --dataset docs/evaluation/EVAL_DATASET_SEED.jsonl --min-average-score 6.0 --report-out artifacts/eval-report.local.json`

## CI behavior
- CI runs evals after pytest.
- CI fails when `average_score < min_average_score`.
- CI uploads `artifacts/eval-report.json` for post-failure analysis.

## Metric interpretation
### Per-item scores
Each item includes:
- retrieval relevance
- groundedness
- citation correctness
- safety/refusal behavior
- clarity/actionability

Interpretation guidance:
- Low retrieval relevance: inspect retrieval fusion/reranker behavior.
- Low groundedness or citation correctness: inspect answer grounding and citation mapping.
- Low safety/refusal score: inspect refusal/clarification policies.
- Low clarity/actionability: inspect prompt and answer style constraints.

### Aggregate metrics
Primary aggregate gate:
- `average_score`

Supporting aggregate indicators:
- `total_items`
- `passed_items`
- `failed_items`

Interpretation guidance:
- A small drop in one item may be noise if aggregate and pass rate stay stable.
- Broad drops across categories indicate systemic regressions.
- Repeated failures on the same IDs indicate targeted behavior regressions.

## Regression triage workflow
1. Download and inspect the eval report artifact.
2. Identify lowest-scoring item IDs and categories.
3. Reproduce locally with the same dataset and threshold.
4. Determine regression class:
   - retrieval quality
   - grounding/citation
   - safety/refusal
   - clarity/actionability
5. Add or update tests for the observed failure mode.
6. Re-run quality + eval commands before merge.

## Dataset expansion policy
- Keep IDs stable and lexicographically ordered (`Q001`, `Q002`, ...).
- Keep scenarios deterministic and reviewable in plain text JSONL diffs.
- Add cases incrementally in small batches.
- Preserve coverage balance across:
  - citation-required and non-citation items
  - easy, medium, and hard difficulty
  - answer, clarify, and refusal-oriented behavior
- Maintain uniqueness of item IDs (enforced by loader + tests).

## Operational notes
- Avoid logging user-identifying free-text as feedback signals.
- Use low-cardinality feedback fields for trendability.
- Keep threshold updates explicit in PR descriptions and issue comments.
