import type { Metadata, Viewport } from 'next';
import '@fontsource-variable/inter';
import './globals.css';
import { Providers } from '@/components/providers';

export const metadata: Metadata = {
  title: { default: 'ReqLint — Audit Kualitas User Story', template: '%s · ReqLint' },
  description: 'Audit kualitas User Story dengan standar ISO 29148 dan INVEST.',
  icons: { icon: '/favicon.svg' },
};

export const viewport: Viewport = {
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#f1f1f6' },
    { media: '(prefers-color-scheme: dark)', color: '#0c0c10' },
  ],
};

// Terapkan tema tersimpan sebelum render pertama agar tidak berkedip.
const themeScript = `try{if(JSON.parse(localStorage.getItem('reqlint.theme'))==='dark')document.documentElement.classList.add('dark')}catch(e){}`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
