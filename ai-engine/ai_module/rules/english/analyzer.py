import re
from typing import List
from ..base import BaseRequirementAnalyzer
from ...schemas.audit_models import SmellResult, AmbiguityScore, SeverityLevel
from .dictionary import (
    ENGLISH_WEAK_DIRECTIVES,
    ENGLISH_SUBJECTIVE_ADJECTIVES,
    ENGLISH_VAGUE_QUANTIFIERS
)

class EnglishAnalyzer(BaseRequirementAnalyzer):
    """
    NLP Rule-based Requirements Analyzer for English Language SRS.
    Uses regex pattern matching and spaCy EN POS tagging / passive voice rules.
    """

    def __init__(self):
        self.nlp = None

    def _load_spacy(self):
        if self.nlp is None:
            try:
                import spacy
                self.nlp = spacy.load("en_core_web_sm")
            except Exception:
                self.nlp = False

    def analyze_smells(self, text: str) -> List[SmellResult]:
        smells: List[SmellResult] = []
        text_lower = text.lower()

        # 1. Weak Directives Detection
        for word, advice in ENGLISH_WEAK_DIRECTIVES.items():
            for match in re.finditer(rf'\b{re.escape(word)}\b', text_lower):
                smells.append(
                    SmellResult(
                        rule_id="WEAK_DIRECTIVE_EN",
                        category="Ambiguity",
                        severity=SeverityLevel.HIGH,
                        message=f"Weak directive '{word}' detected. {advice}",
                        target_text=match.group(0),
                        start_char=match.start(),
                        end_char=match.end()
                    )
                )

        # 2. Subjective Adjectives Detection
        for word, advice in ENGLISH_SUBJECTIVE_ADJECTIVES.items():
            for match in re.finditer(rf'\b{re.escape(word)}\b', text_lower):
                smells.append(
                    SmellResult(
                        rule_id="SUBJECTIVE_ADJECTIVE_EN",
                        category="Unverifiable",
                        severity=SeverityLevel.MEDIUM,
                        message=f"Subjective adjective '{word}' detected. {advice}",
                        target_text=match.group(0),
                        start_char=match.start(),
                        end_char=match.end()
                    )
                )

        # 3. Vague Quantifiers
        for word, advice in ENGLISH_VAGUE_QUANTIFIERS.items():
            for match in re.finditer(rf'\b{re.escape(word)}\b', text_lower):
                smells.append(
                    SmellResult(
                        rule_id="VAGUE_QUANTIFIER_EN",
                        category="Incompleteness",
                        severity=SeverityLevel.MEDIUM,
                        message=f"Vague quantifier '{word}' detected. {advice}",
                        target_text=match.group(0),
                        start_char=match.start(),
                        end_char=match.end()
                    )
                )

        # 4. Passive Voice Patterns in English (e.g., "is processed", "was created by", "be performed")
        passive_pattern = r'\b(am|is|are|was|were|be|been|being)\s+([a-z]+ed|[a-z]+en)\b'
        for match in re.finditer(passive_pattern, text_lower):
            smells.append(
                SmellResult(
                    rule_id="PASSIVE_VOICE_EN",
                    category="Ambiguity",
                    severity=SeverityLevel.LOW,
                    message=f"Passive voice construct '{match.group(0)}' obscures responsible actor.",
                    target_text=match.group(0),
                    start_char=match.start(),
                    end_char=match.end()
                )
            )

        return smells

    def calculate_scores(self, smells: List[SmellResult], text: str) -> AmbiguityScore:
        word_count = max(len(text.split()), 1)
        total_smells = len(smells)

        penalty = 0.0
        for s in smells:
            if s.severity == SeverityLevel.CRITICAL:
                penalty += 25.0
            elif s.severity == SeverityLevel.HIGH:
                penalty += 15.0
            elif s.severity == SeverityLevel.MEDIUM:
                penalty += 8.0
            elif s.severity == SeverityLevel.LOW:
                penalty += 3.0

        ambiguity_index = min(round(total_smells / (word_count * 0.2 + 1e-5), 2), 1.0)
        overall_quality_score = max(round(100.0 - penalty, 1), 0.0)
        completeness_score = max(round(100.0 - (len([s for s in smells if s.category == "Incompleteness"]) * 15.0), 1), 0.0)
        verifiability_score = max(round(100.0 - (len([s for s in smells if s.category == "Unverifiable"]) * 15.0), 1), 0.0)

        return AmbiguityScore(
            overall_quality_score=overall_quality_score,
            ambiguity_index=ambiguity_index,
            completeness_score=completeness_score,
            verifiability_score=verifiability_score
        )
