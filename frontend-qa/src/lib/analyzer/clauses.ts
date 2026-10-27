import type { Clause } from './types';

const ABBREVIATIONS = new Set([
  'dll', 'dsb', 'dst', 'dkk', 'mis', 'dr', 'ir', 'no', 'hlm', 'tgl', 'yth', 'cth',
  'e.g', 'i.e', 'etc', 'vs', 'approx', 'inc', 'ltd',
]);

function isAbbreviation(text: string, dotIndex: number): boolean {
  const before = text.slice(0, dotIndex);
  const match = /([A-Za-z.]+|\d+)$/.exec(before);
  if (!match) return false;
  const token = match[1].toLowerCase();
  // "1." pada daftar bernomor bukan akhir kalimat.
  if (/^\d+$/.test(token)) return true;
  if (!ABBREVIATIONS.has(token)) return false;
  // Singkatan hanya dianggap bukan akhir kalimat bila kata berikutnya huruf kecil.
  const after = /\S/.exec(text.slice(dotIndex + 1));
  return !!after && /\p{Ll}/u.test(after[0]);
}

/** Memecah teks menjadi klausul (kalimat/baris) lengkap dengan offset pada teks asli. */
export function splitClauses(text: string): Clause[] {
  const clauses: Clause[] = [];
  let start = 0;

  const push = (end: number) => {
    const raw = text.slice(start, end);
    const trimmed = raw.trim();
    if (!trimmed) return;
    const offset = start + (raw.length - raw.trimStart().length);
    clauses.push({
      index: clauses.length + 1,
      text: trimmed,
      start: offset,
      end: offset + trimmed.length,
    });
  };

  let i = 0;
  while (i < text.length) {
    const ch = text[i];
    if (ch === '\n') {
      push(i);
      start = i + 1;
    } else if (ch === '.' || ch === '!' || ch === '?') {
      let j = i;
      while (j + 1 < text.length && '.!?'.includes(text[j + 1])) j++;
      const next = text[j + 1];
      const atBoundary = next === undefined || /\s/.test(next);
      if (atBoundary && !(ch === '.' && isAbbreviation(text, i))) {
        push(j + 1);
        start = j + 1;
      }
      i = j;
    }
    i++;
  }
  push(text.length);
  return clauses;
}

export function countWords(text: string): number {
  return text.match(/[\p{L}\p{N}][\p{L}\p{N}'’-]*/gu)?.length ?? 0;
}
