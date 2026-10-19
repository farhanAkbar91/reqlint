"""
invest_annotation_experiment.py
Modul perhitungan Inter-Rater Reliability (Cohen's Kappa & PABAK) untuk evaluasi anotasi INVEST.
Mendukung input berkas CSV anotasi riil dari dua annotator independen.
"""

import sys
import csv
import json
from pathlib import Path
from typing import List, Dict, Tuple

def compute_inter_rater_metrics(labels1: List[int], labels2: List[int]) -> Dict[str, float]:
    """
    Menghitung Po (Observed Agreement), Pe (Expected Chance Agreement),
    Cohen's Kappa, dan PABAK (Prevalence-Adjusted and Bias-Adjusted Kappa).
    """
    n = len(labels1)
    if n == 0:
        return {"po": 1.0, "pe": 1.0, "kappa": 1.0, "pabak": 1.0, "n": 0, "neg_count": 0}

    agree = sum(1 for a, b in zip(labels1, labels2) if a == b)
    po = agree / n

    # Proporsi kelas 1 dan 0
    p1_1 = sum(1 for a in labels1 if a == 1) / n
    p1_0 = 1.0 - p1_1
    p2_1 = sum(1 for b in labels2 if b == 1) / n
    p2_0 = 1.0 - p2_1

    pe = (p1_1 * p2_1) + (p1_0 * p2_0)
    
    if pe >= 1.0:
        kappa = 1.0
    else:
        kappa = (po - pe) / (1.0 - pe)

    # PABAK = 2 * Po - 1
    # Sangat berguna untuk mendiagnosis prevalence paradox jika kelas 1 sangat dominan
    pabak = (2.0 * po) - 1.0

    neg_count = sum(1 for a in labels1 if a == 0)

    return {
        "n": n,
        "po": round(po, 4),
        "pe": round(pe, 4),
        "kappa": round(kappa, 4),
        "pabak": round(pabak, 4),
        "neg_count": neg_count
    }

def evaluate_csv_annotations(csv_path_annotator_1: str, csv_path_annotator_2: str):
    """
    Membaca dua file CSV hasil kerja mandiri penilai 1 dan penilai 2,
    lalu menampilkan tabel evaluasi kesepakatan per kriteria INVEST.
    """
    path1 = Path(csv_path_annotator_1)
    path2 = Path(csv_path_annotator_2)

    if not path1.exists() or not path2.exists():
        print(f"Error: Salah satu berkas tidak ditemukan: {path1} atau {path2}")
        return

    criteria_keys = ["I", "N", "V", "E", "S", "T"]
    data1 = {k: [] for k in criteria_keys}
    data2 = {k: [] for k in criteria_keys}

    with open(path1, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for k in criteria_keys:
                val = row.get(k, "").strip()
                data1[k].append(int(val) if val in {"0", "1"} else -1)

    with open(path2, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for k in criteria_keys:
                val = row.get(k, "").strip()
                data2[k].append(int(val) if val in {"0", "1"} else -1)

    print(f"\n{'='*75}")
    print(f"{'HASIL EVALUASI KESEPAKATAN ANOTASI INDEPENDEN':^75}")
    print(f"{'='*75}")
    print(f"{'Kriteria':<6} | {'N':<4} | {'Label 0':<8} | {'Po (%)':<8} | {'Pe (%)':<8} | {'Kappa':<8} | {'PABAK':<8} | {'Status'}")
    print(f"{'-'*75}")

    for k in criteria_keys:
        # Filter hanya baris yang telah diberi label valid (0 atau 1)
        valid_pairs = [(a, b) for a, b in zip(data1[k], data2[k]) if a in {0, 1} and b in {0, 1}]
        if not valid_pairs:
            print(f"{k:<6} | Data belum lengkap.")
            continue

        l1 = [p[0] for p in valid_pairs]
        l2 = [p[1] for p in valid_pairs]
        res = compute_inter_rater_metrics(l1, l2)

        status = "Substantial (Lolos)" if res["kappa"] >= 0.60 else "Perlu Rekonsiliasi"
        print(f"{k:<6} | {res['n']:<4} | {res['neg_count']:<8} | {res['po']*100:<7.1f}% | {res['pe']*100:<7.1f}% | {res['kappa']:<8.3f} | {res['pabak']:<8.3f} | {status}")

    print(f"{'='*75}\n")

if __name__ == "__main__":
    print("Modul Evaluasi Inter-Rater Reliability ReqLint siap digunakan.")
    print("Gunakan fungsi evaluate_csv_annotations(file_anotator1.csv, file_anotator2.csv) untuk menguji hasil nyata.")
