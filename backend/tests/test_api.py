from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_audit_indonesian_user_story_endpoint():
    payload = {
        "requirement_text": "Sebagai pembeli, saya sebaiknya dapat membayar dengan cepat, sehingga transaksi selesai."
    }
    response = client.post("/api/v1/requirements/audit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["detected_language"] == "id"
    assert len(data["smells"]) > 0
    rule_ids = [s["rule_id"] for s in data["smells"]]
    assert "WEAK_DIRECTIVE_ID" in rule_ids
    assert "SUBJECTIVE_ADJECTIVE_ID" in rule_ids

def test_audit_english_user_story_endpoint():
    payload = {
        "requirement_text": "As a buyer, I should be able to checkout easily, so that I save time."
    }
    response = client.post("/api/v1/requirements/audit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["detected_language"] == "en"
    assert len(data["smells"]) > 0
    rule_ids = [s["rule_id"] for s in data["smells"]]
    assert "WEAK_DIRECTIVE_EN" in rule_ids
    assert "SUBJECTIVE_ADJECTIVE_EN" in rule_ids

