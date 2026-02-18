/**
 * useDeepLinks.ts
 * React hooks for deep link handling in React Native apps
 */

import { useEffect, useState, useCallback, useRef } from 'react';
import { AppState, AppStateStatus, Linking } from 'react-native';

import { deepLinkService, NavigationCallback } from './DeepLinkService';
import type {
  ParsedDeepLink,
  AttributionData,
  DeepLinkServiceConfig,
  ShareLinkParams,
  ReferralLinkData,
} from './types';

/**
 * Options for useDeepLinks hook
 */
export interface UseDeepLinksOptions {
  /** Service configuration */
  config: DeepLinkServiceConfig;
  /** Navigation callback for routing */
  onNavigate: NavigationCallback;
  /** Called when a deep link is received */
  onDeepLinkReceived?: (link: ParsedDeepLink) => void;
  /** Called when deep link processing fails */
  onError?: (error: Error) => void;
  /** Called when attribution is captured */
  onAttribution?: (attribution: AttributionData) => void;
  /** Whether user is authenticated */
  isAuthenticated?: boolean;
  /** Whether user has premium access */
  isPremium?: boolean;
}

/**
 * Return value from useDeepLinks hook
 */
export interface UseDeepLinksReturn {
  /** Whether service is initialized */
  isInitialized: boolean;
  /** Whether initialization is in progress */
  isLoading: boolean;
  /** Last received deep link */
  lastDeepLink: ParsedDeepLink | null;
  /** Pending deep link waiting for auth */
  pendingDeepLink: ParsedDeepLink | null;
  /** Install attribution data */
  installAttribution: AttributionData | null;
  /** Manually process a URL */
  processUrl: (url: string) => Promise<ParsedDeepLink>;
  /** Generate a share link */
  generateShareLink: (params: ShareLinkParams) => Promise<string>;
  /** Clear pending deep link */
  clearPendingDeepLink: () => Promise<void>;
  /** Process pending deep link after auth */
  processPendingDeepLink: () => Promise<boolean>;
  /** Initialization error if any */
  error: Error | null;
}

/**
 * Main hook for deep link handling
 *
 * @example
 * ```tsx
 * import { useDeepLinks } from './deeplinks';
 *
 * function App() {
 *   const navigation = useNavigation();
 *
 *   const {
 *     isInitialized,
 *     pendingDeepLink,
 *     installAttribution,
 *   } = useDeepLinks({
 *     config: {
 *       appId: 'prayerlock',
 *       routes: [
 *         { pattern: '/prayer/:id', screen: 'PrayerDetail', authRequired: false },
 *         { pattern: '/streak', screen: 'StreakView', authRequired: true },
 *       ],
 *       fallbackScreen: 'Home',
 *       debug: __DEV__,
 *     },
 *     onNavigate: (screen, params, stack) => {
 *       if (stack) {
 *         navigation.navigate(stack, { screen, params });
 *       } else {
 *         navigation.navigate(screen, params);
 *       }
 *     },
 *     onDeepLinkReceived: (link) => {
 *       analytics.track('deep_link_received', { url: link.url });
 *     },
 *     isAuthenticated: user !== null,
 *   });
 *
 *   // Handle pending deep link after login
 *   useEffect(() => {
 *     if (isAuthenticated && pendingDeepLink) {
 *       processPendingDeepLink();
 *     }
 *   }, [isAuthenticated, pendingDeepLink]);
 *
 *   return <NavigationContainer>{...}</NavigationContainer>;
 * }
 * ```
 */
