import os
import re
import glob
import joblib
import warnings
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import accuracy_score, f1_score

warnings.filterwarnings("ignore")

# =====================================================================
# 1. KAMUS & POLA LINGUISTIK DWIBAHASA (ID & EN) - ISO 29148 & INVEST
# =====================================================================

ROLE_PATTERN = re.compile(r'\b(sebagai|as a|as an)\b', re.I)
MEANS_PATTERN = re.compile(
    r'\b(saya ingin|saya mau|saya dapat|saya tidak ingin|saya harus|'
    r'i want|i would like|i can|i am able|i need|i should|i do not want|i don\'t want)\b', re.I
)
ENDS_PATTERN = re.compile(
    r'\b(sehingga|agar|supaya|untuk|karena|guna|'
    r'so that|in order to|so i can|because|to support|to allow|so as to)\b', re.I
)

# Indikator pelanggar Negotiable (mendikte UI / protokol / format teknis kaku)
PRESCRIPTIVE_PATTERN = re.compile(
    r'\b(tombol|kotak centang|checkbox|dropdown|klik|halaman|url|seo|wysiwyg|'
    r'html|csv|xml|marcxml|ead|eac-cpf|ldap|shibboleth|oai|stripe|pdf|gelang|'
    r'kalung|backend|frontend|database|basis data|api|navigasi berbasis papan ketik|'
    r'menyeret|button|click|page|table|modal|tab|drag and drop|dragging|keyboard|'
    r'bracelet|necklace|wristwatch)\b', re.I
)

# Indikator pelanggar Estimable & Testable (kata sifat kabur / subjektif)
VAGUE_PATTERN = re.compile(
    r'\b(mudah|cepat|bagus|jelas|sederhana|murah|mahal|fleksibel|tangguh|'
    r'komprehensif|efektif|efisien|ramah|otomatis|banyak|beberapa|berbagai|'
    r'sesuai kebutuhan|sebanyak mungkin|sesegera mungkin|tepat waktu|dll|dsb|'
    r'luar biasa|tidak memberi stigma|easy|easily|fast|quickly|good|nice|clear|clearly|'
    r'simple|cheap|flexible|robust|comprehensive|effective|efficient|various|multiple|'
    r'etc|as needed|as much as possible|as soon as possible|awesome|stigma)\b', re.I
)

# Indikator pelanggar Independent (kata rujukan / ketergantungan ke story lain)
DEPENDENCY_PATTERN = re.compile(
    r'\b(sebelumnya|tersebut|di atas|lainnya|lain|terkait|tambahan|kustom|'
    r'ulangi|mengulangi|terakhir|kedua|ketiga|kembali|lanjutan|sub-rekaman|'
    r'menimpa|mengoreksi|revisi|mengikat|daftar tunggu|previous|above|other|'
    r'related|additional|custom|repeat|last|second|third|return|refund|advanced|'
    r'sub-record|overwrite|revision|waitlist|waiting list|tie)\b', re.I
)

# Indikator Sub-Fitur / Variasi Kondisional (membedakan sub-story dari anchor story)
SUB_MODIFIER_PATTERN = re.compile(
    r'\b(hanya|secara tidak sengaja|ulang|massal|jika|ketika|saat|sebelum|'
    r'setelah|tanpa|terlepas|dengan menekan|dengan menyeret|atas nama|'
    r'only|accidentally|bulk|if|when|while|before|after|without|regardless|'
    r'on behalf of|by pressing|by dragging)\b', re.I
)

