/**
 * useFeatureFlag Hook
 *
 * React hooks for accessing feature flags in components.
 */

import { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import type { FlagName, FlagValueMap } from './flags';
import type { FeatureFlagContext, FlagEvaluation, FlagValue, UserAttributes } from './types';
import { featureFlagService } from './FeatureFlagService';
import { getDefaultValue } from './flags';

/**
 * Hook to get a single feature flag value
 */
export function useFeatureFlag<T extends FlagName>(
  flagName: T,
  defaultValue?: FlagValueMap[T]
): FlagValueMap[T] {
  const fallback = defaultValue ?? getDefaultValue(flagName);
  const [value, setValue] = useState<FlagValueMap[T]>(() =>
    featureFlagService.getFlag(flagName, fallback)
  );

  useEffect(() => {
    // Get initial value
    setValue(featureFlagService.getFlag(flagName, fallback));

    // Subscribe to changes
    const unsubscribe = featureFlagService.onFlagChange((changedFlag, _oldValue, newValue) => {
      if (changedFlag === flagName) {
        setValue(newValue as FlagValueMap[T]);
      }
    });

    return unsubscribe;
  }, [flagName, fallback]);

  return value;
}

/**
 * Hook to get a boolean feature flag
 */
export function useBooleanFlag(flagName: FlagName, defaultValue = false): boolean {
  return useFeatureFlag(flagName, defaultValue as FlagValueMap[typeof flagName]) as boolean;
}

/**
 * Hook to get a numeric feature flag
 */
export function useNumericFlag(flagName: FlagName, defaultValue = 0): number {
  return useFeatureFlag(flagName, defaultValue as FlagValueMap[typeof flagName]) as number;
}

/**
 * Hook to get a string feature flag
 */
export function useStringFlag(flagName: FlagName, defaultValue = ''): string {
  return useFeatureFlag(flagName, defaultValue as FlagValueMap[typeof flagName]) as string;
}

/**
 * Hook to get a JSON feature flag
 */
export function useJsonFlag<T extends Record<string, unknown>>(
  flagName: FlagName,
  defaultValue: T
): T {
  return useFeatureFlag(flagName, defaultValue as FlagValueMap[typeof flagName]) as T;
}

/**
 * Hook to get flag evaluation details
 */
export function useFlagEvaluation<T extends FlagName>(
  flagName: T,
  defaultValue?: FlagValueMap[T]
): FlagEvaluation<FlagValueMap[T]> {
  const fallback = defaultValue ?? getDefaultValue(flagName);
  const [evaluation, setEvaluation] = useState<FlagEvaluation<FlagValueMap[T]>>(() =>
    featureFlagService.getFlagEvaluation(flagName, fallback)
  );

  useEffect(() => {
    setEvaluation(featureFlagService.getFlagEvaluation(flagName, fallback));

    const unsubscribe = featureFlagService.onFlagChange((changedFlag) => {
      if (changedFlag === flagName) {
        setEvaluation(featureFlagService.getFlagEvaluation(flagName, fallback));
      }
    });

    return unsubscribe;
  }, [flagName, fallback]);

  return evaluation;
}

/**
 * Hook to get async flag value (fetches fresh from provider)
 */
export function useAsyncFeatureFlag<T extends FlagName>(
  flagName: T,
  defaultValue?: FlagValueMap[T]
): {
  value: FlagValueMap[T];
  isLoading: boolean;
  error: Error | null;
  refresh: () => Promise<void>;
} {
  const fallback = defaultValue ?? getDefaultValue(flagName);
  const [value, setValue] = useState<FlagValueMap[T]>(fallback);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchFlag = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await featureFlagService.getFlagAsync(flagName, fallback);
      setValue(result);
    } catch (err) {
      setError(err as Error);
    } finally {
      setIsLoading(false);
    }
  }, [flagName, fallback]);

  useEffect(() => {
    fetchFlag();
  }, [fetchFlag]);

  return { value, isLoading, error, refresh: fetchFlag };
}

/**
 * Hook to get multiple flags at once
 */
