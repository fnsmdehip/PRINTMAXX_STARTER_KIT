/**
 * API Security Utility
 *
 * Handles certificate pinning, request signing, token refresh, and rate limiting.
 *
 * Dependencies:
 * - axios
 * - react-native-ssl-pinning (for cert pinning)
 * - crypto-js (for request signing)
 */

import axios, {
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from 'axios';
import { fetch as sslFetch } from 'react-native-ssl-pinning';
import CryptoJS from 'crypto-js';
import { TokenManager } from './secure_storage';

// Configuration types
interface ApiConfig {
  baseURL: string;
  timeout?: number;
  // Certificate pins (SHA256 hashes)
  certificatePins?: string[];
  // Request signing secret (stored securely, injected at build)
  signingSecret?: string;
  // Retry configuration
  maxRetries?: number;
  retryDelay?: number;
}

interface RateLimitState {
  remaining: number;
  resetTime: number;
  isLimited: boolean;
}

// Token refresh callback type
type RefreshTokenCallback = (
  refreshToken: string
) => Promise<{ accessToken: string; refreshToken: string; expiresAt: number }>;

/**
 * Secure API client with certificate pinning
 *
 * Usage:
 * ```
 * const api = new SecureApiClient({
 *   baseURL: 'https://api.yourapp.com',
 *   certificatePins: ['sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='],
 *   signingSecret: Config.API_SIGNING_SECRET,
 * });
 *
 * api.setRefreshCallback(async (refreshToken) => {
 *   const response = await api.post('/auth/refresh', { refreshToken });
 *   return response.data;
 * });
 *
 * const data = await api.get('/users/me');
 * ```
 */
export class SecureApiClient {
  private config: ApiConfig;
  private axiosInstance: AxiosInstance;
  private rateLimitState: RateLimitState;
  private refreshCallback: RefreshTokenCallback | null = null;
  private isRefreshing = false;
  private refreshSubscribers: ((token: string) => void)[] = [];

  constructor(config: ApiConfig) {
    this.config = {
      timeout: 30000,
      maxRetries: 3,
      retryDelay: 1000,
      ...config,
    };

    this.rateLimitState = {
      remaining: Infinity,
      resetTime: 0,
      isLimited: false,
    };

    this.axiosInstance = axios.create({
      baseURL: this.config.baseURL,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  /**
   * Set the token refresh callback
   */
  setRefreshCallback(callback: RefreshTokenCallback): void {
    this.refreshCallback = callback;
  }

  /**
   * Setup request and response interceptors
   */
  private setupInterceptors(): void {
    // Request interceptor
    this.axiosInstance.interceptors.request.use(
      async (config: InternalAxiosRequestConfig) => {
        // Check rate limit before making request
        if (this.isRateLimited()) {
          const waitTime = this.getWaitTime();
          throw new RateLimitError(
            `Rate limited. Retry after ${waitTime}ms`,
            waitTime
          );
        }

        // Add auth token
        const token = await TokenManager.getAccessToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }

        // Add request signature
        if (this.config.signingSecret) {
          const signature = this.signRequest(config);
          config.headers['X-Request-Signature'] = signature;
          config.headers['X-Request-Timestamp'] = Date.now().toString();
        }

        // Add request ID for tracing
        config.headers['X-Request-ID'] = this.generateRequestId();

        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.axiosInstance.interceptors.response.use(
      (response: AxiosResponse) => {
        // Update rate limit state from headers
        this.updateRateLimitState(response);
        return response;
      },
      async (error) => {
        const originalRequest = error.config;

        // Handle 401 - Token expired
        if (error.response?.status === 401 && !originalRequest._retry) {
          if (this.isRefreshing) {
            // Wait for refresh to complete
            return new Promise((resolve) => {
              this.refreshSubscribers.push((token: string) => {
                originalRequest.headers.Authorization = `Bearer ${token}`;
                resolve(this.axiosInstance(originalRequest));
              });
            });
          }

          originalRequest._retry = true;
          this.isRefreshing = true;

          try {
            const newToken = await this.refreshTokens();
            this.notifyRefreshSubscribers(newToken);
            originalRequest.headers.Authorization = `Bearer ${newToken}`;
            return this.axiosInstance(originalRequest);
          } catch (refreshError) {
            // Refresh failed - clear tokens and redirect to login
            await TokenManager.clear();
            throw new AuthenticationError('Session expired. Please login again.');
          } finally {
            this.isRefreshing = false;
          }
        }

        // Handle 429 - Rate limited
        if (error.response?.status === 429) {
          this.handleRateLimitResponse(error.response);
          const retryAfter = this.getRetryAfter(error.response);
          throw new RateLimitError(
            'Rate limit exceeded',
            retryAfter
          );
        }

        return Promise.reject(error);
      }
    );
  }

  /**
   * Refresh authentication tokens
   */
  private async refreshTokens(): Promise<string> {
    if (!this.refreshCallback) {
      throw new Error('No refresh callback configured');
    }

    const refreshToken = await TokenManager.getRefreshToken();
    if (!refreshToken) {
      throw new AuthenticationError('No refresh token available');
    }

    const tokens = await this.refreshCallback(refreshToken);
    await TokenManager.setTokens(tokens);

    return tokens.accessToken;
  }

  /**
   * Notify all subscribers that token has been refreshed
   */
  private notifyRefreshSubscribers(token: string): void {
    this.refreshSubscribers.forEach((callback) => callback(token));
    this.refreshSubscribers = [];
  }

  /**
   * Sign a request for integrity verification
   */
  private signRequest(config: InternalAxiosRequestConfig): string {
    const timestamp = Date.now();
    const method = config.method?.toUpperCase() || 'GET';
    const path = config.url || '';
    const body = config.data ? JSON.stringify(config.data) : '';

    const payload = `${timestamp}.${method}.${path}.${body}`;
    const signature = CryptoJS.HmacSHA256(
      payload,
      this.config.signingSecret!
    ).toString(CryptoJS.enc.Hex);

    return signature;
  }

  /**
   * Generate unique request ID
   */
  private generateRequestId(): string {
    return `${Date.now()}-${Math.random().toString(36).substring(2, 15)}`;
  }

  /**
   * Update rate limit state from response headers
   */
  private updateRateLimitState(response: AxiosResponse): void {
    const remaining = response.headers['x-ratelimit-remaining'];
    const reset = response.headers['x-ratelimit-reset'];

    if (remaining !== undefined) {
      this.rateLimitState.remaining = parseInt(remaining, 10);
    }

    if (reset !== undefined) {
      this.rateLimitState.resetTime = parseInt(reset, 10) * 1000;
    }

    this.rateLimitState.isLimited = this.rateLimitState.remaining <= 0;
  }

  /**
   * Handle rate limit response
   */
  private handleRateLimitResponse(response: AxiosResponse): void {
    const retryAfter = this.getRetryAfter(response);
    this.rateLimitState.isLimited = true;
    this.rateLimitState.resetTime = Date.now() + retryAfter;
    this.rateLimitState.remaining = 0;
  }

  /**
   * Get retry-after time from response
   */
  private getRetryAfter(response: AxiosResponse): number {
    const retryAfter = response.headers['retry-after'];
    if (retryAfter) {
      return parseInt(retryAfter, 10) * 1000;
    }
    return this.config.retryDelay || 1000;
  }

  /**
   * Check if currently rate limited
   */
  private isRateLimited(): boolean {
    if (!this.rateLimitState.isLimited) {
      return false;
    }

    // Check if reset time has passed
    if (Date.now() >= this.rateLimitState.resetTime) {
      this.rateLimitState.isLimited = false;
      this.rateLimitState.remaining = Infinity;
      return false;
    }

    return true;
  }

  /**
   * Get wait time until rate limit resets
   */
  private getWaitTime(): number {
    return Math.max(0, this.rateLimitState.resetTime - Date.now());
  }

  /**
   * Make request with certificate pinning
   */
  private async pinnedRequest<T>(
    method: string,
    path: string,
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<T> {
    if (!this.config.certificatePins?.length) {
      // No pins configured, use regular request
      const response = await this.axiosInstance.request({
        method,
        url: path,
        data,
        ...config,
      });
      return response.data;
    }

    // Use SSL pinning
    const token = await TokenManager.getAccessToken();
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(config?.headers as Record<string, string>),
    };

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    if (this.config.signingSecret) {
      const timestamp = Date.now();
      const payload = `${timestamp}.${method.toUpperCase()}.${path}.${
        data ? JSON.stringify(data) : ''
      }`;
      headers['X-Request-Signature'] = CryptoJS.HmacSHA256(
        payload,
        this.config.signingSecret
      ).toString(CryptoJS.enc.Hex);
      headers['X-Request-Timestamp'] = timestamp.toString();
    }

    const response = await sslFetch(`${this.config.baseURL}${path}`, {
      method: method as any,
      headers,
      body: data ? JSON.stringify(data) : undefined,
      sslPinning: {
        certs: this.config.certificatePins,
      },
      timeoutInterval: this.config.timeout,
    });

    return response.json();
  }

  /**
   * GET request
   */
  async get<T = any>(path: string, config?: AxiosRequestConfig): Promise<T> {
    return this.pinnedRequest<T>('GET', path, undefined, config);
  }

  /**
   * POST request
   */
  async post<T = any>(
    path: string,
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<T> {
    return this.pinnedRequest<T>('POST', path, data, config);
  }

  /**
   * PUT request
   */
  async put<T = any>(
    path: string,
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<T> {
    return this.pinnedRequest<T>('PUT', path, data, config);
  }

  /**
   * PATCH request
   */
  async patch<T = any>(
    path: string,
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<T> {
    return this.pinnedRequest<T>('PATCH', path, data, config);
  }

  /**
   * DELETE request
   */
  async delete<T = any>(path: string, config?: AxiosRequestConfig): Promise<T> {
    return this.pinnedRequest<T>('DELETE', path, undefined, config);
  }

  /**
   * Get current rate limit state
   */
  getRateLimitState(): RateLimitState {
    return { ...this.rateLimitState };
  }
}

/**
 * Certificate pinning helper
 *
 * Extract certificate pins from your API server:
 * ```bash
 * openssl s_client -servername api.yourapp.com -connect api.yourapp.com:443 < /dev/null 2>/dev/null \
 *   | openssl x509 -pubkey -noout \
 *   | openssl pkey -pubin -outform DER \
 *   | openssl dgst -sha256 -binary \
 *   | openssl enc -base64
 * ```
 */
export const CertificatePinning = {
  /**
   * Validate a certificate pin format
   */
  isValidPin(pin: string): boolean {
    // SHA256 base64 encoded = 44 characters
    const sha256Base64Regex = /^sha256\/[A-Za-z0-9+/]{43}=$/;
    return sha256Base64Regex.test(pin);
  },

  /**
   * Get pins for common services (for reference)
   */
  getCommonPins(): Record<string, string[]> {
    return {
      // These are examples - always extract your own pins
      'api.stripe.com': [
        'sha256/placeholder_stripe_pin_1',
        'sha256/placeholder_stripe_pin_2',
      ],
      'api.twilio.com': [
        'sha256/placeholder_twilio_pin_1',
      ],
    };
  },
};

/**
 * Request retry with exponential backoff
 */
export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries?: number;
    baseDelay?: number;
    maxDelay?: number;
    shouldRetry?: (error: any) => boolean;
  } = {}
): Promise<T> {
  const {
    maxRetries = 3,
    baseDelay = 1000,
    maxDelay = 30000,
    shouldRetry = (error) => {
      // Retry on network errors and 5xx responses
      if (!error.response) return true;
      return error.response.status >= 500;
    },
  } = options;

  let lastError: any;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      if (attempt === maxRetries || !shouldRetry(error)) {
        throw error;
      }

      // Calculate delay with exponential backoff and jitter
      const delay = Math.min(
        baseDelay * Math.pow(2, attempt) + Math.random() * 1000,
        maxDelay
      );

      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw lastError;
}

/**
 * Rate limit handler for client-side throttling
 */
export class RateLimiter {
  private tokens: number;
  private maxTokens: number;
  private refillRate: number;
  private lastRefill: number;

  /**
   * Create a rate limiter
   * @param maxTokens Maximum requests allowed
   * @param refillRate Tokens added per second
   */
  constructor(maxTokens: number, refillRate: number) {
    this.maxTokens = maxTokens;
    this.tokens = maxTokens;
    this.refillRate = refillRate;
    this.lastRefill = Date.now();
  }

  /**
   * Refill tokens based on elapsed time
   */
  private refill(): void {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    const tokensToAdd = elapsed * this.refillRate;

    this.tokens = Math.min(this.maxTokens, this.tokens + tokensToAdd);
    this.lastRefill = now;
  }

  /**
   * Check if request is allowed
   */
  canMakeRequest(): boolean {
    this.refill();
    return this.tokens >= 1;
  }

  /**
   * Consume a token (make request)
   */
  consumeToken(): boolean {
    this.refill();

    if (this.tokens >= 1) {
      this.tokens -= 1;
      return true;
    }

    return false;
  }

  /**
   * Get time until next token available
   */
  getWaitTime(): number {
    this.refill();

    if (this.tokens >= 1) {
      return 0;
    }

    return ((1 - this.tokens) / this.refillRate) * 1000;
  }

  /**
   * Wait until request is allowed
   */
  async waitForToken(): Promise<void> {
    const waitTime = this.getWaitTime();
    if (waitTime > 0) {
      await new Promise((resolve) => setTimeout(resolve, waitTime));
    }
    this.consumeToken();
  }
}

// Custom error classes

export class RateLimitError extends Error {
  retryAfter: number;

  constructor(message: string, retryAfter: number) {
    super(message);
    this.name = 'RateLimitError';
    this.retryAfter = retryAfter;
  }
}

export class AuthenticationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'AuthenticationError';
  }
}

export class CertificatePinningError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'CertificatePinningError';
  }
}

// Factory function for easy setup
export function createSecureApi(config: ApiConfig): SecureApiClient {
  return new SecureApiClient(config);
}

export default SecureApiClient;
