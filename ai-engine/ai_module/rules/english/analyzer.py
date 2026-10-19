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
    NLP Rule-based Analyzer for English Agile User Stories based on INVEST Criteria.
    Evaluates:
    - Connextra format (As a [Role], I want [Action], So that [Benefit])
    - INVEST Criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable)
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
        text_lower = text.lower().strip()

        # --- 1. User Story Connextra Template & INVEST: Valuable Checks ---
        # Check Role component ('As a/an [role]...')
        has_role = bool(re.search(r'\bas an?\b', text_lower))
        if not has_role:
            smells.append(
                SmellResult(
                    rule_id="MISSING_ROLE_EN",
                    category="INVEST: Valuable",
                    severity=SeverityLevel.HIGH,
                    message="User story does not identify a user persona or role ('As a [Role]...').",
                    target_text=text[:min(len(text), 30)],
                    start_char=0,
                    end_char=min(len(text), 30)
                )
            )

        # Check Action component ('I/we want/need...')
        has_action = bool(re.search(r'\b(i|we)\s+(want|need|would like)\b', text_lower))
        if not has_action:
            smells.append(
                SmellResult(
                    rule_id="MISSING_ACTION_EN",
                    category="INVEST: Negotiable & Valuable",
                    severity=SeverityLevel.HIGH,
                    message="User story does not declare a desired action or capability ('...I want [Action]...').",
                    target_text=text[:min(len(text), 30)],
                    start_char=0,
                    end_char=min(len(text), 30)
                )
            )

        # Check Benefit/Value component ('so that/in order to...')
        has_benefit = bool(re.search(r'\b(so that|in order to|so)\b', text_lower))
        if not has_benefit:
            smells.append(
                SmellResult(
                    rule_id="MISSING_BENEFIT_EN",
                    category="INVEST: Valuable",
                    severity=SeverityLevel.HIGH,
                    message="User story lacks a business value or rationale clause ('so that...', 'in order to...'). A story without value violates INVEST: Valuable.",
                    target_text=text[-min(len(text), 30):],
                    start_char=max(0, len(text) - 30),
                    end_char=len(text)
                )
            )

        # --- 2. INVEST: Small (Compound / Epic Check) ---
        compound_matches = re.finditer(r'\b(and also|as well as|in addition to)\b', text_lower)
        for match in compound_matches:
            smells.append(
                SmellResult(
                    rule_id="COMPOUND_STORY_EN",
                    category="INVEST: Small",
                    severity=SeverityLevel.MEDIUM,
                    message=f"Compound clause '{match.group(0)}' indicates this story might be an Epic. Consider splitting it into smaller, atomic stories.",
                    target_text=match.group(0),
                    start_char=match.start(),
                    end_char=match.end()
                )
            )

        # --- 3. INVEST: Testable (Weak Directives Detection) ---
        for word, advice in ENGLISH_WEAK_DIRECTIVES.items():
            for match in re.finditer(rf'\b{re.escape(word)}\b', text_lower):
                smells.append(
                    SmellResult(
                        rule_id="WEAK_DIRECTIVE_EN",
                        category="INVEST: Testable",
                        severity=SeverityLevel.HIGH,
                        message=f"Weak directive '{word}' detected. {advice}",
                        target_text=match.group(0),
                        start_char=match.start(),
                        end_char=match.end()
                    )
                )

        # --- 4. INVEST: Estimable & Testable (Subjective Adjectives) ---
        for word, advice in ENGLISH_SUBJECTIVE_ADJECTIVES.items():
            for match in re.finditer(rf'\b{re.escape(word)}\b', text_lower):
                smells.append(
                    SmellResult(
                        rule_id="SUBJECTIVE_ADJECTIVE_EN",
                        category="INVEST: Estimable & Testable",
                        severity=SeverityLevel.MEDIUM,
                        message=f"Subjective adjective '{word}' detected. {advice}",
                        target_text=match.group(0),
                        start_char=match.start(),
                        end_char=match.end()
                    )
                )

        # --- 5. INVEST: Estimable (Vague Quantifiers) ---
        for word, advice in ENGLISH_VAGUE_QUANTIFIERS.items():
            for match in re.finditer(rf'\b{re.escape(word)}\b', text_lower):
                smells.append(
                    SmellResult(
                        rule_id="VAGUE_QUANTIFIER_EN",
                        category="INVEST: Estimable",
                        severity=SeverityLevel.MEDIUM,
                        message=f"Vague quantifier '{word}' detected. {advice}",
                        target_text=match.group(0),
                        start_char=match.start(),
                        end_char=match.end()
                    )
                )

        # --- 6. INVEST: Testable (Passive Voice Detection) ---
        passive_pattern = r'\b(am|is|are|was|were|be|been|being)\s+([a-z]+ed|[a-z]+en)\b'
        for match in re.finditer(passive_pattern, text_lower):
            smells.append(
                SmellResult(
                    rule_id="PASSIVE_VOICE_EN",
                    category="INVEST: Testable",
                    severity=SeverityLevel.LOW,
                    message=f"Passive voice construct '{match.group(0)}' obscures the responsible actor.",
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
        
        # INVEST Completeness (Role, Action, Benefit presence)
        completeness_flaws = [s for s in smells if "Valuable" in s.category or "Negotiable" in s.category]
        completeness_score = max(round(100.0 - (len(completeness_flaws) * 25.0), 1), 0.0)

        # INVEST Testability & Estimability
        testability_flaws = [s for s in smells if "Testable" in s.category or "Estimable" in s.category]
        verifiability_score = max(round(100.0 - (len(testability_flaws) * 15.0), 1), 0.0)

        return AmbiguityScore(
            overall_quality_score=overall_quality_score,
            ambiguity_index=ambiguity_index,
            completeness_score=completeness_score,
            verifiability_score=verifiability_score
        )

