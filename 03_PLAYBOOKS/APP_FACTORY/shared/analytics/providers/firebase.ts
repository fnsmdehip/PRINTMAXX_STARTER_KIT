/**
 * Firebase Analytics Provider
 *
 * Integration with Firebase/Google Analytics for mobile analytics.
 * Includes screen tracking, user properties, and custom events.
 */

import analytics from '@react-native-firebase/analytics';
import type {
  AnalyticsProvider,
  ProviderConfig,
  UserTraits,
  UserProperties,
  RevenueData,
} from '../types';
import type { AnalyticsEventName, AnalyticsEventMap } from '../events';

// Firebase-specific configuration
export interface FirebaseConfig extends ProviderConfig {
  sessionTimeoutDuration?: number;
  analyticsCollectionEnabled?: boolean;
  defaultEventParametersEnabled?: boolean;
}

// State
let isInitialized = false;
let isEnabled = true;
let debugMode = false;
let currentUserId: string | undefined;

// Firebase Analytics instance
const firebaseAnalytics = analytics();

/**
 * Initialize Firebase Analytics
 */
export async function initializeFirebase(config: FirebaseConfig): Promise<void> {
  if (isInitialized) {
    log('Firebase Analytics already initialized');
    return;
  }

  debugMode = config.debug ?? false;

  try {
    // Set collection enabled state
    await firebaseAnalytics.setAnalyticsCollectionEnabled(
      config.analyticsCollectionEnabled ?? !config.optOut
    );

    if (config.optOut) {
      isEnabled = false;
    }

    // Set session timeout if specified
    if (config.sessionTimeoutDuration) {
      await firebaseAnalytics.setSessionTimeoutDuration(config.sessionTimeoutDuration);
    }

    isInitialized = true;
    log('Firebase Analytics initialized successfully');
  } catch (error) {
    console.error('[Firebase] Initialization failed:', error);
    throw error;
  }
}

/**
 * Identify a user
 */
export async function identifyUser(userId: string, traits?: UserTraits): Promise<void> {
  if (!isInitialized || !isEnabled) {
    log('Firebase not ready, skipping identify');
    return;
  }

  try {
    await firebaseAnalytics.setUserId(userId);
    currentUserId = userId;

    if (traits) {
      const userProperties = transformTraitsToProperties(traits);
      for (const [key, value] of Object.entries(userProperties)) {
        await firebaseAnalytics.setUserProperty(key, String(value));
      }
    }

    log(`User identified: ${userId}`);
  } catch (error) {
    console.error('[Firebase] Identify failed:', error);
    throw error;
  }
}

/**
 * Track an event
 *
 * Firebase has specific event name and parameter restrictions:
 * - Event names: up to 40 characters, alphanumeric and underscores
 * - Parameter names: up to 40 characters
 * - Parameter values: up to 100 characters (strings)
 * - Max 25 parameters per event
 */
export async function trackEvent<T extends AnalyticsEventName>(
  event: T,
  properties: AnalyticsEventMap[T]
): Promise<void> {
  if (!isInitialized || !isEnabled) {
    log(`Firebase not ready, skipping event: ${event}`);
    return;
  }

  try {
    const sanitizedEvent = sanitizeEventName(event);
    const sanitizedProperties = sanitizeParameters(properties);

    await firebaseAnalytics.logEvent(sanitizedEvent, sanitizedProperties);
    log(`Event tracked: ${sanitizedEvent}`, sanitizedProperties);
  } catch (error) {
    console.error(`[Firebase] Track failed for ${event}:`, error);
    throw error;
  }
}

/**
 * Track screen view
 */
export async function trackScreenView(
  screenName: string,
  screenClass?: string
): Promise<void> {
  if (!isInitialized || !isEnabled) {
    return;
  }

  try {
    await firebaseAnalytics.logScreenView({
      screen_name: screenName,
      screen_class: screenClass ?? screenName,
    });
    log(`Screen view: ${screenName}`);
  } catch (error) {
    console.error(`[Firebase] Screen view failed for ${screenName}:`, error);
    throw error;
  }
}

/**
 * Track revenue / purchase
 */
