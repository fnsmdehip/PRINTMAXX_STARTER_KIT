/**
 * Cloud Backup Connector System for cnsnt app.
 *
 * Architecture: local-first, zero centralized server.
 * All data encrypted BEFORE it leaves the device.
 * Cloud providers receive encrypted blobs only.
 *
 * Connectors:
 *  1. iCloud - via DocumentDirectory (iOS auto-syncs to iCloud)
 *  2. Google Drive - REST API + OAuth via expo-auth-session
 *  3. Dropbox - REST API + OAuth via expo-auth-session
 *  4. Local Export - manual .cnsnt file export/import
 *
 * Backup format: CnsntBackup envelope with AES-encrypted payload + HMAC integrity.
 */

import * as FileSystem from 'expo-file-system';
import * as Crypto from 'expo-crypto';
import * as Sharing from 'expo-sharing';
import * as AuthSession from 'expo-auth-session';
import * as WebBrowser from 'expo-web-browser';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform, Alert } from 'react-native';
import * as Device from 'expo-device';
import vault from './encryption';
import db from './database';
import type { ConsentRecord } from '../types';

// ─── Backup Format ──────────────────────────────────────────────────────

export interface CnsntBackup {
  version: 1;
  createdAt: string;
  deviceId: string;
  recordCount: number;
  encryptedPayload: string;
  payloadHash: string;
  metadata: {
    appVersion: string;
    platform: 'ios' | 'android';
    backupType: 'full' | 'incremental';
  };
}

export type CloudProvider = 'icloud' | 'gdrive' | 'dropbox' | 'local';

export type BackupHealthStatus = 'good' | 'warning' | 'critical' | 'never';

export interface BackupInfo {
  provider: CloudProvider;
  timestamp: string;
  recordCount: number;
  filename: string;
}

export interface CloudConnectionState {
  icloud: { connected: boolean; lastBackup: string | null };
  gdrive: { connected: boolean; lastBackup: string | null; email: string | null };
  dropbox: { connected: boolean; lastBackup: string | null; email: string | null };
}

// ─── Storage Keys ───────────────────────────────────────────────────────

const BACKUP_PREFS_KEY = 'cnsnt_backup_prefs';
const GDRIVE_TOKEN_KEY = 'cnsnt_gdrive_token';
const DROPBOX_TOKEN_KEY = 'cnsnt_dropbox_token';
const LAST_BACKUP_KEY = 'cnsnt_last_backup';
const AUTO_BACKUP_KEY = 'cnsnt_auto_backup_enabled';
const GDRIVE_EMAIL_KEY = 'cnsnt_gdrive_email';
const DROPBOX_EMAIL_KEY = 'cnsnt_dropbox_email';

// ─── OAuth Config ───────────────────────────────────────────────────────

// These are configured in app.json scheme: "cnsnt"
// Redirect URI = cnsnt://oauth (handled by expo-auth-session)

const GOOGLE_CLIENT_ID_IOS = '__GOOGLE_IOS_CLIENT_ID__';
const GOOGLE_CLIENT_ID_ANDROID = '__GOOGLE_ANDROID_CLIENT_ID__';

const DROPBOX_APP_KEY = '__DROPBOX_APP_KEY__';

const GOOGLE_SCOPES = [
  'https://www.googleapis.com/auth/drive.file',
  'https://www.googleapis.com/auth/userinfo.email',
];

/**
 * Check whether a provider's OAuth credentials are real (not placeholders).
 * Placeholder values start with '__' and end with '__'.
 * Returns false if the client ID/app key is still a placeholder.
 */
function isOAuthConfigured(provider: 'gdrive' | 'dropbox'): boolean {
  if (provider === 'gdrive') {
    const clientId =
      Platform.OS === 'ios' ? GOOGLE_CLIENT_ID_IOS : GOOGLE_CLIENT_ID_ANDROID;
    return !clientId.startsWith('__') && clientId.length > 0;
  }
  if (provider === 'dropbox') {
    return !DROPBOX_APP_KEY.startsWith('__') && DROPBOX_APP_KEY.length > 0;
  }
  return false;
}

// Ensure web browser sessions complete properly
WebBrowser.maybeCompleteAuthSession();

// ─── Encryption Helpers ─────────────────────────────────────────────────

/**
 * Encrypt a plaintext string using the vault's current key.
 * Returns the vault's iv:ciphertext:mac format string.
 * Vault must be unlocked.
 */
async function encryptPayload(plaintext: string): Promise<string> {
  // Use the vault's encrypt-and-store mechanism, extract the encrypted data,
  // then clean up the temp key. The vault produces iv:ciphertext:mac format
  // which already includes the random IV and authentication MAC.
  const tempKey = `_backup_temp_${Date.now()}`;
  await vault.encryptAndStore(tempKey, plaintext);
  const raw = await AsyncStorage.getItem(`vault_${tempKey}`);
  await AsyncStorage.removeItem(`vault_${tempKey}`);
  if (!raw) throw new Error('Encryption failed: no output produced');
  const envelope = JSON.parse(raw);
  return envelope.data;
}

