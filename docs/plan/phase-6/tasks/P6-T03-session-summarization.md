# P6-T03 - Add optional summarization for long sessions

## Sub-issue description
### Objective
Provide optional summarization of long sessions to keep downstream context bounded while preserving key conversational facts.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add deterministic session summarization service over bounded recent messages.
2. Define summary trigger rules (message threshold and summary length bounds).
3. Add unit tests for summary activation and no-op behavior.

## Decisions made
- Summarization is optional and deterministic for reproducible tests.
- Summary output should be concise and suitable for prompt context injection.
