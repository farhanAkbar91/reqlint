# 📊 ReqLint: Laporan Progres Proyek (Minggu ke-1)
## Status Eksekutif: Fondasi Arsitektur, Metodologi INVEST, & Pipeline Data AI

* **Nama Proyek**: ReqLint (Agile User Story Quality Assurance via NLP)
* **Kelompok / Kelas**: Kelompok 3 – PPL Praktikum I4
* **Periode**: Minggu ke-1 (Sprint 1)
* **Peran Penulis Laporan**: Project Manager (PM) & AI / NLP Engineer 1
* **Status Keseluruhan**: ✅ **Fondasi Inti Selesai (On Track & Ahead of Schedule)**

---

## 📌 Ringkasan Eksekutif (Executive Summary)

Pada minggu pertama pelaksanaan proyek, fokus utama dialokasikan pada penetapan arah metodologi yang solid, penyusunan arsitektur sistem modular 4-peran, perumusan standar operasional anotasi yang taat kaidah ilmiah, serta rekayasa pipeline data korpus kebutuhan. 

Meskipun kontribusi rekan tim lain (Backend, Frontend-QA, dan AI Engineer 2) belum dimulai karena masih pada fase transisi awal iterasi, **seluruh fondasi inti arsitektur, dokumentasi metodologis, *engine rule-based* NLP dwibahasa, dan dataset korpus 1.000 User Story telah berhasil dibangun dan diuji 100%**. Fondasi ini siap digunakan oleh seluruh anggota tim saat mereka mulai aktif di modul masing-masing.

---

## 🏆 Rincian Kontribusi & Pencapaian Kerja

### 1. Peran: Project Manager (PM) & System Architect

Sebagai PM dan Arsitek Sistem, tanggung jawab difokuskan pada manajemen cakupan proyek (*scope management*), metodologi penjaminan mutu kebutuhan, dan arsitektur kerja terisolasi:

1. **Penyelarasan & Penajaman Ruang Lingkup (Scope Alignment)**:
   * Menggeser dan menyederhanakan fokus proyek dari format SRS kaku tradisional (ISO/IEC/IEEE 29148) menjadi **khusus dan penuh pada Agile User Stories** dengan standar format **Connextra** (*Role - Action - Benefit*) dan kriteria **INVEST** (*Independent, Negotiable, Valuable, Estimable, Small, Testable*).
   * Memastikan bahwa seluruh dokumentasi rubrik, aturan evaluasi, dan model hanya berfokus pada *User Story*.
