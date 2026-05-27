# P6-T04 - Pass bounded context through retrieval and answering

## Sub-issue description
### Objective
Thread bounded follow-up context into retrieval and answering requests so multi-turn behavior remains grounded and explainable.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Define bounded-context transport schema between session and answering layers.
2. Integrate context resolver output into answer-generation request flow.
3. Add tests ensuring deterministic bounded-context propagation.

## Decisions made
- Context propagation should be explicit and bounded by configured limits.
- Integration should avoid breaking existing single-turn API behavior.