/**
 * Decrypt an iv:ciphertext:mac string back to plaintext using the vault.
 * Vault must be unlocked with the same key that encrypted it.
 *
 * Works by storing the encrypted data in a temporary vault envelope (v2 format)
 * and using the vault's standard retrieveAndDecrypt, which handles IV extraction
 * and MAC verification internally. The temp key is always cleaned up.
 */
async function decryptPayload(encrypted: string): Promise<string> {
  const tempKey = `_backup_restore_${Date.now()}`;
  try {
    // Build a v2 vault envelope that retrieveAndDecrypt knows how to handle.
    // The vault's v2 path decrypts the iv:ciphertext:mac string directly
    // with full MAC verification -- no plaintext hash needed.
    const envelope = JSON.stringify({
      version: 2,
      data: encrypted,
      timestamp: new Date().toISOString(),
    });
    await AsyncStorage.setItem(`vault_${tempKey}`, envelope);
    const result = await vault.retrieveAndDecrypt(tempKey);
    if (result === null) {
      throw new Error('Decryption returned null -- vault key may not match.');
    }
    return result;
  } finally {
    // Always clean up, even on error
    await AsyncStorage.removeItem(`vault_${tempKey}`);
  }
}

/**
 * Compute HMAC-SHA-256 of data using the vault's MAC key.
 * Used for backup integrity verification.
 * Vault must be unlocked.
 */
async function computeHmac(data: string): Promise<string> {
  if (!vault.isUnlocked()) {
    throw new Error('Vault must be unlocked to compute backup HMAC.');
  }
  return vault.hmac(data);
}

// ─── Backup Creation ────────────────────────────────────────────────────

/**
 * Create a full backup of all records, templates settings, and audit data.
 * Everything is encrypted with the user's vault key before packaging.
 */
async function createBackup(): Promise<CnsntBackup> {
  if (!vault.isUnlocked()) {
    throw new Error('Vault must be unlocked to create backups.');
  }

  // Gather all data
  const records = await db.getAllRecords();

  // Get custom templates from AsyncStorage
  let customTemplates: unknown[] = [];
  try {
    const templatesRaw = await AsyncStorage.getItem('cnsnt_custom_templates');
    if (templatesRaw) customTemplates = JSON.parse(templatesRaw);
  } catch {
    // no custom templates
  }

  // Get user preferences
  let preferences: Record<string, string> = {};
  try {
    const keys = await AsyncStorage.getAllKeys();
    const cnsntKeys = keys.filter(
      (k) => k.startsWith('cnsnt_') && !k.startsWith('vault_')
    );
    const pairs = await AsyncStorage.multiGet(cnsntKeys);
    for (const [key, value] of pairs) {
      if (value !== null) preferences[key] = value;
    }
  } catch {
    // preferences optional
  }

  const payload = JSON.stringify({
    records,
    customTemplates,
    preferences,
    exportedAt: new Date().toISOString(),
  });

  // Encrypt the entire payload
  const encryptedPayload = await encryptPayload(payload);

  // HMAC for integrity verification
  const payloadHash = await computeHmac(encryptedPayload);

  const deviceId = Device.modelId || Device.deviceName || 'unknown';

  const backup: CnsntBackup = {
    version: 1,
    createdAt: new Date().toISOString(),
    deviceId,
    recordCount: records.length,
    encryptedPayload,
    payloadHash,
    metadata: {
      appVersion: '1.0.0',
      platform: Platform.OS === 'ios' ? 'ios' : 'android',
      backupType: 'full',
    },
  };

  return backup;
}

/**
 * Restore from a CnsntBackup object. Decrypts and verifies integrity.
 * Returns the decrypted records for the caller to decide merge vs replace.
 */
async function restoreFromBackup(backup: CnsntBackup): Promise<{
  records: ConsentRecord[];
  customTemplates: unknown[];
  preferences: Record<string, string>;
}> {
  if (!vault.isUnlocked()) {
    throw new Error('Vault must be unlocked to restore backups.');
  }

  if (backup.version !== 1) {
    throw new Error(`Unsupported backup version: ${backup.version}`);
  }

  // Verify HMAC integrity
  const computedHash = await computeHmac(backup.encryptedPayload);
  if (computedHash !== backup.payloadHash) {
    throw new Error(
      'Backup integrity check failed. The file may be corrupted or was encrypted with a different vault key.'
    );
  }

  // Decrypt
  const plaintext = await decryptPayload(backup.encryptedPayload);

  let parsed: {
    records: ConsentRecord[];
    customTemplates: unknown[];
    preferences: Record<string, string>;
  };

  try {
    parsed = JSON.parse(plaintext);
  } catch {
    throw new Error(
      'Failed to parse decrypted backup. The vault key may not match the one used to create this backup.'
    );
  }

  if (!Array.isArray(parsed.records)) {
    throw new Error('Invalid backup structure: missing records array.');
  }

  return {
    records: parsed.records,
    customTemplates: parsed.customTemplates || [],
    preferences: parsed.preferences || {},
  };
}

