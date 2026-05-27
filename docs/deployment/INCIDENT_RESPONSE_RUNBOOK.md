# Incident Response Runbook

## Purpose
Provide a practical response flow for reliability, security, and performance incidents.

## Severity guide
1. Sev-1: Production outage or major integrity/security risk.
2. Sev-2: Significant degradation with workaround.
3. Sev-3: Minor impact with limited scope.

## Triage workflow
1. Capture request IDs, route, and error codes from logs.
2. Classify incident type:
   - reliability/dependency
   - scalability/concurrency
   - security/abuse
   - deployment/configuration
3. Determine blast radius and affected APIs.
4. Decide mitigation path: hotfix, config update, rollback.

## Investigation references
1. Observability: `docs/development/OBSERVABILITY_RUNBOOK.md`
2. Security: `docs/development/SECURITY_RUNBOOK.md`
3. Reliability: `docs/development/RELIABILITY_RUNBOOK.md`
4. Scalability: `docs/development/SCALABILITY_RUNBOOK.md`

## Mitigation actions
1. Apply immediate containment (rate-limit tightening, degraded mode, rollback).
2. Verify health endpoints and route-level behavior.
3. Validate structured error contract consistency for client safety.
4. Escalate to rollback runbook if stability not restored rapidly.

## Post-incident actions
1. Publish timeline with request IDs and technical findings.
2. Open follow-up tasks for root cause and prevention.
3. Update relevant runbook sections if gaps were identified.
