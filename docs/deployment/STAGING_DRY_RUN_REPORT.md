# Staging Dry Run Report

## Scope
This report documents final production-readiness dry-run checks with realistic and failure-path scenarios.

## Environment snapshot
1. Workspace: `d:/GitHub/farmer-helper`
2. Python interpreter: `d:/GitHub/farmer-helper/.venv/Scripts/python.exe`
3. Date: 2026-05-27

## Full gate baseline
Command sequence:
1. `ruff check src tests alembic`
2. `black --check src tests alembic`
3. `mypy src`
4. `pytest -q`
5. `python scripts/run-evals.py --min-average-score 6.0 --report-out artifacts/eval-report.json`

Observed result:
1. All checks passed
2. `pytest -q`: 197 passed
3. Eval gate: 15/15 passed, average score 9.0667

## Staging dry-run scenario set
Command:
`pytest -q tests/integration/test_embedding_trigger_integration.py tests/integration/test_retrieval_query_integration.py tests/integration/test_concurrency_load.py tests/unit/test_answer_generation_route.py tests/unit/test_embedding_trigger_route.py tests/unit/test_health_error_contracts.py`

Observed result:
1. 25 passed
2. Coverage includes realistic ingestion/retrieval/embedding paths and degraded/conflict/failure contracts.

## Coverage verification
Command:
`pytest --cov=src/farmer_helper --cov-report=term-missing --cov-report=xml:artifacts/coverage.xml -q`

Observed result:
1. 197 passed
2. Total line coverage: 95%
3. Coverage artifact generated: `artifacts/coverage.xml`

## Failure-path validation highlights
1. Idempotency conflict behavior (`409`) validated for answer and embedding routes.
2. Degraded provider fallback behavior validated in answer and embedding routes.
3. Structured error contract validation includes health/readiness and async queue limits.
4. Concurrency coexistence validated for embedding and retrieval traffic.

## Cleanup follow-up
1. A post-sign-off cleanup pass added centralized SQLAlchemy session/engine teardown in `tests/conftest.py`.
2. Coverage and test runs now complete without the prior SQLite `ResourceWarning` output.