/**
 * Apply restored data to the local database.
 * mode 'replace' clears existing data first.
 * mode 'merge' adds records that don't already exist (by ID).
 */
async function applyRestore(
  data: {
    records: ConsentRecord[];
    customTemplates: unknown[];
    preferences: Record<string, string>;
  },
  mode: 'replace' | 'merge'
): Promise<{ imported: number; skipped: number }> {
  let imported = 0;
  let skipped = 0;

  if (mode === 'replace') {
    await db.deleteAllRecords();
  }

  const existingRecords = mode === 'merge' ? await db.getAllRecords() : [];
  const existingIds = new Set(existingRecords.map((r) => r.id));

  for (const record of data.records) {
    if (mode === 'merge' && existingIds.has(record.id)) {
      skipped++;
      continue;
    }

    // Re-create record through the database service (re-encrypts with current key)
    const { id, ...rest } = record;
    await db.createRecord(rest);
    imported++;
  }

  // Restore custom templates
  if (data.customTemplates && data.customTemplates.length > 0) {
    if (mode === 'replace') {
      await AsyncStorage.setItem(
        'cnsnt_custom_templates',
        JSON.stringify(data.customTemplates)
      );
    } else {
      // Merge: append any templates that don't exist
      let existing: unknown[] = [];
      try {
        const raw = await AsyncStorage.getItem('cnsnt_custom_templates');
        if (raw) existing = JSON.parse(raw);
      } catch {
        // nothing
      }
      const merged = [...existing, ...data.customTemplates];
      await AsyncStorage.setItem('cnsnt_custom_templates', JSON.stringify(merged));
    }
  }

  // Record the restore event
  await recordBackupEvent('restore', mode);

  return { imported, skipped };
}

// ─── iCloud Connector ───────────────────────────────────────────────────

/**
 * iCloud backup works by writing an encrypted file to the app's Documents
 * directory. On iOS, if iCloud Drive is enabled, this directory is
 * automatically synced. On Android this falls back to local-only storage.
 */
