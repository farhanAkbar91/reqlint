# ReqLint

Prototype frontend React yang terinspirasi dari screenshot ReqLint. Memiliki halaman daftar, editor User Story, hasil audit, contoh template, upload PDF (ekstraksi teks dasar), revisi, dan ekspor laporan.

## Instalasi lokal

1. Install **Node.js LTS** dari https://nodejs.org/ (npm ikut terpasang).
2. Ekstrak ZIP ini.
3. Buka terminal di folder `reqlint`, lalu jalankan:

   ```bash
   npm install
   npm run dev
   ```

4. Buka URL yang ditampilkan Vite, biasanya `http://localhost:5173`.

## Build production

```bash
npm run build
npm run preview
```

Hasil build ada di folder `dist/`.

## Upload ke GitHub

1. Buat repository baru di GitHub.
2. Ekstrak ZIP, lalu buka terminal pada folder project.
3. Jalankan:

   ```bash
   git init
   git add .
   git commit -m "Initial ReqLint prototype"
   git branch -M main
   git remote add origin https://github.com/USERNAME/NAMA-REPO.git
   git push -u origin main
   ```

   Ganti URL remote dengan URL repository milikmu.

## Deploy

Bisa di-deploy di Vercel atau Netlify dengan build command `npm run build` dan output directory `dist`.

## Catatan

Ini adalah prototype frontend: data akun/draft disimpan lokal di browser, bukan database/server. Analisis berjalan dengan aturan heuristik di sisi client, bukan AI/backend sungguhan. Login, registrasi, upload PDF, dan ekspor merupakan demo tanpa layanan autentikasi atau penyimpanan server. Jangan gunakan untuk menyimpan kata sandi asli.
