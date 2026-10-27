import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_requirements_audit_indonesian(client: AsyncClient):
    payload = {
        "requirement_text": "Sebagai pembeli, saya sebaiknya dapat membayar transaksi dengan cepat, sehingga pesanan segera diproses.",
        "override_language": "id"
    }
    response = await client.post("/api/v1/requirements/audit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["detected_language"] == "id"
    assert "quality_score" in data
    assert "ambiguity_index" in data
    assert "completeness_score" in data
    assert "verifiability_score" in data
    assert isinstance(data["smells"], list)
    assert len(data["smells"]) > 0
    assert isinstance(data["revisions"], list)

@pytest.mark.asyncio
async def test_requirements_audit_guest_upload_pdf(client: AsyncClient):
    import pymupdf as fitz

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Sebagai analis, saya ingin mengunggah dokumen PDF agar cerita pengguna dapat diekstraksi.")
    pdf_bytes = doc.write()
    doc.close()

    # Guest upload (without Authorization header)
    response = await client.post(
        "/api/v1/documents/upload",
        files={"file": ("guest_sample.pdf", pdf_bytes, "application/pdf")}
    )
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["status"] == "success"
    assert res_json["data"]["nama_dokumen"] == "guest_sample.pdf"
    assert res_json["data"]["id_dokumen"] is None  # Guest mode
