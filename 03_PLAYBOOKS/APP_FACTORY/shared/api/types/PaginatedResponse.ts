/**
 * PaginatedResponse.ts - Pagination types and utilities
 */

// ============================================================================
// Pagination Request Types
// ============================================================================

/**
 * Standard page-based pagination params
 */
export interface PagePaginationParams {
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

/**
 * Cursor-based pagination params
 */
export interface CursorPaginationParams {
  cursor?: string;
  limit?: number;
  direction?: 'forward' | 'backward';
}

/**
 * Offset-based pagination params
 */
export interface OffsetPaginationParams {
  offset?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

/**
 * Combined pagination params (supports all types)
 */
export type PaginationParams =
  | PagePaginationParams
  | CursorPaginationParams
  | OffsetPaginationParams;

// ============================================================================
// Pagination Response Types
// ============================================================================

/**
 * Page-based pagination metadata
 */
export interface PagePaginationMeta {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
  hasNext: boolean;
  hasPrev: boolean;
}

/**
 * Cursor-based pagination metadata
 */
export interface CursorPaginationMeta {
  nextCursor: string | null;
  prevCursor: string | null;
  hasNext: boolean;
  hasPrev: boolean;
}

/**
 * Offset-based pagination metadata
 */
export interface OffsetPaginationMeta {
  offset: number;
  limit: number;
  total: number;
  hasMore: boolean;
}

/**
 * Page-based paginated response
 */
export interface PagePaginatedResponse<T> {
  items: T[];
  meta: PagePaginationMeta;
}

/**
 * Cursor-based paginated response
 */
export interface CursorPaginatedResponse<T> {
  items: T[];
  meta: CursorPaginationMeta;
}

/**
 * Offset-based paginated response
 */
export interface OffsetPaginatedResponse<T> {
  items: T[];
  meta: OffsetPaginationMeta;
}

/**
 * Generic paginated response (union type)
 */
export type PaginatedResponse<T> =
  | PagePaginatedResponse<T>
  | CursorPaginatedResponse<T>
  | OffsetPaginatedResponse<T>;

// ============================================================================
// Pagination State
// ============================================================================

/**
 * Client-side pagination state
 */
export interface PaginationState<T> {
  items: T[];
  currentPage: number;
  totalPages: number;
  totalItems: number;
  pageSize: number;
  isLoading: boolean;
  hasMore: boolean;
  error: Error | null;
}

/**
 * Initial pagination state factory
 */
export function createInitialPaginationState<T>(pageSize: number = 20): PaginationState<T> {
  return {
    items: [],
    currentPage: 1,
    totalPages: 0,
    totalItems: 0,
    pageSize,
    isLoading: false,
    hasMore: true,
    error: null,
  };
}

// ============================================================================
// Type Guards
// ============================================================================

export function isPagePaginatedResponse<T>(
  response: PaginatedResponse<T>
): response is PagePaginatedResponse<T> {
  return 'meta' in response && 'page' in (response as PagePaginatedResponse<T>).meta;
}

export function isCursorPaginatedResponse<T>(
  response: PaginatedResponse<T>
): response is CursorPaginatedResponse<T> {
  return 'meta' in response && 'nextCursor' in (response as CursorPaginatedResponse<T>).meta;
}

export function isOffsetPaginatedResponse<T>(
  response: PaginatedResponse<T>
): response is OffsetPaginatedResponse<T> {
  return 'meta' in response && 'offset' in (response as OffsetPaginatedResponse<T>).meta;
}

// ============================================================================
// Pagination Helpers
// ============================================================================

/**
 * Calculate total pages from total items and page size
 */
export function calculateTotalPages(totalItems: number, pageSize: number): number {
  return Math.ceil(totalItems / pageSize);
}

/**
 * Calculate offset from page number and page size
 */
export function calculateOffset(page: number, pageSize: number): number {
  return (page - 1) * pageSize;
}

/**
 * Calculate page number from offset and page size
 */
export function calculatePage(offset: number, pageSize: number): number {
  return Math.floor(offset / pageSize) + 1;
}

/**
 * Check if there are more pages
 */
export function hasMorePages(currentPage: number, totalPages: number): boolean {
  return currentPage < totalPages;
}

/**
 * Get page range for pagination UI
 */
export function getPageRange(
  currentPage: number,
  totalPages: number,
  maxVisible: number = 5
): number[] {
  if (totalPages <= maxVisible) {
    return Array.from({ length: totalPages }, (_, i) => i + 1);
  }

  const half = Math.floor(maxVisible / 2);
  let start = currentPage - half;
  let end = currentPage + half;

  if (start < 1) {
    start = 1;
    end = maxVisible;
  }

  if (end > totalPages) {
    end = totalPages;
    start = totalPages - maxVisible + 1;
  }

  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
}

/**
 * Build pagination params for API request
 */
export function buildPaginationParams(
  page: number,
  pageSize: number,
  sortBy?: string,
  sortOrder?: 'asc' | 'desc'
): PagePaginationParams {
  const params: PagePaginationParams = {
    page,
    limit: pageSize,
  };

  if (sortBy) {
    params.sortBy = sortBy;
    params.sortOrder = sortOrder ?? 'asc';
  }

  return params;
}

/**
 * Merge new page data into existing state
 */
export function mergePaginatedData<T>(
  currentItems: T[],
  newItems: T[],
  page: number,
  mode: 'replace' | 'append' | 'prepend' = 'replace'
): T[] {
  switch (mode) {
    case 'append':
      return [...currentItems, ...newItems];
    case 'prepend':
      return [...newItems, ...currentItems];
    case 'replace':
    default:
      return newItems;
  }
}

/**
 * Create empty paginated response
 */
export function createEmptyPaginatedResponse<T>(): PagePaginatedResponse<T> {
  return {
    items: [],
    meta: {
      page: 1,
      limit: 20,
      total: 0,
      totalPages: 0,
      hasNext: false,
      hasPrev: false,
    },
  };
}

/**
 * Transform API response to normalized pagination state
 */
export function normalizePaginatedResponse<T>(
  response: PaginatedResponse<T>,
  pageSize: number
): PaginationState<T> {
  if (isPagePaginatedResponse(response)) {
    return {
      items: response.items,
      currentPage: response.meta.page,
      totalPages: response.meta.totalPages,
      totalItems: response.meta.total,
      pageSize: response.meta.limit,
      isLoading: false,
      hasMore: response.meta.hasNext,
      error: null,
    };
  }

  if (isCursorPaginatedResponse(response)) {
    return {
      items: response.items,
      currentPage: 1, // Cursor pagination doesn't have pages
      totalPages: 0,
      totalItems: 0,
      pageSize,
      isLoading: false,
      hasMore: response.meta.hasNext,
      error: null,
    };
  }

  if (isOffsetPaginatedResponse(response)) {
    const currentPage = calculatePage(response.meta.offset, response.meta.limit);
    const totalPages = calculateTotalPages(response.meta.total, response.meta.limit);

    return {
      items: response.items,
      currentPage,
      totalPages,
      totalItems: response.meta.total,
      pageSize: response.meta.limit,
      isLoading: false,
      hasMore: response.meta.hasMore,
      error: null,
    };
  }

  return createInitialPaginationState(pageSize);
}

export default PagePaginatedResponse;
