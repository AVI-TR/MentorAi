from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Test the root welcoming endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Mentor AI" in data["message"]
    assert "version" in data
    assert data["health"] == "/api/v1/health"


def test_health_check_endpoint(client: TestClient):
    """Test the /api/v1/health endpoint and verify database connectivity."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["project"] == "Mentor AI"
    assert data["database"] == "connected"
