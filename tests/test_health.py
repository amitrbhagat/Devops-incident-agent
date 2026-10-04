from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_returns_ready():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_correlation_id_is_echoed_back():
    response = client.get("/health", headers={"X-Correlation-ID": "abc123"})
    assert response.headers["X-Correlation-ID"] == "abc123"


def test_correlation_id_is_generated_when_missing():
    response = client.get("/health")
    assert len(response.headers["X-Correlation-ID"]) == 32
