'use client';

import { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react';
import { createLocalStore } from '@/lib/store';

// ───────────── Tema ─────────────
type Theme = 'light' | 'dark';
const themeStore = createLocalStore<Theme>('reqlint.theme', 'light');

export function useTheme() {
  const theme = themeStore.useValue();
  const toggle = useCallback(() => {
    themeStore.set(themeStore.get() === 'dark' ? 'light' : 'dark');
  }, []);
  return { theme, toggle };
}

// ───────────── Toast ─────────────
type ToastFn = (message: string) => void;
const ToastContext = createContext<ToastFn>(() => {});
export const useToast = () => useContext(ToastContext);

export function Providers({ children }: { children: React.ReactNode }) {
  const theme = themeStore.useValue();
  const [message, setMessage] = useState<string | null>(null);
  const timer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, [theme]);

  const toast = useCallback<ToastFn>((m) => {
    setMessage(m);
    clearTimeout(timer.current);
    timer.current = setTimeout(() => setMessage(null), 2600);
  }, []);

  return (
    <ToastContext.Provider value={toast}>
      {children}
      {message && (
        <div
          role="status"
          aria-live="polite"
          className="animate-toast fixed bottom-6 left-1/2 z-[100] max-w-[90vw] -translate-x-1/2 rounded-full bg-btn px-5 py-2.5 text-[13.5px] font-medium text-btnink shadow-card"
        >
          {message}
        </div>
      )}
    </ToastContext.Provider>
  );
}
