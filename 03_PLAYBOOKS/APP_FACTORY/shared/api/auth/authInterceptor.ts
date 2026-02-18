/**
 * authInterceptor.ts - Authentication interceptor for API client
 *
 * Handles automatic token attachment, refresh on 401, and auth error handling.
 */

import { ApiClient, RequestConfig } from '../ApiClient';
import { ApiError, AuthError, ErrorCodes } from '../types/ApiError';
import { tokenManager } from './tokenManager';
import { authApi } from './authApi';

// ============================================================================
// Types
// ============================================================================

export interface AuthInterceptorConfig {
  /** Callback when user needs to re-authenticate */
  onAuthRequired?: () => void;
  /** Callback when refresh fails */
  onRefreshFailed?: (error: ApiError) => void;
  /** Callback when session is expired */
  onSessionExpired?: () => void;
  /** Custom logic to determine if request needs auth */
  shouldAttachToken?: (config: RequestConfig) => boolean;
  /** Endpoints that should skip token refresh on 401 */
  noRefreshEndpoints?: string[];
}

// ============================================================================
// Auth Interceptor
// ============================================================================

let isRefreshing = false;
let refreshSubscribers: ((token: string | null) => void)[] = [];

/**
 * Subscribe to token refresh completion
 */
function subscribeTokenRefresh(callback: (token: string | null) => void): void {
  refreshSubscribers.push(callback);
}

/**
 * Notify all subscribers of new token
 */
function onRefreshComplete(token: string | null): void {
  refreshSubscribers.forEach((callback) => callback(token));
  refreshSubscribers = [];
}

/**
 * Set up authentication interceptors on API client
 */
export function setupAuthInterceptors(
  client: ApiClient,
  config: AuthInterceptorConfig = {}
): () => void {
  const {
    onAuthRequired,
    onRefreshFailed,
    onSessionExpired,
    shouldAttachToken,
    noRefreshEndpoints = ['/auth/login', '/auth/register', '/auth/refresh'],
  } = config;

  // Configure token manager with refresh handler
  tokenManager.configure({
    onTokenRefresh: async (tokens) => {
      const newTokens = await authApi.refreshToken(tokens.refreshToken);
      return newTokens;
    },
    onTokenExpired: () => {
      onSessionExpired?.();
    },
  });

  // --------------------------------------------------------------------------
  // Request Interceptor
  // --------------------------------------------------------------------------

  const removeRequestInterceptor = client.addRequestInterceptor(
    async (requestConfig: RequestConfig): Promise<RequestConfig> => {
      // Skip if explicitly marked
      if (requestConfig.skipAuth) {
        return requestConfig;
      }

      // Custom check if provided
      if (shouldAttachToken && !shouldAttachToken(requestConfig)) {
        return requestConfig;
      }

      // Get valid access token (may trigger refresh)
      const token = await tokenManager.getAccessToken();

      if (token) {
        return {
          ...requestConfig,
          headers: {
            ...requestConfig.headers,
            Authorization: `Bearer ${token}`,
          },
        };
      }

      return requestConfig;
    }
  );

  // --------------------------------------------------------------------------
  // Error Interceptor
  // --------------------------------------------------------------------------

  const removeErrorInterceptor = client.addErrorInterceptor(
    async (error: ApiError): Promise<ApiError> => {
      // Only handle 401 errors
      if (error.status !== 401) {
        return error;
      }

      // Don't retry on certain endpoints
      if (
        noRefreshEndpoints.some((endpoint) =>
          error.data && typeof error.data === 'object' && 'url' in error.data
            ? (error.data.url as string).includes(endpoint)
            : false
        )
      ) {
        return error;
      }

      // Check if we have a refresh token
      const refreshToken = await tokenManager.getRefreshToken();
      if (!refreshToken) {
        onAuthRequired?.();
        return error;
      }

      // Handle concurrent refresh
      if (isRefreshing) {
        // Wait for ongoing refresh
        return new Promise((resolve, reject) => {
          subscribeTokenRefresh((token) => {
            if (token) {
              // Retry with new token - error transformation handled upstream
              resolve(error);
            } else {
              reject(error);
            }
          });
        });
      }

      // Start refresh
      isRefreshing = true;

      try {
        const newTokens = await authApi.refreshToken(refreshToken);
        isRefreshing = false;
        onRefreshComplete(newTokens.accessToken);

        // Return the original error to signal retry needed
        // The calling code should retry the request
        return error;
      } catch (refreshError) {
        isRefreshing = false;
        onRefreshComplete(null);

        // Clear tokens on refresh failure
        await tokenManager.clearTokens();

        const authError =
          refreshError instanceof ApiError
            ? refreshError
            : new AuthError('Session expired', ErrorCodes.SESSION_EXPIRED);

        onRefreshFailed?.(authError);
        onSessionExpired?.();

        return authError;
      }
    }
  );

  // Return cleanup function
  return () => {
    removeRequestInterceptor();
    removeErrorInterceptor();
  };
}

// ============================================================================
// Request Retry Utility
// ============================================================================

/**
 * Retry a failed request with refreshed token
 */
export async function retryWithRefresh<T>(
  request: () => Promise<T>
): Promise<T> {
  try {
    return await request();
  } catch (error) {
    if (!(error instanceof ApiError) || error.status !== 401) {
      throw error;
    }

    // Try to refresh token
    const newToken = await tokenManager.refreshAccessToken();

    if (!newToken) {
      throw new AuthError('Authentication required', ErrorCodes.UNAUTHORIZED);
    }

    // Retry the request
    return request();
  }
}

// ============================================================================
// Auth State Utilities
// ============================================================================

/**
 * Get current authentication state
 */
export async function getAuthState(): Promise<{
  isAuthenticated: boolean;
  isExpired: boolean;
  user: null; // Would need to store user separately
}> {
  const authState = await tokenManager.getAuthState();

  return {
    isAuthenticated: authState.isAuthenticated,
    isExpired: authState.isExpired,
    user: null,
  };
}

/**
 * Check if user is authenticated
 */
export async function isAuthenticated(): Promise<boolean> {
  return tokenManager.isAuthenticated();
}

/**
 * Clear authentication state
 */
export async function clearAuth(): Promise<void> {
  await tokenManager.clearTokens();
}

export default setupAuthInterceptors;
