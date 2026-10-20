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
      <div className="bg-white border border-[#e3e5eb] rounded-lg p-5 shadow-[0_5px_18px_rgba(40,48,72,0.04)]">
        <h3 className="text-md font-semibold text-[#343845] mb-3 flex items-center gap-2">
          Temuan cacat <span className="text-xs font-medium text-[#858894]">{smells.length}</span>
        </h3>
        {smells.length === 0 ? (
          <div className="text-[#35785d] text-sm bg-[#f3fbf6] border border-[#d9eee3] p-4 rounded-md">
            User story ini tidak memiliki smell yang terdeteksi.
          </div>
        ) : (
          <div className="space-y-2.5">
            {smells.map((smell, idx) => (
              <div
                key={idx}
                className="p-3.5 bg-[#fffdfc] rounded-md border border-[#f0e7e3] text-sm flex justify-between items-start gap-4"
              >
                <div>
                  <div className="font-semibold text-[#9a5947] flex items-center gap-2 flex-wrap">
                    <span className="text-xs px-2 py-0.5 bg-[#fff3ee] rounded border border-[#f1ddd4] font-mono text-[#a45c43]">
                      {smell.rule_id}
                    </span>
                    <span>&quot;{smell.target_text}&quot;</span>
                    <span className="text-xs text-[#858894] font-normal">({smell.category})</span>
                  </div>
                  <div className="text-[#626674] text-xs mt-1.5 leading-relaxed">{smell.message}</div>
                </div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider shrink-0 bg-[#fff8e8] border border-[#f0e5c8] text-[#9a781e]">
                  {smell.severity}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {revisions.length > 0 && (
        <div className="bg-white border border-[#e3e5eb] rounded-lg p-5 shadow-[0_5px_18px_rgba(40,48,72,0.04)]">
          <h3 className="text-md font-semibold text-[#343845] mb-3 flex items-center gap-2">
            <span className="text-[#3978d4]">✦</span> Saran revisi & acceptance criteria
          </h3>
          {revisions.map((rev, idx) => (
            <div key={idx} className="bg-[#f8f9fb] p-5 rounded-md border border-[#e7eaf0] space-y-3">
              <div className="text-xs font-semibold text-[#777b87] uppercase tracking-wide">
                Revisi yang disarankan:
              </div>
              <div className="text-[#326b51] font-mono text-sm leading-relaxed whitespace-pre-wrap bg-white p-4 rounded-md border border-[#e3e8e5]">
                {rev.suggested_text}
              </div>
              <div className="text-xs text-[#747783]">
                <span className="font-semibold text-[#4d5260]">Rasional:</span> {rev.rationale}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

