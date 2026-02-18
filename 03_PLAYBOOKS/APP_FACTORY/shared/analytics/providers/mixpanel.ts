/**
 * Mixpanel Analytics Provider
 *
 * Integration with Mixpanel for product analytics.
 * Handles event tracking, user identification, and profile management.
 */

import { Mixpanel } from 'mixpanel-react-native';
import type {
  AnalyticsProvider,
  ProviderConfig,
  UserTraits,
  UserProperties,
  RevenueData,
} from '../types';
import type { AnalyticsEventName, AnalyticsEventMap } from '../events';

// Mixpanel-specific configuration
export interface MixpanelConfig extends ProviderConfig {
  apiKey: string;
  serverURL?: string;
  trackAutomaticEvents?: boolean;
  superProperties?: Record<string, unknown>;
}

// Singleton instance
let mixpanelInstance: Mixpanel | null = null;
let isInitialized = false;
let isEnabled = true;
let debugMode = false;

/**
 * Initialize Mixpanel
 */
export async function initializeMixpanel(config: MixpanelConfig): Promise<void> {
  if (isInitialized) {
    log('Mixpanel already initialized');
    return;
  }

  if (!config.apiKey) {
    throw new Error('Mixpanel API key is required');
  }

  debugMode = config.debug ?? false;

  try {
    mixpanelInstance = new Mixpanel(config.apiKey, config.trackAutomaticEvents ?? true);

    await mixpanelInstance.init();

    if (config.serverURL) {
      mixpanelInstance.setServerURL(config.serverURL);
    }

    if (config.superProperties) {
      mixpanelInstance.registerSuperProperties(config.superProperties);
    }

    if (config.optOut) {
      mixpanelInstance.optOutTracking();
      isEnabled = false;
    }

    isInitialized = true;
    log('Mixpanel initialized successfully');
  } catch (error) {
    console.error('[Mixpanel] Initialization failed:', error);
    throw error;
  }
}

/**
 * Identify a user
 */
export async function identifyUser(userId: string, traits?: UserTraits): Promise<void> {
  if (!isInitialized || !mixpanelInstance || !isEnabled) {
    log('Mixpanel not ready, skipping identify');
    return;
  }

  try {
    mixpanelInstance.identify(userId);

    if (traits) {
      const profileProperties = transformTraitsToProfile(traits);
      mixpanelInstance.getPeople().set(profileProperties);
    }

    log(`User identified: ${userId}`);
  } catch (error) {
    console.error('[Mixpanel] Identify failed:', error);
    throw error;
  }
}

/**
 * Track an event
 */
export async function trackEvent<T extends AnalyticsEventName>(
  event: T,
  properties: AnalyticsEventMap[T]
): Promise<void> {
  if (!isInitialized || !mixpanelInstance || !isEnabled) {
    log(`Mixpanel not ready, skipping event: ${event}`);
    return;
  }

  try {
    const enrichedProperties = enrichProperties(properties);
    mixpanelInstance.track(event, enrichedProperties);
    log(`Event tracked: ${event}`, enrichedProperties);
  } catch (error) {
    console.error(`[Mixpanel] Track failed for ${event}:`, error);
    throw error;
  }
}

/**
 * Track revenue
 */
export async function trackRevenue(revenue: RevenueData): Promise<void> {
  if (!isInitialized || !mixpanelInstance || !isEnabled) {
    log('Mixpanel not ready, skipping revenue');
    return;
  }

  try {
    // Track as people property
    mixpanelInstance.getPeople().trackCharge(revenue.amount, {
      product_id: revenue.product_id,
      currency: revenue.currency,
      quantity: revenue.quantity ?? 1,
      is_trial_conversion: revenue.is_trial_conversion ?? false,
      is_renewal: revenue.is_renewal ?? false,
    });

    // Also track as event
    await trackEvent('purchase_completed', {
      product_id: revenue.product_id,
      price: revenue.amount,
      currency: revenue.currency,
      is_trial: revenue.is_trial_conversion ?? false,
      transaction_id: revenue.receipt ?? '',
    });

    log('Revenue tracked:', revenue);
  } catch (error) {
    console.error('[Mixpanel] Revenue tracking failed:', error);
    throw error;
  }
}

/**
 * Set user properties
 */
export async function setUserProperties(properties: UserProperties): Promise<void> {
  if (!isInitialized || !mixpanelInstance || !isEnabled) {
    log('Mixpanel not ready, skipping setUserProperties');
    return;
  }

  try {
    mixpanelInstance.getPeople().set(properties);
    log('User properties set:', properties);
  } catch (error) {
    console.error('[Mixpanel] Set user properties failed:', error);
    throw error;
  }
}

/**
 * Increment a user property
 */
