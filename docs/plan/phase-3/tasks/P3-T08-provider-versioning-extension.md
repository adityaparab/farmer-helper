# P3-T08 - Document provider versioning and extension path

## Sub-issue description
### Objective
Document embedding provider versioning strategy and extension workflow for introducing new providers safely.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added provider versioning and extension guide `docs/development/EMBEDDING_PROVIDERS.md`.
2. Updated `README.md` with Phase 3 implementation references.
3. Updated `docs/development/ARCHITECTURE_OVERVIEW.md` with embedding pipeline capability and docs links.

## Decisions made
- Keep provider versioning explicit in persisted records and trigger interfaces.
- Prioritize clear extension contracts over provider-specific implementation details.
