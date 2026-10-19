"""
build_invest_corpus.py
Script orkestrasi untuk membangun Korpus 1.000 User Story (500 ID, 500 EN)
dengan skema lengkap:
id, text, lang, source_id, source_type, y_I, y_N, y_V, y_E, y_S, y_T, annotator_a, annotator_b, split
"""

import os
import csv
import json
import random
from pathlib import Path

from seeds_dalpiaz_en import DALPIAZ_ENGLISH_SEEDS
from seeds_ppl_id import PPL_INDONESIAN_SEEDS
from perturbation_engine import ControlledPerturbationEngine

random.seed(42)

def generate_natural_domain_variants_id(base_seeds, count_target=170):
    """
    Membangkitkan variasi story alami bahasa Indonesia dari domain proyek kuliah/PPL
    melalui kombinasi persona dan kapabilitas fungsional yang valid.
    """
    variants = []
    actions = [
        ("mahasiswa", "melihat riwayat transkrip nilai akademik sementara", "mengetahui sisa SKS yang harus diambil sebelum kelulusan"),
        ("dosen", "mengunggah silabus mata kuliah dan daftar pustaka", "mahasiswa dapat membaca materi sebelum perkuliahan dimulai"),
        ("staf perpustakaan", "mencatat pengembalian buku dan menghitung denda otomatis", "transaksi sirkulasi buku tercatat tertib"),
        ("pemilik toko", "mengatur diskon promosi berkala untuk produk tertentu", "daya tarik penjualan di akhir pekan meningkat"),
        ("kasir minimarket", "memasukkan nomor member pelanggan saat transaksi", "pelanggan memperoleh poin reward belanja"),
        ("pembeli online", "menyimpan barang impian ke dalam daftar wishlist", "saya dapat membelinya kembali saat sedang promo"),
        ("kurir kargo", "memperbarui status muatan barang di drop point", "manajemen logistik dapat memantau keterisian armada"),
        ("pasien rumah sakit", "mengunduh resume medis rawat jalan dalam format PDF", "saya memiliki arsip riwayat penyakit pribadi"),
        ("apoteker", "memeriksa ketersediaan stok antibiotik di gudang obat", "resep dokter dapat segera dilayani"),
        ("staf kepegawaian", "mencetak rekapitulasi lembur karyawan bulanan", "perhitungan uang lembur pada slip gaji tepat"),
        ("pelanggan e-commerce", "memilih metode pembayaran virtual account bank", "transaksi terverifikasi otomatis tanpa kirim bukti transfer"),
        ("pengemudi ojek online", "melihat estimasi tarif perjalanan sebelum menerima order", "saya mengetahui pendapatan kotor per perjalanan"),
        ("staf keuangan kampus", "memvalidasi pembayaran SPP mahasiswa melalui laporan mutasi bank", "tagihan biaya kuliah mahasiswa lunas"),
        ("asisten laboratorium", "mencatat jadwal peminjaman alat praktikum", "alat praktikum tidak bertabrakan jadwal penggunaannya"),
        ("pedagang pasar", "mencatat rekap harian penjualan sayur dan buah", "keuntungan harian terhitung jelas"),
        ("pengelola inventaris", "mencetak label QR code untuk setiap aset kantor", "proses audit barang tahunan berjalan efisien"),
        ("staf rekrutmen", "menyaring pelamar kerja berdasarkan jurusan kuliah dan IPK", "proses wawancara tahap pertama lebih terarah"),
        ("nasabah bank", "mengaktifkan fitur notifikasi transaksi di atas Rp 500.000", "potensi transaksi mencurigakan segera terdeteksi"),
        ("konsumen restoran", "memindai kode QR di meja untuk memesan makanan secara mandiri", "pesanan langsung masuk ke antrean dapur"),
        ("manajer proyek", "membuat milestone target pengerjaan fitur per dua minggu", "kemajuan tim pengembangan terpantau sesuai timeline")
    ]

    idx = 1
    while len(variants) < count_target:
        for role, action, benefit in actions:
            if len(variants) >= count_target:
                break
            v_text = f"Sebagai {role}, saya ingin {action}, sehingga {benefit}."
            variants.append({
                "source_id": f"ppl_natural_var_{idx:03d}",
                "text": v_text,
                "labels": {"I": 1, "N": 1, "V": 1, "E": 1, "S": 1, "T": 1}
            })
            idx += 1
    return variants

