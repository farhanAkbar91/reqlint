import pytest
from httpx import AsyncClient
from app.services.audit_service import AuditService

@pytest.mark.asyncio
async def test_audit_lifecycle(client: AsyncClient):
    # 1. Register User A
    email_a = "user_a@example.com"
    pwd = "SecretP@ss123"
    await client.post("/api/v1/auth/register", json={
        "name": "User A", "email": email_a, "password": pwd, "password_confirmation": pwd
    })
    login_a = await client.post("/api/v1/auth/login", json={"email": email_a, "password": pwd})
    token_a = login_a.json()["data"]["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # 2. Register User B (for cross-user ownership tests)
    email_b = "user_b@example.com"
    await client.post("/api/v1/auth/register", json={
        "name": "User B", "email": email_b, "password": pwd, "password_confirmation": pwd
    })
    login_b = await client.post("/api/v1/auth/login", json={"email": email_b, "password": pwd})
    token_b = login_b.json()["data"]["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 3. User B has no history yet
    resp_hist_b = await client.get("/api/v1/audits", headers=headers_b)
    assert resp_hist_b.status_code == 200
    assert resp_hist_b.json()["message"] == "Belum ada riwayat audit yang tersedia"
    assert resp_hist_b.json()["data"]["has_any_history"] is False

    # 4. User A submits empty draft -> 422
    resp_empty = await client.post("/api/v1/audits", json={"konten": "   "}, headers=headers_a)
    assert resp_empty.status_code == 422
    data_empty = resp_empty.json()
    assert data_empty["status"] == "error"
    assert data_empty["message"] == "Draf kebutuhan tidak boleh kosong"
    assert data_empty["error_code"] == "EMPTY_DRAFT"

    # 5. User A submits valid draft -> 202
    draft_text = "As a user, I want the system to be fast so that I can work easily."
    resp_create = await client.post(
        "/api/v1/audits",
        json={"konten": draft_text, "judul_klausul": "Kecepatan sistem"},
        headers=headers_a
    )
    assert resp_create.status_code == 202
    data_create = resp_create.json()
    assert data_create["status"] == "success"
    assert data_create["message"] == "Draf diterima dan sedang dianalisis"
    id_audit = data_create["data"]["id_audit"]
    assert "poll_url" in data_create["data"]

    # Execute pipeline synchronously for predictable test state
    await AuditService.run_pipeline(id_audit)

    # 6. Check polling status
    resp_status = await client.get(f"/api/v1/audits/{id_audit}/status", headers=headers_a)
    assert resp_status.status_code == 200
    data_status = resp_status.json()
    assert data_status["data"]["status_audit"] == "COMPLETED"
    assert data_status["data"]["stage2_status"] == "DONE"

    # 7. Get full audit detail
    resp_detail = await client.get(f"/api/v1/audits/{id_audit}", headers=headers_a)
    assert resp_detail.status_code == 200
    detail = resp_detail.json()["data"]
    assert detail["id_audit"] == id_audit
    assert detail["judul_klausul"] == "Kecepatan sistem"
    assert detail["scorecard"] is not None
    assert detail["ringkasan"]["ambiguity"] >= 1
    assert len(detail["temuan"]) > 0
    assert detail["rekomendasi_ai"] is not None
    assert "ai_rewrite" in detail["rekomendasi_ai"]
    assert len(detail["rekomendasi_ai"]["acceptance_criteria"]) > 0

    # 8. SEC-4: User B cannot access User A's audit -> 404, NOT 403!
    resp_cross = await client.get(f"/api/v1/audits/{id_audit}", headers=headers_b)
    assert resp_cross.status_code == 404
    assert resp_cross.json()["message"] == "Data audit tidak ditemukan"

    # 9. 1-Click Apply AI Recommendation
    resp_apply = await client.post(
        f"/api/v1/audits/{id_audit}/apply",
        json={"terapkan": ["rewrite", "acceptance_criteria"]},
        headers=headers_a
    )
    assert resp_apply.status_code == 200
    apply_data = resp_apply.json()
    assert apply_data["status"] == "success"
    assert apply_data["message"] == "Draf berhasil diperbarui"
    assert apply_data["data"]["status_revisi"] == "SUDAH_DIREVISI"
    assert apply_data["data"]["label"] == "Skor Kualitas Terkini"
    assert "Acceptance Criteria" in apply_data["data"]["konten_revisi"]

    # 10. Manual edit revision
    resp_rev = await client.put(
        f"/api/v1/audits/{id_audit}/revision",
        json={"konten_revisi": "As a user, I want the system to respond within 2 seconds so that I can finish work quickly."},
        headers=headers_a
    )
    assert resp_rev.status_code == 200
    assert resp_rev.json()["message"] == "Draf berhasil diperbarui"
    assert resp_rev.json()["data"]["skor_kualitas"] > 0

    # 11. Manual edit with empty text -> 422
    resp_rev_empty = await client.put(
        f"/api/v1/audits/{id_audit}/revision",
        json={"konten_revisi": "   "},
        headers=headers_a
    )
    assert resp_rev_empty.status_code == 422
    assert resp_rev_empty.json()["message"] == "Draf kebutuhan tidak boleh kosong"

    # 12. History List & Search
    resp_list = await client.get("/api/v1/audits", headers=headers_a)
    assert resp_list.status_code == 200
    assert resp_list.json()["data"]["has_any_history"] is True
    assert len(resp_list.json()["data"]["items"]) >= 1

    resp_search_none = await client.get("/api/v1/audits?q=nonexistentqueryxyz", headers=headers_a)
    assert resp_search_none.status_code == 200
    assert resp_search_none.json()["message"] == "Tidak ada riwayat yang cocok dengan pencarian"
    assert resp_search_none.json()["data"]["has_any_history"] is True

    # 13. Export JSON, MD, PDF
    resp_export_json = await client.get(f"/api/v1/audits/{id_audit}/export?format=json", headers=headers_a)
    assert resp_export_json.status_code == 200
    assert resp_export_json.headers["content-type"] == "application/json"
    assert "reqlint-audit" in resp_export_json.headers["content-disposition"]

    resp_export_md = await client.get(f"/api/v1/audits/{id_audit}/export?format=md", headers=headers_a)
    assert resp_export_md.status_code == 200
    assert "text/markdown" in resp_export_md.headers["content-type"]

    resp_export_pdf = await client.get(f"/api/v1/audits/{id_audit}/export?format=pdf", headers=headers_a)
    assert resp_export_pdf.status_code == 200
    assert resp_export_pdf.headers["content-type"] == "application/pdf"

    # Export invalid format -> 422
    resp_export_inv = await client.get(f"/api/v1/audits/{id_audit}/export?format=docx", headers=headers_a)
    assert resp_export_inv.status_code == 422
    assert resp_export_inv.json()["message"] == "Format tidak didukung"

    # Cross-user export -> 404
    resp_export_cross = await client.get(f"/api/v1/audits/{id_audit}/export?format=json", headers=headers_b)
    assert resp_export_cross.status_code == 404
    assert resp_export_cross.json()["message"] == "Data audit tidak ditemukan"

    # 14. Reanalyze
    resp_reanalyze = await client.post(f"/api/v1/audits/{id_audit}/reanalyze", headers=headers_a)
    assert resp_reanalyze.status_code == 202
    assert resp_reanalyze.json()["message"] == "Analisis ulang dimulai"
