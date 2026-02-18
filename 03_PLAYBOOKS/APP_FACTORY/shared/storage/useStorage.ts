/**
 * useStorage - React hook for storage operations
 *
 * Features:
 * - Loading states for async operations
 * - Auto-persist on value changes
 * - Clear storage functionality
 * - Type-safe operations
 * - Optimistic updates
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { StorageService, StorageOptions, StorageResult } from './StorageService';

// Types
export interface UseStorageState<T> {
  value: T | null;
  isLoading: boolean;
  error: string | null;
  lastUpdated: number | null;
}

export interface UseStorageActions<T> {
  setValue: (newValue: T) => Promise<void>;
  refresh: () => Promise<void>;
  clear: () => Promise<void>;
  update: (updater: (current: T | null) => T) => Promise<void>;
}

export type UseStorageReturn<T> = UseStorageState<T> & UseStorageActions<T>;

/**
 * Hook for persisted storage with loading states
 *
 * @param key - Storage key
 * @param defaultValue - Default value if key doesn't exist
 * @param options - Storage options (encryption, TTL)
 */
export function useStorage<T>(
  key: string,
  defaultValue: T | null = null,
  options?: StorageOptions
): UseStorageReturn<T> {
  const [state, setState] = useState<UseStorageState<T>>({
    value: defaultValue,
    isLoading: true,
    error: null,
    lastUpdated: null,
  });

  const mountedRef = useRef(true);
  const optionsRef = useRef(options);
  optionsRef.current = options;

  // Load initial value
  useEffect(() => {
    mountedRef.current = true;

    const loadValue = async () => {
      const result = await StorageService.get<T>(key);

      if (!mountedRef.current) return;

      if (result.success) {
        setState({
          value: result.data ?? defaultValue,
          isLoading: false,
          error: null,
          lastUpdated: Date.now(),
        });
      } else {
        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: result.error.message,
        }));
      }
    };

    loadValue();

    return () => {
      mountedRef.current = false;
    };
  }, [key, defaultValue]);

  // Set new value with auto-persist
  const setValue = useCallback(
    async (newValue: T): Promise<void> => {
      // Optimistic update
      setState((prev) => ({
        ...prev,
        value: newValue,
        isLoading: true,
        error: null,
      }));

      const result = await StorageService.set(key, newValue, optionsRef.current);

      if (!mountedRef.current) return;

      if (result.success) {
        setState((prev) => ({
          ...prev,
          isLoading: false,
          lastUpdated: Date.now(),
        }));
      } else {
        // Rollback on error
        const currentResult = await StorageService.get<T>(key);
        setState((prev) => ({
          ...prev,
          value: currentResult.success ? (currentResult.data ?? defaultValue) : prev.value,
          isLoading: false,
          error: result.error.message,
        }));
      }
    },
    [key, defaultValue]
  );

  // Refresh value from storage
  const refresh = useCallback(async (): Promise<void> => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    const result = await StorageService.get<T>(key);

    if (!mountedRef.current) return;

    if (result.success) {
      setState({
        value: result.data ?? defaultValue,
        isLoading: false,
        error: null,
        lastUpdated: Date.now(),
      });
    } else {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: result.error.message,
      }));
    }
  }, [key, defaultValue]);

  // Clear storage for this key
  const clear = useCallback(async (): Promise<void> => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    const result = await StorageService.delete(key);

    if (!mountedRef.current) return;

    if (result.success) {
      setState({
        value: defaultValue,
        isLoading: false,
        error: null,
        lastUpdated: Date.now(),
      });
    } else {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: result.error.message,
      }));
    }
  }, [key, defaultValue]);

  // Update value based on current state
  const update = useCallback(
    async (updater: (current: T | null) => T): Promise<void> => {
      const currentResult = await StorageService.get<T>(key);
      const currentValue = currentResult.success ? currentResult.data : state.value;
      const newValue = updater(currentValue);
      await setValue(newValue);
    },
    [key, state.value, setValue]
  );

  return {
    ...state,
    setValue,
    refresh,
    clear,
    update,
  };
}

/**
 * Hook for multiple storage keys at once
 */
