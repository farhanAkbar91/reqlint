import pytest
from ai_module.nlp_pipeline import ReqLintEngine
from ai_module.schemas.audit_models import LanguageCode

@pytest.fixture
def engine():
    return ReqLintEngine()

def test_indonesian_user_story_missing_benefit(engine):
    # Missing 'sehingga / agar' clause
    text = "Sebagai pembeli, saya sebaiknya dapat membayar pesanan dengan cepat."
    report = engine.audit_requirement(text)
    assert report.detected_language == LanguageCode.INDONESIAN
    assert len(report.smells) > 0
    rule_ids = [s.rule_id for s in report.smells]
    assert "MISSING_BENEFIT_ID" in rule_ids
    assert "WEAK_DIRECTIVE_ID" in rule_ids
    assert "SUBJECTIVE_ADJECTIVE_ID" in rule_ids

def test_indonesian_clean_user_story(engine):
    text = "Sebagai pelanggan, saya ingin menerima bukti pembayaran digital melalui email, sehingga saya memiliki riwayat pengeluaran yang terverifikasi."
    report = engine.audit_requirement(text)
    assert report.detected_language == LanguageCode.INDONESIAN
    assert report.scores.overall_quality_score >= 90.0

def test_english_user_story_flaws(engine):
    # Missing 'so that' and has 'should' and 'easily'
    text = "As a buyer, I should be able to checkout easily."
    report = engine.audit_requirement(text)
    assert report.detected_language == LanguageCode.ENGLISH
    assert len(report.smells) > 0
    rule_ids = [s.rule_id for s in report.smells]
    assert "MISSING_BENEFIT_EN" in rule_ids
    assert "WEAK_DIRECTIVE_EN" in rule_ids
    assert "SUBJECTIVE_ADJECTIVE_EN" in rule_ids

def test_english_clean_user_story(engine):
    text = "As a customer, I want to download monthly transaction invoices in PDF format, so that I can submit expense reports to my accounting department."
    report = engine.audit_requirement(text)
    assert report.detected_language == LanguageCode.ENGLISH
    assert report.scores.overall_quality_score >= 90.0

def test_compound_user_story_epic(engine):
    text = "Sebagai admin, saya ingin melihat statistik penjualan dan juga mengelola hak akses staf, sehingga operasional toko berjalan lancar."
    report = engine.audit_requirement(text)
    rule_ids = [s.rule_id for s in report.smells]
    assert "COMPOUND_STORY_ID" in rule_ids

