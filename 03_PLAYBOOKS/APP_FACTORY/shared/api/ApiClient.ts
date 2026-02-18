/**
 * ApiClient.ts - Base HTTP client with interceptors
 *
 * Core networking layer for all API calls.
 * Uses fetch with axios-like interface.
 */

import { ApiError, NetworkError, TimeoutError } from './types/ApiError';
import type { ApiResponse } from './types/ApiResponse';
import { tokenManager } from './auth/tokenManager';

// ============================================================================
// Types
// ============================================================================

export interface RequestConfig {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  headers?: Record<string, string>;
  body?: unknown;
  params?: Record<string, string | number | boolean | undefined>;
  timeout?: number;
  retry?: RetryConfig;
  cache?: RequestCache;
  signal?: AbortSignal;
  skipAuth?: boolean;
}

export interface RetryConfig {
  attempts: number;
  delay: number;
  backoff?: 'linear' | 'exponential';
  retryOn?: number[];
}

export interface ApiClientConfig {
  baseUrl: string;
  timeout?: number;
  defaultHeaders?: Record<string, string>;
  onRequest?: (config: RequestConfig) => RequestConfig | Promise<RequestConfig>;
  onResponse?: <T>(response: ApiResponse<T>) => ApiResponse<T> | Promise<ApiResponse<T>>;
  onError?: (error: ApiError) => ApiError | Promise<ApiError>;
}

type Interceptor<T> = (value: T) => T | Promise<T>;

interface Interceptors {
  request: Interceptor<RequestConfig>[];
  response: Interceptor<ApiResponse<unknown>>[];
  error: Interceptor<ApiError>[];
}

// ============================================================================
// Constants
// ============================================================================

const DEFAULT_TIMEOUT = 30000; // 30 seconds
const DEFAULT_RETRY: RetryConfig = {
  attempts: 3,
  delay: 1000,
  backoff: 'exponential',
  retryOn: [408, 429, 500, 502, 503, 504],
};

// ============================================================================
// ApiClient Class
// ============================================================================

export class ApiClient {
  private baseUrl: string;
  private timeout: number;
  private defaultHeaders: Record<string, string>;
  private interceptors: Interceptors = {
    request: [],
    response: [],
    error: [],
  };

