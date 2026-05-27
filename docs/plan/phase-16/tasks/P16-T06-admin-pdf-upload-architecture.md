# P16-T06 - Define admin PDF upload architecture and controls

## Sub-issue description
### Objective
Define the secure PDF upload architecture for admin users and its integration with ingestion jobs.

### Acceptance criteria
- Upload constraints cover file type, size, storage path, and audit logging.
- Ingestion job trigger and status behavior are documented.
- Failure behavior and security controls are testable.

## Implementation status
- Status: Completed
- Remote issue: https://github.com/adityaparab/farmer-helper/issues/175

## Architecture
- Endpoint: `POST /admin/documents/upload` under existing admin JWT/RBAC protection.
- Request shape: multipart form data with `file` and optional `content_version`.
- Response shape: typed `AdminPdfUploadResponse` with pending ingestion `job_id`, `document_id`, `source_path`, `content_hash`, `size_bytes`, and `document_created`.
- Storage path: `ADMIN_UPLOAD_DIR/<safe-content-version>/<sha256>.pdf`; default `ADMIN_UPLOAD_DIR=data/uploads/admin`.
- Size limit: `ADMIN_UPLOAD_MAX_SIZE_BYTES`, default `26214400` bytes.
- File type controls: `.pdf` extension, PDF content type, non-empty body, configured size cap, and `%PDF-` signature check.
- Idempotency: documents are reused by `content_hash + content_version`; repeated uploads start a new pending ingestion job for the existing document.
- Audit logging: accepted uploads write `admin.document.upload` entries with document ID, content hash, and byte size.

## Failure behavior
- Non-PDF filename/content type: `400`.
- Empty upload: `400`.
- Oversized upload: `413`.
- Invalid PDF signature: `400`.
- Rejected uploads do not create document or ingestion-job rows.

## Evidence
- Tracked remotely under Phase 16 Epic: https://github.com/adityaparab/farmer-helper/issues/168
- Added upload settings in `src/farmer_helper/core/config.py` and `config/examples/.env.development.example`.
- Added multipart support dependency in `pyproject.toml`.
- Added typed upload response contract in `src/farmer_helper/schemas/admin.py`.
- Added upload endpoint in `src/farmer_helper/api/routes/admin.py`.
- Added success, idempotency, audit, invalid type, and oversize coverage in `tests/unit/test_admin_routes.py`.
- Validation: `ruff check .` passes.
- Validation: `pytest tests/unit/test_admin_routes.py` passes.
