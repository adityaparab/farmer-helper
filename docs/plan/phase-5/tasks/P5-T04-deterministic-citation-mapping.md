# P5-T04 - Add deterministic citation mapping

## Sub-issue description
### Objective
Ensure generated answer citations are deterministic, deduplicated, and stably ordered relative to retrieved evidence.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Define deterministic citation mapping service and tie-break behavior.
2. Deduplicate citations by stable identity key.
3. Add unit tests for citation ordering and deduplication.

## Decisions made
- Citation identity should be stable and content-backed.
- Mapping behavior should be deterministic for regression testing.
