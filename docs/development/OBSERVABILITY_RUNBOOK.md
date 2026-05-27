# Observability and Alerting Runbook

## Purpose
This runbook defines practical workflows for diagnosing request failures, latency regressions, and production incidents using structured logs, request IDs, timings, and Sentry events.

## Observability signals
### Structured logs
Key event families:
1. `http.request.completed`
2. `retrieval.query.completed`
3. `answer.generation.completed`
4. `answers.route.completed`
5. `embeddings.route.completed`
6. `reliability.degraded`
7. `reliability.conflict`
8. `evaluation.feedback.signal`

### Request correlation
- Request IDs are accepted via `x-request-id` or generated server-side.
- Response headers:
  - `x-request-id`
  - `x-response-time-ms`
- Log records include request IDs through context filters.

### Timing fields
- Route-level: `*_route_total_ms`, `http_latency_ms`
- Service-level: retrieval and answer generation timing diagnostics

## Redaction policy
Sensitive fields are redacted before emission when keys contain:
- `password`
- `token`
- `secret`
- `authorization`
- `api_key`
- `database_url`
- `dsn`

Expected redacted value: `[REDACTED]`

## Local debugging workflow
1. Reproduce request with explicit `x-request-id`.
2. Confirm response headers include the same request ID.
3. Filter logs by request ID.
4. Inspect event sequence:
   - `http.request.completed`
   - route-level completion event
   - service diagnostics events
   - reliability events (if degraded/conflict)
5. Compare timing fields to identify bottleneck stage.

## Production workflow (Railway + Sentry)
1. Check Railway logs for request ID-correlated traces.
2. Check Sentry event stream for matching error context.
3. Validate whether error path matches known reliability contracts.
4. Use event timing fields to classify latency vs provider failure.
5. Open or update issue with:
   - request ID
   - route
   - reliability code (if any)
   - timing metrics
   - remediation plan

## Sentry configuration
Environment variables:
- `SENTRY_DSN`
- `SENTRY_TRACES_SAMPLE_RATE`
- `SENTRY_ENVIRONMENT`

Behavior:
- If `SENTRY_DSN` is empty, Sentry init is skipped.
- If SDK is unavailable, app logs `observability.sentry.unavailable` and continues.

## Verification checklist
1. `ruff check src tests`
2. `black --check src tests`
3. `mypy src`
4. `pytest -q`
5. Confirm request IDs and redaction behavior in observability tests.
