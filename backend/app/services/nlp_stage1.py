import os
import re
from typing import List, Dict, Any, Optional
import spacy
from spacy.matcher import PhraseMatcher

from app.services.story_parser import StoryParser

# Global model container loaded during startup lifespan
_nlp_model = None
_phrase_matcher = None
_vague_terms_id = set()
_vague_terms_en = set()
_weak_directives = set()

def load_stage1_resources():
    global _nlp_model, _phrase_matcher, _vague_terms_id, _vague_terms_en, _weak_directives
    if _nlp_model is None:
        try:
            _nlp_model = spacy.load("en_core_web_sm")
        except Exception:
            _nlp_model = spacy.blank("en")

    lexicon_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lexicon"))
    
    id_path = os.path.join(lexicon_dir, "vague_terms_id.txt")
    if os.path.exists(id_path):
        with open(id_path, "r", encoding="utf-8") as f:
            _vague_terms_id = {line.strip().lower() for line in f if line.strip() and not line.startswith("#")}

    en_path = os.path.join(lexicon_dir, "vague_terms_en.txt")
    if os.path.exists(en_path):
        with open(en_path, "r", encoding="utf-8") as f:
            _vague_terms_en = {line.strip().lower() for line in f if line.strip() and not line.startswith("#")}

    weak_path = os.path.join(lexicon_dir, "weak_directives.txt")
    if os.path.exists(weak_path):
        with open(weak_path, "r", encoding="utf-8") as f:
            _weak_directives = {line.strip().lower() for line in f if line.strip() and not line.startswith("#")}

    # Build spaCy PhraseMatcher for English and multi-word terms
    _phrase_matcher = PhraseMatcher(_nlp_model.vocab, attr="LOWER")
    all_ambiguity = list(_vague_terms_en | _vague_terms_id)
    patterns_ambiguity = [_nlp_model.make_doc(t) for t in all_ambiguity if " " in t]
    if patterns_ambiguity:
        _phrase_matcher.add("AMBIGUITY_MULTI", patterns_ambiguity)

    patterns_weak = [_nlp_model.make_doc(t) for t in _weak_directives if " " in t]
    if patterns_weak:
        _phrase_matcher.add("WEAK_MULTI", patterns_weak)

