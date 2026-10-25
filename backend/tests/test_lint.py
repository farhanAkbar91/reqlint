import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_lint_endpoint_empty(client: AsyncClient):
    # Register & Login
    email = "lint_user@example.com"
    pwd = "SecretP@ss123"
    await client.post("/api/v1/auth/register", json={
        "name": "Lint User", "email": email, "password": pwd, "password_confirmation": pwd
    })
    login_res = await client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    token = login_res.json()["data"]["access_token"]

    resp = await client.post(
        "/api/v1/lint",
        json={"konten": ""},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["data"]["skor_perkiraan"] == 100.0
    assert len(data["data"]["temuan"]) == 0

@pytest.mark.asyncio
async def test_lint_endpoint_detects_ambiguity(client: AsyncClient):
    login_res = await client.post("/api/v1/auth/login", json={"email": "lint_user@example.com", "password": "SecretP@ss123"})
    token = login_res.json()["data"]["access_token"]

    resp = await client.post(
        "/api/v1/lint",
        json={"konten": "As a user, I want the system to be fast so that I can work easily."},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    categories = [f["kategori_cacat"] for f in data["data"]["temuan"]]
    assert "AMBIGUITY" in categories
    assert data["data"]["ringkasan"]["ambiguity"] >= 1