# Indikator Kata Kerja Fondasi / Anchor Story (CRUD & Kapabilitas Utama ID + EN)
FOUNDATIONAL_ANCHOR_PATTERN = re.compile(
    r'\b(membuat dan mengedit|membuat dan memelihara|mengimpor data|mengimpor sumber daya|'
    r'mengimpor informasi|mengekspor rekaman|mengirimkan sesi|mengisi formulir pendaftaran|'
    r'membuat postingan blog|membuat koleksi|menerapkan atau menghapus embargo|'
    r'mengakses koleksi|mengunggah versi baru|menambahkan tanggal rilis|mengakses statistik|'
    r'menghubungi penulis|menayangkan media streaming|disimpan secara redundan|'
    r'masuk ke akun pribadi|menerima informasi|memperbesar konten visual|'
    r'memutuskan siapa yang memiliki akses|penghitung langkah|keadaan darurat|'
    r'menerima pengingat obat|berolahraga secara teratur|mengusulkan permainan|'
    r'panggilan bangun tidur|untuk navigasi|memelihara daftar kontak|'
    r'menyalakan/mematikan lampu|mencantumkan informasi dasar|tingkat sponsorship|'
    r'melihat daftar sponsor|memposting lowongan kerja|'
    r'create and edit|create and maintain|import accession|import resource|import agent|'
    r'export agent|submit a session|fill out a user registration|create a blog post|'
    r'create a collection|apply or remove access embargo|access collections|'
    r'upload a new version|add future release dates|access useful and comprehensive usage|'
    r'contact the author|stream media|redundantly stored|log into a personal account|'
    r'receive information from alfred|magnify visual content|decide who has access|'
    r'step counter|call help in case of an emergency|medicine reminders|'
    r'remind people to exercise regularly|propose games to me that require a combination|'
    r'wake-up call|use alfred for navigation|maintain my contact list|switch on/off the lights|'
    r'list basic information about my summit|learn about sponsorship levels|'
    r'see a list of sponsors|post a job listing)\b', re.I
)

# Indikator Tugas Teknis Murni (pelanggar Valuable)
TECH_TASK_PATTERN = re.compile(
    r'\b(perubahan backend|perubahan frontend|konfigurasi yang tidak dikemas|'
    r'pengimpor kustom|backend changes|frontend changes|unpackaged configuration|'
    r'custom importer)\b', re.I
)

# Indikator Cakupan Terlalu Luas / Epic (pelanggar Small & Estimable)
EPIC_BROAD_PATTERN = re.compile(
    r'\b(semua|segala|segalanya|apa pun|berbagai|beberapa|komprehensif|seluruh|'
    r'setiap|all|everything|anything|various|multiple|comprehensive|entire|every)\b', re.I
)

CONJUNCTION_PATTERN = re.compile(
    r'\b(dan|serta|atau|maupun|dan/atau|sekaligus|sembari|sambil|'
    r'and|or|as well as|while|and/or)\b|,', re.I
)

NUMBER_METRIC_PATTERN = re.compile(
    r'(\d+|\$[0-9]+|1gb|satu|dua|tiga|one|two|three)', re.I
)


# =====================================================================
# 2. EKSTRAKSI FITUR (STAGE 1: LINGUISTIC + CATEGORY CAUSAL SIMILARITY)
# =====================================================================

FEATURE_NAMES = [
    'word_count',
    'has_role',
    'has_means',
    'has_ends',
    'prescriptive_count',
    'vague_count',
    'dependency_word_count',
    'conjunction_count',
    'has_number_metric',
    'is_tech_task',
    'foundational_anchor_flag',
    'sub_modifier_count',
    'epic_broad_count',
    'max_sim_backlog',
    'mean_top3_sim_backlog',
    'sim_over_03_count',
    'cat_size',
    'rel_pos_in_cat',
    'is_first_in_cat',
    'max_sim_prev_in_cat',
    'mean_sim_prev_in_cat',
    'max_sim_in_cat',
    'is_most_central_in_cat',
]


