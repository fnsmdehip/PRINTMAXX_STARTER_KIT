/**
 * Firebase Remote Config Provider
 *
 * Feature flag provider implementation for Firebase Remote Config.
 * https://firebase.google.com/docs/remote-config
 */

import type {
  FeatureFlagProvider,
  FeatureFlagProviderInterface,
  FlagChangeCallback,
  ProviderConfig,
  UserAttributes,
} from '../types';
import type { FlagName, FlagValueMap } from '../flags';
import { DEFAULT_FLAG_VALUES, getDefaultValue, isJsonFlag } from '../flags';

// Firebase Remote Config types (simplified)
interface FirebaseRemoteConfig {
  setDefaults: (defaults: Record<string, unknown>) => Promise<void>;
  fetchAndActivate: () => Promise<boolean>;
  fetch: (minimumFetchIntervalMillis?: number) => Promise<void>;
  activate: () => Promise<boolean>;
  getAll: () => Record<string, RemoteConfigValue>;
  getValue: (key: string) => RemoteConfigValue;
  setLogLevel: (level: string) => void;
}

interface RemoteConfigValue {
  asBoolean: () => boolean;
  asNumber: () => number;
  asString: () => string;
  getSource: () => 'default' | 'remote' | 'static';
}

interface UserProperties {
  [key: string]: string | null;
}

interface FirebaseAnalytics {
  setUserId: (userId: string) => Promise<void>;
  setUserProperties: (properties: UserProperties) => Promise<void>;
}

export class FirebaseRemoteConfigProvider implements FeatureFlagProviderInterface {
  name: FeatureFlagProvider = 'firebase';
  private remoteConfig: FirebaseRemoteConfig | null = null;
  private analytics: FirebaseAnalytics | null = null;
  private config: ProviderConfig | null = null;
  private ready = false;
  private changeCallbacks: Set<FlagChangeCallback> = new Set();
  private cachedValues: Record<string, unknown> = {};
  private refreshInterval: ReturnType<typeof setInterval> | null = null;

  /**
   * Initialize Firebase Remote Config
   */
  async initialize(config: ProviderConfig): Promise<void> {
    this.config = config;

    try {
      // Dynamic imports for React Native
      const { firebase } = await this.loadFirebase();

      this.remoteConfig = firebase.remoteConfig;
      this.analytics = firebase.analytics;

      // Set log level
      if (config.debug) {
        this.remoteConfig.setLogLevel('debug');
      }

      // Set default values
      const defaults: Record<string, unknown> = {};
      for (const [key, value] of Object.entries(DEFAULT_FLAG_VALUES)) {
        if (typeof value === 'object') {
          defaults[key] = JSON.stringify(value);
        } else {
          defaults[key] = value;
        }
      }
      await this.remoteConfig.setDefaults(defaults);

      // Fetch and activate
      await this.remoteConfig.fetchAndActivate();

      // Cache current values
      this.updateCachedValues();

      // Set up periodic refresh if configured
      if (config.refreshInterval) {
        this.refreshInterval = setInterval(() => {
          this.refresh().catch(console.error);
        }, config.refreshInterval);
      }

      this.ready = true;

      if (config.debug) {
        console.log('Firebase Remote Config initialized');
      }
    } catch (error) {
      console.error('Firebase Remote Config initialization failed:', error);
      throw error;
    }
  }

  /**
   * Load Firebase modules
   * This is a placeholder - in production, import the actual SDK
   */
  private async loadFirebase(): Promise<{
    firebase: {
      remoteConfig: FirebaseRemoteConfig;
      analytics: FirebaseAnalytics;
    };
  }> {
    // Placeholder implementation for demonstration
    // In production, use: import remoteConfig from '@react-native-firebase/remote-config';
    const configValues: Record<string, unknown> = {};

    return {
      firebase: {
        remoteConfig: {
          setDefaults: async (defaults: Record<string, unknown>) => {
            Object.assign(configValues, defaults);
          },
          fetchAndActivate: async () => true,
          fetch: async () => {},
          activate: async () => true,
          getAll: () => {
            const result: Record<string, RemoteConfigValue> = {};
            for (const [key, value] of Object.entries(configValues)) {
              result[key] = this.createConfigValue(value);
            }
            return result;
          },
          getValue: (key: string) => {
            return this.createConfigValue(configValues[key]);
          },
          setLogLevel: () => {},
        },
        analytics: {
          setUserId: async () => {},
          setUserProperties: async () => {},
        },
      },
    };
  }

  private createConfigValue(value: unknown): RemoteConfigValue {
    return {
      asBoolean: () => {
        if (typeof value === 'boolean') return value;
        if (typeof value === 'string') return value === 'true';
        return Boolean(value);
      },
      asNumber: () => {
        if (typeof value === 'number') return value;
        return Number(value) || 0;
      },
      asString: () => {
        if (typeof value === 'string') return value;
        if (typeof value === 'object') return JSON.stringify(value);
        return String(value);
      },
      getSource: () => 'remote',
    };
  }

