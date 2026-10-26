'use client';

import { CalendarDays, ChevronDown, Copy, Download, RefreshCw, FileSearch } from 'lucide-react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { useMemo } from 'react';
import { PageHeader } from '@/components/app-shell';
import { DiffViewer } from '@/components/audit/diff-viewer';
import { FindingsTable } from '@/components/audit/findings-table';
import { AcceptanceCard, RevisionCard } from '@/components/audit/revision-cards';
import { ScoreCard } from '@/components/audit/score-card';
import { SummaryCard } from '@/components/audit/summary-card';
import { Popover } from '@/components/popover';
import { useToast } from '@/components/providers';
import { acceptanceCriteria, analyze, revise } from '@/lib/analyzer';
import { createAudit, setDraft, touchAudit, useAudit } from '@/lib/audits';
import { buildExport, copyText, download, toMarkdown, type ExportFormat } from '@/lib/export';
import { formatDate } from '@/lib/format';

const EXPORTS: Array<{ format: ExportFormat; label: string }> = [
  { format: 'md', label: 'Markdown (.md)' },
  { format: 'csv', label: 'CSV (.csv)' },
  { format: 'json', label: 'JSON (.json)' },
];

export default function AuditPage() {
  const { id } = useParams<{ id: string }>();
  const audit = useAudit(id);
  const router = useRouter();
  const toast = useToast();

  const result = useMemo(() => (audit ? analyze(audit.text, audit.language) : null), [audit]);
  const revision = useMemo(() => (audit ? revise(audit.text, audit.language) : null), [audit]);
  const criteria = useMemo(
    () => (audit && revision ? acceptanceCriteria(revision.changed ? revision.text : audit.text, audit.language) : null),
    [audit, revision],
  );

  if (audit === undefined) return <div aria-busy="true" />;

  if (audit === null || !result || !revision) {
    return (
      <div className="card mx-auto flex max-w-[520px] flex-col items-center gap-3 px-8 py-14 text-center">
        <FileSearch size={30} strokeWidth={1.5} className="text-muted" aria-hidden />
        <h1 className="text-[20px] font-semibold">Audit tidak ditemukan</h1>
        <p className="text-[14px] text-muted">
          Audit <span className="font-mono">{id}</span> tidak ada di browser ini. Mungkin sudah dihapus atau dibuat di perangkat lain.
        </p>
        <Link href="/editor" className="btn-primary mt-2 h-11 px-6 text-[14px]">
          Kembali ke editor
        </Link>
      </div>
    );
  }

  const openInEditor = (text: string) => {
    setDraft({ text, language: audit.language });
    router.push('/editor');
  };

  /** Terapkan revisi: jalankan audit baru dari teks revisi dan tampilkan hasilnya. */
  const applyRevision = () => {
    const next = createAudit(revision.text, audit.language);
    setDraft({ text: revision.text, language: audit.language });
    toast('Revisi diterapkan. Menampilkan hasil audit baru.');
    router.push(`/audit/${next.id}`);
  };

  const rerun = () => {
    touchAudit(audit.id);
    toast('Analisis dijalankan ulang dengan aturan terbaru.');
  };

  const copyResult = async () => {
    const ok = await copyText(toMarkdown(audit, result, revision));
    toast(ok ? 'Hasil audit disalin (Markdown).' : 'Gagal menyalin. Coba gunakan Export.');
  };

  const exportAs = (format: ExportFormat) => {
    const { filename, mime, content } = buildExport(format, audit, result, revision);
    download(filename, mime, content);
    toast(`${filename} diunduh.`);
  };

  return (
    <>
      <PageHeader
        crumb="Workspace / Analisis Kebutuhan"
        title="Hasil Audit"
        subtitle={
          <span className="flex flex-wrap items-center gap-x-3 gap-y-1 text-[12.5px]">
            <span className="font-mono">{audit.id}</span>
            <span aria-hidden>·</span>
            <span className="inline-flex items-center gap-1.5">
              <CalendarDays size={13} aria-hidden /> {formatDate(audit.createdAt)}
            </span>
            <span aria-hidden>·</span>
            <span>{audit.title}</span>
          </span>
        }
        right={
          <div className="flex flex-wrap items-center gap-2.5">
            <button type="button" onClick={rerun} className="btn-ghost h-10 rounded-full px-4 text-[13px]">
              <RefreshCw size={14} aria-hidden /> Analisis Ulang
            </button>
            <button type="button" onClick={copyResult} className="btn-ghost h-10 rounded-full px-4 text-[13px]">
              <Copy size={14} aria-hidden /> Salin Hasil
            </button>
            <Popover
              align="right"
              trigger={({ toggle }) => (
                <button type="button" onClick={toggle} className="btn-primary h-10 rounded-full px-4 text-[13px]">
                  <Download size={14} aria-hidden /> Export <ChevronDown size={13} aria-hidden />
                </button>
              )}
            >
              {(close) =>
                EXPORTS.map(({ format, label }) => (
                  <button
                    key={format}
                    type="button"
                    className="menu-item"
                    onClick={() => {
                      exportAs(format);
                      close();
                    }}
                  >
                    {label}
                  </button>
                ))
              }
            </Popover>
          </div>
        }
      />

      <div className="space-y-5">
        <div className="grid gap-5 lg:grid-cols-[minmax(0,340px)_1fr]">
          <ScoreCard result={result} />
          <SummaryCard result={result} />
        </div>

        <FindingsTable findings={result.findings} onOpenEditor={() => openInEditor(audit.text)} />

        <div className="grid gap-5 md:grid-cols-2">
          <RevisionCard
            revision={revision}
            remaining={revision.result.findings.length}
            onApply={applyRevision}
            onEdit={() => openInEditor(revision.changed ? revision.text : audit.text)}
          />
          <AcceptanceCard criteria={criteria} />
        </div>

        {revision.changed && (
          <DiffViewer
            before={audit.text}
            after={revision.text}
            beforeScore={result.score}
            afterScore={revision.result.score}
            onApply={applyRevision}
            canApply
          />
        )}
      </div>
    </>
  );
}
