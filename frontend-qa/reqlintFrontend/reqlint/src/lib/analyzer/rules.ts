import type { Category, Language } from './types';

/**
 * Aturan deteksi berbasis kamus + regex (rule-based, deterministik).
 * Menambah aturan baru cukup menambah entri pada array di bawah.
 */
export interface TermRule {
  id: string;
  lang: Language;
  category: Category;
  pattern: RegExp;
  recommendation: string;
  /** Pengganti otomatis untuk draf revisi (nilai contoh, perlu disesuaikan tim). */
  replacement?: string;
}

/** Bungkus alternasi dengan batas kata yang aman untuk huruf Unicode dan tanda hubung. */
const word = (source: string): RegExp =>
  new RegExp(`(?<![\\p{L}\\p{N}_-])(?:${source})(?![\\p{L}\\p{N}_-])`, 'giu');

export const TERM_RULES: TermRule[] = [
  // ───────────── Bahasa Indonesia ─────────────
  {
    id: 'id.latency',
    lang: 'id',
    category: 'ambiguity',
    pattern: word('sangat\\s+cepat|secepat\\s+mungkin|cepat|kilat'),
    recommendation: 'Kata tidak terukur. Tentukan parameter latensi spesifik (misal < 2 detik).',
    replacement: 'dalam waktu kurang dari 2 detik',
  },
  {
    id: 'id.quantity',
    lang: 'id',
    category: 'ambiguity',
    pattern: word('banyak|beberapa|sejumlah|sebagian\\s+besar|sebagian\\s+kecil|sedikit'),
    recommendation: 'Jumlah tidak jelas. Sebutkan angka atau rentang yang terukur.',
  },
  {
    id: 'id.deadline',
    lang: 'id',
    category: 'ambiguity',
    pattern: word('secepatnya|segera|sesegera\\s+mungkin|sebisa\\s+mungkin|sebanyak\\s+mungkin'),
    recommendation: 'Batas waktu atau jumlah tidak jelas. Tentukan tenggat atau target numerik.',
  },
  {
    id: 'id.vague-condition',
    lang: 'id',
    category: 'ambiguity',
    pattern: word(
      'jika\\s+perlu|bila\\s+perlu|seperlunya|yang\\s+sesuai|yang\\s+tepat|sebagaimana\\s+mestinya|memadai|secukupnya',
    ),
    recommendation: 'Kondisi tidak jelas. Definisikan kriteria atau aturan yang eksplisit.',
  },
  {
    id: 'id.relative-adjective',
    lang: 'id',
    category: 'ambiguity',
    pattern: word('optimal|efisien|fleksibel|handal|andal|stabil|ringan|aman|besar|kecil|tinggi|rendah|canggih'),
    recommendation: 'Istilah relatif. Ganti dengan metrik atau ambang batas yang dapat diukur.',
  },
  {
    id: 'id.usability',
    lang: 'id',
    category: 'non-testable',
    pattern: word(
      'user[\\s-]?friendly|ramah\\s+pengguna|mudah\\s+(?:digunakan|dipakai|dioperasikan|dipahami)|mudah|intuitif|nyaman',
    ),
    recommendation: 'Kata bersifat subjektif. Ganti dengan kriteria UI/UX spesifik.',
    replacement: 'memerlukan maksimal 3 langkah',
  },
  {
    id: 'id.subjective',
    lang: 'id',
    category: 'non-testable',
    pattern: word('menarik|modern|elegan|simpel|sederhana|bagus|dengan\\s+baik|mulus|seamless'),
    recommendation: 'Kata bersifat subjektif. Ganti dengan kriteria yang dapat diverifikasi.',
  },
  {
    id: 'id.weak',
    lang: 'id',
    category: 'weak-directive',
    pattern: word(
      'sebaiknya|seharusnya|diharapkan|mungkin|barangkali|kira-kira|sekiranya|idealnya|bisa\\s+jadi|kalau\\s+bisa|jika\\s+memungkinkan|bila\\s+memungkinkan|sebisanya',
    ),
    recommendation: "Direktif lemah. Gunakan 'harus' atau 'wajib' untuk kebutuhan yang mengikat.",
  },
  {
    id: 'id.open-list',
    lang: 'id',
    category: 'incomplete',
    pattern: word('dll|dsb|dst|dan\\s+lain-lain|dan\\s+sebagainya|dan\\s+seterusnya|tbd|tbc'),
    recommendation: 'Daftar tidak lengkap. Sebutkan seluruh item secara eksplisit.',
  },

  // ───────────── English ─────────────
  {
    id: 'en.latency',
    lang: 'en',
    category: 'ambiguity',
    pattern: word('as\\s+quickly\\s+as\\s+possible|quickly|rapidly|fast|slow|quick'),
    recommendation: 'Unmeasurable. Specify a concrete latency target (e.g. < 2 seconds).',
    replacement: 'within 2 seconds',
  },
  {
    id: 'en.quantity',
    lang: 'en',
    category: 'ambiguity',
    pattern: word('many|several|some|a\\s+few|a\\s+lot\\s+of|most|numerous'),
    recommendation: 'Vague quantity. State a number or measurable range.',
  },
  {
    id: 'en.deadline',
    lang: 'en',
    category: 'ambiguity',
    pattern: word('asap|as\\s+soon\\s+as\\s+possible|as\\s+needed|if\\s+necessary|as\\s+appropriate|and/or|appropriate|adequate|sufficient'),
    recommendation: 'Unclear condition or deadline. Define explicit criteria or a target date.',
  },
  {
    id: 'en.relative-adjective',
    lang: 'en',
    category: 'ambiguity',
    pattern: word('optimal|efficient|flexible|robust|stable|lightweight|secure|large|small|high|low'),
    recommendation: 'Relative term. Replace with a metric or threshold that can be measured.',
  },
  {
    id: 'en.usability',
    lang: 'en',
    category: 'non-testable',
    pattern: word('user[\\s-]?friendly|easy\\s+to\\s+use|easy|intuitive|comfortable'),
    recommendation: 'Subjective wording. Replace with specific UI/UX criteria.',
    replacement: 'completable in at most 3 steps',
  },
  {
    id: 'en.subjective',
    lang: 'en',
    category: 'non-testable',
    pattern: word('attractive|modern|elegant|simple|nice|good|better|beautiful|seamless|smooth'),
    recommendation: 'Subjective wording. Replace with criteria that can be verified.',
  },
  {
    id: 'en.weak',
    lang: 'en',
    category: 'weak-directive',
    pattern: word('should|may|might|could|ideally|preferably|if\\s+possible|if\\s+feasible|probably'),
    recommendation: "Weak directive. Use 'shall' or 'must' for binding requirements.",
  },
  {
    id: 'en.open-list',
    lang: 'en',
    category: 'incomplete',
    pattern: word('etc|and\\s+so\\s+on|and\\s+so\\s+forth|tbd|tbc'),
    recommendation: 'Open-ended list. List every item explicitly.',
  },
];

