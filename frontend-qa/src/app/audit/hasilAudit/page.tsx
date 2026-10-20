'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { ArrowLeft, Check, Clipboard, Download, FileText, RotateCcw, Sparkles } from 'lucide-react';
import { useEffect, useState } from 'react';
import styles from './index.module.css';
import type { AuditResponse, SmellResult } from '../../../types/audit';

const STORAGE_KEY = 'reqlint:last-audit';

function categoryLabel(category: SmellResult['category']) {
  if (category === 'Ambiguity') return 'Ambiguitas';
  if (category === 'Incompleteness') return 'Tidak lengkap';
  return 'Sulit diverifikasi';
}

export default function HasilAuditPage() {
  const router = useRouter();
  const [audit, setAudit] = useState<AuditResponse | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const value = sessionStorage.getItem(STORAGE_KEY);
    if (!value) return;
    try { setAudit(JSON.parse(value) as AuditResponse); }
    catch { sessionStorage.removeItem(STORAGE_KEY); }
  }, []);

  const copyResult = async () => {
    if (!audit) return;
    await navigator.clipboard.writeText(JSON.stringify(audit, null, 2));
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  };

  const exportResult = () => {
    if (!audit) return;
    const url = URL.createObjectURL(new Blob([JSON.stringify(audit, null, 2)], { type: 'application/json' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'reqlint-hasil-audit.json';
    link.click();
    URL.revokeObjectURL(url);
  };

  const useRevision = (text: string) => {
    sessionStorage.setItem('reqlint:pending-requirement', text);
    router.push('/');
  };

  if (!audit) return (
    <section className={styles.emptyState}>
      <div className={styles.emptyIcon}><FileText size={22} /></div>
      <p className={styles.eyebrow}>WORKSPACE / ANALISIS KEBUTUHAN</p>
      <h1>Belum ada hasil audit</h1>
      <p>Jalankan audit dari editor untuk melihat skor, temuan, dan rekomendasi di sini.</p>
      <Link className={styles.primaryButton} href="/"><ArrowLeft size={15} /> Buka editor</Link>
    </section>
  );

  const score = Math.max(0, Math.min(100, Math.round(audit.quality_score)));
  const recommendation = audit.revisions[0];
  const categories = [
    ['Ambiguitas', audit.smells.filter((item) => item.category === 'Ambiguity').length],
    ['Tidak lengkap', audit.smells.filter((item) => item.category === 'Incompleteness').length],
    ['Sulit diverifikasi', audit.smells.filter((item) => item.category === 'Unverifiable').length],
  ] as const;

  return <div className={styles.page}>
    <div className={styles.heading}>
      <div><p className={styles.eyebrow}>WORKSPACE / ANALISIS KEBUTUHAN</p><h1>Hasil Audit</h1>
        <div className={styles.meta}><span className={styles.auditId}>AUD-{new Date().toISOString().slice(2, 10).replaceAll('-', '')}</span>
          <span>{new Date().toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })}</span>
          <span>{audit.detected_language === 'id' ? 'Bahasa Indonesia' : audit.detected_language === 'en' ? 'Bahasa Inggris' : 'Bahasa tidak diketahui'}</span>
        </div>
      </div>
      <div className={styles.actions}>
        <Link href="/" className={styles.secondaryButton}><RotateCcw size={15} /> Analisis ulang</Link>
        <button type="button" onClick={copyResult} className={styles.secondaryButton}>{copied ? <Check size={15} /> : <Clipboard size={15} />}{copied ? 'Tersalin' : 'Salin hasil'}</button>
        <button type="button" onClick={exportResult} className={styles.primaryButton}><Download size={15} /> Export JSON</button>
      </div>
    </div>

    <section className={styles.overview} aria-label="Ringkasan audit">
      <article className={styles.panel}>
        <div className={styles.sectionTitle}><div><p className={styles.eyebrow}>QUALITY SCORECARD</p><h2>Kualitas kebutuhan</h2></div><span className={styles.language}>{audit.detected_language.toUpperCase()}</span></div>
        <div className={styles.scoreBody}><div className={styles.scoreRing} style={{ '--score': `${score}%` } as React.CSSProperties}><div><strong>{score}</strong><span>/ 100</span></div></div>
          <div><strong className={score >= 80 ? styles.good : score >= 60 ? styles.medium : styles.needsWork}>{score >= 80 ? 'Kualitas baik' : score >= 60 ? 'Perlu sedikit perbaikan' : 'Perlu perbaikan'}</strong><p className={styles.muted}>Kejelasan dimulai dari kebutuhan yang baik.</p></div>
        </div>
        <div className={styles.metrics}><Metric label="Kelengkapan" value={audit.completeness_score} /><Metric label="Dapat diverifikasi" value={audit.verifiability_score} /><Metric label="Indeks ambiguitas" value={audit.ambiguity_index} inverse /></div>
      </article>
      <article className={styles.panel}>
        <div className={styles.sectionTitle}><div><p className={styles.eyebrow}>TEMUAN</p><h2>Ringkasan analisis</h2></div><span className={styles.countBadge}>{audit.smells.length} temuan</span></div>
        <p className={styles.complete}><i /> Analisis selesai</p>
        <div className={styles.categoryList}>{categories.map(([label, count]) => <div className={styles.categoryRow} key={label}><span>{label}</span><strong>{count}</strong></div>)}</div>
        <div className={styles.sourceText}><span className={styles.eyebrow}>USER STORY DIAUDIT</span><p>{audit.requirement_text}</p></div>
      </article>
    </section>

    <section className={`${styles.panel} ${styles.findings}`}>
      <div className={styles.sectionTitle}><div><p className={styles.eyebrow}>HASIL PEMERIKSAAN</p><h2>Temuan cacat</h2></div><span className={styles.countBadge}>{audit.smells.length}</span></div>
      {audit.smells.length === 0 ? <p className={styles.noFindings}><Check size={17} /> Tidak ada smell terdeteksi berdasarkan pemeriksaan yang tersedia.</p> :
        <div className={styles.tableWrap}><table><thead><tr><th>LOKASI</th><th>KATEGORI</th><th>ISTILAH TERDETEKSI</th><th>REKOMENDASI</th></tr></thead><tbody>
          {audit.smells.map((smell, index) => <tr key={`${smell.rule_id}-${smell.start_char}-${index}`}>
            <td><b className={styles.rowNumber}>{String(index + 1).padStart(2, '0')}</b>Kalimat {Math.max(1, audit.requirement_text.slice(0, smell.start_char).split(/[.!?]+/).filter(Boolean).length + 1)}</td>
            <td><span className={`${styles.categoryTag} ${styles[`tag${smell.category}`]}`}>{categoryLabel(smell.category)}</span></td>
            <td><code>{smell.target_text || smell.rule_id}</code><small>{smell.rule_id} · {smell.severity}</small></td><td>{smell.message}</td>
          </tr>)}
        </tbody></table></div>}
    </section>

    {recommendation && <section className={styles.revisionGrid}>
      <article className={styles.panel}><div className={styles.titleIcon}><Sparkles size={17} /><div><p className={styles.eyebrow}>SARAN REVISI · {recommendation.framework}</p><h2>Rekomendasi perbaikan</h2></div></div>
        <blockquote>{recommendation.suggested_text}</blockquote><p className={styles.rationale}><b>Rasional</b>{recommendation.rationale}</p>
        <button type="button" onClick={() => useRevision(recommendation.suggested_text)} className={styles.primaryButton}><Check size={15} /> Gunakan revisi di editor</button>
      </article>
      <article className={styles.panel}><div className={styles.sectionTitle}><div><p className={styles.eyebrow}>PERBANDINGAN</p><h2>Sebelum dan sesudah</h2></div><span className={styles.legend}>Asli <i /> Revisi <i /></span></div>
        <div className={styles.diffBlock}><span className={styles.eyebrow}>DRAF ASLI</span><p className={styles.original}>{recommendation.original_text || audit.requirement_text}</p></div>
        <div className={styles.diffBlock}><span className={styles.eyebrow}>REVISI</span><p className={styles.revised}>{recommendation.suggested_text}</p></div>
        <p className={styles.muted}>Revisi hanya diterapkan setelah Anda memilihnya.</p>
      </article>
    </section>}
    <footer className={styles.footer}><span>ReqLint · Clarity, by design.</span><span>ISO 29148 / INVEST</span></footer>
  </div>;
}

function Metric({ label, value, inverse = false }: { label: string; value: number; inverse?: boolean }) {
  const normalized = Math.max(0, Math.min(100, Math.round(value)));
  return <div className={styles.metric}><div><span>{label}</span><b>{normalized}%</b></div><div className={styles.track}><i style={{ width: `${inverse ? 100 - normalized : normalized}%` }} /></div></div>;
}
