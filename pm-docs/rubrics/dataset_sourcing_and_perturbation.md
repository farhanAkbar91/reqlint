# Standar Operasional Sourcing & Perturbasi Dataset INVEST (1.000 User Stories)

**Dokumen Standar Pengadaan Data & Augmentasi Terkontrol**  
**Proyek**: ReqLint (Automated Agile User Story Quality Assurance via NLP)  
**Target Korpus**: 1.000 User Stories (500 Bahasa Indonesia, 500 Bahasa Inggris)  
**Lokasi Data Master**: [ai-engine/data/invest_corpus_1000.csv](file:///d:/portfolio/AI/reqlint/ai-engine/data/invest_corpus_1000.csv)  

---

## 1. Latar Belakang & Rasional Metodologis

Dalam penelitian *Requirements Engineering* (RE), korpus *user story* publik (seperti repositori Dalpiaz et al.) hampir seluruhnya berstatus kebutuhan "baik" atau "bersih" (*positive instances*). Hal ini memicu ketimpangan distribusi kelas (*class imbalance*) yang ekstrim untuk tugas deteksi cacat kebutuhan (*defect detection*).

Untuk mengatasi kelangkaan contoh negatif tanpa merusak keabsahan pengujian empiris, kami menerapkan metodologi **Perturbasi Terkontrol (*Controlled Perturbation*)** dengan protokol isolasi ketat:

1. **Sumber Alami (*Natural Stories*)**:
   * **Bahasa Inggris**: Mengadopsi domain publik dari repositori **Fabiano Dalpiaz et al.** (22 dataset sistem perangkat lunak, mencakup domain *OpenGov, FAA Aviation, CMS, SmartHome, University Management, Healthcare, Financial Systems,* dan *Logistics*).
   * **Bahasa Indonesia**: Diambil dari proyek kuliah riil dan studi kasus **PPL (Praktek Proyek Perangkat Lunak)** yang mencakup sistem informasi lokal (*SIAKAD/KRS Kampus, Perpustakaan Digital, POS/Kasir Toko UMKM, Ekspedisi Kargo, HRIS/Kepegawaian,* dan *Layanan Klinik*).
2. **Sampel Sintetis (*Synthetic Stories*)**:
   * Digunakan semata-mata untuk melengkapi variasi perbendaharaan kata pada fase *training*.
   * **Wajib ditandai** dengan kolom `source_type="synthetic"`.
3. **Sampel Cacat Hasil Perturbasi (*Controlled Perturbation*)**:
   * Dihasilkan melalui modifikasi terkontrol pada cerita alami dengan memicu kegagalan spesifik pada salah satu kriteria INVEST ($y_I, y_N, y_V, y_E, y_S, y_T = 0$).
4. **Aturan Emas Evaluasi (Test Set Isolation)**:
   * **Seluruh sampel sintetis dan perturbasi HANYA diperbolehkan masuk ke *Train Set***.
   * **Test Set (150 stories) dan Validation Set (100 stories) DIJAMIN 100% BERASAL DARI STORY ALAMI (*Natural Stories*)**. Hal ini memastikan model dievaluasi pada distribusi teks alami manusia, bukan mengevaluasi apakah model sekadar meniru aturan perturbasi.

---

## 2. Skema Metadata Dataset

Setiap baris data disimpan dengan skema seragam sebagai berikut:

| Nama Kolom | Tipe Data | Deskripsi |
|---|---|---|
| `id` | Integer | ID unik urut (1 s.d. 1.000) |
| `text` | String | Teks lengkap klausul *User Story* |
| `lang` | String | Kode bahasa (`id` untuk Indonesia, `en` untuk Inggris) |
| `source_id` | String | ID asal benih (contoh: `dalpiaz_opengov_001`, `ppl_siakad_001`, `perturb_t_id_005`) |
| `source_type` | String | Tipe asal: `natural_dalpiaz`, `natural_ppl`, `perturbed`, `synthetic` |
| `y_I` | Integer (0/1) | Label biner kriteria Independent |
| `y_N` | Integer (0/1) | Label biner kriteria Negotiable |
| `y_V` | Integer (0/1) | Label biner kriteria Valuable |
| `y_E` | Integer (0/1) | Label biner kriteria Estimable |
| `y_S` | Integer (0/1) | Label biner kriteria Small |
| `y_T` | Integer (0/1) | Label biner kriteria Testable |
| `annotator_a` | Integer (0/1) | Label kriteria utama dari Anotator A |
| `annotator_b` | Integer (0/1) | Label kriteria utama dari Anotator B |
| `split` | String | Pemisahan dataset: `train` (75%), `val` (10%), `test` (15%) |

---

## 3. Mekanisme Perturbasi Terkontrol per Kriteria

Modul `perturbation_engine.py` menginjeksi kecacatan tunggal yang ortogonal (*isolated flaw*) sehingga label *ground truth* diketahui secara pasti:

1. **Perturbasi Kriteria T ($y_T = 0$)**:
   * *Mekanisme*: Mengganti klausul aksi menjadi kalimat kualitatif subjektif (*"dengan sangat cepat, mudah, dan user-friendly"* / *"quickly, easily, and in a highly user-friendly manner"*).
2. **Perturbasi Kriteria S ($y_S = 0$)**:
   * *Mekanisme*: Menggabungkan dua user story independen dengan konjungsi majemuk (*"dan juga [aksi 2] serta sekaligus menyinkronkan seluruh database"* / *"and also [action 2] as well as sync all enterprise databases"*).
3. **Perturbasi Kriteria V ($y_V = 0$)**:
   * *Mekanisme*: Memotong dan membuang klausul manfaat (*"sehingga..."* / *"so that..."*), sehingga story kehilangan alasan nilai bisnisnya.
4. **Perturbasi Kriteria N ($y_N = 0$)**:
   * *Mekanisme*: Menginjeksi batasan implementasi fisik/teknis preskriptif tingkat rendah (misal: tombol biru 120x40px, font Arial 11pt, dan eksekusi kueri `SQL INSERT` ke tabel spesifik).
5. **Perturbasi Kriteria E ($y_E = 0$)**:
   * *Mekanisme*: Menginjeksi kuantitas tak berbatas (*vague quantifiers*) seperti *"beberapa data yang banyak dan berbagai macam metrik statistik lainnya dll"* / *"some various transaction metrics, several data items, and many open-ended options etc"*.
6. **Perturbasi Kriteria I ($y_I = 0$)**:
   * *Mekanisme*: Menginjeksi ketergantungan tiket cerita lain secara eksplisit (*"Hanya setelah User Story #US-25 selesai dikerjakan, sebagai..."* / *"Only after User Story US-42 is completed and deployed, as a..."*).

---

## 4. Distribusi Korpus Final (1.000 Stories)

Hasil eksekusi pembentukan korpus:

```
Total Stories     : 1.000
  - Bahasa ID     : 500 stories
  - Bahasa EN     : 500 stories

Distribusi Pembagian (Splits):
  - Train Set     : 750 stories (Kombinasi Natural, Perturbed, dan Synthetic)
  - Val Set       : 100 stories (100% Natural Stories)
  - Test Set      : 150 stories (100% Natural Stories - 0% Sintetis/Perturbasi)
```

### Akses Berkas Data:
* **Master CSV**: [ai-engine/data/invest_corpus_1000.csv](file:///d:/portfolio/AI/reqlint/ai-engine/data/invest_corpus_1000.csv)
* **Master JSON**: [ai-engine/data/invest_corpus_1000.json](file:///d:/portfolio/AI/reqlint/ai-engine/data/invest_corpus_1000.json)
* **Train Split**: [ai-engine/data/splits/train.csv](file:///d:/portfolio/AI/reqlint/ai-engine/data/splits/train.csv)
* **Val Split**: [ai-engine/data/splits/val.csv](file:///d:/portfolio/AI/reqlint/ai-engine/data/splits/val.csv)
* **Test Split**: [ai-engine/data/splits/test.csv](file:///d:/portfolio/AI/reqlint/ai-engine/data/splits/test.csv)
* **Skrip Generator**: [ai-engine/data_pipeline/build_invest_corpus.py](file:///d:/portfolio/AI/reqlint/ai-engine/data_pipeline/build_invest_corpus.py)
