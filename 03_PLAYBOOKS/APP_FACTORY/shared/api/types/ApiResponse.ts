/**
 * ApiResponse.ts - Standard API response types
 */

// ============================================================================
// Base Response Types
// ============================================================================

/**
 * Standard API response wrapper
 */
export interface ApiResponse<T> {
  data: T;
  status: number;
  headers: Record<string, string>;
}

/**
 * Success response with optional message
 */
export interface SuccessResponse<T = void> {
  success: true;
  data: T;
  message?: string;
}

/**
 * Error response structure
 */
export interface ErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
    field?: string;
  };
}

/**
 * Combined response type
 */
export type ApiResult<T> = SuccessResponse<T> | ErrorResponse;

// ============================================================================
// List & Collection Responses
// ============================================================================

/**
 * List response with items
 */
export interface ListResponse<T> {
  items: T[];
  count: number;
}

/**
 * Paginated response with metadata
 */
export interface PaginatedResponse<T> {
  items: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
    hasMore: boolean;
    nextCursor?: string;
    prevCursor?: string;
  };
}

/**
 * Cursor-based pagination response
 */
export interface CursorPaginatedResponse<T> {
  items: T[];
  cursor: {
    next: string | null;
    previous: string | null;
  };
  hasMore: boolean;
}

// ============================================================================
// Common Field Types
// ============================================================================

/**
 * Timestamp fields present on most resources
 */
export interface TimestampFields {
  createdAt: string;
  updatedAt: string;
}

/**
 * Resource with ID and timestamps
 */
export interface Resource extends TimestampFields {
  id: string;
}

/**
 * Soft-deletable resource
 */
export interface SoftDeletableResource extends Resource {
  deletedAt: string | null;
}

// ============================================================================
// Operation Responses
// ============================================================================

/**
 * Create operation response
 */
export interface CreateResponse<T> {
  id: string;
  data: T;
  message?: string;
}

/**
 * Update operation response
 */
export interface UpdateResponse<T> {
  data: T;
  message?: string;
}

/**
 * Delete operation response
 */
export interface DeleteResponse {
  id: string;
  deleted: boolean;
  message?: string;
}

/**
 * Bulk operation response
 */
export interface BulkResponse<T> {
  successful: T[];
  failed: {
    item: unknown;
    error: string;
  }[];
  total: number;
  successCount: number;
  failureCount: number;
}

// ============================================================================
// Status Responses
// ============================================================================

/**
 * Health check response
 */
export interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  version: string;
  timestamp: string;
  services: {
    name: string;
    status: 'up' | 'down' | 'degraded';
    latency?: number;
  }[];
}

/**
 * Rate limit info (typically in headers, but sometimes in response)
 */
export interface RateLimitInfo {
  limit: number;
  remaining: number;
  reset: number;
  retryAfter?: number;
}

// ============================================================================
// Validation Types
// ============================================================================

/**
 * Field validation error
 */
export interface FieldError {
  field: string;
  message: string;
  code: string;
}

/**
 * Validation error response
 */
export interface ValidationErrorResponse {
  success: false;
  error: {
    code: 'VALIDATION_ERROR';
    message: string;
    fields: FieldError[];
  };
}

// ============================================================================
// Type Guards
// ============================================================================

export function isSuccessResponse<T>(response: ApiResult<T>): response is SuccessResponse<T> {
  return response.success === true;
}

export function isErrorResponse<T>(response: ApiResult<T>): response is ErrorResponse {
  return response.success === false;
}

export function isPaginatedResponse<T>(response: unknown): response is PaginatedResponse<T> {
  return (
    typeof response === 'object' &&
    response !== null &&
    'items' in response &&
    'pagination' in response
  );
}

export function isCursorPaginatedResponse<T>(response: unknown): response is CursorPaginatedResponse<T> {
  return (
    typeof response === 'object' &&
    response !== null &&
    'items' in response &&
    'cursor' in response
  );
}

// ============================================================================
// Response Helpers
// ============================================================================

/**
 * Extract items from any paginated response type
 */
export function extractItems<T>(
  response: ListResponse<T> | PaginatedResponse<T> | CursorPaginatedResponse<T>
): T[] {
  return response.items;
}

/**
 * Create a success response
 */
export function createSuccessResponse<T>(data: T, message?: string): SuccessResponse<T> {
  return {
    success: true,
    data,
    message,
  };
}

/**
 * Create an error response
 */
export function createErrorResponse(
  code: string,
  message: string,
  details?: Record<string, unknown>
): ErrorResponse {
  return {
    success: false,
    error: {
      code,
      message,
      details,
    },
  };
}

export default ApiResponse;
