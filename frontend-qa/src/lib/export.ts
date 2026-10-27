import type { Audit } from './audits';
import { CATEGORY_LABEL, GRADE_LABEL, formatDate } from './format';
import type { AnalysisResult, Revision } from './analyzer';

export type ExportFormat = 'md' | 'csv' | 'json';

export function toMarkdown(audit: Audit, result: AnalysisResult, revision: Revision): string {
  const lines: string[] = [
    `# Hasil Audit ${audit.id}`,
    '',
    `- Judul: ${audit.title}`,
    `- Tanggal: ${formatDate(audit.createdAt)}`,
    `- Skor kualitas: **${result.score}/100** (${GRADE_LABEL[result.grade]})`,
    `- Kepatuhan: ISO 29148 ${result.compliance.iso29148}% · INVEST ${result.compliance.invest}%`,
    '',
    '## Draf Orisinal',
    '',
    ...audit.text.split('\n').map((l) => `> ${l}`),
    '',
    `## Temuan Cacat (${result.findings.length})`,
    '',
  ];
  if (result.findings.length) {
    lines.push('| Lokasi | Kategori | Istilah | Rekomendasi |', '| --- | --- | --- | --- |');
    for (const f of result.findings) {
      lines.push(`| Kalimat ${f.clause} | ${CATEGORY_LABEL[f.category]} | \`${f.term}\` | ${f.recommendation} |`);
    }
  } else {
    lines.push('Tidak ada temuan.');
  }
  if (revision.changed) {
    lines.push('', `## Saran Revisi (skor ${revision.result.score})`, '', ...revision.text.split('\n').map((l) => `> ${l}`));
  }
  return lines.join('\n') + '\n';
}

const csvCell = (v: string | number) => `"${String(v).replace(/"/g, '""')}"`;

export function toCsv(audit: Audit, result: AnalysisResult): string {
  const rows = [['audit_id', 'kalimat', 'kategori', 'istilah', 'rekomendasi']];
  for (const f of result.findings) {
    rows.push([audit.id, String(f.clause), CATEGORY_LABEL[f.category], f.term, f.recommendation]);
  }
  return rows.map((r) => r.map(csvCell).join(',')).join('\n') + '\n';
}

export function toJson(audit: Audit, result: AnalysisResult, revision: Revision): string {
  return JSON.stringify(
    { audit, result, revision: { changed: revision.changed, text: revision.text, score: revision.result.score } },
    null,
    2,
  );
}

const MIME: Record<ExportFormat, string> = {
  md: 'text/markdown;charset=utf-8',
  csv: 'text/csv;charset=utf-8',
  json: 'application/json;charset=utf-8',
};

export function buildExport(format: ExportFormat, audit: Audit, result: AnalysisResult, revision: Revision) {
  const content =
    format === 'md' ? toMarkdown(audit, result, revision) : format === 'csv' ? toCsv(audit, result) : toJson(audit, result, revision);
  return { filename: `${audit.id}.${format}`, mime: MIME[format], content };
}

export function download(filename: string, mime: string, content: string) {
  // BOM agar Excel membaca CSV UTF-8 dengan benar.
  const blob = new Blob([mime.startsWith('text/csv') ? '﻿' + content : content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export async function copyText(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    const ok = document.execCommand('copy');
    ta.remove();
    return ok;
  }
}
