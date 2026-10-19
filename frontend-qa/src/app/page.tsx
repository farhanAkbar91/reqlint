'use client';

import React, { useState } from 'react';
import { RequirementEditor } from '../components/editor/RequirementEditor';
import { AuditScorecard } from '../components/analysis/AuditScorecard';
import { SmellList } from '../components/analysis/SmellList';
import { auditRequirement } from '../lib/api';
import { AuditResponse } from '../types/audit';

export default function HomePage() {
  const [text, setText] = useState(
    'Sebagai pembeli, saya sebaiknya dapat membayar transaksi dengan cepat, sehingga pesanan segera diproses.'
  );

  const [auditResult, setAuditResult] = useState<AuditResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAudit = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await auditRequirement(text);
      setAuditResult(res);
    } catch (err: any) {
      setError(err.message || 'Failed to analyze requirement');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="space-y-4">
        <RequirementEditor
          value={text}
          onChange={setText}
          onAudit={handleAudit}
          isLoading={isLoading}
        />
        {error && (
          <div className="p-4 bg-rose-950 border border-rose-800 text-rose-300 text-sm rounded-xl">
            {error}
          </div>
        )}
      </div>

      <div className="space-y-6">
        <AuditScorecard auditResult={auditResult} />
        {auditResult && (
          <SmellList smells={auditResult.smells} revisions={auditResult.revisions} />
        )}
      </div>
    </div>
  );
}
