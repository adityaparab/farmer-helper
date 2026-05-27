# P18-T05 - Validate frontend integration workflows

## Sub-issue description
### Objective
Add Vitest coverage and build validation for authenticated frontend workflows.

### Acceptance criteria
- Frontend tests cover auth, role routing, admin metrics/upload, user chat/history, and error states.
- `npm run test`, `npm run build`, backend Ruff, backend mypy, and impacted backend tests pass.
- Documentation links validation commands and known local setup requirements.
- Phase 18 epic can be closed only after all sub-issues are complete.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/192

## What was validated
1. Frontend API client coverage for JSON, auth headers, multipart upload, and error normalization.
2. Backend-driven auth routing for admin and user roles.
3. Admin metrics hydration and PDF upload workflow.
4. User answer generation flow and answer-service failure handling.
5. Backend auth/admin/static/security compatibility after frontend integration.

## Evidence
- Tracked remotely under Phase 18 Epic: https://github.com/adityaparab/farmer-helper/issues/184
- Validation: `npm run test` from `frontend/` passes with 12 tests.
- Validation: `npm run build` from `frontend/` passes.
- Validation: `npm run lint` from `frontend/` passes.
- Validation: `d:/GitHub/farmer-helper/.venv/Scripts/python.exe -m ruff check .` passes.
- Validation: `d:/GitHub/farmer-helper/.venv/Scripts/python.exe -m mypy src` passes with 82 source files checked.
- Validation: `d:/GitHub/farmer-helper/.venv/Scripts/python.exe -m pytest tests/unit/test_auth_routes.py tests/unit/test_admin_routes.py tests/smoke/test_frontend_static_serving.py tests/unit/test_security_guards.py` passes with 13 tests.