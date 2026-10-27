import type { Language } from './analyzer';

export interface Template {
  id: string;
  label: Record<Language, string>;
  text: Record<Language, string>;
}

/** Contoh draf yang sengaja memuat cacat umum agar fitur audit mudah dicoba. */
export const TEMPLATES: Template[] = [
  {
    id: 'login',
    label: { id: 'Fitur Login', en: 'Login feature' },
    text: {
      id: 'Sebagai user, saya ingin proses login sistem berjalan dengan sangat cepat dan user-friendly agar tidak membuang waktu.\nData sesi pengguna harus disimpan oleh sistem.',
      en: 'As a user, I want the login process to be fast and user-friendly so that I do not waste time.\nUser session data should be stored by the system.',
    },
  },
  {
    id: 'report',
    label: { id: 'Laporan Penjualan', en: 'Sales report' },
    text: {
      id: 'Sebagai manajer, saya ingin laporan penjualan ditampilkan secepatnya dengan tampilan yang menarik.\nLaporan sebaiknya dapat diekspor ke PDF, Excel, dll.\nSebagai manajer, saya ingin melihat tren penjualan.',
      en: 'As a manager, I want the sales report to be shown as quickly as possible with an attractive layout.\nThe report should be exportable to PDF, Excel, etc.\nAs a manager, I want to see sales trends.',
    },
  },
  {
    id: 'checkout',
    label: { id: 'Checkout Pembayaran', en: 'Payment checkout' },
    text: {
      id: 'Sebagai pembeli, saya ingin proses pembayaran aman dan mudah digunakan agar yakin menyelesaikan pesanan.\nNotifikasi konfirmasi pesanan akan dikirim ke email pembeli.\nSistem mungkin mendukung banyak metode pembayaran.',
      en: 'As a buyer, I want the payment process to be secure and easy to use so that I feel confident completing my order.\nOrder confirmation will be sent to the buyer by email.\nThe system may support many payment methods.',
    },
  },
  {
    id: 'good',
    label: { id: 'Contoh yang sudah baik', en: 'A well-formed example' },
    text: {
      id: 'Sebagai pengguna, saya ingin masuk ke aplikasi dalam waktu kurang dari 2 detik agar dapat langsung mengakses dashboard.\nSistem harus menyimpan data sesi pengguna selama 30 menit.',
      en: 'As a user, I want to sign in within 2 seconds so that I can open the dashboard immediately.\nThe system shall store user session data for 30 minutes.',
    },
  },
];
