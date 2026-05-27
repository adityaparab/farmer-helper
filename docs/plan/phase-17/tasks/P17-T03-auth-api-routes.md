# P17-T03 - Implement auth API routes

## Sub-issue description
### Objective
Expose user registration, login, current-user, and logout-ready authentication endpoints.

### Acceptance criteria
- POST /auth/register creates active user-role accounts.
- POST /auth/login returns JWT access and refresh token values.
- GET /auth/me returns the authenticated user.
- Auth route contracts are typed with Pydantic schemas.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/180

## What was done
1. Added typed auth request/response schemas.
2. Added register, login, refresh, logout, and current-user endpoints.
3. Registered auth router in the FastAPI app.

## Evidence
- src/farmer_helper/schemas/auth.py
- src/farmer_helper/api/routes/auth.py
- src/farmer_helper/main.py
- https://github.com/adityaparab/farmer-helper/issues/180