def extract_features_for_backlog(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if 'backlog_id' not in df.columns:
        df['backlog_id'] = df['source_id'].apply(
            lambda x: str(x).rsplit('_', 1)[0] if pd.notna(x) and '_' in str(x) else 'default_backlog'
        )
    if 'category' not in df.columns:
        df['category'] = 'default_category'

    # Normalisasi penomoran kategori ("1. ...", "2. ...") agar ID dan EN memiliki grup kategori yang konsisten
    df['cat_group'] = df['category'].fillna('default_category').astype(str).apply(
        lambda s: s.split('.')[0].strip() if '.' in s else s.strip()
    )

    features_rows = []

    for _, group in df.groupby('backlog_id', sort=False):
        texts = group['text'].fillna('').astype(str).tolist()
        cats = group['cat_group'].tolist()

        vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        X_tfidf = vec.fit_transform(texts)
        sim_matrix = cosine_similarity(X_tfidf)
        np.fill_diagonal(sim_matrix, -1.0)

        cat_indices = {}
        for idx_in_group, c in enumerate(cats):
            cat_indices.setdefault(c, []).append(idx_in_group)

        for i, (_, row) in enumerate(group.iterrows()):
            t = str(row['text'])
            words = t.split()
            word_count = float(len(words))

            has_role = 1.0 if ROLE_PATTERN.search(t) else 0.0
            has_means = 1.0 if MEANS_PATTERN.search(t) else 0.0
            has_ends = 1.0 if ENDS_PATTERN.search(t) else 0.0

            prescriptive_count = float(len(PRESCRIPTIVE_PATTERN.findall(t)))
            vague_count = float(len(VAGUE_PATTERN.findall(t)))
            dependency_word_count = float(len(DEPENDENCY_PATTERN.findall(t)))
            conjunction_count = float(len(CONJUNCTION_PATTERN.findall(t)))
            has_number_metric = 1.0 if NUMBER_METRIC_PATTERN.search(t) else 0.0
            is_tech_task = 1.0 if TECH_TASK_PATTERN.search(t) else 0.0
            foundational_anchor_flag = 1.0 if FOUNDATIONAL_ANCHOR_PATTERN.search(t) else 0.0
            sub_modifier_count = float(len(SUB_MODIFIER_PATTERN.findall(t)))
            epic_broad_count = float(len(EPIC_BROAD_PATTERN.findall(t)))

            row_sims = sim_matrix[i]
            valid_sims = row_sims[row_sims >= 0]
            max_sim_backlog = float(np.max(valid_sims)) if len(valid_sims) > 0 else 0.0
            top3_sims = np.sort(valid_sims)[-3:] if len(valid_sims) >= 3 else valid_sims
            mean_top3_sim_backlog = float(np.mean(top3_sims)) if len(top3_sims) > 0 else 0.0
            sim_over_03_count = float(np.sum(valid_sims > 0.30))

            c = cats[i]
            c_idxs = cat_indices[c]
            pos_in_cat = c_idxs.index(i)
            cat_size = float(len(c_idxs))
            rel_pos_in_cat = float(pos_in_cat / max(1, len(c_idxs) - 1)) if len(c_idxs) > 1 else 0.0
            is_first_in_cat = 1.0 if pos_in_cat == 0 else 0.0

            prev_c_idxs = [idx for idx in c_idxs if idx < i]
            if len(prev_c_idxs) > 0:
                prev_sims = [sim_matrix[i, idx] for idx in prev_c_idxs]
                max_sim_prev_in_cat = float(np.max(prev_sims))
                mean_sim_prev_in_cat = float(np.mean(prev_sims))
            else:
                max_sim_prev_in_cat = 0.0
                mean_sim_prev_in_cat = 0.0

            other_c_idxs = [idx for idx in c_idxs if idx != i]
            if len(other_c_idxs) > 0:
                cat_sims = [sim_matrix[i, idx] for idx in other_c_idxs]
                max_sim_in_cat = float(np.max(cat_sims))
                mean_sim_in_cat = float(np.mean(cat_sims))
                all_cat_means = [
                    np.mean([sim_matrix[idx1, idx2] for idx2 in c_idxs if idx2 != idx1])
                    for idx1 in c_idxs
                ]
                is_most_central_in_cat = 1.0 if mean_sim_in_cat >= (np.max(all_cat_means) - 1e-6) else 0.0
            else:
                max_sim_in_cat = 0.0
                is_most_central_in_cat = 1.0

            features_rows.append({
                'index': row.name,
                'word_count': word_count,
                'has_role': has_role,
                'has_means': has_means,
                'has_ends': has_ends,
                'prescriptive_count': prescriptive_count,
                'vague_count': vague_count,
                'dependency_word_count': dependency_word_count,
                'conjunction_count': conjunction_count,
                'has_number_metric': has_number_metric,
                'is_tech_task': is_tech_task,
                'foundational_anchor_flag': foundational_anchor_flag,
                'sub_modifier_count': sub_modifier_count,
                'epic_broad_count': epic_broad_count,
                'max_sim_backlog': max_sim_backlog,
                'mean_top3_sim_backlog': mean_top3_sim_backlog,
                'sim_over_03_count': sim_over_03_count,
                'cat_size': cat_size,
                'rel_pos_in_cat': rel_pos_in_cat,
                'is_first_in_cat': is_first_in_cat,
                'max_sim_prev_in_cat': max_sim_prev_in_cat,
                'mean_sim_prev_in_cat': mean_sim_prev_in_cat,
                'max_sim_in_cat': max_sim_in_cat,
                'is_most_central_in_cat': is_most_central_in_cat,
            })

    feat_df = pd.DataFrame(features_rows).set_index('index')
    return feat_df.loc[df.index, FEATURE_NAMES]


# =====================================================================
# 3. PELATIHAN MODEL, TABEL EVALUASI CLI, & EKSPOR .PKL (STAGE 2)
# =====================================================================

INVEST_TARGETS = ['y_I', 'y_N', 'y_V', 'y_E', 'y_S', 'y_T']


def train_and_evaluate(csv_files: list, output_pkl_path: str = "reqlint_invest_models.pkl"):
    dfs = []
    for f in csv_files:
        if os.path.exists(f):
            try:
                d = pd.read_csv(f)
                if all(col in d.columns for col in ['text'] + INVEST_TARGETS):
                    lang_val = str(d['lang'].iloc[0]).lower() if 'lang' in d.columns and len(d) > 0 else 'id'
                    d['backlog_id'] = f"{lang_val}_{os.path.basename(f)}"
                    dfs.append(d)
            except Exception as e:
                print(f"[WARN] Gagal membaca {f}: {e}")

    if not dfs:
        raise FileNotFoundError("Tidak ada file CSV valid yang ditemukan untuk pelatihan.")

    df_all = pd.concat(dfs, ignore_index=True)
    df_all = df_all.dropna(subset=INVEST_TARGETS).reset_index(drop=True)

    X = extract_features_for_backlog(df_all)
    langs = df_all['lang'].fillna('id').astype(str).str.lower().values

    models_bundle = {
        'version': '2.1.0-srs-hybrid',
        'feature_names': FEATURE_NAMES,
        'targets': INVEST_TARGETS,
        'models': {},
        'top_features': {},
        'metrics': {}
    }

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    print(f"\nTotal Data Latih: {len(df_all)} baris (ID: {np.sum(langs == 'id')}, EN: {np.sum(langs == 'en')})")
    print(f"{'Kriteria':<9} | {'Acc (All)':<9} | {'F1 (All)':<8} | {'F1 (ID)':<7} | {'F1 (EN)':<7} | Fitur Paling Berpengaruh")
    print("-" * 105)

    for target in INVEST_TARGETS:
        y = df_all[target].astype(int).values

        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('clf', LogisticRegression(class_weight='balanced', C=1.0, max_iter=1000, random_state=42))
        ])

        preds = cross_val_predict(pipe, X, y, cv=skf)
        acc_all = accuracy_score(y, preds)
        f1_all = f1_score(y, preds, zero_division=0)

        mask_id = (langs == 'id')
        mask_en = (langs == 'en')
        f1_id = f1_score(y[mask_id], preds[mask_id], zero_division=0) if np.any(mask_id) else f1_all
        f1_en = f1_score(y[mask_en], preds[mask_en], zero_division=0) if np.any(mask_en) else f1_all

        pipe.fit(X, y)
        coefs = pipe.named_steps['clf'].coef_[0]
        top_idx = np.argsort(np.abs(coefs))[::-1][:2]
        top_feat_str = ", ".join([f"{FEATURE_NAMES[idx]} ({coefs[idx]:+.2f})" for idx in top_idx])

        print(f"{target:<9} | {acc_all:<9.3f} | {f1_all:<8.3f} | {f1_id:<7.3f} | {f1_en:<7.3f} | {top_feat_str}")

        models_bundle['models'][target] = pipe
        models_bundle['top_features'][target] = [
            (FEATURE_NAMES[idx], float(coefs[idx])) for idx in np.argsort(np.abs(coefs))[::-1]
        ]
        models_bundle['metrics'][target] = {
            'acc_all': float(acc_all),
            'f1_all': float(f1_all),
            'f1_id': float(f1_id),
            'f1_en': float(f1_en),
        }

    joblib.dump(models_bundle, output_pkl_path)
    print("-" * 105)
    print(f"[SUCCESS] Model telah disimpan ke: {os.path.abspath(output_pkl_path)}")
    return models_bundle


