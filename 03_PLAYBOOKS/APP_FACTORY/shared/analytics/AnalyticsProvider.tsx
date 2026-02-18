/**
 * AnalyticsProvider
 *
 * React Native context provider for analytics.
 * Initializes multiple providers, handles user identification,
 * and manages session tracking.
 */

import React, {
  createContext,
  useContext,
  useEffect,
  useRef,
  useState,
  useCallback,
  ReactNode,
} from 'react';
import { AppState, AppStateStatus, Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { v4 as uuidv4 } from 'uuid';
import DeviceInfo from 'react-native-device-info';

import type {
  AnalyticsConfig,
  AnalyticsContext as AnalyticsContextType,
  SessionData,
  UserTraits,
  UserProperties,
  RevenueData,
} from './types';
import type { AnalyticsEventName, AnalyticsEventMap } from './events';

// Providers
import { initializeMixpanel, mixpanelProvider } from './providers/mixpanel';
import { initializePostHog, posthogProvider } from './providers/posthog';
import { initializeFirebase, firebaseProvider } from './providers/firebase';
import { initializeRevenueCat, revenueCatProvider } from './providers/revenuecat';

// Storage keys
const STORAGE_KEYS = {
  ANONYMOUS_ID: '@analytics/anonymous_id',
  DEVICE_ID: '@analytics/device_id',
  FIRST_LAUNCH_DATE: '@analytics/first_launch_date',
  SESSION_COUNT: '@analytics/session_count',
  LAST_SESSION_END: '@analytics/last_session_end',
  USER_ID: '@analytics/user_id',
  INSTALL_SOURCE: '@analytics/install_source',
};

// Default session timeout (30 minutes)
const DEFAULT_SESSION_TIMEOUT = 30 * 60 * 1000;

// Analytics context interface
interface AnalyticsContextValue {
  // Context data
  context: AnalyticsContextType | null;
  isInitialized: boolean;
  isEnabled: boolean;

  // Core methods
  track: <T extends AnalyticsEventName>(
    event: T,
    properties: AnalyticsEventMap[T]
  ) => Promise<void>;
  identify: (userId: string, traits?: UserTraits) => Promise<void>;
  setUserProperties: (properties: UserProperties) => Promise<void>;
  trackRevenue: (revenue: RevenueData) => Promise<void>;
  reset: () => Promise<void>;
  flush: () => Promise<void>;

  // Session methods
  startSession: () => void;
  endSession: () => void;

  // Settings
  setEnabled: (enabled: boolean) => void;
  setDebug: (debug: boolean) => void;
}

// Create context
const AnalyticsContext = createContext<AnalyticsContextValue | null>(null);

// Provider props
interface AnalyticsProviderProps {
  children: ReactNode;
  config: AnalyticsConfig;
  onInitialized?: () => void;
  onError?: (error: Error) => void;
}

/**
 * Analytics Provider Component
 */
export function AnalyticsProvider({
  children,
  config,
  onInitialized,
  onError,
}: AnalyticsProviderProps): JSX.Element {
  // State
  const [isInitialized, setIsInitialized] = useState(false);
  const [isEnabled, setIsEnabled] = useState(config.enabled ?? true);
  const [context, setContext] = useState<AnalyticsContextType | null>(null);

  // Refs
  const sessionRef = useRef<SessionData | null>(null);
  const appStateRef = useRef<AppStateStatus>(AppState.currentState);
  const debugRef = useRef(config.debug ?? false);
  const sessionTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  /**
   * Initialize all providers
   */
  const initializeProviders = useCallback(async () => {
    try {
      log('Initializing analytics providers...');

      // Get or create IDs
      const [anonymousId, deviceId, firstLaunchDate, sessionCount] = await Promise.all([
        getOrCreateAnonymousId(),
        getOrCreateDeviceId(),
        getFirstLaunchDate(),
        getSessionCount(),
      ]);

      // Get device info
      const appVersion = DeviceInfo.getVersion();
      const buildNumber = DeviceInfo.getBuildNumber();
      const osVersion = DeviceInfo.getSystemVersion();
      const deviceModel = DeviceInfo.getModel();
      const locale = 'en-US'; // Would use i18n library in real app
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

      // Calculate days since install
      const daysSinceInstall = Math.floor(
        (Date.now() - new Date(firstLaunchDate).getTime()) / (1000 * 60 * 60 * 24)
      );

      // Get stored user ID if exists
      const storedUserId = await AsyncStorage.getItem(STORAGE_KEYS.USER_ID);
      const installSource = await AsyncStorage.getItem(STORAGE_KEYS.INSTALL_SOURCE);

      // Create session
      const newSessionNumber = sessionCount + 1;
      await AsyncStorage.setItem(STORAGE_KEYS.SESSION_COUNT, String(newSessionNumber));

      const sessionId = uuidv4();
      const isFirstSession = newSessionNumber === 1;

      // Set context
      const analyticsContext: AnalyticsContextType = {
        anonymousId,
        deviceId,
        sessionId,
        sessionNumber: newSessionNumber,
        appVersion,
        buildNumber,
        platform: Platform.OS as 'ios' | 'android',
        osVersion,
        deviceModel,
        locale,
        timezone,
        isFirstSession,
        daysSinceInstall,
        userId: storedUserId ?? undefined,
        installSource: installSource ?? undefined,
      };

      setContext(analyticsContext);

      // Initialize providers in parallel
      const initPromises: Promise<void>[] = [];

      if (config.providers.mixpanel?.apiKey) {
        initPromises.push(
          initializeMixpanel({
            ...config.providers.mixpanel,
            debug: config.debug,
          })
        );
      }

      if (config.providers.posthog?.apiKey) {
        initPromises.push(
          initializePostHog({
            ...config.providers.posthog,
            debug: config.debug,
          })
        );
      }

      if (config.providers.firebase) {
        initPromises.push(
          initializeFirebase({
            ...config.providers.firebase,
            debug: config.debug,
          })
        );
      }

      if (config.providers.revenuecat?.apiKey) {
        initPromises.push(
          initializeRevenueCat({
            ...config.providers.revenuecat,
            debug: config.debug,
          })
        );
      }

      await Promise.all(initPromises);

      // Set initial super properties
      const superProperties = {
        app_version: appVersion,
        build_number: buildNumber,
        platform: Platform.OS,
        os_version: osVersion,
        device_model: deviceModel,
        days_since_install: daysSinceInstall,
        session_number: newSessionNumber,
      };

      // Set on each provider
      if (config.providers.mixpanel?.apiKey) {
        const { setSuperProperties } = await import('./providers/mixpanel');
        setSuperProperties(superProperties);
      }

      if (config.providers.posthog?.apiKey) {
        const { registerSuperProperties } = await import('./providers/posthog');
        registerSuperProperties(superProperties);
      }

      // Start session
      startNewSession(sessionId, newSessionNumber, isFirstSession);

      setIsInitialized(true);
      log('Analytics initialized successfully');
      onInitialized?.();
    } catch (error) {
      console.error('[Analytics] Initialization failed:', error);
      onError?.(error as Error);
    }
  }, [config, onInitialized, onError]);

  /**
   * Start a new session
   */
  const startNewSession = useCallback(
    (sessionId: string, sessionNumber: number, isFirstSession: boolean) => {
      const session: SessionData = {
        session_id: sessionId,
        started_at: new Date().toISOString(),
        screens_visited: [],
        events: [],
        is_first_session: isFirstSession,
        session_number: sessionNumber,
      };

      sessionRef.current = session;

      // Track session start
      trackToProviders('session_started', {
        session_number: sessionNumber,
        days_since_install: context?.daysSinceInstall ?? 0,
        is_first_session_today: true, // Would check actual date
      });

      log(`Session started: ${sessionId}`);
    },
    [context]
  );

  /**
   * End current session
   */
  const endCurrentSession = useCallback(() => {
    if (!sessionRef.current) return;

    const session = sessionRef.current;
    const now = new Date();
    const startTime = new Date(session.started_at);
    const durationMs = now.getTime() - startTime.getTime();

    // Track session end
    trackToProviders('session_ended', {
      duration_ms: durationMs,
      screens_visited: session.screens_visited.length,
      features_used: [], // Would track actual features
      events_count: session.events.length,
    });

    // Store session end time
    AsyncStorage.setItem(STORAGE_KEYS.LAST_SESSION_END, now.toISOString());

    session.ended_at = now.toISOString();
    session.duration_ms = durationMs;

    log(`Session ended: ${session.session_id}, duration: ${durationMs}ms`);

    // Flush events
    flushAllProviders();
  }, []);

  /**
   * Track event to all providers
   */
  const trackToProviders = useCallback(
    async <T extends AnalyticsEventName>(
      event: T,
      properties: AnalyticsEventMap[T]
    ): Promise<void> => {
      if (!isEnabled) {
        log(`Tracking disabled, skipping: ${event}`);
        return;
      }

      const enrichedProperties = {
        ...properties,
        timestamp: new Date().toISOString(),
        session_id: sessionRef.current?.session_id ?? context?.sessionId,
        user_id: context?.userId,
        app_version: context?.appVersion,
        platform: context?.platform,
      };

      // Track to session
      if (sessionRef.current) {
        sessionRef.current.events.push({
          name: event,
          timestamp: enrichedProperties.timestamp,
        });
      }

      const trackPromises: Promise<void>[] = [];

      if (config.providers.mixpanel?.apiKey) {
        trackPromises.push(
          mixpanelProvider.track(event, enrichedProperties as AnalyticsEventMap[T])
        );
      }

      if (config.providers.posthog?.apiKey) {
        trackPromises.push(
          posthogProvider.track(event, enrichedProperties as AnalyticsEventMap[T])
        );
      }

      if (config.providers.firebase) {
        trackPromises.push(
          firebaseProvider.track(event, enrichedProperties as AnalyticsEventMap[T])
        );
      }

      try {
        await Promise.all(trackPromises);
        log(`Event tracked: ${event}`, enrichedProperties);
      } catch (error) {
        console.error(`[Analytics] Track failed for ${event}:`, error);
      }
    },
    [isEnabled, context, config.providers]
  );

  /**
   * Identify user across all providers
   */
  const identifyUser = useCallback(
    async (userId: string, traits?: UserTraits): Promise<void> => {
      if (!isEnabled || !isInitialized) return;

      // Store user ID
      await AsyncStorage.setItem(STORAGE_KEYS.USER_ID, userId);

      // Update context
      setContext((prev) => (prev ? { ...prev, userId } : null));

      const identifyPromises: Promise<void>[] = [];

      if (config.providers.mixpanel?.apiKey) {
        identifyPromises.push(mixpanelProvider.identify(userId, traits));
      }

      if (config.providers.posthog?.apiKey) {
        identifyPromises.push(posthogProvider.identify(userId, traits));
      }

      if (config.providers.firebase) {
        identifyPromises.push(firebaseProvider.identify(userId, traits));
      }

      if (config.providers.revenuecat?.apiKey) {
        identifyPromises.push(revenueCatProvider.identify(userId).then(() => {}));
      }

      try {
        await Promise.all(identifyPromises);
        log(`User identified: ${userId}`);
      } catch (error) {
        console.error('[Analytics] Identify failed:', error);
      }
    },
    [isEnabled, isInitialized, config.providers]
  );

  /**
   * Set user properties across all providers
   */
  const setUserPropertiesAll = useCallback(
    async (properties: UserProperties): Promise<void> => {
      if (!isEnabled || !isInitialized) return;

      const promises: Promise<void>[] = [];

      if (config.providers.mixpanel?.apiKey) {
        promises.push(mixpanelProvider.setUserProperties(properties));
      }

      if (config.providers.posthog?.apiKey) {
        promises.push(posthogProvider.setUserProperties(properties));
      }

      if (config.providers.firebase) {
        promises.push(firebaseProvider.setUserProperties(properties));
      }

      try {
        await Promise.all(promises);
        log('User properties set:', properties);
      } catch (error) {
        console.error('[Analytics] Set user properties failed:', error);
      }
    },
    [isEnabled, isInitialized, config.providers]
  );

  /**
   * Track revenue
   */
  const trackRevenueAll = useCallback(
    async (revenue: RevenueData): Promise<void> => {
      if (!isEnabled || !isInitialized) return;

      const promises: Promise<void>[] = [];

      if (config.providers.mixpanel?.apiKey) {
        const { trackRevenue } = await import('./providers/mixpanel');
        promises.push(trackRevenue(revenue));
      }

      if (config.providers.firebase) {
        const { trackRevenue } = await import('./providers/firebase');
        promises.push(trackRevenue(revenue));
      }

      try {
        await Promise.all(promises);
        log('Revenue tracked:', revenue);
      } catch (error) {
        console.error('[Analytics] Revenue tracking failed:', error);
      }
    },
    [isEnabled, isInitialized, config.providers]
  );

  /**
   * Reset all providers
   */
  const resetAll = useCallback(async (): Promise<void> => {
    // Clear stored data
    await AsyncStorage.multiRemove([STORAGE_KEYS.USER_ID]);

    setContext((prev) => (prev ? { ...prev, userId: undefined } : null));

    const promises: Promise<void>[] = [];

    if (config.providers.mixpanel?.apiKey) {
      promises.push(mixpanelProvider.reset());
    }

    if (config.providers.posthog?.apiKey) {
      promises.push(posthogProvider.reset());
    }

    if (config.providers.firebase) {
      promises.push(firebaseProvider.reset());
    }

    if (config.providers.revenuecat?.apiKey) {
      promises.push(revenueCatProvider.reset());
    }

    try {
      await Promise.all(promises);
      log('Analytics reset');
    } catch (error) {
      console.error('[Analytics] Reset failed:', error);
    }
  }, [config.providers]);

  /**
   * Flush all providers
   */
  const flushAllProviders = useCallback(async (): Promise<void> => {
    const promises: Promise<void>[] = [];

    if (config.providers.mixpanel?.apiKey) {
      promises.push(mixpanelProvider.flush());
    }

    if (config.providers.posthog?.apiKey) {
      promises.push(posthogProvider.flush());
    }

    if (config.providers.firebase) {
      promises.push(firebaseProvider.flush());
    }

    try {
      await Promise.all(promises);
      log('Analytics flushed');
    } catch (error) {
      console.error('[Analytics] Flush failed:', error);
    }
  }, [config.providers]);

  /**
   * Handle app state changes
   */
  useEffect(() => {
    const handleAppStateChange = (nextAppState: AppStateStatus) => {
      if (
        appStateRef.current.match(/inactive|background/) &&
        nextAppState === 'active'
      ) {
        // App has come to foreground
        const sessionTimeout = config.sessionTimeout ?? DEFAULT_SESSION_TIMEOUT;

        // Check if we need a new session
        AsyncStorage.getItem(STORAGE_KEYS.LAST_SESSION_END).then((lastEnd) => {
          if (lastEnd) {
            const timeSinceLastSession =
              Date.now() - new Date(lastEnd).getTime();
            if (timeSinceLastSession > sessionTimeout) {
              // Start new session
              const newSessionId = uuidv4();
              const newSessionNumber = (context?.sessionNumber ?? 0) + 1;
              startNewSession(newSessionId, newSessionNumber, false);
            }
          }
        });

        // Track app open
        trackToProviders('app_opened', {
          open_type: 'warm',
          days_since_last_open: 0, // Would calculate
        });
      } else if (
        appStateRef.current === 'active' &&
        nextAppState.match(/inactive|background/)
      ) {
        // App has gone to background
        if (sessionRef.current) {
          const startTime = new Date(sessionRef.current.started_at);
          const durationMs = Date.now() - startTime.getTime();

          trackToProviders('app_backgrounded', {
            session_duration_ms: durationMs,
            screens_visited: sessionRef.current.screens_visited.length,
            actions_taken: sessionRef.current.events.length,
          });
        }

        // Set timeout to end session
        if (sessionTimeoutRef.current) {
          clearTimeout(sessionTimeoutRef.current);
        }

        sessionTimeoutRef.current = setTimeout(() => {
          endCurrentSession();
        }, config.sessionTimeout ?? DEFAULT_SESSION_TIMEOUT);
      }

      appStateRef.current = nextAppState;
    };

    const subscription = AppState.addEventListener('change', handleAppStateChange);

    return () => {
      subscription.remove();
      if (sessionTimeoutRef.current) {
        clearTimeout(sessionTimeoutRef.current);
      }
    };
  }, [
    config.sessionTimeout,
    context?.sessionNumber,
    startNewSession,
    endCurrentSession,
    trackToProviders,
  ]);

  /**
   * Initialize on mount
   */
  useEffect(() => {
    initializeProviders();

    return () => {
      endCurrentSession();
    };
  }, [initializeProviders, endCurrentSession]);

  // Context value
  const value: AnalyticsContextValue = {
    context,
    isInitialized,
    isEnabled,
    track: trackToProviders,
    identify: identifyUser,
    setUserProperties: setUserPropertiesAll,
    trackRevenue: trackRevenueAll,
    reset: resetAll,
    flush: flushAllProviders,
    startSession: () => {
      const sessionId = uuidv4();
      const sessionNumber = (context?.sessionNumber ?? 0) + 1;
      startNewSession(sessionId, sessionNumber, false);
    },
    endSession: endCurrentSession,
    setEnabled: (enabled) => {
      setIsEnabled(enabled);
      mixpanelProvider.setEnabled(enabled);
      posthogProvider.setEnabled(enabled);
      firebaseProvider.setEnabled(enabled);
    },
    setDebug: (debug) => {
      debugRef.current = debug;
    },
  };

  return (
    <AnalyticsContext.Provider value={value}>
      {children}
    </AnalyticsContext.Provider>
  );
}

// Helper functions

async function getOrCreateAnonymousId(): Promise<string> {
  let id = await AsyncStorage.getItem(STORAGE_KEYS.ANONYMOUS_ID);
  if (!id) {
    id = uuidv4();
    await AsyncStorage.setItem(STORAGE_KEYS.ANONYMOUS_ID, id);
  }
  return id;
}

async function getOrCreateDeviceId(): Promise<string> {
  let id = await AsyncStorage.getItem(STORAGE_KEYS.DEVICE_ID);
  if (!id) {
    id = await DeviceInfo.getUniqueId();
    await AsyncStorage.setItem(STORAGE_KEYS.DEVICE_ID, id);
  }
  return id;
}

async function getFirstLaunchDate(): Promise<string> {
  let date = await AsyncStorage.getItem(STORAGE_KEYS.FIRST_LAUNCH_DATE);
  if (!date) {
    date = new Date().toISOString();
    await AsyncStorage.setItem(STORAGE_KEYS.FIRST_LAUNCH_DATE, date);
  }
  return date;
}

async function getSessionCount(): Promise<number> {
  const count = await AsyncStorage.getItem(STORAGE_KEYS.SESSION_COUNT);
  return count ? parseInt(count, 10) : 0;
}

function log(message: string, data?: unknown): void {
  if (__DEV__) {
    if (data) {
      console.log(`[Analytics] ${message}`, data);
    } else {
      console.log(`[Analytics] ${message}`);
    }
  }
}

/**
 * Hook to access analytics context
 */
export function useAnalyticsContext(): AnalyticsContextValue {
  const context = useContext(AnalyticsContext);
  if (!context) {
    throw new Error('useAnalyticsContext must be used within AnalyticsProvider');
  }
  return context;
}

export default AnalyticsProvider;
