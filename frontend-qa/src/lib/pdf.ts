import { uploadDocumentPdf } from './api';

/** Ekstrak teks dari PDF menggunakan backend FastAPI ReqLint (/api/v1/documents/upload) */
export async function extractPdfText(file: File): Promise<string> {
  try {
    const res = await uploadDocumentPdf(file);
    if (res && res.teks) {
      return res.teks;
    }
    throw new Error('Tidak ada teks yang dapat diekstrak dari berkas PDF.');
  } catch (err: any) {
    const msg = err.response?.data?.message || err.message || 'Gagal mengekstrak teks PDF melalui backend';
    throw new Error(msg);
  }
}

export async function readTextFile(file: File): Promise<string> {
  const isPdf = file.type === 'application/pdf' || /\.pdf$/i.test(file.name);
  return isPdf ? extractPdfText(file) : file.text();
}
