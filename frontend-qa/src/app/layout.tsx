import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ReqLint - Agile User Story Quality Assurance & INVEST Linter',
  description: 'Automated Agile User Story linting and quality assurance based on INVEST criteria and Connextra format.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-100 min-h-screen">
        <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center font-bold text-slate-950">
                RL
              </div>
              <span className="text-xl font-bold tracking-tight text-slate-100">
                Req<span className="text-emerald-400">Lint</span>
              </span>
              <span className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-md font-medium">
                User Story Focus
              </span>
            </div>
            <div className="text-xs font-mono text-slate-400 bg-slate-800 px-3 py-1 rounded-full">
              Bilingual INVEST Linter (ID / EN)
            </div>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-6 py-8">{children}</main>

      </body>
    </html>
  );
}
