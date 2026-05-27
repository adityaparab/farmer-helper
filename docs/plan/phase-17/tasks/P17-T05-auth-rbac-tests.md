# P17-T05 - Add auth and RBAC tests

## Sub-issue description
### Objective
Add unit/integration coverage for auth contracts and role enforcement.

### Acceptance criteria
- Tests prove default admin can log in.
- Tests prove registered users can authenticate and call /auth/me.
- Tests prove user role cannot access admin endpoints.
- Tests prove admin role can access admin endpoints.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/182

## What was done
1. Added auth route tests for default admin login and /auth/me.
2. Added registration tests for user role accounts.
3. Added forbidden-path tests for user-role access to admin endpoints.
4. Updated admin route tests to authenticate with admin JWT.

## Evidence
- tests/unit/test_auth_routes.py
- tests/unit/test_admin_routes.py
- https://github.com/adityaparab/farmer-helper/issues/182
