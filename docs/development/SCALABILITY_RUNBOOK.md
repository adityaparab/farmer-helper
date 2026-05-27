# Scalability and Concurrency Runbook

## Purpose
Document practical scale controls, concurrency boundaries, and operational procedures for Farmer Helper.

## Key controls
1. `DATABASE_POOL_MIN` and `DATABASE_POOL_MAX` control SQLAlchemy QueuePool size and overflow.
2. `DATABASE_POOL_TIMEOUT_SECONDS` controls DB pool checkout timeout.
3. `EMBEDDING_JOB_QUEUE_MAX_SIZE` controls async embedding queue capacity.
4. `EMBEDDING_WORKER_COUNT` defines intended worker fan-out for async embedding processing.

## Connection pool guidance
### Single app instance
1. Start with `DATABASE_POOL_MIN=5` and `DATABASE_POOL_MAX=20`.
2. Keep `DATABASE_POOL_TIMEOUT_SECONDS` at 30 unless traffic profile requires lower fail-fast behavior.

### Multiple app instances
1. Ensure aggregate pool max across instances does not exceed database connection limits.
2. If using 4 instances and DB allows 120 connections, keep per-instance max near 20-25.

## Worker queue guidance
1. Set `EMBEDDING_JOB_QUEUE_MAX_SIZE` to absorb short bursts but avoid unbounded memory growth.
2. Monitor queue pressure by counting async trigger `503` responses.
3. Scale horizontally when sustained queue saturation appears.

## Known bottlenecks
1. SQLite is suitable for local/dev testing only and is not a high-concurrency production store.
2. In-process worker queue capacity is process-local; restarts can delay work already accepted.
3. External provider latency dominates throughput under heavy embedding loads.

## Operational checks
1. Run: `ruff check src tests alembic`
2. Run: `black --check src tests alembic`
3. Run: `mypy src`
4. Run: `pytest -q`
5. Validate `/embeddings/trigger-async` returns `503` at configured queue saturation.

## Incident response
### Symptom: elevated async queue saturation
1. Confirm recent `503` rates from async trigger endpoint.
2. Increase worker capacity by adding app instances.
3. Raise `EMBEDDING_JOB_QUEUE_MAX_SIZE` only if memory headroom exists.

### Symptom: DB checkout timeouts
1. Confirm DB-level connection limits and active connections.
2. Tune `DATABASE_POOL_MIN`, `DATABASE_POOL_MAX`, and `DATABASE_POOL_TIMEOUT_SECONDS`.
3. Investigate slow queries and upstream provider latency coupling.

## Scale verification workflow
1. Run integration test `tests/integration/test_concurrency_load.py`.
2. Verify ingestion/embedding and retrieval traffic complete under concurrent load without 5xx responses.
3. Record observed limits and update this runbook when infrastructure changes.