export function useMultiStorage<T extends Record<string, unknown>>(
  keys: Array<keyof T & string>,
  defaults?: Partial<T>
): {
  values: Partial<T>;
  isLoading: boolean;
  errors: Partial<Record<keyof T, string>>;
  setValue: <K extends keyof T>(key: K, value: T[K]) => Promise<void>;
  refresh: () => Promise<void>;
  clearAll: () => Promise<void>;
} {
  const [values, setValues] = useState<Partial<T>>(defaults ?? {});
  const [isLoading, setIsLoading] = useState(true);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const mountedRef = useRef(true);

  useEffect(() => {
    mountedRef.current = true;

    const loadValues = async () => {
      const result = await StorageService.getMultiple<unknown>(keys);

      if (!mountedRef.current) return;

      if (result.success) {
        const loaded: Partial<T> = { ...defaults };
        result.data.forEach((value, key) => {
          if (value !== null) {
            (loaded as Record<string, unknown>)[key] = value;
          }
        });
        setValues(loaded);
      }

      setIsLoading(false);
    };

    loadValues();

    return () => {
      mountedRef.current = false;
    };
  }, [keys.join(','), defaults]);

  const setValue = useCallback(async <K extends keyof T>(key: K, value: T[K]): Promise<void> => {
    setValues((prev) => ({ ...prev, [key]: value }));

    const result = await StorageService.set(key as string, value);

    if (!mountedRef.current) return;

    if (!result.success) {
      setErrors((prev) => ({ ...prev, [key]: result.error.message }));
    }
  }, []);

  const refresh = useCallback(async (): Promise<void> => {
    setIsLoading(true);
    const result = await StorageService.getMultiple<unknown>(keys);

    if (!mountedRef.current) return;

    if (result.success) {
      const loaded: Partial<T> = { ...defaults };
      result.data.forEach((value, key) => {
        if (value !== null) {
          (loaded as Record<string, unknown>)[key] = value;
        }
      });
      setValues(loaded);
      setErrors({});
    }

    setIsLoading(false);
  }, [keys, defaults]);

  const clearAll = useCallback(async (): Promise<void> => {
    setIsLoading(true);

    const result = await StorageService.deleteMultiple(keys);

    if (!mountedRef.current) return;

    if (result.success) {
      setValues(defaults ?? {});
      setErrors({});
    }

    setIsLoading(false);
  }, [keys, defaults]);

  return {
    values,
    isLoading,
    errors,
    setValue,
    refresh,
    clearAll,
  };
}

/**
 * Hook for boolean flags (feature flags, preferences)
 */
export function useStorageFlag(key: string, defaultValue = false): {
  value: boolean;
  isLoading: boolean;
  toggle: () => Promise<void>;
  setFlag: (value: boolean) => Promise<void>;
} {
  const { value, isLoading, setValue } = useStorage<boolean>(key, defaultValue);

  const toggle = useCallback(async () => {
    await setValue(!value);
  }, [value, setValue]);

  const setFlag = useCallback(
    async (newValue: boolean) => {
      await setValue(newValue);
    },
    [setValue]
  );

  return {
    value: value ?? defaultValue,
    isLoading,
    toggle,
    setFlag,
  };
}

/**
 * Hook for numeric counters (streaks, counts)
 */
export function useStorageCounter(key: string, initialValue = 0): {
  count: number;
  isLoading: boolean;
  increment: (by?: number) => Promise<void>;
  decrement: (by?: number) => Promise<void>;
  reset: () => Promise<void>;
  set: (value: number) => Promise<void>;
} {
  const { value, isLoading, setValue } = useStorage<number>(key, initialValue);

  const count = value ?? initialValue;

  const increment = useCallback(
    async (by = 1) => {
      await setValue(count + by);
    },
    [count, setValue]
  );

  const decrement = useCallback(
    async (by = 1) => {
      await setValue(Math.max(0, count - by));
    },
    [count, setValue]
  );

  const reset = useCallback(async () => {
    await setValue(initialValue);
  }, [initialValue, setValue]);

  const set = useCallback(
    async (newValue: number) => {
      await setValue(newValue);
    },
    [setValue]
  );

  return {
    count,
    isLoading,
    increment,
    decrement,
    reset,
    set,
  };
}

/**
 * Hook for arrays (lists, history)
 */
export function useStorageArray<T>(key: string, maxItems?: number): {
  items: T[];
  isLoading: boolean;
  push: (item: T) => Promise<void>;
  remove: (index: number) => Promise<void>;
  removeByValue: (item: T) => Promise<void>;
  clear: () => Promise<void>;
  setItems: (items: T[]) => Promise<void>;
} {
  const { value, isLoading, setValue, clear } = useStorage<T[]>(key, []);

  const items = value ?? [];

  const push = useCallback(
    async (item: T) => {
      let newItems = [...items, item];
      if (maxItems && newItems.length > maxItems) {
        newItems = newItems.slice(-maxItems);
      }
      await setValue(newItems);
    },
    [items, maxItems, setValue]
  );

  const remove = useCallback(
    async (index: number) => {
      const newItems = [...items];
      newItems.splice(index, 1);
      await setValue(newItems);
    },
    [items, setValue]
  );

  const removeByValue = useCallback(
    async (item: T) => {
      const newItems = items.filter((i) => i !== item);
      await setValue(newItems);
    },
    [items, setValue]
  );

  const setItems = useCallback(
    async (newItems: T[]) => {
      let finalItems = newItems;
      if (maxItems && finalItems.length > maxItems) {
        finalItems = finalItems.slice(-maxItems);
      }
      await setValue(finalItems);
    },
    [maxItems, setValue]
  );

  return {
    items,
    isLoading,
    push,
    remove,
    removeByValue,
    clear,
    setItems,
  };
}
