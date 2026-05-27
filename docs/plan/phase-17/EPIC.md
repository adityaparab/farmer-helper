# Epic: Phase 17 - Auth and RBAC foundation

## Summary
Implement production-ready user authentication and role-based access control with exactly two roles: admin and user.

## Scope
This Epic maps to the web interface security foundation after Phase 16. It adds user persistence, password login, JWT access tokens, refresh token records, default admin bootstrap, and admin route authorization.

## Epic status
- Status: Completed
- Started on: 2026-05-27
- Completed on: 2026-05-27
- Remote GitHub Epic: https://github.com/adityaparab/farmer-helper/issues/169
- Local/remote sync: Synced on 2026-05-27

## Sub-issues
| ID | Title | Status | Remote issue | Last updated | Notes |
|---|---|---|---|---|---|
| P17-T01 | Add auth schema and default admin bootstrap | Completed | https://github.com/adityaparab/farmer-helper/issues/178 | 2026-05-27 | Users, refresh tokens, admin seed migration/runtime bootstrap |
| P17-T02 | Implement password and JWT services | Completed | https://github.com/adityaparab/farmer-helper/issues/179 | 2026-05-27 | Standard library hashing and signing |
| P17-T03 | Implement auth API routes | Completed | https://github.com/adityaparab/farmer-helper/issues/180 | 2026-05-27 | Register, login, me, refresh/logout foundation |
| P17-T04 | Enforce admin/user RBAC dependencies | Completed | https://github.com/adityaparab/farmer-helper/issues/181 | 2026-05-27 | Admin route protection |
| P17-T05 | Add auth and RBAC tests | Completed | https://github.com/adityaparab/farmer-helper/issues/182 | 2026-05-27 | Login/register/me/admin guard coverage |
| P17-T06 | Document security operations and rotation | Completed | https://github.com/adityaparab/farmer-helper/issues/183 | 2026-05-27 | Security runbook and config examples updated |

## Completion confirmation
Phase 17 is complete as of 2026-05-27. Auth/RBAC implementation, tests, migration, default admin bootstrap, and operational documentation are delivered and linked to remote GitHub issues.

## Exit criteria for Epic completion
- Users can register and log in with JWT access tokens.
- Default admin exists with username admin and password P@ssw0rd.
- Admin APIs reject anonymous and user-role requests.
- User-role requests can authenticate and resolve /auth/me.
- Tests cover happy path and forbidden path behavior.
