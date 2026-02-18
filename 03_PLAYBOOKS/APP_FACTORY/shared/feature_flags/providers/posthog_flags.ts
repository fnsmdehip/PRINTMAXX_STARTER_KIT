/**
 * PostHog Feature Flags Provider
 *
 * Feature flag provider implementation for PostHog.
 * https://posthog.com
 */

import type {
  FeatureFlagProvider,
  FeatureFlagProviderInterface,
  FlagChangeCallback,
  ProviderConfig,
  UserAttributes,
} from '../types';
import type { FlagName, FlagValueMap } from '../flags';
import { getDefaultValue, isJsonFlag } from '../flags';

// PostHog SDK types (simplified)
interface PostHogProperties {
  [key: string]: string | number | boolean | string[] | null | undefined;
}

interface PostHogClient {
  identify: (distinctId: string, properties?: PostHogProperties) => void;
  reset: () => void;
  getFeatureFlag: (flagKey: string) => string | boolean | undefined;
  getFeatureFlagPayload: (flagKey: string) => unknown;
  isFeatureEnabled: (flagKey: string) => boolean | undefined;
  reloadFeatureFlags: () => Promise<void>;
  onFeatureFlags: (callback: (flags: Record<string, string | boolean>) => void) => () => void;
  capture: (event: string, properties?: PostHogProperties) => void;
  shutdown: () => Promise<void>;
  flush: () => Promise<void>;
  register: (properties: PostHogProperties) => void;
  unregister: (propertyName: string) => void;
  opt_out_capturing: () => void;
  opt_in_capturing: () => void;
}

interface PostHogOptions {
  apiKey: string;
  host?: string;
  captureAppLifecycleEvents?: boolean;
  captureDeepLinks?: boolean;
  flushAt?: number;
  flushInterval?: number;
  debug?: boolean;
  sendFeatureFlagEvent?: boolean;
  preloadFeatureFlags?: boolean;
  bootstrap?: {
    distinctId?: string;
    featureFlags?: Record<string, string | boolean>;
    featureFlagPayloads?: Record<string, unknown>;
  };
}

export class PostHogFlagsProvider implements FeatureFlagProviderInterface {
  name: FeatureFlagProvider = 'posthog';
  private posthog: PostHogClient | null = null;
  private config: ProviderConfig | null = null;
  private ready = false;
  private changeCallbacks: Set<FlagChangeCallback> = new Set();
  private cachedFlags: Map<string, unknown> = new Map();
  private unsubscribeFlagUpdates: (() => void) | null = null;

  /**
   * Initialize PostHog client
   */
  async initialize(config: ProviderConfig): Promise<void> {
    this.config = config;

    if (!config.apiKey) {
      throw new Error('PostHog apiKey is required');
    }

    try {
      // Dynamic import for React Native
      const PostHog = await this.loadSDK();

      const options: PostHogOptions = {
        apiKey: config.apiKey,
        host: config.projectId ?? 'https://app.posthog.com',
        debug: config.debug ?? false,
        flushInterval: config.refreshInterval ?? 30000,
        sendFeatureFlagEvent: true,
        preloadFeatureFlags: true,
        captureAppLifecycleEvents: true,
      };

      await PostHog.setup(options);
      this.posthog = PostHog.client;

      // Subscribe to feature flag updates
      this.unsubscribeFlagUpdates = this.posthog.onFeatureFlags((flags) => {
        this.handleFlagUpdates(flags);
      });

      // Wait for initial flags to load
      await this.posthog.reloadFeatureFlags();

      this.ready = true;

      if (config.debug) {
        console.log('PostHog initialized');
      }
    } catch (error) {
      console.error('PostHog initialization failed:', error);
      throw error;
    }
  }

