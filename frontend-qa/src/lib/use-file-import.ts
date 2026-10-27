'use client';

import { useCallback, useState } from 'react';
import { useToast } from '@/components/providers';
import { readTextFile } from './pdf';
import { MAX_CHARS } from './validation';

const MAX_FILE_BYTES = 8 * 1024 * 1024;

/**
 * Logika bersama untuk memuat berkas PDF/TXT/MD ke editor (dipakai landing page dan halaman editor).
 * `onText` menerima teks yang sudah dipotong sesuai batas karakter.
 */
export function useFileImport(onText: (text: string) => void) {
  const toast = useToast();
  const [busy, setBusy] = useState(false);

  const onChange = useCallback(
    async (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      e.target.value = '';
      if (!file) return;
      if (file.size > MAX_FILE_BYTES) return toast('Berkas terlalu besar (maks. 8 MB).');

      setBusy(true);
      try {
        const text = (await readTextFile(file)).trim();
        if (!text) return toast('Tidak ada teks yang dapat dibaca dari berkas ini.');
        onText(text.slice(0, MAX_CHARS));
        toast(
          text.length > MAX_CHARS
            ? `Berkas dimuat dan dipotong hingga ${MAX_CHARS.toLocaleString('id-ID')} karakter.`
            : 'Berkas dimuat ke editor.',
        );
      } catch {
        toast('Gagal membaca berkas. Pastikan berkas PDF/teks tidak rusak atau terkunci.');
      } finally {
        setBusy(false);
      }
    },
    [onText, toast],
  );

  return { busy, onChange };
}
