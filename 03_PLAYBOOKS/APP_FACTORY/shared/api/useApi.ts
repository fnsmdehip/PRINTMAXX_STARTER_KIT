/**
 * useApi.ts - React hook for API calls
 *
 * Provides loading states, error handling, retry logic, and caching.
 */

import { useState, useCallback, useRef, useEffect } from 'react';
import { ApiError } from './types/ApiError';

// ============================================================================
// Types
// ============================================================================

export interface UseApiState<T> {
  data: T | null;
  error: ApiError | null;
  isLoading: boolean;
  isRefreshing: boolean;
  isSuccess: boolean;
  isError: boolean;
}

export interface UseApiOptions<T> {
  /** Initial data before fetch */
  initialData?: T;
  /** Fetch immediately on mount */
  immediate?: boolean;
  /** Cache key for deduplication */
  cacheKey?: string;
  /** Cache TTL in ms (default: 5 minutes) */
  cacheTtl?: number;
  /** Max retry attempts */
  retryCount?: number;
  /** Delay between retries in ms */
  retryDelay?: number;
  /** Callback on success */
  onSuccess?: (data: T) => void;
  /** Callback on error */
  onError?: (error: ApiError) => void;
  /** Transform response data */
  transform?: (data: unknown) => T;
  /** Dependencies to trigger refetch */
  deps?: unknown[];
}

export interface UseApiReturn<T, P extends unknown[]> extends UseApiState<T> {
  /** Execute the API call */
  execute: (...params: P) => Promise<T | null>;
  /** Refresh (shows refresh indicator instead of loading) */
  refresh: (...params: P) => Promise<T | null>;
  /** Reset to initial state */
  reset: () => void;
  /** Manually set data */
  setData: (data: T | null) => void;
  /** Manually set error */
  setError: (error: ApiError | null) => void;
}

export interface UseMutationOptions<T, P> {
  /** Callback on success */
  onSuccess?: (data: T, params: P) => void;
  /** Callback on error */
  onError?: (error: ApiError, params: P) => void;
  /** Optimistic update function */
  optimisticUpdate?: (params: P) => void;
  /** Rollback function on error */
  rollback?: (params: P) => void;
}

export interface UseMutationReturn<T, P> {
  data: T | null;
  error: ApiError | null;
  isLoading: boolean;
  isSuccess: boolean;
  isError: boolean;
  mutate: (params: P) => Promise<T | null>;
  reset: () => void;
}

// ============================================================================
// Cache Implementation
// ============================================================================

interface CacheEntry<T> {
  data: T;
  timestamp: number;
  ttl: number;
}

class ApiCache {
  private cache = new Map<string, CacheEntry<unknown>>();

  get<T>(key: string): T | null {
    const entry = this.cache.get(key);
    if (!entry) return null;

    const isExpired = Date.now() - entry.timestamp > entry.ttl;
    if (isExpired) {
      this.cache.delete(key);
      return null;
    }

    return entry.data as T;
  }

  set<T>(key: string, data: T, ttl: number): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl,
    });
  }

  invalidate(key: string): void {
    this.cache.delete(key);
  }

  invalidatePattern(pattern: string): void {
    const regex = new RegExp(pattern);
    for (const key of this.cache.keys()) {
      if (regex.test(key)) {
        this.cache.delete(key);
      }
    }
  }

  clear(): void {
    this.cache.clear();
  }
}

export const apiCache = new ApiCache();

// ============================================================================
// Main Hook
// ============================================================================

const DEFAULT_CACHE_TTL = 5 * 60 * 1000; // 5 minutes
const DEFAULT_RETRY_COUNT = 0;
const DEFAULT_RETRY_DELAY = 1000;

