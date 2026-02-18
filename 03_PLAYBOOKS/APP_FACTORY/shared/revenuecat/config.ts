/**
 * RevenueCat Configuration
 * Centralized configuration for all apps
 *
 * IMPORTANT: API keys should be loaded from environment variables.
 * Never commit actual API keys to version control.
 */

import { Platform } from 'react-native';
import type { AppConfig, EntitlementId } from './types';

/**
 * Environment variable names for API keys
 */
export const ENV_KEYS = {
  PRAYERLOCK_IOS: 'REVENUECAT_IOS_KEY_PRAYERLOCK',
  PRAYERLOCK_ANDROID: 'REVENUECAT_ANDROID_KEY_PRAYERLOCK',
  WALKTOUNLOCK_IOS: 'REVENUECAT_IOS_KEY_WALKTOUNLOCK',
  WALKTOUNLOCK_ANDROID: 'REVENUECAT_ANDROID_KEY_WALKTOUNLOCK',
  STUDYLOCK_IOS: 'REVENUECAT_IOS_KEY_STUDYLOCK',
  STUDYLOCK_ANDROID: 'REVENUECAT_ANDROID_KEY_STUDYLOCK',
  PROMPTVAULT_IOS: 'REVENUECAT_IOS_KEY_PROMPTVAULT',
  PROMPTVAULT_ANDROID: 'REVENUECAT_ANDROID_KEY_PROMPTVAULT',
  DAILYANCHOR_IOS: 'REVENUECAT_IOS_KEY_DAILYANCHOR',
  DAILYANCHOR_ANDROID: 'REVENUECAT_ANDROID_KEY_DAILYANCHOR',
  FEMFIT_IOS: 'REVENUECAT_IOS_KEY_FEMFIT',
  FEMFIT_ANDROID: 'REVENUECAT_ANDROID_KEY_FEMFIT',
  DAILYDEVOTION_IOS: 'REVENUECAT_IOS_KEY_DAILYDEVOTION',
  DAILYDEVOTION_ANDROID: 'REVENUECAT_ANDROID_KEY_DAILYDEVOTION',
  WEBHOOK_SECRET: 'REVENUECAT_WEBHOOK_SECRET',
} as const;

/**
 * Default entitlement ID used across all apps
 */
export const DEFAULT_ENTITLEMENT_ID: EntitlementId = 'premium';

/**
 * Package identifiers (RevenueCat standard)
 */
export const PACKAGE_IDS = {
  MONTHLY: '$rc_monthly',
  ANNUAL: '$rc_annual',
  WEEKLY: '$rc_weekly',
  LIFETIME: '$rc_lifetime',
} as const;

/**
 * Offering identifiers
 */
export const OFFERING_IDS = {
  DEFAULT: 'default',
  SALE: 'sale',
  UPGRADE: 'upgrade',
} as const;

/**
 * Product ID configurations per app
 *
 * Format: {app}_{duration}_{price_cents}
 */
export const PRODUCT_IDS = {
  PRAYERLOCK: {
    monthly: 'prayerlock_monthly_999',
    annual: 'prayerlock_annual_4999',
  },
  WALKTOUNLOCK: {
    monthly: 'walktounlock_monthly_799',
    annual: 'walktounlock_annual_3999',
  },
  STUDYLOCK: {
    monthly: 'studylock_monthly_699',
    annual: 'studylock_annual_3499',
  },
  PROMPTVAULT: {
    monthly: 'promptvault_monthly_499',
    annual: 'promptvault_annual_2999',
  },
  DAILYANCHOR: {
    monthly: 'dailyanchor_monthly_499',
    annual: 'dailyanchor_annual_2999',
  },
  FEMFIT: {
    monthly: 'femfit_monthly_799',
    annual: 'femfit_annual_3999',
  },
  DAILYDEVOTION: {
    monthly: 'dailydevotion_monthly_499',
    annual: 'dailydevotion_annual_2499',
  },
} as const;

/**
 * App-specific configurations
 *
 * Replace placeholder API keys with your actual keys from RevenueCat dashboard.
 * Store keys in environment variables for production.
 */
