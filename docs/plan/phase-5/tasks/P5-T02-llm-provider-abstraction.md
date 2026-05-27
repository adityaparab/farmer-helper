# P5-T02 - Add LLM provider abstraction

## Sub-issue description
### Objective
Add a provider-agnostic LLM interface and error contract to support safe answer generation and future provider switching.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Define provider request/response schemas for answer generation.
2. Implement abstract LLM provider interface and provider error type.
3. Add deterministic unit tests for provider contract semantics.

## Decisions made
- Provider contract should separate prompt preparation from model invocation.
- Provider errors should expose stable machine-readable codes and retryability.