export async function trackRevenue(revenue: RevenueData): Promise<void> {
  if (!isInitialized || !isEnabled) {
    log('Firebase not ready, skipping revenue');
    return;
  }

  try {
    await firebaseAnalytics.logPurchase({
      value: revenue.amount,
      currency: revenue.currency,
      transaction_id: revenue.receipt,
      items: [
        {
          item_id: revenue.product_id,
          item_name: revenue.product_id,
          quantity: revenue.quantity ?? 1,
          price: revenue.amount,
        },
      ],
    });

    log('Revenue tracked:', revenue);
  } catch (error) {
    console.error('[Firebase] Revenue tracking failed:', error);
    throw error;
  }
}

/**
 * Set user properties
 *
 * Firebase limits:
 * - Up to 25 user properties
 * - Property names up to 24 characters
 * - Property values up to 36 characters
 */
export async function setUserProperties(properties: UserProperties): Promise<void> {
  if (!isInitialized || !isEnabled) {
    log('Firebase not ready, skipping setUserProperties');
    return;
  }

  try {
    for (const [key, value] of Object.entries(properties)) {
      if (value !== undefined && value !== null) {
        const sanitizedKey = sanitizePropertyName(key);
        const sanitizedValue = sanitizePropertyValue(value);
        await firebaseAnalytics.setUserProperty(sanitizedKey, sanitizedValue);
      }
    }
    log('User properties set:', properties);
  } catch (error) {
    console.error('[Firebase] Set user properties failed:', error);
    throw error;
  }
}

/**
 * Log app open event
 */
export async function logAppOpen(): Promise<void> {
  if (!isInitialized || !isEnabled) {
    return;
  }

  try {
    await firebaseAnalytics.logAppOpen();
    log('App open logged');
  } catch (error) {
    console.error('[Firebase] Log app open failed:', error);
    throw error;
  }
}

/**
 * Log login event
 */
export async function logLogin(method: string): Promise<void> {
  if (!isInitialized || !isEnabled) {
    return;
  }

  try {
    await firebaseAnalytics.logLogin({ method });
    log(`Login logged: ${method}`);
  } catch (error) {
    console.error('[Firebase] Log login failed:', error);
    throw error;
  }
}

/**
 * Log sign up event
 */
export async function logSignUp(method: string): Promise<void> {
  if (!isInitialized || !isEnabled) {
    return;
  }

  try {
    await firebaseAnalytics.logSignUp({ method });
    log(`Sign up logged: ${method}`);
  } catch (error) {
    console.error('[Firebase] Log sign up failed:', error);
    throw error;
  }
}

/**
 * Log tutorial begin
 */
export async function logTutorialBegin(): Promise<void> {
  if (!isInitialized || !isEnabled) {
    return;
  }

  try {
    await firebaseAnalytics.logTutorialBegin();
    log('Tutorial begin logged');
  } catch (error) {
    console.error('[Firebase] Log tutorial begin failed:', error);
    throw error;
  }
}

/**
 * Log tutorial complete
 */
export async function logTutorialComplete(): Promise<void> {
  if (!isInitialized || !isEnabled) {
    return;
  }

  try {
    await firebaseAnalytics.logTutorialComplete();
    log('Tutorial complete logged');
  } catch (error) {
    console.error('[Firebase] Log tutorial complete failed:', error);
    throw error;
  }
}

/**
 * Log share event
 */
export async function logShare(
  contentType: string,
  itemId: string,
  method: string
): Promise<void> {
  if (!isInitialized || !isEnabled) {
    return;
  }

  try {
    await firebaseAnalytics.logShare({
      content_type: contentType,
      item_id: itemId,
      method,
    });
    log(`Share logged: ${contentType} via ${method}`);
  } catch (error) {
    console.error('[Firebase] Log share failed:', error);
    throw error;
  }
}

/**
 * Reset analytics data
 */
export async function reset(): Promise<void> {
  if (!isInitialized) {
    return;
  }

  try {
    await firebaseAnalytics.resetAnalyticsData();
    await firebaseAnalytics.setUserId(null);
    currentUserId = undefined;
    log('Firebase Analytics reset');
  } catch (error) {
    console.error('[Firebase] Reset failed:', error);
    throw error;
  }
}