class NLPStage1Service:
    @staticmethod
    def analyze_draft(raw_text: str) -> Dict[str, Any]:
        """
        Executes Stage 1 analysis across all user stories in the draft.
        Returns:
            findings: list of defect dicts
            summary: ringkasan per kategori
            stories: list of parsed stories
        """
        if _nlp_model is None:
            load_stage1_resources()

        stories = StoryParser.split_stories(raw_text)
        all_findings: List[Dict[str, Any]] = []

        for story in stories:
            story_findings = NLPStage1Service._analyze_single_story(story, raw_text)
            all_findings.extend(story_findings)

        # Count summary
        ringkasan = {
            "ambiguity": sum(1 for f in all_findings if f["kategori_cacat"] == "AMBIGUITY"),
            "tidak_lengkap": sum(1 for f in all_findings if f["kategori_cacat"] == "TIDAK_LENGKAP"),
            "weak_directive": sum(1 for f in all_findings if f["kategori_cacat"] == "WEAK_DIRECTIVE"),
            "passive_voice": sum(1 for f in all_findings if f["kategori_cacat"] == "PASSIVE_VOICE"),
            "total": len(all_findings)
        }

        return {
            "stories": stories,
            "findings": all_findings,
            "ringkasan": ringkasan
        }

    @staticmethod
    def _analyze_single_story(story: Dict[str, Any], full_text: str) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []
        text = story["text"]
        start_offset = story["start_offset"]
        story_idx = story["story_index"]

        parsed_struct = StoryParser.parse_structure(text)
        lang = parsed_struct["lang"]

        # 1. Check TIDAK_LENGKAP
        missing_elements = parsed_struct["missing_elements"]
        for missing in missing_elements:
            if missing == "Role":
                saran = "Tambahkan peran pengguna (Role) menggunakan pola 'Sebagai <peran>' / 'As a <role>'."
            elif missing == "Means":
                saran = "Tambahkan kapabilitas/fitur (Means) menggunakan pola 'saya ingin <fitur>' / 'I want <feature>'."
            else:
                saran = "Tambahkan manfaat/tujuan (End) menggunakan pola 'agar/sehingga <tujuan>' / 'so that <benefit>'."

            # Find appropriate highlight portion
            potongan = text[:min(len(text), 40)]
            findings.append({
                "story_index": story_idx,
                "kategori_cacat": "TIDAK_LENGKAP",
                "severity": "HIGH",
                "stage": 1,
                "iso_characteristic": "complete",
                "potongan_teks_asli": potongan,
                "highlight_start": start_offset,
                "highlight_end": start_offset + len(potongan),
                "saran_perbaikan": saran
            })

        # 2. Check AMBIGUITY and WEAK_DIRECTIVE (lexicon regex matching on word boundaries)
        # Combine ID and EN sets
        ambiguity_terms = sorted(list(_vague_terms_id | _vague_terms_en), key=len, reverse=True)
        weak_terms = sorted(list(_weak_directives), key=len, reverse=True)

        found_spans = []  # to avoid overlapping duplicates

        # Check Ambiguity
        for term in ambiguity_terms:
            pattern = re.compile(rf'\b{re.escape(term)}\b', re.IGNORECASE)
            for m in pattern.finditer(text):
                m_start = m.start()
                m_end = m.end()
                if any(s <= m_start < e or s < m_end <= e for s, e in found_spans):
                    continue
                found_spans.append((m_start, m_end))
                matched_text = text[m_start:m_end]

                is_high = term.lower() in {"cepat", "fast", "mudah", "easy", "aman", "safe", "user-friendly", "fleksibel", "flexible"}
                findings.append({
                    "story_index": story_idx,
                    "kategori_cacat": "AMBIGUITY",
                    "severity": "HIGH" if is_high else "MEDIUM",
                    "stage": 1,
                    "iso_characteristic": "unambiguous",
                    "potongan_teks_asli": matched_text,
                    "highlight_start": start_offset + m_start,
                    "highlight_end": start_offset + m_end,
                    "saran_perbaikan": "Ganti dengan metrik terukur, mis. 'merespons dalam 2 detik' atau 'responds within 2 seconds'."
                })

        # Check Weak Directives
        for term in weak_terms:
            pattern = re.compile(rf'\b{re.escape(term)}\b', re.IGNORECASE)
            for m in pattern.finditer(text):
                m_start = m.start()
                m_end = m.end()
                if any(s <= m_start < e or s < m_end <= e for s, e in found_spans):
                    continue
                found_spans.append((m_start, m_end))
                matched_text = text[m_start:m_end]

                findings.append({
                    "story_index": story_idx,
                    "kategori_cacat": "WEAK_DIRECTIVE",
                    "severity": "MEDIUM",
                    "stage": 1,
                    "iso_characteristic": "verifiable",
                    "potongan_teks_asli": matched_text,
                    "highlight_start": start_offset + m_start,
                    "highlight_end": start_offset + m_end,
                    "saran_perbaikan": "Hindari kata direktif lemah; gunakan kata aksi pasti (mis. 'menampilkan', 'memvalidasi', 'display')."
                })

        # 3. Check PASSIVE_VOICE
        # Indonesian: words starting with "di" + verb (e.g. dibayar, diproses, dikirim, diverifikasi)
        id_passive_pattern = re.compile(r'\b(di(?:bayar|proses|kirim|tampilkan|simpan|hapus|buat|lakukan|verifikasi|terima|jalankan|unggah|unduh|atur|akses))\b', re.IGNORECASE)
        for m in id_passive_pattern.finditer(text):
            m_start = m.start()
            m_end = m.end()
            if any(s <= m_start < e or s < m_end <= e for s, e in found_spans):
                continue
            found_spans.append((m_start, m_end))
            matched_text = text[m_start:m_end]
            findings.append({
                "story_index": story_idx,
                "kategori_cacat": "PASSIVE_VOICE",
                "severity": "MEDIUM",
                "stage": 1,
                "iso_characteristic": "verifiable",
                "potongan_teks_asli": matched_text,
                "highlight_start": start_offset + m_start,
                "highlight_end": start_offset + m_end,
                "saran_perbaikan": "Ubah ke kalimat aktif yang menjelaskan secara eksplisit siapa pelaku aksi."
            })

        # English: spaCy nsubjpass / auxpass / passive auxiliary + participle
        if _nlp_model and lang == "en":
            try:
                doc = _nlp_model(text)
                for token in doc:
                    if token.dep_ in ("nsubjpass", "auxpass") or (token.tag_ == "VBN" and token.head.lemma_ in ("be", "get")):
                        m_start = token.idx
                        m_end = token.idx + len(token.text)
                        if any(s <= m_start < e or s < m_end <= e for s, e in found_spans):
                            continue
                        found_spans.append((m_start, m_end))
                        findings.append({
                            "story_index": story_idx,
                            "kategori_cacat": "PASSIVE_VOICE",
                            "severity": "MEDIUM",
                            "stage": 1,
                            "iso_characteristic": "verifiable",
                            "potongan_teks_asli": token.text,
                            "highlight_start": start_offset + m_start,
                            "highlight_end": start_offset + m_end,
                            "saran_perbaikan": "Change to active voice specifying who or what performs the action."
                        })
            except Exception:
                pass

        # Sort findings by highlight_start
        findings.sort(key=lambda x: x["highlight_start"])
        return findings
