# ReqLint — Panduan Integrasi Backend (Frontend & Tim AI/NLP)

Dokumen ini adalah panduan integrasi teknis hasil implementasi **ReqLint Backend Spec (SRS v1.0)**. Semua endpoint, skema envelope, pipeline 2-tahap, dan pengujian otomatis (19 test cases) telah selesai dan berstatus **PASSING**.

---

## 1. Status Kesiapan Push ke GitHub

Backend sudah **100% siap di-commit dan di-push ke GitHub**.
- Tidak ada file secret, token JWT keras, atau database lokal `.db` yang tersisa (sudah dilindungi `.gitignore`).
- Dependensi sudah dicatat rapi di [`requirements.txt`](file:///d:/portfolio/AI/reqlint/backend/requirements.txt).
- Skema database dan migrasi Alembic sudah sinkron.
- Semua 19 skenario pengujian Gherkin SRS lulus uji (`pytest` 100% passing).

### Rekomendasi Perintah Git untuk Push:
```bash
git add backend/ .gitignore
git commit -m "feat(backend): implement complete ReqLint API spec v1.0 (auth, 2-stage nlp, audits, export)"
git push origin feat/week1-invest-pipeline-and-report
```

---

## 2. Panduan Integrasi untuk Tim Frontend (Web UI)

### 2.1 Konfigurasi & Autentikasi
- **Base URL:** `http://localhost:8000/api/v1`
- **Header Autentikasi:** `Authorization: Bearer <access_token>` untuk semua endpoint terproteksi.
- **Isolasi Data (SEC-4):** Jika user mencoba mengakses data audit milik user lain, backend akan membalas status **`404 Not Found`** (`"Data audit tidak ditemukan"`), bukan `403`.

### 2.2 Format Envelope Standar

#### A. Envelope Sukses
```json
{
  "status": "success",
  "message": "Pesan deskriptif",
  "data": { ... }
}
```

#### B. Envelope Error
```json
{
  "status": "error",
  "message": "Pesan error untuk user",
  "error_code": "KODE_ERROR",
  "errors": [
    { "field": "nama_field", "message": "Detail kegagalan" }
  ]
}
```

### 2.3 Pesan String Baku (Gherkin SRS Compliance)
Gunakan string berikut untuk validasi toast / notifikasi di UI karena diuji persis oleh automated acceptance tests:
- Register sukses: `"Pendaftaran berhasil, silakan masuk"` (201)
- Email duplikat: `"Email sudah terdaftar"` (409)
- Sandi tidak cocok/valid: `"Format sandi tidak valid atau konfirmasi sandi tidak cocok"` (422)
- Login gagal: `"Kredensial tidak valid"` (401)
- Draf kosong: `"Draf kebutuhan tidak boleh kosong"` (422)
- PDF bukan dokumen valid/korup: `"Format file tidak valid, harap unggah dokumen .pdf"` (422)
- PDF hasil scan (tanpa teks digital): `"PDF tidak memuat lapisan teks (hasil pemindaian), harap unggah dokumen digital"` (422)
- File melebihi batas: `"Ukuran file melebihi batas 10 MB"` (413)
- Upload sukses: `"Dokumen berhasil diekstraksi"` (200)
- 1-Click Apply / Manual Edit sukses: `"Draf berhasil diperbarui"` (200)
- Label skor terkini setelah revisi: `"Skor Kualitas Terkini"`
- Riwayat kosong: `"Belum ada riwayat audit yang tersedia"` (200, `has_any_history: false`)
- Pencarian riwayat nihil: `"Tidak ada riwayat yang cocok dengan pencarian"` (200, `has_any_history: true`)

---

### 2.4 Alur Interaksi UI & Peta Endpoint

```
[Register / Login] ──► Token JWT
                            │
        ┌───────────────────┴───────────────────┐
  Input Teks Manual                       Upload PDF (POST /documents/upload)
        │                                       │
        └───────────────────┬───────────────────┘
                            ▼
              Mulai Audit: POST /audits
              (Dapat 202 Accepted, id_audit, poll_url)
                            │
                            ▼
             Polling: GET /audits/{id_audit}/status
             (Tiap ~1 detik sampai status != "PROCESSING")
                            │
                            ▼
               Detail: GET /audits/{id_audit}
              (Scorecard, Temuan, Diff, Gherkin AC)
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
  1-Click Apply        Edit Manual         Export Laporan
(POST /apply)        (PUT /revision)     (GET /export?format=pdf|md|json)
```

#### Detail Request Tiap Fitur:

1. **Upload Dokumen PDF (`POST /documents/upload`)**
   - Header: `Content-Type: multipart/form-data`
   - Form Data: `file: <binary .pdf>`
   - Response Data: `{ "id_dokumen": 12, "nama_dokumen": "spec.pdf", "teks": "Sebagai...", "truncated": false }`
   - *Aksi Frontend:* Isi editor Monaco dengan `data.teks`, dan simpan `data.id_dokumen`.

2. **Inline Linting Real-time Monaco (`POST /lint`)**
   - Panggil saat user mengetik di editor dengan **debounce 300–500 ms**.
   - Body: `{"konten": "Sebagai pengguna, saya ingin..."}`
   - Tidak menyimpan ke DB (stateless Stage 1, <50ms).
   - Response Data: `{ "skor_perkiraan": 75.0, "ringkasan": {...}, "temuan": [{"kategori_cacat": "AMBIGUITY", "highlight_start": 32, "highlight_end": 37, ...}] }`

3. **Kirim Audit (`POST /audits`)**
   - Body:
     ```json
     {
       "konten": "Sebagai pembeli, saya ingin...",
       "judul_klausul": "Judul Klausul (Opsional)",
       "tipe_masukan": "manual",  // atau "pdf"
       "id_dokumen": null         // isi id_dokumen jika tipe_masukan="pdf"
     }
     ```
   - Respon **202 Accepted**:
     ```json
     {
       "status": "success",
       "message": "Draf diterima dan sedang dianalisis",
       "data": { "id_audit": 101, "poll_url": "/api/v1/audits/101/status" }
     }
     ```

4. **Polling Status (`GET /audits/{id_audit}/status`)**
   - Polling tiap ~1 detik sampai `status_audit != "PROCESSING"`.
   - Field `stage1_ready`: jika `true`, frontend boleh menampilkan preview hasil Stage 1 lebih awal sebelum Stage 2 selesai.

5. **Hasil Lengkap Audit (`GET /audits/{id_audit}`)**
   - Menyediakan objek lengkap:
     - `scorecard`: `skor_awal`, `skor_kualitas`, dan `breakdown` (8 karakteristik ISO 29148 & 6 kriteria INVEST).
     - `ringkasan`: ringkasan jumlah cacat per kategori (`ambiguity`, `tidak_lengkap`, `weak_directive`, `passive_voice`, `total`).
     - `temuan`: daftar cacat lengkap dengan offset karakter `highlight_start` & `highlight_end` untuk highlighting di editor.
     - `rekomendasi_ai`: `ai_rewrite` dan array `acceptance_criteria` format Gherkin (`given`, `when`, `then`).
     - `diff`: komparasi `original` (teks & skor) vs `revised` (teks & skor).
     - `notifikasi`: jika `status_audit == "PARTIAL"` (SAFE-2 fallback), objek notifikasi berisi `{ "tipe": "warning", "message": "Gagal memuat rekomendasi AI, silakan klik tombol Analisis Ulang", "aksi": "reanalyze" }`.

6. **1-Click Apply AI Recommendation (`POST /audits/{id_audit}/apply`)**
   - Body: `{"terapkan": ["rewrite", "acceptance_criteria"]}` (bisa salah satu atau keduanya).
   - Menghitung ulang skor kualitas secara sinkron (<50ms).
   - Respon memuat data terupdate dan label `"Skor Kualitas Terkini"`.

7. **Revisi Manual (`PUT /audits/{id_audit}/revision`)**
   - Body: `{"konten_revisi": "Teks hasil edit user..."}`.
   - Rescore sinkron dan atomic update.

8. **Export Unduhan (`GET /audits/{id_audit}/export?format=pdf|md|json`)**
   - Karena memerlukan header `Authorization: Bearer <token>`, unduh melalui `fetch()` -> `blob` -> `URL.createObjectURL(blob)`.

---

## 3. Panduan Integrasi untuk Tim AI / NLP Engine

Backend ReqLint mengadopsi arsitektur **Hybrid 2-Stage Analysis** yang memadukan kecepatan & transparansi rule-based NLP (Stage 1) dengan kecerdasan generatif SLM (Stage 2).

### 3.1 Arsitektur Pipeline 2-Stage

```
                      User Story Draft
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: Deterministic / White-box NLP (< 50 ms)            │
│  - StoryParser: Deteksi multi-story + Role/Means/End        │
│  - Matcher & Leksikon: Ambiguity & Weak Directive           │
│  - Syntactic / POS Parsing: Deteksi Passive Voice           │
│  - Preliminary Scoring & Initial Breakdown                  │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 2: Generative SLM Inference (Target ≤ 4 detik)        │
│  - Anti-Prompt Injection Enclosure: <user_story>...</>      │
│  - Structured Output via Pydantic JSON                      │
│  - Generasi AI Rewrite (Measurable SLA)                     │
│  - Generasi Acceptance Criteria (Gherkin BDD)               │
│  - INVEST Criteria Evaluation & Final Rescore               │
│  - SAFE-2 Fallback Handlers (PARTIAL mode)                  │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Stage 1 (Deterministic NLP)
- **File Implementasi:** [`app/services/nlp_stage1.py`](file:///d:/portfolio/AI/reqlint/backend/app/services/nlp_stage1.py), [`app/services/story_parser.py`](file:///d:/portfolio/AI/reqlint/backend/app/services/story_parser.py), [`app/services/scoring.py`](file:///d:/portfolio/AI/reqlint/backend/app/services/scoring.py).
- **Leksikon Kamus:**
  - `app/lexicon/vague_terms_id.txt`: kata ambigu Bahasa Indonesia (*cepat, lambat, mudah, aman, ramah pengguna, dll*).
  - `app/lexicon/vague_terms_en.txt`: kata ambigu Bahasa Inggris (*fast, easily, user-friendly, robust, flexible, dll*).
  - `app/lexicon/weak_directives.txt`: kata direktif lemah dwibahasa (*bisa, sebaiknya, mungkin, can, should ideally, dll*).
- **Menambahkan Leksikon Baru:** Tim AI cukup menambahkan entri kata baru di file `.txt` di atas (satu frasa per baris). Server akan otomatis memuat saat startup.
- **Kategori Cacat (4 Kategori Baku):**
  1. `AMBIGUITY`: Kata sifat/keterangan subjektif dan tidak terukur.
  2. `WEAK_DIRECTIVE`: Kata modalitas yang mengurangi ketegasan requirement.
  3. `PASSIVE_VOICE`: Kalimat pasif yang menyembunyikan pelaku aksi (prefiks `di-` atau konstruksi pasif EN).
  4. `TIDAK_LENGKAP`: Pola User Story kehilangan salah satu komponen (Role / Means / End).

### 3.3 Stage 2 (SLM Integration)
- **File Implementasi:** [`app/services/nlp_stage2.py`](file:///d:/portfolio/AI/reqlint/backend/app/services/nlp_stage2.py).
- **Konfigurasi Provider (`.env`):**
  - `SLM_PROVIDER=mock`: Mengembalikan hasil rewrite SLA dan acceptance criteria Gherkin bawaan (ideal untuk dev lokal tanpa GPU).
  - `SLM_PROVIDER=ollama`: Menghubungkan ke instance Ollama lokal via `SLM_BASE_URL` (contoh: `http://localhost:11434`, model `phi3:mini` atau `llama3:8b`).
  - `SLM_PROVIDER=openai_compatible`: Menghubungkan ke vLLM, Groq, atau OpenAI kompatibel endpoint via `/v1/chat/completions`.
- **Format Prompt & Keamanan:**
  Teks masukan dibungkus ketat dalam delimiter:
  ```xml
  <user_story>
  {teks_pengguna}
  </user_story>
  ```
  System prompt menegaskan bahwa isi tag adalah **data murni**, bukan instruksi (kebal prompt injection).
- **Skema JSON Kontrak SLM:**
  ```json
  {
    "ai_rewrite": "User story yang telah diperbaiki dengan metrik SLA terukur",
    "acceptance_criteria": [
      {
        "given": "kondisi prasyarat",
        "when": "aksi pengguna",
        "then": "hasil terukur yang diharapkan"
      }
    ],
    "invest": {
      "independent": true,
      "negotiable": true,
      "valuable": true,
      "estimable": true,
      "small": true,
      "testable": true
    }
  }
  ```

### 3.4 Formula Scoring & Evaluasi INVEST
- **Formula Penalti:**
  $$\text{Skor} = \max\left(0, \min\left(100, 100 - \sum (\text{Penalti} \times \text{Multiplier})\right)\right)$$
  - Ambiguity: 8
  - Passive Voice: 6
  - Weak Directive: 5
  - Tidak Lengkap: 15 per elemen hilang
  - Multiplier: `LOW` = 0.5, `MEDIUM` = 1.0, `HIGH` = 1.5
  - Stage 2: Tiap kriteria INVEST yang gagal bernilai penalti tambahan -4.
- **Breakdown Metrik:**
  - **ISO 29148 (8 Karakteristik):** `unambiguous`, `complete`, `consistent`, `verifiable`, `modifiable`, `traceable`, `ranked`, `correct`.
  - **INVEST (6 Prinsip):** `independent`, `negotiable`, `valuable`, `estimable`, `small`, `testable`.