  /**
   * Identify a user
   * Firebase uses Analytics user properties for targeting
   */
  async identify(userId: string, attributes?: UserAttributes): Promise<void> {
    if (!this.analytics) {
      throw new Error('Firebase Analytics not initialized');
    }

    await this.analytics.setUserId(userId);

    if (attributes) {
      const properties: UserProperties = {};

      if (attributes.platform) properties.platform = attributes.platform;
      if (attributes.app_version) properties.app_version = attributes.app_version;
      if (attributes.subscription_status) {
        properties.subscription_status = attributes.subscription_status;
      }
      if (attributes.country) properties.country = attributes.country;
      if (attributes.is_beta_tester !== undefined) {
        properties.is_beta_tester = String(attributes.is_beta_tester);
      }

      // Add custom properties
      if (attributes.custom) {
        for (const [key, value] of Object.entries(attributes.custom)) {
          properties[key] = String(value);
        }
      }

      await this.analytics.setUserProperties(properties);
    }

    // Refresh config after identifying user
    await this.refresh();

    if (this.config?.debug) {
      console.log('Firebase user identified:', userId);
    }
  }

  /**
   * Get a flag value synchronously
   */
  getFlag<T extends FlagName>(flagName: T, defaultValue: FlagValueMap[T]): FlagValueMap[T] {
    if (!this.remoteConfig || !this.ready) {
      return defaultValue;
    }

    // Use cached value for performance
    if (flagName in this.cachedValues) {
      return this.cachedValues[flagName] as FlagValueMap[T];
    }

    const configValue = this.remoteConfig.getValue(flagName);

    // Handle different types
    if (typeof defaultValue === 'boolean') {
      return configValue.asBoolean() as FlagValueMap[T];
    }

    if (typeof defaultValue === 'number') {
      return configValue.asNumber() as FlagValueMap[T];
    }

    if (isJsonFlag(flagName)) {
      try {
        const jsonString = configValue.asString();
        return JSON.parse(jsonString) as FlagValueMap[T];
      } catch {
        return defaultValue;
      }
    }

    return configValue.asString() as FlagValueMap[T];
  }

  /**
   * Get a flag value asynchronously
   */
  async getFlagAsync<T extends FlagName>(
    flagName: T,
    defaultValue: FlagValueMap[T]
  ): Promise<FlagValueMap[T]> {
    return this.getFlag(flagName, defaultValue);
  }

  /**
   * Get all flag values
   */
  async getAllFlags(): Promise<Partial<FlagValueMap>> {
    if (!this.remoteConfig || !this.ready) {
      return {};
    }

    return { ...this.cachedValues } as Partial<FlagValueMap>;
  }

  /**
   * Refresh flags from Firebase
   */
  async refresh(): Promise<void> {
    if (!this.remoteConfig) return;

    const oldValues = { ...this.cachedValues };

    try {
      // Fetch with 0 interval to force refresh
      await this.remoteConfig.fetch(0);
      await this.remoteConfig.activate();

      this.updateCachedValues();

      // Check for changes and notify
      for (const [key, newValue] of Object.entries(this.cachedValues)) {
        const oldValue = oldValues[key];
        if (JSON.stringify(oldValue) !== JSON.stringify(newValue)) {
          this.notifyFlagChange(key as FlagName, oldValue, newValue);
        }
      }
    } catch (error) {
      console.error('Firebase Remote Config refresh failed:', error);
    }
  }

  /**
   * Close the provider
   */
  async close(): Promise<void> {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
      this.refreshInterval = null;
    }

    this.ready = false;
  }

  /**
   * Check if provider is ready
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

  // Private methods

  private updateCachedValues(): void {
    if (!this.remoteConfig) return;

    const allConfigs = this.remoteConfig.getAll();
    const newCache: Record<string, unknown> = {};

    for (const [key, configValue] of Object.entries(allConfigs)) {
      const defaultVal = DEFAULT_FLAG_VALUES[key as FlagName];

      if (typeof defaultVal === 'boolean') {
        newCache[key] = configValue.asBoolean();
      } else if (typeof defaultVal === 'number') {
        newCache[key] = configValue.asNumber();
      } else if (typeof defaultVal === 'object') {
        try {
          newCache[key] = JSON.parse(configValue.asString());
        } catch {
          newCache[key] = defaultVal;
        }
      } else {
        newCache[key] = configValue.asString();
      }
    }

    this.cachedValues = newCache;
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
export function createFirebaseConfig(): ProviderConfig {
  return {
    environment:
      process.env.NODE_ENV === 'production'
        ? 'production'
        : process.env.NODE_ENV === 'test'
          ? 'staging'
          : 'development',
    debug: process.env.NODE_ENV !== 'production',
    refreshInterval: 12 * 60 * 60 * 1000, // 12 hours default
    cacheExpiration: 60 * 60 * 1000, // 1 hour
  };
}
