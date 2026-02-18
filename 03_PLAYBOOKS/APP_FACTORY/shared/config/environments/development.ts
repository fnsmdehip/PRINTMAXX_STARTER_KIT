/**
 * Development environment configuration
 *
 * Used when running locally with Metro bundler.
 * Enables debug features and uses local/mock services.
 */

import { Environment } from './index';

export interface EnvironmentConfig {
  environment: Environment;
  apiBaseUrl: string;
  apiTimeout: number;
  features: {
    debugMode: boolean;
    enableAnalytics: boolean;
    enableCrashReporting: boolean;
    logLevel: 'debug' | 'info' | 'warn' | 'error';
    mockPurchases: boolean;
    showDevMenu: boolean;
  };
  services: {
    revenueCatDebug: boolean;
    stripeTestMode: boolean;
  };
}

export const developmentConfig: EnvironmentConfig = {
  environment: 'development',

  // API
  apiBaseUrl: process.env.DEV_API_URL || 'http://localhost:3000/api',
  apiTimeout: 60000, // Longer timeout for debugging

  // Features
  features: {
    debugMode: true,
    enableAnalytics: false, // Don't pollute analytics with dev data
    enableCrashReporting: false,
    logLevel: 'debug',
    mockPurchases: true, // Use mock purchases in dev
    showDevMenu: true,
  },

  // External services
  services: {
    revenueCatDebug: true, // Enable RevenueCat debug logs
    stripeTestMode: true,
  },
};

/**
 * Development-specific overrides
 *
 * Apply these when environment === 'development'
 */
export const developmentOverrides = {
  // Disable production-only features
  features: {
    showPaywallOnLaunch: false,
    enablePushNotifications: false,
  },

  // Use sandbox APIs
  api: {
    timeout: 60000,
    retryAttempts: 1, // Fail fast in development
  },

  // Analytics disabled
  analytics: {
    enabled: false,
  },
};

export default developmentConfig;
