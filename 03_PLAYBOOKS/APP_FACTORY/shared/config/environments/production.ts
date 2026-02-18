/**
 * Production environment configuration
 *
 * Used for App Store releases.
 * Maximum security, real services, minimal logging.
 */

import { EnvironmentConfig } from './development';

export const productionConfig: EnvironmentConfig = {
  environment: 'production',

  // API - production server
  apiBaseUrl: process.env.PROD_API_URL || 'https://api.printmaxx.com',
  apiTimeout: 30000,

  // Features
  features: {
    debugMode: false, // No debug in production
    enableAnalytics: true,
    enableCrashReporting: true,
    logLevel: 'error', // Only log errors
    mockPurchases: false, // Real purchases only
    showDevMenu: false, // No dev menu in production
  },

  // External services
  services: {
    revenueCatDebug: false, // No debug logs
    stripeTestMode: false, // Live mode
  },
};

/**
 * Production-specific overrides
 *
 * Apply these when environment === 'production'
 */
export const productionOverrides = {
  // All production features enabled
  features: {
    showPaywallOnLaunch: true, // Show paywall to new users
    enablePushNotifications: true,
    enableAnalytics: true,
    enableCrashReporting: true,
    debugMode: false,
  },

  // Production API settings
  api: {
    timeout: 30000,
    retryAttempts: 3, // Retry for reliability
  },

  // Full analytics
  analytics: {
    enabled: true,
  },
};

/**
 * Production validation
 *
 * Checks to run before production builds
 */
export function validateProductionConfig(): string[] {
  const errors: string[] = [];

  // Check required environment variables
  const requiredEnvVars = [
    'REVENUECAT_IOS_KEY',
    'MIXPANEL_TOKEN',
    'SENTRY_DSN',
  ];

  for (const envVar of requiredEnvVars) {
    if (!process.env[envVar]) {
      errors.push(`Missing required environment variable: ${envVar}`);
    }
  }

  return errors;
}

export default productionConfig;
