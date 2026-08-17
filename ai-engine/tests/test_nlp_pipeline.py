import pytest
from ai_module.nlp_pipeline import ReqLintEngine
from ai_module.schemas.audit_models import LanguageCode

@pytest.fixture
def engine():
    return ReqLintEngine()

def test_indonesian_weak_directive(engine):
    text = "Sistem sebaiknya dapat mengirim email pemberitahuan."
    report = engine.audit_requirement(text)
    assert report.detected_language == LanguageCode.INDONESIAN
    assert len(report.smells) > 0
    rule_ids = [s.rule_id for s in report.smells]
    assert "WEAK_DIRECTIVE_ID" in rule_ids

def test_english_weak_directive(engine):
    text = "The system should allow users to change passwords."
    report = engine.audit_requirement(text)
    assert report.detected_language == LanguageCode.ENGLISH
    assert len(report.smells) > 0
    rule_ids = [s.rule_id for s in report.smells]
    assert "WEAK_DIRECTIVE_EN" in rule_ids

def test_clean_requirement(engine):
    text = "The system SHALL encrypt passwords using bcrypt hash with salt factor 12."
    report = engine.audit_requirement(text)
    assert report.scores.overall_quality_score > 90.0
