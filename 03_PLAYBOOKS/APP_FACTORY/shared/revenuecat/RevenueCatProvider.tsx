/**
 * RevenueCat Context Provider
 * Provides subscription state and customer info throughout the app
 */

import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  useMemo,
  type ReactNode,
} from 'react';
import { Platform } from 'react-native';
import Purchases, {
  LOG_LEVEL,
  CustomerInfo,
  PurchasesOfferings,
  PurchasesOffering,
} from 'react-native-purchases';

import type {
  RevenueCatContextValue,
  SubscriptionStatus,
  OfferingsState,
  AppConfig,
} from './types';
import {
  getApiKey,
  getLogLevel,
  isValidApiKey,
  FEATURE_FLAGS,
  TIMEOUTS,
  DEFAULT_ENTITLEMENT_ID,
} from './config';
import { parseSubscriptionStatus, withTimeout, withRetry } from './utils';

/**
 * Default context value
 */
const defaultContextValue: RevenueCatContextValue = {
  isInitialized: false,
  customerInfo: null,
  subscriptionStatus: {
    isActive: false,
    isInTrial: false,
    willRenew: false,
    expirationDate: null,
    periodType: 'none',
    activeProductId: null,
    entitlementId: null,
  },
  offerings: {
    current: null,
    all: {},
    isLoading: true,
    error: null,
  },
  refreshCustomerInfo: async () => {},
  refreshOfferings: async () => {},
};

/**
 * RevenueCat Context
 */
const RevenueCatContext = createContext<RevenueCatContextValue>(defaultContextValue);

/**
 * Provider props
 */
interface RevenueCatProviderProps {
  /** App configuration */
  config: AppConfig;
  /** Child components */
  children: ReactNode;
  /** Optional user ID for identification */
  userId?: string;
  /** Called when initialization completes */
  onInitialized?: () => void;
  /** Called on initialization error */
  onError?: (error: Error) => void;
}

/**
 * RevenueCat Provider Component
 *
 * Wraps your app to provide subscription state management.
 *
 * @example
 * ```tsx
 * import { RevenueCatProvider, getAppConfig } from './revenuecat';
 *
 * function App() {
 *   return (
 *     <RevenueCatProvider config={getAppConfig('prayerlock')}>
 *       <YourApp />
 *     </RevenueCatProvider>
 *   );
 * }
 * ```
 */
