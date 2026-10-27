import axios from 'axios';
import { AuditResponse } from '../types/audit';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const checkBackendHealth = async (): Promise<{ ok: boolean; version?: string }> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`, { timeout: 2000 });
    return { ok: response.status === 200, version: '1.0.0' };
  } catch {
    return { ok: false };
  }
};

export const auditRequirement = async (
  requirementText: string,
  overrideLanguage?: string
): Promise<AuditResponse> => {
  const response = await axios.post<AuditResponse>(`${API_BASE_URL}/requirements/audit`, {
    requirement_text: requirementText,
    override_language: overrideLanguage,
  }, { timeout: 5000 });
  return response.data;
};

export interface DocumentUploadResponse {
  id_dokumen: number | null;
  nama_dokumen: string;
  ukuran_dokumen: number;
  jumlah_halaman: number;
  jumlah_karakter: number;
  truncated: boolean;
  teks: string;
}

export const uploadDocumentPdf = async (
  file: File,
  onProgress?: (progress: number) => void
): Promise<DocumentUploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post<{ status: string; message: string; data: DocumentUploadResponse }>(
    `${API_BASE_URL}/documents/upload`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percentCompleted);
        }
      },
    }
  );

  return response.data.data;
};
