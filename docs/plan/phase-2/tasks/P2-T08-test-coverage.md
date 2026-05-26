# P2-T08 - Add unit, integration, and failure-path tests

## Sub-issue description
### Objective
Expand test coverage for ingestion orchestration and failure-path handling so pipeline behavior is validated end-to-end.

## Implementation status
- Status: In progress
- Started: 2026-05-26
- Completed: -

## Next work
1. Add orchestration-level ingestion flow tests.
2. Add failure-path tests for extraction/normalization/chunking errors.
3. Validate deterministic status updates across successful and failed runs.

## Decisions made
- Start with high-value failure paths first to prevent regressions in status/error handling.
- Keep test fixtures deterministic and minimal.
