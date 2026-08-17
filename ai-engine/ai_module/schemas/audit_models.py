from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class SeverityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class LanguageCode(str, Enum):
    INDONESIAN = "id"
    ENGLISH = "en"
    UNKNOWN = "unknown"

class SmellResult(BaseModel):
    rule_id: str = Field(..., description="ID of the violated rule (e.g. WEAK_DIRECTIVE, PASSIVE_VOICE)")
    category: str = Field(..., description="Category (Ambiguity, Incompleteness, Unverifiable)")
    severity: SeverityLevel
    message: str = Field(..., description="Explanation of why this is a requirement smell")
    target_text: str = Field(..., description="The specific substring flagged")
    start_char: int = Field(..., description="Start character offset")
    end_char: int = Field(..., description="End character offset")

class RevisionSuggestion(BaseModel):
    original_text: str
    suggested_text: str
    rationale: str
    framework: str = Field("IEEE_29148", description="Applied framework, e.g. IEEE 29148 or INVEST")

class AmbiguityScore(BaseModel):
    overall_quality_score: float = Field(..., ge=0.0, le=100.0, description="0 to 100 quality rating")
    ambiguity_index: float = Field(..., ge=0.0, le=1.0, description="0.0 (clean) to 1.0 (highly ambiguous)")
    completeness_score: float = Field(..., ge=0.0, le=100.0)
    verifiability_score: float = Field(..., ge=0.0, le=100.0)

class AuditReport(BaseModel):
    requirement_text: str
    detected_language: LanguageCode
    scores: AmbiguityScore
    smells: List[SmellResult]
    revisions: List[RevisionSuggestion] = []
    metadata: Dict[str, Any] = {}
