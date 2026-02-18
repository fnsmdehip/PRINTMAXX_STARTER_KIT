/**
 * LaunchDarkly Provider
 *
 * Feature flag provider implementation for LaunchDarkly.
 * https://launchdarkly.com
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

// LaunchDarkly SDK types (simplified for implementation)
interface LDClient {
  identify: (context: LDContext) => Promise<void>;
  variation: <T>(flagKey: string, defaultValue: T) => T;
  variationDetail: <T>(flagKey: string, defaultValue: T) => LDEvaluationDetail<T>;
  allFlags: () => Record<string, unknown>;
  on: (event: string, callback: (flag?: string) => void) => void;
  off: (event: string, callback: (flag?: string) => void) => void;
  close: () => Promise<void>;
  waitForInitialization: () => Promise<void>;
  flush: () => Promise<void>;
}

interface LDContext {
  kind: string;
  key: string;
  name?: string;
  email?: string;
  custom?: Record<string, string | number | boolean>;
}

interface LDEvaluationDetail<T> {
  value: T;
  variationIndex?: number;
  reason: {
    kind: string;
    errorKind?: string;
  };
}

export class LaunchDarklyProvider implements FeatureFlagProviderInterface {
  name: FeatureFlagProvider = 'launchdarkly';
  private client: LDClient | null = null;
  private config: ProviderConfig | null = null;
  private ready = false;
  private changeCallbacks: Set<FlagChangeCallback> = new Set();
  private changeHandler: ((flag?: string) => void) | null = null;
  private currentFlags: Record<string, unknown> = {};

  /**
   * Initialize LaunchDarkly client
   */
  async initialize(config: ProviderConfig): Promise<void> {
    this.config = config;

    if (!config.mobileKey) {
      throw new Error('LaunchDarkly mobileKey is required');
    }

    try {
      // Dynamic import for React Native
      // In a real implementation, you would import the actual SDK:
      // import LDClient from 'launchdarkly-react-native-client-sdk';
      const LDModule = await this.loadSDK();

      // Create anonymous context for initial setup
      const context: LDContext = {
        kind: 'user',
        key: `anonymous-${Date.now()}`,
      };

      // Initialize the client
      this.client = await LDModule.configure(
        {
          mobileKey: config.mobileKey,
          debug: config.debug ?? false,
          connectionTimeout: config.connectionTimeout ?? 10000,
          evaluationTimeout: config.evaluationTimeout ?? 5000,
          offline: config.offline ?? false,
        },
        context
      );

      await this.client.waitForInitialization();

      // Set up change listener
      this.changeHandler = (flag?: string) => {
        if (flag) {
          const oldValue = this.currentFlags[flag];
          const newValue = this.client?.variation(flag, oldValue);
          if (JSON.stringify(oldValue) !== JSON.stringify(newValue)) {
            this.currentFlags[flag] = newValue;
            this.notifyFlagChange(flag as FlagName, oldValue, newValue);
          }
        }
      };

      this.client.on('change', this.changeHandler);

      // Store current flag values
      this.currentFlags = this.client.allFlags();
      this.ready = true;

      if (config.debug) {
        console.log('LaunchDarkly initialized');
      }
    } catch (error) {
      console.error('LaunchDarkly initialization failed:', error);
      throw error;
    }
  }

  /**
   * Load the LaunchDarkly SDK
   * This is a placeholder - in production, import the actual SDK
   */
  private async loadSDK(): Promise<{
    configure: (config: unknown, context: LDContext) => Promise<LDClient>;
  }> {
    // Placeholder implementation for demonstration
    // In production, use: import LDClient from 'launchdarkly-react-native-client-sdk';
    return {
      configure: async (_config: unknown, context: LDContext): Promise<LDClient> => {
        const flags: Record<string, unknown> = {};
        const listeners: Map<string, Array<(flag?: string) => void>> = new Map();

        return {
          identify: async (_ctx: LDContext) => {},
          variation: <T>(flagKey: string, defaultValue: T): T => {
            return (flags[flagKey] as T) ?? defaultValue;
          },
          variationDetail: <T>(flagKey: string, defaultValue: T): LDEvaluationDetail<T> => ({
            value: (flags[flagKey] as T) ?? defaultValue,
            reason: { kind: 'FALLTHROUGH' },
          }),
          allFlags: () => ({ ...flags }),
          on: (event: string, callback: (flag?: string) => void) => {
            if (!listeners.has(event)) {
              listeners.set(event, []);
            }
            listeners.get(event)?.push(callback);
          },
          off: (event: string, callback: (flag?: string) => void) => {
            const eventListeners = listeners.get(event);
            if (eventListeners) {
              const index = eventListeners.indexOf(callback);
              if (index > -1) {
                eventListeners.splice(index, 1);
              }
            }
          },
          close: async () => {},
          waitForInitialization: async () => {},
          flush: async () => {},
        };
      },
    };
  }

  /**
   * Identify a user
   */
  async identify(userId: string, attributes?: UserAttributes): Promise<void> {
    if (!this.client) {
      throw new Error('LaunchDarkly client not initialized');
    }

    const context: LDContext = {
      kind: 'user',
      key: userId,
      name: attributes?.name,
      email: attributes?.email,
      custom: {
        ...attributes?.custom,
        platform: attributes?.platform ?? 'unknown',
        app_version: attributes?.app_version ?? 'unknown',
        subscription_status: attributes?.subscription_status ?? 'free',
        is_beta_tester: attributes?.is_beta_tester ?? false,
      },
    };

    await this.client.identify(context);

    // Update current flags after identification
    this.currentFlags = this.client.allFlags();

    if (this.config?.debug) {
      console.log('LaunchDarkly user identified:', userId);
    }
  }

  /**
   * Get a flag value synchronously
   */
  getFlag<T extends FlagName>(flagName: T, defaultValue: FlagValueMap[T]): FlagValueMap[T] {
    if (!this.client || !this.ready) {
      return defaultValue;
    }

    return this.client.variation(flagName, defaultValue);
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
    if (!this.client || !this.ready) {
      return {};
    }

    return this.client.allFlags() as Partial<FlagValueMap>;
  }

  /**
   * Refresh flags (flush evaluation cache)
   */
  async refresh(): Promise<void> {
    if (!this.client) return;

    await this.client.flush();
    this.currentFlags = this.client.allFlags();
  }

  /**
   * Close the client
   */
  async close(): Promise<void> {
    if (!this.client) return;

    if (this.changeHandler) {
      this.client.off('change', this.changeHandler);
      this.changeHandler = null;
    }

    await this.client.close();
    this.client = null;
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
   * Get evaluation details for a flag
   */
  getFlagWithDetails<T extends FlagName>(
    flagName: T,
    defaultValue: FlagValueMap[T]
  ): {
    value: FlagValueMap[T];
    reason: string;
    variationIndex?: number;
  } {
    if (!this.client || !this.ready) {
      return { value: defaultValue, reason: 'CLIENT_NOT_READY' };
    }

    const detail = this.client.variationDetail(flagName, defaultValue);
    return {
      value: detail.value,
      reason: detail.reason.kind,
      variationIndex: detail.variationIndex,
    };
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
export function createLaunchDarklyConfig(mobileKey: string): ProviderConfig {
  return {
    mobileKey,
    environment:
      process.env.NODE_ENV === 'production'
        ? 'production'
        : process.env.NODE_ENV === 'test'
          ? 'staging'
          : 'development',
    debug: process.env.NODE_ENV !== 'production',
    connectionTimeout: 10000,
    evaluationTimeout: 5000,
  };
}
