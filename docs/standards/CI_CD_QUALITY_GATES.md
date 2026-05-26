# CI/CD Quality Gates

## Purpose
Define minimum automated checks required to merge and release Farmer Helper changes.

## Gate model
There are two gate classes:
1. Pre-merge gates: must pass for pull request merge.
2. Pre-release gates: must pass before deployment promotion.

## Pre-merge gates (mandatory)
1. Static quality checks
- Linting and formatting checks pass.
- Type checks pass for changed modules.

2. Test checks
- Unit tests pass.
- Relevant integration tests pass for changed components.
- Coverage does not regress below current repository baseline.

3. Security checks
- Dependency vulnerability scan has no unresolved high/critical findings.
- Secret scanning has no confirmed leaks.

4. Contract and docs checks
- API/schema contract changes are versioned and documented.
- Docs are updated when behavior/configuration changed.

5. Review checks
- Required reviewers approved.
- Blocking review comments resolved.

## Pre-release gates (mandatory)
1. Build and artifact integrity
- Build succeeds with reproducible lockfile/dependency state.
- Artifact metadata includes version and commit reference.

2. Validation in staging
- Smoke tests pass in staging.
- Health and readiness checks pass.
- Critical path scenario tests pass (ingestion, retrieval, generation).

3. Operational readiness
- Rollback procedure is verified.
- Alerting and error reporting are active.
- Runbooks for impacted components are current.

4. Risk controls
- Open high-risk defects explicitly accepted by approver.
- Release notes include known limitations and mitigations.

## Gate outcomes
1. Pass: change may proceed.
2. Fail: merge/release blocked until corrected.
3. Exception: temporary waiver allowed only when:
- Approved by designated owner.
- Time-bounded.
- Linked to a tracked remediation issue.

## Evidence retention
For each merge and release, retain:
1. CI run identifiers and timestamps.
2. Test summary artifacts.
3. Security scan summary.
4. Reviewer approvals.
5. Exception records (if any).

## Ownership
1. Engineering owns enforcement in CI configuration.
2. Code owners own module-level quality standards.
3. Release owner owns pre-release gate sign-off.