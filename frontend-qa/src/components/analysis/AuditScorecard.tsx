'use client';

import React from 'react';
import { AuditResponse } from '../../types/audit';

interface AuditScorecardProps {
  auditResult: AuditResponse | null;
}

export const AuditScorecard: React.FC<AuditScorecardProps> = ({ auditResult }) => {
  if (!auditResult) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center text-slate-400">
        Run audit to view quality score breakdown.
      </div>
    );
  }

  const { quality_score, detected_language, completeness_score, verifiability_score } = auditResult;

  const scoreColor =
    quality_score >= 80 ? 'text-emerald-400' : quality_score >= 60 ? 'text-amber-400' : 'text-rose-400';

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-slate-100 shadow-lg">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-md font-semibold text-slate-300">Quality Scorecard</h3>
        <span className="text-xs px-2.5 py-1 bg-slate-800 rounded-full font-mono text-emerald-400 uppercase">
          Lang: {detected_language}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-4 text-center">
        <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
          <div className="text-xs text-slate-400 mb-1">Overall Quality</div>
          <div className={`text-3xl font-extrabold ${scoreColor}`}>{quality_score} / 100</div>
        </div>
        <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
          <div className="text-xs text-slate-400 mb-1">Completeness</div>
          <div className="text-2xl font-bold text-sky-400">{completeness_score}%</div>
        </div>
        <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
          <div className="text-xs text-slate-400 mb-1">Verifiability</div>
          <div className="text-2xl font-bold text-purple-400">{verifiability_score}%</div>
        </div>
      </div>
    </div>
  );
};
