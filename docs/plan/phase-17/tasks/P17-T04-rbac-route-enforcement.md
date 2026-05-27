# P17-T04 - Enforce admin/user RBAC dependencies

## Sub-issue description
### Objective
Protect administrative APIs so only authenticated admin users can access them, while preserving authenticated user identity resolution for user-facing routes.

### Acceptance criteria
- Anonymous requests to admin endpoints are rejected.
- Authenticated user-role requests to admin endpoints receive 403.
- Authenticated admin requests can use existing admin operations.
- Authorization logic is centralized in dependency helpers.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/181

## What was done
1. Added bearer-token current-user dependency.
2. Added admin role dependency.
3. Applied admin dependency at the admin router boundary.

## Evidence
- src/farmer_helper/services/auth/dependencies.py
- src/farmer_helper/api/routes/admin.py
- https://github.com/adityaparab/farmer-helper/issues/181
