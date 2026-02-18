/**
 * Secure Storage Utility
 *
 * Cross-platform secure storage for React Native apps.
 * Uses Keychain on iOS and Keystore on Android.
 *
 * Dependencies:
 * - react-native-keychain
 * - @react-native-async-storage/async-storage (for non-sensitive data)
 * - react-native-encrypted-storage (alternative)
 */

import * as Keychain from 'react-native-keychain';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform } from 'react-native';

// Storage accessibility levels
export enum AccessibleOption {
  // Data accessible when device unlocked
  WHEN_UNLOCKED = 'AccessibleWhenUnlocked',
  // Data accessible when device unlocked, only on this device
  WHEN_UNLOCKED_THIS_DEVICE_ONLY = 'AccessibleWhenUnlockedThisDeviceOnly',
  // Data accessible after first unlock until reboot
  AFTER_FIRST_UNLOCK = 'AccessibleAfterFirstUnlock',
  // Most restrictive - only when device unlocked, this device only
  WHEN_PASSCODE_SET_THIS_DEVICE_ONLY = 'AccessibleWhenPasscodeSetThisDeviceOnly',
}

// Biometric authentication type
export enum BiometricType {
  FACE_ID = 'FaceID',
  TOUCH_ID = 'TouchID',
  FINGERPRINT = 'Fingerprint',
  IRIS = 'Iris',
  NONE = 'None',
}

// Storage options
interface StorageOptions {
  // Require biometric authentication to access
  biometric?: boolean;
  // Biometric prompt message
  biometricPrompt?: string;
  // Accessibility level (iOS)
  accessible?: AccessibleOption;
  // Service name for Keychain (groups related items)
  service?: string;
}

// Storage result
interface StorageResult<T> {
  success: boolean;
  data?: T;
  error?: string;
}

/**
 * Check available biometric authentication
 */
export async function getBiometricType(): Promise<BiometricType> {
  try {
    const biometryType = await Keychain.getSupportedBiometryType();

    if (!biometryType) {
      return BiometricType.NONE;
    }

    switch (biometryType) {
      case Keychain.BIOMETRY_TYPE.FACE_ID:
        return BiometricType.FACE_ID;
      case Keychain.BIOMETRY_TYPE.TOUCH_ID:
        return BiometricType.TOUCH_ID;
      case Keychain.BIOMETRY_TYPE.FINGERPRINT:
        return BiometricType.FINGERPRINT;
      case Keychain.BIOMETRY_TYPE.IRIS:
        return BiometricType.IRIS;
      default:
        return BiometricType.NONE;
    }
  } catch {
    return BiometricType.NONE;
  }
}

/**
 * Check if biometric authentication is available
 */
export async function isBiometricAvailable(): Promise<boolean> {
  const type = await getBiometricType();
  return type !== BiometricType.NONE;
}

/**
 * Secure Storage class
 *
 * Usage:
 * ```
 * // Store token
 * await SecureStorage.setItem('auth_token', token);
 *
 * // Retrieve token
 * const token = await SecureStorage.getItem('auth_token');
 *
 * // Store with biometric
 * await SecureStorage.setItem('sensitive_data', data, { biometric: true });
 *
 * // Retrieve with biometric
 * const data = await SecureStorage.getItem('sensitive_data', {
 *   biometric: true,
 *   biometricPrompt: 'Authenticate to access your data'
 * });
 * ```
 */
