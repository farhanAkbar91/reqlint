
import { useState, type FormEvent, type SVGProps } from "react";

type IconProps = SVGProps<SVGSVGElement>;

function CheckLogo({ className = "" }: IconProps) {
  return (
    <svg
      viewBox="0 0 32 32"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <path d="m4 16 6 6 13-13" />
      <path d="m15 16 3 3L29 8" />
    </svg>
  );
}

function EyeIcon({
  visible,
  ...props
}: IconProps & { visible: boolean }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      {visible ? (
        <>
          <path d="M3 3l18 18" />
          <path d="M10.6 10.6a2 2 0 0 0 2.8 2.8" />
          <path d="M9.9 5.2A10.8 10.8 0 0 1 12 5c5 0 8.3 4.4 9 7-.3 1.2-1 2.4-2 3.5" />
          <path d="M6.2 6.2C3.8 7.7 2.3 10.1 2 12c.7 2.6 4 7 10 7 1.1 0 2.1-.2 3-.5" />
        </>
      ) : (
        <>
          <path d="M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6S2 12 2 12Z" />
          <circle cx="12" cy="12" r="2.5" />
        </>
      )}
    </svg>
  );
}

function ArrowRight({ className = "" }: IconProps) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <path d="M5 12h14" />
      <path d="m13 6 6 6-6 6" />
    </svg>
  );
}

function ArrowLeft({ className = "" }: IconProps) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <path d="M19 12H5" />
      <path d="m11 6-6 6 6 6" />
    </svg>
  );
}

function MoonIcon({ className = "" }: IconProps) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <path d="M20.5 14.2A8.5 8.5 0 0 1 9.8 3.5 8.5 8.5 0 1 0 20.5 14.2Z" />
    </svg>
  );
}

function ShieldIcon({ className = "" }: IconProps) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.4"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <path d="M12 3 19 6v5c0 4.5-3 7.8-7 10-4-2.2-7-5.5-7-10V6l7-3Z" />
      <path d="m9 12 2 2 4-4" />
    </svg>
  );
}

