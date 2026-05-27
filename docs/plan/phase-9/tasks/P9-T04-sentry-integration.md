# P9-T04 - Integrate with Railway/Sentry

## Sub-issue description
### Objective
Provide optional production-ready Sentry integration controlled through environment settings.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added Sentry settings to config (`SENTRY_DSN`, `SENTRY_TRACES_SAMPLE_RATE`, `SENTRY_ENVIRONMENT`).
2. Added Sentry initialization helper with graceful no-op behavior when DSN is empty.
3. Wired Sentry initialization into app startup flow.
4. Added unit tests for Sentry setup behavior.
