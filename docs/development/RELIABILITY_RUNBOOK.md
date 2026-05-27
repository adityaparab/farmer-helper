# Reliability and Resilience Runbook

## Purpose
This runbook documents how reliability controls in Phase 7 behave and how to diagnose degraded or conflicted outcomes.

## Reliability controls
### Timeout policies
- External provider boundaries are wrapped with explicit timeout policies.
- Timeout failures map to stable provider error codes:
  - `LLM_PROVIDER_TIMEOUT`
  - `EMBEDDING_PROVIDER_TIMEOUT`

### Retry policies
- Retry wrappers re-attempt only retryable provider errors.
- Non-retryable errors fail fast.
- Exhausted retries map to stable codes:
  - `LLM_RETRIES_EXHAUSTED`
  - `EMBEDDING_RETRIES_EXHAUSTED`

### Circuit breaker
- Circuit breakers operate with deterministic states:
  - `closed`
  - `open`
  - `half_open`
- Open-circuit behavior uses fallback providers when configured.
- Without fallback, open-circuit errors are explicit:
  - `LLM_CIRCUIT_OPEN`
  - `EMBEDDING_CIRCUIT_OPEN`

### Idempotency protections
- API requests can include `idempotency_key`.
- Same operation + same key + same payload:
  - replay prior response deterministically.
- Same operation + same key + different payload:
  - return `409` with `IDEMPOTENCY_KEY_REUSED_DIFFERENT_REQUEST`.

### Graceful degradation
- Provider failures in reliability-sensitive routes return deterministic degraded responses.
- Degraded responses include reliability contract fields for diagnosis.

## Normalized reliability contract
### Success/degraded payload fields
Both answer and embedding response payloads include:
- `reliability_status`: `normal` or `degraded`
- `reliability_retryable`: `true`/`false`/`null`
- `reliability_code`: stable reliability code or `null`

Degraded responses also include legacy-compatible fields:
- `degraded`
- `degradation_code`

### Error detail payload fields
Conflict-style reliability errors return:
- `status`: `error`
- `error_code`
- `message`
- `retryable`

## Observability events
Reliability events are logged as structured warnings:
1. `reliability.degraded`
2. `reliability.conflict`

Log fields emitted:
- `route`
- `reliability_status`
- `reliability_code`
- `reliability_retryable`

## Incident diagnosis workflow
1. Identify the request and route from request logs.
2. Check for `reliability.degraded` or `reliability.conflict` events.
3. Read `reliability_code` and `reliability_retryable`.
4. Determine control-path classification:
   - timeout
   - retries exhausted
   - circuit open
   - idempotency conflict
5. Apply corrective action:
   - retry safe requests when retryable
   - inspect provider health and latency
   - inspect circuit-breaker thresholds/timeouts
   - fix duplicated-key client behavior for conflicts

## Operational tuning levers
Configured through settings/env:
- `EXTERNAL_CALL_TIMEOUT_SECONDS`
- `EMBEDDING_RETRY_MAX_ATTEMPTS`
- `LLM_RETRY_MAX_ATTEMPTS`
- `EMBEDDING_CIRCUIT_BREAKER_FAILURE_THRESHOLD`
- `EMBEDDING_CIRCUIT_BREAKER_RECOVERY_TIMEOUT_SECONDS`
- `LLM_CIRCUIT_BREAKER_FAILURE_THRESHOLD`
- `LLM_CIRCUIT_BREAKER_RECOVERY_TIMEOUT_SECONDS`

## Verification checklist
When changing reliability behavior:
1. Run `ruff check src tests alembic scripts/trigger-embeddings.py`.
2. Run `black --check src tests alembic scripts/trigger-embeddings.py`.
3. Run `mypy src`.
4. Run `pytest -q`.
5. Verify route tests still assert normalized reliability fields.
6. Verify observability tests still assert structured reliability events.