export default function SignUp() {
  const [darkMode, setDarkMode] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false);
  const [accepted, setAccepted] = useState(false);
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);

  const passwordStrength = [
    password.length >= 8,
    /[A-Za-z]/.test(password) && /\d/.test(password),
    /[^A-Za-z0-9]/.test(password),
  ].filter(Boolean).length;

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    setSuccess(false);

    if (password.length < 8) {
      setMessage("Kata sandi harus minimal 8 karakter.");
      return;
    }

    if (password !== confirmPassword) {
      setMessage("Konfirmasi kata sandi tidak cocok.");
      return;
    }

    if (!accepted) {
      setMessage("Silakan setujui Ketentuan Layanan dan Kebijakan Privasi.");
      return;
    }

    // Demo frontend: belum terhubung ke backend.
    setSuccess(true);
    setMessage(
      `Formulir pendaftaran berhasil divalidasi untuk ${name}. Hubungkan backend untuk membuat akun.`
    );
  }

  const inputClass =
    "h-[56px] w-full rounded-[16px] border px-[18px] text-[15px] outline-none transition-all duration-200 placeholder:text-[#73737b] focus:border-[#a1a1aa] focus:ring-2 focus:ring-black/[0.04]";

  return (
    <main
      className={`relative flex min-h-screen flex-col overflow-x-hidden font-sans transition-colors duration-300 ${
        darkMode ? "dark-page" : "light-page"
      }`}
    >
      <style>{`
        .light-page {
          --page-text: #202023;
          --muted-text: #77777e;
          --input-bg: rgba(255,255,255,0.48);
          --input-border: #e9e9ed;
          --card-bg: rgba(255,255,255,0.65);
          --card-border: rgba(215,215,223,0.95);
          --link-color: #0068ff;
          --button-bg: #1d1d1f;
          --button-text: #fff;
          color: var(--page-text);
          background:
            radial-gradient(ellipse at 14% 10%, rgba(216,229,247,0.78), transparent 42%),
            radial-gradient(ellipse at 87% 13%, rgba(232,228,244,0.78), transparent 43%),
            linear-gradient(115deg, #f0f3fa 0%, #f8f4f3 50%, #f0eff8 100%);
        }
        .dark-page {
          --page-text: #f4f4f5;
          --muted-text: #a1a1aa;
          --input-bg: rgba(24,24,27,0.5);
          --input-border: #3f3f46;
          --card-bg: rgba(24,24,27,0.78);
          --card-border: #3f3f46;
          --link-color: #60a5fa;
          --button-bg: #fafafa;
          --button-text: #18181b;
          color: var(--page-text);
          background:
            radial-gradient(ellipse at 14% 10%, #202b40, transparent 45%),
            radial-gradient(ellipse at 87% 13%, #30253f, transparent 43%),
            linear-gradient(115deg, #111827, #18181b 55%, #211c2d);
        }
        .signup-card {
          background: var(--card-bg);
          border-color: var(--card-border);
          color: var(--page-text);
          backdrop-filter: blur(28px);
          -webkit-backdrop-filter: blur(28px);
          box-shadow: 0 20px 55px rgba(27, 31, 44, 0.08);
        }
        .signup-input {
          background: var(--input-bg);
          border-color: var(--input-border);
          color: var(--page-text);
        }
        .muted { color: var(--muted-text); }
        .signup-link { color: var(--link-color); }
        .signup-button {
          background: var(--button-bg);
          color: var(--button-text);
        }
        .strength-segment {
          height: 3px;
          flex: 1;
          border-radius: 999px;
          background: var(--input-border);
          transition: background 180ms ease;
        }
        .strength-segment.active { background: #71717a; }
        .dark-page .strength-segment.active { background: #d4d4d8; }
      `}</style>

      {/* Background decorations */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 opacity-40"
        style={{
          backgroundImage:
            "radial-gradient(#a1a1aa 0.55px, transparent 0.55px)",
          backgroundSize: "5px 5px",
          maskImage:
            "linear-gradient(to bottom, black, transparent 75%)",
        }}
      />

      {/* Header */}
      <header className="relative z-10 flex h-[78px] shrink-0 items-center justify-between px-6 sm:px-[3.3%]">
        <a
          href="#home"
          onClick={(e) => {
            e.preventDefault();
            setMessage("Anda berada di halaman pendaftaran ReqLint.");
          }}
          className="flex items-center gap-[14px] no-underline"
          aria-label="ReqLint home"
        >
          <span className="flex h-[33px] w-[33px] items-center justify-center rounded-[11px] border border-[#d6dce7] bg-white/85 text-[#24242a] shadow-sm">
            <CheckLogo className="h-[22px] w-[22px]" />
          </span>
          <span className="text-[21px] font-bold tracking-[-1px]">
            ReqLint<span className="text-[#1677ff]">.</span>
          </span>
        </a>

        <div className="flex items-center gap-5 sm:gap-7">
          <button
            type="button"
            onClick={() => {
              setMessage("Navigasi kembali ke workspace belum dihubungkan.");
            }}
            className="muted flex items-center gap-2 text-[12px] transition hover:opacity-70 sm:text-[13px]"
          >
            <ArrowLeft className="h-[15px] w-[15px]" />
            <span>Kembali ke workspace</span>
          </button>

          <button
            type="button"
            onClick={() => setDarkMode((value) => !value)}
            className="muted flex h-9 w-9 items-center justify-center rounded-full transition hover:bg-black/5 dark:hover:bg-white/10"
            aria-label={
              darkMode ? "Aktifkan mode terang" : "Aktifkan mode gelap"
            }
            title={darkMode ? "Mode terang" : "Mode gelap"}
          >
            {darkMode ? (
              <svg
                viewBox="0 0 24 24"
                className="h-5 w-5"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
              >
                <circle cx="12" cy="12" r="4" />
                <path d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42" />
              </svg>
            ) : (
              <MoonIcon className="h-5 w-5" />
            )}
          </button>
        </div>
      </header>

      {/* Main content */}
      <section
        id="home"
        className="relative z-10 flex flex-1 items-center justify-center px-4 py-5 sm:px-6 sm:py-6"
      >
        <div className="signup-card w-full max-w-[480px] rounded-[30px] border px-7 py-8 sm:px-[44px] sm:py-[44px]">
          {/* Logo */}
          <div className="mb-[27px] flex h-[54px] w-[54px] items-center justify-center rounded-[17px] border border-[#dedfe5] bg-white/80 text-[#25252a] shadow-[0_2px_5px_rgba(0,0,0,0.03)]">
            <CheckLogo className="h-[35px] w-[35px]" />
          </div>

          {/* Title */}
          <div className="mb-[28px]">
            <h1 className="text-[29px] font-semibold leading-[1.25] tracking-[-1.4px]">
              Buat akun baru
            </h1>
            <p className="muted mt-[11px] max-w-[365px] text-[14px] leading-[24px]">
              Mulai audit kualitas User Story Anda dengan standar
              ISO 29148 dan INVEST.
            </p>
          </div>

          {/* Registration form */}
          <form onSubmit={handleSubmit} noValidate>
            <div className="mb-[18px]">
              <label
                htmlFor="signup-name"
                className="mb-[9px] block text-[13px] font-medium"
              >
                Nama
              </label>
              <input
                id="signup-name"
                name="name"
                type="text"
                autoComplete="name"
                placeholder="Nama lengkap Anda"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className={`${inputClass} signup-input`}
                required
              />
            </div>

            <div className="mb-[18px]">
              <label
                htmlFor="signup-email"
                className="mb-[9px] block text-[13px] font-medium"
              >
                Email
              </label>
              <input
                id="signup-email"
                name="email"
                type="email"
                autoComplete="email"
                placeholder="nama@perusahaan.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={`${inputClass} signup-input`}
                required
              />
            </div>

            <div className="mb-[20px]">
              <label
                htmlFor="signup-password"
                className="mb-[9px] block text-[13px] font-medium"
              >
                Kata Sandi
              </label>

              <div className="relative">
                <input
                  id="signup-password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  autoComplete="new-password"
                  placeholder="Minimal 8 karakter"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className={`${inputClass} signup-input pr-[50px]`}
                  required
                  minLength={8}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((value) => !value)}
                  aria-label={
                    showPassword
                      ? "Sembunyikan kata sandi"
                      : "Tampilkan kata sandi"
                  }
                  className="muted absolute inset-y-0 right-0 flex w-[48px] items-center justify-center transition hover:opacity-60"
                >
                  <EyeIcon
                    visible={showPassword}
                    className="h-[18px] w-[18px]"
                  />
                </button>
              </div>

              <div
                className="mt-[12px] flex gap-[5px]"
                aria-label={`Kekuatan kata sandi: ${passwordStrength} dari 3`}
              >
                {[0, 1, 2].map((segment) => (
                  <span
                    key={segment}
                    className={`strength-segment ${
                      passwordStrength > segment ? "active" : ""
                    }`}
                  />
                ))}
              </div>
              <p className="muted mt-[8px] text-[10px] leading-4">
                Gunakan huruf, angka, dan simbol
              </p>
            </div>

            <div className="mb-[18px]">
              <label
                htmlFor="signup-confirm-password"
                className="mb-[9px] block text-[13px] font-medium"
              >
                Konfirmasi Kata Sandi
              </label>

              <div className="relative">
                <input
                  id="signup-confirm-password"
                  name="confirmPassword"
                  type={showConfirmPassword ? "text" : "password"}
                  autoComplete="new-password"
                  placeholder="Ulangi kata sandi Anda"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className={`${inputClass} signup-input pr-[50px]`}
                  required
                />
                <button
                  type="button"
                  onClick={() =>
                    setShowConfirmPassword((value) => !value)
                  }
                  aria-label={
                    showConfirmPassword
                      ? "Sembunyikan konfirmasi kata sandi"
                      : "Tampilkan konfirmasi kata sandi"
                  }
                  className="muted absolute inset-y-0 right-0 flex w-[48px] items-center justify-center transition hover:opacity-60"
                >
                  <EyeIcon
                    visible={showConfirmPassword}
                    className="h-[18px] w-[18px]"
                  />
                </button>
              </div>
            </div>

            {/* Terms checkbox */}
            <label className="muted mb-[19px] flex cursor-pointer items-start gap-[10px] text-[11px] leading-[18px]">
              <input
                type="checkbox"
                checked={accepted}
                onChange={(e) => setAccepted(e.target.checked)}
                className="mt-[2px] h-[17px] w-[17px] shrink-0 cursor-pointer appearance-none rounded-[5px] border border-[var(--input-border)] bg-[var(--input-bg)] checked:border-[#1d1d1f] checked:bg-[#1d1d1f] checked:after:block checked:after:ml-[4px] checked:after:mt-[1px] checked:after:h-[9px] checked:after:w-[5px] checked:after:rotate-45 checked:after:border-b-2 checked:after:border-r-2 checked:after:border-white checked:after:content-['']"
                required
              />
              <span>
                Saya menyetujui{" "}
                <a
                  href="#ketentuan-layanan"
                  onClick={(e) => {
                    e.preventDefault();
                    setMessage(
                      "Halaman Ketentuan Layanan belum dihubungkan."
                    );
                  }}
                  className="signup-link font-medium hover:underline"
                >
                  Ketentuan Layanan
                </a>{" "}
                dan{" "}
                <a
                  href="#kebijakan-privasi"
                  onClick={(e) => {
                    e.preventDefault();
                    setMessage(
                      "Halaman Kebijakan Privasi belum dihubungkan."
                    );
                  }}
                  className="signup-link font-medium hover:underline"
                >
                  Kebijakan Privasi
                </a>
              </span>
            </label>

            {/* Form feedback */}
            {message && (
              <div
                role="status"
                className={`mb-4 rounded-xl border px-3 py-3 text-xs leading-5 ${
                  success
                    ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300"
                    : "border-red-500/25 bg-red-500/5 text-red-600 dark:text-red-300"
                }`}
              >
                {message}
              </div>
            )}

            {/* Submit button */}
            <button
              type="submit"
              className="signup-button group flex h-[56px] w-full items-center justify-center rounded-[15px] text-[15px] font-medium shadow-sm transition duration-200 hover:opacity-90 active:scale-[0.99]"
            >
              <span>Daftar</span>
              <ArrowRight className="absolute right-[calc(50%-170px)] h-[17px] w-[17px] transition-transform group-hover:translate-x-1 sm:right-[65px]" />
            </button>

            {/* Sign in link */}
            <p className="muted mt-[23px] text-center text-[13px]">
              Sudah punya akun?{" "}
              <a
                href="#masuk"
                onClick={(e) => {
                  e.preventDefault();
                  setMessage("Halaman Masuk belum dihubungkan.");
                  setSuccess(false);
                }}
                className="signup-link ml-[7px] font-medium hover:underline"
              >
                Masuk
              </a>
            </p>
          </form>
        </div>
      </section>

      {/* Footer */}
      <footer className="muted relative z-10 flex min-h-[60px] shrink-0 flex-col items-center justify-between gap-3 px-6 py-4 text-[10px] sm:flex-row sm:px-[3.3%] sm:py-5">
        <span>© 2026 ReqLint</span>

        <span className="flex items-center justify-center gap-[7px] text-center">
          <ShieldIcon className="h-[14px] w-[14px] shrink-0" />
          Pratinjau interaktif. Tidak ada akun yang dibuat atau data yang dikirim.
        </span>

        <a
          href="#privasi"
          onClick={(e) => {
            e.preventDefault();
            setMessage("Halaman Privasi & Ketentuan belum dihubungkan.");
          }}
          className="whitespace-nowrap transition hover:opacity-70"
        >
          Privasi &amp; Ketentuan
        </a>
      </footer>
    </main>
  );
}
