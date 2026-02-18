/**
 * ApiError.ts - Error types for API layer
 */

// ============================================================================
// Error Codes
// ============================================================================

export const ErrorCodes = {
  // Client errors (4xx)
  BAD_REQUEST: 'BAD_REQUEST',
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  NOT_FOUND: 'NOT_FOUND',
  CONFLICT: 'CONFLICT',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  RATE_LIMITED: 'RATE_LIMITED',
  PAYLOAD_TOO_LARGE: 'PAYLOAD_TOO_LARGE',

  // Server errors (5xx)
  SERVER_ERROR: 'SERVER_ERROR',
  SERVICE_UNAVAILABLE: 'SERVICE_UNAVAILABLE',
  GATEWAY_TIMEOUT: 'GATEWAY_TIMEOUT',

  // Network errors
  NETWORK_ERROR: 'NETWORK_ERROR',
  TIMEOUT: 'TIMEOUT',
  ABORTED: 'ABORTED',

  // Auth errors
  TOKEN_EXPIRED: 'TOKEN_EXPIRED',
  TOKEN_INVALID: 'TOKEN_INVALID',
  SESSION_EXPIRED: 'SESSION_EXPIRED',
  REFRESH_FAILED: 'REFRESH_FAILED',

  // Unknown
  UNKNOWN: 'UNKNOWN',
} as const;

export type ErrorCode = (typeof ErrorCodes)[keyof typeof ErrorCodes];

// ============================================================================
// Error Config
// ============================================================================

export interface ApiErrorConfig {
  message: string;
  status: number;
  code?: string;
  data?: unknown;
  cause?: Error;
  retryable?: boolean;
}

// ============================================================================
// Base ApiError Class
// ============================================================================

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly data: unknown;
  readonly retryable: boolean;
  readonly timestamp: Date;

  constructor(config: ApiErrorConfig) {
    super(config.message);
    this.name = 'ApiError';
    this.status = config.status;
    this.code = config.code ?? this.deriveCode(config.status);
    this.data = config.data;
    this.retryable = config.retryable ?? this.isRetryable(config.status);
    this.timestamp = new Date();

    if (config.cause) {
      this.cause = config.cause;
    }

    // Maintain proper stack trace
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, ApiError);
    }
  }

  private deriveCode(status: number): ErrorCode {
    const statusCodeMap: Record<number, ErrorCode> = {
      400: ErrorCodes.BAD_REQUEST,
      401: ErrorCodes.UNAUTHORIZED,
      403: ErrorCodes.FORBIDDEN,
      404: ErrorCodes.NOT_FOUND,
      409: ErrorCodes.CONFLICT,
      422: ErrorCodes.VALIDATION_ERROR,
      429: ErrorCodes.RATE_LIMITED,
      413: ErrorCodes.PAYLOAD_TOO_LARGE,
      500: ErrorCodes.SERVER_ERROR,
      503: ErrorCodes.SERVICE_UNAVAILABLE,
      504: ErrorCodes.GATEWAY_TIMEOUT,
    };

    return statusCodeMap[status] ?? ErrorCodes.UNKNOWN;
  }

  private isRetryable(status: number): boolean {
    // Retry on server errors and specific client errors
    const retryableStatuses = [408, 429, 500, 502, 503, 504];
    return retryableStatuses.includes(status);
  }

  /**
   * Check if error is a client error (4xx)
   */
  isClientError(): boolean {
    return this.status >= 400 && this.status < 500;
  }

  /**
   * Check if error is a server error (5xx)
   */
  isServerError(): boolean {
    return this.status >= 500 && this.status < 600;
  }

  /**
   * Check if error is an auth error
   */
  isAuthError(): boolean {
    return this.status === 401 || this.status === 403;
  }

  /**
   * Check if error is a validation error
   */
  isValidationError(): boolean {
    return this.status === 422 || this.code === ErrorCodes.VALIDATION_ERROR;
  }

  /**
   * Check if error is rate limited
   */
  isRateLimited(): boolean {
    return this.status === 429 || this.code === ErrorCodes.RATE_LIMITED;
  }

  /**
   * Get user-friendly error message
   */
  getUserMessage(): string {
    const userMessages: Record<string, string> = {
      [ErrorCodes.NETWORK_ERROR]: 'Connection failed. Check your internet.',
      [ErrorCodes.TIMEOUT]: 'Request timed out. Try again.',
      [ErrorCodes.UNAUTHORIZED]: 'Please sign in to continue.',
      [ErrorCodes.FORBIDDEN]: 'You don\'t have access to this.',
      [ErrorCodes.NOT_FOUND]: 'Not found.',
      [ErrorCodes.RATE_LIMITED]: 'Too many requests. Wait a moment.',
      [ErrorCodes.SERVER_ERROR]: 'Something went wrong. Try again.',
      [ErrorCodes.SERVICE_UNAVAILABLE]: 'Service temporarily unavailable.',
      [ErrorCodes.VALIDATION_ERROR]: 'Please check your input.',
    };

    return userMessages[this.code] ?? this.message;
  }

  /**
   * Convert to plain object for logging
   */
  toJSON(): Record<string, unknown> {
    return {
      name: this.name,
      message: this.message,
      status: this.status,
      code: this.code,
      data: this.data,
      retryable: this.retryable,
      timestamp: this.timestamp.toISOString(),
    };
  }
}

