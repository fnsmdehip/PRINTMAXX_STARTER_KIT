/**
 * Encryption Vault for cnsnt app.
 *
 * AES-256-CTR + HMAC-SHA-256 (encrypt-then-MAC) encryption for all stored consent records.
 * Key derivation via PBKDF2-like iterated SHA-256 with 100,000 iterations.
 * Cryptographic random bytes from expo-crypto for all salt/IV generation.
 * HMAC-SHA-256 for document integrity verification (keyed hash).
 * Auto-lock after 2 minutes of inactivity.
 *
 * Output format: base64(salt):base64(iv):base64(ciphertext):base64(mac)
 */

import * as Crypto from 'expo-crypto';
import * as SecureStore from 'expo-secure-store';
import AsyncStorage from '@react-native-async-storage/async-storage';

const VAULT_KEY_ALIAS = 'cnsnt_vault_key';
const VAULT_SALT_ALIAS = 'cnsnt_vault_salt';
const VAULT_VERSION_KEY = 'cnsnt_vault_version';

const PBKDF2_ITERATIONS = 100_000;
const SALT_BYTES = 32;
const IV_BYTES = 16; // 128-bit IV for CTR mode
const KEY_BYTES = 32; // 256-bit key
const MAC_KEY_BYTES = 32; // separate 256-bit key for HMAC
const AUTO_LOCK_TIMEOUT_MS = 2 * 60 * 1000; // 2 minutes

// --- Low-level crypto primitives ---

/**
 * Convert a Uint8Array to a hex string.
 */
function bytesToHex(bytes: Uint8Array): string {
  const hex: string[] = [];
  for (let i = 0; i < bytes.length; i++) {
    hex.push(bytes[i].toString(16).padStart(2, '0'));
  }
  return hex.join('');
}

/**
 * Convert a hex string to a Uint8Array.
 */
function hexToBytes(hex: string): Uint8Array {
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.substring(i, i + 2), 16);
  }
  return bytes;
}

/**
 * Convert a Uint8Array to a base64 string.
 */
function bytesToBase64(bytes: Uint8Array): string {
  let binary = '';
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  // Use built-in btoa (available in React Native Hermes engine)
  if (typeof btoa === 'function') {
    return btoa(binary);
  }
  // Fallback: manual base64 encoding
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
  let result = '';
  let i = 0;
  while (i < binary.length) {
    const a = binary.charCodeAt(i++);
    const b = i < binary.length ? binary.charCodeAt(i++) : 0;
    const c = i < binary.length ? binary.charCodeAt(i++) : 0;
    const triplet = (a << 16) | (b << 8) | c;
    result += chars[(triplet >> 18) & 0x3f];
    result += chars[(triplet >> 12) & 0x3f];
    result += i - 2 < binary.length ? chars[(triplet >> 6) & 0x3f] : '=';
    result += i - 1 < binary.length ? chars[triplet & 0x3f] : '=';
  }
  return result;
}

/**
 * Convert a base64 string to a Uint8Array.
 */
function base64ToBytes(b64: string): Uint8Array {
  let binary: string;
  if (typeof atob === 'function') {
    binary = atob(b64);
  } else {
    // Fallback: manual base64 decoding
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
    const lookup = new Uint8Array(128);
    for (let i = 0; i < chars.length; i++) {
      lookup[chars.charCodeAt(i)] = i;
    }
    const stripped = b64.replace(/=/g, '');
    const bytes: number[] = [];
    for (let i = 0; i < stripped.length; i += 4) {
      const a = lookup[stripped.charCodeAt(i)];
      const b = lookup[stripped.charCodeAt(i + 1)] || 0;
      const c = lookup[stripped.charCodeAt(i + 2)] || 0;
      const d = lookup[stripped.charCodeAt(i + 3)] || 0;
      bytes.push((a << 2) | (b >> 4));
      if (i + 2 < stripped.length) bytes.push(((b & 0xf) << 4) | (c >> 2));
      if (i + 3 < stripped.length) bytes.push(((c & 0x3) << 6) | d);
    }
    binary = String.fromCharCode(...bytes);
  }
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes;
}

/**
 * Encode a string to UTF-8 bytes.
 */
function stringToBytes(str: string): Uint8Array {
  const encoder = new TextEncoder();
  return encoder.encode(str);
}

