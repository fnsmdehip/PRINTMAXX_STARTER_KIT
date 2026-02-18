/**
 * tokenManager.ts - Token storage and refresh management
 *
 * Handles secure token storage, automatic refresh, and expiration.
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import { AuthError, ErrorCodes } from '../types/ApiError';

// ============================================================================
// Types
// ============================================================================

export interface TokenPair {
  accessToken: string;
  refreshToken: string;
  expiresIn: number; // seconds until expiration
  tokenType: string;
}

export interface StoredTokens {
  accessToken: string;
  refreshToken: string;
  expiresAt: number; // timestamp
  tokenType: string;
}

export interface TokenManagerConfig {
  storage?: TokenStorage;
  onTokenRefresh?: (tokens: TokenPair) => Promise<TokenPair>;
  onTokenExpired?: () => void;
  refreshThreshold?: number; // seconds before expiry to trigger refresh
}

export interface TokenStorage {
  getItem(key: string): Promise<string | null>;
  setItem(key: string, value: string): Promise<void>;
  removeItem(key: string): Promise<void>;
}

// ============================================================================
// Constants
// ============================================================================

const STORAGE_KEYS = {
  ACCESS_TOKEN: '@auth/access_token',
  REFRESH_TOKEN: '@auth/refresh_token',
  EXPIRES_AT: '@auth/expires_at',
  TOKEN_TYPE: '@auth/token_type',
} as const;

const DEFAULT_REFRESH_THRESHOLD = 60; // Refresh 60 seconds before expiry

// ============================================================================
// TokenManager Class
// ============================================================================

class TokenManager {
  private storage: TokenStorage;
  private onTokenRefresh?: (tokens: TokenPair) => Promise<TokenPair>;
  private onTokenExpired?: () => void;
  private refreshThreshold: number;

  private cachedAccessToken: string | null = null;
  private cachedRefreshToken: string | null = null;
  private cachedExpiresAt: number | null = null;
  private refreshPromise: Promise<string | null> | null = null;
  private listeners: Set<(tokens: StoredTokens | null) => void> = new Set();

  constructor(config: TokenManagerConfig = {}) {
    this.storage = config.storage ?? AsyncStorage;
    this.onTokenRefresh = config.onTokenRefresh;
    this.onTokenExpired = config.onTokenExpired;
    this.refreshThreshold = config.refreshThreshold ?? DEFAULT_REFRESH_THRESHOLD;
  }

  // --------------------------------------------------------------------------
  // Configuration
  // --------------------------------------------------------------------------

  configure(config: Partial<TokenManagerConfig>): void {
    if (config.storage) this.storage = config.storage;
    if (config.onTokenRefresh) this.onTokenRefresh = config.onTokenRefresh;
    if (config.onTokenExpired) this.onTokenExpired = config.onTokenExpired;
    if (config.refreshThreshold) this.refreshThreshold = config.refreshThreshold;
  }

  // --------------------------------------------------------------------------
  // Token Storage
  // --------------------------------------------------------------------------

  /**
   * Store tokens from auth response
   */
  async setTokens(tokens: TokenPair): Promise<void> {
    const expiresAt = Date.now() + tokens.expiresIn * 1000;

    await Promise.all([
      this.storage.setItem(STORAGE_KEYS.ACCESS_TOKEN, tokens.accessToken),
      this.storage.setItem(STORAGE_KEYS.REFRESH_TOKEN, tokens.refreshToken),
      this.storage.setItem(STORAGE_KEYS.EXPIRES_AT, expiresAt.toString()),
      this.storage.setItem(STORAGE_KEYS.TOKEN_TYPE, tokens.tokenType),
    ]);

    // Update cache
    this.cachedAccessToken = tokens.accessToken;
    this.cachedRefreshToken = tokens.refreshToken;
    this.cachedExpiresAt = expiresAt;

    // Notify listeners
    this.notifyListeners({
      accessToken: tokens.accessToken,
      refreshToken: tokens.refreshToken,
      expiresAt,
      tokenType: tokens.tokenType,
    });
  }

  /**
   * Get stored tokens
   */
  async getTokens(): Promise<StoredTokens | null> {
    const [accessToken, refreshToken, expiresAtStr, tokenType] = await Promise.all([
      this.storage.getItem(STORAGE_KEYS.ACCESS_TOKEN),
      this.storage.getItem(STORAGE_KEYS.REFRESH_TOKEN),
      this.storage.getItem(STORAGE_KEYS.EXPIRES_AT),
      this.storage.getItem(STORAGE_KEYS.TOKEN_TYPE),
    ]);

    if (!accessToken || !refreshToken || !expiresAtStr) {
      return null;
    }

    const expiresAt = parseInt(expiresAtStr, 10);

    // Update cache
    this.cachedAccessToken = accessToken;
    this.cachedRefreshToken = refreshToken;
    this.cachedExpiresAt = expiresAt;

    return {
      accessToken,
      refreshToken,
      expiresAt,
      tokenType: tokenType ?? 'Bearer',
    };
  }

  /**
   * Clear all stored tokens
   */
  async clearTokens(): Promise<void> {
    await Promise.all([
      this.storage.removeItem(STORAGE_KEYS.ACCESS_TOKEN),
      this.storage.removeItem(STORAGE_KEYS.REFRESH_TOKEN),
      this.storage.removeItem(STORAGE_KEYS.EXPIRES_AT),
      this.storage.removeItem(STORAGE_KEYS.TOKEN_TYPE),
    ]);

    // Clear cache
    this.cachedAccessToken = null;
    this.cachedRefreshToken = null;
    this.cachedExpiresAt = null;

    // Notify listeners
    this.notifyListeners(null);
  }

  // --------------------------------------------------------------------------
  // Access Token
  // --------------------------------------------------------------------------

  /**
   * Get valid access token, refreshing if needed
   */
  async getAccessToken(): Promise<string | null> {
    // Check cache first
    if (this.cachedAccessToken && this.cachedExpiresAt) {
      if (!this.isTokenExpiringSoon()) {
        return this.cachedAccessToken;
      }
    }

    // Load from storage
    const tokens = await this.getTokens();
    if (!tokens) {
      return null;
    }

    // Check if expired or expiring soon
    if (this.isTokenExpired(tokens.expiresAt)) {
      // Token is fully expired, try to refresh
      return this.refreshAccessToken();
    }

    if (this.isExpiringSoon(tokens.expiresAt)) {
      // Token is expiring soon, refresh in background
      this.refreshAccessToken().catch(() => {
        // Silent fail for background refresh
      });
    }

    return tokens.accessToken;
  }

  /**
   * Get refresh token
   */
  async getRefreshToken(): Promise<string | null> {
    if (this.cachedRefreshToken) {
      return this.cachedRefreshToken;
    }

    const refreshToken = await this.storage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
    this.cachedRefreshToken = refreshToken;
    return refreshToken;
  }

  // --------------------------------------------------------------------------
  // Token Refresh
  // --------------------------------------------------------------------------

  /**
   * Refresh the access token
   */
  async refreshAccessToken(): Promise<string | null> {
    // Deduplicate concurrent refresh calls
    if (this.refreshPromise) {
      return this.refreshPromise;
    }

    this.refreshPromise = this.executeRefresh();

    try {
      return await this.refreshPromise;
    } finally {
      this.refreshPromise = null;
    }
  }

  private async executeRefresh(): Promise<string | null> {
    const refreshToken = await this.getRefreshToken();

    if (!refreshToken) {
      this.handleTokenExpired();
      return null;
    }

    if (!this.onTokenRefresh) {
      throw new AuthError(
        'Token refresh handler not configured',
        ErrorCodes.REFRESH_FAILED
      );
    }

    try {
      const currentTokens: TokenPair = {
        accessToken: this.cachedAccessToken ?? '',
        refreshToken,
        expiresIn: 0,
        tokenType: 'Bearer',
      };

      const newTokens = await this.onTokenRefresh(currentTokens);
      await this.setTokens(newTokens);
      return newTokens.accessToken;
    } catch (error) {
      // Clear tokens on refresh failure
      await this.clearTokens();
      this.handleTokenExpired();
      throw new AuthError(
        'Failed to refresh token',
        ErrorCodes.REFRESH_FAILED
      );
    }
  }

  // --------------------------------------------------------------------------
  // Expiration Checks
  // --------------------------------------------------------------------------

  /**
   * Check if token is expired
   */
  isTokenExpired(expiresAt?: number): boolean {
    const expiry = expiresAt ?? this.cachedExpiresAt;
    if (!expiry) return true;
    return Date.now() >= expiry;
  }

  /**
   * Check if token is expiring soon
   */
  isExpiringSoon(expiresAt?: number): boolean {
    const expiry = expiresAt ?? this.cachedExpiresAt;
    if (!expiry) return true;
    const threshold = this.refreshThreshold * 1000;
    return Date.now() >= expiry - threshold;
  }

  /**
   * Check if cached token is expiring soon
   */
  private isTokenExpiringSoon(): boolean {
    return this.isExpiringSoon(this.cachedExpiresAt ?? undefined);
  }

  /**
   * Get time until expiration in seconds
   */
  async getTimeUntilExpiry(): Promise<number> {
    if (this.cachedExpiresAt) {
      return Math.max(0, Math.floor((this.cachedExpiresAt - Date.now()) / 1000));
    }

    const tokens = await this.getTokens();
    if (!tokens) return 0;
    return Math.max(0, Math.floor((tokens.expiresAt - Date.now()) / 1000));
  }

  // --------------------------------------------------------------------------
  // Event Handling
  // --------------------------------------------------------------------------

  /**
   * Handle token expired event
   */
  private handleTokenExpired(): void {
    this.onTokenExpired?.();
  }

  /**
   * Subscribe to token changes
   */
  subscribe(listener: (tokens: StoredTokens | null) => void): () => void {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  /**
   * Notify all listeners of token changes
   */
  private notifyListeners(tokens: StoredTokens | null): void {
    this.listeners.forEach((listener) => listener(tokens));
  }

  // --------------------------------------------------------------------------
  // Auth State
  // --------------------------------------------------------------------------

  /**
   * Check if user is authenticated
   */
  async isAuthenticated(): Promise<boolean> {
    const tokens = await this.getTokens();
    if (!tokens) return false;

    // Consider authenticated if we have a refresh token
    // (access token can be refreshed)
    return !!tokens.refreshToken;
  }

  /**
   * Get current auth state for debugging
   */
  async getAuthState(): Promise<{
    isAuthenticated: boolean;
    hasAccessToken: boolean;
    hasRefreshToken: boolean;
    isExpired: boolean;
    expiresIn: number;
  }> {
    const tokens = await this.getTokens();
    const timeUntilExpiry = await this.getTimeUntilExpiry();

    return {
      isAuthenticated: !!tokens?.refreshToken,
      hasAccessToken: !!tokens?.accessToken,
      hasRefreshToken: !!tokens?.refreshToken,
      isExpired: tokens ? this.isTokenExpired(tokens.expiresAt) : true,
      expiresIn: timeUntilExpiry,
    };
  }
}

// ============================================================================
// Singleton Export
// ============================================================================

export const tokenManager = new TokenManager();

export default tokenManager;