export function rulesFor(lang: Language): TermRule[] {
  return TERM_RULES.filter((r) => r.lang === lang);
}

// ───────────── Kalimat pasif ─────────────

export const PASSIVE_RECOMMENDATION: Record<Language, string> = {
  id: 'Ubah ke bentuk aktif dengan subjek dan tindakan yang jelas.',
  en: 'Rewrite in active voice with a clear actor and action.',
};

/** Kata berawalan "di-" yang bukan kata kerja pasif. */
export const ID_NON_PASSIVE = new Set([
  'dimana', 'diri', 'dibawah', 'diatas', 'disini', 'disana', 'disitu', 'didalam', 'diluar',
  'diagram', 'dialog', 'digital', 'dimensi', 'direktori', 'direktur', 'disiplin', 'diskon',
  'diskusi', 'distribusi', 'dinamis', 'dinamika', 'dinas', 'display', 'disk', 'divisi', 'diet',
]);

const MODAL_ID = 'harus|wajib|perlu|akan|dapat|bisa|boleh|sudah|telah|sedang';

/** Modal + kata kerja "di-": "harus disimpan". Grup 1 = kata kerja. */
export const ID_PASSIVE_MODAL = new RegExp(
  `(?<![\\p{L}\\p{N}_-])(?:${MODAL_ID})\\s+(di[a-z]{3,})(?![\\p{L}\\p{N}_-])`,
  'giu',
);
/** Kata kerja "di-" + "oleh": "disimpan oleh". Grup 1 = kata kerja. */
export const ID_PASSIVE_OLEH = new RegExp(
  '(?<![\\p{L}\\p{N}_-])(di[a-z]{3,})\\s+oleh(?![\\p{L}\\p{N}_-])',
  'giu',
);
export const EN_PASSIVE = new RegExp(
  '(?<![\\p{L}\\p{N}_-])(?:(?:will|shall|must|should|can|may|could|would)\\s+be|is|are|was|were|been|being)\\s+(?:\\w+ly\\s+)?(?:\\w{3,}ed|built|made|done|stored|kept|sent|shown|given|held|written|seen|taken|known|chosen)(?![\\p{L}\\p{N}_-])',
  'giu',
);

// ───────────── Struktur user story ─────────────

export const STORY = {
  id: {
    start: /^sebagai\b/i,
    role: /^sebagai\s+(?:seorang\s+)?[^,]{2,}/i,
    goal: /\bsaya\s+(?:ingin|mau|perlu|butuh)\b/i,
    benefit: /\b(?:agar|supaya|sehingga|untuk\s+dapat|guna)\b/i,
    parse:
      /^sebagai\s+(?:seorang\s+)?(?<role>[^,]+?),?\s+saya\s+(?:ingin|mau|perlu|butuh)\s+(?<goal>.+?)(?:\s+(?:agar|supaya|sehingga)\s+(?<benefit>.+?))?\s*[.!?]*$/i,
  },
  en: {
    start: /^as\s+an?\b/i,
    role: /^as\s+an?\s+[^,]{2,}/i,
    goal: /\bi\s+(?:want|need|would\s+like)\b/i,
    benefit: /\b(?:so\s+that|in\s+order\s+to|so\s+i\s+can)\b/i,
    parse:
      /^as\s+an?\s+(?<role>[^,]+?),?\s+i\s+(?:want|need|would\s+like)(?:\s+to)?\s+(?<goal>.+?)(?:\s+(?:so\s+that|in\s+order\s+to)\s+(?<benefit>.+?))?\s*[.!?]*$/i,
  },
} as const;

export const DEPENDENCY: Record<Language, RegExp> = {
  id: /\b(?:bergantung\s+pada|tergantung\s+(?:pada\s+)?|menunggu\s+(?:fitur|modul)|setelah\s+.+?\s+selesai)/i,
  en: /\b(?:depends?\s+on|dependent\s+on|blocked\s+by|after\s+.+?\s+(?:is|are)\s+(?:complete|done|finished))/i,
};

export const TECH_LOCK: RegExp =
  /\b(?:menggunakan|memakai|using|built\s+with|must\s+use)\s+(?:react|angular|vue|mysql|postgres(?:ql)?|mongodb|oracle|java|python|php|aws|azure|firebase)\b/i;
