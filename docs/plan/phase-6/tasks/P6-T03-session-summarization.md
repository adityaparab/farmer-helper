# P6-T03 - Add optional summarization for long sessions

## Sub-issue description
### Objective
Provide optional summarization of long sessions to keep downstream context bounded while preserving key conversational facts.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added session summarization schemas in `src/farmer_helper/schemas/session.py`.
2. Added optional deterministic summarizer in `src/farmer_helper/services/session/summarizer.py`.
3. Added threshold/no-op behavior tests in `tests/unit/test_session_summarizer.py`.

## Decisions made
- Summarization is optional and deterministic for reproducible tests.
- Summary output should be concise and suitable for prompt context injection.
