/**
 * Statsig Provider
 *
 * Feature flag provider implementation for Statsig.
 * https://statsig.com
 */

import type {
  FeatureFlagProvider,
  FeatureFlagProviderInterface,
  FlagChangeCallback,
  ProviderConfig,
  UserAttributes,
} from '../types';
import type { FlagName, FlagValueMap } from '../flags';
import { getDefaultValue } from '../flags';

// Statsig SDK types (simplified)
interface StatsigUser {
  userID: string;
  email?: string;
  custom?: Record<string, string | number | boolean | string[]>;
  privateAttributes?: Record<string, unknown>;
  customIDs?: Record<string, string>;
}

interface StatsigConfig {
  get: <T>(key: string, defaultValue: T) => T;
  getValue: () => Record<string, unknown>;
  getRuleID: () => string;
  getGroupName: () => string | null;
}

interface StatsigExperiment {
  get: <T>(key: string, defaultValue: T) => T;
  getValue: () => Record<string, unknown>;
  getGroupName: () => string | null;
}

interface StatsigSDK {
  initialize: (
    clientKey: string,
    user: StatsigUser,
    options?: StatsigOptions
  ) => Promise<void>;
  updateUser: (user: StatsigUser) => Promise<void>;
  checkGate: (gateName: string) => boolean;
  getConfig: (configName: string) => StatsigConfig;
  getExperiment: (experimentName: string) => StatsigExperiment;
  logEvent: (
    eventName: string,
    value?: string | number | null,
    metadata?: Record<string, string>
  ) => void;
  shutdown: () => Promise<void>;
  flush: () => Promise<void>;
  overrideGate: (gateName: string, value: boolean) => void;
  overrideConfig: (configName: string, value: Record<string, unknown>) => void;
  removeOverride: (name: string) => void;
}

interface StatsigOptions {
  environment?: { tier: string };
  initTimeoutMs?: number;
  overrideStableID?: string;
  disableLocalStorage?: boolean;
  api?: string;
}

export class StatsigProvider implements FeatureFlagProviderInterface {
  name: FeatureFlagProvider = 'statsig';
  private statsig: StatsigSDK | null = null;
  private config: ProviderConfig | null = null;
  private ready = false;
  private changeCallbacks: Set<FlagChangeCallback> = new Set();
  private currentUser: StatsigUser | null = null;
  private cachedGates: Map<string, boolean> = new Map();
  private cachedConfigs: Map<string, Record<string, unknown>> = new Map();

  /**
   * Initialize Statsig client
   */
  async initialize(config: ProviderConfig): Promise<void> {
    this.config = config;

    if (!config.clientKey) {
      throw new Error('Statsig clientKey is required');
    }

    try {
      // Dynamic import for React Native
      const Statsig = await this.loadSDK();

      // Create initial anonymous user
      const user: StatsigUser = {
        userID: `anonymous-${Date.now()}`,
      };

      const options: StatsigOptions = {
        environment: {
          tier:
            config.environment === 'production'
              ? 'production'
              : config.environment === 'staging'
                ? 'staging'
                : 'development',
        },
        initTimeoutMs: config.connectionTimeout ?? 10000,
      };

      await Statsig.initialize(config.clientKey, user, options);

      this.statsig = Statsig;
      this.currentUser = user;
      this.ready = true;

      if (config.debug) {
        console.log('Statsig initialized');
      }
    } catch (error) {
      console.error('Statsig initialization failed:', error);
      throw error;
    }
  }

  /**
   * Load the Statsig SDK
   * This is a placeholder - in production, import the actual SDK
   */
  private async loadSDK(): Promise<StatsigSDK> {
    // Placeholder implementation for demonstration
    // In production, use: import Statsig from 'statsig-react-native';
    const gates: Map<string, boolean> = new Map();
    const configs: Map<string, Record<string, unknown>> = new Map();
    const experiments: Map<string, Record<string, unknown>> = new Map();

    return {
      initialize: async (
        _clientKey: string,
        _user: StatsigUser,
        _options?: StatsigOptions
      ) => {},
      updateUser: async (_user: StatsigUser) => {},
      checkGate: (gateName: string) => gates.get(gateName) ?? false,
      getConfig: (configName: string) => ({
        get: <T>(key: string, defaultValue: T): T => {
          const config = configs.get(configName);
          return (config?.[key] as T) ?? defaultValue;
        },
        getValue: () => configs.get(configName) ?? {},
        getRuleID: () => 'default',
        getGroupName: () => null,
      }),
      getExperiment: (experimentName: string) => ({
        get: <T>(key: string, defaultValue: T): T => {
          const exp = experiments.get(experimentName);
          return (exp?.[key] as T) ?? defaultValue;
        },
        getValue: () => experiments.get(experimentName) ?? {},
        getGroupName: () => null,
      }),
      logEvent: () => {},
      shutdown: async () => {},
      flush: async () => {},
      overrideGate: (gateName: string, value: boolean) => {
        gates.set(gateName, value);
      },
      overrideConfig: (configName: string, value: Record<string, unknown>) => {
        configs.set(configName, value);
      },
      removeOverride: (name: string) => {
        gates.delete(name);
        configs.delete(name);
      },
    };
  }