/**
 * Flush is not directly supported by Firebase
 * Events are automatically batched and sent
 */
export async function flush(): Promise<void> {
  log('Firebase Analytics auto-flushes events');
}

/**
 * Enable/disable tracking
 */
export async function setEnabled(enabled: boolean): Promise<void> {
  isEnabled = enabled;
  try {
    await firebaseAnalytics.setAnalyticsCollectionEnabled(enabled);
    log(`Firebase Analytics ${enabled ? 'enabled' : 'disabled'}`);
  } catch (error) {
    console.error('[Firebase] Set enabled failed:', error);
    throw error;
  }
}

/**
 * Check if tracking is enabled
 */
export function getIsEnabled(): boolean {
  return isEnabled && isInitialized;
}

/**
 * Get current user ID
 */
export function getCurrentUserId(): string | undefined {
  return currentUserId;
}

/**
 * Set default event parameters
 */
export async function setDefaultEventParameters(
  params: Record<string, string | number | null>
): Promise<void> {
  if (!isInitialized) {
    return;
  }

  try {
    await firebaseAnalytics.setDefaultEventParameters(params);
    log('Default event parameters set:', params);
  } catch (error) {
    console.error('[Firebase] Set default event parameters failed:', error);
    throw error;
  }
}

// Helper functions

function transformTraitsToProperties(traits: UserTraits): Record<string, string> {
  const properties: Record<string, string> = {};

  for (const [key, value] of Object.entries(traits)) {
    if (value !== undefined && value !== null) {
      properties[sanitizePropertyName(key)] = sanitizePropertyValue(value);
    }
  }

  return properties;
}

function sanitizeEventName(name: string): string {
  // Firebase event names must be alphanumeric and underscores, max 40 chars
  return name.replace(/[^a-zA-Z0-9_]/g, '_').substring(0, 40);
}

function sanitizePropertyName(name: string): string {
  // Firebase property names max 24 chars
  return name.replace(/[^a-zA-Z0-9_]/g, '_').substring(0, 24);
}

function sanitizePropertyValue(value: unknown): string {
  // Firebase property values max 36 chars
  const stringValue = typeof value === 'object' ? JSON.stringify(value) : String(value);
  return stringValue.substring(0, 36);
}

function sanitizeParameters(
  params: Record<string, unknown>
): Record<string, string | number> {
  const sanitized: Record<string, string | number> = {};
  let count = 0;

  for (const [key, value] of Object.entries(params)) {
    if (count >= 25) break; // Firebase max 25 parameters

    if (value !== undefined && value !== null) {
      const sanitizedKey = key.replace(/[^a-zA-Z0-9_]/g, '_').substring(0, 40);

      if (typeof value === 'number') {
        sanitized[sanitizedKey] = value;
      } else if (typeof value === 'boolean') {
        sanitized[sanitizedKey] = value ? 1 : 0;
      } else if (typeof value === 'string') {
        sanitized[sanitizedKey] = value.substring(0, 100);
      } else {
        sanitized[sanitizedKey] = JSON.stringify(value).substring(0, 100);
      }

      count++;
    }
  }

  return sanitized;
}

function log(message: string, data?: unknown): void {
  if (debugMode) {
    if (data) {
      console.log(`[Firebase] ${message}`, data);
    } else {
      console.log(`[Firebase] ${message}`);
    }
  }
}

// Export as provider interface
export const firebaseProvider: AnalyticsProvider = {
  name: 'firebase',
  initialize: initializeFirebase,
  identify: identifyUser,
  track: trackEvent,
  setUserProperties,
  reset,
  flush,
  isEnabled: getIsEnabled,
  setEnabled: async (enabled: boolean) => {
    await setEnabled(enabled);
  },
};

// Export convenience functions
export const firebaseEvents = {
  trackScreenView,
  trackRevenue,
  logAppOpen,
  logLogin,
  logSignUp,
  logTutorialBegin,
  logTutorialComplete,
  logShare,
};

export default firebaseProvider;
