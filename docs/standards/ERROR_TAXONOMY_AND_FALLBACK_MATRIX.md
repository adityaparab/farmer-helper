# Error Taxonomy and Fallback Matrix

## Purpose
Define a consistent error taxonomy, user-facing error contract, and deterministic fallback behavior for all critical flows.

## Error taxonomy

## Category A: Input and contract errors
1. `INPUT_VALIDATION_ERROR`
- Cause: Invalid request schema or unsupported parameter values.
- User response: 400 with structured field details.
- Retry: No.

2. `UNSUPPORTED_REQUEST_ERROR`
- Cause: Request outside supported product scope.
- User response: 422 with guidance.
- Retry: No.

## Category B: External dependency errors
1. `PROVIDER_TIMEOUT_ERROR`
- Cause: Upstream provider timeout.
- User response: 504 with retry-safe guidance.
- Retry: Yes (bounded retries).

2. `PROVIDER_RATE_LIMIT_ERROR`
- Cause: Upstream quota/rate limit exceeded.
- User response: 429 with retry-after metadata if available.
- Retry: Yes (backoff).

3. `PROVIDER_RESPONSE_ERROR`
- Cause: Non-timeout provider failure, malformed payload, unavailable service.
- User response: 502.
- Retry: Yes for transient, no for deterministic failures.

## Category C: Data and pipeline errors
1. `INGESTION_EXTRACTION_ERROR`
2. `INGESTION_NORMALIZATION_ERROR`
3. `EMBEDDING_JOB_ERROR`
4. `RETRIEVAL_FUSION_ERROR`
5. `CITATION_MAPPING_ERROR`
- User response: 500 class (internal workflow failure).
- Retry: Depends on stage and idempotency guard.

## Category D: Platform and persistence errors
1. `DATABASE_CONNECTIVITY_ERROR`
2. `DATABASE_CONSTRAINT_ERROR`
3. `CONFIGURATION_ERROR`
4. `INTERNAL_UNHANDLED_ERROR`
- User response: 500 or 503 depending on recovery expectation.
- Retry: Only for transient connectivity and contention.

## User-facing error contract
All errors must map to:
1. `error_code` (stable machine-readable code)
2. `message` (human-readable summary)
3. `request_id` (traceability)
4. `retryable` (boolean)
5. `category` (taxonomy group)
6. `details` (safe metadata; no sensitive leakage)

## Fallback matrix
| Failure point | Primary behavior | Fallback behavior | User response | Observability fields |
|---|---|---|---|---|
| Embedding provider timeout | Retry with bounded backoff | Queue for async retry and mark partial completion | 202/partial status where applicable | `error_code`, `attempt`, `provider`, `request_id` |
| Retrieval vector search failure | Try vector search | Fall back to keyword-only retrieval | 200 with degraded mode marker | `fallback_mode`, `vector_status`, `request_id` |
| Keyword retrieval failure | Hybrid retrieval | Fall back to vector-only retrieval | 200 with degraded mode marker | `fallback_mode`, `keyword_status`, `request_id` |
| Reranker failure | Apply reranker | Skip reranker and return fused top-K | 200 with reranker skipped marker | `reranker_status`, `fallback_mode`, `request_id` |
| LLM generation provider timeout | Retry bounded | Return safe failure with optional concise fallback response | 504 or guarded fallback message | `provider`, `latency_ms`, `request_id` |
| Citation mapping failure | Build citation links | Refuse answer and return deterministic error | 500 with retry guidance if transient | `citation_status`, `request_id` |
| DB transient connectivity loss | Execute request | Retry transaction or fail fast based on operation type | 503 | `db_status`, `request_id` |

## Determinism rules
1. Fallback selection must be deterministic by error code and operation type.
2. No silent fallback: all degradations must be logged and surfaced in response metadata when safe.
3. Retry count and timeout budgets must be configuration-driven.

## Logging and tracing requirements
1. Include `request_id`, `error_code`, `error_category`, `operation`, `component`, and `fallback_mode`.
2. Emit stage timings for success and failure paths.
3. Redact sensitive payloads and secrets.