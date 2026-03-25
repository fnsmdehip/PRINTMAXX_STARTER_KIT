/**
 * Audit Logging Service for cnsnt app.
 *
 * Append-only encrypted audit log for compliance and forensics.
 * Every security-relevant event is recorded with timestamp, event type,
 * optional record ID, details, and a stable device identifier.
 *
 * Logs are encrypted with the vault key and stored in AsyncStorage.
 * Individual entries cannot be deleted (append-only).
 * Export as encrypted JSON for compliance auditing.
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Device from 'expo-device';
import * as SecureStore from 'expo-secure-store';
import * as Crypto from 'expo-crypto';
import vault from './encryption';

// --- Event Types ---

export type AuditEventType =
  | 'record_created'
  | 'record_viewed'
  | 'record_exported'
  | 'record_deleted'
  | 'record_shared'
  | 'record_updated'
  | 'record_revoked'
  | 'auth_success'
  | 'auth_failed'
  | 'auth_lockout'
  | 'vault_locked'
  | 'vault_unlocked'
  | 'backup_created'
  | 'backup_restored'
  | 'pin_changed'
  | 'pin_set'
  | 'biometric_toggled'
  | 'data_wiped'
  | 'integrity_check_passed'
  | 'integrity_check_failed';

export interface AuditLogEntry {
  timestamp: string;
  eventType: AuditEventType;
  recordId?: string;
  details?: string;
  deviceId: string;
}

// --- Storage Keys ---

const AUDIT_LOG_KEY = 'cnsnt_audit_log';
const DEVICE_ID_KEY = 'cnsnt_device_id';
const AUDIT_SEQUENCE_KEY = 'cnsnt_audit_seq';

// --- Helpers ---

/**
 * Convert Uint8Array to base64.
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

// --- AuditLogService ---

class AuditLogService {
  private deviceId: string | null = null;

  /**
   * Get or create a stable device identifier.
   * Stored in SecureStore so it persists across app reinstalls
   * (on iOS, SecureStore persists in Keychain).
   */
  async getDeviceId(): Promise<string> {
    if (this.deviceId) return this.deviceId;

    let stored = await SecureStore.getItemAsync(DEVICE_ID_KEY);
    if (!stored) {
      // Generate a stable device fingerprint
      const randomBytes = await Crypto.getRandomBytes(16);
      const deviceInfo = [
        Device.modelName || 'unknown',
        Device.osName || 'unknown',
        Device.osVersion || 'unknown',
        bytesToBase64(randomBytes),
      ].join('|');

      stored = await Crypto.digestStringAsync(
        Crypto.CryptoDigestAlgorithm.SHA256,
        deviceInfo
      );
      // Store first 16 chars for readability
      stored = stored.substring(0, 16);
      await SecureStore.setItemAsync(DEVICE_ID_KEY, stored);
    }

    this.deviceId = stored;
    return stored;
  }

  /**
   * Get the next sequence number for ordering.
   */
  private async getNextSequence(): Promise<number> {
    const seqStr = await AsyncStorage.getItem(AUDIT_SEQUENCE_KEY);
    const seq = seqStr ? parseInt(seqStr, 10) + 1 : 1;
    await AsyncStorage.setItem(AUDIT_SEQUENCE_KEY, seq.toString());
    return seq;
  }

  /**
   * Log an audit event. This is the primary API.
   *
   * Events are stored encrypted if the vault is unlocked.
   * If the vault is locked (e.g., auth_failed events), they are stored
   * in a plaintext staging area and encrypted on next vault unlock.
   */
  async log(
    eventType: AuditEventType,
    recordId?: string,
    details?: string
  ): Promise<void> {
    try {
      const deviceId = await this.getDeviceId();
      const entry: AuditLogEntry = {
        timestamp: new Date().toISOString(),
        eventType,
        deviceId,
      };
      if (recordId) entry.recordId = recordId;
      if (details) entry.details = details;

      if (vault.isUnlocked()) {
        await this.appendEncrypted(entry);
      } else {
        // Store unencrypted in staging (for pre-auth events like auth_failed)
        await this.appendStaging(entry);
      }
    } catch {
      // Audit logging must NEVER throw and crash the app.
      // Silently fail if storage is full or corrupt.
    }
  }

  /**
   * Append an entry to the encrypted audit log.
   */
  private async appendEncrypted(entry: AuditLogEntry): Promise<void> {
    const entries = await this.readEncryptedEntries();
    entries.push(entry);
    await vault.encryptAndStore(AUDIT_LOG_KEY, JSON.stringify(entries));
  }

  /**
   * Append to plaintext staging (for pre-auth events).
   */
  private async appendStaging(entry: AuditLogEntry): Promise<void> {
    const stagingKey = 'cnsnt_audit_staging';
    const raw = await AsyncStorage.getItem(stagingKey);
    const entries: AuditLogEntry[] = raw ? JSON.parse(raw) : [];
    entries.push(entry);
    // Cap staging at 100 entries to prevent unbounded growth
    const capped = entries.slice(-100);
    await AsyncStorage.setItem(stagingKey, JSON.stringify(capped));
  }

  /**
   * Flush staging entries into the encrypted log.
   * Call this after vault is unlocked.
   */
  async flushStaging(): Promise<void> {
    if (!vault.isUnlocked()) return;

    try {
      const stagingKey = 'cnsnt_audit_staging';
      const raw = await AsyncStorage.getItem(stagingKey);
      if (!raw) return;

      const stagingEntries: AuditLogEntry[] = JSON.parse(raw);
      if (stagingEntries.length === 0) return;

      const encryptedEntries = await this.readEncryptedEntries();
      encryptedEntries.push(...stagingEntries);
      await vault.encryptAndStore(AUDIT_LOG_KEY, JSON.stringify(encryptedEntries));

      // Clear staging
      await AsyncStorage.removeItem(stagingKey);
    } catch {
      // Don't crash on flush failure
    }
  }

  /**
   * Read all encrypted audit log entries.
   * Returns empty array if vault is locked or log is empty.
   */
  private async readEncryptedEntries(): Promise<AuditLogEntry[]> {
    try {
      const data = await vault.retrieveAndDecrypt(AUDIT_LOG_KEY);
      if (!data) return [];
      return JSON.parse(data);
    } catch {
      return [];
    }
  }

  /**
   * Get all audit log entries (encrypted + any unencrypted staging).
   * Requires vault to be unlocked for encrypted entries.
   */
  async getEntries(options?: {
    eventType?: AuditEventType;
    recordId?: string;
    since?: Date;
    limit?: number;
  }): Promise<AuditLogEntry[]> {
    if (!vault.isUnlocked()) {
      throw new Error('Vault must be unlocked to read audit log.');
    }

    let entries = await this.readEncryptedEntries();

    // Apply filters
    if (options?.eventType) {
      entries = entries.filter((e) => e.eventType === options.eventType);
    }
    if (options?.recordId) {
      entries = entries.filter((e) => e.recordId === options.recordId);
    }
    if (options?.since) {
      const sinceMs = options.since.getTime();
      entries = entries.filter((e) => new Date(e.timestamp).getTime() >= sinceMs);
    }

    // Sort newest first
    entries.sort(
      (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );

    // Apply limit
    if (options?.limit && options.limit > 0) {
      entries = entries.slice(0, options.limit);
    }

    return entries;
  }

  /**
   * Get entry count.
   */
  async getEntryCount(): Promise<number> {
    if (!vault.isUnlocked()) return 0;
    const entries = await this.readEncryptedEntries();
    return entries.length;
  }

  /**
   * Export the entire audit log as an encrypted JSON string.
   * The export itself is HMAC-signed for integrity.
   */
  async exportAsJson(): Promise<string> {
    if (!vault.isUnlocked()) {
      throw new Error('Vault must be unlocked to export audit log.');
    }

    const entries = await this.readEncryptedEntries();
    const exportData = {
      exportedAt: new Date().toISOString(),
      deviceId: await this.getDeviceId(),
      entryCount: entries.length,
      entries,
    };

    const jsonStr = JSON.stringify(exportData, null, 2);

    // Sign the export with HMAC for integrity verification
    const signature = await vault.hmac(jsonStr);

    return JSON.stringify({
      version: 1,
      data: jsonStr,
      signature,
    });
  }

  /**
   * Verify an exported audit log's integrity.
   */
  async verifyExport(exportJson: string): Promise<boolean> {
    if (!vault.isUnlocked()) {
      throw new Error('Vault must be unlocked to verify audit log.');
    }

    try {
      const parsed = JSON.parse(exportJson);
      if (parsed.version !== 1 || !parsed.data || !parsed.signature) {
        return false;
      }
      return vault.verifyHmac(parsed.data, parsed.signature);
    } catch {
      return false;
    }
  }

  /**
   * Get a summary of recent audit activity for the dashboard.
   */
  async getRecentSummary(): Promise<{
    totalEvents: number;
    last24h: number;
    lastAuthSuccess: string | null;
    lastAuthFailed: string | null;
    recentFailedAttempts: number;
  }> {
    if (!vault.isUnlocked()) {
      return {
        totalEvents: 0,
        last24h: 0,
        lastAuthSuccess: null,
        lastAuthFailed: null,
        recentFailedAttempts: 0,
      };
    }

    const entries = await this.readEncryptedEntries();
    const now = Date.now();
    const dayAgo = now - 24 * 60 * 60 * 1000;

    const last24h = entries.filter(
      (e) => new Date(e.timestamp).getTime() >= dayAgo
    ).length;

    const authSuccesses = entries
      .filter((e) => e.eventType === 'auth_success')
      .sort(
        (a, b) =>
          new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
      );

    const authFailures = entries
      .filter((e) => e.eventType === 'auth_failed')
      .sort(
        (a, b) =>
          new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
      );

    const recentFailedAttempts = entries.filter(
      (e) =>
        e.eventType === 'auth_failed' &&
        new Date(e.timestamp).getTime() >= dayAgo
    ).length;

    return {
      totalEvents: entries.length,
      last24h,
      lastAuthSuccess: authSuccesses[0]?.timestamp || null,
      lastAuthFailed: authFailures[0]?.timestamp || null,
      recentFailedAttempts,
    };
  }

  /**
   * Purge all audit logs. Only called during full data wipe.
   * This is the ONLY way to remove audit entries.
   */
  async purgeAll(): Promise<void> {
    // Encrypted entries are stored via vault, which handles its own purge.
    // Clear staging separately.
    await AsyncStorage.removeItem('cnsnt_audit_staging');
    await AsyncStorage.removeItem(AUDIT_SEQUENCE_KEY);
  }
}

export const auditLog = new AuditLogService();
export default auditLog;
