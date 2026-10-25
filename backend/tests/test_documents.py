import pytest
from httpx import AsyncClient
import pymupdf as fitz

@pytest.mark.asyncio
async def test_pdf_upload_success(client: AsyncClient):
    email = "doc_user@example.com"
    pwd = "SecretP@ss123"
    await client.post("/api/v1/auth/register", json={
        "name": "Doc User", "email": email, "password": pwd, "password_confirmation": pwd
    })
    login_res = await client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    token = login_res.json()["data"]["access_token"]

    # Create a valid PDF in memory with text
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Sebagai pengguna, saya ingin sistem merespons cepat agar pekerjaan selesai.")
    pdf_bytes = doc.write()
    doc.close()

    files = {"file": ("spesifikasi.pdf", pdf_bytes, "application/pdf")}
    resp = await client.post(
        "/api/v1/documents/upload",
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["message"] == "Dokumen berhasil diekstraksi"
    assert "id_dokumen" in data["data"]
    assert "Sebagai pengguna" in data["data"]["teks"]

@pytest.mark.asyncio
async def test_pdf_upload_invalid_extension(client: AsyncClient):
    login_res = await client.post("/api/v1/auth/login", json={"email": "doc_user@example.com", "password": "SecretP@ss123"})
    token = login_res.json()["data"]["access_token"]

    files = {"file": ("notes.txt", b"Hello text", "text/plain")}
    resp = await client.post(
        "/api/v1/documents/upload",
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 422
    data = resp.json()
    assert data["status"] == "error"
    assert data["message"] == "Format file tidak valid, harap unggah dokumen .pdf"
    assert data["error_code"] == "INVALID_FILE_FORMAT"

@pytest.mark.asyncio
async def test_pdf_upload_corrupt_content(client: AsyncClient):
    login_res = await client.post("/api/v1/auth/login", json={"email": "doc_user@example.com", "password": "SecretP@ss123"})
    token = login_res.json()["data"]["access_token"]

    files = {"file": ("corrupt.pdf", b"not a real pdf content at all", "application/pdf")}
    resp = await client.post(
        "/api/v1/documents/upload",
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 422
    data = resp.json()
    assert data["status"] == "error"
    assert data["message"] == "Format file tidak valid, harap unggah dokumen .pdf"

@pytest.mark.asyncio
async def test_pdf_upload_scanned_empty(client: AsyncClient):
    login_res = await client.post("/api/v1/auth/login", json={"email": "doc_user@example.com", "password": "SecretP@ss123"})
    token = login_res.json()["data"]["access_token"]

    # Empty page with no text
    doc = fitz.open()
    doc.new_page()
    pdf_bytes = doc.write()
    doc.close()

    files = {"file": ("scanned.pdf", pdf_bytes, "application/pdf")}
    resp = await client.post(
        "/api/v1/documents/upload",
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 422
    data = resp.json()
    assert data["status"] == "error"
    assert data["message"] == "PDF tidak memuat lapisan teks (hasil pemindaian), harap unggah dokumen digital"
    assert data["error_code"] == "EMPTY_PDF_TEXT"

@pytest.mark.asyncio
async def test_pdf_upload_exceeds_10mb(client: AsyncClient):
    login_res = await client.post("/api/v1/auth/login", json={"email": "doc_user@example.com", "password": "SecretP@ss123"})
    token = login_res.json()["data"]["access_token"]

    # 10MB + 1KB
    large_bytes = b"%PDF-1.4\n" + b"0" * (10 * 1024 * 1024 + 1024)
    files = {"file": ("huge.pdf", large_bytes, "application/pdf")}
    resp = await client.post(
        "/api/v1/documents/upload",
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 413
    data = resp.json()
    assert data["status"] == "error"
    assert data["message"] == "Ukuran file melebihi batas 10 MB"
    assert data["error_code"] == "FILE_TOO_LARGE"
