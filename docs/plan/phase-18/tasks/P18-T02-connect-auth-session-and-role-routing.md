# P18-T02 - Connect auth session and role routing

## Sub-issue description
### Objective
Replace mock username routing with backend login/register/me/logout state and protected role rendering.

### Acceptance criteria
- Login uses backend `/auth/login` and stores access/refresh token state safely for the app session.
- `/auth/me` drives current user and role state.
- Admin and user views render from backend role, not username string comparison.
- Logout revokes refresh token when available and clears session state.
- Vitest coverage exercises admin, user, and failed login states.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/186

## What was done
1. Replaced mock username-based role routing with backend auth client calls.
2. Added frontend session state for access token, refresh token, and current user.
3. Login now calls `/auth/login`, then `/auth/me` to drive the rendered backend role.
4. Logout calls `/auth/logout` when a refresh token exists, then clears local session state.
5. Added loading and error states to the auth panel with separate conditional components.
6. Updated frontend tests for admin login, user login, failed login, and logout behavior.

## Evidence
- Tracked remotely under Phase 18 Epic: https://github.com/adityaparab/farmer-helper/issues/184
- `frontend/src/App.tsx`
- `frontend/src/components/AuthPanel.tsx`
- `frontend/src/components/GuestExperience.tsx`
- `frontend/src/components/RoleView.tsx`
- `frontend/src/App.test.tsx`
- Validation: `npm run test` from `frontend/` passes.
- Validation: `npm run build` from `frontend/` passes.
- Validation: `npm run lint` from `frontend/` passes.
- Validation: `ruff check .` passes.