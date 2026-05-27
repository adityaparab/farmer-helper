# Epic: Phase 13 - Scalability and concurrency hardening

## Summary
Harden runtime behavior under concurrent traffic by applying DB connection pooling, controlled async worker queueing, and concurrent load verification.

## Scope
This Epic maps to Phase 13 in docs/plan/PHASES.md and tracks local sub-issue status.

## Epic status
- Status: Completed
- Started on: 2026-05-27

## Sub-issues
| ID | Title | Status | Last updated | Notes |
|---|---|---|---|---|
| P13-T01 | Configure and test connection pooling | Completed | 2026-05-27 | Added QueuePool config and DB pool tests |
| P13-T02 | Move background jobs to worker queue | Completed | 2026-05-27 | Added queue-capacity control and persistent async job records |
| P13-T03 | Add concurrent load test scenarios | Completed | 2026-05-27 | Added concurrent embedding/retrieval integration test |
| P13-T04 | Document scale limits and bottlenecks | Completed | 2026-05-27 | Added scalability runbook |
| P13-T05 | Verify ingestion and query paths coexist under load | Completed | 2026-05-27 | Covered by concurrent integration scenario and green gate run |