  /**
   * Load the PostHog SDK
   * This is a placeholder - in production, import the actual SDK
   */
  private async loadSDK(): Promise<{
    setup: (options: PostHogOptions) => Promise<void>;
    client: PostHogClient;
  }> {
    // Placeholder implementation for demonstration
    // In production, use: import PostHog from 'posthog-react-native';
    const flags: Map<string, string | boolean> = new Map();
    const payloads: Map<string, unknown> = new Map();
    let flagCallbacks: Array<(flags: Record<string, string | boolean>) => void> = [];

    return {
      setup: async (_options: PostHogOptions) => {},
      client: {
        identify: (_distinctId: string, _properties?: PostHogProperties) => {},
        reset: () => {
          flags.clear();
          payloads.clear();
        },
        getFeatureFlag: (flagKey: string) => flags.get(flagKey),
        getFeatureFlagPayload: (flagKey: string) => payloads.get(flagKey),
        isFeatureEnabled: (flagKey: string) => {
          const value = flags.get(flagKey);
          if (value === undefined) return undefined;
          if (typeof value === 'boolean') return value;
          return value === 'true';
        },
        reloadFeatureFlags: async () => {
          // Notify callbacks with current flags
          const flagObj: Record<string, string | boolean> = {};
          for (const [key, value] of flags.entries()) {
            flagObj[key] = value;
          }
          for (const callback of flagCallbacks) {
            callback(flagObj);
          }
        },
        onFeatureFlags: (callback: (flags: Record<string, string | boolean>) => void) => {
          flagCallbacks.push(callback);
          return () => {
            flagCallbacks = flagCallbacks.filter((cb) => cb !== callback);
          };
        },
        capture: () => {},
        shutdown: async () => {},
        flush: async () => {},
        register: () => {},
        unregister: () => {},
        opt_out_capturing: () => {},
        opt_in_capturing: () => {},
      },
    };
  }

  /**
   * Identify a user
   */
  async identify(userId: string, attributes?: UserAttributes): Promise<void> {
    if (!this.posthog) {
      throw new Error('PostHog not initialized');
    }

    const properties: PostHogProperties = {
      platform: attributes?.platform,
      app_version: attributes?.app_version,
      country: attributes?.country,
      subscription_status: attributes?.subscription_status,
      is_beta_tester: attributes?.is_beta_tester,
      days_since_install: attributes?.days_since_install,
      session_count: attributes?.session_count,
      email: attributes?.email,
      name: attributes?.name,
    };

    // Add custom properties
    if (attributes?.custom) {
      for (const [key, value] of Object.entries(attributes.custom)) {
        properties[key] = value;
      }
    }

    this.posthog.identify(userId, properties);

    // Reload flags for the new user
    await this.posthog.reloadFeatureFlags();

    if (this.config?.debug) {
      console.log('PostHog user identified:', userId);
    }
  }

  /**
   * Get a flag value synchronously
   */
  getFlag<T extends FlagName>(flagName: T, defaultValue: FlagValueMap[T]): FlagValueMap[T] {
    if (!this.posthog || !this.ready) {
      return defaultValue;
    }

    // Check cache first
    if (this.cachedFlags.has(flagName)) {
      return this.cachedFlags.get(flagName) as FlagValueMap[T];
    }

    // Boolean flags
    if (typeof defaultValue === 'boolean') {
      const value = this.posthog.isFeatureEnabled(flagName);
      return (value ?? defaultValue) as FlagValueMap[T];
    }

    // Get flag value
    const flagValue = this.posthog.getFeatureFlag(flagName);

    // For JSON flags, try to get payload
    if (isJsonFlag(flagName)) {
      const payload = this.posthog.getFeatureFlagPayload(flagName);
      if (payload !== undefined && typeof payload === 'object') {
        this.cachedFlags.set(flagName, payload);
        return payload as FlagValueMap[T];
      }
    }

    // String flags
    if (typeof defaultValue === 'string') {
      const value = typeof flagValue === 'string' ? flagValue : defaultValue;
      return value as FlagValueMap[T];
    }

    // Numeric flags
    if (typeof defaultValue === 'number') {
      if (typeof flagValue === 'string') {
        const num = parseFloat(flagValue);
        return (isNaN(num) ? defaultValue : num) as FlagValueMap[T];
      }
      return defaultValue;
    }

    return defaultValue;
  }

