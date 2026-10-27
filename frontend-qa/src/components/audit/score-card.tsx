import { HelpCircle } from 'lucide-react';
import type { AnalysisResult } from '@/lib/analyzer';
import { GRADE_BADGE, GRADE_COLOR, GRADE_LABEL, GRADE_TAGLINE } from '@/lib/format';

export function ScoreRing({ score, color, size = 108 }: { score: number; color: string; size?: number }) {
  const stroke = 9;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="-rotate-90" aria-hidden>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={color} strokeOpacity={0.16} strokeWidth={stroke} />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={c * (1 - score / 100)}
          style={{ transition: 'stroke-dashoffset 0.6s ease' }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-[38px] font-semibold leading-none tracking-tight">{score}</span>
        <span className="mt-1 text-[11px] text-muted">/ 100</span>
      </div>
    </div>
  );
}

export function ScoreCard({ result }: { result: AnalysisResult }) {
  return (
    <section className="card flex flex-col p-6" aria-label="Quality Scorecard">
      <div className="flex items-center justify-between">
        <h2 className="text-[16px] font-semibold">Quality Scorecard</h2>
        <span
          className="text-muted"
          title="Skor = 100 − bobot temuan (ambiguity 14, non-testable 16, tidak lengkap 18, weak directive 10, passive 12), diredam untuk teks panjang."
        >
          <HelpCircle size={16} aria-label="Cara menghitung skor" />
        </span>
      </div>
      <div className="flex flex-1 flex-col items-center justify-center py-5" role="img" aria-label={`Skor ${result.score} dari 100`}>
        <ScoreRing score={result.score} color={GRADE_COLOR[result.grade]} />
        <span className={`pill mt-5 ${GRADE_BADGE[result.grade]}`}>
          <span className="h-1.5 w-1.5 rounded-full bg-current" aria-hidden /> {GRADE_LABEL[result.grade]}
        </span>
        <p className="mt-3 text-center text-[12.5px] text-muted">{GRADE_TAGLINE[result.grade]}</p>
      </div>
    </section>
  );
}
