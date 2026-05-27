# Epic: Phase 9 - Observability and alerting

## Summary
Ensure critical API and service flows are diagnosable end-to-end with structured logs, request correlation IDs, timing signals, alert integrations, and safe redaction.

## Scope
This Epic maps to Phase 9 in `docs/plan/PHASES.md` and tracks local sub-issue status.

## Epic status
- Status: Completed
- Started on: 2026-05-27

## Sub-issues
| ID | Title | Status | Last updated | Notes |
|---|---|---|---|---|
| P9-T01 | Add structured logging across modules | Completed | 2026-05-27 | Added request lifecycle and route completion structured logs |
| P9-T02 | Propagate request IDs through all layers | Completed | 2026-05-27 | Request IDs now verified through middleware logs and response headers |
| P9-T03 | Add stage-level timing metrics | Completed | 2026-05-27 | Added route-level timing metrics for answers and embeddings |
| P9-T04 | Integrate with Railway/Sentry | Completed | 2026-05-27 | Added optional Sentry initialization and environment controls |
| P9-T05 | Enforce log redaction/privacy | Completed | 2026-05-27 | Added recursive sensitive field redaction filter and tests |
| P9-T06 | Document operational debugging workflows | Completed | 2026-05-27 | Added observability runbook with request tracing, latency triage, and production incident response workflow |
