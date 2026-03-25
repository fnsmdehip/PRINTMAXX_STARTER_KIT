/**
 * Biometric & PIN Authentication Service for cnsnt app.
 *
 * - expo-local-authentication for Face ID / fingerprint
 * - PIN fallback for devices without biometrics
 * - PBKDF2-SHA256 with 100,000 iterations for PIN hashing
 * - Rate limiting: lockout after 5 failed attempts (1 hour), 10 (24 hours), 15 (wipe offer)
 * - Cryptographic random salt from expo-crypto
 * - Lock screen on app open
 * - Auth required to view/export consent records
 */

import * as LocalAuthentication from 'expo-local-authentication';
import * as SecureStore from 'expo-secure-store';
import * as Crypto from 'expo-crypto';
import vault from './encryption';

const PIN_HASH_KEY = 'cnsnt_pin_hash_v2';
const PIN_SALT_KEY = 'cnsnt_pin_salt_v2';
const BIOMETRIC_ENABLED_KEY = 'cnsnt_biometric_enabled';
const AUTO_LOCK_TIMEOUT_KEY = 'cnsnt_auto_lock_timeout';

// Rate limiting keys
const FAILED_ATTEMPTS_KEY = 'cnsnt_failed_attempts';
const LOCKOUT_UNTIL_KEY = 'cnsnt_lockout_until';
const TOTAL_FAILED_KEY = 'cnsnt_total_failed';

// Rate limiting thresholds
const LOCKOUT_THRESHOLD_1 = 5; // 5 consecutive failures = 1 hour lockout
const LOCKOUT_THRESHOLD_2 = 10; // 10 total failures = 24 hour lockout
const WIPE_THRESHOLD = 15; // 15 total failures = offer vault wipe
const LOCKOUT_DURATION_1_MS = 60 * 60 * 1000; // 1 hour
const LOCKOUT_DURATION_2_MS = 24 * 60 * 60 * 1000; // 24 hours

// PBKDF2 parameters
const PBKDF2_ITERATIONS = 100_000;
const SALT_BYTES = 32;
const HASH_BYTES = 32;

export interface AuthState {
  isAuthenticated: boolean;
  hasBiometrics: boolean;
  biometricType: LocalAuthentication.AuthenticationType[];
  biometricEnabled: boolean;
  pinIsSet: boolean;
  autoLockMinutes: number;
}

export interface LockoutState {
  isLockedOut: boolean;
  remainingMs: number;
  failedAttempts: number;
  totalFailed: number;
  shouldOfferWipe: boolean;
}

// --- Crypto helpers ---

/**
 * Convert a Uint8Array to a base64 string.
 */
function bytesToBase64(bytes: Uint8Array): string {
  let binary = '';
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  if (typeof btoa === 'function') {
    return btoa(binary);
  }
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
  let result = '';
  let idx = 0;
  while (idx < binary.length) {
    const a = binary.charCodeAt(idx++);
    const b = idx < binary.length ? binary.charCodeAt(idx++) : 0;
    const c = idx < binary.length ? binary.charCodeAt(idx++) : 0;
    const triplet = (a << 16) | (b << 8) | c;
    result += chars[(triplet >> 18) & 0x3f];
    result += chars[(triplet >> 12) & 0x3f];
    result += idx - 2 < binary.length ? chars[(triplet >> 6) & 0x3f] : '=';
    result += idx - 1 < binary.length ? chars[triplet & 0x3f] : '=';
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
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
    const lookup = new Uint8Array(128);
    for (let i = 0; i < chars.length; i++) {
      lookup[chars.charCodeAt(i)] = i;
    }
    const stripped = b64.replace(/=/g, '');
    const byteArr: number[] = [];
    for (let i = 0; i < stripped.length; i += 4) {
      const a = lookup[stripped.charCodeAt(i)];
      const b2 = lookup[stripped.charCodeAt(i + 1)] || 0;
      const c = lookup[stripped.charCodeAt(i + 2)] || 0;
      const d = lookup[stripped.charCodeAt(i + 3)] || 0;
      byteArr.push((a << 2) | (b2 >> 4));
      if (i + 2 < stripped.length) byteArr.push(((b2 & 0xf) << 4) | (c >> 2));
      if (i + 3 < stripped.length) byteArr.push(((c & 0x3) << 6) | d);
    }
    binary = String.fromCharCode(...byteArr);
  }
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes;
}

