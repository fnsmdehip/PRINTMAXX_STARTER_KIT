/**
 * Feature Flag Service
 *
 * Central service for managing feature flags across the app.
 * Handles initialization, caching, and flag evaluation.
 */

import type {
  FeatureFlagConfig,
  FeatureFlagContext,
  FeatureFlagProvider,
  FeatureFlagProviderInterface,
  FlagChangeCallback,
  FlagEvaluation,
  FlagValue,
  ProviderConfig,
  UserAttributes,
} from './types';
import type { FlagName, FlagValueMap } from './flags';
import { DEFAULT_FLAG_VALUES, getDefaultValue } from './flags';

// Cache entry with TTL
interface CacheEntry<T> {
  value: T;
  timestamp: number;
  source: 'provider' | 'cache' | 'default';
}

// Cache storage interface
interface CacheStorage {
  get(key: string): Promise<string | null>;
  set(key: string, value: string): Promise<void>;
  remove(key: string): Promise<void>;
  clear(): Promise<void>;
}

// In-memory cache implementation
class MemoryCache implements CacheStorage {
  private cache: Map<string, string> = new Map();

  async get(key: string): Promise<string | null> {
    return this.cache.get(key) ?? null;
  }

  async set(key: string, value: string): Promise<void> {
    this.cache.set(key, value);
  }

  async remove(key: string): Promise<void> {
    this.cache.delete(key);
  }

  async clear(): Promise<void> {
    this.cache.clear();
  }
}

class FeatureFlagService {
  private static instance: FeatureFlagService;
  private provider: FeatureFlagProviderInterface | null = null;
  private config: FeatureFlagConfig | null = null;
  private cache: Map<string, CacheEntry<FlagValue>> = new Map();
  private cacheStorage: CacheStorage = new MemoryCache();
  private changeCallbacks: Set<FlagChangeCallback> = new Set();
  private context: FeatureFlagContext = {
    isReady: false,
    isLoading: false,
    error: null,
    provider: 'local',
  };
  private refreshTimer: ReturnType<typeof setInterval> | null = null;
  private userId: string | null = null;
  private userAttributes: UserAttributes | null = null;

  private constructor() {}

  static getInstance(): FeatureFlagService {
    if (!FeatureFlagService.instance) {
      FeatureFlagService.instance = new FeatureFlagService();
    }
    return FeatureFlagService.instance;
  }

  /**
   * Initialize the feature flag service with a provider
   */
  async initialize(config: FeatureFlagConfig): Promise<void> {
    if (this.context.isReady) {
      console.warn('FeatureFlagService already initialized');
      return;
    }

    this.config = config;
    this.context.isLoading = true;
    this.context.provider = config.provider;

    try {
      // Load cached flags first for instant availability
      await this.loadCachedFlags();

      // Initialize the provider
      this.provider = await this.createProvider(config.provider, config.providerConfig);
      await this.provider.initialize(config.providerConfig);

      // Identify user if we have stored info
      if (this.userId) {
        await this.provider.identify(this.userId, this.userAttributes ?? undefined);
      }

      // Fetch fresh flags
      await this.refreshFlags();

      // Set up periodic refresh if configured
      if (config.providerConfig.refreshInterval) {
        this.startPeriodicRefresh(config.providerConfig.refreshInterval);
      }

      this.context.isReady = true;
      this.context.isLoading = false;
      this.context.error = null;

      if (config.providerConfig.debug) {
        console.log('FeatureFlagService initialized', {
          provider: config.provider,
          flagCount: this.cache.size,
        });
      }
    } catch (error) {
      this.context.isLoading = false;
      this.context.error = error as Error;
      config.onError?.(error as Error);

      if (config.providerConfig.debug) {
        console.error('FeatureFlagService initialization failed', error);
      }

      // Fall back to defaults
      this.loadDefaultFlags();
      this.context.isReady = true;
    }
  }

  /**
   * Create a provider instance based on the provider name
   */
  private async createProvider(
    providerName: FeatureFlagProvider,
    _config: ProviderConfig
  ): Promise<FeatureFlagProviderInterface> {
    switch (providerName) {
      case 'launchdarkly': {
        const { LaunchDarklyProvider } = await import('./providers/launchdarkly_setup');
        return new LaunchDarklyProvider();
      }
      case 'firebase': {
        const { FirebaseRemoteConfigProvider } = await import('./providers/firebase_remote_config');
        return new FirebaseRemoteConfigProvider();
      }
      case 'statsig': {
        const { StatsigProvider } = await import('./providers/statsig_setup');
        return new StatsigProvider();
      }
      case 'posthog': {
        const { PostHogFlagsProvider } = await import('./providers/posthog_flags');
        return new PostHogFlagsProvider();
      }
      case 'local':
      default: {
        return new LocalProvider();
      }
    }
  }