2. **Penyusunan Pedoman Anotasi Ilmiah & Metodologi (v0.9)**:
   * Menyusun dokumen standar operasional [pedoman_anotasi_invest.md](file:///d:/portfolio/AI/reqlint/pm-docs/rubrics/pedoman_anotasi_invest.md) yang menetapkan format label biner 6-dimensi $[y_I, y_N, y_V, y_E, y_S, y_T] \in \{0, 1\}^6$ beserta opsi *"RAGU"*.
   * Menegakkan **integritas akademik**: menghapus klaim data fiktif dan menetapkan protokol anotasi riil (*blind annotation*) serta rekonsiliasi konsensus.
   * Merumuskan pemisahan kriteria operasional yang tegas dan ortogonal:
     * Kata sifat subjektif/kualitatif (*"cepat"*, *"mudah"*) dikhususkan pada kriteria **Testable (T)**.
     * Kuantitas samar (*"beberapa"*, *"banyak"*, *"dll"*) dikhususkan pada kriteria **Estimable (E)**.
     * Ketergantungan tiket eksternal dikhususkan pada kriteria **Independent (I)**.
   * Menetapkan prinsip bahwa nilai kesepakatan manusia (**Cohen's Kappa & PABAK**) menjadi batas atas realistis (*human agreement upper bound*) bagi performa model.
3. **Penyelarasan Rubrik Formal Proyek**:
   * Memperbarui [invest_criteria.json](file:///d:/portfolio/AI/reqlint/pm-docs/rubrics/invest_criteria.json) agar 100% selaras dengan pedoman operasional teks.
4. **Desain Arsitektur Sistem & Isolasi Workspace**:
   * Merancang arsitektur modular yang membagi repositori ke dalam 4 *workspace* terisolasi ([pm-docs/](file:///d:/portfolio/AI/reqlint/pm-docs/), [ai-engine/](file:///d:/portfolio/AI/reqlint/ai-engine/), [backend/](file:///d:/portfolio/AI/reqlint/backend/), [frontend-qa/](file:///d:/portfolio/AI/reqlint/frontend-qa/)).
   * Menyiapkan panduan kolaborasi tim ([CONTRIBUTING.md](file:///d:/portfolio/AI/reqlint/CONTRIBUTING.md)) lengkap dengan *Git Branching Strategy* (`pm/*`, `ai/*`, `backend/*`, `frontend/*) dan standar *Conventional Commits*.
   * Mengonfigurasi orkestrasi lingkungan pengembangan multi-kontainer menggunakan [docker-compose.yml](file:///d:/portfolio/AI/reqlint/docker-compose.yml) (Next.js, FastAPI, PostgreSQL, Redis).
5. **Penyiapan Lembar Kerja Anotasi Tim**:
   * Membuat lembar kerja siap pakai [lembar_anotasi_kosong.csv](file:///d:/portfolio/AI/reqlint/ai-engine/benchmarks/lembar_anotasi_kosong.csv) untuk memfasilitasi pelabelan independen anggota tim saat sesi anotasi resmi dimulai.

---

### 2. Peran: AI / NLP Engineer 1

Sebagai salah satu dari 2 AI Engineer, tanggung jawab difokuskan pada rekayasa pipeline pemrosesan bahasa alami (NLP), pembuatan korpus data, dan mesin perturbasi terkontrol:

1. **Pipeline Analisis NLP Dwibahasa (ID & EN)**:
   * Mengembangkan orchestrator [nlp_pipeline.py](file:///d:/portfolio/AI/reqlint/ai-engine/ai_module/nlp_pipeline.py) yang secara otomatis mendeteksi bahasa teks (*Indonesian* vs *English*).
   * Membangun aturan deteksi kecacatan (*smell matchers*) berbasis pola regex dan POS tagging pada [IndonesianAnalyzer](file:///d:/portfolio/AI/reqlint/ai-engine/ai_module/rules/indonesian/analyzer.py) dan [EnglishAnalyzer](file:///d:/portfolio/AI/reqlint/ai-engine/ai_module/rules/english/analyzer.py):
     * `MISSING_ROLE`: Memeriksa ketiadaan klausul persona pengguna (*"Sebagai..."* / *"As a..."*).
     * `MISSING_ACTION`: Memeriksa ketiadaan deklarasi aksi (*"saya ingin..."* / *"I want..."*).
     * `MISSING_BENEFIT`: Memeriksa ketiadaan klausul manfaat (*"sehingga..."* / *"so that..."*).
     * `COMPOUND_STORY`: Mendeteksi konjungsi majemuk (*"dan juga"*, *"serta sekaligus"*, *"and also"*, *"as well as"*) yang mengindikasikan cerita terlalu besar (*Epic*).
     * `WEAK_DIRECTIVE`: Menandai kata direktif lemah (*"sebaiknya"*, *"bisa"*, *"should"*).
     * `SUBJECTIVE_ADJECTIVE`: Menandai kata sifat kualitatif tak terukur (*"cepat"*, *"mudah"*, *"user-friendly"*).
     * `VAGUE_QUANTIFIER`: Menandai kuantifikasi kabur (*"beberapa"*, *"banyak"*, *"etc"*).
     * `PASSIVE_VOICE`: Menandai kalimat pasif awalan *di-* / *ter-* atau *is by* yang mengaburkan subjek penanggung jawab.
2. **Mesin Perturbasi Terkontrol (*Controlled Perturbation Engine*)**:
   * Membangun modul [perturbation_engine.py](file:///d:/portfolio/AI/reqlint/ai-engine/data_pipeline/perturbation_engine.py) untuk memecahkan masalah kelangkaan contoh negatif (*story buruk*) pada dataset publik.
   * Mampu menginjeksi kecacatan tunggal yang ortogonal secara deterministik untuk kriteria I, N, V, E, S, dan T dengan label biner *ground truth* yang valid.
3. **Penyusunan Korpus 1.000 User Stories**:
   * Menyusun generator otomatis [build_invest_corpus.py](file:///d:/portfolio/AI/reqlint/ai-engine/data_pipeline/build_invest_corpus.py).
   * Mengintegrasikan benih alami publik dari **Dalpiaz et al.** (22 domain: OpenGov, FAA Aviation, IoT Smart Home, CMS, Healthcare, E-Commerce, Logistics, Finance) di [seeds_dalpiaz_en.py](file:///d:/portfolio/AI/reqlint/ai-engine/data_pipeline/seeds_dalpiaz_en.py).
   * Mengintegrasikan benih alami dari proyek kuliah dan PPL (SIAKAD/KRS, Perpustakaan, Kasir POS, Logistik Kargo, HRIS, Klinik) di [seeds_ppl_id.py](file:///d:/portfolio/AI/reqlint/ai-engine/data_pipeline/seeds_ppl_id.py).
   * **Menegakkan Aturan Emas Evaluasi (*Test Set Isolation*)**:
     * **Train Set (750 stories)**: Natural + Perturbed + Synthetic.
     * **Validation Set (100 stories)**: **100% Natural Stories**.
     * **Test Set (150 stories)**: **100% Natural Stories** (*zero synthetic & zero perturbed*).
   * Menghasilkan berkas master [invest_corpus_1000.csv](file:///d:/portfolio/AI/reqlint/ai-engine/data/invest_corpus_1000.csv) dan [invest_corpus_1000.json](file:///d:/portfolio/AI/reqlint/ai-engine/data/invest_corpus_1000.json).
4. **Metrik Reliabilitas Antar-Penilai (Inter-Rater Reliability)**:
   * Membangun skrip [invest_annotation_experiment.py](file:///d:/portfolio/AI/reqlint/ai-engine/benchmarks/invest_annotation_experiment.py) yang menghitung **Cohen's Kappa ($\kappa$)**, **PABAK**, persentase observed agreement ($P_o$), dan expected agreement ($P_e$) langsung dari berkas CSV.
5. **Pengujian Kualitas & Otomasi Tes**:
   * Menulis pengujian unit otomatis di [test_nlp_pipeline.py](file:///d:/portfolio/AI/reqlint/ai-engine/tests/test_nlp_pipeline.py) yang menguji format Connextra, deteksi kelemahan INVEST, dan lolos uji **100% (5/5 passed)**.

---

### 3. Kontribusi Lintas Modul (Inisiasi Backend & Frontend Starter)

Untuk mempermudah rekan tim Backend Engineer dan Frontend-QA saat mulai bekerja, telah disiapkan fondasi integrasi:
* **Backend API Starter**:
  * Menyelaraskan skema Pydantic v2 di [requirement_schema.py](file:///d:/portfolio/AI/reqlint/backend/app/schemas/requirement_schema.py) ke format User Story.
  * Mengintegrasikan endpoint audit di [requirements.py](file:///d:/portfolio/AI/reqlint/backend/app/api/v1/endpoints/requirements.py) langsung ke `ReqLintEngine`.
  * Memperbarui pengujian unit API di [test_api.py](file:///d:/portfolio/AI/reqlint/backend/tests/test_api.py) dengan kelulusan **100% (3/3 passed)**.
* **Frontend UI Starter**:
  * Mengadaptasi antarmuka [RequirementEditor.tsx](file:///d:/portfolio/AI/reqlint/frontend-qa/src/components/editor/RequirementEditor.tsx) menjadi *Agile User Story Editor* dilengkapi tombol template cepat (`🇮🇩 Format ID` dan `🇬🇧 Format EN`).
  * Memperbarui visualisasi kartu skor kualitas [AuditScorecard.tsx](file:///d:/portfolio/AI/reqlint/frontend-qa/src/components/analysis/AuditScorecard.tsx) dan daftar temuan [SmellList.tsx](file:///d:/portfolio/AI/reqlint/frontend-qa/src/components/analysis/SmellList.tsx).
  * Memperbarui skenario pengujian E2E Cypress di [editor-audit.spec.ts](file:///d:/portfolio/AI/reqlint/frontend-qa/tests-e2e/e2e/editor-audit.spec.ts).

---

## 📈 Rekapitulasi Metrik & Artefak Minggu ke-1

| Indikator Capaian | Target Minggu 1 | Realisasi Minggu 1 | Status |
|---|:---:|:---:|:---:|
| **Dokumentasi Metodologi INVEST** | Draf Awal | Dokumen SOP Lengkap v0.9 ([pedoman_anotasi_invest.md](file:///d:/portfolio/AI/reqlint/pm-docs/rubrics/pedoman_anotasi_invest.md)) | ✅ Tercapai |
| **Penyelarasan Rubrik Kriteria** | Ada | JSON Rubrik Formal ([invest_criteria.json](file:///d:/portfolio/AI/reqlint/pm-docs/rubrics/invest_criteria.json)) | ✅ Tercapai |
| **Pipeline Data & Korpus** | Rencana Pengumpulan | 1.000 User Stories (500 ID / 500 EN) ([invest_corpus_1000.csv](file:///d:/portfolio/AI/reqlint/ai-engine/data/invest_corpus_1000.csv)) | 🚀 Melampaui Target |
| **Isolasi Test Set** | Terdefinisi | 100% Natural Stories (0% Perturbasi/Sintetis pada Test) | ✅ Valid |
| **Engine Perturbasi Terkontrol** | Konseptual | Modul Kode Operasional ([perturbation_engine.py](file:///d:/portfolio/AI/reqlint/ai-engine/data_pipeline/perturbation_engine.py)) | ✅ Tercapai |
| **Engine NLP Dwibahasa** | Prototipe Kasar | *Rule Matchers* Connextra & INVEST ID/EN Operasional | ✅ Tercapai |
| **Pengujian Unit Otomatis** | Berjalan | 8/8 Tests Passing (5 AI Engine, 3 Backend API) | ✅ 100% Hijau |

---

## 🗺️ Rencana Kerja Iterasi Berikutnya (Roadmap Minggu ke-2)

Ketika rekan tim mulai aktif di minggu depan, rencana pembagian tugas berikutnya adalah:
1. **Untuk Anggota Tim Lain (Kolaborator)**:
   * **AI Engineer 2**: Melakukan sesi pelabelan mandiri pada [lembar_anotasi_kosong.csv](file:///d:/portfolio/AI/reqlint/ai-engine/benchmarks/lembar_anotasi_kosong.csv) untuk menguji kesepakatan penilai riil (*Inter-Rater Reliability*) dengan skrip [invest_annotation_experiment.py](file:///d:/portfolio/AI/reqlint/ai-engine/benchmarks/invest_annotation_experiment.py), serta mulai mengintegrasikan Stanza untuk *dependency parsing* bahasa Indonesia.
   * **Backend Engineer**: Menyempurnakan penyimpanan riwayat audit ke database relasional PostgreSQL menggunakan SQLAlchemy ORM dan antrean tugas Celery/Redis.
   * **Frontend + QA Engineer**: Mempercantik tampilan UI visual diff, menambahkan fitur ekspor laporan audit ke PDF/JSON, serta menjalankan Cypress E2E test suite.
2. **Untuk Penulis (PM & AI Engineer 1)**:
   * Mengawasi rapat rekonsiliasi hasil anotasi mandiri dan mendokumentasikan nilai Cohen's Kappa & PABAK riil.
   * Mempersiapkan arsitektur ekstraksi fitur *white-box* (Lapisan 1 dan Lapisan 2) menggunakan Stanza sebelum masuk ke pengujian model machine learning *interpretable*.
