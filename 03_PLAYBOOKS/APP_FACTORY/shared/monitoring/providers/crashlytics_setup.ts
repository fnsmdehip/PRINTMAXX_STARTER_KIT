/**
 * crashlytics_setup.ts
 * Firebase Crashlytics provider for React Native
 *
 * Installation:
 * npx expo install @react-native-firebase/app @react-native-firebase/crashlytics
 *
 * Note: Requires Firebase configuration (google-services.json / GoogleService-Info.plist)
 */

import crashlytics from '@react-native-firebase/crashlytics';
import type {
  CrashReportingProvider,
  CrashReportingConfig,
  UserContext,
  ErrorContext,
  ErrorSeverity,
  Breadcrumb,
} from '../types';

class CrashlyticsProvider implements CrashReportingProvider {
  name = 'Firebase Crashlytics';
  private isInitialized = false;
  private config: CrashReportingConfig | null = null;
  private breadcrumbs: Breadcrumb[] = [];
  private maxBreadcrumbs = 100;

  async initialize(config: CrashReportingConfig): Promise<void> {
    if (this.isInitialized) {
      console.warn('[Crashlytics] Already initialized');
      return;
    }

    this.config = config;
    this.maxBreadcrumbs = config.maxBreadcrumbs ?? 100;

    // Enable/disable collection based on config
    await crashlytics().setCrashlyticsCollectionEnabled(config.enabled ?? true);

    // Set custom keys for environment
    await crashlytics().setAttribute('environment', config.environment);

    if (config.release) {
      await crashlytics().setAttribute('release', config.release);
    }

    // In debug mode, log that we're initialized but not sending
    if (config.debug && __DEV__) {
      console.log('[Crashlytics] Initialized in debug mode (events logged locally)');
    }

    this.isInitialized = true;
  }

  setUser(user: UserContext | null): void {
    if (!user) {
      this.clearUser();
      return;
    }

    // Crashlytics requires setting user ID separately
    crashlytics().setUserId(user.id);

    // Set additional user attributes as custom keys
    const attributes: Record<string, string> = {};

    if (user.email) {
      attributes.user_email = user.email;
    }
    if (user.username) {
      attributes.user_name = user.username;
    }
    if (user.subscription_status) {
      attributes.subscription_status = user.subscription_status;
    }
    if (user.subscription_product) {
      attributes.subscription_product = user.subscription_product;
    }
    if (user.app_version) {
      attributes.app_version = user.app_version;
    }
    if (user.device_id) {
      attributes.device_id = user.device_id;
    }

    // Set all attributes at once
    crashlytics().setAttributes(attributes);
  }

  captureException(error: Error, context?: ErrorContext): void {
    if (!this.isInitialized) return;

    // Skip sending in dev unless debug is enabled
    if (__DEV__ && !this.config?.debug) {
      console.log('[Crashlytics] Exception captured (not sent in dev):', error.message);
      return;
    }

    // Set context attributes before recording
    const attributes: Record<string, string> = {};

    if (context?.severity) {
      attributes.severity = context.severity;
    }
    if (context?.category) {
      attributes.error_category = context.category;
    }
    if (context?.handled !== undefined) {
      attributes.handled = String(context.handled);
    }

    // Add tags as attributes
    if (context?.tags) {
      for (const [key, value] of Object.entries(context.tags)) {
        attributes[`tag_${key}`] = value;
      }
    }

    // Set attributes
    crashlytics().setAttributes(attributes);

    // Log breadcrumbs as messages before the error
    for (const breadcrumb of this.breadcrumbs.slice(-10)) {
      crashlytics().log(
        `[${breadcrumb.type}] ${breadcrumb.category}: ${breadcrumb.message}`
      );
    }

    // Log extra context
    if (context?.extra) {
      for (const [key, value] of Object.entries(context.extra)) {
        crashlytics().log(`Extra: ${key} = ${JSON.stringify(value)}`);
      }
    }

    // Record the error
    if (context?.severity === 'fatal') {
      // For fatal errors, use recordError which creates a non-fatal issue
      // True fatal crashes are caught automatically by Crashlytics
      crashlytics().recordError(error);
    } else {
      crashlytics().recordError(error);
    }
  }

