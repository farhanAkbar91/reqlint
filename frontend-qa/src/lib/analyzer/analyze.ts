import { countWords, splitClauses } from './clauses';
import {
  DEPENDENCY,
  EN_PASSIVE,
  ID_NON_PASSIVE,
  ID_PASSIVE_MODAL,
  ID_PASSIVE_OLEH,
  PASSIVE_RECOMMENDATION,
  STORY,
  TECH_LOCK,
  rulesFor,
} from './rules';
import {
  CATEGORIES,
  type AnalysisResult,
  type Category,
  type Clause,
  type Finding,
  type Grade,
  type InvestCheck,
  type Language,
} from './types';

/** Bobot pengurang skor per temuan. Total 100 - (jumlah bobot / faktor panjang teks). */
export const PENALTY: Record<Category, number> = {
  ambiguity: 14,
  'non-testable': 16,
  incomplete: 18,
  'weak-directive': 10,
  'passive-voice': 12,
};

type RawFinding = Omit<Finding, 'id'>;

function pushMatches(
  out: RawFinding[],
  clause: Clause,
  regex: RegExp,
  base: Pick<RawFinding, 'ruleId' | 'category' | 'recommendation'>,
  accept: (match: RegExpMatchArray) => boolean = () => true,
) {
  for (const m of clause.text.matchAll(regex)) {
    if (m.index === undefined || !accept(m)) continue;
    out.push({
      ...base,
      clause: clause.index,
      term: m[0],
      start: clause.start + m.index,
      end: clause.start + m.index + m[0].length,
    });
  }
}

function structureFindings(clause: Clause, lang: Language): RawFinding[] {
  const out: RawFinding[] = [];
  const s = STORY[lang];
  const wordsInClause = countWords(clause.text);
  const msg =
    lang === 'id'
      ? {
          role: 'Peran pengguna tidak jelas. Tulis dengan format "Sebagai <peran>, ...".',
          goal: 'Tujuan tidak ada. Tambahkan "saya ingin <aksi>".',
          benefit: 'Manfaat tidak ada. Tambahkan "agar <alasan/nilai bisnis>".',
          short: 'Klausul terlalu pendek untuk diverifikasi. Lengkapi subjek, tindakan, dan tujuan.',
        }
      : {
          role: 'User role is unclear. Use the form "As a <role>, ...".',
          goal: 'Goal is missing. Add "I want <action>".',
          benefit: 'Benefit is missing. Add "so that <reason/business value>".',
          short: 'Clause is too short to verify. Add an actor, an action and a purpose.',
        };

  const point = (ruleId: string, recommendation: string, term = '—'): RawFinding => ({
    ruleId,
    category: 'incomplete',
    recommendation,
    clause: clause.index,
    term,
    start: clause.start,
    end: clause.end,
  });

  if (s.start.test(clause.text)) {
    if (!s.role.test(clause.text)) out.push(point('story.role', msg.role));
    if (!s.goal.test(clause.text)) out.push(point('story.goal', msg.goal));
    if (!s.benefit.test(clause.text)) out.push(point('story.benefit', msg.benefit));
  } else if (wordsInClause < 4) {
    out.push(point('clause.short', msg.short));
  }
  return out;
}

export function findingsFor(clauses: Clause[], lang: Language): Finding[] {
  const raw: RawFinding[] = [];

  for (const clause of clauses) {
    for (const rule of rulesFor(lang)) {
      pushMatches(raw, clause, rule.pattern, {
        ruleId: rule.id,
        category: rule.category,
        recommendation: rule.recommendation,
      });
    }

    const passive = {
      category: 'passive-voice' as const,
      recommendation: PASSIVE_RECOMMENDATION[lang],
    };
    if (lang === 'id') {
      const acceptVerb = (m: RegExpMatchArray) => !ID_NON_PASSIVE.has(m[1].toLowerCase());
      pushMatches(raw, clause, ID_PASSIVE_MODAL, { ruleId: 'id.passive.modal', ...passive }, acceptVerb);
      pushMatches(raw, clause, ID_PASSIVE_OLEH, { ruleId: 'id.passive.oleh', ...passive }, acceptVerb);
    } else {
      pushMatches(raw, clause, EN_PASSIVE, { ruleId: 'en.passive', ...passive });
    }

    raw.push(...structureFindings(clause, lang));
  }

  // Buang temuan tumpang-tindih pada kategori yang sama (mis. "harus disimpan" vs "disimpan oleh").
  raw.sort((a, b) => a.start - b.start || b.end - b.start - (a.end - a.start));
  const kept: RawFinding[] = [];
  for (const f of raw) {
    const overlaps = kept.some(
      (k) => k.category === f.category && k.term !== '—' && f.term !== '—' && f.start < k.end && f.end > k.start,
    );
    if (!overlaps) kept.push(f);
  }
  return kept.map((f, i) => ({ ...f, id: `F${i + 1}` }));
}