export function useApi<T, P extends unknown[] = []>(
  apiFunction: (...params: P) => Promise<T>,
  options: UseApiOptions<T> = {}
): UseApiReturn<T, P> {
  const {
    initialData = null,
    immediate = false,
    cacheKey,
    cacheTtl = DEFAULT_CACHE_TTL,
    retryCount = DEFAULT_RETRY_COUNT,
    retryDelay = DEFAULT_RETRY_DELAY,
    onSuccess,
    onError,
    transform,
    deps = [],
  } = options;

  const [state, setState] = useState<UseApiState<T>>({
    data: initialData,
    error: null,
    isLoading: immediate,
    isRefreshing: false,
    isSuccess: false,
    isError: false,
  });

  const abortControllerRef = useRef<AbortController | null>(null);
  const mountedRef = useRef(true);
  const retryCountRef = useRef(0);
  const lastParamsRef = useRef<P | null>(null);

  // Cleanup on unmount
  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
      abortControllerRef.current?.abort();
    };
  }, []);

  const executeRequest = useCallback(
    async (params: P, isRefresh: boolean): Promise<T | null> => {
      // Cancel previous request
      abortControllerRef.current?.abort();
      abortControllerRef.current = new AbortController();

      // Check cache
      if (cacheKey && !isRefresh) {
        const cached = apiCache.get<T>(cacheKey);
        if (cached) {
          setState((prev) => ({
            ...prev,
            data: cached,
            isLoading: false,
            isRefreshing: false,
            isSuccess: true,
            isError: false,
            error: null,
          }));
          return cached;
        }
      }

      setState((prev) => ({
        ...prev,
        isLoading: !isRefresh,
        isRefreshing: isRefresh,
        isError: false,
        error: null,
      }));

      try {
        let data = await apiFunction(...params);

        // Transform if needed
        if (transform) {
          data = transform(data);
        }

        if (!mountedRef.current) return null;

        // Update cache
        if (cacheKey) {
          apiCache.set(cacheKey, data, cacheTtl);
        }

        setState({
          data,
          error: null,
          isLoading: false,
          isRefreshing: false,
          isSuccess: true,
          isError: false,
        });

        retryCountRef.current = 0;
        onSuccess?.(data);
        return data;
      } catch (err) {
        if (!mountedRef.current) return null;

        const error = err instanceof ApiError ? err : new ApiError({ message: String(err), status: 0 });

        // Retry logic
        if (retryCountRef.current < retryCount) {
          retryCountRef.current++;
          await new Promise((resolve) => setTimeout(resolve, retryDelay * retryCountRef.current));
          return executeRequest(params, isRefresh);
        }

        setState((prev) => ({
          ...prev,
          error,
          isLoading: false,
          isRefreshing: false,
          isSuccess: false,
          isError: true,
        }));

        retryCountRef.current = 0;
        onError?.(error);
        return null;
      }
    },
    [apiFunction, cacheKey, cacheTtl, retryCount, retryDelay, onSuccess, onError, transform]
  );

  const execute = useCallback(
    async (...params: P): Promise<T | null> => {
      lastParamsRef.current = params;
      retryCountRef.current = 0;
      return executeRequest(params, false);
    },
    [executeRequest]
  );

  const refresh = useCallback(
    async (...params: P): Promise<T | null> => {
      lastParamsRef.current = params;
      retryCountRef.current = 0;
      // Invalidate cache on refresh
      if (cacheKey) {
        apiCache.invalidate(cacheKey);
      }
      return executeRequest(params, true);
    },
    [executeRequest, cacheKey]
  );

  const reset = useCallback(() => {
    abortControllerRef.current?.abort();
    setState({
      data: initialData,
      error: null,
      isLoading: false,
      isRefreshing: false,
      isSuccess: false,
      isError: false,
    });
  }, [initialData]);

  const setData = useCallback((data: T | null) => {
    setState((prev) => ({ ...prev, data }));
  }, []);

  const setError = useCallback((error: ApiError | null) => {
    setState((prev) => ({ ...prev, error, isError: !!error }));
  }, []);

  // Auto-execute on mount or deps change
  useEffect(() => {
    if (immediate) {
      execute(...([] as unknown as P));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [immediate, ...deps]);

  return {
    ...state,
    execute,
    refresh,
    reset,
    setData,
    setError,
  };
}

// ============================================================================
// Mutation Hook
// ============================================================================

export function useMutation<T, P>(
  mutationFn: (params: P) => Promise<T>,
  options: UseMutationOptions<T, P> = {}
): UseMutationReturn<T, P> {
  const { onSuccess, onError, optimisticUpdate, rollback } = options;

  const [state, setState] = useState({
    data: null as T | null,
    error: null as ApiError | null,
    isLoading: false,
    isSuccess: false,
    isError: false,
  });

  const mountedRef = useRef(true);

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
    };
  }, []);

  const mutate = useCallback(
    async (params: P): Promise<T | null> => {
      setState((prev) => ({
        ...prev,
        isLoading: true,
        isError: false,
        error: null,
      }));

      // Optimistic update
      if (optimisticUpdate) {
        optimisticUpdate(params);
      }

      try {
        const data = await mutationFn(params);

        if (!mountedRef.current) return null;

        setState({
          data,
          error: null,
          isLoading: false,
          isSuccess: true,
          isError: false,
        });

        onSuccess?.(data, params);
        return data;
      } catch (err) {
        if (!mountedRef.current) return null;

        const error = err instanceof ApiError ? err : new ApiError({ message: String(err), status: 0 });

        // Rollback on error
        if (rollback) {
          rollback(params);
        }

        setState((prev) => ({
          ...prev,
          error,
          isLoading: false,
          isSuccess: false,
          isError: true,
        }));

        onError?.(error, params);
        return null;
      }
    },
    [mutationFn, onSuccess, onError, optimisticUpdate, rollback]
  );

  const reset = useCallback(() => {
    setState({
      data: null,
      error: null,
      isLoading: false,
      isSuccess: false,
      isError: false,
    });
  }, []);

  return {
    ...state,
    mutate,
    reset,
  };
}

