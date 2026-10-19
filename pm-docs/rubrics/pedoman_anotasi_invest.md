# Pedoman Anotasi Kualitas Agile User Story Berdasarkan INVEST Criteria

**Dokumen Standar Operasional Anotasi Kebutuhan Perangkat Lunak**  
**Proyek**: ReqLint (Automated Agile User Story Quality Assurance via NLP)  
**Versi**: v0.9 (Draf Metodologi untuk Eksperimen Anotasi)  
**Target Korpus**: Agile User Stories Dwibahasa (Bahasa Indonesia & Bahasa Inggris)  

---

## 1. Pendahuluan & Format Pelabelan

Pedoman ini disusun sebagai acuan kerja bagi para anotator (*peer annotators*) untuk melakukan pelabelan kualitas pada korpus *Agile User Story*. Tujuan pelabelan ini adalah membangun *ground truth dataset* yang valid, objektif, dan dapat dipertanggungjawabkan untuk melatih serta menguji model klasifikasi pada sistem ReqLint.

### 1.1 Skema Format Output
Setiap User Story dievaluasi secara independen terhadap 6 kriteria **INVEST** (*Independent, Negotiable, Valuable, Estimable, Small, Testable*). Format luaran berupa vektor biner 6 dimensi:

$$\mathbf{y} = [y_I, y_N, y_V, y_E, y_S, y_T] \in \{0, 1\}^6$$

* **Label `1` (Pass / Memenuhi)**: User story memenuhi prinsip kriteria yang diuji (*clean requirement*).
* **Label `0` (Fail / Cacat)**: User story melanggar batasan kriteria operasional (*smell detected*).
* **Opsi `"RAGU"` (`?`)**: Selama sesi anotasi mandiri (*blind annotation*), anotator menandai opsi ini apabila menemui kasus batas (*borderline*) atau ketidakpastian domain. Kasus bertanda "RAGU" wajib didiskusikan dalam rapat rekonsiliasi hingga diperoleh konsensus biner (`1` atau `0`).

### 1.2 Interpretasi Metodologis Cohen's Kappa & Batasan Pelabelan
Kesepakatan antar-penilai (*Inter-Rater Reliability*) diukur menggunakan **Cohen's Kappa ($\kappa$)** yang didampingi oleh **PABAK (Prevalence-Adjusted and Bias-Adjusted Kappa)** untuk mengatasi *prevalence paradox* (kasus di mana suatu kriteria memiliki proporsi kelas 1 yang sangat dominan).

> [!IMPORTANT]
> **Catatan Metodologis:**  
> Cohen's Kappa mengukur konsistensi kesepakatan antar-manusia di atas faktor kebetulan (*chance agreement*). Nilai kappa **bukanlah** padanan langsung dari skor F1 model machine learning. Kappa yang rendah menandakan bahwa batasan operasional pada rubrik masih ambigu bagi manusia, sehingga data latih yang dihasilkan akan bising (*noisy label*). Target $\kappa \ge 0.60$ (klasifikasi *Substantial Agreement* menurut Landis & Koch, 1977) menjadi indikator kelayakan bahwa pedoman ini cukup jelas dan dapat direplikasi secara konsisten.

---

## 2. Hirarki Prioritas Pembelajaran (*Feature Engineering Hierarchy*)

Sesuai arahan perancangan arsitektur sistem ReqLint yang **dapat dijelaskan (*interpretable / white-box NLP*)**, evaluasi tidak menggunakan model generatif *black box*, melainkan pipeline berbasis fitur linguistik:

```
+-----------------------------------------------------------------------------------+
| TIER 1: Prioritas Utama (S, T, V)                                                |
| Karakteristik: Evaluasi Intrakalimat (Intra-Story / Teks Mandiri)                |
| Pendekatan: Leksikon, Rule-Based Matcher, Stanza Dependency Parsing & POS         |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| TIER 2: Prioritas Menengah (N, E)                                                |
| Karakteristik: Evaluasi Semantik & Batasan Fungsionalitas                         |
| Pendekatan: Ekstraksi fitur entitas teknis, rasio preskripsi UI, pohon sintaksis   |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| TIER 3: Prioritas Lanjutan (I)                                                    |
| Karakteristik: Evaluasi Antarcerita (Inter-Story / Multi-Klausul Backlog)         |
| Pendekatan: Graf Ketergantungan Cerita & Matriks Semantic Similarity (Lapisan 3)  |
+-----------------------------------------------------------------------------------+
```

