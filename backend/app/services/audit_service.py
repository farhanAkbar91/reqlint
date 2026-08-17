import sys
from pathlib import Path

# Add ai-engine directory to sys.path so backend can import ai_module
ai_engine_path = Path(__file__).resolve().parent.parent.parent.parent / "ai-engine"
if str(ai_engine_path) not in sys.path:
    sys.path.insert(0, str(ai_engine_path))

from ai_module.nlp_pipeline import ReqLintEngine
from app.core.config import settings

class AuditService:
    def __init__(self):
        self.engine = ReqLintEngine(groq_api_key=settings.GROQ_API_KEY)

    def analyze(self, text: str, override_language: str = None):
        report = self.engine.audit_requirement(text, override_language=override_language)
        return {
            "requirement_text": report.requirement_text,
            "detected_language": report.detected_language.value,
            "quality_score": report.scores.overall_quality_score,
            "ambiguity_index": report.scores.ambiguity_index,
            "completeness_score": report.scores.completeness_score,
            "verifiability_score": report.scores.verifiability_score,
            "smells": [s.model_dump() for s in report.smells],
            "revisions": [r.model_dump() for r in report.revisions]
        }