// ============================================================================
// Infinite Query Hook (for pagination)
// ============================================================================

export interface UseInfiniteApiOptions<T, P> {
  getNextPageParam: (lastPage: T, allPages: T[]) => P | null;
  initialPageParam?: P;
  cacheKey?: string;
  onSuccess?: (data: T[]) => void;
  onError?: (error: ApiError) => void;
}

export interface UseInfiniteApiReturn<T, P> {
  data: T[];
  error: ApiError | null;
  isLoading: boolean;
  isFetchingNextPage: boolean;
  hasNextPage: boolean;
  fetchNextPage: () => Promise<void>;
  refetch: () => Promise<void>;
  reset: () => void;
}

export function useInfiniteApi<T, P>(
  apiFunction: (pageParam: P) => Promise<T>,
  options: UseInfiniteApiOptions<T, P>
): UseInfiniteApiReturn<T, P> {
  const { getNextPageParam, initialPageParam, cacheKey, onSuccess, onError } = options;

  const [pages, setPages] = useState<T[]>([]);
  const [error, setError] = useState<ApiError | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isFetchingNextPage, setIsFetchingNextPage] = useState(false);
  const [nextPageParam, setNextPageParam] = useState<P | null>(initialPageParam ?? null);

  const mountedRef = useRef(true);

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
    };
  }, []);

  const fetchNextPage = useCallback(async () => {
    if (nextPageParam === null || isFetchingNextPage) return;

    setIsFetchingNextPage(true);
    setError(null);

    try {
      const data = await apiFunction(nextPageParam);

      if (!mountedRef.current) return;

      const newPages = [...pages, data];
      setPages(newPages);
      setNextPageParam(getNextPageParam(data, newPages));

      if (cacheKey) {
        apiCache.set(cacheKey, newPages, 5 * 60 * 1000);
      }

      onSuccess?.(newPages);
    } catch (err) {
      if (!mountedRef.current) return;

      const apiError = err instanceof ApiError ? err : new ApiError({ message: String(err), status: 0 });
      setError(apiError);
      onError?.(apiError);
    } finally {
      if (mountedRef.current) {
        setIsFetchingNextPage(false);
      }
    }
  }, [apiFunction, nextPageParam, isFetchingNextPage, pages, getNextPageParam, cacheKey, onSuccess, onError]);

  const refetch = useCallback(async () => {
    if (initialPageParam === undefined) return;

    setIsLoading(true);
    setError(null);
    setPages([]);
    setNextPageParam(initialPageParam);

    try {
      const data = await apiFunction(initialPageParam);

      if (!mountedRef.current) return;

      setPages([data]);
      setNextPageParam(getNextPageParam(data, [data]));
      onSuccess?.([data]);
    } catch (err) {
      if (!mountedRef.current) return;

      const apiError = err instanceof ApiError ? err : new ApiError({ message: String(err), status: 0 });
      setError(apiError);
      onError?.(apiError);
    } finally {
      if (mountedRef.current) {
        setIsLoading(false);
      }
    }
  }, [apiFunction, initialPageParam, getNextPageParam, onSuccess, onError]);

  const reset = useCallback(() => {
    setPages([]);
    setError(null);
    setIsLoading(false);
    setIsFetchingNextPage(false);
    setNextPageParam(initialPageParam ?? null);
  }, [initialPageParam]);

  return {
    data: pages,
    error,
    isLoading,
    isFetchingNextPage,
    hasNextPage: nextPageParam !== null,
    fetchNextPage,
    refetch,
    reset,
  };
}

export default useApi;