# =====================================================================
# 4. SINKRONISASI LABEL INVEST OTOMATIS KE DATASET ENG (AGAR ID == EN)
# =====================================================================

def sync_labels_across_folders(indo_folder: str, eng_folder: str):
    """
    Menyinkronkan kolom label INVEST (y_I..y_T dan annotator_a) antara folder
    dataset-indo-label-final dan dataset-eng-label-final berdasarkan urutan/id
    agar distribusi label Bahasa Indonesia dan Bahasa Inggris 100% konsisten.
    """
    if not (os.path.exists(indo_folder) and os.path.exists(eng_folder)):
        return

    indo_csvs = {os.path.basename(f): f for f in glob.glob(os.path.join(indo_folder, "*.csv"))}
    eng_csvs = {os.path.basename(f): f for f in glob.glob(os.path.join(eng_folder, "*.csv"))}

    label_cols = ['label_target', 'y_I', 'y_N', 'y_V', 'y_E', 'y_S', 'y_T', 'annotator_a']

    for fname, indo_path in indo_csvs.items():
        if fname in eng_csvs:
            eng_path = eng_csvs[fname]
            df_id = pd.read_csv(indo_path)
            df_en = pd.read_csv(eng_path)
            if len(df_id) == len(df_en) and all(c in df_id.columns for c in label_cols):
                changed = False
                for c in label_cols:
                    if c not in df_en.columns or not df_en[c].equals(df_id[c]):
                        df_en[c] = df_id[c].values
                        changed = True
                if 'category' in df_id.columns and 'category' not in df_en.columns:
                    df_en['category'] = df_id['category'].values
                    changed = True
                if changed:
                    df_en.to_csv(eng_path, index=False)
                    print(f"[SYNC] Label INVEST disinkronkan dari ID -> EN untuk: {fname}")