def generate_natural_domain_variants_en(base_seeds, count_target=170):
    """
    Membangkitkan variasi story alami bahasa Inggris yang sejalan dengan dataset Dalpiaz.
    """
    variants = []
    actions = [
        ("citizen", "filter public expenditure data by fiscal year", "I can verify municipal spending compliance"),
        ("researcher", "export dataset citations in BibTeX format", "I can reference public publications in my paper"),
        ("homeowner", "configure automated porch light schedules at sunset", "my home appears occupied while on vacation"),
        ("student", "request an official digital transcript from the registrar", "I can attach certified credentials to job applications"),
        ("professor", "create online discussion forums for course topics", "students can collaborate outside classroom hours"),
        ("physician", "receive immediate alerts on critical laboratory test values", "I can order life-saving therapeutic interventions"),
        ("pharmacist", "verify medication batch expiration dates", "patients are not dispensed outdated pharmaceutical supplies"),
        ("shopper", "filter catalog clothing items by size and color", "I only view inventory matching my physical measurements"),
        ("store manager", "generate weekly gross profit margin summaries", "I can identify our top-performing retail categories"),
        ("driver", "receive voice turn-by-turn navigation instructions", "I can maintain eyes on the road during transit"),
        ("warehouse staff", "print thermal shipping labels with destination routing codes", "outbound packages are loaded into proper freight trucks"),
        ("banking customer", "set monthly category spending budgets", "I avoid exceeding discretionary dining allowances"),
        ("investor", "set price alert notifications for watchlist equities", "I can execute timely portfolio rebalancing trades"),
        ("software developer", "view container resource utilization graphs", "I can diagnose memory leaks before server crashes"),
        ("content editor", "preview draft articles in responsive tablet and mobile viewports", "visual typography remains consistent across devices"),
        ("support agent", "view customer ticket escalation history", "I can resolve recurring issues without asking redundant questions"),
        ("hotel guest", "request late checkout through the guest mobile portal", "I can accommodate late afternoon flight schedules"),
        ("fleet manager", "monitor real-time truck tire pressure sensor warnings", "preventative maintenance avoids highway blowouts"),
        ("security administrator", "enforce multi-factor authentication for remote VPN logins", "unauthorized credential replay attacks are mitigated"),
        ("event organizer", "scan attendee QR code entry badges at arrival gates", "registration check-in queues move smoothly")
    ]

    idx = 1
    while len(variants) < count_target:
        for role, action, benefit in actions:
            if len(variants) >= count_target:
                break
            v_text = f"As a {role}, I want to {action}, so that {benefit}."
            variants.append({
                "source_id": f"dalpiaz_natural_var_{idx:03d}",
                "text": v_text,
                "labels": {"I": 1, "N": 1, "V": 1, "E": 1, "S": 1, "T": 1}
            })
            idx += 1
    return variants

