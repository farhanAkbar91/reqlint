import { describe, expect, it } from 'vitest';
import { acceptanceCriteria, analyze, diffLines, diffWords, revise, splitClauses, suggestTitle } from './index';

const SAMPLE =
  'Sebagai user, saya ingin proses login sistem berjalan dengan sangat cepat dan user-friendly agar tidak membuang waktu.\nData sesi pengguna harus disimpan oleh sistem.';

describe('splitClauses', () => {
  it('memecah kalimat dan baris dengan offset yang benar', () => {
    const clauses = splitClauses(SAMPLE);
    expect(clauses).toHaveLength(2);
    for (const c of clauses) expect(SAMPLE.slice(c.start, c.end)).toBe(c.text);
  });

  it('tidak memecah pada singkatan dan nomor daftar', () => {
    expect(splitClauses('Sistem mendukung PDF, DOCX dll. dan CSV.')).toHaveLength(1);
    expect(splitClauses('1. Login\n2. Logout')).toHaveLength(2);
    expect(splitClauses('Versi 2.5 harus didukung.')).toHaveLength(1);
  });
});

describe('analyze (id)', () => {
  const result = analyze(SAMPLE, 'id');

  it('mendeteksi ambiguity, non-testable, dan passive voice', () => {
    expect(result.counts.ambiguity).toBe(1);
    expect(result.counts['non-testable']).toBe(1);
    expect(result.counts['passive-voice']).toBe(1);
    expect(result.counts.incomplete).toBe(0);
    expect(result.counts['weak-directive']).toBe(0);
    expect(result.findings.map((f) => f.term)).toEqual(['sangat cepat', 'user-friendly', 'harus disimpan']);
  });

  it('menghitung skor dan INVEST sesuai rumus', () => {
    expect(result.score).toBe(58);
    expect(result.grade).toBe('needs-improvement');
    expect(result.compliance.invest).toBe(67);
    expect(result.wordCount).toBe(17 + 7);
  });

  it('offset temuan menunjuk ke teks asli', () => {
    for (const f of result.findings) expect(SAMPLE.slice(f.start, f.end)).toBe(f.term);
  });

  it('mendeteksi bagian user story yang hilang', () => {
    const r = analyze('Sebagai admin, saya ingin melihat laporan.', 'id');
    expect(r.findings.map((f) => f.ruleId)).toEqual(['story.benefit']);
    const r2 = analyze('Sebagai admin melihat laporan agar cepat tahu.', 'id');
    expect(r2.findings.some((f) => f.ruleId === 'story.goal')).toBe(true);
  });

  it('tidak menandai kata berawalan "di" yang bukan pasif', () => {
    const r = analyze('Sistem harus menampilkan diagram dan dialog konfirmasi.', 'id');
    expect(r.counts['passive-voice']).toBe(0);
  });

  it('mendeteksi direktif lemah dan daftar terbuka', () => {
    const r = analyze('Sistem sebaiknya mendukung PDF, DOCX, dll.', 'id');
    expect(r.counts['weak-directive']).toBe(1);
    expect(r.counts.incomplete).toBe(1);
  });

  it('teks kosong menghasilkan skor 0 tanpa temuan', () => {
    const r = analyze('   ', 'id');
    expect(r.score).toBe(0);
    expect(r.findings).toHaveLength(0);
  });
});

describe('analyze (en)', () => {
  it('mendeteksi temuan bahasa Inggris', () => {
    const r = analyze('As a user, I want the login to be fast and user-friendly so that I save time. Sessions should be stored by the system.', 'en');
    expect(r.counts.ambiguity).toBe(1);
    expect(r.counts['non-testable']).toBe(1);
    expect(r.counts['weak-directive']).toBe(1);
    expect(r.counts['passive-voice']).toBe(1);
  });
});

describe('revise', () => {
  it('menulis ulang kalimat pasif dan mengganti istilah tidak terukur', () => {
    const rev = revise(SAMPLE, 'id');
    expect(rev.changed).toBe(true);
    expect(rev.text).toBe(
      'Sebagai pengguna, saya ingin proses login sistem berjalan dalam waktu kurang dari 2 detik dan memerlukan maksimal 3 langkah agar tidak membuang waktu.\nSistem harus menyimpan data sesi pengguna.',
    );
    expect(rev.result.score).toBeGreaterThan(analyze(SAMPLE, 'id').score);
    expect(rev.result.findings).toHaveLength(0);
  });

  it('tidak mengubah teks yang sudah baik', () => {
    const good = 'Sebagai pengguna, saya ingin masuk dalam waktu kurang dari 2 detik agar dapat bekerja.';
    expect(revise(good, 'id').changed).toBe(false);
  });
});

describe('diff', () => {
  it('menandai kata yang dihapus dan ditambahkan', () => {
    const ops = diffWords('login sangat cepat sekali', 'login dalam 2 detik sekali');
    expect(ops.filter((o) => o.type === 'del').map((o) => o.text.trim())).toContain('sangat');
    expect(ops.filter((o) => o.type === 'add').map((o) => o.text.trim())).toContain('dalam');
    const lines = diffLines(diffWords('a b\nc d', 'a x\nc d'), 'after');
    expect(lines).toHaveLength(2);
  });
});

describe('acceptanceCriteria & suggestTitle', () => {
  it('membuat skenario BDD dari user story', () => {
    const ac = acceptanceCriteria('Sebagai pengguna, saya ingin masuk dengan email agar dapat bekerja.', 'id');
    expect(ac?.when).toContain('masuk dengan email');
    expect(ac?.then).toContain('dapat bekerja');
  });

  it('mengembalikan null bila tidak ada kandidat', () => {
    expect(acceptanceCriteria('Halo dunia.', 'id')).toBeNull();
  });

  it('menyusun judul dari tujuan', () => {
    expect(suggestTitle(SAMPLE, 'id')).toBe('Proses login sistem berjalan');
  });
});
