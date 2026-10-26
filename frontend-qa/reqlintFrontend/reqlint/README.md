# ReqLint.

Audit kualitas **User Story** dan kebutuhan perangkat lunak dengan acuan **ISO/IEC/IEEE 29148** dan **INVEST**.
Tempel atau unggah draf kebutuhan (teks / PDF), dapatkan skor kualitas, daftar temuan cacat, saran revisi,
draf acceptance criteria (BDD), dan diff sebelum/sesudah.

> Pratinjau interaktif. Analisis berjalan **di browser** — draf Anda tidak dikirim ke server.

## Fitur

- **Landing page** publik di `/` (hero + demo analisis tanpa login, fitur, cara kerja, standar, privasi, FAQ).
- **Editor real-time** — nomor baris dan garis bergelombang pada istilah tidak terukur saat mengetik.
- **Upload** PDF / TXT / MD (PDF dibaca di browser dengan `pdfjs-dist`) dan contoh template.
- **Quality Scorecard** (0–100), ringkasan per kategori, kepatuhan ISO 29148 & INVEST (dengan detail I-N-V-E-S-T).
- **Temuan cacat**: Ambiguity, Non-Testable, Tidak Lengkap, Weak Directive, Passive Voice — lengkap dengan lokasi & rekomendasi.
- **Saran revisi otomatis**, **Acceptance Criteria (Given/When/Then)**, dan **Diff Viewer** tingkat kata.
- **History Audit** (cari, buka, hapus), **Export** Markdown / CSV / JSON, **Salin Hasil**.
- Bahasa analisis **Indonesia** dan **English**, **dark mode**, responsif hingga mobile.
- Login / daftar (demo, lihat [Batasan](#batasan-yang-perlu-diketahui)).
- `POST /api/analyze` untuk integrasi (CI, skrip, tool lain).

## Tech stack

Next.js (App Router) · React · TypeScript (strict) · Tailwind CSS 3 · Zod · Vitest · lucide-react · pdfjs-dist

## Instalasi

**Prasyarat:** [Node.js](https://nodejs.org) **20.9 atau lebih baru** (disarankan 22; ada berkas `.nvmrc`) dan npm.

```bash
# 1. masuk ke folder project (setelah zip diekstrak)
cd reqlint

# 2. pasang dependensi
npm install

# 3. jalankan mode pengembangan
npm run dev
```

Buka <http://localhost:3000>. Klik **Gunakan akun demo** di halaman login untuk langsung masuk.

### Perintah lain

| Perintah            | Fungsi                                                          |
| ------------------- | --------------------------------------------------------------- |
| `npm run dev`       | Server pengembangan dengan hot reload                           |
| `npm run build`     | Build produksi                                                  |
| `npm start`         | Menjalankan hasil build (jalankan `npm run build` dulu)         |
| `npm test`          | Unit test mesin analisis (Vitest)                               |
| `npm run typecheck` | Pengecekan tipe TypeScript                                      |
| `npm run check`     | Typecheck + test + build sekaligus (sama seperti CI)            |

Port lain: `npm run dev -- -p 4000`.

### Akun demo

Email `demo@reqlint.app` · kata sandi `demo12345` (atau tombol **Gunakan akun demo**). Anda juga bisa mendaftar akun sendiri —
tersimpan lokal di browser.

## Struktur project

```
src/
├─ app/
│  ├─ page.tsx                   # landing page publik (/)
│  ├─ (auth)/login, register     # halaman masuk & daftar
│  ├─ (app)/                     # area terproteksi (layout = AppShell + guard login)
│  │  ├─ editor/                 # Editor User Story
│  │  ├─ audit/[id]/             # Hasil Audit
│  │  └─ history/                # History Audit
│  └─ api/analyze/route.ts       # REST endpoint (validasi Zod)
├─ components/                   # UI: app-shell, code-editor, audit/*, auth/*, landing/*, popover, providers
└─ lib/
   ├─ analyzer/                  # ★ mesin audit — fungsi murni, tanpa dependensi UI, ada unit test
   │  ├─ rules.ts                #   kamus & regex aturan (tambah aturan di sini)
   │  ├─ clauses.ts              #   pemecah kalimat/klausul + offset
   │  ├─ analyze.ts              #   deteksi temuan, skor, ISO 29148, INVEST
   │  ├─ revise.ts               #   draf revisi + acceptance criteria BDD
   │  ├─ diff.ts                 #   diff tingkat kata (LCS)
   │  └─ analyzer.test.ts
   ├─ store.ts                   # store localStorage aman-SSR (satu-satunya akses penyimpanan)
   ├─ auth.ts · audits.ts        # lapisan data (ganti dengan API/DB nanti)
   ├─ validation.ts              # skema Zod (form & API)
   └─ export.ts · pdf.ts · templates.ts · format.ts
```

Prinsip desain: **mesin analisis dipisah dari UI** (mudah dites & dipakai ulang di server/CLI), **seluruh akses data lewat
`lib/auth.ts` dan `lib/audits.ts`** (mengganti localStorage dengan backend cukup mengubah dua berkas itu), dan hasil audit
**selalu dihitung ulang dari teks** sehingga tidak ada data turunan yang kedaluwarsa.

## Cara kerja analisis

Mesin bersifat **rule-based dan deterministik** (bukan model AI): input yang sama selalu menghasilkan hasil yang sama.

| Kategori          | Contoh yang dideteksi                                               | Bobot skor |
| ----------------- | ------------------------------------------------------------------- | ---------- |
| Ambiguity         | sangat cepat, beberapa, secepatnya, yang sesuai, aman, fleksibel    | −14        |
| Non-Testable      | user-friendly, mudah digunakan, intuitif, menarik, modern           | −16        |
| Tidak Lengkap     | dll, dsb, TBD; user story tanpa peran / tujuan / manfaat; klausul sangat pendek | −18 |
| Weak Directive    | sebaiknya, mungkin, diharapkan, kalau bisa                          | −10        |
| Passive Voice     | harus disimpan, dikirim oleh …                                      | −12        |

- **Skor** = `100 − Σ bobot / max(1, √(jumlah klausul / 2))` (diredam agar teks panjang tidak langsung 0).
  Grade: ≥ 85 Excellent · ≥ 70 Good · ≥ 40 Needs Improvement · selainnya Poor.
- **ISO 29148** = persentase lulus dari 5 kriteria per klausul (tidak ambigu, dapat diverifikasi, lengkap, direktif kuat, aktif).
- **INVEST** = persentase dari 6 pemeriksaan (Independent, Negotiable, Valuable, Estimable, Small, Testable).
- **Saran revisi**: mengganti istilah tidak terukur dengan **nilai contoh** (mis. "kurang dari 2 detik", "maksimal 3 langkah"),
  menulis ulang kalimat pasif untuk kata kerja yang dikenal, dan menormalkan "user" → "pengguna". Angka tersebut
  harus disesuaikan tim — UI menandainya.

### Menambah aturan baru

Tambahkan satu entri di `TERM_RULES` pada `src/lib/analyzer/rules.ts`:

```ts
{
  id: 'id.my-rule',
  lang: 'id',
  category: 'ambiguity',
  pattern: word('semudah mungkin|secukupnya'),
  recommendation: 'Jelaskan kriteria yang dapat diukur.',
  replacement: '…', // opsional, dipakai pada draf revisi
}
```

Lalu tambahkan kasus uji di `analyzer.test.ts` dan jalankan `npm test`.

## API

```bash
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Sebagai user, saya ingin login sangat cepat agar hemat waktu.","language":"id"}'
```

Respons: `{ result, revision }` (skor, temuan, kepatuhan, saran revisi). Input tidak valid → `422` dengan detail per field.

## Deploy

**Vercel (paling mudah):** push ke GitHub → <https://vercel.com/new> → impor repo → Deploy (tanpa konfigurasi tambahan).

**Server sendiri / VPS:**

```bash
npm ci && npm run build
npm start            # default port 3000; ubah dengan: npm start -- -p 8080
```

> Catatan: karena ada route dinamis `/audit/[id]` dan endpoint API, project ini membutuhkan runtime Node.js
> (bukan hosting statis murni seperti GitHub Pages).

## Upload ke GitHub

1. Buat repository kosong di <https://github.com/new> (misal `reqlint`; jangan centang README/.gitignore karena sudah ada).
2. Di folder project:

```bash
git init
git add .
git commit -m "feat: initial ReqLint (Next.js)"
git branch -M main
git remote add origin https://github.com/<username>/reqlint.git
git push -u origin main
```

Folder `node_modules/` dan `.next/` otomatis diabaikan oleh `.gitignore`. Workflow CI (`.github/workflows/ci.yml`) akan
menjalankan typecheck, test, dan build pada setiap push/pull request.

## Batasan yang perlu diketahui

- **Auth hanyalah demo.** Akun, sesi, dan riwayat audit disimpan di `localStorage` browser (kata sandi di-hash SHA-256, tetapi
  ini **bukan** autentikasi produksi). Data tidak tersinkron antar perangkat dan hilang jika data situs dihapus.
  Untuk produksi: ganti `lib/auth.ts` dengan Auth.js (atau sejenis) dan `lib/audits.ts` dengan database.
- **Bukan AI.** Deteksi berbasis kamus & regex; kata yang tidak ada di kamus tidak terdeteksi, dan deteksi kalimat pasif
  berbahasa Indonesia berupa heuristik (ada daftar pengecualian untuk kata berawalan "di-" yang bukan pasif).
  Hasilnya alat bantu review, bukan pengganti penilaian analis.
- Halaman Ketentuan Layanan / Kebijakan Privasi dan reset kata sandi belum ada (tombolnya menampilkan notifikasi).
- Batas teks 20.000 karakter di editor dan 8 MB per berkas unggahan.

## Roadmap ide

Database + Auth.js · berbagi hasil audit via tautan · aturan kustom per tim · integrasi Jira/GitHub Issues ·
penyempurnaan saran revisi dengan LLM (opsional, dengan persetujuan pengguna).
