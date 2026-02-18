/**
 * RemoteConfigProvider
 *
 * React context provider for feature flags and remote configuration.
 * Wraps the app to provide flag access throughout the component tree.
 */

import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  useMemo,
  useRef,
} from 'react';
import type { FlagName, FlagValueMap } from './flags';
import type {
  FeatureFlagConfig,
  FeatureFlagContext,
  FlagValue,
  UserAttributes,
} from './types';
import { featureFlagService } from './FeatureFlagService';
import { DEFAULT_FLAG_VALUES, getDefaultValue } from './flags';

// Context value type
interface RemoteConfigContextValue {
  // State
  isReady: boolean;
  isLoading: boolean;
  error: Error | null;

  // Flag access
  getFlag: <T extends FlagName>(flagName: T, defaultValue?: FlagValueMap[T]) => FlagValueMap[T];
  getAllFlags: () => Partial<FlagValueMap>;

  // User identification
  identify: (userId: string, attributes?: UserAttributes) => Promise<void>;
  reset: () => Promise<void>;

  // Refresh
  refresh: () => Promise<void>;
  lastRefresh: number | undefined;
}

// Create context
const RemoteConfigContext = createContext<RemoteConfigContextValue | null>(null);

// Provider props
interface RemoteConfigProviderProps {
  children: React.ReactNode;
  config: FeatureFlagConfig;
  onReady?: () => void;
  onError?: (error: Error) => void;
  LoadingComponent?: React.ReactNode;
  ErrorComponent?: React.FC<{ error: Error; retry: () => void }>;
}

/**
 * RemoteConfigProvider component
 *
 * Wrap your app with this provider to enable feature flags throughout.
 *
 * @example
 * ```tsx
 * <RemoteConfigProvider
 *   config={{
 *     provider: 'launchdarkly',
 *     providerConfig: { mobileKey: 'mob-xxx' }
 *   }}
 * >
 *   <App />
 * </RemoteConfigProvider>
 * ```
 */
