'use client';

import React from 'react';
import { SmellResult, RevisionSuggestion } from '../../types/audit';

interface SmellListProps {
  smells: SmellResult[];
  revisions: RevisionSuggestion[];
}

export const SmellList: React.FC<SmellListProps> = ({ smells, revisions }) => {
  return (
    <div className="space-y-4">
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
        <h3 className="text-md font-semibold text-slate-200 mb-3 flex items-center gap-2">
          Detected User Story & INVEST Smells ({smells.length})
        </h3>
        {smells.length === 0 ? (
          <div className="text-emerald-400 text-sm italic bg-emerald-950/40 border border-emerald-800/50 p-4 rounded-lg">
            ✓ User Story memenuhi standar format Connextra dan kriteria INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable).
          </div>
        ) : (
          <div className="space-y-2.5">
            {smells.map((smell, idx) => (
              <div
                key={idx}
                className="p-3.5 bg-slate-950 rounded-lg border border-rose-900/40 text-sm flex justify-between items-start gap-4"
              >
                <div>
                  <div className="font-semibold text-rose-300 flex items-center gap-2 flex-wrap">
                    <span className="text-xs px-2 py-0.5 bg-rose-950/80 rounded border border-rose-800 font-mono text-rose-400">
                      {smell.rule_id}
                    </span>
                    <span>&quot;{smell.target_text}&quot;</span>
                    <span className="text-xs text-slate-400 font-normal">({smell.category})</span>
                  </div>
                  <div className="text-slate-300 text-xs mt-1.5 leading-relaxed">{smell.message}</div>
                </div>
                <span className="text-[11px] font-bold px-2 py-0.5 rounded uppercase tracking-wider shrink-0 bg-slate-900 border border-slate-800 text-amber-400">
                  {smell.severity}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {revisions.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
          <h3 className="text-md font-semibold text-emerald-400 mb-3 flex items-center gap-2">
            <span>✨</span> Saran Revisi INVEST & Acceptance Criteria
          </h3>
          {revisions.map((rev, idx) => (
            <div key={idx} className="bg-slate-950 p-5 rounded-lg border border-emerald-900/50 space-y-3">
              <div className="text-xs font-semibold text-emerald-400/80 uppercase tracking-wide">
                INVEST Compliant User Story & Gherkin Criteria:
              </div>
              <div className="text-emerald-300 font-mono text-sm leading-relaxed whitespace-pre-wrap bg-slate-900/90 p-4 rounded-md border border-slate-800">
                {rev.suggested_text}
              </div>
              <div className="text-xs text-slate-400 italic">
                <span className="font-semibold text-slate-300">Rasional:</span> {rev.rationale}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

