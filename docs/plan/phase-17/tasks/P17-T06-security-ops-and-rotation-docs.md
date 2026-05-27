# P17-T06 - Document security operations and rotation

## Sub-issue description
### Objective
Document operational guidance for JWT secrets, default admin credential rotation, refresh-token handling, and RBAC troubleshooting.

### Acceptance criteria
- Security runbook explains default admin bootstrap and immediate password rotation expectation.
- Deployment docs describe AUTH_JWT_SECRET and token TTL configuration.
- Admin/user RBAC behavior is documented for operators and frontend integration.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/183

## What was done
1. Documented JWT access tokens, opaque refresh tokens, and admin/user RBAC behavior.
2. Documented default admin bootstrap and production rotation expectations.
3. Added auth environment knobs to development and production config examples.

## Evidence
- docs/development/SECURITY_RUNBOOK.md
- config/examples/.env.development.example
- config/examples/.env.production.example
- https://github.com/adityaparab/farmer-helper/issues/183
