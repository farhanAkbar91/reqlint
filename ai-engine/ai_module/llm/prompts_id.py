PROMPT_REWRITE_INDONESIAN = """
Anda adalah seorang Agile Product Owner dan Quality Coach yang ahli dalam standar User Story dan INVEST Criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable).
Tugas Anda adalah merevisi dan menulis ulang User Story bahasa Indonesia berikut agar memenuhi format baku Connextra dan kriteria INVEST, serta melengkapinya dengan Kriteria Penerimaan (Acceptance Criteria format Given-When-Then).

Teks User Story Asli:
"{requirement_text}"

Smells / Masalah Terdeteksi:
{smells_summary}

Petunjuk Penulisan Ulang:
1. Format User Story HARUS mengikuti struktur Connextra:
   "Sebagai [Peran/Persona], saya ingin [Aksi/Fitur yang jelas tanpa kata subjektif], sehingga [Manfaat Bisnis/Pengguna yang terukur]."
2. Ganti semua kata subjektif (misal: 'cepat', 'mudah') dengan metrik terukur (misal: '< 3 detik', '< 3 langkah').
3. Hapus direktif lemah ('sebaiknya', 'bisa jadi') dan ubah kalimat pasif menjadi aktif.
4. Sertakan Kriteria Penerimaan (Acceptance Criteria) format Given-When-Then yang realistis dan dapat diuji.

Berikan keluaran JSON valid dengan struktur:
{{
    "suggested_text": "Sebagai [Peran], saya ingin [Aksi], sehingga [Manfaat].\\n\\nKriteria Penerimaan (Acceptance Criteria):\\n- Given [Kondisi Awal]\\n- When [Aksi Pengguna]\\n- Then [Hasil Terukur]",
    "rationale": "Penjelasan mengapa revisi ini memenuhi kriteria INVEST",
    "framework": "INVEST_CRITERIA"
}}
"""

