import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Upload Dokumen PDF - ReqLint',
  description: 'Unggah dokumen SRS atau user story dalam format PDF untuk analisis kualitas requirement otomatis.',
};

export default function UploadLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
