'use client';

import { Moon, Sun } from 'lucide-react';
import { useTheme } from './providers';

export function ThemeToggle() {
  const { theme, toggle } = useTheme();
  const dark = theme === 'dark';
  return (
    <button
      type="button"
      onClick={toggle}
      aria-label={dark ? 'Ganti ke tema terang' : 'Ganti ke tema gelap'}
      className="inline-flex h-10 w-10 items-center justify-center rounded-full text-muted transition hover:bg-line/[0.06] hover:text-ink"
    >
      {dark ? <Sun size={20} strokeWidth={1.6} /> : <Moon size={20} strokeWidth={1.6} />}
    </button>
  );
}
