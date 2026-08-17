from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_audit_indonesian_endpoint():
    payload = {
        "requirement_text": "Sistem sebaiknya dapat memproses data transaksi pengguna dengan cepat."
    }
    response = client.post("/api/v1/requirements/audit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["detected_language"] == "id"
    assert len(data["smells"]) > 0

def test_audit_english_endpoint():
    payload = {
        "requirement_text": "The system should process user payment data quickly."
    }
    response = client.post("/api/v1/requirements/audit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["detected_language"] == "en"
    assert len(data["smells"]) > 0