const iCloudConnector = {
  async isAvailable(): Promise<boolean> {
    return Platform.OS === 'ios';
  },

  async backup(): Promise<BackupInfo> {
    const backupData = await createBackup();
    const filename = `cnsnt_backup_${formatTimestamp(backupData.createdAt)}.cnsnt`;
    const filePath = `${FileSystem.documentDirectory}${filename}`;

    await FileSystem.writeAsStringAsync(filePath, JSON.stringify(backupData));

    const info: BackupInfo = {
      provider: 'icloud',
      timestamp: backupData.createdAt,
      recordCount: backupData.recordCount,
      filename,
    };

    await saveLastBackupInfo(info);
    await recordBackupEvent('backup', 'icloud');

    return info;
  },

  async listBackups(): Promise<BackupInfo[]> {
    const dirUri = FileSystem.documentDirectory;
    if (!dirUri) return [];

    const files = await FileSystem.readDirectoryAsync(dirUri);
    const backupFiles = files.filter(
      (f) => f.startsWith('cnsnt_backup_') && f.endsWith('.cnsnt')
    );

    const infos: BackupInfo[] = [];
    for (const filename of backupFiles) {
      try {
        const content = await FileSystem.readAsStringAsync(`${dirUri}${filename}`);
        const backup: CnsntBackup = JSON.parse(content);
        infos.push({
          provider: 'icloud',
          timestamp: backup.createdAt,
          recordCount: backup.recordCount,
          filename,
        });
      } catch {
        // Corrupted file, skip
      }
    }

    return infos.sort(
      (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );
  },

  async restore(filename: string): Promise<CnsntBackup> {
    const filePath = `${FileSystem.documentDirectory}${filename}`;
    const fileInfo = await FileSystem.getInfoAsync(filePath);

    if (!fileInfo.exists) {
      throw new Error(`Backup file not found: ${filename}`);
    }

    const content = await FileSystem.readAsStringAsync(filePath);
    return JSON.parse(content) as CnsntBackup;
  },

  async deleteBackup(filename: string): Promise<void> {
    const filePath = `${FileSystem.documentDirectory}${filename}`;
    await FileSystem.deleteAsync(filePath, { idempotent: true });
  },
};

// ─── Google Drive Connector ─────────────────────────────────────────────

const gDriveConnector = {
  async getAccessToken(): Promise<string | null> {
    return AsyncStorage.getItem(GDRIVE_TOKEN_KEY);
  },

  async isConnected(): Promise<boolean> {
    const token = await this.getAccessToken();
    if (!token) return false;

    // Verify token is still valid
    try {
      const resp = await fetch('https://www.googleapis.com/oauth2/v1/tokeninfo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `access_token=${token}`,
      });
      return resp.ok;
    } catch {
      return false;
    }
  },

  async connect(): Promise<boolean> {
    if (!isOAuthConfigured('gdrive')) {
      throw new Error(
        'Google Drive is not configured. Set GOOGLE_IOS_CLIENT_ID / GOOGLE_ANDROID_CLIENT_ID in your environment to enable Google Drive backup.'
      );
    }

    const clientId =
      Platform.OS === 'ios' ? GOOGLE_CLIENT_ID_IOS : GOOGLE_CLIENT_ID_ANDROID;

    const redirectUri = AuthSession.makeRedirectUri({ scheme: 'cnsnt' });

    const discovery: AuthSession.DiscoveryDocument = {
      authorizationEndpoint: 'https://accounts.google.com/o/oauth2/v2/auth',
      tokenEndpoint: 'https://oauth2.googleapis.com/token',
      revocationEndpoint: 'https://oauth2.googleapis.com/revoke',
    };

    const request = new AuthSession.AuthRequest({
      clientId,
      redirectUri,
      scopes: GOOGLE_SCOPES,
      responseType: AuthSession.ResponseType.Token,
      usePKCE: false,
    });

    const result = await request.promptAsync(discovery);

    if (result.type === 'success' && result.authentication?.accessToken) {
      const accessToken = result.authentication.accessToken;
      await AsyncStorage.setItem(GDRIVE_TOKEN_KEY, accessToken);

      // Fetch user email for display
      try {
        const userResp = await fetch(
          'https://www.googleapis.com/oauth2/v2/userinfo',
          { headers: { Authorization: `Bearer ${accessToken}` } }
        );
        if (userResp.ok) {
          const userData = await userResp.json();
          if (userData.email) {
            await AsyncStorage.setItem(GDRIVE_EMAIL_KEY, userData.email);
          }
        }
      } catch {
        // email fetch is optional
      }

      return true;
    }

    return false;
  },

  async disconnect(): Promise<void> {
    const token = await this.getAccessToken();
    if (token) {
      // Revoke the token
      try {
        await fetch(
          `https://oauth2.googleapis.com/revoke?token=${token}`,
          { method: 'POST' }
        );
      } catch {
        // Best effort revocation
      }
    }
    await AsyncStorage.removeItem(GDRIVE_TOKEN_KEY);
    await AsyncStorage.removeItem(GDRIVE_EMAIL_KEY);
  },

  async getEmail(): Promise<string | null> {
    return AsyncStorage.getItem(GDRIVE_EMAIL_KEY);
  },

  /**
   * Find or create the cnsnt_backups folder in Google Drive.
   */
  async ensureBackupFolder(token: string): Promise<string> {
    // Search for existing folder
    const searchUrl = `https://www.googleapis.com/drive/v3/files?q=${encodeURIComponent(
      "name='cnsnt_backups' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    )}&fields=files(id,name)`;

    const searchResp = await fetch(searchUrl, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!searchResp.ok) {
      throw new Error(`Google Drive search failed: ${searchResp.status}`);
    }

    const searchData = await searchResp.json();
    if (searchData.files && searchData.files.length > 0) {
      return searchData.files[0].id;
    }

    // Create the folder
    const createResp = await fetch(
      'https://www.googleapis.com/drive/v3/files',
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: 'cnsnt_backups',
          mimeType: 'application/vnd.google-apps.folder',
        }),
      }
    );

    if (!createResp.ok) {
      throw new Error(`Failed to create backup folder: ${createResp.status}`);
    }

    const folderData = await createResp.json();
    return folderData.id;
  },

  async backup(): Promise<BackupInfo> {
    const token = await this.getAccessToken();
    if (!token) throw new Error('Not connected to Google Drive. Connect first.');

    const backupData = await createBackup();
    const filename = `cnsnt_backup_${formatTimestamp(backupData.createdAt)}.enc`;
    const folderId = await this.ensureBackupFolder(token);

    // Multipart upload to Google Drive
    const boundary = 'cnsnt_backup_boundary_' + Date.now();
    const fileContent = JSON.stringify(backupData);

    const metadata = JSON.stringify({
      name: filename,
      parents: [folderId],
      mimeType: 'application/octet-stream',
    });

    const body =
      `--${boundary}\r\n` +
      'Content-Type: application/json; charset=UTF-8\r\n\r\n' +
      metadata +
      '\r\n' +
      `--${boundary}\r\n` +
      'Content-Type: application/octet-stream\r\n\r\n' +
      fileContent +
      '\r\n' +
      `--${boundary}--`;

    const uploadResp = await fetch(
      'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart',
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': `multipart/related; boundary=${boundary}`,
        },
        body,
      }
    );

    if (!uploadResp.ok) {
      const errorText = await uploadResp.text();
      throw new Error(
        `Google Drive upload failed (${uploadResp.status}): ${errorText}`
      );
    }

    const info: BackupInfo = {
      provider: 'gdrive',
      timestamp: backupData.createdAt,
      recordCount: backupData.recordCount,
      filename,
    };

    await saveLastBackupInfo(info);
    await recordBackupEvent('backup', 'gdrive');

    return info;
  },

  async listBackups(): Promise<BackupInfo[]> {
    const token = await this.getAccessToken();
    if (!token) return [];

    try {
      const folderId = await this.ensureBackupFolder(token);

      const listUrl = `https://www.googleapis.com/drive/v3/files?q=${encodeURIComponent(
        `'${folderId}' in parents and trashed=false`
      )}&fields=files(id,name,createdTime,size)&orderBy=createdTime desc&pageSize=50`;

      const resp = await fetch(listUrl, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!resp.ok) return [];

      const data = await resp.json();
      const backups: BackupInfo[] = [];

      for (const file of data.files || []) {
        if (file.name.startsWith('cnsnt_backup_') && file.name.endsWith('.enc')) {
          backups.push({
            provider: 'gdrive',
            timestamp: file.createdTime,
            recordCount: 0, // Would need to download to check
            filename: file.id, // Use file ID for download
          });
        }
      }

      return backups;
    } catch {
      return [];
    }
  },

  async restore(fileId: string): Promise<CnsntBackup> {
    const token = await this.getAccessToken();
    if (!token) throw new Error('Not connected to Google Drive.');

    const downloadUrl = `https://www.googleapis.com/drive/v3/files/${fileId}?alt=media`;
    const resp = await fetch(downloadUrl, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!resp.ok) {
      throw new Error(`Failed to download backup: ${resp.status}`);
    }

    const content = await resp.text();
    return JSON.parse(content) as CnsntBackup;
  },

  async deleteBackup(fileId: string): Promise<void> {
    const token = await this.getAccessToken();
    if (!token) throw new Error('Not connected to Google Drive.');

    await fetch(`https://www.googleapis.com/drive/v3/files/${fileId}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` },
    });
  },
};

