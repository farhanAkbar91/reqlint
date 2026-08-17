"""
Indonesian Requirement Smell Dictionaries based on IEEE 29148 & INVEST
"""

INDONESIAN_WEAK_DIRECTIVES = {
    "sebaiknya": "Gunakan kata kerja imperatif tegas seperti 'harus' (shall/must).",
    "dapat": "Ambiguitas kemampuan/opsional. Gunakan 'harus' jika ini kewajiban sistem.",
    "mungkin": "Ketidakpastian tinggi. Hapus spekulasi.",
    "diharapkan": "Bukan kriteria teruji. Nyatakan secara eksplisit tanggung jawab sistem.",
    "sekiranya": "Perlu diperjelas kondisi pastinya.",
    "bisa": "Ambiguitas kapabilitas vs kewajiban. Perjelas perilaku sistem."
}

INDONESIAN_SUBJECTIVE_ADJECTIVES = {
    "cepat": "Sebutkan ambang batas waktu terukur (misal: response time < 200 ms).",
    "mudah": "Definisikan kriteria kemudahan (misal: dapat diselesaikan dalam max 3 klik).",
    "handal": "Sebutkan target SLA / Uptime (misal: availability 99.9%).",
    "aman": "Sebutkan standar enkripsi / protokol keamanan spesifik (misal: TLS 1.3 / AES-256).",
    "user-friendly": "Definisikan parameter usability atau kriteria pengujian pengguna.",
    "efisien": "Nyatakan batasan penggunaan memori, CPU, atau throughput yang terukur.",
    "fleksibel": "Spesifikasikan parameter modul atau opsi konfigurasi yang didukung."
}

INDONESIAN_VAGUE_QUANTIFIERS = {
    "beberapa": "Sebutkan jumlah persis atau rentang angka pasti.",
    "sebagian besar": "Nyatakan persentase atau kriteria kuantitatif terukur.",
    "banyak": "Nyatakan batasan numerik pasti.",
    "dll": "Hindari singkatan terbuka. Daftarkan seluruh item secara eksplisit.",
    "dan sebagainya": "Hindari kualifikasi terbuka. Sebutkan daftar item lengkap."
}
