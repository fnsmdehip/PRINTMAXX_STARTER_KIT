/**
 * Offline First - Patterns for offline-first data access
 *
 * Provides hooks and utilities for building apps that work
 * seamlessly offline and sync when connectivity returns.
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import NetInfo, { NetInfoState } from '@react-native-community/netinfo';
import { StorageService } from '../StorageService';
import { SyncService, SyncState } from './SyncService';
import { CacheQueries } from '../database/queries';

// Types
export interface OfflineConfig {
  /** Storage key for caching */
  cacheKey: string;
  /** Cache TTL in milliseconds */
  cacheTtl?: number;
  /** Fetch function to get fresh data */
  fetchFn: () => Promise<unknown>;
  /** Whether to show stale data while refreshing */
  staleWhileRevalidate?: boolean;
}

export interface OfflineState<T> {
  data: T | null;
  isLoading: boolean;
  isRefreshing: boolean;
  isStale: boolean;
  isOffline: boolean;
  error: string | null;
  lastUpdated: Date | null;
}

export interface OfflineActions {
  refresh: () => Promise<void>;
  clear: () => Promise<void>;
}

export type UseOfflineReturn<T> = OfflineState<T> & OfflineActions;

/**
 * Hook for network connectivity state
 */
export function useNetworkState(): {
  isConnected: boolean;
  connectionType: string | null;
  isInternetReachable: boolean | null;
} {
  const [state, setState] = useState({
    isConnected: true,
    connectionType: null as string | null,
    isInternetReachable: null as boolean | null,
  });

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener((netState: NetInfoState) => {
      setState({
        isConnected: netState.isConnected ?? false,
        connectionType: netState.type,
        isInternetReachable: netState.isInternetReachable,
      });
    });

    return () => unsubscribe();
  }, []);

  return state;
}

/**
 * Hook for sync state
 */
export function useSyncState(): SyncState & { sync: () => Promise<void> } {
  const [state, setState] = useState<SyncState>({
    status: 'idle',
    lastSyncAt: null,
    pendingCount: 0,
    failedCount: 0,
    isOnline: true,
  });

  useEffect(() => {
    // Get initial state
    SyncService.getState().then(setState);

    // Subscribe to changes
    const unsubscribe = SyncService.subscribe(setState);
    return unsubscribe;
  }, []);

  const sync = useCallback(async () => {
    await SyncService.forcSync();
  }, []);

  return { ...state, sync };
}

/**
 * Hook for offline-first data fetching
 */
export function useOfflineData<T>(config: OfflineConfig): UseOfflineReturn<T> {
  const [state, setState] = useState<OfflineState<T>>({
    data: null,
    isLoading: true,
    isRefreshing: false,
    isStale: false,
    isOffline: false,
    error: null,
    lastUpdated: null,
  });

  const mountedRef = useRef(true);
  const configRef = useRef(config);
  configRef.current = config;

  // Load cached data on mount
  useEffect(() => {
    mountedRef.current = true;

    const loadCached = async () => {
      const result = await StorageService.get<{ data: T; timestamp: number }>(config.cacheKey);

      if (!mountedRef.current) return;

      if (result.success && result.data) {
        const isStale = config.cacheTtl
          ? Date.now() - result.data.timestamp > config.cacheTtl
          : false;

        setState((prev) => ({
          ...prev,
          data: result.data!.data,
          lastUpdated: new Date(result.data!.timestamp),
          isStale,
          isLoading: false,
        }));

        // If stale or no cache TTL, fetch fresh data
        if (isStale || config.staleWhileRevalidate) {
          fetchFreshData();
        }
      } else {
        // No cached data, fetch fresh
        fetchFreshData();
      }
    };

    const fetchFreshData = async () => {
      const netState = await NetInfo.fetch();

      if (!netState.isConnected) {
        if (mountedRef.current) {
          setState((prev) => ({
            ...prev,
            isOffline: true,
            isLoading: false,
            error: prev.data ? null : 'No cached data available offline',
          }));
        }
        return;
      }

      setState((prev) => ({ ...prev, isRefreshing: true, error: null }));

      try {
        const freshData = await configRef.current.fetchFn();
        const timestamp = Date.now();

        // Cache the data
        await StorageService.set(configRef.current.cacheKey, { data: freshData, timestamp });

        if (mountedRef.current) {
          setState({
            data: freshData as T,
            isLoading: false,
            isRefreshing: false,
            isStale: false,
            isOffline: false,
            error: null,
            lastUpdated: new Date(timestamp),
          });
        }
      } catch (error) {
        if (mountedRef.current) {
          setState((prev) => ({
            ...prev,
            isLoading: false,
            isRefreshing: false,
            error: error instanceof Error ? error.message : 'Failed to fetch data',
          }));
        }
      }
    };

    loadCached();

    return () => {
      mountedRef.current = false;
    };
  }, [config.cacheKey]);

  // Subscribe to network changes
  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener((netState: NetInfoState) => {
      if (!mountedRef.current) return;

      const wasOffline = state.isOffline;
      const isNowOnline = netState.isConnected;

      setState((prev) => ({ ...prev, isOffline: !isNowOnline }));

      // If we just came online and have stale data, refresh
      if (wasOffline && isNowOnline && state.isStale) {
        refresh();
      }
    });

    return () => unsubscribe();
  }, [state.isOffline, state.isStale]);

  const refresh = useCallback(async () => {
    const netState = await NetInfo.fetch();

    if (!netState.isConnected) {
      setState((prev) => ({ ...prev, isOffline: true }));
      return;
    }

    setState((prev) => ({ ...prev, isRefreshing: true, error: null }));

    try {
      const freshData = await configRef.current.fetchFn();
      const timestamp = Date.now();

      await StorageService.set(configRef.current.cacheKey, { data: freshData, timestamp });

      if (mountedRef.current) {
        setState((prev) => ({
          ...prev,
          data: freshData as T,
          isRefreshing: false,
          isStale: false,
          isOffline: false,
          lastUpdated: new Date(timestamp),
        }));
      }
    } catch (error) {
      if (mountedRef.current) {
        setState((prev) => ({
          ...prev,
          isRefreshing: false,
          error: error instanceof Error ? error.message : 'Failed to refresh',
        }));
      }
    }
  }, []);

  const clear = useCallback(async () => {
    await StorageService.delete(configRef.current.cacheKey);
    setState({
      data: null,
      isLoading: false,
      isRefreshing: false,
      isStale: false,
      isOffline: false,
      error: null,
      lastUpdated: null,
    });
  }, []);

  return {
    ...state,
    refresh,
    clear,
  };
}

