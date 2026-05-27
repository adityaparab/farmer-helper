# Release Runbook

## Purpose
Provide a deterministic release sequence for promoting Farmer Helper safely.

## Preconditions
1. Main branch is green on CI quality, tests, eval gate, and coverage artifact generation.
2. Production environment variables are configured per `docs/deployment/RAILWAY_DEPLOYMENT.md`.
3. Rollback and incident runbooks are reviewed by on-call owner.

## Release checklist
1. Confirm latest commit on `main` has passed local and CI gates.
2. Apply migrations on target environment: `alembic upgrade head`.
3. Deploy app revision through Railway.
4. Verify health endpoints: `/health/live`, `/health/ready`.
5. Run post-deploy smoke checks for retrieval, answers, and embeddings routes.
6. Verify observability and security signals are being emitted.

## Verification commands
1. `ruff check src tests alembic`
2. `black --check src tests alembic`
3. `mypy src`
4. `pytest -q`
5. `python scripts/run-evals.py --min-average-score 6.0 --report-out artifacts/eval-report.json`

## Post-release checks
1. Check error-rate and latency trends for first 30-60 minutes.
2. Check queue saturation and DB pool pressure indicators.
3. Confirm no sustained degradation/reliability conflict anomalies.

## Release communication template
1. Deployment commit hash
2. Migration version applied
3. Validation command summary
4. Monitoring status and on-call handoff
