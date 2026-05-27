# P6-T07 - Add transcript export/import

## Sub-issue description
### Objective
Provide deterministic transcript export and import utilities for session portability and debugging workflows.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add transcript DTO/schema for exported session + messages.
2. Add repository/service methods for exporting and importing transcripts.
3. Add tests for round-trip integrity and deterministic ordering.

## Decisions made
- Export/import format should remain stable and versionable.
- Round-trip behavior must preserve turn order and message role fidelity.
