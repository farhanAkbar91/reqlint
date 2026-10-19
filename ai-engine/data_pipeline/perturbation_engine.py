"""
perturbation_engine.py
Modul Perturbasi Terkontrol untuk membangkitkan sampel negatif (story buruk)
pada setiap kriteria INVEST (I, N, V, E, S, T) dengan ground truth terdefinisi.
"""

import re
from typing import Dict, Any, Tuple

class ControlledPerturbationEngine:
    """
    Menghasilkan variasi User Story dengan kecacatan terukur (Perturbasi Terkontrol).
    Masing-masing fungsi menjamin label biner kriteria yang tepat.
    """

    @staticmethod
    def perturb_testable(story: Dict[str, Any], lang: str) -> Tuple[str, Dict[str, int]]:
        text = story["text"]
        labels = {"I": 1, "N": 1, "V": 1, "E": 1, "S": 1, "T": 0}

        if lang == "id":
            # Ganti klausa aksi menjadi ambigu / kualitatif tak terukur
            text_p = re.sub(
                r'(saya ingin\s+[^,]+)',
                r'\1 dengan sangat cepat, mudah, dan user-friendly',
                text,
                count=1,
                flags=re.IGNORECASE
            )
            if text_p == text:
                text_p = text.replace("sehingga", "dengan cepat dan mudah, sehingga")
        else:
            text_p = re.sub(
                r'(I want\s+[^,]+)',
                r'\1 quickly, easily, and in a highly user-friendly manner',
                text,
                count=1,
                flags=re.IGNORECASE
            )
            if text_p == text:
                text_p = text.replace("so that", "quickly and easily, so that")

        return text_p, labels

    @staticmethod
    def perturb_small(story_a: Dict[str, Any], story_b: Dict[str, Any], lang: str) -> Tuple[str, Dict[str, int]]:
        labels = {"I": 1, "N": 1, "V": 1, "E": 1, "S": 0, "T": 1}
        text_a = story_a["text"]
        text_b = story_b["text"]

        if lang == "id":
            # Ekstrak bagian aksi story B
            match_b = re.search(r'saya ingin\s+([^,]+)', text_b, re.IGNORECASE)
            action_b = match_b.group(1).strip() if match_b else "mengelola seluruh konfigurasi server"
            
            # Sisipkan ke story A sebagai aksi majemuk (Epic)
            text_p = re.sub(
                r'(saya ingin\s+[^,]+)',
                rf'\1 dan juga {action_b} serta sekaligus menyinkronkan seluruh database',
                text_a,
                count=1,
                flags=re.IGNORECASE
            )
        else:
            match_b = re.search(r'I want\s+([^,]+)', text_b, re.IGNORECASE)
            action_b = match_b.group(1).strip() if match_b else "manage all background server configurations"
            
            text_p = re.sub(
                r'(I want\s+[^,]+)',
                rf'\1 and also {action_b} as well as sync all enterprise databases',
                text_a,
                count=1,
                flags=re.IGNORECASE
            )

        return text_p, labels

    @staticmethod
    def perturb_valuable(story: Dict[str, Any], lang: str) -> Tuple[str, Dict[str, int]]:
        labels = {"I": 1, "N": 1, "V": 0, "E": 1, "S": 1, "T": 1}
        text = story["text"]

        if lang == "id":
            # Hapus klausa sehingga / agar
            text_p = re.split(r',\s*(sehingga|agar|supaya)\b', text, flags=re.IGNORECASE)[0].strip()
            if not text_p.endswith('.'):
                text_p += '.'
        else:
            text_p = re.split(r',\s*(so that|in order to)\b', text, flags=re.IGNORECASE)[0].strip()
            if not text_p.endswith('.'):
                text_p += '.'

        return text_p, labels

    @staticmethod
    def perturb_negotiable(story: Dict[str, Any], lang: str) -> Tuple[str, Dict[str, int]]:
        labels = {"I": 1, "N": 0, "V": 1, "E": 1, "S": 1, "T": 1}
        text = story["text"]

        if lang == "id":
            injection = " dengan mengklik tombol biru 120x40px berlabel 'SUBMIT' berfont Arial 11pt yang mengeksekusi SQL INSERT ke tabel orders_v2"
            text_p = re.sub(
                r'(saya ingin\s+[^,]+)',
                rf'\1{injection}',
                text,
                count=1,
                flags=re.IGNORECASE
            )
        else:
            injection = " by clicking a 120x40px blue button labeled 'SUBMIT' with Arial 11pt font that executes an SQL INSERT into orders_v2 table"
            text_p = re.sub(
                r'(I want\s+[^,]+)',
                rf'\1{injection}',
                text,
                count=1,
                flags=re.IGNORECASE
            )

        return text_p, labels

    @staticmethod
    def perturb_estimable(story: Dict[str, Any], lang: str) -> Tuple[str, Dict[str, int]]:
        labels = {"I": 1, "N": 1, "V": 1, "E": 0, "S": 1, "T": 1}
        text = story["text"]

        if lang == "id":
            injection = " beberapa data transaksi yang banyak dan berbagai macam metrik statistik lainnya dll"
            text_p = re.sub(
                r'(saya ingin\s+[^,]+)',
                rf'\1 serta memuat{injection}',
                text,
                count=1,
                flags=re.IGNORECASE
            )
        else:
            injection = " some various transaction metrics, several data items, and many open-ended options etc"
            text_p = re.sub(
                r'(I want\s+[^,]+)',
                rf'\1 including{injection}',
                text,
                count=1,
                flags=re.IGNORECASE
            )

        return text_p, labels

    @staticmethod
    def perturb_independent(story: Dict[str, Any], lang: str, dep_ticket_id: str = "US-104") -> Tuple[str, Dict[str, int]]:
        labels = {"I": 0, "N": 1, "V": 1, "E": 1, "S": 1, "T": 1}
        text = story["text"]

        if lang == "id":
            prefix = f"Hanya setelah User Story #{dep_ticket_id} selesai dikerjakan, "
            # Lowercase first letter of original story
            text_p = prefix + text[0].lower() + text[1:]
        else:
            prefix = f"Only after User Story {dep_ticket_id} is completed and deployed, "
            text_p = prefix + text[0].lower() + text[1:]

        return text_p, labels
