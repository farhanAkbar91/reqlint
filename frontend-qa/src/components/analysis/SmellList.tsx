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
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h3 className="text-md font-semibold text-slate-200 mb-3 flex items-center gap-2">
          Detected Ambiguity Smells ({smells.length})
        </h3>
        {smells.length === 0 ? (
          <div className="text-emerald-400 text-sm italic">
            ✓ No requirement smells detected. SRS requirement meets IEEE 29148 criteria.
          </div>
        ) : (
          <div className="space-y-2">
            {smells.map((smell, idx) => (
              <div
                key={idx}
                className="p-3 bg-slate-950 rounded-lg border border-rose-900/40 text-sm flex justify-between items-start"
              >
                <div>
                  <div className="font-semibold text-rose-300">
                    [{smell.severity}] {smell.target_text} ({smell.category})
                  </div>
                  <div className="text-slate-400 text-xs mt-1">{smell.message}</div>
                </div>
                <span className="text-xs px-2 py-0.5 bg-rose-950 text-rose-400 rounded border border-rose-800 font-mono">
                  {smell.rule_id}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {revisions.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="text-md font-semibold text-emerald-400 mb-2">Suggested Revision</h3>
          {revisions.map((rev, idx) => (
            <div key={idx} className="bg-slate-950 p-4 rounded-lg border border-emerald-900/50 space-y-2">
              <div className="text-xs text-slate-400">IEEE 29148 Compliant Rewrite:</div>
              <div className="text-emerald-300 font-mono text-sm font-medium">{rev.suggested_text}</div>
              <div className="text-xs text-slate-400 italic">Rationale: {rev.rationale}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