export function useDeepLinks(options: UseDeepLinksOptions): UseDeepLinksReturn {
  const {
    config,
    onNavigate,
    onDeepLinkReceived,
    onError,
    onAttribution,
    isAuthenticated,
    isPremium,
  } = options;

  const [isInitialized, setIsInitialized] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [lastDeepLink, setLastDeepLink] = useState<ParsedDeepLink | null>(null);
  const [pendingDeepLink, setPendingDeepLink] = useState<ParsedDeepLink | null>(
    null
  );
  const [installAttribution, setInstallAttribution] =
    useState<AttributionData | null>(null);
  const [error, setError] = useState<Error | null>(null);

  // Track mount state
  const isMountedRef = useRef(true);

  // Initialize service
  useEffect(() => {
    const initialize = async () => {
      try {
        setIsLoading(true);
        await deepLinkService.initialize(config);

        // Set navigation callback
        deepLinkService.setNavigationCallback(onNavigate);

        if (isMountedRef.current) {
          setIsInitialized(true);
          setInstallAttribution(deepLinkService.getInstallAttribution());
          setPendingDeepLink(deepLinkService.getPendingDeepLink());

          // Notify about install attribution if captured
          const attribution = deepLinkService.getInstallAttribution();
          if (attribution) {
            onAttribution?.(attribution);
          }
        }
      } catch (err) {
        const error = err instanceof Error ? err : new Error(String(err));
        if (isMountedRef.current) {
          setError(error);
          onError?.(error);
        }
      } finally {
        if (isMountedRef.current) {
          setIsLoading(false);
        }
      }
    };

    initialize();

    return () => {
      isMountedRef.current = false;
    };
  }, [config, onNavigate, onError, onAttribution]);

  // Handle app state changes for deep links received while backgrounded
  useEffect(() => {
    const handleAppStateChange = async (nextState: AppStateStatus) => {
      if (nextState === 'active') {
        // Check for new deep links when app becomes active
        const url = await Linking.getInitialURL();
        if (url && isInitialized) {
          const parsed = await deepLinkService.processUrl(url, 'background');
          if (parsed.isValid) {
            setLastDeepLink(parsed);
            onDeepLinkReceived?.(parsed);
          }
        }
      }
    };

    const subscription = AppState.addEventListener(
      'change',
      handleAppStateChange
    );

    return () => {
      subscription.remove();
    };
  }, [isInitialized, onDeepLinkReceived]);

  // Process pending deep link when auth state changes
  useEffect(() => {
    const processPending = async () => {
      if (isAuthenticated && pendingDeepLink && isInitialized) {
        const processed = await deepLinkService.processPendingDeepLink();
        if (processed) {
          setPendingDeepLink(null);
        }
      }
    };

    processPending();
  }, [isAuthenticated, pendingDeepLink, isInitialized]);

  // Manual URL processing
  const processUrl = useCallback(
    async (url: string): Promise<ParsedDeepLink> => {
      const parsed = await deepLinkService.processUrl(url, 'foreground');
      if (parsed.isValid) {
        setLastDeepLink(parsed);
        onDeepLinkReceived?.(parsed);
      }
      return parsed;
    },
    [onDeepLinkReceived]
  );

  // Generate share link
  const generateShareLink = useCallback(
    async (params: ShareLinkParams): Promise<string> => {
      return deepLinkService.generateShareLink(params);
    },
    []
  );

  // Clear pending deep link
  const clearPendingDeepLink = useCallback(async (): Promise<void> => {
    await deepLinkService.clearPendingDeepLink();
    setPendingDeepLink(null);
  }, []);

  // Process pending deep link
  const processPendingDeepLink = useCallback(async (): Promise<boolean> => {
    const processed = await deepLinkService.processPendingDeepLink();
    if (processed) {
      setPendingDeepLink(null);
    }
    return processed;
  }, []);

  return {
    isInitialized,
    isLoading,
    lastDeepLink,
    pendingDeepLink,
    installAttribution,
    processUrl,
    generateShareLink,
    clearPendingDeepLink,
    processPendingDeepLink,
    error,
  };
}

/**
 * Hook for subscribing to deep link events
 *
 * @example
 * ```tsx
 * function DeepLinkHandler() {
 *   useDeepLinkListener({
 *     onReceive: (link) => {
 *       console.log('Received:', link.url);
 *     },
 *     onRoute: (link, route) => {
 *       analytics.track('deep_link_routed', { screen: route.screen });
 *     },
 *   });
 *
 *   return null;
 * }
 * ```
 */
export interface DeepLinkListenerOptions {
  /** Called when deep link is received */
  onReceive?: (link: ParsedDeepLink) => void;
  /** Called when link requires auth */
  onAuthRequired?: (link: ParsedDeepLink) => void;
  /** Called when link requires premium */
  onPremiumRequired?: (link: ParsedDeepLink) => void;
  /** Called on error */
  onError?: (error: Error, url: string) => void;
}

export function useDeepLinkListener(options: DeepLinkListenerOptions): void {
  const { onReceive, onAuthRequired, onPremiumRequired, onError } = options;

  useEffect(() => {
    const subscription = Linking.addEventListener('url', async ({ url }) => {
      try {
        const parsed = deepLinkService.parseUrl(url);

        if (parsed.isValid) {
          onReceive?.(parsed);
        } else if (parsed.error) {
          onError?.(new Error(parsed.error), url);
        }
      } catch (err) {
        const error = err instanceof Error ? err : new Error(String(err));
        onError?.(error, url);
      }
    });

    return () => {
      subscription.remove();
    };
  }, [onReceive, onAuthRequired, onPremiumRequired, onError]);
}

