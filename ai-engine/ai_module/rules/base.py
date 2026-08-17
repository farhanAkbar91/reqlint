from abc import ABC, abstractmethod
from typing import List
from ..schemas.audit_models import SmellResult, AmbiguityScore

class BaseRequirementAnalyzer(ABC):
    """
    Abstract Base Class for Language-Specific Requirement Analyzers.
    Must be implemented by IndonesianAnalyzer and EnglishAnalyzer.
    """

    @abstractmethod
    def analyze_smells(self, text: str) -> List[SmellResult]:
        """Detect ambiguous words, passive voice, weak directives, and subjective adjectives."""
        pass

    @abstractmethod
    def calculate_scores(self, smells: List[SmellResult], text: str) -> AmbiguityScore:
        """Calculate overall quality, ambiguity index, completeness score, and verifiability score."""
        pass
