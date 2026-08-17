import axios from 'axios';
import { AuditResponse } from '../types/audit';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const auditRequirement = async (
  requirementText: string,
  overrideLanguage?: string
): Promise<AuditResponse> => {
  const response = await axios.post<AuditResponse>(`${API_BASE_URL}/requirements/audit`, {
    requirement_text: requirementText,
    override_language: overrideLanguage,
  });
  return response.data;
};