export function RemoteConfigProvider({
  children,
  config,
  onReady,
  onError,
  LoadingComponent,
  ErrorComponent,
}: RemoteConfigProviderProps): JSX.Element {
  const [isReady, setIsReady] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [lastRefresh, setLastRefresh] = useState<number | undefined>();
  const [flags, setFlags] = useState<Partial<FlagValueMap>>(() => ({ ...DEFAULT_FLAG_VALUES }));
  const initAttempted = useRef(false);

  // Initialize the service
  const initialize = useCallback(async () => {
    if (initAttempted.current) return;
    initAttempted.current = true;

    setIsLoading(true);
    setError(null);

    try {
      await featureFlagService.initialize({
        ...config,
        onError: (err) => {
          setError(err);
          onError?.(err);
          config.onError?.(err);
        },
      });

      // Fetch all flags after initialization
      const allFlags = await featureFlagService.getAllFlags();
      setFlags(allFlags);
      setLastRefresh(Date.now());

      setIsReady(true);
      onReady?.();
    } catch (err) {
      const error = err as Error;
      setError(error);
      onError?.(error);
      // Still set ready to allow app to function with defaults
      setIsReady(true);
    } finally {
      setIsLoading(false);
    }
  }, [config, onReady, onError]);

  useEffect(() => {
    initialize();

    // Subscribe to flag changes
    const unsubscribe = featureFlagService.onFlagChange((flagName, _oldValue, newValue) => {
      setFlags((prev) => ({
        ...prev,
        [flagName]: newValue,
      }));
    });

    // Cleanup on unmount
    return () => {
      unsubscribe();
    };
  }, [initialize]);

  // Handle app state changes (foreground/background)
  useEffect(() => {
    if (!config.refreshOnForeground) return;

    // In React Native, you would use AppState here
    // For web, we can use visibilitychange
    const handleVisibilityChange = () => {
      if (typeof document !== 'undefined' && document.visibilityState === 'visible') {
        featureFlagService.refreshFlags().catch(console.error);
      }
    };

    if (typeof document !== 'undefined') {
      document.addEventListener('visibilitychange', handleVisibilityChange);
      return () => {
        document.removeEventListener('visibilitychange', handleVisibilityChange);
      };
    }
  }, [config.refreshOnForeground]);

  // Handle network reconnection
  useEffect(() => {
    if (!config.refreshOnReconnect) return;

    const handleOnline = () => {
      featureFlagService.refreshFlags().catch(console.error);
    };

    if (typeof window !== 'undefined') {
      window.addEventListener('online', handleOnline);
      return () => {
        window.removeEventListener('online', handleOnline);
      };
    }
  }, [config.refreshOnReconnect]);

  // Context methods
  const getFlag = useCallback(
    <T extends FlagName>(flagName: T, defaultValue?: FlagValueMap[T]): FlagValueMap[T] => {
      const cached = flags[flagName];
      if (cached !== undefined) {
        return cached as FlagValueMap[T];
      }
      return featureFlagService.getFlag(flagName, defaultValue ?? getDefaultValue(flagName));
    },
    [flags]
  );

  const getAllFlags = useCallback((): Partial<FlagValueMap> => {
    return { ...flags };
  }, [flags]);

  const identify = useCallback(async (userId: string, attributes?: UserAttributes) => {
    await featureFlagService.identify(userId, attributes);
    // Refresh flags after identification
    const allFlags = await featureFlagService.getAllFlags();
    setFlags(allFlags);
  }, []);

  const reset = useCallback(async () => {
    await featureFlagService.reset();
    setFlags({ ...DEFAULT_FLAG_VALUES });
  }, []);

  const refresh = useCallback(async () => {
    setIsLoading(true);
    try {
      await featureFlagService.refreshFlags();
      const allFlags = await featureFlagService.getAllFlags();
      setFlags(allFlags);
      setLastRefresh(Date.now());
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Build context value
  const contextValue = useMemo<RemoteConfigContextValue>(
    () => ({
      isReady,
      isLoading,
      error,
      getFlag,
      getAllFlags,
      identify,
      reset,
      refresh,
      lastRefresh,
    }),
    [isReady, isLoading, error, getFlag, getAllFlags, identify, reset, refresh, lastRefresh]
  );

  // Show loading state
  if (!isReady && isLoading && LoadingComponent) {
    return <>{LoadingComponent}</>;
  }

  // Show error state
  if (error && ErrorComponent && !isReady) {
    return <ErrorComponent error={error} retry={initialize} />;
  }

  return (
    <RemoteConfigContext.Provider value={contextValue}>
      {children}
    </RemoteConfigContext.Provider>
  );
}

/**
 * Hook to access the remote config context
 */
export function useRemoteConfigContext(): RemoteConfigContextValue {
  const context = useContext(RemoteConfigContext);

  if (!context) {
    throw new Error('useRemoteConfigContext must be used within a RemoteConfigProvider');
  }

  return context;
}

/**
 * Consumer component for class-based components
 */
export const RemoteConfigConsumer = RemoteConfigContext.Consumer;

/**
 * Feature gate component for conditional rendering
 */
interface FeatureGateProps {
  flag: FlagName;
  children: React.ReactNode;
  fallback?: React.ReactNode;
  showLoading?: boolean;
}

export function FeatureGate({
  flag,
  children,
  fallback = null,
  showLoading = false,
}: FeatureGateProps): JSX.Element | null {
  const { getFlag, isLoading } = useRemoteConfigContext();
  const isEnabled = getFlag(flag);

  if (isLoading && showLoading) {
    return null; // Or a loading spinner
  }

  if (isEnabled) {
    return <>{children}</>;
  }

  return <>{fallback}</>;
}

/**
 * Config value component for displaying remote config values
 */
interface ConfigValueProps<T extends FlagName> {
  configKey: T;
  children: (value: FlagValueMap[T]) => React.ReactNode;
  defaultValue?: FlagValueMap[T];
}

export function ConfigValue<T extends FlagName>({
  configKey,
  children,
  defaultValue,
}: ConfigValueProps<T>): JSX.Element {
  const { getFlag } = useRemoteConfigContext();
  const value = getFlag(configKey, defaultValue);

  return <>{children(value)}</>;
}

/**
 * Error boundary for feature flag failures
 */
interface FlagErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

interface FlagErrorBoundaryProps {
  children: React.ReactNode;
  fallback: React.ReactNode;
}

export class FlagErrorBoundary extends React.Component<
  FlagErrorBoundaryProps,
  FlagErrorBoundaryState
> {
  constructor(props: FlagErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): FlagErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    console.error('Feature flag error:', error, errorInfo);
  }

  render(): React.ReactNode {
    if (this.state.hasError) {
      return this.props.fallback;
    }

    return this.props.children;
  }
}

// Export context for testing
export { RemoteConfigContext };
