# P2-T08 - Add unit, integration, and failure-path tests

## Sub-issue description
### Objective
Expand test coverage for ingestion orchestration and failure-path handling so pipeline behavior is validated end-to-end.

## Implementation status
- Status: Completed
- Started: 2026-05-26
- Completed: 2026-05-26

## What was done
1. Added integration test coverage in `tests/integration/test_ingestion_pipeline_paths.py`.
2. Added re-ingestion path test validating idempotent document reuse with successful job completion.
3. Added failure-path test validating status failure persistence on file validation errors.

## Decisions made
- Prioritized high-value pipeline collaboration paths across idempotency and status services.
- Kept tests deterministic with in-memory SQLite and explicit assertions on persisted state.
