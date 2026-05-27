# P5-T03 - Build end-to-end answer generation API

## Sub-issue description
### Objective
Implement an API endpoint that takes a grounded question context and produces a citation-rich answer through the prompt builder and LLM provider abstraction.

## Implementation status
- Status: Completed
- Started: 2026-05-27
- Completed: 2026-05-27

## What was done
1. Added answer-generation request/response schemas in `src/farmer_helper/schemas/answering.py`.
2. Added orchestration service in `src/farmer_helper/services/answering/generation_service.py`.
3. Added mock provider in `src/farmer_helper/services/answering/mock_provider.py` for deterministic local behavior.
4. Added API route in `src/farmer_helper/api/routes/answers.py` and router registration in `src/farmer_helper/main.py`.
5. Added service and route unit tests in `tests/unit/test_answer_generation_service.py` and `tests/unit/test_answer_generation_route.py`.

## Decisions made
- API should preserve clear separation between retrieval context input and generated answer output.
- Provider-specific details should remain behind the provider abstraction.
