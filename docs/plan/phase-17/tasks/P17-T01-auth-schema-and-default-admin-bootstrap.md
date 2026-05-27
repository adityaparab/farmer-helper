# P17-T01 - Add auth schema and default admin bootstrap

## Sub-issue description
### Objective
Add persistent user and refresh-token records with a default admin account for clean production bootstrap.

### Acceptance criteria
- User table supports username, password hash, role, active flag, and timestamps.
- Refresh token table supports token revocation and expiration tracking.
- Default admin credentials are available as admin / P@ssw0rd on clean bootstrap.
- Alembic migration exists for production databases.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/178

## What was done
1. Added `UserAccount` and `RefreshTokenRecord` ORM models.
2. Added auth settings for JWT secret and token TTLs.
3. Added Alembic migration for auth tables and default admin seed.
4. Added runtime default admin bootstrap for clean metadata-created test/dev databases.

## Evidence
- src/farmer_helper/db/models/foundation.py
- src/farmer_helper/core/config.py
- alembic/versions/20260527_0007_auth_rbac_schema.py
- src/farmer_helper/api/routes/auth.py
- https://github.com/adityaparab/farmer-helper/issues/178
