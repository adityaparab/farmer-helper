# P6-T01 - Add session and message schemas

## Sub-issue description
### Objective
Introduce deterministic session/message contracts and persistence schemas to support multi-turn memory in later steps.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added session/message models to persistence schema and migration.
2. Added typed API/service schemas for session/message payloads.
3. Added session/message repository and deterministic unit tests.

## Decisions made
- Session/message identity and ordering must be deterministic and testable.
- Message role and turn index constraints are validated via typed schemas.
