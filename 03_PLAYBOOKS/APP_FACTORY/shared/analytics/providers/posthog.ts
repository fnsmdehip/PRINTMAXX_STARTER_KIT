/**
 * PostHog Analytics Provider
 *
 * Integration with PostHog for product analytics, feature flags, and session recording.
 */

import PostHog from 'posthog-react-native';
import type {
  AnalyticsProvider,
  ProviderConfig,
  UserTraits,
  UserProperties,
} from '../types';
import type { AnalyticsEventName, AnalyticsEventMap } from '../events';

// PostHog-specific configuration
export interface PostHogConfig extends ProviderConfig {
  apiKey: string;
  host?: string;
  captureApplicationLifecycleEvents?: boolean;
  captureDeepLinks?: boolean;
  recordScreenViews?: boolean;
  flushAt?: number;
  maxBatchSize?: number;
  maxQueueSize?: number;
}

// Singleton instance
let posthogInstance: PostHog | null = null;
let isInitialized = false;
let isEnabled = true;
let debugMode = false;

/**
 * Initialize PostHog
 */
export async function initializePostHog(config: PostHogConfig): Promise<void> {
  if (isInitialized) {
    log('PostHog already initialized');
    return;
  }

  if (!config.apiKey) {
    throw new Error('PostHog API key is required');
  }

  debugMode = config.debug ?? false;

  try {
    posthogInstance = new PostHog(config.apiKey, {
      host: config.host ?? 'https://app.posthog.com',
      captureApplicationLifecycleEvents: config.captureApplicationLifecycleEvents ?? true,
      captureDeepLinks: config.captureDeepLinks ?? true,
      recordScreenViews: config.recordScreenViews ?? true,
      flushAt: config.flushAt ?? 20,
      flushInterval: config.flushInterval ?? 30000,
      maxBatchSize: config.maxBatchSize ?? 100,
      maxQueueSize: config.maxQueueSize ?? 1000,
      debug: config.debug ?? false,
    });

    if (config.optOut) {
      posthogInstance.optOut();
      isEnabled = false;
    }

    isInitialized = true;
    log('PostHog initialized successfully');
  } catch (error) {
    console.error('[PostHog] Initialization failed:', error);
    throw error;
  }
}

/**
 * Identify a user
 */