// ─── Dropbox Connector ──────────────────────────────────────────────────

const dropboxConnector = {
  async getAccessToken(): Promise<string | null> {
    return AsyncStorage.getItem(DROPBOX_TOKEN_KEY);
  },

  async isConnected(): Promise<boolean> {
    const token = await this.getAccessToken();
    if (!token) return false;

    try {
      const resp = await fetch(
        'https://api.dropboxapi.com/2/users/get_current_account',
        {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      return resp.ok;
    } catch {
      return false;
    }
  },

  async connect(): Promise<boolean> {
    if (!isOAuthConfigured('dropbox')) {
      throw new Error(
        'Dropbox is not configured. Set DROPBOX_APP_KEY in your environment to enable Dropbox backup.'
      );
    }

    const redirectUri = AuthSession.makeRedirectUri({ scheme: 'cnsnt' });

    const request = new AuthSession.AuthRequest({
      clientId: DROPBOX_APP_KEY,
      redirectUri,
      scopes: [],
      responseType: AuthSession.ResponseType.Token,
      usePKCE: false,
      extraParams: {
        token_access_type: 'offline',
      },
    });

    const discovery: AuthSession.DiscoveryDocument = {
      authorizationEndpoint: 'https://www.dropbox.com/oauth2/authorize',
      tokenEndpoint: 'https://api.dropboxapi.com/oauth2/token',
    };

    const result = await request.promptAsync(discovery);

    if (result.type === 'success' && result.authentication?.accessToken) {
      const accessToken = result.authentication.accessToken;
      await AsyncStorage.setItem(DROPBOX_TOKEN_KEY, accessToken);

      // Fetch account email for display
      try {
        const acctResp = await fetch(
          'https://api.dropboxapi.com/2/users/get_current_account',
          {
            method: 'POST',
            headers: { Authorization: `Bearer ${accessToken}` },
          }
        );
        if (acctResp.ok) {
          const acctData = await acctResp.json();
          if (acctData.email) {
            await AsyncStorage.setItem(DROPBOX_EMAIL_KEY, acctData.email);
          }
        }
      } catch {
        // email fetch is optional
      }

      return true;
    }

    return false;
  },

  async disconnect(): Promise<void> {
    const token = await this.getAccessToken();
    if (token) {
      try {
        await fetch('https://api.dropboxapi.com/2/auth/token/revoke', {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` },
        });
      } catch {
        // Best effort
      }
    }
    await AsyncStorage.removeItem(DROPBOX_TOKEN_KEY);
    await AsyncStorage.removeItem(DROPBOX_EMAIL_KEY);
  },

  async getEmail(): Promise<string | null> {
    return AsyncStorage.getItem(DROPBOX_EMAIL_KEY);
  },

  async backup(): Promise<BackupInfo> {
    const token = await this.getAccessToken();
    if (!token) throw new Error('Not connected to Dropbox. Connect first.');

    const backupData = await createBackup();
    const filename = `cnsnt_backup_${formatTimestamp(backupData.createdAt)}.enc`;
    const fileContent = JSON.stringify(backupData);

    const uploadResp = await fetch(
      'https://content.dropboxapi.com/2/files/upload',
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/octet-stream',
          'Dropbox-API-Arg': JSON.stringify({
            path: `/Apps/cnsnt/${filename}`,
            mode: 'add',
            autorename: true,
            mute: false,
          }),
        },
        body: fileContent,
      }
    );

    if (!uploadResp.ok) {
      const errorText = await uploadResp.text();

      // If folder doesn't exist, create it and retry
      if (uploadResp.status === 409) {
        await this.ensureFolder(token);

        const retryResp = await fetch(
          'https://content.dropboxapi.com/2/files/upload',
          {
            method: 'POST',
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/octet-stream',
              'Dropbox-API-Arg': JSON.stringify({
                path: `/Apps/cnsnt/${filename}`,
                mode: 'add',
                autorename: true,
                mute: false,
              }),
            },
            body: fileContent,
          }
        );

        if (!retryResp.ok) {
          throw new Error(`Dropbox upload failed after folder creation: ${retryResp.status}`);
        }
      } else {
        throw new Error(`Dropbox upload failed (${uploadResp.status}): ${errorText}`);
      }
    }

    const info: BackupInfo = {
      provider: 'dropbox',
      timestamp: backupData.createdAt,
      recordCount: backupData.recordCount,
      filename,
    };

    await saveLastBackupInfo(info);
    await recordBackupEvent('backup', 'dropbox');

    return info;
  },

  async ensureFolder(token: string): Promise<void> {
    try {
      await fetch('https://api.dropboxapi.com/2/files/create_folder_v2', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ path: '/Apps/cnsnt', autorename: false }),
      });
    } catch {
      // Folder may already exist, that's fine
    }
  },

  async listBackups(): Promise<BackupInfo[]> {
    const token = await this.getAccessToken();
    if (!token) return [];

    try {
      const resp = await fetch(
        'https://api.dropboxapi.com/2/files/list_folder',
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            path: '/Apps/cnsnt',
            recursive: false,
            include_deleted: false,
          }),
        }
      );

      if (!resp.ok) return [];

      const data = await resp.json();
      const backups: BackupInfo[] = [];

      for (const entry of data.entries || []) {
        if (
          entry['.tag'] === 'file' &&
          entry.name.startsWith('cnsnt_backup_') &&
          entry.name.endsWith('.enc')
        ) {
          backups.push({
            provider: 'dropbox',
            timestamp: entry.server_modified || entry.client_modified || '',
            recordCount: 0,
            filename: entry.path_lower,
          });
        }
      }

      return backups.sort(
        (a, b) =>
          new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
      );
    } catch {
      return [];
    }
  },

  async restore(filePath: string): Promise<CnsntBackup> {
    const token = await this.getAccessToken();
    if (!token) throw new Error('Not connected to Dropbox.');

    const resp = await fetch(
      'https://content.dropboxapi.com/2/files/download',
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Dropbox-API-Arg': JSON.stringify({ path: filePath }),
        },
      }
    );

    if (!resp.ok) {
      throw new Error(`Failed to download from Dropbox: ${resp.status}`);
    }

    const content = await resp.text();
    return JSON.parse(content) as CnsntBackup;
  },

  async deleteBackup(filePath: string): Promise<void> {
    const token = await this.getAccessToken();
    if (!token) throw new Error('Not connected to Dropbox.');

    await fetch('https://api.dropboxapi.com/2/files/delete_v2', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ path: filePath }),
    });
  },
};

// ─── Local Export Connector ─────────────────────────────────────────────

const localExportConnector = {
  /**
   * Export encrypted backup as a .cnsnt file and open the share sheet.
   * User can AirDrop, email, save to Files, etc.
   */
  async exportBackup(): Promise<BackupInfo> {
    const backupData = await createBackup();
    const filename = `cnsnt_backup_${formatTimestamp(backupData.createdAt)}.cnsnt`;
    const filePath = `${FileSystem.cacheDirectory}${filename}`;

    await FileSystem.writeAsStringAsync(filePath, JSON.stringify(backupData));

    const sharingAvailable = await Sharing.isAvailableAsync();
    if (!sharingAvailable) {
      throw new Error('Sharing is not available on this device.');
    }

    await Sharing.shareAsync(filePath, {
      mimeType: 'application/octet-stream',
      dialogTitle: 'Export cnsnt Backup',
      UTI: 'public.data',
    });

    const info: BackupInfo = {
      provider: 'local',
      timestamp: backupData.createdAt,
      recordCount: backupData.recordCount,
      filename,
    };

    await saveLastBackupInfo(info);
    await recordBackupEvent('backup', 'local_export');

    return info;
  },

  /**
   * Import a .cnsnt backup file from a URI.
   * The URI comes from expo-document-picker or a deep link.
   */
  async importFromUri(fileUri: string): Promise<CnsntBackup> {
    const content = await FileSystem.readAsStringAsync(fileUri);
    const backup = JSON.parse(content) as CnsntBackup;

    if (!backup.version || !backup.encryptedPayload || !backup.payloadHash) {
      throw new Error('Invalid .cnsnt backup file format.');
    }

    return backup;
  },

  /**
   * Import from a raw JSON string (for clipboard paste or other input methods).
   */
  async importFromString(jsonString: string): Promise<CnsntBackup> {
    const backup = JSON.parse(jsonString) as CnsntBackup;

    if (!backup.version || !backup.encryptedPayload || !backup.payloadHash) {
      throw new Error('Invalid backup data format.');
    }

    return backup;
  },
};

// ─── Auto-Backup Manager ────────────────────────────────────────────────

let autoBackupDebounceTimer: ReturnType<typeof setTimeout> | null = null;
const AUTO_BACKUP_DEBOUNCE_MS = 60 * 60 * 1000; // 1 hour

/**
 * Trigger auto-backup (debounced to max 1 per hour).
 * Call this after every record change.
 */
async function triggerAutoBackup(): Promise<void> {
  const enabled = await isAutoBackupEnabled();
  if (!enabled) return;

  if (autoBackupDebounceTimer) {
    clearTimeout(autoBackupDebounceTimer);
  }

  autoBackupDebounceTimer = setTimeout(async () => {
    try {
      // Check which providers are connected and backup to all of them
      const connections = await getConnectionState();

      if (connections.icloud.connected && Platform.OS === 'ios') {
        await iCloudConnector.backup();
      }

      if (connections.gdrive.connected) {
        try {
          await gDriveConnector.backup();
        } catch {
          // Token may have expired, silently fail
        }
      }

      if (connections.dropbox.connected) {
        try {
          await dropboxConnector.backup();
        } catch {
          // Token may have expired, silently fail
        }
      }
    } catch {
      // Auto-backup failures are silent - user will see health indicator
    }
  }, 5000); // 5 second debounce before actually running
}

// ─── Preferences & State ────────────────────────────────────────────────

async function isAutoBackupEnabled(): Promise<boolean> {
  const value = await AsyncStorage.getItem(AUTO_BACKUP_KEY);
  return value === 'true';
}

async function setAutoBackupEnabled(enabled: boolean): Promise<void> {
  await AsyncStorage.setItem(AUTO_BACKUP_KEY, enabled ? 'true' : 'false');
}

async function saveLastBackupInfo(info: BackupInfo): Promise<void> {
  const existing = await getLastBackupInfo();
  existing[info.provider] = info;
  await AsyncStorage.setItem(LAST_BACKUP_KEY, JSON.stringify(existing));
}

async function getLastBackupInfo(): Promise<
  Partial<Record<CloudProvider, BackupInfo>>
> {
  try {
    const raw = await AsyncStorage.getItem(LAST_BACKUP_KEY);
    if (raw) return JSON.parse(raw);
  } catch {
    // Corrupted data
  }
  return {};
}

async function getLastBackupTime(): Promise<string | null> {
  const infos = await getLastBackupInfo();
  let latest: string | null = null;

  for (const info of Object.values(infos)) {
    if (info && (!latest || new Date(info.timestamp) > new Date(latest))) {
      latest = info.timestamp;
    }
  }

  return latest;
}

function getBackupHealthStatus(lastBackupTime: string | null): BackupHealthStatus {
  if (!lastBackupTime) return 'never';

  const now = new Date();
  const backupDate = new Date(lastBackupTime);
  const hoursSince = (now.getTime() - backupDate.getTime()) / (1000 * 60 * 60);

  if (hoursSince < 24) return 'good';
  if (hoursSince < 168) return 'warning'; // 7 days
  return 'critical';
}

async function getConnectionState(): Promise<CloudConnectionState> {
  const gdriveConnected = await gDriveConnector.isConnected();
  const dropboxConnected = await dropboxConnector.isConnected();
  const icloudAvailable = await iCloudConnector.isAvailable();

  const lastBackups = await getLastBackupInfo();

  return {
    icloud: {
      connected: icloudAvailable,
      lastBackup: lastBackups.icloud?.timestamp || null,
    },
    gdrive: {
      connected: gdriveConnected,
      lastBackup: lastBackups.gdrive?.timestamp || null,
      email: gdriveConnected ? await gDriveConnector.getEmail() : null,
    },
    dropbox: {
      connected: dropboxConnected,
      lastBackup: lastBackups.dropbox?.timestamp || null,
      email: dropboxConnected ? await dropboxConnector.getEmail() : null,
    },
  };
}

async function recordBackupEvent(
  action: 'backup' | 'restore',
  detail: string
): Promise<void> {
  try {
    const eventsRaw = await AsyncStorage.getItem('cnsnt_backup_audit_log');
    const events: Array<{
      action: string;
      detail: string;
      timestamp: string;
    }> = eventsRaw ? JSON.parse(eventsRaw) : [];

    events.unshift({
      action,
      detail,
      timestamp: new Date().toISOString(),
    });

    // Keep last 100 events
    const trimmed = events.slice(0, 100);
    await AsyncStorage.setItem('cnsnt_backup_audit_log', JSON.stringify(trimmed));
  } catch {
    // Audit log failure is non-fatal
  }
}

// ─── Utilities ──────────────────────────────────────────────────────────

function formatTimestamp(isoString: string): string {
  return isoString.replace(/[:.]/g, '-').substring(0, 19);
}

function formatRelativeTime(isoString: string): string {
  const now = new Date();
  const date = new Date(isoString);
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString();
}

// ─── Unified Cloud Backup Service ───────────────────────────────────────

class CloudBackupService {
  // ── Core backup/restore ──

  async createBackup(): Promise<CnsntBackup> {
    return createBackup();
  }

  async restoreFromBackup(
    backup: CnsntBackup
  ): Promise<{
    records: ConsentRecord[];
    customTemplates: unknown[];
    preferences: Record<string, string>;
  }> {
    return restoreFromBackup(backup);
  }

  async applyRestore(
    data: {
      records: ConsentRecord[];
      customTemplates: unknown[];
      preferences: Record<string, string>;
    },
    mode: 'replace' | 'merge'
  ): Promise<{ imported: number; skipped: number }> {
    return applyRestore(data, mode);
  }

  // ── Provider-specific operations ──

  get icloud() {
    return iCloudConnector;
  }

  get gdrive() {
    return gDriveConnector;
  }

  get dropbox() {
    return dropboxConnector;
  }

  get local() {
    return localExportConnector;
  }

  // ── Backup to a specific provider ──

  async backupTo(provider: CloudProvider): Promise<BackupInfo> {
    switch (provider) {
      case 'icloud':
        return iCloudConnector.backup();
      case 'gdrive':
        return gDriveConnector.backup();
      case 'dropbox':
        return dropboxConnector.backup();
      case 'local':
        return localExportConnector.exportBackup();
      default:
        throw new Error(`Unknown provider: ${provider}`);
    }
  }

  // ── Backup to all connected providers ──

  async backupToAll(): Promise<BackupInfo[]> {
    const results: BackupInfo[] = [];
    const connections = await this.getConnectionState();

    if (connections.icloud.connected) {
      try {
        results.push(await iCloudConnector.backup());
      } catch (err) {
        console.warn('iCloud backup failed:', err);
      }
    }

    if (connections.gdrive.connected) {
      try {
        results.push(await gDriveConnector.backup());
      } catch (err) {
        console.warn('Google Drive backup failed:', err);
      }
    }

    if (connections.dropbox.connected) {
      try {
        results.push(await dropboxConnector.backup());
      } catch (err) {
        console.warn('Dropbox backup failed:', err);
      }
    }

    return results;
  }

  // ── List backups from all providers ──

  async listAllBackups(): Promise<BackupInfo[]> {
    const [icloudBackups, gdriveBackups, dropboxBackups] = await Promise.all([
      iCloudConnector.listBackups().catch(() => [] as BackupInfo[]),
      gDriveConnector.listBackups().catch(() => [] as BackupInfo[]),
      dropboxConnector.listBackups().catch(() => [] as BackupInfo[]),
    ]);

    return [...icloudBackups, ...gdriveBackups, ...dropboxBackups].sort(
      (a, b) =>
        new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );
  }

  // ── Connection management ──

  async connectProvider(provider: CloudProvider): Promise<boolean> {
    switch (provider) {
      case 'gdrive':
        return gDriveConnector.connect();
      case 'dropbox':
        return dropboxConnector.connect();
      case 'icloud':
        return true; // iCloud is always available on iOS
      default:
        return false;
    }
  }

  async disconnectProvider(provider: CloudProvider): Promise<void> {
    switch (provider) {
      case 'gdrive':
        return gDriveConnector.disconnect();
      case 'dropbox':
        return dropboxConnector.disconnect();
      default:
        break;
    }
  }

  // ── State & preferences ──

  async getConnectionState(): Promise<CloudConnectionState> {
    return getConnectionState();
  }

  async getLastBackupTime(): Promise<string | null> {
    return getLastBackupTime();
  }

  getBackupHealthStatus(lastBackupTime: string | null): BackupHealthStatus {
    return getBackupHealthStatus(lastBackupTime);
  }

  async isAutoBackupEnabled(): Promise<boolean> {
    return isAutoBackupEnabled();
  }

  async setAutoBackupEnabled(enabled: boolean): Promise<void> {
    return setAutoBackupEnabled(enabled);
  }

  // ── Auto-backup trigger ──

  async triggerAutoBackup(): Promise<void> {
    return triggerAutoBackup();
  }

  // ── Helpers ──

  formatRelativeTime(isoString: string): string {
    return formatRelativeTime(isoString);
  }

  /**
   * Check whether OAuth credentials are configured (not placeholders) for a provider.
   * Use this to hide/disable connect buttons in the UI when credentials aren't set up.
   */
  isOAuthConfigured(provider: 'gdrive' | 'dropbox'): boolean {
    return isOAuthConfigured(provider);
  }
}

export const cloudBackup = new CloudBackupService();
export default cloudBackup;
