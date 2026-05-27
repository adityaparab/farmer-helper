# P5-T02 - Add LLM provider abstraction

## Sub-issue description
### Objective
Add a provider-agnostic LLM interface and error contract to support safe answer generation and future provider switching.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added LLM provider request/response schemas in `src/farmer_helper/schemas/answering.py`.
2. Added `LLMProvider` abstraction and `LLMProviderError` in `src/farmer_helper/services/answering/provider.py`.
3. Added deterministic contract tests in `tests/unit/test_llm_provider_abstraction.py`.

## Decisions made
- Provider contract should separate prompt preparation from model invocation.
- Provider errors should expose stable machine-readable codes and retryability.
