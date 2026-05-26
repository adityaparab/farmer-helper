# KPI Specification

## Purpose
Define measurable KPIs for retrieval quality, latency, groundedness, and reliability, including formulas, data sources, and release thresholds.

## Metric groups

## 1. Retrieval quality KPIs
1. `retrieval_hit_at_k`
- Definition: Fraction of evaluation queries where at least one gold chunk appears in top K.
- Formula: hits_at_k / total_queries
- Data source: Offline eval runner output.

2. `retrieval_mrr_at_k`
- Definition: Mean reciprocal rank of first relevant chunk in top K.
- Formula: (sum of reciprocal_rank) / total_queries
- Data source: Offline eval runner output.

3. `retrieval_ndcg_at_k`
- Definition: Ranking quality for graded relevance in top K.
- Formula: DCG@K / IDCG@K
- Data source: Offline eval runner output with graded labels.

## 2. Groundedness KPIs
1. `citation_precision`
- Definition: Fraction of citations that correctly support answer claims.
- Formula: valid_citations / total_citations
- Data source: Regression evaluation and manual spot-check sampling.

2. `answer_groundedness_rate`
- Definition: Fraction of answers judged grounded in provided sources.
- Formula: grounded_answers / total_answers
- Data source: Offline eval and adjudication workflow.

3. `unsupported_answer_rate`
- Definition: Fraction of answers with unsupported claims.
- Formula: unsupported_answers / total_answers
- Data source: Offline eval and production audit sampling.

## 3. Latency KPIs
1. `api_latency_p50_ms`
2. `api_latency_p95_ms`
3. `api_latency_p99_ms`
- Definition: End-to-end API latency percentiles.
- Data source: Request timing telemetry with request IDs.

4. `retrieval_stage_latency_p95_ms`
5. `generation_stage_latency_p95_ms`
- Definition: Stage-level latency percentiles for retrieval and generation.
- Data source: Structured stage timing logs/traces.

## 4. Reliability KPIs
1. `request_success_rate`
- Formula: successful_requests / total_requests

2. `request_error_rate`
- Formula: failed_requests / total_requests

3. `timeout_rate`
- Formula: timeout_failures / total_requests

4. `fallback_activation_rate`
- Formula: requests_using_fallback / total_requests

5. `critical_incident_count`
- Definition: Count of sev-1/sev-2 incidents in window.

Data source for reliability KPIs: production logs, traces, and incident records.

## Thresholds by environment

## Local/dev
- Used for correctness and instrumentation checks; hard pass/fail only for syntax, tests, and schema integrity.

## Staging (release gate)
1. `retrieval_hit_at_k (k=10) >= 0.80`
2. `citation_precision >= 0.90`
3. `answer_groundedness_rate >= 0.90`
4. `api_latency_p95_ms <= 3500`
5. `request_success_rate >= 0.98`
6. `timeout_rate <= 0.02`

## Production (SLO targets)
1. `api_latency_p95_ms <= 2500`
2. `api_latency_p99_ms <= 5000`
3. `request_success_rate >= 0.995`
4. `request_error_rate <= 0.005`
5. `citation_precision >= 0.93`
6. `unsupported_answer_rate <= 0.03`

## Alert severities
1. Warning: threshold drift for 30 minutes.
2. Critical: threshold breach for 60 minutes or severe single-window breach.

## Measurement and reporting cadence
1. Offline eval KPIs: on PR for relevant modules and nightly scheduled runs.
2. Online KPIs: continuous telemetry with hourly rollups and daily summaries.
3. Release report: snapshot of staging KPIs compared against release gate thresholds.

## Release decision policy
1. Release is blocked when any staging gate metric fails without approved exception.
2. Exceptions must include owner, expiry, mitigation, and follow-up issue.