export async function incrementUserProperty(
  property: string,
  value: number = 1
): Promise<void> {
  if (!isInitialized || !mixpanelInstance || !isEnabled) {
    return;
  }

  try {
    mixpanelInstance.getPeople().increment(property, value);
    log(`Property incremented: ${property} by ${value}`);
  } catch (error) {
    console.error('[Mixpanel] Increment failed:', error);
    throw error;
  }
}

/**
 * Append to a list property
 */
export async function appendToListProperty(
  property: string,
  value: unknown
): Promise<void> {
  if (!isInitialized || !mixpanelInstance || !isEnabled) {
    return;
  }

  try {
    mixpanelInstance.getPeople().append(property, value);
    log(`Appended to ${property}:`, value);
  } catch (error) {
    console.error('[Mixpanel] Append failed:', error);
    throw error;
  }
}

/**
 * Set super properties (sent with every event)
 */
export function setSuperProperties(properties: Record<string, unknown>): void {
  if (!isInitialized || !mixpanelInstance) {
    return;
  }

  mixpanelInstance.registerSuperProperties(properties);
  log('Super properties set:', properties);
}

/**
 * Set super properties once (only if not already set)
 */
export function setSuperPropertiesOnce(properties: Record<string, unknown>): void {
  if (!isInitialized || !mixpanelInstance) {
    return;
  }

  mixpanelInstance.registerSuperPropertiesOnce(properties);
  log('Super properties set once:', properties);
}

/**
 * Reset user identity
 */
export async function reset(): Promise<void> {
  if (!isInitialized || !mixpanelInstance) {
    return;
  }

  try {
    mixpanelInstance.reset();
    log('Mixpanel reset');
  } catch (error) {
    console.error('[Mixpanel] Reset failed:', error);
    throw error;
  }
}

/**
 * Flush pending events
 */
export async function flush(): Promise<void> {
  if (!isInitialized || !mixpanelInstance) {
    return;
  }

  try {
    mixpanelInstance.flush();
    log('Mixpanel flushed');
  } catch (error) {
    console.error('[Mixpanel] Flush failed:', error);
    throw error;
  }
}

/**
 * Enable/disable tracking
 */
export function setEnabled(enabled: boolean): void {
  isEnabled = enabled;
  if (mixpanelInstance) {
    if (enabled) {
      mixpanelInstance.optInTracking();
    } else {
      mixpanelInstance.optOutTracking();
    }
  }
  log(`Mixpanel ${enabled ? 'enabled' : 'disabled'}`);
}

/**
 * Check if tracking is enabled
 */
export function getIsEnabled(): boolean {
  return isEnabled && isInitialized;
}

/**
 * Get distinct ID
 */
export async function getDistinctId(): Promise<string | undefined> {
  if (!isInitialized || !mixpanelInstance) {
    return undefined;
  }

  return mixpanelInstance.getDistinctId();
}

/**
 * Time event (for measuring duration)
 */
export function timeEvent(eventName: AnalyticsEventName): void {
  if (!isInitialized || !mixpanelInstance || !isEnabled) {
    return;
  }

  mixpanelInstance.timeEvent(eventName);
  log(`Timing started for: ${eventName}`);
}

/**
 * Create group
 */
export function setGroup(groupKey: string, groupId: string): void {
  if (!isInitialized || !mixpanelInstance) {
    return;
  }

  mixpanelInstance.setGroup(groupKey, groupId);
  log(`Group set: ${groupKey}=${groupId}`);
}

// Helper functions

function transformTraitsToProfile(traits: UserTraits): Record<string, unknown> {
  const profile: Record<string, unknown> = {};

  if (traits.email) profile.$email = traits.email;
  if (traits.name) profile.$name = traits.name;
  if (traits.created_at) profile.$created = traits.created_at;

  // Copy remaining traits
  const { email, name, created_at, ...rest } = traits;
  Object.assign(profile, rest);

  return profile;
}

function enrichProperties(properties: Record<string, unknown>): Record<string, unknown> {
  return {
    ...properties,
    $lib: 'react-native',
    $lib_version: '2.0.0', // Update with actual version
  };
}

function log(message: string, data?: unknown): void {
  if (debugMode) {
    if (data) {
      console.log(`[Mixpanel] ${message}`, data);
    } else {
      console.log(`[Mixpanel] ${message}`);
    }
  }
}

// Export as provider interface
export const mixpanelProvider: AnalyticsProvider = {
  name: 'mixpanel',
  initialize: initializeMixpanel,
  identify: identifyUser,
  track: trackEvent,
  setUserProperties,
  reset,
  flush,
  isEnabled: getIsEnabled,
  setEnabled,
};

export default mixpanelProvider;
