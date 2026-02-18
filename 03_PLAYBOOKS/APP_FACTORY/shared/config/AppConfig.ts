/**
 * AppConfig.ts - Main configuration for APP_FACTORY apps
 *
 * Central configuration system for all React Native apps.
 * Environment-aware with type safety.
 */

import { Platform } from 'react-native';
import { getEnvironment, Environment } from './environments';

// Type definitions
export interface ApiConfig {
  baseUrl: string;
  timeout: number;
  retryAttempts: number;
}

export interface RevenueCatConfig {
  iosApiKey: string;
  androidApiKey?: string;
  entitlementId: string;
}

export interface AnalyticsConfig {
  mixpanelToken?: string;
  amplitudeKey?: string;
  enabled: boolean;
}

export interface FeatureFlagsConfig {
  showPaywallOnLaunch: boolean;
  enablePushNotifications: boolean;
  enableAnalytics: boolean;
  enableCrashReporting: boolean;
  debugMode: boolean;
}

export interface AppIdentity {
  appName: string;
  bundleId: string;
  appStoreId?: string;
  teamId?: string;
}

export interface AppConfigType {
  // App identity
  identity: AppIdentity;

  // Environment
  environment: Environment;
  isDev: boolean;
  isStaging: boolean;
  isProd: boolean;

  // API
  api: ApiConfig;

  // RevenueCat
  revenueCat: RevenueCatConfig;

  // Analytics
  analytics: AnalyticsConfig;

  // Feature flags
  features: FeatureFlagsConfig;

  // Platform
  platform: 'ios' | 'android';

  // Build info
  version: string;
  buildNumber: string;
}

// Get current environment
const env = getEnvironment();

// Check for __DEV__ safely (React Native global)
const isDev = typeof __DEV__ !== 'undefined' ? __DEV__ : env === 'development';

// Base configuration - override per-app
export const APP_CONFIG: AppConfigType = {
  // App identity (override in per-app config)
  identity: {
    appName: 'AppName',
    bundleId: 'com.printmaxx.appname',
    appStoreId: undefined,
    teamId: process.env.APPLE_TEAM_ID,
  },

  // Environment detection
  environment: env,
  isDev: env === 'development',
  isStaging: env === 'staging',
  isProd: env === 'production',

  // API configuration
  api: {
    baseUrl: getApiUrl(env),
    timeout: 30000,
    retryAttempts: 3,
  },

  // RevenueCat (override per-app)
  revenueCat: {
    iosApiKey: process.env.REVENUECAT_IOS_KEY || '',
    androidApiKey: process.env.REVENUECAT_ANDROID_KEY,
    entitlementId: 'premium',
  },

  // Analytics
  analytics: {
    mixpanelToken: process.env.MIXPANEL_TOKEN,
    amplitudeKey: process.env.AMPLITUDE_KEY,
    enabled: env === 'production',
  },

  // Feature flags defaults
  features: {
    showPaywallOnLaunch: false,
    enablePushNotifications: true,
    enableAnalytics: env === 'production',
    enableCrashReporting: env !== 'development',
    debugMode: isDev,
  },

  // Platform
  platform: Platform.OS as 'ios' | 'android',

  // Build info (injected at build time)
  version: process.env.APP_VERSION || '1.0.0',
  buildNumber: process.env.BUILD_NUMBER || '1',
};

/**
 * Get API URL based on environment
 */
function getApiUrl(environment: Environment): string {
  switch (environment) {
    case 'development':
      return process.env.DEV_API_URL || 'http://localhost:3000/api';
    case 'staging':
      return process.env.STAGING_API_URL || 'https://staging.api.printmaxx.com';
    case 'production':
      return process.env.PROD_API_URL || 'https://api.printmaxx.com';
    default:
      return 'http://localhost:3000/api';
  }
}

/**
 * Create app-specific config by merging with base
 */
export function createAppConfig(
  overrides: Partial<AppConfigType> & { identity: AppIdentity }
): AppConfigType {
  return {
    ...APP_CONFIG,
    ...overrides,
    identity: {
      ...APP_CONFIG.identity,
      ...overrides.identity,
    },
    api: {
      ...APP_CONFIG.api,
      ...overrides.api,
    },
    revenueCat: {
      ...APP_CONFIG.revenueCat,
      ...overrides.revenueCat,
    },
    analytics: {
      ...APP_CONFIG.analytics,
      ...overrides.analytics,
    },
    features: {
      ...APP_CONFIG.features,
      ...overrides.features,
    },
  };
}

/**
 * Validate config on app startup
 */
export function validateConfig(config: AppConfigType): void {
  const errors: string[] = [];

  if (!config.identity.bundleId) {
    errors.push('Bundle ID is required');
  }

  if (config.isProd && !config.revenueCat.iosApiKey) {
    errors.push('RevenueCat API key required for production');
  }

  if (config.isProd && config.features.debugMode) {
    errors.push('Debug mode should not be enabled in production');
  }

  if (errors.length > 0) {
    console.error('Config validation errors:', errors);
    if (config.isProd) {
      throw new Error(`Invalid configuration: ${errors.join(', ')}`);
    }
  }
}

export default APP_CONFIG;
