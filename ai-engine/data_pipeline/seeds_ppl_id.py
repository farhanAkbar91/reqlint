"""
seeds_ppl_id.py
Koleksi benih User Story alami (Natural) Bahasa Indonesia yang bersumber dari proyek kuliah,
PPL (Praktek Proyek Perangkat Lunak), dan sistem informasi nyata di lingkungan universitas & industri lokal.
Mencakup: SIAKAD/KRS, Perpustakaan, Kasir POS, Logistik Ekspedisi, HRIS, E-Commerce, Kesehatan.
"""

PPL_INDONESIAN_SEEDS = [
    # Sistem Akademik & Portal Kampus (SIAKAD / KRS)
    {"source_id": "ppl_siakad_001", "text": "Sebagai mahasiswa, saya ingin mengisi formulir KRS online pada jadwal yang ditentukan, sehingga mata kuliah semester baru terdaftar resmi."},
    {"source_id": "ppl_siakad_002", "text": "Sebagai dosen pembimbing akademik, saya ingin menyetujui draf KRS mahasiswa bimbingan secara daring, sehingga status registrasi mahasiswa valid."},
    {"source_id": "ppl_siakad_003", "text": "Sebagai mahasiswa, saya ingin mengunduh Kartu Hasil Studi (KHS) dalam format PDF, sehingga saya memiliki arsip nilai resmi tiap semester."},
    {"source_id": "ppl_siakad_004", "text": "Sebagai bagian akademik, saya ingin mengunggah jadwal ujian akhir semester terpadu, sehingga mahasiswa mengetahui waktu dan ruang ujian."},
    {"source_id": "ppl_siakad_005", "text": "Sebagai mahasiswa tingkat akhir, saya ingin mendaftarkan judul skripsi dan memilih calon dosen pembimbing, sehingga proses tugas akhir dapat dimulai."},

    # Sistem Perpustakaan Digital Kampus
    {"source_id": "ppl_perpus_006", "text": "Sebagai anggota perpustakaan, saya ingin mencari ketersediaan buku fisik berdasarkan nomor ISBN atau nama pengarang, sehingga saya dapat langsung menuju rak yang tepat."},
    {"source_id": "ppl_perpus_007", "text": "Sebagai mahasiswa, saya ingin memperpanjang masa peminjaman buku secara online selama 7 hari, sehingga saya terhindar dari denda keterlambatan."},
    {"source_id": "ppl_perpus_008", "text": "Sebagai pustakawan, saya ingin memindai barcode kartu anggota saat peminjaman buku, sehingga pencatatan transaksi sirkulasi buku tercatat otomatis."},
    {"source_id": "ppl_perpus_009", "text": "Sebagai pengunjung perpustakaan, saya ingin mengunduh karya ilmiah tugas akhir dalam format PDF ber-watermark, sehingga saya memperoleh referensi penelitian."},
    {"source_id": "ppl_perpus_010", "text": "Sebagai pustakawan, saya ingin mencetak rekapitulasi buku yang belum dikembalikan melewati batas tempo, sehingga notifikasi peringatan dapat dikirimkan ke mahasiswa."},

    # Sistem Kasir & Point of Sale (POS) UMKM
    {"source_id": "ppl_pos_011", "text": "Sebagai kasir toko, saya ingin memindai barcode produk belanjaan dengan pemindai laser, sehingga harga barang langsung muncul pada struk pembayaran."},
    {"source_id": "ppl_pos_012", "text": "Sebagai kasir, saya ingin menerima pembayaran non-tunai melalui QRIS statis maupun dinamis, sehingga pembeli dapat bertransaksi tanpa uang tunai."},
    {"source_id": "ppl_pos_013", "text": "Sebagai pemilik toko, saya ingin melihat ringkasan omzet penjualan harian pada dashboard pemilik, sehingga saya dapat memantau perputaran kas usaha."},
    {"source_id": "ppl_pos_014", "text": "Sebagai staf gudang, saya ingin mencatat barang masuk dari surat jalan pemasok, sehingga jumlah stok barang pada sistem kasir selalu akurat."},
    {"source_id": "ppl_pos_015", "text": "Sebagai kasir, saya ingin mencetak struk transaksi duplikat saat kertas struk macet, sehingga pelanggan tetap mendapatkan bukti pembayaran sah."},

    # Logistik, Pengiriman, & Ekspedisi Lokal
    {"source_id": "ppl_logistik_016", "text": "Sebagai pembeli, saya ingin melacak posisi paket kiriman berdasarkan nomor resi pengiriman, sehingga saya mengetahui tahapan perjalanan pesanan."},
    {"source_id": "ppl_logistik_017", "text": "Sebagai kurir ekspedisi, saya ingin mengambil foto penerima paket sebagai bukti serah terima barang, sehingga status pengiriman terverifikasi sukses."},
    {"source_id": "ppl_logistik_018", "text": "Sebagai pengirim paket, saya ingin menghitung estimasi ongkos kirim berdasarkan berat paket dan kota tujuan, sehingga saya dapat memilih layanan pengiriman yang sesuai."},
    {"source_id": "ppl_logistik_019", "text": "Sebagai koordinator gudang sortir, saya ingin memilah paket berdasarkan kode area drop point, sehingga rute distribusi armada logistik lebih efisien."},
    {"source_id": "ppl_logistik_020", "text": "Sebagai penerima paket, saya ingin memberikan instruksi titik titip paket jika rumah kosong, sehingga kurir meletakkan paket di tempat yang aman."},

    # Kepegawaian & HRIS (Praktek Industri PPL)
    {"source_id": "ppl_hris_021", "text": "Sebagai karyawan, saya ingin mengajukan izin cuti tahunan melalui formulir elektronik, sehingga atasan langsung dapat memberikan persetujuan tanpa surat fisik."},
    {"source_id": "ppl_hris_022", "text": "Sebagai manajer HR, saya ingin melihat daftar rekapitulasi presensi bulanan seluruh staf, sehingga perhitungan tunjangan kehadiran akurat."},
    {"source_id": "ppl_hris_023", "text": "Sebagai staf akuntansi, saya ingin mengunduh slip gaji bulanan dalam format PDF berpassword NIK, sehingga kerahasiaan data pendapatan karyawan terjaga."},
    {"source_id": "ppl_hris_024", "text": "Sebagai pelamar kerja, saya ingin mengunggah berkas portofolio dan resume maksimal 5 MB, sehingga tim rekruter dapat meninjau kualifikasi saya."},
    {"source_id": "ppl_hris_025", "text": "Sebagai pimpinan divisi, saya ingin mengisi lembar evaluasi kinerja KPI staf setiap semester, sehingga penilaian promosi jabatan objektif."},

    # Layanan Kesehatan & Klinik Kampus
    {"source_id": "ppl_klinik_026", "text": "Sebagai pasien klinik, saya ingin mengambil nomor antrean poli umum secara online, sehingga saya tidak perlu menunggu lama di ruang tunggu klinik."},
    {"source_id": "ppl_klinik_027", "text": "Sebagai dokter pemeriksa, saya ingin mencatat resep obat digital ke modul farmasi, sehingga apoteker dapat segera meracik obat pasien."},
    {"source_id": "ppl_klinik_028", "text": "Sebagai apoteker klinik, saya ingin mencatat tanggal kadaluarsa obat pada kartu stok, sehingga obat yang hampir kedaluwarsa tidak diberikan ke pasien."},
    {"source_id": "ppl_klinik_029", "text": "Sebagai staf administrasi, saya ingin memverifikasi kepesertaan BPJS Kesehatan pasien secara real-time, sehingga biaya pengobatan ter-cover sistem."},
    {"source_id": "ppl_klinik_030", "text": "Sebagai pasien, saya ingin melihat riwayat kunjungan dokter dan catatan alergi obat, sehingga saya memahami kondisi kesehatan saya pribadi."}
]
