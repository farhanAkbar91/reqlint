import re
from typing import Tuple
from ..schemas.audit_models import LanguageCode

class LanguageDetector:
    """
    Bilingual Language Detector for SRS text (Indonesian 'id' vs English 'en').
    Uses keyword heuristics as lightweight fallback and langdetect library when available.
    """
    
    INDONESIAN_MARKERS = {
        "sistem", "harus", "dapat", "pengguna", "dengan", "akan", "sebagai", "saya", 
        "ingin", "sehingga", "diharpkan", "bisa", "fitur", "halaman", "data", "proses"
    }
    
    ENGLISH_MARKERS = {
        "system", "shall", "should", "user", "with", "will", "as", "i", 
        "want", "so", "that", "feature", "page", "data", "process", "allow"
    }

    @classmethod
    def detect(cls, text: str) -> Tuple[LanguageCode, float]:
        if not text or not text.strip():
            return LanguageCode.UNKNOWN, 0.0
            
        # Try langdetect package if installed
        try:
            from langdetect import detect_langs
            results = detect_langs(text)
            for res in results:
                if res.lang in ['id', 'indonesian']:
                    return LanguageCode.INDONESIAN, round(res.prob, 2)
                elif res.lang in ['en', 'english']:
                    return LanguageCode.ENGLISH, round(res.prob, 2)
        except Exception:
            pass # Fallback to deterministic word frequency marker match
            
        words = set(re.findall(r'\b\w+\b', text.lower()))
        id_count = len(words.intersection(cls.INDONESIAN_MARKERS))
        en_count = len(words.intersection(cls.ENGLISH_MARKERS))
        
        if id_count > en_count:
            confidence = round(id_count / (id_count + en_count + 1e-5), 2)
            return LanguageCode.INDONESIAN, confidence
        elif en_count > id_count:
            confidence = round(en_count / (id_count + en_count + 1e-5), 2)
            return LanguageCode.ENGLISH, confidence
        else:
            # Default to English if ambiguous
            return LanguageCode.ENGLISH, 0.50