  /**
   * Identify the current user for targeted flags
   */
  async identify(userId: string, attributes?: UserAttributes): Promise<void> {
    this.userId = userId;
    this.userAttributes = attributes ?? null;
    this.context.userId = userId;

    if (this.provider) {
      await this.provider.identify(userId, attributes);
      // Refresh flags after identification for user-specific targeting
      await this.refreshFlags();
    }
  }

  /**
   * Get a flag value with type safety
   */
  getFlag<T extends FlagName>(flagName: T, defaultValue?: FlagValueMap[T]): FlagValueMap[T] {
    const cached = this.cache.get(flagName);
    const fallback = defaultValue ?? getDefaultValue(flagName);

    // Check cache freshness
    if (cached && this.isCacheValid(cached)) {
      this.logEvaluation(flagName, cached.value as FlagValueMap[T], cached.source);
      return cached.value as FlagValueMap[T];
    }

    // Try provider if available
    if (this.provider?.isReady()) {
      const value = this.provider.getFlag(flagName, fallback);
      this.setCacheEntry(flagName, value, 'provider');
      this.logEvaluation(flagName, value, 'provider');
      return value;
    }

    // Use stale cache if available
    if (cached) {
      this.logEvaluation(flagName, cached.value as FlagValueMap[T], 'cache');
      return cached.value as FlagValueMap[T];
    }

    // Return default
    this.logEvaluation(flagName, fallback, 'default');
    return fallback;
  }

  /**
   * Get a flag value asynchronously (fetches fresh if needed)
   */
  async getFlagAsync<T extends FlagName>(
    flagName: T,
    defaultValue?: FlagValueMap[T]
  ): Promise<FlagValueMap[T]> {
    const fallback = defaultValue ?? getDefaultValue(flagName);

    if (this.provider?.isReady()) {
      try {
        const value = await this.provider.getFlagAsync(flagName, fallback);
        this.setCacheEntry(flagName, value, 'provider');
        return value;
      } catch (error) {
        console.error(`Error fetching flag ${flagName}`, error);
      }
    }

    return this.getFlag(flagName, defaultValue);
  }

  /**
   * Get detailed evaluation info for a flag
   */
  getFlagEvaluation<T extends FlagName>(
    flagName: T,
    defaultValue?: FlagValueMap[T]
  ): FlagEvaluation<FlagValueMap[T]> {
    const cached = this.cache.get(flagName);
    const fallback = defaultValue ?? getDefaultValue(flagName);

    if (cached && this.isCacheValid(cached)) {
      return {
        value: cached.value as FlagValueMap[T],
        source: cached.source,
        reason: cached.source === 'default' ? 'default' : 'match',
        timestamp: cached.timestamp,
        flagName,
      };
    }

    return {
      value: fallback,
      source: 'default',
      reason: 'default',
      timestamp: Date.now(),
      flagName,
    };
  }

  /**
   * Get all flags
   */
  async getAllFlags(): Promise<Partial<FlagValueMap>> {
    if (this.provider?.isReady()) {
      const flags = await this.provider.getAllFlags();
      // Update cache with all flags
      for (const [key, value] of Object.entries(flags)) {
        this.setCacheEntry(key as FlagName, value as FlagValue, 'provider');
      }
      return flags;
    }

    // Return cached values
    const result: Partial<FlagValueMap> = {};
    for (const [key, entry] of this.cache.entries()) {
      result[key as FlagName] = entry.value as FlagValueMap[FlagName];
    }
    return result;
  }

  /**
   * Refresh flags from the provider
   */
  async refreshFlags(): Promise<void> {
    if (!this.provider) return;

    try {
      await this.provider.refresh();
      const flags = await this.provider.getAllFlags();

      // Detect changes and notify listeners
      for (const [key, newValue] of Object.entries(flags)) {
        const cached = this.cache.get(key);
        if (cached && JSON.stringify(cached.value) !== JSON.stringify(newValue)) {
          this.notifyFlagChange(key as FlagName, cached.value, newValue as FlagValue);
        }
        this.setCacheEntry(key as FlagName, newValue as FlagValue, 'provider');
      }

      this.context.lastRefresh = Date.now();
      await this.persistCache();
    } catch (error) {
      console.error('Failed to refresh flags', error);
      this.config?.onError?.(error as Error);
    }
  }

  /**
   * Subscribe to flag changes
   */
  onFlagChange(callback: FlagChangeCallback): () => void {
    this.changeCallbacks.add(callback);
    return () => this.changeCallbacks.delete(callback);
  }

  /**
   * Get current context
   */
  getContext(): FeatureFlagContext {
    return { ...this.context };
  }