  /**
   * Get a flag value asynchronously
   */
  async getFlagAsync<T extends FlagName>(
    flagName: T,
    defaultValue: FlagValueMap[T]
  ): Promise<FlagValueMap[T]> {
    if (this.posthog) {
      // Ensure flags are loaded
      await this.posthog.reloadFeatureFlags();
    }
    return this.getFlag(flagName, defaultValue);
  }

  /**
   * Get all flag values
   */
  async getAllFlags(): Promise<Partial<FlagValueMap>> {
    if (!this.posthog || !this.ready) {
      return {};
    }

    // PostHog doesn't have a getAllFlags method
    // Return cached values
    const result: Partial<FlagValueMap> = {};
    for (const [key, value] of this.cachedFlags.entries()) {
      result[key as FlagName] = value as FlagValueMap[FlagName];
    }
    return result;
  }

  /**
   * Refresh flags from PostHog
   */
  async refresh(): Promise<void> {
    if (!this.posthog) return;

    // Clear cache
    this.cachedFlags.clear();

    // Reload flags
    await this.posthog.reloadFeatureFlags();
  }

  /**
   * Close the client
   */
  async close(): Promise<void> {
    if (!this.posthog) return;

    if (this.unsubscribeFlagUpdates) {
      this.unsubscribeFlagUpdates();
      this.unsubscribeFlagUpdates = null;
    }

    await this.posthog.flush();
    await this.posthog.shutdown();
    this.posthog = null;
    this.ready = false;
  }

  /**
   * Check if client is ready
   */
  isReady(): boolean {
    return this.ready;
  }

  /**
   * Subscribe to flag changes
   */
  onFlagChange(callback: FlagChangeCallback): () => void {
    this.changeCallbacks.add(callback);
    return () => this.changeCallbacks.delete(callback);
  }

  /**
   * Track an event
   */
  capture(event: string, properties?: Record<string, unknown>): void {
    if (!this.posthog || !this.ready) return;
    this.posthog.capture(event, properties as PostHogProperties);
  }

  /**
   * Register super properties (attached to all events)
   */
  register(properties: Record<string, unknown>): void {
    if (!this.posthog || !this.ready) return;
    this.posthog.register(properties as PostHogProperties);
  }

  /**
   * Unregister a super property
   */
  unregister(propertyName: string): void {
    if (!this.posthog || !this.ready) return;
    this.posthog.unregister(propertyName);
  }

  /**
   * Opt out of tracking
   */
  optOut(): void {
    if (!this.posthog) return;
    this.posthog.opt_out_capturing();
  }

  /**
   * Opt in to tracking
   */
  optIn(): void {
    if (!this.posthog) return;
    this.posthog.opt_in_capturing();
  }

  /**
   * Reset user and flags
   */
  reset(): void {
    if (!this.posthog) return;
    this.posthog.reset();
    this.cachedFlags.clear();
  }

  // Private methods

  private handleFlagUpdates(flags: Record<string, string | boolean>): void {
    const oldFlags = new Map(this.cachedFlags);

    // Update cached flags
    for (const [key, value] of Object.entries(flags)) {
      this.cachedFlags.set(key, value);

      // Check for changes
      const oldValue = oldFlags.get(key);
      if (JSON.stringify(oldValue) !== JSON.stringify(value)) {
        this.notifyFlagChange(key as FlagName, oldValue, value);
      }
    }
  }

  private notifyFlagChange(
    flagName: FlagName,
    oldValue: unknown,
    newValue: unknown
  ): void {
    for (const callback of this.changeCallbacks) {
      try {
        callback(flagName, oldValue, newValue);
      } catch (error) {
        console.error('Flag change callback error:', error);
      }
    }
  }
}

// Configuration helper
export function createPostHogConfig(apiKey: string, host?: string): ProviderConfig {
  return {
    apiKey,
    projectId: host ?? 'https://app.posthog.com',
    environment:
      process.env.NODE_ENV === 'production'
        ? 'production'
        : process.env.NODE_ENV === 'test'
          ? 'staging'
          : 'development',
    debug: process.env.NODE_ENV !== 'production',
    refreshInterval: 30000, // 30 seconds
  };
}
