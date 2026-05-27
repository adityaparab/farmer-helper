# Rollback Runbook

## Purpose
Define safe rollback procedures for application and data-path incidents.

## Rollback triggers
1. Sustained elevated 5xx/4xx unexpected error rates.
2. Regression in core answer/retrieval correctness.
3. Deployment-level failure to satisfy health/readiness checks.
4. Critical security/availability issue after release.

## Decision inputs
1. Latest stable commit hash.
2. Applied migration version(s).
3. Scope of behavioral regression.
4. Data mutation impact from current release.

## Rollback sequence
1. Announce rollback intent in incident channel.
2. Redeploy last known-good commit.
3. If needed, perform Alembic downgrade for release-specific migration changes.
4. Re-run health and smoke checks.
5. Validate observability/security telemetry stability.
6. Record rollback timeline and technical root cause stub.

## Post-rollback verification
1. `/health/live` and `/health/ready` return healthy.
2. Retrieval and answer generation smoke checks pass.
3. Async embedding workflow recovers expected queue behavior.
4. Error-rate and latency trends normalize.

## Documentation requirements
1. Link incident ticket.
2. Capture rollback cause, action, and recovery timestamp.
3. Add preventive follow-up tasks.
