# Epic: Phase 10 - Security, abuse resistance, and AI safety

## Summary
Secure the API and AI workflows against abuse, secret leakage, and prompt-injection attempts with enforceable controls and regression tests.

## Scope
This Epic maps to Phase 10 in `docs/plan/PHASES.md` and tracks local sub-issue status.

## Epic status
- Status: Completed
- Started on: 2026-05-27

## Sub-issues
| ID | Title | Status | Last updated | Notes |
|---|---|---|---|---|
| P10-T01 | Add auth and rate limiting | Completed | 2026-05-27 | Added API key auth and in-memory rate limiting at middleware guard layer |
| P10-T02 | Enforce strict input validation | Completed | 2026-05-27 | Added strict question/query validators and length constraints across critical schemas |
| P10-T03 | Protect secrets and environment configuration | Completed | 2026-05-27 | Added security config knobs and expanded environment configuration guidance |
| P10-T04 | Add prompt injection defenses and tests | Completed | 2026-05-27 | Added prompt-injection detection and refusal path with audit log events |
| P10-T05 | Add security audit logging | Completed | 2026-05-27 | Added structured security audit events for auth/rate-limit and injection defenses |
| P10-T06 | Add regression tests for exploit scenarios | Completed | 2026-05-27 | Added exploit regression tests for unauthorized access and rate-limit behavior |
| P10-T07 | Document security model and runbook | Completed | 2026-05-27 | Added security runbook with threat model, controls, and incident workflow |