/**
 * Hook for generating share links
 *
 * @example
 * ```tsx
 * function ShareButton({ prayerId }) {
 *   const { generateLink, isGenerating, link, error } = useShareLink();
 *
 *   const handleShare = async () => {
 *     const url = await generateLink({
 *       action: 'prayer',
 *       resourceId: prayerId,
 *       campaign: 'in_app_share',
 *     });
 *
 *     await Share.share({ url });
 *   };
 *
 *   return (
 *     <Button onPress={handleShare} disabled={isGenerating}>
 *       Share
 *     </Button>
 *   );
 * }
 * ```
 */
export interface UseShareLinkReturn {
  /** Generate a share link */
  generateLink: (params: ShareLinkParams) => Promise<string>;
  /** Whether link generation is in progress */
  isGenerating: boolean;
  /** Last generated link */
  link: string | null;
  /** Error if generation failed */
  error: Error | null;
}

export function useShareLink(): UseShareLinkReturn {
  const [isGenerating, setIsGenerating] = useState(false);
  const [link, setLink] = useState<string | null>(null);
  const [error, setError] = useState<Error | null>(null);

  const generateLink = useCallback(
    async (params: ShareLinkParams): Promise<string> => {
      try {
        setIsGenerating(true);
        setError(null);

        const generatedLink = await deepLinkService.generateShareLink(params);
        setLink(generatedLink);
        return generatedLink;
      } catch (err) {
        const error = err instanceof Error ? err : new Error(String(err));
        setError(error);
        throw error;
      } finally {
        setIsGenerating(false);
      }
    },
    []
  );

  return {
    generateLink,
    isGenerating,
    link,
    error,
  };
}

/**
 * Hook for accessing install attribution
 *
 * @example
 * ```tsx
 * function AnalyticsProvider({ children }) {
 *   const attribution = useInstallAttribution();
 *
 *   useEffect(() => {
 *     if (attribution) {
 *       analytics.setUserProperties({
 *         install_source: attribution.utmSource,
 *         install_campaign: attribution.campaign,
 *       });
 *     }
 *   }, [attribution]);
 *
 *   return children;
 * }
 * ```
 */
export function useInstallAttribution(): AttributionData | null {
  const [attribution, setAttribution] = useState<AttributionData | null>(
    deepLinkService.getInstallAttribution()
  );

  useEffect(() => {
    // Re-check on mount in case service initialized after initial render
    const attr = deepLinkService.getInstallAttribution();
    if (attr && !attribution) {
      setAttribution(attr);
    }
  }, [attribution]);

  return attribution;
}

/**
 * Hook for handling pending deep links after authentication
 *
 * @example
 * ```tsx
 * function AuthenticatedApp() {
 *   const { hasPending, pending, process, clear } = usePendingDeepLink();
 *
 *   useEffect(() => {
 *     if (hasPending) {
 *       // Show a prompt or auto-process
 *       Alert.alert(
 *         'Pending Action',
 *         'You have a pending action from a deep link. Process now?',
 *         [
 *           { text: 'Cancel', onPress: clear },
 *           { text: 'Continue', onPress: process },
 *         ]
 *       );
 *     }
 *   }, [hasPending]);
 *
 *   return <MainApp />;
 * }
 * ```
 */
export interface UsePendingDeepLinkReturn {
  /** Whether there's a pending deep link */
  hasPending: boolean;
  /** The pending deep link data */
  pending: ParsedDeepLink | null;
  /** Process the pending deep link */
  process: () => Promise<boolean>;
  /** Clear the pending deep link */
  clear: () => Promise<void>;
}

export function usePendingDeepLink(): UsePendingDeepLinkReturn {
  const [pending, setPending] = useState<ParsedDeepLink | null>(
    deepLinkService.getPendingDeepLink()
  );

  const process = useCallback(async (): Promise<boolean> => {
    const processed = await deepLinkService.processPendingDeepLink();
    if (processed) {
      setPending(null);
    }
    return processed;
  }, []);

  const clear = useCallback(async (): Promise<void> => {
    await deepLinkService.clearPendingDeepLink();
    setPending(null);
  }, []);

  return {
    hasPending: pending !== null,
    pending,
    process,
    clear,
  };
}

export default useDeepLinks;