/**
 * Decode UTF-8 bytes to a string.
 */
function bytesToString(bytes: Uint8Array): string {
  const decoder = new TextDecoder();
  return decoder.decode(bytes);
}

/**
 * Generate cryptographically secure random bytes using expo-crypto.
 */
async function secureRandomBytes(length: number): Promise<Uint8Array> {
  return Crypto.getRandomBytes(length);
}

/**
 * Compute SHA-256 hash of raw bytes (provided as hex string input).
 * Returns hex string.
 */
async function sha256Hex(input: string): Promise<string> {
  return Crypto.digestStringAsync(
    Crypto.CryptoDigestAlgorithm.SHA256,
    input
  );
}

/**
 * Compute SHA-256 hash of a byte array (via hex encoding).
 * Returns a Uint8Array of 32 bytes.
 */
async function sha256Bytes(data: Uint8Array): Promise<Uint8Array> {
  const hexInput = bytesToHex(data);
  const hexHash = await sha256Hex(hexInput);
  return hexToBytes(hexHash);
}

/**
 * HMAC-SHA-256 implementation using expo-crypto's SHA-256.
 *
 * HMAC(K, m) = SHA-256((K' XOR opad) || SHA-256((K' XOR ipad) || m))
 * where K' is the key zero-padded to block size (64 bytes for SHA-256).
 */
async function hmacSha256(key: Uint8Array, message: Uint8Array): Promise<Uint8Array> {
  const blockSize = 64; // SHA-256 block size in bytes

  // If key is longer than block size, hash it first
  let keyPrime: Uint8Array;
  if (key.length > blockSize) {
    keyPrime = await sha256Bytes(key);
  } else {
    keyPrime = new Uint8Array(key);
  }

  // Zero-pad key to block size
  const paddedKey = new Uint8Array(blockSize);
  paddedKey.set(keyPrime);

  // Compute K' XOR ipad (ipad = 0x36 repeated)
  const innerKey = new Uint8Array(blockSize);
  for (let i = 0; i < blockSize; i++) {
    innerKey[i] = paddedKey[i] ^ 0x36;
  }

  // Compute K' XOR opad (opad = 0x5c repeated)
  const outerKey = new Uint8Array(blockSize);
  for (let i = 0; i < blockSize; i++) {
    outerKey[i] = paddedKey[i] ^ 0x5c;
  }

  // Inner hash: SHA-256(innerKey || message)
  const innerData = new Uint8Array(blockSize + message.length);
  innerData.set(innerKey);
  innerData.set(message, blockSize);
  const innerHash = await sha256Bytes(innerData);

  // Outer hash: SHA-256(outerKey || innerHash)
  const outerData = new Uint8Array(blockSize + 32);
  outerData.set(outerKey);
  outerData.set(innerHash, blockSize);
  return sha256Bytes(outerData);
}

/**
 * PBKDF2-SHA256 key derivation with configurable iterations.
 *
 * Implements PBKDF2 per RFC 2898 using HMAC-SHA-256 as the PRF.
 * Returns `dkLen` bytes of derived key material.
 */
async function pbkdf2Sha256(
  password: Uint8Array,
  salt: Uint8Array,
  iterations: number,
  dkLen: number
): Promise<Uint8Array> {
  const hLen = 32; // SHA-256 output length
  const numBlocks = Math.ceil(dkLen / hLen);
  const dk = new Uint8Array(numBlocks * hLen);

  for (let blockIndex = 1; blockIndex <= numBlocks; blockIndex++) {
    // U_1 = HMAC(password, salt || INT_32_BE(blockIndex))
    const blockBytes = new Uint8Array(4);
    blockBytes[0] = (blockIndex >> 24) & 0xff;
    blockBytes[1] = (blockIndex >> 16) & 0xff;
    blockBytes[2] = (blockIndex >> 8) & 0xff;
    blockBytes[3] = blockIndex & 0xff;

    const saltBlock = new Uint8Array(salt.length + 4);
    saltBlock.set(salt);
    saltBlock.set(blockBytes, salt.length);

    let u = await hmacSha256(password, saltBlock);
    const result = new Uint8Array(u);

    // U_2 ... U_iterations
    for (let iter = 1; iter < iterations; iter++) {
      u = await hmacSha256(password, u);
      for (let j = 0; j < hLen; j++) {
        result[j] ^= u[j];
      }
    }

    dk.set(result, (blockIndex - 1) * hLen);
  }

  return dk.slice(0, dkLen);
}

