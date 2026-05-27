# P5-T08 - Document prompting and provider switching

## Sub-issue description
### Objective
Document prompt construction rules, decision policy behavior, and how to switch or extend answer-generation providers safely.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added `docs/development/ANSWERING_PIPELINE.md` with prompt construction and policy behavior.
2. Documented provider abstraction contracts and provider-switching workflow.
3. Documented deterministic citation mapping and answer diagnostics logging fields.
4. Added references in `README.md` and `docs/development/ARCHITECTURE_OVERVIEW.md`.

## Decisions made
- Documentation should map directly to current service and schema contracts.
- Include deterministic behavior guarantees to support regression and review.
