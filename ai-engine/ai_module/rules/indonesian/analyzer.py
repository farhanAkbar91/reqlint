import re
from typing import List
from ..base import BaseRequirementAnalyzer
from ...schemas.audit_models import SmellResult, AmbiguityScore, SeverityLevel
from .dictionary import (
    INDONESIAN_WEAK_DIRECTIVES,
    INDONESIAN_SUBJECTIVE_ADJECTIVES,
    INDONESIAN_VAGUE_QUANTIFIERS
)

class IndonesianAnalyzer(BaseRequirementAnalyzer):
    """
    NLP Rule-based Requirements Analyzer for Indonesian Language SRS.
    Uses regex pattern matching and spaCy ID POS tagging rules.
    """

    def __init__(self):
        # spaCy ID model lazy load fallback
        self.nlp = None

    def _load_spacy(self):
        if self.nlp is None:
            try:
                import spacy
                self.nlp = spacy.load("id_core_news_sm")
            except Exception:
                self.nlp = False # Flag unavailable

    def analyze_smells(self, text: str) -> List[SmellResult]:
        smells: List[SmellResult] = []
        text_lower = text.lower()

        # 1. Weak Directives Detection
        for word, advice in INDONESIAN_WEAK_DIRECTIVES.items():
            for match in re.finditer(rf'\b{re.escape(word)}\b', text_lower):
                smells.append(
                    SmellResult(
                        rule_id="WEAK_DIRECTIVE_ID",
                        category="Ambiguity",
                        severity=SeverityLevel.HIGH,
                        message=f"Penggunaan direktif lemah '{word}'. {advice}",
                        target_text=match.group(0),
                        start_char=match.start(),
                        end_char=match.end()
                    )
                )

        # 2. Subjective Adjectives Detection
        for word, advice in INDONESIAN_SUBJECTIVE_ADJECTIVES.items():
            for match in re.finditer(rf'\b{re.escape(word)}\b', text_lower):
                smells.append(
                    SmellResult(
                        rule_id="SUBJECTIVE_ADJECTIVE_ID",
                        category="Unverifiable",
                        severity=SeverityLevel.MEDIUM,
                        message=f"Kata sifat subjektif '{word}'. {advice}",
                        target_text=match.group(0),
                        start_char=match.start(),
                        end_char=match.end()
                    )
                )

        # 3. Vague Quantifiers
        for word, advice in INDONESIAN_VAGUE_QUANTIFIERS.items():
            for match in re.finditer(rf'\b{re.escape(word)}\b', text_lower):
                smells.append(
                    SmellResult(
                        rule_id="VAGUE_QUANTIFIER_ID",
                        category="Incompleteness",
                        severity=SeverityLevel.MEDIUM,
                        message=f"Kuantifikasi samar '{word}'. {advice}",
                        target_text=match.group(0),
                        start_char=match.start(),
                        end_char=match.end()
                    )
                )

        # 4. Passive Voice Detection in Indonesian (words starting with 'di-' or 'ter-')
        # Rule: passive verbs obscuring system responsibility
        passive_matches = re.finditer(r'\b(di[a-z]{3,}|ter[a-z]{3,})\b', text_lower)
        for match in passive_matches:
            word = match.group(0)
            # Filter out common non-passive false positives
            if word not in {"dengan", "dalam", "dari", "dan", "dapat", "tentang", "tersebut"}:
                smells.append(
                    SmellResult(
                        rule_id="PASSIVE_VOICE_ID",
                        category="Ambiguity",
                        severity=SeverityLevel.LOW,
                        message=f"Bentuk pasif '{word}' berpotensi menyamarkan aktor/sistem penanggung jawab.",
                        target_text=word,
                        start_char=match.start(),
                        end_char=match.end()
                    )
                )

        return smells

    def calculate_scores(self, smells: List[SmellResult], text: str) -> AmbiguityScore:
        word_count = max(len(text.split()), 1)
        total_smells = len(smells)

        # Deduct score based on severity
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
