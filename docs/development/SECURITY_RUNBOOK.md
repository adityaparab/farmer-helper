# Security Model and Runbook

## Purpose
This runbook documents Phase 10 security controls, exploit-resistance expectations, and operational incident workflow.

## Threat model focus
Primary risks addressed:
1. Unauthorized API access
2. High-volume abuse requests
3. Prompt-injection attempts against instruction boundaries
4. Sensitive value leakage through logs

## Security controls
### Auth control
- Non-health routes require `x-api-key` when `SECURITY_API_KEY` is configured.
- Unauthorized requests return `401` with `AUTH_REQUIRED`.

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

Operational recommendation:
- Keep `SECURITY_API_KEY` only in environment secrets (never committed).
- Use conservative rate limits in production and tighten based on observed traffic patterns.

## Incident response workflow
1. Identify affected route and request ID from logs.
2. Inspect `security.audit` events around incident window.
3. Determine class:
   - auth bypass attempt
   - rate-limit abuse
   - prompt-injection attempt
4. Apply response:
   - rotate API key if compromise suspected
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