* **Tier 1 (S, T, V)**: Dapat diputuskan 100% dari struktur satu *user story* tanpa konteks tambahan.
* **Tier 2 (N, E)**: Menilai batas antara kebutuhan fungsional pengguna (*what/why*) vs instruksi teknis kaku (*how*), serta batas kuantitatif lingkup kerja.
* **Tier 3 (I)**: Mengidentifikasi ketergantungan antar-story yang membutuhkan analisis konteks backlog (Lapisan 3).

---

## 3. Definisi Operasional, Aturan Keputusan, & Contoh Kasus

> [!NOTE]
> Daftar kata atau frasa pada aturan keputusan di bawah berfungsi sebagai **petunjuk/indikator linguistik (*heuristic cues*)**, bukan definisi mutlak. Anotator harus selalu mempertimbangkan konteks semantik kalimat secara utuh.

---

### Kriteria S: Small (Ukuran Tepat / Atomik) — *Prioritas Tier 1*

* **Definisi Operasional**: User Story harus berukuran ringkas dan merepresentasikan satu kapabilitas atomik yang wajar diselesaikan dalam satu siklus iterasi sprint (1–2 minggu).
* **Aturan Keputusan**:
  * **Beri Label `1`**: Story berfokus pada satu alur fungsionalitas tunggal.
  * **Beri Label `0`**: Story menggabungkan beberapa fungsionalitas independen yang dihubungkan dengan konjungsi majemuk (*"dan juga"*, *"serta sekaligus"*, *"and also"*, *"as well as"*) atau merangkum workflow end-to-end (Epic terselubung).
* **Contoh Kasus**:
  * **Positif (`1`)**: *"Sebagai kasir, saya ingin mencetak struk thermal, sehingga pelanggan menerima bukti pembayaran fisik."*
  * **Negatif (`0`)**: *"Sebagai admin gudang, saya ingin mencetak label barcode dan juga memperbarui stok barang serta mengirim notifikasi ke supplier, sehingga pengiriman siap."* *(Cacat S: Menggabungkan 3 domain aksi terpisah).*
  * **Borderline**: *"Sebagai kurir, saya ingin mengunggah foto paket dan membubuhkan tanda tangan penerima, sehingga bukti serah terima lengkap."*  
    *Resolusi Konsensus*: **Label `1`**. Foto dan tanda tangan merupakan dua elemen data dalam satu form transaksi serah terima yang sama, bukan fitur independen yang perlu dipisah sprint-nya.

---

### Kriteria T: Testable (Dapat Diuji) — *Prioritas Tier 1*

* **Definisi Operasional**: Story harus dirumuskan tanpa istilah kualitatif kabur, sehingga QA engineer dapat menyusun skenario pengujian *Given-When-Then* dengan kriteria kelulusan biner (Pass/Fail).
* **Aturan Keputusan**:
  * **Beri Label `1`**: Menggunakan parameter operasional terukur atau aksi sistem yang dapat diobservasi secara langsung.
  * **Beri Label `0`**: Mengandung kata sifat kualitatif tak terukur (*"cepat"*, *"mudah"*, *"user-friendly"*, *"aman"*, *"fast"*, *"easily"*) tanpa ambang batas kuantitatif, atau kalimat pasif yang mengaburkan penanggung jawab aksi.
* **Pemisahan Tegas dengan E**: Kata sifat subjektif/kualitatif dinilai pada **T**, **bukan** pada E.
* **Contoh Kasus**:
  * **Positif (`1`)**: *"Sebagai pengguna, saya ingin mengunduh laporan PDF berukuran < 5 MB dalam waktu < 3 detik, sehingga kuota data saya hemat."*
  * **Negatif (`0`)**: *"Sebagai pengguna, saya ingin sistem memproses transaksi dengan cepat dan user-friendly."* *(Cacat T: 'Cepat' dan 'user-friendly' tidak memiliki tolok ukur pengujian).*
  * **Borderline**: *"Sebagai kasir, saya ingin sistem memvalidasi barcode secara akurat, agar proses kasir lancar."*  
    *Resolusi Konsensus*: **Label `0`**. Kata *"secara akurat"* tidak memiliki ambang batas (misal: tingkat akurasi 99.9% atau toleransi karakter salah baca).

---

### Kriteria V: Valuable (Memberikan Nilai Nyata) — *Prioritas Tier 1*

