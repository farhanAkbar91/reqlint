from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AuditRequest(BaseModel):
    requirement_text: str = Field(..., example="Sistem sebaiknya dapat memproses pembayaran dengan cepat.")
    override_language: Optional[str] = Field(None, example="id", description="Optional 'id' or 'en' language override")

class AuditResponse(BaseModel):
    requirement_text: str
    detected_language: str
    quality_score: float
    ambiguity_index: float
    completeness_score: float
    verifiability_score: float
    smells: List[Dict[str, Any]]
    revisions: List[Dict[str, Any]]