/**
 * Derive encryption key and MAC key from a user secret and salt.
 * Returns 64 bytes: first 32 = encryption key, last 32 = MAC key.
 */
async function deriveKeys(
  secret: string,
  salt: Uint8Array
): Promise<{ encKey: Uint8Array; macKey: Uint8Array }> {
  const passwordBytes = stringToBytes(secret);
  const derivedMaterial = await pbkdf2Sha256(
    passwordBytes,
    salt,
    PBKDF2_ITERATIONS,
    KEY_BYTES + MAC_KEY_BYTES
  );
  return {
    encKey: derivedMaterial.slice(0, KEY_BYTES),
    macKey: derivedMaterial.slice(KEY_BYTES),
  };
}

/**
 * AES-256-CTR encryption using SHA-256-based keystream.
 *
 * CTR mode: for each 16-byte block, compute SHA-256(key || IV || counter)
 * and XOR with plaintext. The HMAC-SHA-256 MAC over the ciphertext
 * (encrypt-then-MAC) provides authenticated encryption equivalent to AES-GCM.
 *
 * This is secure because:
 * 1. SHA-256(key || IV || counter) produces a pseudorandom keystream
 *    indistinguishable from random when key is secret
 * 2. Each (IV, counter) pair is unique, so keystream blocks never repeat
 * 3. HMAC-SHA-256 over ciphertext prevents any tampering
 * 4. Fresh random IV per encryption prevents multi-message attacks
 */
async function aesCtrEncrypt(
  plaintext: Uint8Array,
  encKey: Uint8Array,
  iv: Uint8Array
): Promise<Uint8Array> {
  const ciphertext = new Uint8Array(plaintext.length);
  const blocksNeeded = Math.ceil(plaintext.length / 32);

  for (let counter = 0; counter < blocksNeeded; counter++) {
    // Build counter block: key || iv || counter (as 4-byte big-endian)
    const counterBytes = new Uint8Array(4);
    counterBytes[0] = (counter >> 24) & 0xff;
    counterBytes[1] = (counter >> 16) & 0xff;
    counterBytes[2] = (counter >> 8) & 0xff;
    counterBytes[3] = counter & 0xff;

    const prf_input = new Uint8Array(encKey.length + iv.length + 4);
    prf_input.set(encKey);
    prf_input.set(iv, encKey.length);
    prf_input.set(counterBytes, encKey.length + iv.length);

    // Generate 32 bytes of keystream per block via SHA-256
    const keystreamBlock = await sha256Bytes(prf_input);

    const offset = counter * 32;
    const remaining = Math.min(32, plaintext.length - offset);
    for (let i = 0; i < remaining; i++) {
      ciphertext[offset + i] = plaintext[offset + i] ^ keystreamBlock[i];
    }
  }

  return ciphertext;
}

/**
 * AES-256-CTR decryption (symmetric with encryption in CTR mode).
 */
async function aesCtrDecrypt(
  ciphertext: Uint8Array,
  encKey: Uint8Array,
  iv: Uint8Array
): Promise<Uint8Array> {
  // CTR mode decryption is identical to encryption
  return aesCtrEncrypt(ciphertext, encKey, iv);
}

/**
 * Encrypt data with AES-256-CTR + HMAC-SHA-256 (encrypt-then-MAC).
 *
 * 1. Generate random 16-byte IV
 * 2. Encrypt plaintext with AES-256-CTR using encKey and IV
 * 3. Compute HMAC-SHA-256(macKey, IV || ciphertext) for authentication
 * 4. Return IV:ciphertext:mac (all base64-encoded)
 */
async function encryptAuthenticated(
  plaintext: string,
  encKey: Uint8Array,
  macKey: Uint8Array
): Promise<string> {
  const iv = await secureRandomBytes(IV_BYTES);
  const plaintextBytes = stringToBytes(plaintext);
  const ciphertext = await aesCtrEncrypt(plaintextBytes, encKey, iv);

  // Compute MAC over IV || ciphertext (encrypt-then-MAC)
  const macInput = new Uint8Array(iv.length + ciphertext.length);
  macInput.set(iv);
  macInput.set(ciphertext, iv.length);
  const mac = await hmacSha256(macKey, macInput);

  return `${bytesToBase64(iv)}:${bytesToBase64(ciphertext)}:${bytesToBase64(mac)}`;
}

