from typing import Optional
from pydantic import BaseModel

class DocumentUploadResponse(BaseModel):
    id_dokumen: int
    nama_dokumen: str
    ukuran_dokumen: int
    jumlah_halaman: int
    jumlah_karakter: int
    truncated: bool
    teks: str
