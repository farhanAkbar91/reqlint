export type DiffOp = { type: 'equal' | 'del' | 'add'; text: string };

/** Diff tingkat kata (LCS). Whitespace diperlakukan sebagai token agar susunan baris tetap utuh. */
export function diffWords(before: string, after: string): DiffOp[] {
  const a = before.split(/(\s+)/).filter(Boolean);
  const b = after.split(/(\s+)/).filter(Boolean);
  const n = a.length;
  const m = b.length;

  // Teks sangat besar: jangan bangun tabel O(n·m); tampilkan sebagai satu blok perubahan.
  if (n * m > 4_000_000) {
    return [
      { type: 'del', text: before },
      { type: 'add', text: after },
    ];
  }

  const dp: Uint32Array[] = Array.from({ length: n + 1 }, () => new Uint32Array(m + 1));
  for (let i = n - 1; i >= 0; i--) {
    for (let j = m - 1; j >= 0; j--) {
      dp[i][j] = a[i] === b[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
    }
  }

  const ops: DiffOp[] = [];
  const push = (type: DiffOp['type'], text: string) => {
    const last = ops[ops.length - 1];
    if (last && last.type === type) last.text += text;
    else ops.push({ type, text });
  };

  let i = 0;
  let j = 0;
  while (i < n && j < m) {
    if (a[i] === b[j]) {
      push('equal', a[i]);
      i++;
      j++;
    } else if (dp[i + 1][j] >= dp[i][j + 1]) {
      push('del', a[i++]);
    } else {
      push('add', b[j++]);
    }
  }
  while (i < n) push('del', a[i++]);
  while (j < m) push('add', b[j++]);
  return ops;
}

/** Ambil sisi kiri (before) atau kanan (after) dari diff, dipecah per baris. */
export function diffLines(ops: DiffOp[], side: 'before' | 'after'): DiffOp[][] {
  const keep = side === 'before' ? 'del' : 'add';
  const lines: DiffOp[][] = [[]];
  for (const op of ops) {
    if (op.type !== 'equal' && op.type !== keep) continue;
    const parts = op.text.split('\n');
    parts.forEach((part, idx) => {
      if (idx > 0) lines.push([]);
      if (part) lines[lines.length - 1].push({ type: op.type, text: part });
    });
  }
  return lines;
}
