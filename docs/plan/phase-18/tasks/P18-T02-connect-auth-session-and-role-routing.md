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
- Status: Not Started
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/186

## Evidence
- Tracked remotely under Phase 18 Epic: https://github.com/adityaparab/farmer-helper/issues/184