  /**
   * Identify a user
   */
  async identify(userId: string, attributes?: UserAttributes): Promise<void> {
    if (!this.statsig) {
      throw new Error('Statsig not initialized');
    }

    const user: StatsigUser = {
      userID: userId,
      email: attributes?.email,
      custom: {
        platform: attributes?.platform ?? 'unknown',
        app_version: attributes?.app_version ?? 'unknown',
        country: attributes?.country ?? 'unknown',
        subscription_status: attributes?.subscription_status ?? 'free',
        is_beta_tester: attributes?.is_beta_tester ?? false,
        days_since_install: attributes?.days_since_install ?? 0,
        session_count: attributes?.session_count ?? 0,
        ...attributes?.custom,
      },
    };

    await this.statsig.updateUser(user);
    this.currentUser = user;

    // Clear cached values after user change
    this.cachedGates.clear();
    this.cachedConfigs.clear();

    if (this.config?.debug) {
      console.log('Statsig user identified:', userId);
    }
  }

  /**
   * Get a flag value synchronously
   * Uses Statsig gates for boolean flags and configs for other types
   */
  getFlag<T extends FlagName>(flagName: T, defaultValue: FlagValueMap[T]): FlagValueMap[T] {
    if (!this.statsig || !this.ready) {
      return defaultValue;
    }

    // Boolean flags use gates
    if (typeof defaultValue === 'boolean') {
      if (this.cachedGates.has(flagName)) {
        return this.cachedGates.get(flagName) as FlagValueMap[T];
      }
      const value = this.statsig.checkGate(flagName);
      this.cachedGates.set(flagName, value);
      return value as FlagValueMap[T];
    }

    // Other flags use dynamic configs
    const config = this.statsig.getConfig(flagName);
    const value = config.getValue();

    // If config has a 'value' key, use that
    if ('value' in value) {
      return value.value as FlagValueMap[T];
    }

    // Otherwise return the whole config object for JSON flags
    if (typeof defaultValue === 'object') {
      return (Object.keys(value).length > 0 ? value : defaultValue) as FlagValueMap[T];
    }

    // For primitives, try to get from config
    const configValue = config.get('value', defaultValue);
    return configValue as FlagValueMap[T];
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
    if (!this.statsig || !this.ready) {
      return {};
    }

    // Statsig doesn't have a getAllFlags method, so we return cached values
    const result: Partial<FlagValueMap> = {};

    for (const [key, value] of this.cachedGates.entries()) {
      result[key as FlagName] = value as FlagValueMap[FlagName];
    }

    for (const [key, value] of this.cachedConfigs.entries()) {
      result[key as FlagName] = value as FlagValueMap[FlagName];
    }

    return result;
  }

  /**
   * Refresh flags (clear cache and refetch)
   */
  async refresh(): Promise<void> {
    if (!this.statsig) return;

    // Clear caches
    this.cachedGates.clear();
    this.cachedConfigs.clear();

    // Flush pending events
    await this.statsig.flush();
  }

  /**
   * Close the client
   */
  async close(): Promise<void> {
    if (!this.statsig) return;

    await this.statsig.shutdown();
    this.statsig = null;
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
   * Note: Statsig doesn't have real-time updates, so changes are detected on refresh
   */
  onFlagChange(callback: FlagChangeCallback): () => void {
    this.changeCallbacks.add(callback);
    return () => this.changeCallbacks.delete(callback);
  }

  /**
   * Get experiment variant
   */
  getExperiment(
    experimentName: string
  ): {
    groupName: string | null;
    value: Record<string, unknown>;
    get: <T>(key: string, defaultValue: T) => T;
  } {
    if (!this.statsig || !this.ready) {
      return {
        groupName: null,
        value: {},
        get: <T>(_key: string, defaultValue: T) => defaultValue,
      };
    }

    const experiment = this.statsig.getExperiment(experimentName);
    return {
      groupName: experiment.getGroupName(),
      value: experiment.getValue(),
      get: <T>(key: string, defaultValue: T) => experiment.get(key, defaultValue),
    };
  }

  /**
   * Log a custom event
   */
  logEvent(
    eventName: string,
    value?: string | number | null,
    metadata?: Record<string, string>
  ): void {
    if (!this.statsig || !this.ready) return;
    this.statsig.logEvent(eventName, value, metadata);
  }

  /**
   * Override a gate for testing
   */
  overrideGate(gateName: string, value: boolean): void {
    if (!this.statsig) return;
    this.statsig.overrideGate(gateName, value);
    this.cachedGates.set(gateName, value);
  }

  /**
   * Override a config for testing
   */
  overrideConfig(configName: string, value: Record<string, unknown>): void {
    if (!this.statsig) return;
    this.statsig.overrideConfig(configName, value);
    this.cachedConfigs.set(configName, value);
  }

  /**
   * Remove an override
   */
  removeOverride(name: string): void {
    if (!this.statsig) return;
    this.statsig.removeOverride(name);
    this.cachedGates.delete(name);
    this.cachedConfigs.delete(name);
  }

  // Private methods

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
export function createStatsigConfig(clientKey: string): ProviderConfig {
  return {
    clientKey,
    environment:
      process.env.NODE_ENV === 'production'
        ? 'production'
        : process.env.NODE_ENV === 'test'
          ? 'staging'
          : 'development',
    debug: process.env.NODE_ENV !== 'production',
    connectionTimeout: 10000,
  };
}