export const APP_CONFIGS: Record<string, AppConfig> = {
  prayerlock: {
    appId: 'prayerlock',
    iosApiKey: process.env[ENV_KEYS.PRAYERLOCK_IOS] || 'appl_PLACEHOLDER',
    androidApiKey: process.env[ENV_KEYS.PRAYERLOCK_ANDROID],
    entitlementId: 'premium',
    products: PRODUCT_IDS.PRAYERLOCK,
  },
  walktounlock: {
    appId: 'walktounlock',
    iosApiKey: process.env[ENV_KEYS.WALKTOUNLOCK_IOS] || 'appl_PLACEHOLDER',
    androidApiKey: process.env[ENV_KEYS.WALKTOUNLOCK_ANDROID],
    entitlementId: 'premium',
    products: PRODUCT_IDS.WALKTOUNLOCK,
  },
  studylock: {
    appId: 'studylock',
    iosApiKey: process.env[ENV_KEYS.STUDYLOCK_IOS] || 'appl_PLACEHOLDER',
    androidApiKey: process.env[ENV_KEYS.STUDYLOCK_ANDROID],
    entitlementId: 'premium',
    products: PRODUCT_IDS.STUDYLOCK,
  },
  promptvault: {
    appId: 'promptvault',
    iosApiKey: process.env[ENV_KEYS.PROMPTVAULT_IOS] || 'appl_PLACEHOLDER',
    androidApiKey: process.env[ENV_KEYS.PROMPTVAULT_ANDROID],
    entitlementId: 'premium',
    products: PRODUCT_IDS.PROMPTVAULT,
  },
  dailyanchor: {
    appId: 'dailyanchor',
    iosApiKey: process.env[ENV_KEYS.DAILYANCHOR_IOS] || 'appl_PLACEHOLDER',
    androidApiKey: process.env[ENV_KEYS.DAILYANCHOR_ANDROID],
    entitlementId: 'premium',
    products: PRODUCT_IDS.DAILYANCHOR,
  },
  femfit: {
    appId: 'femfit',
    iosApiKey: process.env[ENV_KEYS.FEMFIT_IOS] || 'appl_PLACEHOLDER',
    androidApiKey: process.env[ENV_KEYS.FEMFIT_ANDROID],
    entitlementId: 'premium',
    products: PRODUCT_IDS.FEMFIT,
  },
  dailydevotion: {
    appId: 'dailydevotion',
    iosApiKey: process.env[ENV_KEYS.DAILYDEVOTION_IOS] || 'appl_PLACEHOLDER',
    androidApiKey: process.env[ENV_KEYS.DAILYDEVOTION_ANDROID],
    entitlementId: 'premium',
    products: PRODUCT_IDS.DAILYDEVOTION,
  },
};

/**
 * Get the appropriate API key for the current platform
 */
export function getApiKey(config: AppConfig): string {
  if (Platform.OS === 'ios') {
    return config.iosApiKey;
  } else if (Platform.OS === 'android') {
    if (!config.androidApiKey) {
      throw new Error(
        `Android API key not configured for app: ${config.appId}`
      );
    }
    return config.androidApiKey;
  }
  throw new Error(`Unsupported platform: ${Platform.OS}`);
}

/**
 * Get app config by app ID
 */
export function getAppConfig(appId: string): AppConfig {
  const config = APP_CONFIGS[appId.toLowerCase()];
  if (!config) {
    throw new Error(`Unknown app ID: ${appId}. Available: ${Object.keys(APP_CONFIGS).join(', ')}`);
  }
  return config;
}

/**
 * Validate that API key is not a placeholder
 */
export function isValidApiKey(apiKey: string): boolean {
  return (
    apiKey.length > 0 &&
    !apiKey.includes('PLACEHOLDER') &&
    (apiKey.startsWith('appl_') || apiKey.startsWith('goog_'))
  );
}

/**
 * Log level configuration
 */
export const LOG_LEVELS = {
  DEBUG: 'DEBUG',
  INFO: 'INFO',
  WARN: 'WARN',
  ERROR: 'ERROR',
  VERBOSE: 'VERBOSE',
} as const;

/**
 * Get log level based on environment
 */
export function getLogLevel(): keyof typeof LOG_LEVELS {
  if (__DEV__) {
    return 'DEBUG';
  }
  return 'ERROR';
}

/**
 * Feature flags for RevenueCat behavior
 */
export const FEATURE_FLAGS = {
  /** Enable debug logging in development */
  enableDebugLogs: __DEV__,
  /** Show paywall on app launch for new users */
  showPaywallOnLaunch: false,
  /** Enable automatic receipt validation */
  enableReceiptValidation: true,
  /** Enable customer info caching */
  enableCaching: true,
  /** Cache duration in milliseconds (5 minutes) */
  cacheDuration: 5 * 60 * 1000,
} as const;

/**
 * Timeout configurations
 */
export const TIMEOUTS = {
  /** SDK initialization timeout (ms) */
  initialization: 10000,
  /** Purchase operation timeout (ms) */
  purchase: 60000,
  /** Fetch offerings timeout (ms) */
  offerings: 15000,
  /** Customer info fetch timeout (ms) */
  customerInfo: 10000,
  /** Restore purchases timeout (ms) */
  restore: 30000,
} as const;

/**
 * Analytics event names
 */
export const ANALYTICS_EVENTS = {
  PAYWALL_VIEWED: 'paywall_viewed',
  PAYWALL_CLOSED: 'paywall_closed',
  PURCHASE_STARTED: 'purchase_started',
  PURCHASE_COMPLETED: 'purchase_completed',
  PURCHASE_FAILED: 'purchase_failed',
  PURCHASE_CANCELLED: 'purchase_cancelled',
  RESTORE_STARTED: 'restore_started',
  RESTORE_COMPLETED: 'restore_completed',
  RESTORE_FAILED: 'restore_failed',
  TRIAL_STARTED: 'trial_started',
  SUBSCRIPTION_ACTIVE: 'subscription_active',
  SUBSCRIPTION_EXPIRED: 'subscription_expired',
} as const;