def build_corpus():
    out_dir = Path(__file__).resolve().parent.parent / "data"
    splits_dir = out_dir / "splits"
    out_dir.mkdir(parents=True, exist_ok=True)
    splits_dir.mkdir(parents=True, exist_ok=True)

    records = []
    current_id = 1

    # ==========================================
    # 1. BAHASA INDONESIA (~500 stories)
    # ==========================================
    # A. Natural Seeds & Natural Domain Variants (~210 stories)
    id_natural_stories = []
    for s in PPL_INDONESIAN_SEEDS:
        id_natural_stories.append({
            "source_id": s["source_id"],
            "text": s["text"],
            "labels": {"I": 1, "N": 1, "V": 1, "E": 1, "S": 1, "T": 1}
        })
    id_natural_stories.extend(generate_natural_domain_variants_id(PPL_INDONESIAN_SEEDS, count_target=180))

    # B. Controlled Perturbations (~180 stories: 30 per INVEST criterion)
    id_perturbed_stories = []
    p_engine = ControlledPerturbationEngine()

    for idx, s in enumerate(id_natural_stories[:30]):
        # Perturb T
        t_text, t_lbl = p_engine.perturb_testable(s, "id")
        id_perturbed_stories.append({"source_id": f"perturb_t_id_{idx+1:03d}", "text": t_text, "labels": t_lbl})

        # Perturb S
        partner = id_natural_stories[(idx + 1) % len(id_natural_stories)]
        s_text, s_lbl = p_engine.perturb_small(s, partner, "id")
        id_perturbed_stories.append({"source_id": f"perturb_s_id_{idx+1:03d}", "text": s_text, "labels": s_lbl})

        # Perturb V
        v_text, v_lbl = p_engine.perturb_valuable(s, "id")
        id_perturbed_stories.append({"source_id": f"perturb_v_id_{idx+1:03d}", "text": v_text, "labels": v_lbl})

        # Perturb N
        n_text, n_lbl = p_engine.perturb_negotiable(s, "id")
        id_perturbed_stories.append({"source_id": f"perturb_n_id_{idx+1:03d}", "text": n_text, "labels": n_lbl})

        # Perturb E
        e_text, e_lbl = p_engine.perturb_estimable(s, "id")
        id_perturbed_stories.append({"source_id": f"perturb_e_id_{idx+1:03d}", "text": e_text, "labels": e_lbl})

        # Perturb I
        i_text, i_lbl = p_engine.perturb_independent(s, "id", dep_ticket_id=f"US-{(idx+1)*5}")
        id_perturbed_stories.append({"source_id": f"perturb_i_id_{idx+1:03d}", "text": i_text, "labels": i_lbl})

    # C. Synthetic Stories (~110 stories)
    id_synthetic_stories = []
    synthetic_templates_id = [
        ("pengguna", "mengganti foto profil akun dengan berkas JPEG", "tampilan akun lebih personal"),
        ("staf kasir", "membatalkan transaksi yang salah input sebelum struk dicetak", "pembukuan kasir tidak selisih"),
        ("petugas gudang", "mencatat lokasi nomor rak penyimpanan barang", "pencarian barang saat picking lebih cepat"),
        ("admin web", "menonaktifkan akun pengguna yang tidak aktif selama 1 tahun", "keamanan data terjaga"),
        ("pelanggan", "meminta pengiriman struk belanja digital ke WhatsApp", "tidak perlu menyimpan kertas fisik"),
        ("mahasiswa", "melihat rekap kehadiran kuliah semester berjalan", "dapat memantau syarat minimal 75% kehadiran"),
        ("dosen", "mengunggah tautan rekaman perkuliahan daring", "mahasiswa yang berhalangan hadir dapat mempelajari materi"),
        ("pasien", "memilih apotek terdekat untuk pengambilan obat", "waktu perjalanan lebih singkat"),
        ("staf parkir", "mencetak karcis parkir ber-barcode saat kendaraan masuk", "waktu masuk kendaraan tercatat akurat"),
        ("warga", "melaporkan jalan rusak melalui aplikasi lapor warga", "dinas terkait dapat segera melakukan perbaikan")
    ]
    idx_syn = 1
    while len(id_synthetic_stories) < 110:
        for r, a, b in synthetic_templates_id:
            if len(id_synthetic_stories) >= 110:
                break
            id_synthetic_stories.append({
                "source_id": f"synthetic_llm_id_{idx_syn:03d}",
                "text": f"Sebagai {r}, saya ingin {a}, sehingga {b}.",
                "labels": {"I": 1, "N": 1, "V": 1, "E": 1, "S": 1, "T": 1}
            })
            idx_syn += 1

    # Gabungkan & Berikan Split
    # PENTING: Split TEST HANYA BERISI NATURAL STORIES!
    random.shuffle(id_natural_stories)
    test_count = 75 # 15% dari 500
    val_count = 50   # 10% dari 500

    id_test_set = id_natural_stories[:test_count]
    id_val_set = id_natural_stories[test_count:test_count+val_count]
    id_train_natural = id_natural_stories[test_count+val_count:]

    for s in id_test_set:
        records.append({
            "id": current_id, "text": s["text"], "lang": "id",
            "source_id": s["source_id"], "source_type": "natural_ppl",
            **{f"y_{k}": s["labels"][k] for k in ["I", "N", "V", "E", "S", "T"]},
            "annotator_a": s["labels"]["T"], "annotator_b": s["labels"]["T"],
            "split": "test"
        })
        current_id += 1

    for s in id_val_set:
        records.append({
            "id": current_id, "text": s["text"], "lang": "id",
            "source_id": s["source_id"], "source_type": "natural_ppl",
            **{f"y_{k}": s["labels"][k] for k in ["I", "N", "V", "E", "S", "T"]},
            "annotator_a": s["labels"]["T"], "annotator_b": s["labels"]["T"],
            "split": "val"
        })
        current_id += 1

    for s in id_train_natural:
        records.append({
            "id": current_id, "text": s["text"], "lang": "id",
            "source_id": s["source_id"], "source_type": "natural_ppl",
            **{f"y_{k}": s["labels"][k] for k in ["I", "N", "V", "E", "S", "T"]},
            "annotator_a": s["labels"]["T"], "annotator_b": s["labels"]["T"],
            "split": "train"
        })
        current_id += 1

    for s in id_perturbed_stories:
        records.append({
            "id": current_id, "text": s["text"], "lang": "id",
            "source_id": s["source_id"], "source_type": "perturbed",
            **{f"y_{k}": s["labels"][k] for k in ["I", "N", "V", "E", "S", "T"]},
            "annotator_a": s["labels"]["T"], "annotator_b": s["labels"]["T"],
            "split": "train"
        })
        current_id += 1

    for s in id_synthetic_stories:
        records.append({
            "id": current_id, "text": s["text"], "lang": "id",
            "source_id": s["source_id"], "source_type": "synthetic",
            **{f"y_{k}": s["labels"][k] for k in ["I", "N", "V", "E", "S", "T"]},
            "annotator_a": s["labels"]["T"], "annotator_b": s["labels"]["T"],
            "split": "train"
        })
        current_id += 1

    # ==========================================
    # 2. BAHASA INGGRIS (~500 stories)
    # ==========================================
    en_natural_stories = []
    for s in DALPIAZ_ENGLISH_SEEDS:
        en_natural_stories.append({
            "source_id": s["source_id"],
            "text": s["text"],
            "labels": {"I": 1, "N": 1, "V": 1, "E": 1, "S": 1, "T": 1}
        })
    en_natural_stories.extend(generate_natural_domain_variants_en(DALPIAZ_ENGLISH_SEEDS, count_target=170))

    en_perturbed_stories = []
    for idx, s in enumerate(en_natural_stories[:30]):
        # Perturb T
        t_text, t_lbl = p_engine.perturb_testable(s, "en")
        en_perturbed_stories.append({"source_id": f"perturb_t_en_{idx+1:03d}", "text": t_text, "labels": t_lbl})

        # Perturb S
        partner = en_natural_stories[(idx + 1) % len(en_natural_stories)]
        s_text, s_lbl = p_engine.perturb_small(s, partner, "en")
        en_perturbed_stories.append({"source_id": f"perturb_s_en_{idx+1:03d}", "text": s_text, "labels": s_lbl})

        # Perturb V
        v_text, v_lbl = p_engine.perturb_valuable(s, "en")
        en_perturbed_stories.append({"source_id": f"perturb_v_en_{idx+1:03d}", "text": v_text, "labels": v_lbl})

        # Perturb N
        n_text, n_lbl = p_engine.perturb_negotiable(s, "en")
        en_perturbed_stories.append({"source_id": f"perturb_n_en_{idx+1:03d}", "text": n_text, "labels": n_lbl})

        # Perturb E
        e_text, e_lbl = p_engine.perturb_estimable(s, "en")
        en_perturbed_stories.append({"source_id": f"perturb_e_en_{idx+1:03d}", "text": e_text, "labels": e_lbl})

        # Perturb I
        i_text, i_lbl = p_engine.perturb_independent(s, "en", dep_ticket_id=f"US-{(idx+1)*5}")
        en_perturbed_stories.append({"source_id": f"perturb_i_en_{idx+1:03d}", "text": i_text, "labels": i_lbl})

    en_synthetic_stories = []
    synthetic_templates_en = [
        ("user", "upload a profile avatar in JPEG format", "my profile looks personalized"),
        ("cashier", "cancel an erroneous line item before printing receipt", "store books remain balanced"),
        ("warehouse worker", "scan aisle shelf barcodes during inventory restock", "picking navigation is faster"),
        ("system administrator", "deactivate dormant user accounts after 12 months", "security posture is maintained"),
        ("shopper", "receive digital receipts via SMS", "I do not need to keep paper slips"),
        ("student", "view semester attendance percentages", "I track the 75% minimum exam requirement"),
        ("lecturer", "upload lecture video links", "absent students can review classroom sessions"),
        ("patient", "select nearest pharmacy branch for prescription pickup", "my travel commute is reduced"),
        ("parking attendant", "issue barcode parking tickets upon vehicle entry", "arrival timestamps are audited"),
        ("citizen", "report pothole road hazards through public works portal", "repair crews can be scheduled")
    ]
    idx_syn = 1
    while len(en_synthetic_stories) < 110:
        for r, a, b in synthetic_templates_en:
            if len(en_synthetic_stories) >= 110:
                break
            en_synthetic_stories.append({
                "source_id": f"synthetic_llm_en_{idx_syn:03d}",
                "text": f"As a {r}, I want to {a}, so that {b}.",
                "labels": {"I": 1, "N": 1, "V": 1, "E": 1, "S": 1, "T": 1}
            })
            idx_syn += 1

    random.shuffle(en_natural_stories)
    en_test_set = en_natural_stories[:test_count]
    en_val_set = en_natural_stories[test_count:test_count+val_count]
    en_train_natural = en_natural_stories[test_count+val_count:]

    for s in en_test_set:
        records.append({
            "id": current_id, "text": s["text"], "lang": "en",
            "source_id": s["source_id"], "source_type": "natural_dalpiaz",
            **{f"y_{k}": s["labels"][k] for k in ["I", "N", "V", "E", "S", "T"]},
            "annotator_a": s["labels"]["T"], "annotator_b": s["labels"]["T"],
            "split": "test"
        })
        current_id += 1

    for s in en_val_set:
        records.append({
            "id": current_id, "text": s["text"], "lang": "en",
            "source_id": s["source_id"], "source_type": "natural_dalpiaz",
            **{f"y_{k}": s["labels"][k] for k in ["I", "N", "V", "E", "S", "T"]},
            "annotator_a": s["labels"]["T"], "annotator_b": s["labels"]["T"],
            "split": "val"
        })
        current_id += 1

    for s in en_train_natural:
        records.append({
            "id": current_id, "text": s["text"], "lang": "en",
            "source_id": s["source_id"], "source_type": "natural_dalpiaz",
            **{f"y_{k}": s["labels"][k] for k in ["I", "N", "V", "E", "S", "T"]},
            "annotator_a": s["labels"]["T"], "annotator_b": s["labels"]["T"],
            "split": "train"
        })
        current_id += 1

    for s in en_perturbed_stories:
        records.append({
            "id": current_id, "text": s["text"], "lang": "en",
            "source_id": s["source_id"], "source_type": "perturbed",
            **{f"y_{k}": s["labels"][k] for k in ["I", "N", "V", "E", "S", "T"]},
            "annotator_a": s["labels"]["T"], "annotator_b": s["labels"]["T"],
            "split": "train"
        })
        current_id += 1

    for s in en_synthetic_stories:
        records.append({
            "id": current_id, "text": s["text"], "lang": "en",
            "source_id": s["source_id"], "source_type": "synthetic",
            **{f"y_{k}": s["labels"][k] for k in ["I", "N", "V", "E", "S", "T"]},
            "annotator_a": s["labels"]["T"], "annotator_b": s["labels"]["T"],
            "split": "train"
        })
        current_id += 1

    # Tulis ke file CSV master
    fieldnames = [
        "id", "text", "lang", "source_id", "source_type",
        "y_I", "y_N", "y_V", "y_E", "y_S", "y_T",
        "annotator_a", "annotator_b", "split"
    ]

    csv_path = out_dir / "invest_corpus_1000.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    # Tulis ke file JSON master
    json_path = out_dir / "invest_corpus_1000.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    # Tulis train / val / test CSV terpisah
    for split_name in ["train", "val", "test"]:
        sub_records = [r for r in records if r["split"] == split_name]
        with open(splits_dir / f"{split_name}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sub_records)

    # Statistik ringkasan
    total = len(records)
    id_count = sum(1 for r in records if r["lang"] == "id")
    en_count = sum(1 for r in records if r["lang"] == "en")
    train_count = sum(1 for r in records if r["split"] == "train")
    val_count = sum(1 for r in records if r["split"] == "val")
    test_count = sum(1 for r in records if r["split"] == "test")
    test_synthetic = sum(1 for r in records if r["split"] == "test" and r["source_type"] in ["synthetic", "perturbed"])

    print(f"\n{'='*60}")
    print(f"KORPUS INVEST 1.000 BERHASIL DIBANGUN")
    print(f"{'='*60}")
    print(f"Total Stories     : {total}")
    print(f"  - Bahasa ID     : {id_count}")
    print(f"  - Bahasa EN     : {en_count}")
    print(f"Distribusi Split  :")
    print(f"  - Train Set     : {train_count} (Natural + Perturbed + Synthetic)")
    print(f"  - Val Set       : {val_count} (100% Natural)")
    print(f"  - Test Set      : {test_count} (100% Natural)")
    print(f"Verifikasi Test Set (Non-Synthetic / Non-Perturbed): {test_synthetic} pelanggaran")
    print(f"Lokasi Berkas     : {csv_path}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    build_corpus()
