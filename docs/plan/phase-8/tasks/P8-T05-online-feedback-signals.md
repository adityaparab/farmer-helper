# P8-T05 - Log online feedback signals

## Sub-issue description
### Objective
Add structured online feedback signal capture to track user-perceived answer quality and identify degradation trends over time.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added typed feedback schema contracts in `src/farmer_helper/schemas/answering.py`.
2. Added structured logging signal service in `src/farmer_helper/services/evaluation/feedback_signals.py`.
3. Added `POST /answers/feedback` route for online feedback capture.
4. Added tests for route acceptance and structured logging payload fields.

## Decisions made
- Signals should remain low-cardinality and privacy-conscious.
- Signal contracts should be typed and testable.
