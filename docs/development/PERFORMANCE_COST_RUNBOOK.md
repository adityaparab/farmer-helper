# Performance and Cost Control Runbook

## Purpose
Document Phase 11 tuning levers for latency, throughput, and model/provider cost control.

## Key controls
### Response caching
- Retrieval cache: `RETRIEVAL_CACHE_TTL_SECONDS`
- Answer cache: `ANSWER_CACHE_TTL_SECONDS`
- Shared cache capacity: `PERFORMANCE_CACHE_MAX_ENTRIES`

Guidance:
1. Keep TTL low for freshness-sensitive workloads.
2. Increase TTL for repeated high-volume stable queries.
3. Monitor cache hit/miss events to tune effectiveness.

### Model tiering and routing
- Enable request-side `model=auto` for answer generation.
- Routing knobs:
  - `LLM_MODEL_LOW_COST`
  - `LLM_MODEL_HIGH_QUALITY`
  - `LLM_MODEL_ROUTER_QUESTION_LENGTH_THRESHOLD`

Guidance:
1. Route short/simple prompts to low-cost model.
2. Route long/complex prompts to high-quality model.
3. Validate quality impact using eval suite and feedback signals.

### Context trimming and deduplication
- `SESSION_CONTEXT_MAX_CHARS_PER_MESSAGE`

Guidance:
1. Lower value reduces token footprint and cost.
2. Too-low values can reduce answer quality for nuanced follow-ups.
3. Balance with eval and multi-turn regression test outcomes.

### Asynchronous heavy work
- Use `POST /embeddings/trigger-async` for non-blocking embedding orchestration.
- Poll `GET /embeddings/jobs/{job_id}` for completion status.

Guidance:
1. Prefer async trigger for large ingestion waves.
2. Keep sync trigger for deterministic immediate workflows when required.

## Diagnostics and regression checks
1. `ruff check src tests`
2. `black --check src tests`
3. `mypy src`
4. `pytest -q`
5. `python scripts/run-evals.py --dataset docs/evaluation/EVAL_DATASET_SEED.jsonl --min-average-score 6.0 --report-out artifacts/eval-report.local.json`

## Incident and tuning workflow
1. Identify high-latency or high-cost path from observability logs.
2. Check cache hit/miss patterns and model routing behavior.
3. Tune one control at a time and re-run tests/evals.
4. Capture changes in issue comments and update docs if defaults change.
