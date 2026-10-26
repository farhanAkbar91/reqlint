'use client';

import { ArrowRight, ChevronDown, FileText, FileUp, Languages, Lightbulb, X, Check } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useMemo, useRef } from 'react';
import { PageHeader } from '@/components/app-shell';
import { CodeEditor } from '@/components/code-editor';
import { Popover } from '@/components/popover';
import { countWords, liveMarks, splitClauses, type Language } from '@/lib/analyzer';
import { createAudit, dismissTip, setDraft, useDraft, useTipDismissed } from '@/lib/audits';
import { TEMPLATES } from '@/lib/templates';
import { useFileImport } from '@/lib/use-file-import';
import { MAX_CHARS } from '@/lib/validation';

const LANGUAGES: Record<Language, string> = { id: 'Bahasa Indonesia', en: 'English' };

export default function EditorPage() {
  const router = useRouter();
  const draft = useDraft();
  const tipDismissed = useTipDismissed();
  const fileInput = useRef<HTMLInputElement>(null);
  const { busy: uploading, onChange: onFile } = useFileImport((text) => setDraft({ ...draft, text }));

  const stats = useMemo(
    () => ({
      clauses: splitClauses(draft.text).length,
      words: countWords(draft.text),
      flagged: liveMarks(draft.text, draft.language).length,
    }),
    [draft.text, draft.language],
  );
  const empty = draft.text.trim().length === 0;

  const update = (patch: Partial<typeof draft>) => setDraft({ ...draft, ...patch });

  function analyzeNow() {
    if (empty) return;
    const audit = createAudit(draft.text, draft.language);
    router.push(`/audit/${audit.id}`);
  }

  return (
    <>
      <PageHeader
        crumb="Workspace / Draf Kebutuhan"
        title="Editor User Story"
        subtitle="Tulis atau tempel draf kebutuhan Anda. ReqLint akan mengauditnya secara real-time."
        right={
          <span className="pill bg-line/[0.06] text-muted">
            <span className="h-1.5 w-1.5 rounded-full bg-faint" aria-hidden /> Ruang kerja personal
          </span>
        }
      />

      <section className="card overflow-visible p-5 sm:p-6" aria-label="Editor">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-line/[0.07] pb-5">
          <Popover
            trigger={({ toggle }) => (
              <button
                type="button"
                onClick={toggle}
                className="btn-ghost h-9 gap-2 rounded-full px-3 text-[12.5px]"
                aria-label="Pilih bahasa analisis"
              >
                <Languages size={14} aria-hidden /> {LANGUAGES[draft.language]}
              </button>
            )}
          >
            {(close) =>
              (Object.keys(LANGUAGES) as Language[]).map((l) => (
                <button
                  key={l}
                  type="button"
                  className="menu-item justify-between"
                  onClick={() => {
                    update({ language: l });
                    close();
                  }}
                >
                  {LANGUAGES[l]}
                  {l === draft.language && <Check size={15} aria-hidden />}
                </button>
              ))
            }
          </Popover>

          <div className="flex flex-wrap items-center gap-2.5">
            <input
              ref={fileInput}
              type="file"
              accept=".pdf,.txt,.md,application/pdf,text/plain,text/markdown"
              className="sr-only"
              onChange={onFile}
              aria-label="Unggah berkas PDF atau teks"
              tabIndex={-1}
            />
            <button
              type="button"
              disabled={uploading}
              onClick={() => fileInput.current?.click()}
              className="btn-ghost h-11 whitespace-nowrap px-4 text-[14px]"
            >
              <FileUp size={16} aria-hidden /> {uploading ? 'Membaca…' : 'Upload PDF'}
            </button>

            <Popover
              align="right"
              trigger={({ toggle }) => (
                <button type="button" onClick={toggle} className="btn-ghost h-11 whitespace-nowrap px-4 text-[14px]">
                  <FileText size={16} aria-hidden /> Contoh Template <ChevronDown size={14} aria-hidden />
                </button>
              )}
            >
              {(close) =>
                TEMPLATES.map((t) => (
                  <button
                    key={t.id}
                    type="button"
                    className="menu-item"
                    onClick={() => {
                      update({ text: t.text[draft.language] });
                      close();
                    }}
                  >
                    {t.label[draft.language]}
                  </button>
                ))
              }
            </Popover>
          </div>
        </div>

        <div className="mt-5">
          <CodeEditor
            value={draft.text}
            onChange={(text) => update({ text })}
            language={draft.language}
            maxLength={MAX_CHARS}
          />
        </div>

        <p className="mt-3.5 flex items-center gap-2 text-[12.5px] text-muted" aria-live="polite">
          <span className={`h-1.5 w-1.5 rounded-full ${stats.flagged ? 'bg-amber-500' : 'bg-emerald-500'}`} aria-hidden />
          {empty
            ? 'Tulis atau tempel draf kebutuhan untuk mulai.'
            : stats.flagged
              ? 'Istilah yang digarisbawahi mungkin tidak terukur. Jalankan analisis untuk melihat rekomendasi.'
              : 'Belum ada istilah tidak terukur yang terdeteksi saat mengetik. Jalankan analisis untuk pemeriksaan lengkap.'}
        </p>

        <div className="mt-5 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3 text-[13.5px] text-muted">
            <span>
              {stats.clauses} klausul · {stats.words} kata
            </span>
            <span className="h-4 w-px bg-line/10" aria-hidden />
            <span className="inline-flex items-center gap-1.5">
              <Check size={14} aria-hidden /> Tersimpan otomatis
            </span>
          </div>
          <button type="button" onClick={analyzeNow} disabled={empty} className="btn-primary h-[52px] gap-3 px-7 text-[16px]">
            Analisis <ArrowRight size={18} aria-hidden />
          </button>
        </div>
      </section>

      {!tipDismissed && (
        <aside className="card mt-5 flex items-center gap-4 rounded-[22px] px-4 py-3.5" aria-label="Tips">
          <span className="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl border border-line/[0.07] bg-card">
            <Lightbulb size={18} strokeWidth={1.6} aria-hidden />
          </span>
          <div className="min-w-0 flex-1">
            <p className="text-[14.5px] font-semibold">Kebutuhan yang baik dimulai dari tiga hal.</p>
            <p className="text-[12.5px] text-muted">
              Tentukan siapa penggunanya, apa yang dibutuhkan, dan mengapa itu penting. Kami membantu menyempurnakan sisanya.
            </p>
          </div>
          <a
            href="https://en.wikipedia.org/wiki/INVEST_(mnemonic)"
            target="_blank"
            rel="noreferrer"
            className="hidden items-center gap-1.5 whitespace-nowrap text-[12.5px] font-medium text-accent hover:underline sm:inline-flex"
          >
            Pelajari INVEST <ArrowRight size={14} aria-hidden />
          </a>
          <button
            type="button"
            onClick={dismissTip}
            aria-label="Tutup tips"
            className="inline-flex h-8 w-8 items-center justify-center rounded-full text-muted transition hover:bg-line/[0.06] hover:text-ink"
          >
            <X size={16} />
          </button>
        </aside>
      )}
    </>
  );
}
