import os
import uuid
import re
import asyncio
from typing import Dict, Any, Tuple
from fastapi import UploadFile, status
import pymupdf as fitz

from app.core.config import settings
from app.core.errors import AppException

class PDFService:
    @staticmethod
    def _is_valid_pdf_magic(content_header: bytes) -> bool:
        # Standard PDF magic header starts with %PDF-
        return content_header.startswith(b"%PDF-") or b"%PDF" in content_header[:1024]

    @staticmethod
    def _sanitize_extracted_text(text: str) -> str:
        # Remove null bytes and non-printable control characters (except newline, tab, carriage return)
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        # Normalize multiple spaces / excessive blank lines
        sanitized = re.sub(r'[ \t]+', ' ', sanitized)
        sanitized = re.sub(r'\n{3,}', '\n\n', sanitized)
        return sanitized.strip()

    @staticmethod
    def _sync_extract(file_path: str) -> Tuple[int, str]:
        doc = fitz.open(file_path)
        num_pages = len(doc)
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()
        full_text = "\n".join(text_parts)
        return num_pages, full_text

    @classmethod
    async def process_pdf(cls, file: UploadFile) -> Dict[str, Any]:
        # 1. Check file extension
        filename = file.filename or ""
        if not filename.lower().endswith(".pdf"):
            raise AppException(
                message="Format file tidak valid, harap unggah dokumen .pdf",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                error_code="INVALID_FILE_FORMAT"
            )

        # Read content
        content = await file.read()
        file_size = len(content)

        # 2. Check size
        max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
        if file_size > max_bytes:
            raise AppException(
                message="Ukuran file melebihi batas 10 MB",
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                error_code="FILE_TOO_LARGE"
            )

        # 3. Check MIME / magic bytes
        if not cls._is_valid_pdf_magic(content):
            raise AppException(
                message="Format file tidak valid, harap unggah dokumen .pdf",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                error_code="INVALID_FILE_FORMAT"
            )

        # 4. Save to temp dir with UUID name
        os.makedirs(settings.TEMP_DIR, exist_ok=True)
        temp_filename = f"{uuid.uuid4().hex}.pdf"
        temp_path = os.path.join(settings.TEMP_DIR, temp_filename)

        try:
            with open(temp_path, "wb") as f:
                f.write(content)

            # 5. Extract text via PyMuPDF in threadpool
            try:
                loop = asyncio.get_running_loop()
                num_pages, raw_text = await loop.run_in_executor(None, cls._sync_extract, temp_path)
            except Exception:
                raise AppException(
                    message="Format file tidak valid, harap unggah dokumen .pdf",
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    error_code="INVALID_FILE_FORMAT"
                )

            # 6. Check scanned / empty text (BR-02)
            cleaned_text = cls._sanitize_extracted_text(raw_text)
            if not cleaned_text:
                raise AppException(
                    message="PDF tidak memuat lapisan teks (hasil pemindaian), harap unggah dokumen digital",
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    error_code="EMPTY_PDF_TEXT"
                )

            # 7. Truncate if exceeds MAX_TEXT_CHARS
            truncated = False
            if len(cleaned_text) > settings.MAX_TEXT_CHARS:
                cleaned_text = cleaned_text[:settings.MAX_TEXT_CHARS]
                truncated = True

            return {
                "nama_dokumen": filename,
                "ukuran_dokumen": file_size,
                "jumlah_halaman": num_pages,
                "jumlah_karakter": len(cleaned_text),
                "truncated": truncated,
                "teks": cleaned_text
            }

        finally:
            # 8. Clean up temporary file immediately (SAFE-3)
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