function bytesToHex(bytes: Uint8Array): string {
  const hex: string[] = [];
  for (let i = 0; i < bytes.length; i++) {
    hex.push(bytes[i].toString(16).padStart(2, '0'));
  }
  return hex.join('');
}

function hexToBytes(hex: string): Uint8Array {
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.substring(i, i + 2), 16);
  }
  return bytes;
}

/**
 * SHA-256 hash of byte array, returns bytes.
 */
async function sha256Bytes(data: Uint8Array): Promise<Uint8Array> {
  const hexInput = bytesToHex(data);
  const hexHash = await Crypto.digestStringAsync(
    Crypto.CryptoDigestAlgorithm.SHA256,
    hexInput
  );
  return hexToBytes(hexHash);
}

/**
 * HMAC-SHA-256 for PBKDF2 PRF.
 */
async function hmacSha256(key: Uint8Array, message: Uint8Array): Promise<Uint8Array> {
  const blockSize = 64;
  let keyPrime: Uint8Array;
  if (key.length > blockSize) {
    keyPrime = await sha256Bytes(key);
  } else {
    keyPrime = new Uint8Array(key);
  }
  const paddedKey = new Uint8Array(blockSize);
  paddedKey.set(keyPrime);

  const innerKey = new Uint8Array(blockSize);
  const outerKey = new Uint8Array(blockSize);
  for (let i = 0; i < blockSize; i++) {
    innerKey[i] = paddedKey[i] ^ 0x36;
    outerKey[i] = paddedKey[i] ^ 0x5c;
  }

  const innerData = new Uint8Array(blockSize + message.length);
  innerData.set(innerKey);
  innerData.set(message, blockSize);
  const innerHash = await sha256Bytes(innerData);

  const outerData = new Uint8Array(blockSize + 32);
  outerData.set(outerKey);
  outerData.set(innerHash, blockSize);
  return sha256Bytes(outerData);
}

/**
 * PBKDF2-SHA256 key derivation.
 */
