# P6-T04 - Pass bounded context through retrieval and answering

## Sub-issue description
### Objective
Thread bounded follow-up context into retrieval and answering requests so multi-turn behavior remains grounded and explainable.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added optional session-context transport fields in `src/farmer_helper/schemas/retrieval.py` and `src/farmer_helper/schemas/answering.py`.
2. Integrated context resolver output into retrieval query flow in `src/farmer_helper/api/routes/retrieval.py`.
3. Integrated context resolver output into answer-generation flow in `src/farmer_helper/services/answering/generation_service.py` and `src/farmer_helper/api/routes/answers.py`.
4. Added propagation and failure-path tests in `tests/unit/test_answer_generation_service.py`, `tests/unit/test_answer_generation_route.py`, and `tests/unit/test_retrieval_route.py`.

## Decisions made
- Context propagation should be explicit and bounded by configured limits.
- Integration should avoid breaking existing single-turn API behavior.