export function RevenueCatProvider({
  config,
  children,
  userId,
  onInitialized,
  onError,
}: RevenueCatProviderProps): JSX.Element {
  const [isInitialized, setIsInitialized] = useState(false);
  const [customerInfo, setCustomerInfo] = useState<CustomerInfo | null>(null);
  const [offerings, setOfferings] = useState<OfferingsState>({
    current: null,
    all: {},
    isLoading: true,
    error: null,
  });

  /**
   * Initialize RevenueCat SDK
   */
  const initializeSDK = useCallback(async () => {
    try {
      const apiKey = getApiKey(config);

      if (!isValidApiKey(apiKey)) {
        throw new Error(
          `Invalid API key for ${config.appId}. Please configure your RevenueCat API key.`
        );
      }

      // Set log level based on environment
      const logLevel = getLogLevel();
      if (logLevel === 'DEBUG') {
        Purchases.setLogLevel(LOG_LEVEL.DEBUG);
      } else if (logLevel === 'VERBOSE') {
        Purchases.setLogLevel(LOG_LEVEL.VERBOSE);
      }

      // Configure SDK with timeout
      await withTimeout(
        Purchases.configure({
          apiKey,
          appUserID: userId || null,
        }),
        TIMEOUTS.initialization,
        'SDK initialization'
      );

      setIsInitialized(true);
      onInitialized?.();

      if (FEATURE_FLAGS.enableDebugLogs) {
        console.log(`[RevenueCat] Initialized for ${config.appId}`);
      }
    } catch (error) {
      const err = error instanceof Error ? error : new Error(String(error));
      console.error('[RevenueCat] Initialization error:', err.message);
      onError?.(err);
    }
  }, [config, userId, onInitialized, onError]);

  /**
   * Fetch customer info
   */
  const fetchCustomerInfo = useCallback(async (): Promise<void> => {
    if (!isInitialized) return;

    try {
      const info = await withRetry(
        () =>
          withTimeout(
            Purchases.getCustomerInfo(),
            TIMEOUTS.customerInfo,
            'Fetch customer info'
          ),
        2
      );

      setCustomerInfo(info);

      if (FEATURE_FLAGS.enableDebugLogs) {
        const status = parseSubscriptionStatus(info, config.entitlementId);
        console.log('[RevenueCat] Customer info updated:', {
          isActive: status.isActive,
          isInTrial: status.isInTrial,
        });
      }
    } catch (error) {
      console.error('[RevenueCat] Error fetching customer info:', error);
    }
  }, [isInitialized, config.entitlementId]);

  /**
   * Fetch offerings
   */
  const fetchOfferings = useCallback(async (): Promise<void> => {
    if (!isInitialized) return;

    setOfferings((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const result = await withRetry(
        () =>
          withTimeout(
            Purchases.getOfferings(),
            TIMEOUTS.offerings,
            'Fetch offerings'
          ),
        2
      );

      setOfferings({
        current: result.current,
        all: result.all,
        isLoading: false,
        error: null,
      });

      if (FEATURE_FLAGS.enableDebugLogs) {
        console.log('[RevenueCat] Offerings fetched:', {
          current: result.current?.identifier,
          packageCount: result.current?.availablePackages.length ?? 0,
        });
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to fetch offerings';

      setOfferings((prev) => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));

      console.error('[RevenueCat] Error fetching offerings:', error);
    }
  }, [isInitialized]);

  /**
   * Customer info update listener
   */
  useEffect(() => {
    if (!isInitialized) return;

    const customerInfoUpdateListener = (info: CustomerInfo) => {
      setCustomerInfo(info);

      if (FEATURE_FLAGS.enableDebugLogs) {
        console.log('[RevenueCat] Customer info updated via listener');
      }
    };

    Purchases.addCustomerInfoUpdateListener(customerInfoUpdateListener);

    return () => {
      Purchases.removeCustomerInfoUpdateListener(customerInfoUpdateListener);
    };
  }, [isInitialized]);

  /**
   * Initialize on mount
   */
  useEffect(() => {
    initializeSDK();
  }, [initializeSDK]);

  /**
   * Fetch data after initialization
   */
  useEffect(() => {
    if (isInitialized) {
      fetchCustomerInfo();
      fetchOfferings();
    }
  }, [isInitialized, fetchCustomerInfo, fetchOfferings]);

  /**
   * Handle user ID changes
   */
  useEffect(() => {
    if (!isInitialized || !userId) return;

    const identifyUser = async () => {
      try {
        const { customerInfo } = await Purchases.logIn(userId);
        setCustomerInfo(customerInfo);

        if (FEATURE_FLAGS.enableDebugLogs) {
          console.log('[RevenueCat] User identified:', userId);
        }
      } catch (error) {
        console.error('[RevenueCat] Error identifying user:', error);
      }
    };

    identifyUser();
  }, [isInitialized, userId]);

  /**
   * Compute subscription status
   */
  const subscriptionStatus = useMemo<SubscriptionStatus>(() => {
    return parseSubscriptionStatus(customerInfo, config.entitlementId);
  }, [customerInfo, config.entitlementId]);

  /**
   * Context value
   */
  const contextValue = useMemo<RevenueCatContextValue>(
    () => ({
      isInitialized,
      customerInfo,
      subscriptionStatus,
      offerings,
      refreshCustomerInfo: fetchCustomerInfo,
      refreshOfferings: fetchOfferings,
    }),
    [
      isInitialized,
      customerInfo,
      subscriptionStatus,
      offerings,
      fetchCustomerInfo,
      fetchOfferings,
    ]
  );

  return (
    <RevenueCatContext.Provider value={contextValue}>
      {children}
    </RevenueCatContext.Provider>
  );
}

/**
 * Hook to access RevenueCat context
 *
 * @returns RevenueCat context value
 * @throws Error if used outside provider
 *
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { subscriptionStatus, offerings } = useRevenueCat();
 *
 *   if (subscriptionStatus.isActive) {
 *     return <PremiumContent />;
 *   }
 *
 *   return <Paywall />;
 * }
 * ```
 */
export function useRevenueCat(): RevenueCatContextValue {
  const context = useContext(RevenueCatContext);

  if (context === undefined) {
    throw new Error('useRevenueCat must be used within a RevenueCatProvider');
  }

  return context;
}

/**
 * Hook to check if SDK is ready
 *
 * @returns Whether SDK is initialized
 */
export function useRevenueCatReady(): boolean {
  const { isInitialized } = useRevenueCat();
  return isInitialized;
}

/**
 * Hook to access customer info directly
 *
 * @returns Customer info or null
 */
export function useCustomerInfo(): CustomerInfo | null {
  const { customerInfo } = useRevenueCat();
  return customerInfo;
}

/**
 * Logout the current user (for use on app logout)
 *
 * @example
 * ```tsx
 * import { logoutRevenueCat } from './revenuecat';
 *
 * async function handleLogout() {
 *   await logoutRevenueCat();
 *   // Continue with app logout
 * }
 * ```
 */
export async function logoutRevenueCat(): Promise<void> {
  try {
    await Purchases.logOut();

    if (FEATURE_FLAGS.enableDebugLogs) {
      console.log('[RevenueCat] User logged out');
    }
  } catch (error) {
    console.error('[RevenueCat] Error logging out:', error);
    throw error;
  }
}

/**
 * Set user attributes for analytics
 *
 * @param attributes - Key-value pairs of attributes
 */
export async function setUserAttributes(
  attributes: Record<string, string>
): Promise<void> {
  try {
    await Purchases.setAttributes(attributes);

    if (FEATURE_FLAGS.enableDebugLogs) {
      console.log('[RevenueCat] User attributes set:', Object.keys(attributes));
    }
  } catch (error) {
    console.error('[RevenueCat] Error setting attributes:', error);
  }
}

/**
 * Set user email for RevenueCat
 *
 * @param email - User email address
 */
export async function setUserEmail(email: string): Promise<void> {
  await setUserAttributes({ $email: email });
}

/**
 * Set user display name for RevenueCat
 *
 * @param displayName - User display name
 */
export async function setUserDisplayName(displayName: string): Promise<void> {
  await setUserAttributes({ $displayName: displayName });
}

export default RevenueCatProvider;
