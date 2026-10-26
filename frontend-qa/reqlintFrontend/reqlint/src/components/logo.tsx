import { CheckCheck } from 'lucide-react';
import Link from 'next/link';

export function LogoMark({ size = 48 }: { size?: number }) {
  return (
    <span
      className="inline-flex items-center justify-center rounded-[14px] border border-line/[0.06] bg-card shadow-soft"
      style={{ width: size, height: size }}
    >
      <CheckCheck size={size * 0.46} strokeWidth={2.2} className="text-ink" aria-hidden />
    </span>
  );
}

export function Wordmark({ className = 'text-[24px]' }: { className?: string }) {
  return (
    <span className={`font-bold tracking-tight text-ink ${className}`}>
      ReqLint<span className="text-accent">.</span>
    </span>
  );
}

export function Logo({ href = '/', small = false }: { href?: string; small?: boolean }) {
  return (
    <Link href={href} className="inline-flex items-center" aria-label="ReqLint">
      <Wordmark className={small ? 'text-[20px]' : 'text-[26px]'} />
    </Link>
  );
}
