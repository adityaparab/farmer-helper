# P5-T01 - Build prompt builder with refusal and clarification policy

## Sub-issue description
### Objective
Create a deterministic prompt builder that assembles grounded answer prompts and enforces refusal/clarification policy decisions before model invocation.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added answering prompt schemas in `src/farmer_helper/schemas/answering.py`.
2. Added prompt builder service with deterministic refusal and clarification policy in `src/farmer_helper/services/answering/prompt_builder.py`.
3. Added unit tests in `tests/unit/test_prompt_builder.py`.

## Decisions made
- Policy is deterministic and keyword/shape based for repeatable tests.
- Clarification is returned for underspecified or context-free requests.
- Refusal is returned for unsafe request terms.
