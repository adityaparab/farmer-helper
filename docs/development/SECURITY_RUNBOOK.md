# Security Model and Runbook

## Purpose
This runbook documents security controls, RBAC expectations, exploit-resistance expectations, and operational incident workflow.

## Threat model focus
Primary risks addressed:
1. Unauthorized API access
2. High-volume abuse requests
3. Prompt-injection attempts against instruction boundaries
4. Sensitive value leakage through logs
5. Incorrect role assignment or admin endpoint exposure

## Security controls
### Auth control
- Non-health routes require `x-api-key` when `SECURITY_API_KEY` is configured.
- Unauthorized requests return `401` with `AUTH_REQUIRED`.

### User authentication and RBAC
- Browser users authenticate through `/auth/register`, `/auth/login`, `/auth/me`, `/auth/refresh`, and `/auth/logout`.
- Access tokens are signed JWT bearer tokens controlled by `AUTH_JWT_SECRET` and `AUTH_ACCESS_TOKEN_TTL_MINUTES`.
- Refresh tokens are opaque random values; only SHA-256 hashes are stored in `refresh_token_records`.
- Supported user roles are exactly `admin` and `user`.
- Administrative endpoints under `/admin` require a valid bearer token for an active `admin` user.
- Authenticated `user` accounts receive `403` with `Admin role required` when calling admin endpoints.

### Default admin bootstrap
- Clean database migrations seed a default admin account with username `admin` and password `P@ssw0rd`.
- Runtime clean-database bootstrap also creates the same default admin if `/auth/login` or `/auth/register` runs before migration-seeded data exists.
- Treat the default credential as bootstrap-only in production operations.
- Immediately after first production login, create/rotate to a non-shared administrator credential through the user-management workflow once available.
- Until user-management UI/API exists, restrict access to production deployment controls and rotate `AUTH_JWT_SECRET` if default credential exposure is suspected.

### Rate limiting
- Enabled when `SECURITY_RATE_LIMIT_REQUESTS > 0`.
- Window controlled by `SECURITY_RATE_LIMIT_WINDOW_SECONDS`.
- Exceeded requests return `429` with `RATE_LIMIT_EXCEEDED` and `Retry-After`.

### Prompt-injection defense
- Prompt builder checks known injection phrases.
- Detected attempts are refused with `REFUSAL_PROMPT_INJECTION`.

### Input validation hardening
- Critical query/question fields are bounded and normalized.
- Blank and malformed string values are rejected deterministically.

### Security audit logging
Structured `security.audit` events include:
- `security_event`
- `security_outcome`
- `security_route`
- `security_method`
- `security_principal`
- `security_detail`

## Configuration
Security runtime knobs:
- `SECURITY_API_KEY`
- `SECURITY_RATE_LIMIT_REQUESTS`
- `SECURITY_RATE_LIMIT_WINDOW_SECONDS`
- `AUTH_JWT_SECRET`
- `AUTH_ACCESS_TOKEN_TTL_MINUTES`
- `AUTH_REFRESH_TOKEN_TTL_DAYS`

Operational recommendation:
- Keep `SECURITY_API_KEY` only in environment secrets (never committed).
- Keep `AUTH_JWT_SECRET` only in environment secrets (never committed) and use at least 32 bytes of entropy.
- Rotating `AUTH_JWT_SECRET` invalidates existing access tokens immediately; active refresh tokens should also be revoked if compromise is suspected.
- Use conservative rate limits in production and tighten based on observed traffic patterns.

## Incident response workflow
1. Identify affected route and request ID from logs.
2. Inspect `security.audit` events around incident window.
3. Determine class:
   - auth bypass attempt
   - RBAC bypass attempt
   - rate-limit abuse
   - prompt-injection attempt
4. Apply response:
   - rotate API key if compromise suspected
   - rotate `AUTH_JWT_SECRET` if token signing compromise is suspected
   - revoke refresh tokens tied to affected users
   - tighten rate limits
   - expand injection pattern defense/tests if novel payload observed
5. Record issue with request IDs, event fields, and remediation decision.

## Verification checklist
1. `ruff check src tests`
2. `black --check src tests`
3. `mypy src`
4. `pytest -q`
5. Verify security tests:
   - auth rejection
   - rate-limit rejection
   - prompt-injection refusal
   - security audit event emission
   - default admin login
   - user-role denial for admin endpoints
   - admin-role access for admin endpoints