  /**
   * Reset user identification
   */
  async reset(): Promise<void> {
    this.userId = null;
    this.userAttributes = null;
    this.context.userId = undefined;
    await this.provider?.close();
    this.cache.clear();
    await this.cacheStorage.clear();
  }

  /**
   * Shutdown the service
   */
  async shutdown(): Promise<void> {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
      this.refreshTimer = null;
    }
    await this.persistCache();
    await this.provider?.close();
    this.context.isReady = false;
  }

  // Private helper methods

  private isCacheValid(entry: CacheEntry<FlagValue>): boolean {
    if (!this.config?.cacheStrategy?.enabled) return false;
    const ttl = this.config.cacheStrategy.ttl;
    return Date.now() - entry.timestamp < ttl;
  }

  private setCacheEntry(flagName: FlagName, value: FlagValue, source: 'provider' | 'cache' | 'default'): void {
    this.cache.set(flagName, {
      value,
      timestamp: Date.now(),
      source,
    });
  }

  private loadDefaultFlags(): void {
    for (const [key, value] of Object.entries(DEFAULT_FLAG_VALUES)) {
      this.setCacheEntry(key as FlagName, value, 'default');
    }

    // Override with custom defaults from config
    if (this.config?.defaultFlags) {
      for (const [key, value] of Object.entries(this.config.defaultFlags)) {
        if (value !== undefined) {
          this.setCacheEntry(key as FlagName, value, 'default');
        }
      }
    }
  }

  private async loadCachedFlags(): Promise<void> {
    try {
      const cached = await this.cacheStorage.get('feature_flags_cache');
      if (cached) {
        const parsed = JSON.parse(cached) as Record<string, CacheEntry<FlagValue>>;
        for (const [key, entry] of Object.entries(parsed)) {
          this.cache.set(key, entry);
        }
      }
    } catch (error) {
      console.warn('Failed to load cached flags', error);
    }
  }

  private async persistCache(): Promise<void> {
    try {
      const cacheObj: Record<string, CacheEntry<FlagValue>> = {};
      for (const [key, value] of this.cache.entries()) {
        cacheObj[key] = value;
      }
      await this.cacheStorage.set('feature_flags_cache', JSON.stringify(cacheObj));
    } catch (error) {
      console.warn('Failed to persist cache', error);
    }
  }

  private startPeriodicRefresh(interval: number): void {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
    this.refreshTimer = setInterval(() => {
      this.refreshFlags().catch(console.error);
    }, interval);
  }

  private notifyFlagChange(flagName: FlagName, oldValue: FlagValue, newValue: FlagValue): void {
    for (const callback of this.changeCallbacks) {
      try {
        callback(flagName, oldValue, newValue);
      } catch (error) {
        console.error('Flag change callback error', error);
      }
    }
  }

  private logEvaluation(flagName: FlagName, value: FlagValue, source: string): void {
    if (this.config?.logEvaluations) {
      console.log(`Flag evaluated: ${flagName} = ${JSON.stringify(value)} (${source})`);
    }
  }
}

// Local provider implementation for development/offline mode
class LocalProvider implements FeatureFlagProviderInterface {
  name: FeatureFlagProvider = 'local';
  private flags: Partial<FlagValueMap> = {};
  private ready = false;

  async initialize(_config: ProviderConfig): Promise<void> {
    this.flags = { ...DEFAULT_FLAG_VALUES };
    this.ready = true;
  }

  async identify(_userId: string, _attributes?: UserAttributes): Promise<void> {
    // No-op for local provider
  }

  getFlag<T extends FlagName>(flagName: T, defaultValue: FlagValueMap[T]): FlagValueMap[T] {
    return (this.flags[flagName] as FlagValueMap[T]) ?? defaultValue;
  }

  async getFlagAsync<T extends FlagName>(
    flagName: T,
    defaultValue: FlagValueMap[T]
  ): Promise<FlagValueMap[T]> {
    return this.getFlag(flagName, defaultValue);
  }

  async getAllFlags(): Promise<Partial<FlagValueMap>> {
    return { ...this.flags };
  }

  async refresh(): Promise<void> {
    // No-op for local provider
  }

  async close(): Promise<void> {
    this.ready = false;
  }

  isReady(): boolean {
    return this.ready;
  }

  onFlagChange(_callback: FlagChangeCallback): () => void {
    return () => {};
  }

  // Local provider specific: set flag for testing
  setFlag<T extends FlagName>(flagName: T, value: FlagValueMap[T]): void {
    this.flags[flagName] = value;
  }
}

// Export singleton instance
export const featureFlagService = FeatureFlagService.getInstance();

// Export class for testing
export { FeatureFlagService, LocalProvider };