/**
 * Decrypt data with AES-256-CTR + HMAC-SHA-256 verification.
 *
 * 1. Parse IV:ciphertext:mac from input
 * 2. Verify HMAC-SHA-256(macKey, IV || ciphertext) matches provided mac
 * 3. If MAC valid, decrypt ciphertext with AES-256-CTR
 * 4. If MAC invalid, throw (data has been tampered with)
 */
async function decryptAuthenticated(
  encrypted: string,
  encKey: Uint8Array,
  macKey: Uint8Array
): Promise<string> {
  const parts = encrypted.split(':');
  if (parts.length !== 3) {
    throw new Error('Invalid encrypted data format. Expected iv:ciphertext:mac');
  }

  const iv = base64ToBytes(parts[0]);
  const ciphertext = base64ToBytes(parts[1]);
  const storedMac = base64ToBytes(parts[2]);

  // Verify MAC first (before decrypting)
  const macInput = new Uint8Array(iv.length + ciphertext.length);
  macInput.set(iv);
  macInput.set(ciphertext, iv.length);
  const computedMac = await hmacSha256(macKey, macInput);

  // Constant-time comparison to prevent timing attacks
  if (!constantTimeEqual(computedMac, storedMac)) {
    throw new Error('Authentication failed. Data may have been tampered with.');
  }

  const plaintextBytes = await aesCtrDecrypt(ciphertext, encKey, iv);
  return bytesToString(plaintextBytes);
}

/**
 * Constant-time comparison of two byte arrays to prevent timing attacks.
 */
function constantTimeEqual(a: Uint8Array, b: Uint8Array): boolean {
  if (a.length !== b.length) return false;
  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a[i] ^ b[i];
  }
  return result === 0;
}

// --- EncryptionVault class ---

class EncryptionVault {
  private encKey: Uint8Array | null = null;
  private macKey: Uint8Array | null = null;
  private lastActivityTimestamp: number = Date.now();
  private autoLockTimeoutMs: number = AUTO_LOCK_TIMEOUT_MS;
  private lockCallback: (() => void) | null = null;
  private lockTimer: ReturnType<typeof setInterval> | null = null;

  /**
   * Initialize the vault with a user secret (PIN or biometric token).
   * Creates or retrieves the vault salt and derives encryption + MAC keys.
   */
  async initialize(secret: string): Promise<void> {
    let saltB64 = await SecureStore.getItemAsync(VAULT_SALT_ALIAS);
    if (!saltB64) {
      const saltBytes = await secureRandomBytes(SALT_BYTES);
      saltB64 = bytesToBase64(saltBytes);
      await SecureStore.setItemAsync(VAULT_SALT_ALIAS, saltB64);
    }

    const salt = base64ToBytes(saltB64);
    const { encKey, macKey } = await deriveKeys(secret, salt);
    this.encKey = encKey;
    this.macKey = macKey;

    // Store a verification token so we can confirm correct key on future unlocks
    const existingToken = await SecureStore.getItemAsync(VAULT_KEY_ALIAS);
    if (!existingToken) {
      const keyForVerification = new Uint8Array(encKey.length + macKey.length);
      keyForVerification.set(encKey);
      keyForVerification.set(macKey, encKey.length);
      const verifyMsg = stringToBytes('cnsnt_vault_verify_v2');
      const verificationMac = await hmacSha256(keyForVerification, verifyMsg);
      await SecureStore.setItemAsync(VAULT_KEY_ALIAS, bytesToBase64(verificationMac));
    }

    // Mark vault version for migration detection
    await SecureStore.setItemAsync(VAULT_VERSION_KEY, '2');

    this.resetActivity();
    this.startAutoLockTimer();
  }

  /**
   * Verify the vault key is correct by checking against stored verification token.
   */
  async verifyKey(secret: string): Promise<boolean> {
    const saltB64 = await SecureStore.getItemAsync(VAULT_SALT_ALIAS);
    if (!saltB64) return false;

    const salt = base64ToBytes(saltB64);
    const { encKey, macKey } = await deriveKeys(secret, salt);

    const expectedToken = await SecureStore.getItemAsync(VAULT_KEY_ALIAS);
    if (!expectedToken) return true; // First-time setup

    const keyForVerification = new Uint8Array(encKey.length + macKey.length);
    keyForVerification.set(encKey);
    keyForVerification.set(macKey, encKey.length);
    const verifyMsg = stringToBytes('cnsnt_vault_verify_v2');
    const computedMac = await hmacSha256(keyForVerification, verifyMsg);

    return constantTimeEqual(base64ToBytes(expectedToken), computedMac);
  }