/**
 * Hook for offline-first mutations
 */
export function useOfflineMutation<TData, TVariables>(
  entityType: string,
  mutationFn: (variables: TVariables) => Promise<TData>
): {
  mutate: (variables: TVariables, entityId: string) => Promise<TData | null>;
  isPending: boolean;
  error: string | null;
} {
  const [isPending, setIsPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mutate = useCallback(
    async (variables: TVariables, entityId: string): Promise<TData | null> => {
      setIsPending(true);
      setError(null);

      const netState = await NetInfo.fetch();

      if (!netState.isConnected) {
        // Queue for later sync
        await SyncService.queueChange(
          'UPDATE',
          entityType,
          entityId,
          variables as Record<string, unknown>
        );

        setIsPending(false);
        return null;
      }

      try {
        const result = await mutationFn(variables);
        setIsPending(false);
        return result;
      } catch (err) {
        // Queue for retry
        await SyncService.queueChange(
          'UPDATE',
          entityType,
          entityId,
          variables as Record<string, unknown>
        );

        setError(err instanceof Error ? err.message : 'Mutation failed');
        setIsPending(false);
        return null;
      }
    },
    [entityType, mutationFn]
  );

  return { mutate, isPending, error };
}

/**
 * Optimistic update helper
 */
export async function optimisticUpdate<T>(
  cacheKey: string,
  updater: (current: T | null) => T,
  rollback?: () => void
): Promise<{ commit: () => Promise<void>; rollback: () => Promise<void> }> {
  // Get current data
  const currentResult = await StorageService.get<{ data: T; timestamp: number }>(cacheKey);
  const currentData = currentResult.success ? currentResult.data?.data ?? null : null;

  // Apply optimistic update
  const newData = updater(currentData);
  await StorageService.set(cacheKey, { data: newData, timestamp: Date.now() });

  return {
    commit: async () => {
      // Data is already saved, nothing to do
    },
    rollback: async () => {
      // Restore original data
      if (currentData) {
        await StorageService.set(cacheKey, { data: currentData, timestamp: Date.now() });
      } else {
        await StorageService.delete(cacheKey);
      }
      rollback?.();
    },
  };
}

/**
 * Prefetch data for offline use
 */
export async function prefetchForOffline<T>(
  cacheKey: string,
  fetchFn: () => Promise<T>,
  options?: { ttl?: number; contentType?: string }
): Promise<boolean> {
  try {
    const data = await fetchFn();
    const timestamp = Date.now();

    await StorageService.set(cacheKey, { data, timestamp }, { ttl: options?.ttl });

    // Also store in database cache if content type provided
    if (options?.contentType) {
      await CacheQueries.set(cacheKey, options.contentType, data, options.ttl);
    }

    return true;
  } catch {
    return false;
  }
}

/**
 * Check if data is available offline
 */
export async function isAvailableOffline(cacheKey: string): Promise<boolean> {
  const result = await StorageService.get(cacheKey);
  return result.success && result.data !== null;
}

/**
 * Get offline cache size
 */
export async function getOfflineCacheSize(): Promise<{
  asyncStorageSize: number;
  dbCacheSize: number;
  totalSize: number;
}> {
  const storageInfo = await StorageService.getStorageInfo();
  const asyncStorageSize = storageInfo.success ? storageInfo.data.estimatedSize : 0;

  const dbCacheSize = await CacheQueries.getSize();

  return {
    asyncStorageSize,
    dbCacheSize,
    totalSize: asyncStorageSize + dbCacheSize,
  };
}

/**
 * Clear old offline data
 */
export async function clearOldOfflineData(maxAgeMs: number): Promise<number> {
  // Clean expired cache entries
  const cleaned = await CacheQueries.cleanExpired();
  return cleaned;
}
