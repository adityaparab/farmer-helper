# P5-T05 - Add refusal and ambiguity handling

## Sub-issue description
### Objective
Harden answer-generation behavior for unsafe or ambiguous requests with explicit, user-facing refusal and clarification handling.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added stable policy code fields to prompt and answer schemas in `src/farmer_helper/schemas/answering.py`.
2. Hardened refusal and clarification policy logic in `src/farmer_helper/services/answering/prompt_builder.py`.
3. Propagated policy codes through answer generation in `src/farmer_helper/services/answering/generation_service.py`.
4. Added regression tests in `tests/unit/test_prompt_builder.py`, `tests/unit/test_answer_generation_service.py`, and `tests/unit/test_answer_generation_route.py`.

## Decisions made
- Decision outputs must remain deterministic for testability.
- Policy handling should not invoke LLM provider when refusal or clarification is selected.