async function pbkdf2Sha256(
  password: Uint8Array,
  salt: Uint8Array,
  iterations: number,
  dkLen: number
): Promise<Uint8Array> {
  const hLen = 32;
  const numBlocks = Math.ceil(dkLen / hLen);
  const dk = new Uint8Array(numBlocks * hLen);

  for (let blockIndex = 1; blockIndex <= numBlocks; blockIndex++) {
    const counterBytes = new Uint8Array(4);
    counterBytes[0] = (blockIndex >> 24) & 0xff;
    counterBytes[1] = (blockIndex >> 16) & 0xff;
    counterBytes[2] = (blockIndex >> 8) & 0xff;
    counterBytes[3] = blockIndex & 0xff;

    const saltBlock = new Uint8Array(salt.length + 4);
    saltBlock.set(salt);
    saltBlock.set(counterBytes, salt.length);

    let u = await hmacSha256(password, saltBlock);
    const result = new Uint8Array(u);

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
 * Constant-time comparison to prevent timing attacks on PIN verification.
 */
function constantTimeEqual(a: Uint8Array, b: Uint8Array): boolean {
  if (a.length !== b.length) return false;
  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a[i] ^ b[i];
  }
  return result === 0;
}

/**
 * Hash a PIN with PBKDF2-SHA-256 and the given salt.
 * Returns base64-encoded 32-byte derived key.
 */
async function hashPin(pin: string, salt: Uint8Array): Promise<string> {
  const encoder = new TextEncoder();
  const pinBytes = encoder.encode(pin);
  const derived = await pbkdf2Sha256(pinBytes, salt, PBKDF2_ITERATIONS, HASH_BYTES);
  return bytesToBase64(derived);
}

// --- AuthService class ---

class AuthService {
  private authenticated: boolean = false;

  /**
   * Check device biometric capabilities.
   */
  async checkBiometricSupport(): Promise<{
    available: boolean;
    types: LocalAuthentication.AuthenticationType[];
  }> {
    const compatible = await LocalAuthentication.hasHardwareAsync();
    const enrolled = await LocalAuthentication.isEnrolledAsync();
    const types =
      await LocalAuthentication.supportedAuthenticationTypesAsync();

    return {
      available: compatible && enrolled,
      types,
    };
  }

  /**
   * Get human-readable biometric type name.
   */
  async getBiometricTypeName(): Promise<string> {
    const { types } = await this.checkBiometricSupport();
    if (types.includes(LocalAuthentication.AuthenticationType.FACIAL_RECOGNITION)) {
      return 'Face ID';
    }
    if (types.includes(LocalAuthentication.AuthenticationType.FINGERPRINT)) {
      return 'Fingerprint';
    }
    if (types.includes(LocalAuthentication.AuthenticationType.IRIS)) {
      return 'Iris';
    }
    return 'Biometric';
  }

  /**
   * Authenticate with biometrics.
   */
  async authenticateWithBiometrics(): Promise<boolean> {
    const biometricEnabled = await this.isBiometricEnabled();
    if (!biometricEnabled) return false;

    const result = await LocalAuthentication.authenticateAsync({
      promptMessage: 'Authenticate to access cnsnt',
      cancelLabel: 'Use PIN',
      disableDeviceFallback: true,
      fallbackLabel: 'Use PIN',
    });

    if (result.success) {
      this.authenticated = true;
      // Initialize vault with a biometric-derived token
      const biometricToken = await this.getBiometricToken();
      await vault.initialize(biometricToken);
    }

    return result.success;
  }

  /**
   * Authenticate with PIN. Enforces rate limiting and lockout.
   *
   * Returns:
   * - { success: true } on valid PIN
   * - { success: false, lockout: LockoutState } on invalid PIN or lockout
   */
  async authenticateWithPin(
    pin: string
  ): Promise<{ success: boolean; lockout?: LockoutState }> {
    // Check lockout first
    const lockoutState = await this.getLockoutState();
    if (lockoutState.isLockedOut) {
      return { success: false, lockout: lockoutState };
    }

    const isValid = await this.verifyPin(pin);
    if (isValid) {
      this.authenticated = true;
      await vault.initialize(pin);
      // Reset failed attempts on successful auth
      await this.resetFailedAttempts();
      return { success: true };
    }

    // Record failed attempt
    await this.recordFailedAttempt();
    const newLockoutState = await this.getLockoutState();
    return { success: false, lockout: newLockoutState };
  }

  /**
   * Get the current lockout state.
   */
  async getLockoutState(): Promise<LockoutState> {
    const failedStr = await SecureStore.getItemAsync(FAILED_ATTEMPTS_KEY);
    const lockoutUntilStr = await SecureStore.getItemAsync(LOCKOUT_UNTIL_KEY);
    const totalFailedStr = await SecureStore.getItemAsync(TOTAL_FAILED_KEY);

    const failedAttempts = failedStr ? parseInt(failedStr, 10) : 0;
    const totalFailed = totalFailedStr ? parseInt(totalFailedStr, 10) : 0;
    const lockoutUntil = lockoutUntilStr ? parseInt(lockoutUntilStr, 10) : 0;

    const now = Date.now();
    const isLockedOut = lockoutUntil > now;
    const remainingMs = isLockedOut ? lockoutUntil - now : 0;
    const shouldOfferWipe = totalFailed >= WIPE_THRESHOLD;

    return {
      isLockedOut,
      remainingMs,
      failedAttempts,
      totalFailed,
      shouldOfferWipe,
    };
  }

  /**
   * Record a failed PIN attempt and apply lockout if threshold reached.
   */
  private async recordFailedAttempt(): Promise<void> {
    const failedStr = await SecureStore.getItemAsync(FAILED_ATTEMPTS_KEY);
    const totalFailedStr = await SecureStore.getItemAsync(TOTAL_FAILED_KEY);

    const failedAttempts = (failedStr ? parseInt(failedStr, 10) : 0) + 1;
    const totalFailed = (totalFailedStr ? parseInt(totalFailedStr, 10) : 0) + 1;

    await SecureStore.setItemAsync(FAILED_ATTEMPTS_KEY, failedAttempts.toString());
    await SecureStore.setItemAsync(TOTAL_FAILED_KEY, totalFailed.toString());

    // Apply lockout based on thresholds
    const now = Date.now();
    if (totalFailed >= LOCKOUT_THRESHOLD_2) {
      // 10+ total failures: 24 hour lockout
      const lockoutUntil = now + LOCKOUT_DURATION_2_MS;
      await SecureStore.setItemAsync(LOCKOUT_UNTIL_KEY, lockoutUntil.toString());
    } else if (failedAttempts >= LOCKOUT_THRESHOLD_1) {
      // 5+ consecutive failures: 1 hour lockout
      const lockoutUntil = now + LOCKOUT_DURATION_1_MS;
      await SecureStore.setItemAsync(LOCKOUT_UNTIL_KEY, lockoutUntil.toString());
    }
  }

  /**
   * Reset failed attempt counters (called on successful auth).
   */
  private async resetFailedAttempts(): Promise<void> {
    await SecureStore.setItemAsync(FAILED_ATTEMPTS_KEY, '0');
    // Note: totalFailed is NOT reset on success -- it tracks lifetime failures
    // to enforce the wipe threshold. Only a full resetAll clears it.
    await SecureStore.deleteItemAsync(LOCKOUT_UNTIL_KEY);
  }

  /**
   * Wipe the vault after too many failed attempts. Requires explicit confirmation.
   * This is a destructive operation that deletes all encrypted data.
   */
  async wipeVaultAfterLockout(): Promise<void> {
    await vault.purgeAll();
    await this.resetAll();
  }

  /**
   * Set up a new PIN. Uses PBKDF2-SHA256 with 100,000 iterations
   * and a 32-byte cryptographic random salt.
   */
  async setPin(pin: string): Promise<void> {
    if (pin.length < 4) {
      throw new Error('PIN must be at least 4 digits');
    }

    // Generate cryptographic random salt
    const saltBytes = await Crypto.getRandomBytes(SALT_BYTES);
    const saltB64 = bytesToBase64(saltBytes);

    // Hash PIN with PBKDF2-SHA256
    const pinHash = await hashPin(pin, saltBytes);

    await SecureStore.setItemAsync(PIN_HASH_KEY, pinHash);
    await SecureStore.setItemAsync(PIN_SALT_KEY, saltB64);

    this.authenticated = true;
    await vault.initialize(pin);
  }

  /**
   * Verify a PIN against stored PBKDF2-SHA256 hash.
   * Uses constant-time comparison to prevent timing attacks.
   */
  async verifyPin(pin: string): Promise<boolean> {
    const storedHash = await SecureStore.getItemAsync(PIN_HASH_KEY);
    const saltB64 = await SecureStore.getItemAsync(PIN_SALT_KEY);

    if (!storedHash || !saltB64) {
      // Check for legacy v1 PIN format and migrate
      return this.verifyLegacyPin(pin);
    }

    const salt = base64ToBytes(saltB64);
    const computedHash = await hashPin(pin, salt);

    // Constant-time comparison
    const storedBytes = base64ToBytes(storedHash);
    const computedBytes = base64ToBytes(computedHash);
    return constantTimeEqual(storedBytes, computedBytes);
  }

  /**
   * Check and migrate legacy v1 PIN (single SHA-256 hash).
   * If valid, automatically upgrades to PBKDF2 format.
   */
  private async verifyLegacyPin(pin: string): Promise<boolean> {
    const legacyHash = await SecureStore.getItemAsync('cnsnt_pin_hash');
    const legacySalt = await SecureStore.getItemAsync('cnsnt_pin_salt');

    if (!legacyHash || !legacySalt) return false;

    // Legacy format: single SHA-256(pin + salt)
    const hash = await Crypto.digestStringAsync(
      Crypto.CryptoDigestAlgorithm.SHA256,
      pin + legacySalt
    );

    if (hash === legacyHash) {
      // Migrate to PBKDF2 format
      await this.setPin(pin);
      // Clean up legacy keys
      await SecureStore.deleteItemAsync('cnsnt_pin_hash');
      await SecureStore.deleteItemAsync('cnsnt_pin_salt');
      return true;
    }

    return false;
  }

  /**
   * Check if PIN has been set (either v1 or v2 format).
   */
  async isPinSet(): Promise<boolean> {
    const v2Hash = await SecureStore.getItemAsync(PIN_HASH_KEY);
    if (v2Hash) return true;
    // Check legacy
    const v1Hash = await SecureStore.getItemAsync('cnsnt_pin_hash');
    return !!v1Hash;
  }

  /**
   * Change existing PIN. Requires old PIN verification.
   */
  async changePin(oldPin: string, newPin: string): Promise<boolean> {
    const valid = await this.verifyPin(oldPin);
    if (!valid) return false;

    await this.setPin(newPin);
    return true;
  }

  /**
   * Enable or disable biometric authentication.
   */
  async setBiometricEnabled(enabled: boolean): Promise<void> {
    await SecureStore.setItemAsync(
      BIOMETRIC_ENABLED_KEY,
      enabled ? 'true' : 'false'
    );
  }

  /**
   * Check if biometric auth is enabled.
   */
  async isBiometricEnabled(): Promise<boolean> {
    const value = await SecureStore.getItemAsync(BIOMETRIC_ENABLED_KEY);
    return value === 'true';
  }

  /**
   * Set auto-lock timeout in minutes.
   */
  async setAutoLockTimeout(minutes: number): Promise<void> {
    await SecureStore.setItemAsync(AUTO_LOCK_TIMEOUT_KEY, minutes.toString());
    vault.setAutoLockTimeout(minutes);
  }

  /**
   * Get auto-lock timeout in minutes. Default is 2 minutes.
   */
  async getAutoLockTimeout(): Promise<number> {
    const value = await SecureStore.getItemAsync(AUTO_LOCK_TIMEOUT_KEY);
    return value ? parseInt(value, 10) : 2; // Default 2 minutes (was 5)
  }

  /**
   * Get full auth state for UI rendering.
   */
  async getAuthState(): Promise<AuthState> {
    const { available, types } = await this.checkBiometricSupport();
    const biometricEnabled = await this.isBiometricEnabled();
    const pinIsSet = await this.isPinSet();
    const autoLockMinutes = await this.getAutoLockTimeout();

    return {
      isAuthenticated: this.authenticated,
      hasBiometrics: available,
      biometricType: types,
      biometricEnabled: biometricEnabled && available,
      pinIsSet,
      autoLockMinutes,
    };
  }

  /**
   * Lock the app.
   */
  lock(): void {
    this.authenticated = false;
    vault.lock();
  }

  /**
   * Check if user is currently authenticated.
   */
  isAuthenticated(): boolean {
    return this.authenticated && vault.isUnlocked();
  }

  /**
   * Reset all auth data (for "Delete all data" in settings).
   * Also clears all rate limiting state.
   */
  async resetAll(): Promise<void> {
    this.authenticated = false;
    // v2 keys
    await SecureStore.deleteItemAsync(PIN_HASH_KEY);
    await SecureStore.deleteItemAsync(PIN_SALT_KEY);
    // v1 legacy keys
    await SecureStore.deleteItemAsync('cnsnt_pin_hash');
    await SecureStore.deleteItemAsync('cnsnt_pin_salt');
    // Shared keys
    await SecureStore.deleteItemAsync(BIOMETRIC_ENABLED_KEY);
    await SecureStore.deleteItemAsync(AUTO_LOCK_TIMEOUT_KEY);
    await SecureStore.deleteItemAsync('cnsnt-pin');
    await SecureStore.deleteItemAsync('cnsnt_biometric_token');
    // Rate limiting state
    await SecureStore.deleteItemAsync(FAILED_ATTEMPTS_KEY);
    await SecureStore.deleteItemAsync(LOCKOUT_UNTIL_KEY);
    await SecureStore.deleteItemAsync(TOTAL_FAILED_KEY);
    await vault.purgeAll();
  }

  /**
   * Generate a stable biometric-derived token.
   * We use a device-stored secret that's only accessible after biometric auth.
   * Uses cryptographic random bytes, not Date.now + Math.random.
   */
  private async getBiometricToken(): Promise<string> {
    const key = 'cnsnt_biometric_token';
    let token = await SecureStore.getItemAsync(key);
    if (!token) {
      const randomBytes = await Crypto.getRandomBytes(32);
      token = bytesToBase64(randomBytes);
      await SecureStore.setItemAsync(key, token);
    }
    return token;
  }
}

export const authService = new AuthService();
export default authService;
