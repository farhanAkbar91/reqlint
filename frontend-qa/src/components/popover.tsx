'use client';

import { useEffect, useRef, useState } from 'react';

interface PopoverProps {
  /** Render tombol pemicu. */
  trigger: (state: { open: boolean; toggle: () => void }) => React.ReactNode;
  /** Isi menu; `close` menutup popover. */
  children: (close: () => void) => React.ReactNode;
  align?: 'left' | 'right';
  className?: string;
}

/** Popover sederhana: tutup saat klik di luar atau menekan Escape. */
export function Popover({ trigger, children, align = 'left', className = '' }: PopoverProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onDown = (e: MouseEvent) => {
      if (!ref.current?.contains(e.target as Node)) setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setOpen(false);
    document.addEventListener('mousedown', onDown);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDown);
      document.removeEventListener('keydown', onKey);
    };
  }, [open]);

  return (
    <div ref={ref} className={`relative ${className}`}>
      {trigger({ open, toggle: () => setOpen((o) => !o) })}
      {open && (
        <div className={`menu ${align === 'right' ? 'right-0' : 'left-0'}`} role="menu">
          {children(() => setOpen(false))}
        </div>
      )}
    </div>
  );
}
