# P17-T02 - Implement password and JWT services

## Sub-issue description
### Objective
Provide testable password hashing/verification and signed JWT access token helpers without adding unnecessary runtime dependencies.

### Acceptance criteria
- Password hashing uses salted PBKDF2-HMAC-SHA256.
- JWT signing and verification include subject, role, expiry, and token type.
- Invalid, expired, or malformed tokens are rejected consistently.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/179

## What was done
1. Added salted PBKDF2-HMAC-SHA256 password hashing and verification.
2. Added HS256 JWT access token signing and verification.
3. Added opaque refresh-token generation and hashing helpers.

## Evidence
- src/farmer_helper/services/auth/passwords.py
- src/farmer_helper/services/auth/tokens.py
- https://github.com/adityaparab/farmer-helper/issues/179
