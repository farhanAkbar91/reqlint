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
    <div className="flex flex-col h-full bg-white border border-[#e3e5eb] rounded-lg p-5 shadow-[0_5px_18px_rgba(40,48,72,0.04)]">
      <div className="flex flex-wrap justify-between items-center gap-3 mb-3">
        <div>
          <h2 className="text-lg font-semibold text-[#292d39] flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-[#3978d4]"></span>
            Agile User Story Editor
          </h2>
          <p className="text-xs text-[#777b87] mt-0.5">
            Format Connextra: <span className="font-mono text-[#3978d4]">Role - Action - Benefit</span> & kriteria <span className="font-semibold text-[#3978d4]">INVEST</span>
          </p>
        </div>
        <button
          onClick={onAudit}
          disabled={isLoading || !value.trim()}
          className="px-4 py-2 bg-[#3978d4] hover:bg-[#2d68c0] text-white font-semibold rounded-md transition-all disabled:opacity-50 flex items-center gap-2 text-sm"
        >
          {isLoading ? 'Menganalisis...' : 'Audit user story'}
        </button>
      </div>

      <div className="flex gap-2 mb-3">
        <span className="text-xs text-[#777b87] self-center">Template cepat:</span>
        <button
          type="button"
          onClick={insertTemplateId}
          className="text-xs px-2.5 py-1 bg-[#f7f8fa] hover:bg-[#eef3fb] text-[#555a68] rounded border border-[#e5e7ed] transition"
        >
          🇮🇩 Format ID (Sebagai... Saya ingin... Sehingga...)
        </button>
        <button
          type="button"
          onClick={insertTemplateEn}
          className="text-xs px-2.5 py-1 bg-[#f7f8fa] hover:bg-[#eef3fb] text-[#555a68] rounded border border-[#e5e7ed] transition"
        >
          🇬🇧 Format EN (As a... I want... So that...)
        </button>
      </div>

      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Tuliskan User Story dalam Bahasa Indonesia atau Bahasa Inggris...\nContoh: Sebagai pembeli, saya ingin melacak pengiriman secara real-time, sehingga saya mengetahui perkiraan kedatangan barang."
        className="w-full h-64 bg-[#fbfcfe] text-[#303440] border border-[#e3e6ed] rounded-md p-4 font-mono text-sm focus:outline-none focus:border-[#76a3dc] transition-colors resize-y leading-relaxed placeholder:text-[#a0a3ad]"
        id="user-story-input"
      />
    </div>
  );
};

