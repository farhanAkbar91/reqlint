'use client';

import React from 'react';

interface RequirementEditorProps {
  value: string;
  onChange: (val: string) => void;
  onAudit: () => void;
  isLoading: boolean;
}

export const RequirementEditor: React.FC<RequirementEditorProps> = ({
  value,
  onChange,
  onAudit,
  isLoading,
}) => {
  const insertTemplateId = () => {
    onChange('Sebagai [Peran], saya ingin [Aksi atau Fitur], sehingga [Manfaat / Nilai Bisnis].');
  };

  const insertTemplateEn = () => {
    onChange('As a [Role], I want [Action or Feature], so that [Business or User Benefit].');
  };

  return (
    <div className="flex flex-col h-full bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
      <div className="flex flex-wrap justify-between items-center gap-3 mb-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
            Agile User Story Editor
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Format Connextra: <span className="font-mono text-emerald-400">Role - Action - Benefit</span> & kriteria <span className="font-semibold text-sky-400">INVEST</span>
          </p>
        </div>
        <button
          onClick={onAudit}
          disabled={isLoading || !value.trim()}
          className="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-lg transition-all disabled:opacity-50 flex items-center gap-2 text-sm shadow-md hover:shadow-emerald-500/20"
        >
          {isLoading ? 'Analyzing INVEST...' : 'Audit User Story'}
        </button>
      </div>

      <div className="flex gap-2 mb-3">
        <span className="text-xs text-slate-400 self-center">Template Cepat:</span>
        <button
          type="button"
          onClick={insertTemplateId}
          className="text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded border border-slate-700 transition"
        >
          🇮🇩 Format ID (Sebagai... Saya ingin... Sehingga...)
        </button>
        <button
          type="button"
          onClick={insertTemplateEn}
          className="text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded border border-slate-700 transition"
        >
          🇬🇧 Format EN (As a... I want... So that...)
        </button>
      </div>

      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Tuliskan User Story dalam Bahasa Indonesia atau Bahasa Inggris...\nContoh: Sebagai pembeli, saya ingin melacak pengiriman secara real-time, sehingga saya mengetahui perkiraan kedatangan barang."
        className="w-full h-64 bg-slate-950 text-slate-100 border border-slate-800 rounded-lg p-4 font-mono text-sm focus:outline-none focus:border-emerald-500 transition-colors resize-none leading-relaxed"
        id="user-story-input"
      />
    </div>
  );
};

