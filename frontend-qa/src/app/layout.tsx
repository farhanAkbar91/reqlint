import type { Metadata } from 'next';
import Link from 'next/link';
import './globals.css';

export const metadata: Metadata = {
  title: 'ReqLint - Analisis Kebutuhan',
  description: 'Automated Agile User Story linting and quality assurance based on INVEST criteria and Connextra format.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <body className="min-h-screen bg-[#f3f4f8] text-[#242631]">
        <header className="sticky top-0 z-50 border-b border-white/80 bg-white/80 backdrop-blur-xl">
          <div className="mx-auto flex h-[68px] max-w-[1320px] items-center gap-7 px-5 sm:px-8">
            <Link href="/" className="flex shrink-0 items-center gap-2.5 text-lg font-bold tracking-tight text-[#242631]">
              <span className="grid h-8 w-8 place-items-center rounded-[9px] bg-[#3978d4] text-xs font-bold text-white">RL</span>
              ReqLint<span className="-ml-2 text-[#3978d4]">.</span>
            </Link>
            <nav aria-label="Navigasi utama" className="flex items-center gap-1 rounded-lg bg-[#f3f4f7] p-1 text-xs font-semibold">
              <Link href="/" className="rounded-md bg-white px-3.5 py-2 text-[#343845] shadow-sm">Editor</Link>
              <Link href="/audit/hasilAudit" className="rounded-md px-3.5 py-2 text-[#737783] transition hover:text-[#343845]">Hasil audit</Link>
            </nav>
            <span className="ml-auto hidden text-xs text-[#777b87] sm:block">Personal workspace</span>
            <span className="grid h-8 w-8 place-items-center rounded-full bg-[#e8edf5] text-[10px] font-bold text-[#53627b]">RL</span>
          </div>
        </header>
        <main className="mx-auto min-h-[calc(100vh-68px)] max-w-[1320px] px-4 py-6 sm:px-6">{children}</main>
      </body>
    </html>
  );
}