export function useFeatureFlags<T extends FlagName>(
  flagNames: T[]
): Record<T, FlagValueMap[T]> {
  const [values, setValues] = useState<Record<T, FlagValueMap[T]>>(() => {
    const initial = {} as Record<T, FlagValueMap[T]>;
    for (const name of flagNames) {
      initial[name] = featureFlagService.getFlag(name, getDefaultValue(name));
    }
    return initial;
  });

  useEffect(() => {
    // Update initial values
    const updated = {} as Record<T, FlagValueMap[T]>;
    for (const name of flagNames) {
      updated[name] = featureFlagService.getFlag(name, getDefaultValue(name));
    }
    setValues(updated);

    // Subscribe to changes
    const unsubscribe = featureFlagService.onFlagChange((changedFlag, _oldValue, newValue) => {
      if (flagNames.includes(changedFlag as T)) {
        setValues((prev) => ({
          ...prev,
          [changedFlag]: newValue,
        }));
      }
    });

    return unsubscribe;
  }, [flagNames.join(',')]); // eslint-disable-line react-hooks/exhaustive-deps

  return values;
}

/**
 * Hook to get feature flag service context
 */
export function useFeatureFlagContext(): FeatureFlagContext {
  const [context, setContext] = useState<FeatureFlagContext>(() =>
    featureFlagService.getContext()
  );

  useEffect(() => {
    // Poll for context changes (simple approach)
    const interval = setInterval(() => {
      setContext(featureFlagService.getContext());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return context;
}

/**
 * Hook to identify a user
 */
export function useIdentifyUser(): {
  identify: (userId: string, attributes?: UserAttributes) => Promise<void>;
  reset: () => Promise<void>;
  isIdentified: boolean;
} {
  const [isIdentified, setIsIdentified] = useState(false);

  const identify = useCallback(async (userId: string, attributes?: UserAttributes) => {
    await featureFlagService.identify(userId, attributes);
    setIsIdentified(true);
  }, []);

  const reset = useCallback(async () => {
    await featureFlagService.reset();
    setIsIdentified(false);
  }, []);

  return { identify, reset, isIdentified };
}

/**
 * Hook to refresh flags manually
 */
export function useRefreshFlags(): {
  refresh: () => Promise<void>;
  isRefreshing: boolean;
  lastRefresh: number | undefined;
} {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [lastRefresh, setLastRefresh] = useState<number | undefined>(
    featureFlagService.getContext().lastRefresh
  );

  const refresh = useCallback(async () => {
    setIsRefreshing(true);
    try {
      await featureFlagService.refreshFlags();
      setLastRefresh(Date.now());
    } finally {
      setIsRefreshing(false);
    }
  }, []);

  return { refresh, isRefreshing, lastRefresh };
}

/**
 * Hook for conditional rendering based on flag
 */
export function useFeatureGate(flagName: FlagName): {
  isEnabled: boolean;
  isLoading: boolean;
} {
  const context = useFeatureFlagContext();
  const value = useFeatureFlag(flagName);

  return {
    isEnabled: Boolean(value),
    isLoading: context.isLoading,
  };
}

/**
 * Hook for remote config values with type inference
 */
export function useRemoteConfig<T extends FlagName>(
  configKey: T
): {
  value: FlagValueMap[T];
  source: 'default' | 'remote' | 'cache';
  isLoading: boolean;
} {
  const evaluation = useFlagEvaluation(configKey);
  const context = useFeatureFlagContext();

  const source = useMemo(() => {
    if (evaluation.source === 'provider') return 'remote' as const;
    if (evaluation.source === 'cache') return 'cache' as const;
    return 'default' as const;
  }, [evaluation.source]);

  return {
    value: evaluation.value,
    source,
    isLoading: context.isLoading,
  };
}

/**
 * Hook for tracking flag changes
 */
export function useOnFlagChange(
  callback: (flagName: FlagName, oldValue: FlagValue, newValue: FlagValue) => void
): void {
  const callbackRef = useRef(callback);
  callbackRef.current = callback;

  useEffect(() => {
    const unsubscribe = featureFlagService.onFlagChange((flagName, oldValue, newValue) => {
      callbackRef.current(flagName, oldValue, newValue);
    });

    return unsubscribe;
  }, []);
}

/**
 * HOC for feature-gated components
 */
export function withFeatureFlag<P extends object>(
  Component: React.ComponentType<P>,
  flagName: FlagName,
  FallbackComponent?: React.ComponentType<P>
): React.FC<P> {
  return function FeatureGatedComponent(props: P) {
    const { isEnabled, isLoading } = useFeatureGate(flagName);

    if (isLoading) {
      return null; // Or a loading component
    }

    if (!isEnabled) {
      return FallbackComponent ? <FallbackComponent {...props} /> : null;
    }

    return <Component {...props} />;
  };
}
