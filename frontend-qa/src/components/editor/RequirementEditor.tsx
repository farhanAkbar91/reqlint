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
  return (
    <div className="flex flex-col h-full bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
      <div className="flex justify-between items-center mb-3">
        <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
          SRS Requirement Editor
        </h2>
        <button
          onClick={onAudit}
          disabled={isLoading || !value.trim()}
          className="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-lg transition-all disabled:opacity-50 flex items-center gap-2"
        >
          {isLoading ? 'Analyzing NLP...' : 'Run ReqLint Audit'}
        </button>
      </div>

      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Masukkan dokumen SRS atau User Story dalam Bahasa Indonesia atau Bahasa Inggris..."
        className="w-full h-64 bg-slate-950 text-slate-100 border border-slate-800 rounded-lg p-4 font-mono text-sm focus:outline-none focus:border-emerald-500 transition-colors resize-none"
        id="srs-requirement-input"
      />
    </div>
  );
};