export function gradeFor(score: number, hasClauses: boolean): Grade {
  if (!hasClauses) return 'poor';
  if (score >= 85) return 'excellent';
  if (score >= 70) return 'good';
  if (score >= 40) return 'needs-improvement';
  return 'poor';
}

function emptyCounts(): Record<Category, number> {
  return Object.fromEntries(CATEGORIES.map((c) => [c, 0])) as Record<Category, number>;
}

function investChecks(
  clauses: Clause[],
  findings: Finding[],
  counts: Record<Category, number>,
  lang: Language,
  fullText: string,
): InvestCheck[] {
  const s = STORY[lang];
  const stories = clauses.filter((c) => s.start.test(c.text));
  const hasBenefit = (c: Clause) => s.benefit.test(c.text);
  const valuable = stories.length
    ? stories.every(hasBenefit)
    : clauses.some(hasBenefit);
  const maxWords = Math.max(0, ...clauses.map((c) => countWords(c.text)));

  const id = lang === 'id';
  return [
    {
      key: 'I',
      label: 'Independent',
      passed: clauses.length > 0 && !DEPENDENCY[lang].test(fullText),
      note: id ? 'Tidak bergantung pada fitur lain.' : 'Does not depend on other items.',
    },
    {
      key: 'N',
      label: 'Negotiable',
      passed: clauses.length > 0 && !TECH_LOCK.test(fullText),
      note: id ? 'Tidak mengunci solusi teknis.' : 'Does not lock the technical solution.',
    },
    {
      key: 'V',
      label: 'Valuable',
      passed: clauses.length > 0 && valuable,
      note: id ? 'Manfaat/nilai bisnis dinyatakan.' : 'Business value is stated.',
    },
    {
      key: 'E',
      label: 'Estimable',
      passed:
        clauses.length > 0 &&
        counts.ambiguity === 0 &&
        !findings.some((f) => f.category === 'incomplete'),
      note: id ? 'Cukup jelas untuk diestimasi.' : 'Clear enough to estimate.',
    },
    {
      key: 'S',
      label: 'Small',
      passed: clauses.length > 0 && maxWords <= 35 && clauses.length <= 8,
      note: id ? 'Cukup kecil (≤ 35 kata per klausul).' : 'Small enough (≤ 35 words per clause).',
    },
    {
      key: 'T',
      label: 'Testable',
      passed: clauses.length > 0 && counts['non-testable'] === 0 && counts['weak-directive'] === 0,
      note: id ? 'Dapat diverifikasi dengan kriteria jelas.' : 'Verifiable with clear criteria.',
    },
  ];
}

/** Jalankan seluruh audit untuk sebuah teks kebutuhan. Fungsi murni — aman dipakai di server maupun browser. */
export function analyze(text: string, language: Language): AnalysisResult {
  const clauses = splitClauses(text);
  const findings = findingsFor(clauses, language);

  const counts = emptyCounts();
  for (const f of findings) counts[f.category]++;

  const penalty = findings.reduce((sum, f) => sum + PENALTY[f.category], 0);
  // Teks yang lebih panjang menerima pengurang yang diredam agar skor tidak langsung 0.
  const dampening = Math.max(1, Math.sqrt(clauses.length / 2));
  const score = clauses.length ? Math.max(0, Math.round(100 - penalty / dampening)) : 0;

  // ISO 29148: 5 kriteria per klausul (tidak ambigu, dapat diverifikasi, lengkap, direktif kuat, aktif).
  const flagged = (clause: number, category: Category) =>
    findings.some((f) => f.clause === clause && f.category === category);
  let passed = 0;
  for (const c of clauses) {
    for (const cat of CATEGORIES) if (!flagged(c.index, cat)) passed++;
  }
  const iso29148 = clauses.length ? Math.round((passed / (clauses.length * CATEGORIES.length)) * 100) : 0;

  const invest = investChecks(clauses, findings, counts, language, text);
  const investScore = Math.round((invest.filter((i) => i.passed).length / invest.length) * 100);

  return {
    language,
    clauses,
    wordCount: clauses.reduce((n, c) => n + countWords(c.text), 0),
    findings,
    counts,
    score,
    grade: gradeFor(score, clauses.length > 0),
    compliance: { iso29148, invest: investScore },
    invest,
  };
}

/** Rentang yang digarisbawahi secara real-time di editor (tanpa struktur/pasif, agar ringan). */
export function liveMarks(text: string, language: Language): Array<{ start: number; end: number }> {
  const marks: Array<{ start: number; end: number }> = [];
  for (const rule of rulesFor(language)) {
    if (rule.category === 'incomplete') continue;
    for (const m of text.matchAll(rule.pattern)) {
      if (m.index !== undefined) marks.push({ start: m.index, end: m.index + m[0].length });
    }
  }
  marks.sort((a, b) => a.start - b.start);
  // Gabungkan rentang yang saling tumpang-tindih.
  const merged: typeof marks = [];
  for (const m of marks) {
    const last = merged[merged.length - 1];
    if (last && m.start < last.end) last.end = Math.max(last.end, m.end);
    else merged.push({ ...m });
  }
  return merged;
}
