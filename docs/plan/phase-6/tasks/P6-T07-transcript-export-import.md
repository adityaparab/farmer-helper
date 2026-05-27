# P6-T07 - Add transcript export/import

## Sub-issue description
### Objective
Provide deterministic transcript export and import utilities for session portability and debugging workflows.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added transcript schemas in `src/farmer_helper/schemas/session.py`.
2. Added transcript service in `src/farmer_helper/services/session/transcript_service.py`.
3. Added round-trip tests in `tests/unit/test_session_transcript_service.py`.

## Decisions made
- Export/import format should remain stable and versionable.
- Round-trip behavior must preserve turn order and message role fidelity.
