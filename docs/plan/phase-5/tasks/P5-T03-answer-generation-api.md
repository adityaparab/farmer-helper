# P5-T03 - Build end-to-end answer generation API

## Sub-issue description
### Objective
Implement an API endpoint that takes a grounded question context and produces a citation-rich answer through the prompt builder and LLM provider abstraction.

## Implementation status
- Status: In progress
- Started: 2026-05-27
- Completed: -

## Next work
1. Add answer-generation request/response schemas for API transport.
2. Compose prompt builder and LLM provider into a service orchestrator.
3. Add route and unit tests for success and provider-failure handling.

## Decisions made
- API should preserve clear separation between retrieval context input and generated answer output.
- Provider-specific details should remain behind the provider abstraction.
