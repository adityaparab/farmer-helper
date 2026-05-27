# Admin Operations and Rollback Runbook

## Purpose
Provide operational playbooks for ingestion/reindex workflows, version tracking, QA review operations, and rollback execution.

## Admin API overview
Core endpoints:
1. `POST /admin/ingestion/jobs`
2. `POST /admin/reindex/jobs`
3. `POST /admin/jobs/{job_id}/status`
4. `POST /admin/versions`
5. `GET /admin/versions`
6. `POST /admin/gold-answers`
7. `POST /admin/gold-answers/{answer_id}`
8. `GET /admin/gold-answers`
9. `POST /admin/review-queue`
10. `POST /admin/review-queue/{item_id}`
11. `GET /admin/review-queue`
12. `GET /admin/access-audit`

All admin mutations emit persistent access audit records.

## Operational workflows
### Ingestion workflow
1. Create ingestion job via `POST /admin/ingestion/jobs`.
2. Move job to processing via `POST /admin/jobs/{job_id}/status`.
3. Mark succeeded or failed with deterministic status transition semantics.

### Reindex workflow
1. Create reindex job via `POST /admin/reindex/jobs`.
2. Track and update job state through admin job status endpoint.
3. Capture pipeline/model version details in metadata for traceability.

### Version tracking workflow
1. Register rollout version tuple via `POST /admin/versions`.
2. Inspect recent records using `GET /admin/versions`.
3. Use version records as rollback anchors during incident response.

### Gold-answer workflow
1. Create draft gold answer via `POST /admin/gold-answers`.
2. Review and update status/editor attribution via `POST /admin/gold-answers/{answer_id}`.
3. List records for review and quality process auditing via `GET /admin/gold-answers`.

### QA/corpus review workflow
1. Add queue item via `POST /admin/review-queue`.
2. Assign and update progress via `POST /admin/review-queue/{item_id}`.
3. Audit queue state via `GET /admin/review-queue`.

## Access audit usage
`GET /admin/access-audit` shows persistent admin action trails including:
- actor
- action
- target type/id
- request id
- action details

Use this for postmortem reconstruction and governance review.

## Rollback playbook
1. Identify incident scope and affected workflows.
2. Look up recent version records from `GET /admin/versions`.
3. Choose rollback target tuple (content/model/pipeline).
4. Open review queue item documenting rollback reason and impact.
5. Trigger required reindex/ingestion jobs for rollback alignment.
6. Validate health, retrieval, and answer behavior after rollback.
7. Record final actions in access audit and issue tracker.

## Verification checklist
1. `ruff check src tests`
2. `black --check src tests`
3. `mypy src`
4. `pytest -q`
5. Validate admin route tests and audit log assertions.
