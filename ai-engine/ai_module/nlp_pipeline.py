from typing import Optional
from .detector.language_detector import LanguageDetector
from .rules.indonesian.analyzer import IndonesianAnalyzer
from .rules.english.analyzer import EnglishAnalyzer
from .llm.rewriter import RequirementRewriter
from .schemas.audit_models import AuditReport, LanguageCode

class ReqLintEngine:
    """
    Main Orchestrator Engine for ReqLint.
    Auto-detects language (ID/EN), dispatches to specific NLP analyzer, and triggers LLM rewriting.
    """

    def __init__(self, groq_api_key: Optional[str] = None):
        self.indonesian_analyzer = IndonesianAnalyzer()
        self.english_analyzer = EnglishAnalyzer()
        self.rewriter = RequirementRewriter(api_key=groq_api_key)

    def audit_requirement(self, requirement_text: str, override_language: Optional[str] = None) -> AuditReport:
        # 1. Language Detection
        if override_language and override_language.lower() in ["id", "indonesian"]:
            lang = LanguageCode.INDONESIAN
            confidence = 1.0
        elif override_language and override_language.lower() in ["en", "english"]:
            lang = LanguageCode.ENGLISH
            confidence = 1.0
        else:
            lang, confidence = LanguageDetector.detect(requirement_text)

        # 2. Select Analyzer based on Language
        if lang == LanguageCode.INDONESIAN:
            analyzer = self.indonesian_analyzer
        else:
            analyzer = self.english_analyzer

        # 3. Rule Matching & Smell Detection
        smells = analyzer.analyze_smells(requirement_text)

        # 4. Score Calculation
        scores = analyzer.calculate_scores(smells, requirement_text)

        # 5. Generate Revisions if smells exist
        revisions = []
        if smells:
            revision = self.rewriter.generate_revision(requirement_text, smells, lang)
            if revision:
                revisions.append(revision)

        return AuditReport(
            requirement_text=requirement_text,
            detected_language=lang,
            scores=scores,
            smells=smells,
            revisions=revisions,
            metadata={
                "language_confidence": confidence,
                "total_words": len(requirement_text.split()),
                "total_smells": len(smells)
            }
        )
