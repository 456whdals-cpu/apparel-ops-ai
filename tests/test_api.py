from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_seeded_items_and_search():
    with TestClient(app) as client:
        items = client.get("/api/v1/items?limit=5")
        search = client.post("/api/v1/search", json={"query": "네이비 재킷 검수", "limit": 3})
    assert items.status_code == 200
    assert len(items.json()) == 5
    assert search.status_code == 200
    assert search.json()["total_candidates"] >= 100
    assert search.json()["elapsed_ms"] >= 0


def test_validation_rejects_short_query():
    with TestClient(app) as client:
        response = client.post("/api/v1/search", json={"query": "a"})
    assert response.status_code == 422


