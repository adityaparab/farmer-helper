# Release Runbook

## Purpose
Provide a deterministic semver-based release sequence for promoting Farmer Helper safely.

## Versioning policy
1. Releases use semantic versioning: `MAJOR.MINOR.PATCH`.
2. `PATCH` is for backward-compatible fixes and operational improvements.
3. `MINOR` is for backward-compatible feature delivery.
4. `MAJOR` is for backward-incompatible API, schema, or operational contract changes.
5. Backend and frontend release versions must stay identical.
6. The canonical project version lives in `src/farmer_helper/__about__.py` and is synchronized to `frontend/package.json` and `frontend/package-lock.json` by `scripts/release_version.py`.

## Release workflow
1. Use GitHub Actions workflow `Release` in `.github/workflows/release.yml`.
2. Trigger the workflow manually from `main` with either:
	- `release_type=patch|minor|major`, or
	- `version=<explicit semver>` for an approved override.
3. The workflow will:
	- bump and sync version files,
	- run backend quality gates,
	- run frontend lint, test, and build,
	- build Python distribution artifacts,
	- package frontend build output,
	- upload a release artifact bundle,
	- commit the version bump, create `vX.Y.Z` tag, push to `main`, and create a GitHub Release.
4. Protect the `production` GitHub environment with required approvals before using the workflow in production.
5. If branch protection blocks `github-actions[bot]` from pushing to `main`, configure repository secret `RELEASE_PAT` with `contents:write` and permission to bypass or satisfy the branch policy.

## Preconditions
1. Main branch is green on backend and frontend CI quality gates.
2. Production environment variables are configured per `docs/deployment/RAILWAY_DEPLOYMENT.md`.
3. Rollback and incident runbooks are reviewed by on-call owner.
4. Railway is configured to deploy from `main` so the release commit/tag promotion triggers the production deployment path.

## Release checklist
1. Review pending changes and choose the next semantic version bump.
2. Trigger the `Release` workflow from `main`.
3. Wait for the workflow to publish the GitHub Release, artifacts, release commit, and release tag.
4. Confirm Railway has deployed the release commit from `main`.
5. Apply migrations on target environment: `alembic upgrade head`.
6. Verify health endpoints: `/health/live`, `/health/ready`.
7. Run post-deploy smoke checks for retrieval, answers, embeddings, and authenticated frontend access.
8. Verify observability and security signals are being emitted.

## Verification commands
1. `ruff check src tests alembic`
2. `black --check src tests alembic`
3. `mypy src`
4. `pytest -q`
5. `python scripts/run-evals.py --min-average-score 6.0 --report-out artifacts/eval-report.json`
6. `npm --prefix frontend run lint`
7. `npm --prefix frontend run test`
8. `npm --prefix frontend run build`

## Post-release checks
1. Check error-rate and latency trends for first 30-60 minutes.
2. Check queue saturation and DB pool pressure indicators.
3. Confirm no sustained degradation/reliability conflict anomalies.
4. Confirm `/` serves the current frontend build and authenticated admin/user flows are reachable.

## Release communication template
1. Deployment commit hash
2. Semantic version and Git tag
3. Migration version applied
4. Validation command summary
5. Monitoring status and on-call handoff