// ============================================================================
// Specialized Error Classes
// ============================================================================

/**
 * Network-level error (no response received)
 */
export class NetworkError extends ApiError {
  constructor(message: string = 'Network request failed') {
    super({
      message,
      status: 0,
      code: ErrorCodes.NETWORK_ERROR,
      retryable: true,
    });
    this.name = 'NetworkError';
  }
}

/**
 * Request timeout error
 */
export class TimeoutError extends ApiError {
  constructor(message: string = 'Request timed out') {
    super({
      message,
      status: 0,
      code: ErrorCodes.TIMEOUT,
      retryable: true,
    });
    this.name = 'TimeoutError';
  }
}

/**
 * Request aborted error
 */
export class AbortError extends ApiError {
  constructor(message: string = 'Request was aborted') {
    super({
      message,
      status: 0,
      code: ErrorCodes.ABORTED,
      retryable: false,
    });
    this.name = 'AbortError';
  }
}

/**
 * Authentication error
 */
export class AuthError extends ApiError {
  constructor(
    message: string = 'Authentication required',
    code: ErrorCode = ErrorCodes.UNAUTHORIZED
  ) {
    super({
      message,
      status: 401,
      code,
      retryable: false,
    });
    this.name = 'AuthError';
  }
}

/**
 * Validation error with field-level details
 */
export interface FieldError {
  field: string;
  message: string;
  code?: string;
}

export class ValidationError extends ApiError {
  readonly fields: FieldError[];

  constructor(message: string, fields: FieldError[] = []) {
    super({
      message,
      status: 422,
      code: ErrorCodes.VALIDATION_ERROR,
      data: { fields },
      retryable: false,
    });
    this.name = 'ValidationError';
    this.fields = fields;
  }

  /**
   * Get error message for a specific field
   */
  getFieldError(field: string): string | undefined {
    return this.fields.find((f) => f.field === field)?.message;
  }

  /**
   * Get all field errors as a map
   */
  getFieldErrors(): Record<string, string> {
    return this.fields.reduce(
      (acc, f) => {
        acc[f.field] = f.message;
        return acc;
      },
      {} as Record<string, string>
    );
  }
}

/**
 * Rate limit error with retry info
 */
export class RateLimitError extends ApiError {
  readonly retryAfter: number;

  constructor(message: string = 'Rate limit exceeded', retryAfter: number = 60) {
    super({
      message,
      status: 429,
      code: ErrorCodes.RATE_LIMITED,
      data: { retryAfter },
      retryable: true,
    });
    this.name = 'RateLimitError';
    this.retryAfter = retryAfter;
  }
}

// ============================================================================
// Error Factory
// ============================================================================

/**
 * Create appropriate error type from response
 */
export function createApiError(
  status: number,
  message: string,
  data?: unknown
): ApiError {
  switch (status) {
    case 0:
      return new NetworkError(message);
    case 401:
      return new AuthError(message);
    case 422:
      if (data && typeof data === 'object' && 'fields' in data) {
        return new ValidationError(message, (data as { fields: FieldError[] }).fields);
      }
      return new ValidationError(message);
    case 429:
      const retryAfter = data && typeof data === 'object' && 'retryAfter' in data
        ? (data as { retryAfter: number }).retryAfter
        : 60;
      return new RateLimitError(message, retryAfter);
    default:
      return new ApiError({ message, status, data });
  }
}

// ============================================================================
// Type Guards
// ============================================================================

export function isApiError(error: unknown): error is ApiError {
  return error instanceof ApiError;
}

export function isNetworkError(error: unknown): error is NetworkError {
  return error instanceof NetworkError;
}

export function isTimeoutError(error: unknown): error is TimeoutError {
  return error instanceof TimeoutError;
}

export function isAuthError(error: unknown): error is AuthError {
  return error instanceof AuthError;
}

export function isValidationError(error: unknown): error is ValidationError {
  return error instanceof ValidationError;
}

export function isRateLimitError(error: unknown): error is RateLimitError {
  return error instanceof RateLimitError;
}

export default ApiError;
