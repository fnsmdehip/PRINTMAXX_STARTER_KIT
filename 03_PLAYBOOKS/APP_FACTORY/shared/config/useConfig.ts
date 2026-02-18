/**
 * useConfig.ts - React hook for accessing app configuration
 *
 * Provides type-safe access to configuration values with
 * environment-aware defaults and memoization.
 */

import { useMemo, useCallback } from 'react';
import { APP_CONFIG, AppConfigType, FeatureFlagsConfig } from './AppConfig';

// Singleton for current app config (set during app init)
let currentConfig: AppConfigType = APP_CONFIG;

/**
 * Set the active app configuration
 * Call this once during app initialization with the app-specific config
 */
export function setActiveConfig(config: AppConfigType): void {
  currentConfig = config;
}

/**
 * Get the current active configuration
 */
export function getActiveConfig(): AppConfigType {
  return currentConfig;
}

/**
 * Main config hook - provides access to full configuration
 */
export function useConfig(): AppConfigType {
  return useMemo(() => currentConfig, []);
}

/**
 * Hook for accessing app identity
 */
export function useAppIdentity() {
  const config = useConfig();
  return useMemo(
    () => ({
      appName: config.identity.appName,
      bundleId: config.identity.bundleId,
      appStoreId: config.identity.appStoreId,
      version: config.version,
      buildNumber: config.buildNumber,
      fullVersion: `${config.version} (${config.buildNumber})`,
    }),
    [config]
  );
}

/**
 * Hook for accessing environment info
 */
export function useEnvironment() {
  const config = useConfig();
  return useMemo(
    () => ({
      environment: config.environment,
      isDev: config.isDev,
      isStaging: config.isStaging,
      isProd: config.isProd,
      platform: config.platform,
    }),
    [config]
  );
}

/**
 * Hook for accessing API configuration
 */
export function useApiConfig() {
  const config = useConfig();
  return useMemo(
    () => ({
      baseUrl: config.api.baseUrl,
      timeout: config.api.timeout,
      retryAttempts: config.api.retryAttempts,
      buildUrl: (path: string) => `${config.api.baseUrl}${path}`,
    }),
    [config]
  );
}

/**
 * Hook for accessing RevenueCat configuration
 */
export function useRevenueCatConfig() {
  const config = useConfig();
  return useMemo(
    () => ({
      apiKey:
        config.platform === 'ios'
          ? config.revenueCat.iosApiKey
          : config.revenueCat.androidApiKey,
      entitlementId: config.revenueCat.entitlementId,
      isConfigured: Boolean(
        config.platform === 'ios'
          ? config.revenueCat.iosApiKey
          : config.revenueCat.androidApiKey
      ),
    }),
    [config]
  );
}

/**
 * Hook for checking feature flags
 */
export function useFeatureFlags(): FeatureFlagsConfig & {
  isEnabled: (flag: keyof FeatureFlagsConfig) => boolean;
} {
  const config = useConfig();

  const isEnabled = useCallback(
    (flag: keyof FeatureFlagsConfig) => {
      return Boolean(config.features[flag]);
    },
    [config.features]
  );

  return useMemo(
    () => ({
      ...config.features,
      isEnabled,
    }),
    [config.features, isEnabled]
  );
}

/**
 * Hook for accessing analytics configuration
 */
export function useAnalyticsConfig() {
  const config = useConfig();
  return useMemo(
    () => ({
      mixpanelToken: config.analytics.mixpanelToken,
      amplitudeKey: config.analytics.amplitudeKey,
      enabled: config.analytics.enabled,
      isConfigured: Boolean(
        config.analytics.mixpanelToken || config.analytics.amplitudeKey
      ),
    }),
    [config]
  );
}

/**
 * Hook for debug mode check
 */
export function useDebugMode(): boolean {
  const config = useConfig();
  return config.features.debugMode;
}

/**
 * Hook for getting a specific config value with a fallback
 */
export function useConfigValue<T>(
  selector: (config: AppConfigType) => T,
  fallback?: T
): T {
  const config = useConfig();
  return useMemo(() => {
    try {
      const value = selector(config);
      return value ?? fallback ?? (undefined as T);
    } catch {
      return fallback ?? (undefined as T);
    }
  }, [config, selector, fallback]);
}

/**
 * Non-hook version for use outside React components
 */
export const Config = {
  get: () => getActiveConfig(),

  getApiUrl: (path: string = '') => {
    const config = getActiveConfig();
    return `${config.api.baseUrl}${path}`;
  },

  isFeatureEnabled: (flag: keyof FeatureFlagsConfig) => {
    const config = getActiveConfig();
    return Boolean(config.features[flag]);
  },

  getRevenueCatKey: () => {
    const config = getActiveConfig();
    return config.platform === 'ios'
      ? config.revenueCat.iosApiKey
      : config.revenueCat.androidApiKey;
  },

  isDev: () => getActiveConfig().isDev,
  isProd: () => getActiveConfig().isProd,
  isStaging: () => getActiveConfig().isStaging,
};

export default useConfig;
