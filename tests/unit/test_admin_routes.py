from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from farmer_helper.core.config import get_settings
from farmer_helper.db.base import get_engine
from farmer_helper.db.models.base import Base
from farmer_helper.main import app

PDF_BYTES = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\n%%EOF\n"


def _reset_db() -> None:
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def _admin_headers(client: TestClient, actor_id: str) -> dict[str, str]:
    login = client.post("/auth/login", json={"username": "admin", "password": "P@ssw0rd"})
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}", "x-actor-id": actor_id}
    api_key = get_settings().security_api_key
    if api_key is not None:
        headers["x-api-key"] = api_key
    return headers


def _configure_upload_dir(monkeypatch: pytest.MonkeyPatch, upload_dir: Path) -> None:
    monkeypatch.setenv("ADMIN_UPLOAD_DIR", str(upload_dir))
    monkeypatch.setenv("ADMIN_UPLOAD_MAX_SIZE_BYTES", "1024")
    get_settings.cache_clear()


def test_admin_ingestion_reindex_and_status_workflow() -> None:
    _reset_db()
    client = TestClient(app)
    headers = _admin_headers(client, "admin-user")

    create = client.post(
        "/admin/ingestion/jobs",
        headers=headers,
        json={
            "source_path": "docs/source/a.pdf",
            "content_hash": "hash-a",
            "content_version": "v1",
        },
    )
    assert create.status_code == 201
    created = create.json()
    assert created["status"] == "pending"

    update = client.post(
        f"/admin/jobs/{created['job_id']}/status",
        headers=headers,
        json={"status": "processing"},
    )
    assert update.status_code == 200
    assert update.json()["status"] == "processing"

    reindex = client.post(
        "/admin/reindex/jobs",
        headers=headers,
        json={
            "document_id": created["document_id"],
            "pipeline_version": "v2",
            "model_version": "mock-embedding-v2",
        },
    )
    assert reindex.status_code == 201
    assert reindex.json()["status"] == "pending"


def test_admin_dashboard_metrics_contract() -> None:
    _reset_db()
    client = TestClient(app)
    headers = _admin_headers(client, "metrics-admin")

    create = client.post(
        "/admin/ingestion/jobs",
        headers=headers,
        json={
            "source_path": "docs/source/metrics.pdf",
            "content_hash": "hash-metrics",
            "content_version": "v1",
        },
    )
    assert create.status_code == 201
    job_id = create.json()["job_id"]

    processing = client.post(
        f"/admin/jobs/{job_id}/status",
        headers=headers,
        json={"status": "processing"},
    )
    assert processing.status_code == 200

    update = client.post(
        f"/admin/jobs/{job_id}/status",
        headers=headers,
        json={"status": "succeeded"},
    )
    assert update.status_code == 200

    gold = client.post(
        "/admin/gold-answers",
        headers=headers,
        json={"question": "What is compost?", "answer": "Compost is decomposed organic matter."},
    )
    assert gold.status_code == 201

    review = client.post(
        "/admin/review-queue",
        headers=headers,
        json={"issue_type": "source_gap", "details": "Need stronger citation coverage"},
    )
    assert review.status_code == 201

    metrics = client.get("/admin/dashboard/metrics", headers=headers)
    assert metrics.status_code == 200

    payload = metrics.json()
    assert {item["label"] for item in payload["cards"]} == {
        "Documents",
        "Embedded chunks",
        "Chat messages",
        "QA review items",
        "Audit events",
    }
    assert payload["ingestion_jobs_by_status"] == {"succeeded": 1}
    assert payload["gold_answers_by_status"] == {"draft": 1}
    assert payload["qa_review_items_by_status"] == {"pending": 1}
    assert payload["chat_sessions_by_status"] == {}
    assert payload["embedding_jobs_by_status"] == {}


