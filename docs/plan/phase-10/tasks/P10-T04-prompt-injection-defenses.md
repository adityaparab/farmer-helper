# P10-T04 - Add prompt injection defenses and tests

## Sub-issue description
### Objective
Detect and safely refuse likely prompt-injection attempts in prompt construction flow.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added known-pattern prompt-injection detection in prompt builder.
2. Added deterministic refusal code `REFUSAL_PROMPT_INJECTION`.
3. Added audit event emission for prompt-injection rejection.
4. Added unit regression coverage for prompt-injection refusal path.