export async function identifyUser(userId: string, traits?: UserTraits): Promise<void> {
  if (!isInitialized || !posthogInstance || !isEnabled) {
    log('PostHog not ready, skipping identify');
    return;
  }

  try {
    posthogInstance.identify(userId, traits);
    log(`User identified: ${userId}`);
  } catch (error) {
    console.error('[PostHog] Identify failed:', error);
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
  if (!isInitialized || !posthogInstance || !isEnabled) {
    log(`PostHog not ready, skipping event: ${event}`);
    return;
  }

  try {
    posthogInstance.capture(event, properties);
    log(`Event tracked: ${event}`, properties);
  } catch (error) {
    console.error(`[PostHog] Track failed for ${event}:`, error);
    throw error;
  }
}

/**
 * Set user properties
 */
export async function setUserProperties(properties: UserProperties): Promise<void> {
  if (!isInitialized || !posthogInstance || !isEnabled) {
    log('PostHog not ready, skipping setUserProperties');
    return;
  }

  try {
    // PostHog uses $set for person properties
    posthogInstance.capture('$set', {
      $set: properties,
    });
    log('User properties set:', properties);
  } catch (error) {
    console.error('[PostHog] Set user properties failed:', error);
    throw error;
  }
}

/**
 * Set user properties once (only if not already set)
 */
export async function setUserPropertiesOnce(properties: UserProperties): Promise<void> {
  if (!isInitialized || !posthogInstance || !isEnabled) {
    return;
  }

  try {
    posthogInstance.capture('$set', {
      $set_once: properties,
    });
    log('User properties set once:', properties);
  } catch (error) {
    console.error('[PostHog] Set user properties once failed:', error);
    throw error;
  }
}

/**
 * Alias user (connect anonymous and identified user)
 */
export async function alias(alias: string): Promise<void> {
  if (!isInitialized || !posthogInstance || !isEnabled) {
    return;
  }

  try {
    posthogInstance.alias(alias);
    log(`Alias created: ${alias}`);
  } catch (error) {
    console.error('[PostHog] Alias failed:', error);
    throw error;
  }
}

/**
 * Register super properties (sent with every event)
 */
export function registerSuperProperties(properties: Record<string, unknown>): void {
  if (!isInitialized || !posthogInstance) {
    return;
  }

  posthogInstance.register(properties);
  log('Super properties registered:', properties);
}

/**
 * Get feature flag value
 */
export async function getFeatureFlag(flagKey: string): Promise<boolean | string | undefined> {
  if (!isInitialized || !posthogInstance || !isEnabled) {
    return undefined;
  }

  try {
    await posthogInstance.reloadFeatureFlagsAsync();
    const value = posthogInstance.getFeatureFlag(flagKey);
    log(`Feature flag ${flagKey}:`, value);
    return value;
  } catch (error) {
    console.error(`[PostHog] Get feature flag failed for ${flagKey}:`, error);
    return undefined;
  }
}

/**
 * Get feature flag payload
 */
export async function getFeatureFlagPayload(
  flagKey: string
): Promise<Record<string, unknown> | undefined> {
  if (!isInitialized || !posthogInstance || !isEnabled) {
    return undefined;
  }

  try {
    await posthogInstance.reloadFeatureFlagsAsync();
    const payload = posthogInstance.getFeatureFlagPayload(flagKey);
    log(`Feature flag payload ${flagKey}:`, payload);
    return payload as Record<string, unknown> | undefined;
  } catch (error) {
    console.error(`[PostHog] Get feature flag payload failed for ${flagKey}:`, error);
    return undefined;
  }
}

/**
 * Check if feature is enabled
 */
export async function isFeatureEnabled(flagKey: string): Promise<boolean> {
  if (!isInitialized || !posthogInstance || !isEnabled) {
    return false;
  }

  try {
    await posthogInstance.reloadFeatureFlagsAsync();
    const enabled = posthogInstance.isFeatureEnabled(flagKey);
    log(`Feature ${flagKey} enabled:`, enabled);
    return enabled ?? false;
  } catch (error) {
    console.error(`[PostHog] Is feature enabled failed for ${flagKey}:`, error);
    return false;
  }
}

/**
 * Reload feature flags
 */
export async function reloadFeatureFlags(): Promise<void> {
  if (!isInitialized || !posthogInstance) {
    return;
  }

  try {
    await posthogInstance.reloadFeatureFlagsAsync();
    log('Feature flags reloaded');
  } catch (error) {
    console.error('[PostHog] Reload feature flags failed:', error);
    throw error;
  }
}

/**
 * Track a screen view
 */
export async function trackScreen(
  screenName: string,
  properties?: Record<string, unknown>
): Promise<void> {
  if (!isInitialized || !posthogInstance || !isEnabled) {
    return;
  }

  try {
    posthogInstance.screen(screenName, properties);
    log(`Screen tracked: ${screenName}`, properties);
  } catch (error) {
    console.error(`[PostHog] Screen track failed for ${screenName}:`, error);
    throw error;
  }
}

/**
 * Group user
 */
export async function group(
  groupType: string,
  groupKey: string,
  groupProperties?: Record<string, unknown>
): Promise<void> {
  if (!isInitialized || !posthogInstance || !isEnabled) {
    return;
  }

  try {
    posthogInstance.group(groupType, groupKey, groupProperties);
    log(`Group set: ${groupType}/${groupKey}`, groupProperties);
  } catch (error) {
    console.error('[PostHog] Group failed:', error);
    throw error;
  }
}

/**
 * Reset user identity
 */
export async function reset(): Promise<void> {
  if (!isInitialized || !posthogInstance) {
    return;
  }

  try {
    posthogInstance.reset();
    log('PostHog reset');
  } catch (error) {
    console.error('[PostHog] Reset failed:', error);
    throw error;
  }
}

/**
 * Flush pending events
 */
export async function flush(): Promise<void> {
  if (!isInitialized || !posthogInstance) {
    return;
  }

  try {
    posthogInstance.flush();
    log('PostHog flushed');
  } catch (error) {
    console.error('[PostHog] Flush failed:', error);
    throw error;
  }
}

/**
 * Enable/disable tracking
 */
export function setEnabled(enabled: boolean): void {
  isEnabled = enabled;
  if (posthogInstance) {
    if (enabled) {
      posthogInstance.optIn();
    } else {
      posthogInstance.optOut();
    }
  }
  log(`PostHog ${enabled ? 'enabled' : 'disabled'}`);
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
export function getDistinctId(): string | undefined {
  if (!isInitialized || !posthogInstance) {
    return undefined;
  }

  return posthogInstance.getDistinctId();
}

/**
 * Close PostHog
 */
export async function close(): Promise<void> {
  if (!isInitialized || !posthogInstance) {
    return;
  }

  try {
    await posthogInstance.flush();
    isInitialized = false;
    posthogInstance = null;
    log('PostHog closed');
  } catch (error) {
    console.error('[PostHog] Close failed:', error);
    throw error;
  }
}

// Helper functions

function log(message: string, data?: unknown): void {
  if (debugMode) {
    if (data) {
      console.log(`[PostHog] ${message}`, data);
    } else {
      console.log(`[PostHog] ${message}`);
    }
  }
}

// Export as provider interface
export const posthogProvider: AnalyticsProvider = {
  name: 'posthog',
  initialize: initializePostHog,
  identify: identifyUser,
  track: trackEvent,
  setUserProperties,
  reset,
  flush,
  isEnabled: getIsEnabled,
  setEnabled,
};

// Export feature flag functions separately
export const featureFlags = {
  getFeatureFlag,
  getFeatureFlagPayload,
  isFeatureEnabled,
  reloadFeatureFlags,
};

export default posthogProvider;