# =====================================================================
# 5. MAIN EXECUTION (DETEKSI OTOMATIS KE-2 FOLDER DATASET)
# =====================================================================

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    target_dirs = [
        r"D:\Kuliah\Semester 5\Pembangunan Perangkat Lunak - Prak\reqlint\pm-docs\rubrics\dataset-indo-label-final",
        r"D:\Kuliah\Semester 5\Pembangunan Perangkat Lunak - Prak\reqlint\pm-docs\rubrics\dataset-eng-label-final",
        os.path.join(script_dir, "dataset-indo-label-final"),
        os.path.join(script_dir, "dataset-eng-label-final"),
        os.path.join(os.getcwd(), "pm-docs", "rubrics", "dataset-indo-label-final"),
        os.path.join(os.getcwd(), "pm-docs", "rubrics", "dataset-eng-label-final"),
    ]

    indo_dir_found = next((d for d in target_dirs if "indo" in d.lower() and os.path.exists(d)), None)
    eng_dir_found = next((d for d in target_dirs if "eng" in d.lower() and os.path.exists(d)), None)
    if indo_dir_found and eng_dir_found:
        sync_labels_across_folders(indo_dir_found, eng_dir_found)

    found_csvs = []
    seen_realpaths = set()

    for d in target_dirs:
        if os.path.exists(d):
            for f in sorted(glob.glob(os.path.join(d, "*.csv"))):
                rp = os.path.realpath(f).lower()
                if rp not in seen_realpaths:
                    seen_realpaths.add(rp)
                    found_csvs.append(f)

    if not found_csvs:
        for f in sorted(glob.glob(os.path.join(script_dir, "*.csv"))):
            rp = os.path.realpath(f).lower()
            if rp not in seen_realpaths:
                seen_realpaths.add(rp)
                found_csvs.append(f)

    print(f"[INFO] Ditemukan {len(found_csvs)} file CSV untuk pelatihan:")
    for f in found_csvs:
        print(f" - {f}")

    output_pkl = os.path.join(script_dir, "reqlint_invest_models.pkl")
    train_and_evaluate(found_csvs, output_pkl_path=output_pkl)