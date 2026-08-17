import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from ..core.database import Base

class RequirementAuditHistory(Base):
    __tablename__ = "requirement_audits"

    id = Column(Integer, primary_key=True, index=True)
    requirement_text = Column(Text, nullable=False)
    detected_language = Column(String(10), nullable=False)
    quality_score = Column(Float, nullable=False)
    ambiguity_index = Column(Float, nullable=False)
    smells_json = Column(JSON, nullable=True)
    revisions_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