* **Definisi Operasional**: Story harus memberikan manfaat nyata bagi pengguna akhir (*business/user value*) yang diekspresikan secara eksplisit dan substantif (bukan sekadar formalitas sintaksis).
* **Aturan Keputusan**:
  * **Beri Label `1`**: Memiliki klausul manfaat (*"sehingga..."* / *"so that..."*) yang menjelaskan dampak positif atau motivasi bisnis bagi persona pengguna.
  * **Beri Label `0`**: Klausul manfaat diabaikan sama sekali, atau manfaat bersifat tautologis (hanya mengulang aksi yang diminta), atau persona yang ditulis bukan pengguna nyata (*"Sebagai sistem..."*).
* **Contoh Kasus**:
  * **Positif (`1`)**: *"Sebagai pembeli, saya ingin melacak posisi kurir pada peta secara real-time, sehingga saya mengetahui estimasi waktu pesanan tiba."*
  * **Negatif (`0`)**: *"Sebagai user, saya ingin login dengan username dan password."* *(Cacat V: Tidak ada penjelasan manfaat nilai bisnis mengapa pengguna perlu login).*
  * **Borderline**: *"Sebagai staf HR, saya ingin mengajukan cuti tahunan, agar jatah cuti saya terpotong sesuai ketentuan perusahaan."*  
    *Resolusi Konsensus*: **Label `1`**. Terpotongnya kuota cuti secara akurat merupakan nilai administratif nyata bagi karyawan agar hak cutinya tercatat resmi.

---

### Kriteria N: Negotiable (Dapat Dinegosiasikan) — *Prioritas Tier 2*

* **Definisi Operasional**: User Story mendeskripsikan kebutuhan dari kacamata bisnis (*what & why*), bukan dokumen spesifikasi teknis kaku yang mengunci arsitektur atau tata letak antarmuka (*how*).
* **Aturan Keputusan**:
  * **Beri Label `1`**: Menyerahkan detail implementasi visual dan teknis kepada hasil diskusi kolaboratif tim pengembang dan desainer UI/UX.
  * **Beri Label `0`**: Mengunci rincian teknis tingkat rendah yang tidak esensial bagi pengguna (misal: ukuran piksel tombol, warna hex, font, nama tabel database relasional, atau perintah kueri SQL).
* **Contoh Kasus**:
  * **Positif (`1`)**: *"Sebagai kasir, saya ingin menyimpan transaksi penjualan dengan satu tombol konfirmasi, sehingga proses kasir ringkas."*
  * **Negatif (`0`)**: *"Sebagai kasir, saya ingin menekan tombol biru 120x40px berlabel 'SUBMIT' dengan font Roboto 12pt untuk menyimpan data ke tabel orders_v2."* *(Cacat N: Mengunci detail desain grafis dan skema database).*
  * **Borderline**: *"Sebagai nasabah, saya ingin mentransfer dana melalui jaringan BI-FAST, sehingga biaya transfer hemat."*  
    *Resolusi Konsensus*: **Label `1`**. Menyebutkan protokol "BI-FAST" adalah batasan produk finansial yang diinginkan konsumen, bukan instruksi coding internal.

---

### Kriteria E: Estimable (Dapat Diestimasi) — *Prioritas Tier 2*

* **Definisi Operasional**: Ruang lingkup fungsionalitas memiliki batasan yang jelas sehingga pengembang dapat memperkirakan kompleksitas teknis dan bobot kerja (*story points*).
* **Aturan Keputusan**:
  * **Beri Label `1`**: Batasan fungsionalitas dan masukan data terdefinisi dengan jelas.
  * **Beri Label `0`**: Mengandung kuantifikasi tak berbatas (*vague quantifiers*) seperti *"beberapa"*, *"sebagian besar"*, *"banyak"*, *"dll"*, *"several"*, *"various"*, *"etc"* yang membuat ruang lingkup mengambang.
