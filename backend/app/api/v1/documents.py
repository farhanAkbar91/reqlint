from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from typing import Optional
from app.core.database import get_db
from app.core.responses import success_response
from app.api.deps import get_optional_current_user
from app.db.models import User, DokumenUpload
from app.services.pdf_service import PDFService

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", status_code=status.HTTP_200_OK, summary="Upload PDF Document")
async def upload_document(
    file: UploadFile = File(...),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_db)
):
    extracted_data = await PDFService.process_pdf(file)

    doc_id = None
    if current_user:
        # Save to database for authenticated users
        doc_record = DokumenUpload(
            nama_dokumen=extracted_data["nama_dokumen"],
            ukuran_dokumen=extracted_data["ukuran_dokumen"],
            waktu_upload=datetime.now(timezone.utc),
            id_user=current_user.id_user
        )
        db.add(doc_record)
        await db.commit()
        await db.refresh(doc_record)
        doc_id = doc_record.id_dokumen

    response_data = {
        "id_dokumen": doc_id,
        "nama_dokumen": extracted_data["nama_dokumen"],
        "ukuran_dokumen": extracted_data["ukuran_dokumen"],
        "jumlah_halaman": extracted_data["jumlah_halaman"],
        "jumlah_karakter": extracted_data["jumlah_karakter"],
        "truncated": extracted_data["truncated"],
        "teks": extracted_data["teks"]
    }

    return success_response(
        message="Dokumen berhasil diekstraksi",
        data=response_data,
        status_code=status.HTTP_200_OK
    )
