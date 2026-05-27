# Retrieval Pipeline

## Overview
The retrieval pipeline combines vector and keyword retrieval, applies deterministic fusion, and optionally reranks results.

Pipeline stages:
1. Vector retrieval (`VectorRetrievalService`)
2. Keyword retrieval (`KeywordRetrievalService`)
3. Fusion and deduplication (`RetrievalFusionService`)
4. Optional reranking (`Reranker` implementations)
5. Response mapping with citation metadata and retrieval metrics (`RetrievalQueryService`)

## API endpoint
Route: `POST /retrieval/query`

Request schema (`RetrievalRequest`):
- `query_text`: keyword query string.
- `query_vector`: query embedding vector.
- `top_k`: number of final results requested.
- `provider`, `model`, `version`: retrieval scope for stored chunk embeddings.
- `vector_weight`, `keyword_weight`: fusion weights in `[0, 1]`.
- `reranker`: reranker selector (`none`, `pass_through`, `keyword_boost`).

Response schema (`RetrievalResponse`):
- `items`: ranked retrieval items with score and citation metadata.
- `metrics`: deterministic retrieval counts per stage.

## Fusion behavior
Fusion input sets:
- `vector_results`: top-K vector-scored chunk candidates.
- `keyword_results`: top-K keyword-scored chunk candidates.

Deduplication identity key:
- `(document_id, chunk_index, content_hash)`

Fusion score formula:
- `fused_score = vector_score * vector_weight + keyword_score * keyword_weight`

Tie-break order (deterministic):
1. higher `fused_score`
2. higher `vector_score`
3. higher `keyword_score`
4. lower `document_id`
5. lower `chunk_index`

## Reranking behavior
Rerankers are pluggable via the `Reranker` interface.

Available implementations:
- `none` or `disabled`: skip reranking.
- `pass_through`: keep fused scores; apply deterministic ordering and top-K truncation.
- `keyword_boost`: add a bounded bonus to fused score for keyword matches, then re-sort deterministically.

Unsupported reranker values return HTTP 400 from the retrieval route.

## Citation metadata
Each retrieval item includes `citation` metadata:
- `document_id`
- `chunk_index`
- `content_hash`

This allows downstream answer-generation layers to map retrieval outputs to source chunks deterministically.

## Retrieval metrics
`metrics` fields in response:
- `vector_count`: number of vector results used by fusion.
- `keyword_count`: number of keyword results used by fusion.
- `fused_count`: number of deduplicated fused candidates before reranking/top-K output.
- `returned_count`: number of returned items in `items`.

## Diagnostics logging
The retrieval query service emits `retrieval.query.completed` structured logs with:
- identity fields: provider/model/version/top_k/reranker
- scoring configuration: vector and keyword weights
- counts: vector, keyword, fused, returned
- timings (ms): vector, keyword, fusion, rerank, total

Request ID propagation is handled by global logging filters, so retrieval diagnostics can be correlated with API requests.