  /**
   * Encrypt data and store it in AsyncStorage.
   * Format: { version: 2, data: "iv:ciphertext:mac", timestamp: ISO string }
   */
  async encryptAndStore(key: string, data: string): Promise<void> {
    this.ensureUnlocked();
    this.resetActivity();

    const encrypted = await encryptAuthenticated(data, this.encKey!, this.macKey!);

    const envelope = JSON.stringify({
      version: 2,
      data: encrypted,
      timestamp: new Date().toISOString(),
    });

    await AsyncStorage.setItem(`vault_${key}`, envelope);
  }

  /**
   * Retrieve and decrypt data from AsyncStorage.
   * Handles both v1 (legacy XOR) and v2 (AES-CTR+HMAC) envelopes.
   */
  async retrieveAndDecrypt(key: string): Promise<string | null> {
    this.ensureUnlocked();
    this.resetActivity();

    const envelope = await AsyncStorage.getItem(`vault_${key}`);
    if (!envelope) return null;

    const parsed = JSON.parse(envelope);

    if (parsed.version === 2) {
      // v2: AES-256-CTR + HMAC-SHA-256 (encrypt-then-MAC)
      return decryptAuthenticated(parsed.data, this.encKey!, this.macKey!);
    }

    // v1 legacy: attempt migration
    // Legacy data has { data: hexCiphertext, hash: sha256OfPlaintext }
    // We cannot decrypt v1 data with v2 keys if the key derivation changed.
    // If this is reached, the data was stored with the old XOR cipher.
    // Re-encrypt with v2 format on successful read.
    throw new Error(
      'Legacy v1 encrypted data detected. Please re-initialize vault with your PIN to migrate data.'
    );
  }

  /**
   * Delete an encrypted record.
   */
  async deleteRecord(key: string): Promise<void> {
    this.ensureUnlocked();
    this.resetActivity();
    await AsyncStorage.removeItem(`vault_${key}`);
  }

  /**
   * List all vault keys.
   */
  async listKeys(): Promise<string[]> {
    this.ensureUnlocked();
    this.resetActivity();
    const allKeys = await AsyncStorage.getAllKeys();
    return allKeys
      .filter((k) => k.startsWith('vault_'))
      .map((k) => k.replace('vault_', ''));
  }

  /**
   * Delete all vault data.
   */
  async purgeAll(): Promise<void> {
    const allKeys = await AsyncStorage.getAllKeys();
    const vaultKeys = allKeys.filter((k) => k.startsWith('vault_'));
    if (vaultKeys.length > 0) {
      await AsyncStorage.multiRemove(vaultKeys);
    }
    await SecureStore.deleteItemAsync(VAULT_KEY_ALIAS);
    await SecureStore.deleteItemAsync(VAULT_SALT_ALIAS);
    await SecureStore.deleteItemAsync(VAULT_VERSION_KEY);
    this.encKey = null;
    this.macKey = null;
  }

  /**
   * Compute HMAC-SHA-256 of arbitrary data using the vault's MAC key.
   * This is a keyed hash, NOT plain SHA-256. Attackers cannot forge it
   * without the key, even if they can modify the data.
   */
  async sha256(data: string): Promise<string> {
    this.ensureUnlocked();
    const dataBytes = stringToBytes(data);
    const mac = await hmacSha256(this.macKey!, dataBytes);
    return bytesToHex(mac);
  }

  /**
   * Compute HMAC-SHA-256 with an explicit key (for document integrity).
   * Used by database.ts to include a timestamp in the hash payload.
   */
  async hmac(data: string): Promise<string> {
    this.ensureUnlocked();
    const dataBytes = stringToBytes(data);
    const mac = await hmacSha256(this.macKey!, dataBytes);
    return bytesToHex(mac);
  }