  constructor(config: ApiClientConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, '');
    this.timeout = config.timeout ?? DEFAULT_TIMEOUT;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      ...config.defaultHeaders,
    };

    if (config.onRequest) {
      this.interceptors.request.push(config.onRequest);
    }
    if (config.onResponse) {
      this.interceptors.response.push(config.onResponse as Interceptor<ApiResponse<unknown>>);
    }
    if (config.onError) {
      this.interceptors.error.push(config.onError);
    }
  }

  // --------------------------------------------------------------------------
  // Interceptor Management
  // --------------------------------------------------------------------------

  addRequestInterceptor(interceptor: Interceptor<RequestConfig>): () => void {
    this.interceptors.request.push(interceptor);
    return () => {
      const index = this.interceptors.request.indexOf(interceptor);
      if (index > -1) this.interceptors.request.splice(index, 1);
    };
  }

  addResponseInterceptor(interceptor: Interceptor<ApiResponse<unknown>>): () => void {
    this.interceptors.response.push(interceptor);
    return () => {
      const index = this.interceptors.response.indexOf(interceptor);
      if (index > -1) this.interceptors.response.splice(index, 1);
    };
  }

  addErrorInterceptor(interceptor: Interceptor<ApiError>): () => void {
    this.interceptors.error.push(interceptor);
    return () => {
      const index = this.interceptors.error.indexOf(interceptor);
      if (index > -1) this.interceptors.error.splice(index, 1);
    };
  }

  // --------------------------------------------------------------------------
  // HTTP Methods
  // --------------------------------------------------------------------------

  async get<T>(endpoint: string, config?: Omit<RequestConfig, 'method' | 'body'>): Promise<T> {
    return this.request<T>(endpoint, { ...config, method: 'GET' });
  }

  async post<T>(endpoint: string, data?: unknown, config?: Omit<RequestConfig, 'method'>): Promise<T> {
    return this.request<T>(endpoint, { ...config, method: 'POST', body: data });
  }

  async put<T>(endpoint: string, data?: unknown, config?: Omit<RequestConfig, 'method'>): Promise<T> {
    return this.request<T>(endpoint, { ...config, method: 'PUT', body: data });
  }

  async patch<T>(endpoint: string, data?: unknown, config?: Omit<RequestConfig, 'method'>): Promise<T> {
    return this.request<T>(endpoint, { ...config, method: 'PATCH', body: data });
  }

  async delete<T>(endpoint: string, config?: Omit<RequestConfig, 'method'>): Promise<T> {
    return this.request<T>(endpoint, { ...config, method: 'DELETE' });
  }

  // --------------------------------------------------------------------------
  // Core Request Method
  // --------------------------------------------------------------------------

  async request<T>(endpoint: string, config: RequestConfig = {}): Promise<T> {
    let processedConfig = { ...config };

    // Run request interceptors
    for (const interceptor of this.interceptors.request) {
      processedConfig = await interceptor(processedConfig);
    }

    const url = this.buildUrl(endpoint, processedConfig.params);
    const timeout = processedConfig.timeout ?? this.timeout;
    const retryConfig = processedConfig.retry ?? DEFAULT_RETRY;

    // Build headers
    const headers: Record<string, string> = {
      ...this.defaultHeaders,
      ...processedConfig.headers,
    };

    // Add auth token if not skipped
    if (!processedConfig.skipAuth) {
      const token = await tokenManager.getAccessToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    // Build fetch options
    const fetchOptions: RequestInit = {
      method: processedConfig.method ?? 'GET',
      headers,
      cache: processedConfig.cache,
      signal: processedConfig.signal,
    };

    if (processedConfig.body && processedConfig.method !== 'GET') {
      fetchOptions.body = JSON.stringify(processedConfig.body);
    }

    // Execute with retry logic
    return this.executeWithRetry<T>(url, fetchOptions, timeout, retryConfig);
  }

  // --------------------------------------------------------------------------
  // Retry Logic
  // --------------------------------------------------------------------------

  private async executeWithRetry<T>(
    url: string,
    options: RequestInit,
    timeout: number,
    retryConfig: RetryConfig,
    attempt: number = 1
  ): Promise<T> {
    try {
      const response = await this.fetchWithTimeout(url, options, timeout);
      return await this.handleResponse<T>(response);
    } catch (error) {
      const apiError = this.normalizeError(error);

      // Check if should retry
      const shouldRetry =
        attempt < retryConfig.attempts &&
        (retryConfig.retryOn?.includes(apiError.status) || apiError instanceof NetworkError);

      if (shouldRetry) {
        const delay = this.calculateDelay(retryConfig, attempt);
        await this.sleep(delay);
        return this.executeWithRetry<T>(url, options, timeout, retryConfig, attempt + 1);
      }

      // Run error interceptors
      let processedError = apiError;
      for (const interceptor of this.interceptors.error) {
        processedError = await interceptor(processedError);
      }

      throw processedError;
    }
  }

  // --------------------------------------------------------------------------
  // Helpers
  // --------------------------------------------------------------------------

  private buildUrl(endpoint: string, params?: Record<string, string | number | boolean | undefined>): string {
    const url = new URL(endpoint.startsWith('http') ? endpoint : `${this.baseUrl}${endpoint}`);

    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          url.searchParams.append(key, String(value));
        }
      });
    }

    return url.toString();
  }

  private async fetchWithTimeout(url: string, options: RequestInit, timeout: number): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: options.signal ?? controller.signal,
      });
      return response;
    } catch (error) {
      if (error instanceof Error && error.name === 'AbortError') {
        throw new TimeoutError(`Request timed out after ${timeout}ms`);
      }
      throw error;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    let data: unknown;

    const contentType = response.headers.get('content-type');
    if (contentType?.includes('application/json')) {
      data = await response.json();
    } else {
      data = await response.text();
    }

    if (!response.ok) {
      throw new ApiError({
        message: this.extractErrorMessage(data) || response.statusText,
        status: response.status,
        code: this.extractErrorCode(data),
        data,
      });
    }

    // Wrap in ApiResponse and run interceptors
    let apiResponse: ApiResponse<T> = {
      data: data as T,
      status: response.status,
      headers: Object.fromEntries(response.headers.entries()),
    };

    for (const interceptor of this.interceptors.response) {
      apiResponse = (await interceptor(apiResponse)) as ApiResponse<T>;
    }

    return apiResponse.data;
  }

  private extractErrorMessage(data: unknown): string | undefined {
    if (typeof data === 'object' && data !== null) {
      const obj = data as Record<string, unknown>;
      return (obj.message ?? obj.error ?? obj.detail) as string | undefined;
    }
    return undefined;
  }

  private extractErrorCode(data: unknown): string | undefined {
    if (typeof data === 'object' && data !== null) {
      const obj = data as Record<string, unknown>;
      return (obj.code ?? obj.error_code) as string | undefined;
    }
    return undefined;
  }

  private normalizeError(error: unknown): ApiError {
    if (error instanceof ApiError) {
      return error;
    }

    if (error instanceof TypeError && error.message === 'Failed to fetch') {
      return new NetworkError('Network request failed. Check your connection.');
    }

    if (error instanceof Error) {
      return new ApiError({
        message: error.message,
        status: 0,
      });
    }

    return new ApiError({
      message: 'Unknown error occurred',
      status: 0,
    });
  }

  private calculateDelay(config: RetryConfig, attempt: number): number {
    if (config.backoff === 'exponential') {
      return config.delay * Math.pow(2, attempt - 1);
    }
    return config.delay * attempt;
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

// ============================================================================
// Default Instance
// ============================================================================

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL ?? 'https://api.example.com/v1';

export const apiClient = new ApiClient({
  baseUrl: API_BASE_URL,
  timeout: DEFAULT_TIMEOUT,
  defaultHeaders: {
    'X-Client-Version': process.env.EXPO_PUBLIC_APP_VERSION ?? '1.0.0',
    'X-Platform': 'mobile',
  },
});

export default apiClient;
