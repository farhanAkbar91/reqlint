from fastapi import APIRouter, HTTPException
from app.schemas.requirement_schema import AuditRequest, AuditResponse
from app.services.audit_service import AuditService

router = APIRouter()
audit_service = AuditService()

@router.post("/audit", response_model=AuditResponse)
def audit_requirement(payload: AuditRequest):
    """
    Analyzes an Agile User Story text for INVEST criteria compliance, completeness, and ambiguity.
    Supports both Indonesian and English text.
    """

    if not payload.requirement_text or not payload.requirement_text.strip():
        raise HTTPException(status_code=400, detail="requirement_text must not be empty.")

    result = audit_service.analyze(
        text=payload.requirement_text,
        override_language=payload.override_language
    )
    return result
