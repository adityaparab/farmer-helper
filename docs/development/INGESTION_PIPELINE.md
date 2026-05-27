# Ingestion Pipeline Flow and Operations Guide

## Scope
This guide documents the current Phase 2 ingestion pipeline behavior, module flow, and operational troubleshooting guidance.

## End-to-end flow
1. Validate input file (`FileValidator`) to enforce existence, file type, and size rules.
2. Extract pages from PDF (`PdfExtractor`) with deterministic error codes.
3. Normalize extracted text (`TextNormalizer`) for stable chunking behavior.
4. Chunk normalized text (`TextChunker`) using page-aware, configurable chunks.
5. Enrich chunk metadata (`ChunkMetadataEnricher`) with page ranges, version, and content hash.
6. Enforce idempotent document persistence (`IngestionIdempotencyService`) using `content_hash + version`.
7. Persist job state transitions (`IngestionStatusService`) and emit trace events (`IngestionTraceLogger`).

## Admin PDF uploads
- Admin users can create pending ingestion jobs through `POST /admin/documents/upload`.
- The endpoint accepts multipart form data with a PDF `file` and optional `content_version`.
- Uploads are stored under `ADMIN_UPLOAD_DIR/<safe-content-version>/<sha256>.pdf`; the default root is `data/uploads/admin`.
- The upload size cap is controlled by `ADMIN_UPLOAD_MAX_SIZE_BYTES`, defaulting to 25 MiB.
- Accepted uploads must have a `.pdf` filename, PDF content type, non-empty body, stay within the configured size cap, and start with the `%PDF-` signature.
- The endpoint computes the SHA-256 content hash, reuses existing documents by `content_hash + content_version`, starts a new pending ingestion job, and records an `admin.document.upload` audit event.

## Primary modules
- Input validation: `src/farmer_helper/services/ingestion/file_validator.py`
- PDF extraction: `src/farmer_helper/services/ingestion/pdf_extractor.py`
- Text normalization: `src/farmer_helper/services/ingestion/text_normalizer.py`
- Chunking: `src/farmer_helper/services/ingestion/text_chunker.py`
- Metadata enrichment: `src/farmer_helper/services/ingestion/chunk_metadata_enricher.py`
- Idempotency: `src/farmer_helper/services/ingestion/idempotency_service.py`
- Status + tracing: `src/farmer_helper/services/ingestion/status_service.py`, `src/farmer_helper/services/ingestion/trace_logger.py`

## Lifecycle trace events
The status service emits deterministic event names:
- `ingestion.job.started`
- `ingestion.job.processing`
- `ingestion.job.succeeded`
- `ingestion.job.failed`

Each event includes structured fields for correlation and diagnostics:
- `job_id`
- `document_id`
- `ingestion_stage`
- `ingestion_status`
- `error_code`, `error_message` (failed events only)

## Local verification checklist
1. Run quality gates:
   - `ruff check src tests`
   - `black --check src tests`
   - `mypy src`
   - `pytest -q`
2. Verify ingestion test coverage:
   - `pytest tests/unit/test_file_validator.py -q`
   - `pytest tests/unit/test_pdf_extractor.py -q`
   - `pytest tests/unit/test_text_normalizer.py -q`
   - `pytest tests/unit/test_text_chunker.py -q`
   - `pytest tests/unit/test_chunk_metadata_enricher.py -q`
   - `pytest tests/unit/test_ingestion_status_service.py -q`
   - `pytest tests/unit/test_idempotency_service.py -q`
   - `pytest tests/unit/test_ingestion_trace_logging.py -q`
   - `pytest tests/integration/test_ingestion_pipeline_paths.py -q`

## Common failure modes
- Missing file path
  - Error code: `INGESTION_INPUT_NOT_FOUND`
  - Action: confirm file path and mount/working directory.
- Unsupported extension
  - Error code: `INGESTION_INPUT_UNSUPPORTED_EXTENSION`
  - Action: provide a supported source type (`.pdf` currently).
- Corrupt or unreadable PDF
  - Error code: `INGESTION_PDF_CORRUPT_OR_UNREADABLE` or `INGESTION_PDF_READ_ERROR`
  - Action: re-export/repair PDF and re-run extraction.
- Invalid state transition
  - Exception: `ValueError` from status service
  - Action: verify transition order is `pending -> processing -> {succeeded|failed}`.

## Operational guidance
- Use idempotency guard before creating new document records to avoid duplicate ingestion artifacts.
- Use status service transitions as the source of truth for job lifecycle state.
- Use trace event names and correlation fields to debug ingestion stage failures quickly.
