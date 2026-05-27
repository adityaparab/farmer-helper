# P8-T05 - Log online feedback signals

## Sub-issue description
### Objective
Add structured online feedback signal capture to track user-perceived answer quality and identify degradation trends over time.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Define feedback signal schema and logging event names.
2. Add deterministic logging hooks for feedback capture.
3. Add tests for signal payload shape and field stability.
4. Ensure signal fields align with future eval expansion workflows.

## Decisions made
- Signals should remain low-cardinality and privacy-conscious.
- Signal contracts should be typed and testable.