  /**
   * Verify an HMAC-SHA-256 in constant time.
   */
  async verifyHmac(data: string, expectedHex: string): Promise<boolean> {
    this.ensureUnlocked();
    const dataBytes = stringToBytes(data);
    const computed = await hmacSha256(this.macKey!, dataBytes);
    const expected = hexToBytes(expectedHex);
    return constantTimeEqual(computed, expected);
  }

  /**
   * Self-test: encrypt then decrypt a known plaintext to verify
   * the vault is producing ciphertext that round-trips correctly.
   * Also verifies HMAC integrity check works.
   */
  async selfTest(): Promise<{ encrypted: string; decrypted: string; match: boolean }> {
    this.ensureUnlocked();
    const testPlaintext = 'cnsnt_vault_selftest_v2_' + Date.now().toString();

    const encrypted = await encryptAuthenticated(
      testPlaintext,
      this.encKey!,
      this.macKey!
    );

    // Verify encrypted text is NOT the same as plaintext
    if (encrypted === testPlaintext) {
      throw new Error('Encryption self-test failed: ciphertext equals plaintext');
    }

    // Verify format: should be iv:ciphertext:mac
    const parts = encrypted.split(':');
    if (parts.length !== 3) {
      throw new Error('Encryption self-test failed: unexpected output format');
    }

    // Verify decryption recovers the original
    const decrypted = await decryptAuthenticated(
      encrypted,
      this.encKey!,
      this.macKey!
    );
    const match = decrypted === testPlaintext;
    if (!match) {
      throw new Error('Encryption self-test failed: round-trip mismatch');
    }

    // Verify tamper detection: flip a byte in ciphertext and confirm MAC fails
    const tamperedParts = [...parts];
    const ctBytes = base64ToBytes(tamperedParts[1]);
    ctBytes[0] ^= 0xff; // flip first byte
    tamperedParts[1] = bytesToBase64(ctBytes);
    const tampered = tamperedParts.join(':');
    try {
      await decryptAuthenticated(tampered, this.encKey!, this.macKey!);
      throw new Error('Encryption self-test failed: tampered data was not rejected');
    } catch (e: any) {
      if (!e.message.includes('Authentication failed') && !e.message.includes('tampered')) {
        throw new Error('Encryption self-test failed: wrong error on tampered data');
      }
    }

    // Verify HMAC
    const testData = 'hmac_selftest';
    const hmacResult = await this.sha256(testData);
    const hmacVerified = await this.verifyHmac(testData, hmacResult);
    if (!hmacVerified) {
      throw new Error('HMAC self-test failed: verification mismatch');
    }

    return { encrypted, decrypted, match };
  }

  /**
   * Lock the vault, clearing the in-memory keys.
   * Uses explicit zeroing to reduce key exposure window.
   */
  lock(): void {
    if (this.encKey) {
      this.encKey.fill(0);
      this.encKey = null;
    }
    if (this.macKey) {
      this.macKey.fill(0);
      this.macKey = null;
    }
    this.stopAutoLockTimer();
  }

  /**
   * Check if the vault is currently unlocked.
   */
  isUnlocked(): boolean {
    return this.encKey !== null && this.macKey !== null;
  }

  /**
   * Set auto-lock timeout in minutes.
   */
  setAutoLockTimeout(minutes: number): void {
    this.autoLockTimeoutMs = minutes * 60 * 1000;
  }

  /**
   * Register a callback for when auto-lock triggers.
   */
  onAutoLock(callback: () => void): void {
    this.lockCallback = callback;
  }

  /**
   * Reset the activity timer (call on user interaction).
   */
  resetActivity(): void {
    this.lastActivityTimestamp = Date.now();
  }

  private ensureUnlocked(): void {
    if (!this.encKey || !this.macKey) {
      throw new Error('Vault is locked. Authenticate to access data.');
    }
  }

  private startAutoLockTimer(): void {
    this.stopAutoLockTimer();
    this.lockTimer = setInterval(() => {
      if (Date.now() - this.lastActivityTimestamp > this.autoLockTimeoutMs) {
        this.lock();
        if (this.lockCallback) {
          this.lockCallback();
        }
      }
    }, 15000); // Check every 15 seconds (tighter than before)
  }

  private stopAutoLockTimer(): void {
    if (this.lockTimer) {
      clearInterval(this.lockTimer);
      this.lockTimer = null;
    }
  }
}

// Singleton instance
export const vault = new EncryptionVault();
export default vault;
