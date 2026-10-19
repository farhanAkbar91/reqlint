from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AuditRequest(BaseModel):
    requirement_text: str = Field(
        ...,
        json_schema_extra={"example": "Sebagai pembeli, saya sebaiknya dapat membayar dengan cepat, sehingga transaksi segera selesai."}
    )
    override_language: Optional[str] = Field(
        None,
        description="Optional 'id' or 'en' language override",
        json_schema_extra={"example": "id"}
    )

class AuditResponse(BaseModel):
    requirement_text: str
    detected_language: str
    quality_score: float
    ambiguity_index: float
    completeness_score: float
    verifiability_score: float
    smells: List[Dict[str, Any]]
    revisions: List[Dict[str, Any]]

