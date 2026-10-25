'use client';

import { useSyncExternalStore } from 'react';

/**
 * Store kecil di atas localStorage yang aman untuk SSR (server snapshot = nilai awal)
 * dan tersinkron antar-tab. Seluruh akses data aplikasi lewat sini, sehingga mengganti
 * localStorage dengan API/database nanti cukup mengubah satu berkas.
 */
export function createLocalStore<T>(key: string, initial: T) {
  let cachedRaw: string | null | undefined;
  let cachedValue: T = initial;
  const listeners = new Set<() => void>();

  function get(): T {
    if (typeof window === 'undefined') return initial;
    let raw: string | null = null;
    try {
      raw = window.localStorage.getItem(key);
    } catch {
      /* storage diblokir: pakai nilai awal */
    }
    if (raw === cachedRaw) return cachedValue;
    cachedRaw = raw;
    try {
      cachedValue = raw === null ? initial : (JSON.parse(raw) as T);
    } catch {
      cachedValue = initial;
    }
    return cachedValue;
  }

  function set(value: T) {
    const raw = JSON.stringify(value);
    try {
      window.localStorage.setItem(key, raw);
    } catch {
      /* kuota penuh / diblokir: tetap perbarui cache memori */
    }
    cachedRaw = raw;
    cachedValue = value;
    listeners.forEach((l) => l());
  }

  function subscribe(listener: () => void) {
    listeners.add(listener);
    const onStorage = (e: StorageEvent) => {
      if (e.key === key || e.key === null) listener();
    };
    window.addEventListener('storage', onStorage);
    return () => {
      listeners.delete(listener);
      window.removeEventListener('storage', onStorage);
    };
  }

  function useValue(): T {
    return useSyncExternalStore(subscribe, get, () => initial);
  }

  return { get, set, subscribe, useValue };
}

const noopSubscribe = () => () => {};

/** false saat SSR/hidrasi, true setelah komponen berjalan di browser. */
export function useHydrated(): boolean {
  return useSyncExternalStore(noopSubscribe, () => true, () => false);
}
