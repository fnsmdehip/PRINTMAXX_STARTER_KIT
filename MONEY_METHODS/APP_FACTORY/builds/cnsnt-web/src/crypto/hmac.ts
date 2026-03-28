/**
 * HMAC-SHA-256 integrity verification
 * Uses Web Crypto API - ZERO external libraries
 */

const HMAC_KEY_STORAGE = 'cnsnt_hmac_key';

async function getOrCreateHmacKey(): Promise<CryptoKey> {
  const stored = localStorage.getItem(HMAC_KEY_STORAGE);

  if (stored) {
    const keyData = Uint8Array.from(atob(stored), (c) => c.charCodeAt(0));
    return crypto.subtle.importKey(
      'raw',
      keyData,
      { name: 'HMAC', hash: 'SHA-256' },
      true,
      ['sign', 'verify']
    );
  }

  const key = await crypto.subtle.generateKey(
    { name: 'HMAC', hash: 'SHA-256' },
    true,
    ['sign', 'verify']
  );

  const exported = await crypto.subtle.exportKey('raw', key);
  const bytes = new Uint8Array(exported);
  let binary = '';
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  localStorage.setItem(HMAC_KEY_STORAGE, btoa(binary));

  return key;
}

export async function computeHmac(data: string): Promise<string> {
  const key = await getOrCreateHmacKey();
  const encoder = new TextEncoder();
  const signature = await crypto.subtle.sign('HMAC', key, encoder.encode(data));
  const bytes = new Uint8Array(signature);
  let binary = '';
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

export async function verifyHmac(data: string, hmacB64: string): Promise<boolean> {
  const key = await getOrCreateHmacKey();
  const encoder = new TextEncoder();
  const signature = Uint8Array.from(atob(hmacB64), (c) => c.charCodeAt(0));
  return crypto.subtle.verify('HMAC', key, signature, encoder.encode(data));
}

export async function computeChainHash(content: string, prevHash: string): Promise<string> {
  const combined = prevHash + '|' + content;
  return computeHmac(combined);
}
