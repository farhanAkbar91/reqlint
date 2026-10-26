'use client';

import React from 'react';
import { AuditResponse } from '../../types/audit';

interface AuditScorecardProps {
  auditResult: AuditResponse | null;
}

export const AuditScorecard: React.FC<AuditScorecardProps> = ({ auditResult }) => {
  if (!auditResult) {
    return (
      <div className="bg-white border border-[#e3e5eb] rounded-lg p-8 text-center text-[#747783] shadow-[0_5px_18px_rgba(40,48,72,0.04)]">
        <div className="w-10 h-10 rounded-xl bg-[#f1f6fe] text-[#3978d4] flex items-center justify-center mx-auto mb-2 text-lg">
          ▤
        </div>
        <p className="font-medium text-[#414552]">Belum ada audit yang dijalankan.</p>
        <p className="text-xs text-[#858894] mt-1">Masukkan user story dan jalankan audit untuk melihat skor evaluasi INVEST.</p>
      </div>
    );
  }

  const { quality_score, detected_language, completeness_score, verifiability_score } = auditResult;

  const scoreColor =
    quality_score >= 80 ? 'text-[#278364]' : quality_score >= 60 ? 'text-[#ad781c]' : 'text-[#bf5e50]';

  return (
    <div className="bg-white border border-[#e3e5eb] rounded-lg p-6 text-[#292d39] shadow-[0_5px_18px_rgba(40,48,72,0.04)]">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-md font-semibold text-[#343845] flex items-center gap-2">
          <span className="text-[#3978d4]">◌</span> INVEST Quality Scorecard
        </h3>
        <span className="text-xs px-2.5 py-1 bg-[#f1f6fe] rounded-md font-mono text-[#3978d4] uppercase border border-[#dce8fa]">
          Bahasa: {detected_language}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-4 text-center">
        <div className="bg-[#f8f9fb] p-4 rounded-md border border-[#eceef2]">
          <div className="text-xs text-[#777b87] mb-1">Skor INVEST</div>
          <div className={`text-3xl font-extrabold ${scoreColor}`}>{quality_score} <span className="text-sm font-normal text-[#9295a0]">/ 100</span></div>
          <div className="text-[11px] text-[#858894] mt-1">Kualitas keseluruhan</div>
        </div>
        <div className="bg-[#f8f9fb] p-4 rounded-md border border-[#eceef2]">
          <div className="text-xs text-[#777b87] mb-1">Kelengkapan format</div>
          <div className="text-2xl font-bold text-[#3978d4]">{completeness_score}%</div>
          <div className="text-[11px] text-[#858894] mt-1">Role · Action · Benefit</div>
        </div>
        <div className="bg-[#f8f9fb] p-4 rounded-md border border-[#eceef2]">
          <div className="text-xs text-[#777b87] mb-1">Dapat diverifikasi</div>
          <div className="text-2xl font-bold text-[#278364]">{verifiability_score}%</div>
          <div className="text-[11px] text-[#858894] mt-1">Terukur dan jelas</div>
        </div>
      </div>
    </div>
  );
};