export const SecureStorage = {
  /**
   * Store a value securely
   */
  async setItem(
    key: string,
    value: string,
    options: StorageOptions = {}
  ): Promise<StorageResult<void>> {
    try {
      const {
        biometric = false,
        accessible = AccessibleOption.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
        service = 'app_secure_storage',
      } = options;

      const keychainOptions: Keychain.Options = {
        service: `${service}_${key}`,
        accessible: mapAccessibleOption(accessible),
      };

      if (biometric) {
        keychainOptions.accessControl =
          Keychain.ACCESS_CONTROL.BIOMETRY_CURRENT_SET;
      }

      await Keychain.setGenericPassword(key, value, keychainOptions);

      return { success: true };
    } catch (error) {
      console.error('SecureStorage.setItem error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  },

  /**
   * Retrieve a value from secure storage
   */
  async getItem(
    key: string,
    options: StorageOptions = {}
  ): Promise<StorageResult<string>> {
    try {
      const {
        biometric = false,
        biometricPrompt = 'Authenticate to access secure data',
        service = 'app_secure_storage',
      } = options;

      const keychainOptions: Keychain.Options = {
        service: `${service}_${key}`,
      };

      if (biometric) {
        keychainOptions.authenticationPrompt = {
          title: biometricPrompt,
        };
      }

      const credentials = await Keychain.getGenericPassword(keychainOptions);

      if (!credentials) {
        return { success: true, data: undefined };
      }

      return { success: true, data: credentials.password };
    } catch (error) {
      console.error('SecureStorage.getItem error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  },

  /**
   * Remove a value from secure storage
   */
  async removeItem(
    key: string,
    options: StorageOptions = {}
  ): Promise<StorageResult<void>> {
    try {
      const { service = 'app_secure_storage' } = options;

      await Keychain.resetGenericPassword({
        service: `${service}_${key}`,
      });

      return { success: true };
    } catch (error) {
      console.error('SecureStorage.removeItem error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  },

  /**
   * Clear all secure storage items
   * Note: This clears items with the default service only
   */
  async clear(service = 'app_secure_storage'): Promise<StorageResult<void>> {
    try {
      // react-native-keychain doesn't have a clearAll method
      // You need to track keys separately or reset individual services
      await Keychain.resetGenericPassword({ service });
      return { success: true };
    } catch (error) {
      console.error('SecureStorage.clear error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  },

  /**
   * Store a JSON object securely
   */
  async setObject<T extends object>(
    key: string,
    value: T,
    options: StorageOptions = {}
  ): Promise<StorageResult<void>> {
    try {
      const jsonString = JSON.stringify(value);
      return this.setItem(key, jsonString, options);
    } catch (error) {
      return {
        success: false,
        error: 'Failed to serialize object',
      };
    }
  },

  /**
   * Retrieve a JSON object from secure storage
   */
  async getObject<T>(
    key: string,
    options: StorageOptions = {}
  ): Promise<StorageResult<T>> {
    try {
      const result = await this.getItem(key, options);

      if (!result.success) {
        return { success: false, error: result.error };
      }

      if (!result.data) {
        return { success: true, data: undefined };
      }

      const parsed = JSON.parse(result.data) as T;
      return { success: true, data: parsed };
    } catch (error) {
      return {
        success: false,
        error: 'Failed to parse stored object',
      };
    }
  },
};

/**
 * Encrypted AsyncStorage wrapper
 *
 * For data that needs to be encrypted but doesn't require Keychain-level security.
 * Uses a key stored in Keychain to encrypt AsyncStorage data.
 *
 * Usage:
 * ```
 * await EncryptedStorage.initialize();
 * await EncryptedStorage.setItem('preferences', JSON.stringify(prefs));
 * const prefs = await EncryptedStorage.getItem('preferences');
 * ```
 */
export const EncryptedStorage = {
  encryptionKey: null as string | null,

  /**
   * Initialize encryption key (call once at app startup)
   */
  async initialize(): Promise<void> {
    const result = await SecureStorage.getItem('_encryption_key');

    if (result.success && result.data) {
      this.encryptionKey = result.data;
    } else {
      // Generate new encryption key
      const newKey = generateRandomKey(32);
      await SecureStorage.setItem('_encryption_key', newKey);
      this.encryptionKey = newKey;
    }
  },

  /**
   * Store encrypted data
   */
  async setItem(key: string, value: string): Promise<void> {
    if (!this.encryptionKey) {
      throw new Error('EncryptedStorage not initialized');
    }

    const encrypted = simpleEncrypt(value, this.encryptionKey);
    await AsyncStorage.setItem(`encrypted_${key}`, encrypted);
  },

  /**
   * Retrieve and decrypt data
   */
  async getItem(key: string): Promise<string | null> {
    if (!this.encryptionKey) {
      throw new Error('EncryptedStorage not initialized');
    }

    const encrypted = await AsyncStorage.getItem(`encrypted_${key}`);
    if (!encrypted) return null;

    return simpleDecrypt(encrypted, this.encryptionKey);
  },

  /**
   * Remove encrypted data
   */
  async removeItem(key: string): Promise<void> {
    await AsyncStorage.removeItem(`encrypted_${key}`);
  },

  /**
   * Clear all encrypted storage
   */
  async clear(): Promise<void> {
    const keys = await AsyncStorage.getAllKeys();
    const encryptedKeys = keys.filter((k) => k.startsWith('encrypted_'));
    await AsyncStorage.multiRemove(encryptedKeys);
  },
};

/**
 * Biometric authentication helper
 *
 * Usage:
 * ```
 * const canUseBiometric = await BiometricAuth.isAvailable();
 *
 * if (canUseBiometric) {
 *   const result = await BiometricAuth.authenticate('Confirm payment');
 *   if (result.success) {
 *     // Proceed with sensitive operation
 *   }
 * }
 * ```
 */
export const BiometricAuth = {
  /**
   * Check if biometric authentication is available
   */
  async isAvailable(): Promise<boolean> {
    return isBiometricAvailable();
  },

  /**
   * Get available biometric type
   */
  async getType(): Promise<BiometricType> {
    return getBiometricType();
  },

  /**
   * Authenticate user with biometrics
   */
  async authenticate(
    promptMessage = 'Authenticate to continue'
  ): Promise<StorageResult<void>> {
    try {
      // We use a dummy storage operation to trigger biometric auth
      // This is a workaround since react-native-keychain doesn't have standalone auth
      const testKey = '_biometric_test';
      const testValue = Date.now().toString();

      // Store with biometric requirement
      await SecureStorage.setItem(testKey, testValue, { biometric: true });

      // Retrieve (this triggers biometric prompt)
      const result = await SecureStorage.getItem(testKey, {
        biometric: true,
        biometricPrompt: promptMessage,
      });

      // Clean up
      await SecureStorage.removeItem(testKey);

      if (result.success) {
        return { success: true };
      }

      return { success: false, error: 'Authentication failed' };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Authentication failed',
      };
    }
  },
};

/**
 * Token manager for auth flows
 *
 * Usage:
 * ```
 * // Store tokens after login
 * await TokenManager.setTokens({
 *   accessToken: 'xxx',
 *   refreshToken: 'yyy',
 *   expiresAt: Date.now() + 3600000
 * });
 *
 * // Get access token (auto-refreshes if expired)
 * const token = await TokenManager.getAccessToken();
 *
 * // Clear on logout
 * await TokenManager.clear();
 * ```
 */
interface Tokens {
  accessToken: string;
  refreshToken: string;
  expiresAt: number;
}

export const TokenManager = {
  /**
   * Store authentication tokens
   */
  async setTokens(tokens: Tokens): Promise<StorageResult<void>> {
    const result = await SecureStorage.setObject('auth_tokens', tokens, {
      accessible: AccessibleOption.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
    });

    return result;
  },

  /**
   * Get stored tokens
   */
  async getTokens(): Promise<Tokens | null> {
    const result = await SecureStorage.getObject<Tokens>('auth_tokens');

    if (result.success && result.data) {
      return result.data;
    }

    return null;
  },

  /**
   * Get access token (checks expiry)
   */
  async getAccessToken(): Promise<string | null> {
    const tokens = await this.getTokens();

    if (!tokens) {
      return null;
    }

    // Check if token is expired (with 60 second buffer)
    const isExpired = tokens.expiresAt < Date.now() + 60000;

    if (isExpired) {
      // Token expired - caller should refresh
      return null;
    }

    return tokens.accessToken;
  },

  /**
   * Get refresh token
   */
  async getRefreshToken(): Promise<string | null> {
    const tokens = await this.getTokens();
    return tokens?.refreshToken ?? null;
  },

  /**
   * Check if tokens exist and are valid
   */
  async isAuthenticated(): Promise<boolean> {
    const token = await this.getAccessToken();
    return token !== null;
  },

  /**
   * Clear all tokens (logout)
   */
  async clear(): Promise<void> {
    await SecureStorage.removeItem('auth_tokens');
  },
};

// Helper functions

function mapAccessibleOption(
  option: AccessibleOption
): Keychain.ACCESSIBLE | undefined {
  switch (option) {
    case AccessibleOption.WHEN_UNLOCKED:
      return Keychain.ACCESSIBLE.WHEN_UNLOCKED;
    case AccessibleOption.WHEN_UNLOCKED_THIS_DEVICE_ONLY:
      return Keychain.ACCESSIBLE.WHEN_UNLOCKED_THIS_DEVICE_ONLY;
    case AccessibleOption.AFTER_FIRST_UNLOCK:
      return Keychain.ACCESSIBLE.AFTER_FIRST_UNLOCK;
    case AccessibleOption.WHEN_PASSCODE_SET_THIS_DEVICE_ONLY:
      return Keychain.ACCESSIBLE.WHEN_PASSCODE_SET_THIS_DEVICE_ONLY;
    default:
      return undefined;
  }
}

/**
 * Generate a random key for encryption
 * Note: In production, use a proper crypto library
 */
function generateRandomKey(length: number): string {
  const chars =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  const randomValues = new Uint32Array(length);
  crypto.getRandomValues(randomValues);

  for (let i = 0; i < length; i++) {
    result += chars[randomValues[i] % chars.length];
  }

  return result;
}

/**
 * Simple XOR encryption
 * Note: For production, use a proper encryption library like react-native-aes-gcm-crypto
 */
function simpleEncrypt(text: string, key: string): string {
  let result = '';
  for (let i = 0; i < text.length; i++) {
    result += String.fromCharCode(
      text.charCodeAt(i) ^ key.charCodeAt(i % key.length)
    );
  }
  return Buffer.from(result).toString('base64');
}

function simpleDecrypt(encrypted: string, key: string): string {
  const text = Buffer.from(encrypted, 'base64').toString();
  let result = '';
  for (let i = 0; i < text.length; i++) {
    result += String.fromCharCode(
      text.charCodeAt(i) ^ key.charCodeAt(i % key.length)
    );
  }
  return result;
}

export default SecureStorage;
