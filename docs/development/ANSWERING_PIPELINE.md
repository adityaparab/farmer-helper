# Answering Pipeline

## Overview
The answering pipeline converts a grounded question plus retrieved context into a safe, citation-aware answer response.

Primary flow:
1. Prompt build and policy decision (`PromptBuilder`)
2. Optional short-circuit for `clarify` or `refuse`
3. LLM generation through provider abstraction (`LLMProvider`)
4. Deterministic citation mapping (`CitationMapper`)
5. Structured diagnostics logging (`AnswerDiagnosticsLogger`)

## Prompting behavior
Prompt construction is deterministic and consists of:
- System prompt: grounded agricultural assistant constraints.
- User prompt: normalized question, grounding context block, and output instructions.

Grounding instructions in prompt enforce:
- context-only answering
- explicit insufficiency acknowledgement
- citation format hints (`[doc:<id> chunk:<index>]`)

## Decision policy
`PromptBuilder` emits one of three decisions:
- `answer`
- `clarify`
- `refuse`

Stable policy codes:
- Refusal: `REFUSAL_UNSAFE_REQUEST`
- Clarify: `CLARIFY_NEED_DETAIL`
- Clarify: `CLARIFY_AMBIGUOUS_REQUEST`
- Clarify: `CLARIFY_MISSING_CONTEXT`

Policy guarantees:
- deterministic, rule-based decisioning
- no provider call for `clarify` or `refuse`
- explicit code/message fields in answer response payloads

## Provider abstraction
Provider contracts:
- Request: `LLMGenerateRequest` (model, messages, max_tokens, temperature)
- Response: `LLMGenerateResponse` (text, finish_reason, token usage)
- Error: `LLMProviderError` (code, message, retryable)

The API/service layer should only depend on `LLMProvider` interface, not provider-specific SDK details.

## Provider switching workflow
To add or switch a provider:
1. Implement `LLMProvider.generate` with deterministic error translation to `LLMProviderError`.
2. Keep `LLMGenerateRequest` and `LLMGenerateResponse` semantics stable.
3. Wire provider construction in route/service builder function.
4. Re-run full gates and regression tests.
5. Verify diagnostics fields still emit expected values.

## Citation mapping
Citations are mapped from retrieved chunks with deterministic behavior:
- deduplication key: `(document_id, chunk_index, content_hash)`
- keep highest scoring duplicate
- stable ordering by score desc, then identity tie-break fields

## Diagnostics and observability
Structured log event: `answer.generation.completed`

Logged fields:
- `answer_decision`
- `answer_model`
- `answer_citations_count`
- `answer_input_tokens`
- `answer_output_tokens`
- `answer_confidence`
- `answer_total_ms`

These logs support latency and usage tracking without high-cardinality payload noise.

## Safety notes
- Unsafe intent requests are refused before model invocation.
- Ambiguous or under-specified requests return clarification guidance.
- Missing grounding context returns explicit context-needed clarification.
