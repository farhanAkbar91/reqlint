from typing import List, Dict, Any, Optional

PENALTY_MAP = {
    "AMBIGUITY": 8.0,
    "PASSIVE_VOICE": 6.0,
    "WEAK_DIRECTIVE": 5.0,
    "TIDAK_LENGKAP": 15.0
}

SEVERITY_MULTIPLIER = {
    "LOW": 0.5,
    "MEDIUM": 1.0,
    "HIGH": 1.5
}

class ScoringService:
    @staticmethod
    def calculate_score(
        stories: List[Dict[str, Any]],
        findings: List[Dict[str, Any]],
        invest_results: Optional[Dict[str, bool]] = None
    ) -> Dict[str, Any]:
        """
        Calculates quality score (0..100) and ISO 29148 / INVEST breakdown.
        For multi-story drafts, score is the average of each story's score.
        """
        if not stories:
            return {
                "skor_kualitas": 100.0,
                "breakdown": ScoringService.default_breakdown(stage2_done=False)
            }

        # Calculate penalty per story
        num_stories = max(len(stories), 1)
        story_penalties = {i: 0.0 for i in range(num_stories)}

        for f in findings:
            cat = f.get("kategori_cacat", "")
            base_pen = PENALTY_MAP.get(cat, 5.0)
            sev = f.get("severity", "MEDIUM")
            mult = SEVERITY_MULTIPLIER.get(sev, 1.0)
            s_idx = f.get("story_index", 0)
            if s_idx not in story_penalties:
                story_penalties[s_idx] = 0.0
            story_penalties[s_idx] += (base_pen * mult)

        story_scores = []
        for s_idx, pen in story_penalties.items():
            s_score = max(0.0, min(100.0, 100.0 - pen))
            story_scores.append(s_score)

        avg_score = sum(story_scores) / len(story_scores)

        # Stage 2 penalties (INVEST criteria failed)
        if invest_results:
            failed_invest_count = sum(1 for val in invest_results.values() if val is False or val == 0)
            avg_score = max(0.0, avg_score - (failed_invest_count * 4.0))

        final_score = round(avg_score, 1)

        # Calculate Breakdown
        breakdown = ScoringService.compute_breakdown(findings, invest_results)

        return {
            "skor_kualitas": final_score,
            "breakdown": breakdown
        }

    @staticmethod
    def compute_breakdown(
        findings: List[Dict[str, Any]],
        invest_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        # Count findings per characteristic
        ambiguity_count = sum(1 for f in findings if f.get("kategori_cacat") == "AMBIGUITY")
        tidak_lengkap_count = sum(1 for f in findings if f.get("kategori_cacat") == "TIDAK_LENGKAP")
        directive_count = sum(1 for f in findings if f.get("kategori_cacat") == "WEAK_DIRECTIVE")
        passive_count = sum(1 for f in findings if f.get("kategori_cacat") == "PASSIVE_VOICE")

        unambiguous = max(0, 100 - (ambiguity_count * 25))
        complete = max(0, 100 - (tidak_lengkap_count * 30))
        verifiable = max(0, 100 - (directive_count * 20 + passive_count * 15))
        consistent = 90 if ambiguity_count == 0 else max(40, 90 - (ambiguity_count * 10))
        modifiable = 80
        correct = max(30, 95 - (len(findings) * 8))

        iso_29148 = {
            "unambiguous": unambiguous,
            "complete": complete,
            "consistent": consistent,
            "verifiable": verifiable,
            "modifiable": modifiable,
            "traceable": None if not invest_results else 85,
            "ranked": None,
            "correct": correct
        }

        # INVEST breakdown
        if invest_results:
            invest = {
                "independent": 90 if invest_results.get("independent", True) else 40,
                "negotiable": 80 if invest_results.get("negotiable", True) else 45,
                "valuable": 85 if invest_results.get("valuable", True) else 35,
                "estimable": max(20, 85 - (ambiguity_count * 15)),
                "small": 85 if invest_results.get("small", True) else 30,
                "testable": max(20, verifiable - 10)
            }
        else:
            invest = {
                "independent": 90,
                "negotiable": 80,
                "valuable": 75 if tidak_lengkap_count == 0 else 40,
                "estimable": max(20, 80 - (ambiguity_count * 15)),
                "small": 85,
                "testable": max(20, verifiable - 10)
            }

        return {
            "iso_29148": iso_29148,
            "invest": invest
        }

    @staticmethod
    def default_breakdown(stage2_done: bool = False) -> Dict[str, Any]:
        return {
            "iso_29148": {
                "unambiguous": 100, "complete": 100, "consistent": 100, "verifiable": 100,
                "modifiable": 100, "traceable": 85 if stage2_done else None,
                "ranked": None, "correct": 100
            },
            "invest": {
                "independent": 90, "negotiable": 85, "valuable": 85,
                "estimable": 85, "small": 90, "testable": 90
            }
        }
