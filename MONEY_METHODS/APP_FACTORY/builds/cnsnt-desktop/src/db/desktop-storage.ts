/**
 * Desktop storage adapter for Tauri.
 *
 * Detects if running inside Tauri desktop app and uses persistent
 * disk storage (~/.cnsnt/vault.enc) instead of browser localStorage.
 * Falls back to localStorage for the web version.
 */

declare global {
  interface Window {
    __TAURI_INTERNALS__?: unknown;
  }
}

export function isTauri(): boolean {
  return typeof window !== 'undefined' && !!window.__TAURI_INTERNALS__;
}

let invokeCache: ((cmd: string, args?: Record<string, unknown>) => Promise<unknown>) | null = null;

async function getInvoke() {
  if (invokeCache) return invokeCache;
  if (!isTauri()) return null;
  try {
    const { invoke } = await import('@tauri-apps/api/core');
    invokeCache = invoke;
    return invoke;
  } catch {
    return null;
  }
}

/**
 * Save data to persistent storage.
 * Tauri: writes to ~/.cnsnt/vault.enc
 * Web: writes to localStorage
 */
export async function persistentSet(key: string, value: string): Promise<void> {
  const invoke = await getInvoke();
  if (invoke) {
    // In Tauri: save entire vault to disk as JSON envelope
    const existing = await persistentGetAll();
    existing[key] = value;
    await invoke('save_vault', { data: JSON.stringify(existing) });
  } else {
    localStorage.setItem(key, value);
  }
}

/**
 * Load data from persistent storage.
 */
export async function persistentGet(key: string): Promise<string | null> {
  const invoke = await getInvoke();
  if (invoke) {
    const all = await persistentGetAll();
    return all[key] ?? null;
  }
  return localStorage.getItem(key);
}

/**
 * Remove a key from persistent storage.
 */
export async function persistentRemove(key: string): Promise<void> {
  const invoke = await getInvoke();
  if (invoke) {
    const existing = await persistentGetAll();
    delete existing[key];
    await invoke('save_vault', { data: JSON.stringify(existing) });
  } else {
    localStorage.removeItem(key);
  }
}

/**
 * Get all stored data as a key-value map.
 */
async function persistentGetAll(): Promise<Record<string, string>> {
  const invoke = await getInvoke();
  if (!invoke) return {};
  try {
    const raw = await invoke('load_vault') as string;
    if (!raw) return {};
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

/**
 * Check if vault exists on disk (Tauri only).
 */
export async function vaultExistsOnDisk(): Promise<boolean> {
  const invoke = await getInvoke();
  if (!invoke) return false;
  try {
    return (await invoke('vault_exists')) as boolean;
  } catch {
    return false;
  }
}

/**
 * Get storage type label for UI display.
 */
export function getStorageType(): string {
  return isTauri() ? 'Desktop (disk)' : 'Browser (localStorage)';
}
