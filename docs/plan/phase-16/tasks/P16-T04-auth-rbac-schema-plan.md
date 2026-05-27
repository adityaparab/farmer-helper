# P16-T04 - Define auth and RBAC schema changes and migration plan

## Sub-issue description
### Objective
Define the backend schema and migration plan for user authentication and RBAC before production hardening.

### Acceptance criteria
- User and token storage requirements are explicit.
- Admin/user role model is constrained to the requested two roles.
- Migration and bootstrap path are traceable to the implementation phase.

## Implementation status
- Status: Completed
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/173

## Resolution
- Auth/RBAC schema and migration planning was implemented under Phase 17 to keep the security foundation independently tracked and testable.
- User storage requirements are implemented by `UserAccount` with username, password hash, role, active flag, and timestamps.
- Refresh-token storage is implemented by `RefreshTokenRecord` with token hash, expiration, creation time, and revocation time.
- The role model is constrained to the requested `admin` and `user` roles through auth schemas and validation.
- Clean bootstrap creates the default admin account with username `admin` and password `P@ssw0rd` through migration/runtime bootstrap paths.
- Admin route enforcement is centralized through auth dependency helpers and applied at the admin router boundary.

## Evidence
- Tracked remotely under Phase 16 Epic: https://github.com/adityaparab/farmer-helper/issues/168
- Phase 17 Epic completed: https://github.com/adityaparab/farmer-helper/issues/169
- Auth schema/default admin tracker: `docs/plan/phase-17/tasks/P17-T01-auth-schema-and-default-admin-bootstrap.md`
- RBAC enforcement tracker: `docs/plan/phase-17/tasks/P17-T04-rbac-route-enforcement.md`
- Migration: `alembic/versions/20260527_0007_auth_rbac_schema.py`
- Runtime routes/bootstrap: `src/farmer_helper/api/routes/auth.py`
- RBAC dependencies: `src/farmer_helper/services/auth/dependencies.py`
- Validation was completed and pushed in Phase 17 commits; Phase 16 tracker is now reconciled to that implementation.
