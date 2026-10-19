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
    NLP Rule-based Analyzer for Indonesian Agile User Stories based on INVEST Criteria.
    Evaluates:
    - Connextra format (Sebagai [Peran], Saya ingin [Aksi], Sehingga [Manfaat])
    - INVEST Criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable)
    """

    def __init__(self):
        self.nlp = None

    def _load_spacy(self):
        if self.nlp is None:
            try:
                import spacy
                self.nlp = spacy.load("id_core_news_sm")
            except Exception:
                self.nlp = False

    def analyze_smells(self, text: str) -> List[SmellResult]:
        smells: List[SmellResult] = []
        text_lower = text.lower().strip()

        # --- 1. User Story Connextra Template & INVEST: Valuable Checks ---
        # Check Role component ('Sebagai [peran]...')
        has_role = bool(re.search(r'\bsebagai\b', text_lower))
        if not has_role:
            smells.append(
                SmellResult(
                    rule_id="MISSING_ROLE_ID",
                    category="INVEST: Valuable",
                    severity=SeverityLevel.HIGH,
                    message="User story tidak mencantumkan Persona / Peran pengguna ('Sebagai [Peran]...').",
                    target_text=text[:min(len(text), 30)],
                    start_char=0,
                    end_char=min(len(text), 30)
                )
            )

        # Check Action/Goal component ('saya/kami ingin/butuh...')
        has_action = bool(re.search(r'\b(saya|kami)\s+(ingin|butuh|perlu|menginginkan|membutuhkan)\b', text_lower))
        if not has_action:
            smells.append(
                SmellResult(
                    rule_id="MISSING_ACTION_ID",
                    category="INVEST: Negotiable & Valuable",
                    severity=SeverityLevel.HIGH,
                    message="User story tidak mendefinisikan aksi atau kemampuan yang diinginkan ('...saya ingin [aksi]...').",
                    target_text=text[:min(len(text), 30)],
                    start_char=0,
                    end_char=min(len(text), 30)
                )
            )

        # Check Benefit/Value component ('sehingga/agar/supaya...')
        has_benefit = bool(re.search(r'\b(sehingga|agar|supaya)\b', text_lower))
        if not has_benefit:
            smells.append(
                SmellResult(
                    rule_id="MISSING_BENEFIT_ID",
                    category="INVEST: Valuable",
                    severity=SeverityLevel.HIGH,
                    message="User story tidak memiliki klausa manfaat ('sehingga...', 'agar...', 'supaya...'). Story tanpa 'value' melanggar prinsip INVEST: Valuable.",
                    target_text=text[-min(len(text), 30):],
                    start_char=max(0, len(text) - 30),
                    end_char=len(text)
                )
            )

        # --- 2. INVEST: Small (Compound / Epic Check) ---
        compound_matches = re.finditer(r'\b(dan juga|serta sekaligus|selain itu juga|dan sekaligus)\b', text_lower)
        for match in compound_matches:
            smells.append(
                SmellResult(
                    rule_id="COMPOUND_STORY_ID",
                    category="INVEST: Small",
                    severity=SeverityLevel.MEDIUM,
                    message=f"Ditemukan konjungsi majemuk '{match.group(0)}' yang mengindikasikan User Story terlalu besar / berpotensi menjadi Epic.",
                    target_text=match.group(0),
                    start_char=match.start(),
                    end_char=match.end()
                )
            )

        # --- 3. INVEST: Testable (Weak Directives Detection) ---
        for word, advice in INDONESIAN_WEAK_DIRECTIVES.items():
            for match in re.finditer(rf'\b{re.escape(word)}\b', text_lower):
                smells.append(
                    SmellResult(
                        rule_id="WEAK_DIRECTIVE_ID",
                        category="INVEST: Testable",
                        severity=SeverityLevel.HIGH,
                        message=f"Penggunaan direktif lemah '{word}'. {advice}",
                        target_text=match.group(0),
                        start_char=match.start(),
                        end_char=match.end()
                    )
                )

        # --- 4. INVEST: Estimable & Testable (Subjective Adjectives) ---
        for word, advice in INDONESIAN_SUBJECTIVE_ADJECTIVES.items():
            for match in re.finditer(rf'\b{re.escape(word)}\b', text_lower):
                smells.append(
                    SmellResult(
                        rule_id="SUBJECTIVE_ADJECTIVE_ID",
                        category="INVEST: Estimable & Testable",
                        severity=SeverityLevel.MEDIUM,
                        message=f"Kata sifat subjektif '{word}'. {advice}",
                        target_text=match.group(0),
                        start_char=match.start(),
                        end_char=match.end()
                    )
                )

        # --- 5. INVEST: Estimable (Vague Quantifiers) ---
        for word, advice in INDONESIAN_VAGUE_QUANTIFIERS.items():
            for match in re.finditer(rf'\b{re.escape(word)}\b', text_lower):
                smells.append(
                    SmellResult(
                        rule_id="VAGUE_QUANTIFIER_ID",
                        category="INVEST: Estimable",
                        severity=SeverityLevel.MEDIUM,
                        message=f"Kuantifikasi samar '{word}'. {advice}",
                        target_text=match.group(0),
                        start_char=match.start(),
                        end_char=match.end()
                    )
                )

        # --- 6. INVEST: Testable (Passive Voice Detection) ---
        passive_matches = re.finditer(r'\b(di[a-z]{3,}|ter[a-z]{3,})\b', text_lower)
        for match in passive_matches:
            word = match.group(0)
            if word not in {"dengan", "dalam", "dari", "dan", "dapat", "tentang", "tersebut"}:
                smells.append(
                    SmellResult(
                        rule_id="PASSIVE_VOICE_ID",
                        category="INVEST: Testable",
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