* **Pemisahan Tegas dengan T**: Kriteria E difokuskan pada **ketidakjelasan cakupan/kuantitas fungsionalitas**, bukan pada sifat kata kualitatif.
* **Contoh Kasus**:
  * **Positif (`1`)**: *"Sebagai pedagang, saya ingin mengunggah katalog produk menggunakan template CSV berisi hingga 100 baris, sehingga proses input efisien."*
  * **Negatif (`0`)**: *"Sebagai investor, saya ingin melihat berbagai macam metrik saham dan banyak grafik interaktif secara otomatis."* *(Cacat E: Kata 'berbagai macam' dan 'banyak' membuat developer tidak tahu berapa komponen yang harus dibuat).*
  * **Borderline**: *"Sebagai penjual, saya ingin mengunggah beberapa berkas foto produk (maksimal 5 berkas), sehingga pembeli dapat melihat produk dari berbagai sisi."*  
    *Resolusi Konsensus*: **Label `1`**. Walaupun terdapat kata *"beberapa"*, terdapat klausul pembatas kuantitas eksplisit *(maksimal 5 berkas)*, sehingga pengembang dapat mengestimasi kapasitas penyimpanan dan validasi upload.

---

### Kriteria I: Independent (Mandiri) — *Prioritas Tier 3*

* **Definisi Operasional**: User Story tidak boleh memiliki keterikatan erat (*tight coupling*) atau ketergantungan urutan eksekusi yang kaku dengan *story* lain.
* **Aturan Keputusan**:
  * **Beri Label `1`**: Story dapat diprioritaskan dan diuji secara independen (misal dengan menggunakan *mock data* atau *stub*).
  * **Beri Label `0`**: Menyebutkan ketergantungan eksplisit terhadap ID story lain (*"setelah Story #12 selesai..."*, *"bergantung pada US-44..."*) atau tidak memiliki arti fungsional jika dipisahkan.
* **Contoh Kasus**:
  * **Positif (`1`)**: *"Sebagai pembeli, saya ingin melihat halaman konfirmasi pembayaran dengan rincian nomor invoice, sehingga saya yakin pesanan berhasil."*
  * **Negatif (`0`)**: *"Sebagai pembeli, setelah menyelesaikan Story #12 tentang checkout, saya ingin melihat halaman terima kasih."* *(Cacat I: Ketergantungan eksplisit ke tiket Story #12).*
  * **Borderline**: *"Sebagai staf gudang, saya ingin melihat daftar pesanan yang berstatus 'Lunas' untuk diproses packing, sehingga pengiriman tepat waktu."*  
    *Resolusi Konsensus*: **Label `1`**. Menjadikan status data ('Lunas') sebagai pra-kondisi adalah hal wajar dalam domain bisnis dan dapat diuji secara mandiri dengan memasukkan data mock bersatus 'Lunas', tanpa perlu menggabungkan pengerjaannya dengan modul payment gateway.

---

## 4. Protokol Eksperimen Anotasi Riil (Langkah Kerja Mandiri)

Untuk menghasilkan evaluasi yang valid secara metodologis, tim wajib menjalankan langkah-langkah berikut:

1. **Persiapan Lembar Kerja Kosong**:
   * Ambil berkas [lembar_anotasi_kosong.csv](file:///d:/portfolio/AI/reqlint/ai-engine/benchmarks/lembar_anotasi_kosong.csv) yang berisi kumpulan *User Story* tanpa ada label bawaan.
2. **Proses Pelabelan Mandiri (Blind Annotation)**:
   * **Anotator 1** dan **Anotator 2** mengisi lembar kerja secara terpisah tanpa saling berkomunikasi atau berdiskusi.
   * Setiap kolom kriteria (I, N, V, E, S, T) diisi `1` atau `0`. Kolom `Catatan_Ragu` diisi apabila anotator merasa ragu.
3. **Kalkulasi Metrik & Identifikasi Perbedaan**:
   * Jalankan skrip [invest_annotation_experiment.py](file:///d:/portfolio/AI/reqlint/ai-engine/benchmarks/invest_annotation_experiment.py) untuk membaca kedua file CSV hasil anotasi riil.
   * Skrip akan menghitung **Cohen's Kappa ($\kappa$)**, **PABAK**, persentase observed agreement ($P_o$), serta distribusi cacat (jumlah label 0).
4. **Rapat Rekonsiliasi & Konsensus**:
   * Kedua anotator duduk bersama untuk mendiskusikan seluruh baris yang berbeda (*discrepancy*) serta baris yang bertanda *RAGU*.
   * Lakukan perbaikan rumusan pedoman jika terdapat kasus batas yang belum terakomodasi.
5. **Putaran Validasi Lanjutan**:
   * Jika pada putaran pertama terdapat kriteria dengan $\kappa < 0.60$, lakukan pengujian Putaran 2 pada batch *user story* baru untuk membuktikan bahwa perbaikan pedoman berhasil meningkatkan reliabilitas anotator.
