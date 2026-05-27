from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient

from farmer_helper.db.base import get_engine
from farmer_helper.db.models.base import Base
from farmer_helper.main import app


def _trigger_payload(document_id: int) -> dict[str, object]:
    return {
        "document_id": document_id,
        "model": "mock-embedding-v1",
        "provider": "mock-provider",
        "version": "v1",
        "batch_size": 2,
        "dimensions": 8,
        "chunks": [
            {
                "chunk_index": 0,
                "text": f"soil note {document_id}",
                "content_hash": f"h-{document_id}-0",
            },
            {
                "chunk_index": 1,
                "text": f"water note {document_id}",
                "content_hash": f"h-{document_id}-1",
            },
        ],
    }


def test_concurrent_embedding_and_query_paths_coexist() -> None:
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Seed retrieval data before concurrent read/write workload begins.
    client = TestClient(app)
    seeded = client.post("/embeddings/trigger", json=_trigger_payload(9800))
    assert seeded.status_code == 200

    def _run_embedding(index: int) -> int:
        with TestClient(app) as worker_client:
            response = worker_client.post(
                "/embeddings/trigger", json=_trigger_payload(9801 + index)
            )
            return response.status_code

    def _run_query() -> int:
        with TestClient(app) as worker_client:
            response = worker_client.post(
                "/retrieval/query",
                json={
                    "query_text": "soil moisture guidance",
                    "query_vector": [0.2] * 8,
                    "top_k": 3,
                    "provider": "mock-provider",
                    "model": "mock-embedding-v1",
                    "version": "v1",
                    "vector_weight": 0.0,
                    "keyword_weight": 1.0,
                    "reranker": "none",
                },
            )
            return response.status_code

    statuses: list[int] = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(_run_embedding, i) for i in range(4)]
        futures.extend(executor.submit(_run_query) for _ in range(4))
        for future in futures:
            statuses.append(future.result())

    assert len(statuses) == 8
    assert all(status == 200 for status in statuses)