def test_admin_pdf_upload_stores_file_starts_job_and_audits(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _reset_db()
    _configure_upload_dir(monkeypatch, tmp_path / "uploads")
    client = TestClient(app)
    headers = _admin_headers(client, "upload-admin")

    upload = client.post(
        "/admin/documents/upload",
        headers=headers,
        data={"content_version": "content-v2"},
        files={"file": ("soil-guide.pdf", PDF_BYTES, "application/pdf")},
    )
    assert upload.status_code == 201

    payload = upload.json()
    assert payload["status"] == "pending"
    assert payload["document_created"] is True
    assert payload["size_bytes"] == len(PDF_BYTES)
    assert len(payload["content_hash"]) == 64
    assert Path(payload["source_path"]).exists()

    duplicate = client.post(
        "/admin/documents/upload",
        headers=headers,
        data={"content_version": "content-v2"},
        files={"file": ("soil-guide.pdf", PDF_BYTES, "application/pdf")},
    )
    assert duplicate.status_code == 201
    assert duplicate.json()["document_id"] == payload["document_id"]
    assert duplicate.json()["document_created"] is False
    assert duplicate.json()["job_id"] != payload["job_id"]

    logs = client.get("/admin/access-audit", headers=headers)
    assert logs.status_code == 200
    assert any(item["action"] == "admin.document.upload" for item in logs.json())

    get_settings.cache_clear()


def test_admin_pdf_upload_rejects_invalid_type_and_size(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _reset_db()
    _configure_upload_dir(monkeypatch, tmp_path / "uploads")
    client = TestClient(app)
    headers = _admin_headers(client, "upload-admin")

    invalid_type = client.post(
        "/admin/documents/upload",
        headers=headers,
        files={"file": ("notes.txt", PDF_BYTES, "application/pdf")},
    )
    assert invalid_type.status_code == 400

    monkeypatch.setenv("ADMIN_UPLOAD_MAX_SIZE_BYTES", "8")
    get_settings.cache_clear()
    too_large = client.post(
        "/admin/documents/upload",
        headers=headers,
        files={"file": ("large.pdf", PDF_BYTES, "application/pdf")},
    )
    assert too_large.status_code == 413

    get_settings.cache_clear()


def test_admin_version_gold_answer_review_queue_and_audit() -> None:
    _reset_db()
    client = TestClient(app)
    editor_headers = _admin_headers(client, "editor-1")
    editor_2_headers = {**editor_headers, "x-actor-id": "editor-2"}
    reviewer_headers = {**editor_headers, "x-actor-id": "reviewer-1"}
    reviewer_2_headers = {**editor_headers, "x-actor-id": "reviewer-2"}

    version = client.post(
        "/admin/versions",
        headers=editor_headers,
        json={
            "content_version": "content-v3",
            "model_version": "model-v2",
            "pipeline_version": "pipeline-v5",
            "notes": "rollout",
        },
    )
    assert version.status_code == 201
    assert version.json()["created_by"] == "editor-1"

    gold = client.post(
        "/admin/gold-answers",
        headers=editor_headers,
        json={"question": "How to mulch?", "answer": "Use organic mulch."},
    )
    assert gold.status_code == 201
    gold_id = gold.json()["id"]

    gold_update = client.post(
        f"/admin/gold-answers/{gold_id}",
        headers=editor_2_headers,
        json={"status": "approved"},
    )
    assert gold_update.status_code == 200
    assert gold_update.json()["status"] == "approved"
    assert gold_update.json()["editor_id"] == "editor-2"

    review = client.post(
        "/admin/review-queue",
        headers=reviewer_headers,
        json={"issue_type": "citation_mismatch", "details": "Check source mapping"},
    )
    assert review.status_code == 201
    review_id = review.json()["id"]

    review_update = client.post(
        f"/admin/review-queue/{review_id}",
        headers=reviewer_2_headers,
        json={"status": "in_review", "assigned_to": "reviewer-2"},
    )
    assert review_update.status_code == 200
    assert review_update.json()["status"] == "in_review"

    logs = client.get("/admin/access-audit", headers=editor_headers)
    assert logs.status_code == 200
    assert len(logs.json()) >= 4
    assert any(item["action"] == "admin.version.create" for item in logs.json())
