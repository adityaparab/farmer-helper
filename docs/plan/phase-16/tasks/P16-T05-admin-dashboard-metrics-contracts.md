# P16-T05 - Define admin dashboard metrics contracts

## Sub-issue description
### Objective
Define backend/frontend contracts for the admin dashboard metrics derived from the existing database schema.

### Acceptance criteria
- Metrics map to concrete tables and query patterns.
- API response shape is typed and frontend-ready.
- Expensive dashboard queries have an explicit performance strategy.

## Implementation status
- Status: Completed
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/174

## Evidence
- Tracked remotely under Phase 16 Epic: https://github.com/adityaparab/farmer-helper/issues/168
- Added typed admin dashboard metric response contracts in `src/farmer_helper/schemas/admin.py`.
- Added `GET /admin/dashboard/metrics` in `src/farmer_helper/api/routes/admin.py`.
- Metrics map to concrete aggregate counts over existing operational tables:
	- documents, embedded chunks, chat messages, QA review queue items, audit events
	- ingestion jobs, chat sessions, gold answers, QA review items, and embedding jobs by status
- Performance strategy: dashboard reads use bounded aggregate `COUNT` and `GROUP BY` queries only; no row payloads are loaded for metric cards or status distributions.
- Added route coverage in `tests/unit/test_admin_routes.py`.
- Validation: `ruff check .` passes.
- Validation: `pytest tests/unit/test_admin_routes.py` passes.
