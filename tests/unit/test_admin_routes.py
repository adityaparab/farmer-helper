from fastapi.testclient import TestClient

from farmer_helper.db.base import get_engine
from farmer_helper.db.models.base import Base
from farmer_helper.main import app


def _reset_db() -> None:
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def _admin_headers(client: TestClient, actor_id: str) -> dict[str, str]:
    login = client.post("/auth/login", json={"username": "admin", "password": "P@ssw0rd"})
    assert login.status_code == 200
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "x-actor-id": actor_id}


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
