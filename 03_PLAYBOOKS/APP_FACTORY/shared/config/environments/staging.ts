/**
 * Staging environment configuration
 *
 * Used for QA testing and pre-production validation.
 * Connects to staging services with production-like settings.
 */

import { EnvironmentConfig } from './development';

export const stagingConfig: EnvironmentConfig = {
  environment: 'staging',

  // API - staging server
  apiBaseUrl: process.env.STAGING_API_URL || 'https://staging.api.printmaxx.com',
  apiTimeout: 30000,

  // Features
  features: {
    debugMode: true, // Still enable debug for QA
    enableAnalytics: true, // Track for comparison with prod
    enableCrashReporting: true, // Catch issues before prod
    logLevel: 'info',
    mockPurchases: false, // Use real sandbox purchases
    showDevMenu: true, // Allow testers to access dev menu
  },

  // External services
  services: {
    revenueCatDebug: true, // Still show logs for debugging
    stripeTestMode: true, // Use Stripe test mode
  },
};

/**
 * Staging-specific overrides
 *
 * Apply these when environment === 'staging'
 */
export const stagingOverrides = {
  // Test paywall flows
  features: {
    showPaywallOnLaunch: true, // Test paywall experience
    enablePushNotifications: true, // Test notifications
    enableCrashReporting: true,
    debugMode: true,
  },

  // Staging API settings
  api: {
    timeout: 30000,
    retryAttempts: 2,
  },

  // Analytics enabled for comparison
  analytics: {
    enabled: true,
  },
};

export default stagingConfig;
