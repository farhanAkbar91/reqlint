'use client';

import React from 'react';
import { AuditResponse } from '../../types/audit';

interface AuditScorecardProps {
  auditResult: AuditResponse | null;
}

export const AuditScorecard: React.FC<AuditScorecardProps> = ({ auditResult }) => {
  if (!auditResult) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center text-slate-400 shadow-lg">
        <div className="w-10 h-10 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center mx-auto mb-2 text-lg">
          📋
        </div>
        <p className="font-medium text-slate-300">Belum ada audit yang dijalankan.</p>
        <p className="text-xs text-slate-500 mt-1">Masukkan User Story dan klik &quot;Audit User Story&quot; untuk melihat skor evaluasi INVEST.</p>
      </div>
    );
  }

  const { quality_score, detected_language, completeness_score, verifiability_score } = auditResult;

  const scoreColor =
    quality_score >= 80 ? 'text-emerald-400' : quality_score >= 60 ? 'text-amber-400' : 'text-rose-400';

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-slate-100 shadow-lg">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-md font-semibold text-slate-200 flex items-center gap-2">
          <span>📊</span> INVEST Quality Scorecard
        </h3>
        <span className="text-xs px-2.5 py-1 bg-slate-800 rounded-full font-mono text-emerald-400 uppercase border border-slate-700">
          Bahasa: {detected_language}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-4 text-center">
        <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
          <div className="text-xs text-slate-400 mb-1">Skor INVEST</div>
          <div className={`text-3xl font-extrabold ${scoreColor}`}>{quality_score} <span className="text-sm font-normal text-slate-500">/ 100</span></div>
          <div className="text-[11px] text-slate-500 mt-1">Overall Quality</div>
        </div>
        <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
          <div className="text-xs text-slate-400 mb-1">Kelengkapan Format</div>
          <div className="text-2xl font-bold text-sky-400">{completeness_score}%</div>
          <div className="text-[11px] text-slate-500 mt-1">Role · Action · Benefit</div>
        </div>
        <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
          <div className="text-xs text-slate-400 mb-1">Dapat Diuji (Testable)</div>
          <div className="text-2xl font-bold text-purple-400">{verifiability_score}%</div>
          <div className="text-[11px] text-slate-500 mt-1">Bebas Kata Ambigu</div>
        </div>
      </div>
    </div>
  );
};