  captureMessage(message: string, severity: ErrorSeverity = 'info'): void {
    if (!this.isInitialized) return;

    // Crashlytics doesn't have direct message capture, so we log it
    crashlytics().log(`[${severity.toUpperCase()}] ${message}`);

    // For errors and above, also record as a non-fatal
    if (severity === 'error' || severity === 'fatal') {
      crashlytics().recordError(new Error(message));
    }
  }

  addBreadcrumb(breadcrumb: Breadcrumb): void {
    if (!this.isInitialized) return;

    // Store breadcrumb locally (Crashlytics doesn't have native breadcrumb support)
    this.breadcrumbs.push(breadcrumb);

    // Trim to max size
    if (this.breadcrumbs.length > this.maxBreadcrumbs) {
      this.breadcrumbs = this.breadcrumbs.slice(-this.maxBreadcrumbs);
    }

    // Also log to Crashlytics
    const timestamp = breadcrumb.timestamp
      ? new Date(breadcrumb.timestamp).toISOString()
      : new Date().toISOString();

    crashlytics().log(
      `[${timestamp}] ${breadcrumb.type}/${breadcrumb.category}: ${breadcrumb.message}`
    );
  }

  setTag(key: string, value: string): void {
    if (!this.isInitialized) return;
    crashlytics().setAttribute(key, value);
  }

  setExtra(key: string, value: unknown): void {
    if (!this.isInitialized) return;
    crashlytics().setAttribute(key, JSON.stringify(value));
  }

  clearUser(): void {
    // Crashlytics doesn't have a direct clear user, but we can set to empty
    crashlytics().setUserId('');
    crashlytics().setAttributes({
      user_email: '',
      user_name: '',
      subscription_status: '',
      subscription_product: '',
    });
  }

  async flush(): Promise<void> {
    // Crashlytics doesn't require manual flushing
    // Events are sent automatically
    if (!this.isInitialized) return;

    // Clear local breadcrumbs after flush
    this.breadcrumbs = [];
  }

  /**
   * Force a crash for testing purposes
   * WARNING: This will crash the app
   */
  testCrash(): void {
    crashlytics().crash();
  }

  /**
   * Check if Crashlytics collection is enabled
   */
  async isCollectionEnabled(): Promise<boolean> {
    return crashlytics().isCrashlyticsCollectionEnabled;
  }

  /**
   * Check if the app crashed in the previous session
   */
  async didCrashInPreviousSession(): Promise<boolean> {
    return crashlytics().didCrashOnPreviousExecution();
  }

  /**
   * Enable or disable Crashlytics collection at runtime
   */
  async setCollectionEnabled(enabled: boolean): Promise<void> {
    await crashlytics().setCrashlyticsCollectionEnabled(enabled);
  }
}

// Export singleton instance
export const crashlyticsProvider = new CrashlyticsProvider();

/**
 * Hook for checking if app crashed previously
 */
export async function checkPreviousCrash(): Promise<{
  crashed: boolean;
}> {
  const crashed = await crashlytics().didCrashOnPreviousExecution();
  return { crashed };
}

/**
 * Utility to log custom message to Crashlytics
 */
export function logToCrashlytics(message: string): void {
  crashlytics().log(message);
}

/**
 * Utility to set custom key in Crashlytics
 */
export function setCrashlyticsAttribute(key: string, value: string): void {
  crashlytics().setAttribute(key, value);
}

/**
 * Record a non-fatal error to Crashlytics
 */
export function recordCrashlyticsError(error: Error): void {
  crashlytics().recordError(error);
}

export default crashlyticsProvider;
