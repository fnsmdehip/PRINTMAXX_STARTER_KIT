/**
 * StorageService - Unified AsyncStorage wrapper
 *
 * Features:
 * - Type-safe get/set operations
 * - Migration support for schema changes
 * - Optional encryption for sensitive data
 * - Batch operations for performance
 * - Error handling with fallbacks
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Crypto from 'expo-crypto';

// Types
export interface StorageOptions {
  encrypt?: boolean;
  ttl?: number; // Time-to-live in milliseconds
}

export interface StorageItem<T> {
  value: T;
  timestamp: number;
  ttl?: number;
  version?: number;
  encrypted?: boolean;
}

export interface MigrationConfig {
  version: number;
  migrate: (oldData: unknown) => unknown;
}

export interface StorageError {
  code: 'READ_ERROR' | 'WRITE_ERROR' | 'DELETE_ERROR' | 'ENCRYPTION_ERROR' | 'MIGRATION_ERROR';
  message: string;
  originalError?: Error;
}

// Result type for operations
export type StorageResult<T> = { success: true; data: T } | { success: false; error: StorageError };

class StorageServiceClass {
  private encryptionKey: string | null = null;
  private currentVersion = 1;
  private migrations: Map<string, MigrationConfig[]> = new Map();

  /**
   * Initialize encryption key for sensitive data
   * Call this during app startup if using encryption
   */
  async initEncryption(key: string): Promise<void> {
    this.encryptionKey = key;
  }

  /**
   * Set the current storage schema version
   */
  setVersion(version: number): void {
    this.currentVersion = version;
  }

  /**
   * Register migrations for a specific key
   */
  registerMigrations(key: string, migrations: MigrationConfig[]): void {
    this.migrations.set(
      key,
      migrations.sort((a, b) => a.version - b.version)
    );
  }

  /**
   * Get a value from storage with type safety
   */
  async get<T>(key: string, options?: StorageOptions): Promise<StorageResult<T | null>> {
    try {
      const raw = await AsyncStorage.getItem(key);

      if (raw === null) {
        return { success: true, data: null };
      }

      let item: StorageItem<T>;
      try {
        item = JSON.parse(raw);
      } catch {
        // Legacy data without wrapper - wrap it
        return { success: true, data: raw as unknown as T };
      }

      // Check TTL
      if (item.ttl && Date.now() - item.timestamp > item.ttl) {
        await this.delete(key);
        return { success: true, data: null };
      }

      // Decrypt if needed
      let value = item.value;
      if (item.encrypted) {
        if (!this.encryptionKey) {
          return {
            success: false,
            error: {
              code: 'ENCRYPTION_ERROR',
              message: 'Encryption key not initialized',
            },
          };
        }
        const decrypted = await this.decrypt(value as unknown as string);
        value = JSON.parse(decrypted) as T;
      }

      // Run migrations if needed
      if (item.version && item.version < this.currentVersion) {
        const migratedValue = await this.runMigrations(key, value, item.version);
        // Save migrated value
        await this.set(key, migratedValue, options);
        return { success: true, data: migratedValue as T };
      }

      return { success: true, data: value };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'READ_ERROR',
          message: `Failed to read key: ${key}`,
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Set a value in storage with type safety
   */
  async set<T>(key: string, value: T, options?: StorageOptions): Promise<StorageResult<void>> {
    try {
      let storedValue: unknown = value;
      let encrypted = false;

      // Encrypt if requested
      if (options?.encrypt) {
        if (!this.encryptionKey) {
          return {
            success: false,
            error: {
              code: 'ENCRYPTION_ERROR',
              message: 'Encryption key not initialized',
            },
          };
        }
        storedValue = await this.encrypt(JSON.stringify(value));
        encrypted = true;
      }

      const item: StorageItem<unknown> = {
        value: storedValue,
        timestamp: Date.now(),
        ttl: options?.ttl,
        version: this.currentVersion,
        encrypted,
      };

      await AsyncStorage.setItem(key, JSON.stringify(item));
      return { success: true, data: undefined };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'WRITE_ERROR',
          message: `Failed to write key: ${key}`,
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Delete a value from storage
   */
  async delete(key: string): Promise<StorageResult<void>> {
    try {
      await AsyncStorage.removeItem(key);
      return { success: true, data: undefined };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'DELETE_ERROR',
          message: `Failed to delete key: ${key}`,
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Check if a key exists
   */
  async exists(key: string): Promise<boolean> {
    const result = await this.get(key);
    return result.success && result.data !== null;
  }

  /**
   * Get multiple values at once
   */
  async getMultiple<T>(keys: string[]): Promise<StorageResult<Map<string, T | null>>> {
    try {
      const pairs = await AsyncStorage.multiGet(keys);
      const result = new Map<string, T | null>();

      for (const [key, value] of pairs) {
        if (value === null) {
          result.set(key, null);
          continue;
        }

        try {
          const item: StorageItem<T> = JSON.parse(value);

          // Check TTL
          if (item.ttl && Date.now() - item.timestamp > item.ttl) {
            result.set(key, null);
            continue;
          }

          result.set(key, item.value);
        } catch {
          result.set(key, value as unknown as T);
        }
      }

      return { success: true, data: result };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'READ_ERROR',
          message: 'Failed to read multiple keys',
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Set multiple values at once
   */
  async setMultiple<T>(entries: Array<[string, T]>, options?: StorageOptions): Promise<StorageResult<void>> {
    try {
      const pairs: Array<[string, string]> = await Promise.all(
        entries.map(async ([key, value]) => {
          let storedValue: unknown = value;
          let encrypted = false;

          if (options?.encrypt && this.encryptionKey) {
            storedValue = await this.encrypt(JSON.stringify(value));
            encrypted = true;
          }

          const item: StorageItem<unknown> = {
            value: storedValue,
            timestamp: Date.now(),
            ttl: options?.ttl,
            version: this.currentVersion,
            encrypted,
          };

          return [key, JSON.stringify(item)] as [string, string];
        })
      );

      await AsyncStorage.multiSet(pairs);
      return { success: true, data: undefined };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'WRITE_ERROR',
          message: 'Failed to write multiple keys',
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Delete multiple values at once
   */
  async deleteMultiple(keys: string[]): Promise<StorageResult<void>> {
    try {
      await AsyncStorage.multiRemove(keys);
      return { success: true, data: undefined };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'DELETE_ERROR',
          message: 'Failed to delete multiple keys',
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Get all keys in storage
   */
  async getAllKeys(): Promise<StorageResult<string[]>> {
    try {
      const keys = await AsyncStorage.getAllKeys();
      return { success: true, data: keys as string[] };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'READ_ERROR',
          message: 'Failed to get all keys',
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Clear all storage
   */
  async clear(): Promise<StorageResult<void>> {
    try {
      await AsyncStorage.clear();
      return { success: true, data: undefined };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'DELETE_ERROR',
          message: 'Failed to clear storage',
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  /**
   * Get storage size info
   */
  async getStorageInfo(): Promise<StorageResult<{ keyCount: number; estimatedSize: number }>> {
    try {
      const keys = await AsyncStorage.getAllKeys();
      let totalSize = 0;

      for (const key of keys) {
        const value = await AsyncStorage.getItem(key);
        if (value) {
          totalSize += key.length + value.length;
        }
      }

      return {
        success: true,
        data: {
          keyCount: keys.length,
          estimatedSize: totalSize * 2, // Approximate bytes (UTF-16)
        },
      };
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'READ_ERROR',
          message: 'Failed to get storage info',
          originalError: error instanceof Error ? error : new Error(String(error)),
        },
      };
    }
  }

  // Private methods

  private async encrypt(data: string): Promise<string> {
    if (!this.encryptionKey) {
      throw new Error('Encryption key not set');
    }

    // Simple XOR encryption for demo - use a proper library in production
    // Consider react-native-aes-crypto or expo-crypto for real encryption
    const keyHash = await Crypto.digestStringAsync(Crypto.CryptoDigestAlgorithm.SHA256, this.encryptionKey);

    const encoded = data
      .split('')
      .map((char, i) => {
        const keyChar = keyHash[i % keyHash.length];
        return String.fromCharCode(char.charCodeAt(0) ^ keyChar.charCodeAt(0));
      })
      .join('');

    return Buffer.from(encoded, 'binary').toString('base64');
  }

  private async decrypt(encryptedData: string): Promise<string> {
    if (!this.encryptionKey) {
      throw new Error('Encryption key not set');
    }

    const keyHash = await Crypto.digestStringAsync(Crypto.CryptoDigestAlgorithm.SHA256, this.encryptionKey);

    const decoded = Buffer.from(encryptedData, 'base64').toString('binary');

    return decoded
      .split('')
      .map((char, i) => {
        const keyChar = keyHash[i % keyHash.length];
        return String.fromCharCode(char.charCodeAt(0) ^ keyChar.charCodeAt(0));
      })
      .join('');
  }

  private async runMigrations(key: string, data: unknown, fromVersion: number): Promise<unknown> {
    const migrations = this.migrations.get(key);
    if (!migrations) {
      return data;
    }

    let migratedData = data;
    for (const migration of migrations) {
      if (migration.version > fromVersion && migration.version <= this.currentVersion) {
        migratedData = migration.migrate(migratedData);
      }
    }

    return migratedData;
  }
}

// Export singleton instance
export const StorageService = new StorageServiceClass();

// Export class for testing
export { StorageServiceClass };
