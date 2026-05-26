# Test and Documentation Strategy

## Purpose
Define how Farmer Helper verifies behavior and maintains reliable documentation across the full development lifecycle.

## Testing strategy
### Test layers
1. Unit tests
- Validate pure logic and isolated module behavior.
- Required for new business logic and bug fixes.

2. Integration tests
- Validate cross-layer behavior (API/service/repository/adapters).
- Required when external systems, persistence, or orchestration are involved.

3. Contract tests
- Validate stable API/schema behavior.
- Required when changing request/response models or error contracts.

4. Regression tests
- Protect retrieval quality, grounding correctness, citations, and resilience behavior.
- Required for AI workflow or ranking/prompt changes.

### Required scenario coverage
For applicable changes, tests must include:
1. Happy path.
2. Boundary/edge cases.
3. Failure and timeout paths.
4. Idempotency/duplicate handling where relevant.

### Quality expectations
1. Tests must be deterministic and reproducible.
2. Flaky tests are treated as defects and must be fixed or quarantined with owner/date.
3. Added complexity requires proportional test depth.

## Documentation strategy
### Documentation categories
1. Product/overview docs: project scope and roadmap status.
2. Architecture docs: ADRs, boundaries, interfaces.
3. API docs: request/response schemas, errors, examples.
4. Operational docs: runbooks, failure handling, recovery procedures.
5. Developer docs: setup, local workflows, quality checks.

### Mandatory update triggers
Documentation updates are required in the same change when:
1. Public contracts or behavior changes.
2. Configuration keys or defaults change.
3. Operational procedures or failure behavior changes.
4. Architectural decisions are introduced or revised.

### Ownership and review
1. Author updates impacted docs.
2. Reviewers verify docs are complete and accurate.
3. Missing critical docs blocks merge unless exception approved.

## Pull request evidence requirements
Each PR should include:
1. Test selection summary and outcomes.
2. Documentation updates made.
3. Known risks and follow-up tasks, if any.

## Release evidence requirements
Before release:
1. Test suite pass summary.
2. Updated runbook references.
3. Contract change notes.
4. Open risk acceptance record (if applicable).