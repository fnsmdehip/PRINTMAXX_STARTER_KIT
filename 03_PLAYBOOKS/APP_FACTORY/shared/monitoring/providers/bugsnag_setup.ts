/**
 * bugsnag_setup.ts
 * Bugsnag crash reporting provider for React Native
 *
 * Installation:
 * npx expo install @bugsnag/react-native @bugsnag/plugin-react-native-navigation
 */

import Bugsnag from '@bugsnag/react-native';
import type {
  CrashReportingProvider,
  CrashReportingConfig,
  UserContext,
  ErrorContext,
  ErrorSeverity,
  Breadcrumb,
} from '../types';

// Map our severity to Bugsnag severity
const SEVERITY_MAP: Record<ErrorSeverity, 'error' | 'warning' | 'info'> = {
  fatal: 'error',
  error: 'error',
  warning: 'warning',
  info: 'info',
  debug: 'info',
};

// Map our breadcrumb types to Bugsnag types
type BugsnagBreadcrumbType =
  | 'navigation'
  | 'request'
  | 'process'
  | 'log'
  | 'user'
  | 'state'
  | 'error'
  | 'manual';

const BREADCRUMB_TYPE_MAP: Record<string, BugsnagBreadcrumbType> = {
  navigation: 'navigation',
  user: 'user',
  http: 'request',
  ui: 'user',
  console: 'log',
  error: 'error',
  transaction: 'process',
  query: 'request',
};

class BugsnagProvider implements CrashReportingProvider {
  name = 'Bugsnag';
  private isInitialized = false;
  private config: CrashReportingConfig | null = null;

  async initialize(config: CrashReportingConfig): Promise<void> {
    if (this.isInitialized) {
      console.warn('[Bugsnag] Already initialized');
      return;
    }

    if (!config.apiKey) {
      throw new Error('[Bugsnag] API key is required for initialization');
    }

    this.config = config;

    Bugsnag.start({
      apiKey: config.apiKey,
      releaseStage: config.environment,
      appVersion: config.release,

      // Only send events in production unless debug is enabled
      enabledReleaseStages: config.debug
        ? ['development', 'staging', 'production']
        : ['staging', 'production'],

      // Enable breadcrumb collection
      enabledBreadcrumbTypes: [
        'navigation',
        'request',
        'process',
        'log',
        'user',
        'state',
        'error',
      ],

      // Max breadcrumbs
      maxBreadcrumbs: config.maxBreadcrumbs ?? 100,

      // Callbacks for filtering
      onError: (event) => {
        // Apply sample rate
        const sampleRate = config.sampleRate ?? 1.0;
        if (Math.random() > sampleRate) {
          return false;
        }

        // Apply custom filter if provided
        if (config.beforeSend) {
          const customEvent = config.beforeSend({
            event_id: event.errors[0]?.errorMessage || '',
            timestamp: new Date().toISOString(),
            platform: 'ios',
            environment: config.environment,
            release: config.release,
            exception: {
              type: event.errors[0]?.errorClass || 'Error',
              value: event.errors[0]?.errorMessage || '',
            },
          });

          if (!customEvent) {
            return false;
          }
        }

        return true;
      },

      // Metadata plugins
      plugins: [],
    });

    // Set global metadata
    Bugsnag.addMetadata('app', {
      environment: config.environment,
      debug: config.debug,
    });

    this.isInitialized = true;
  }

  setUser(user: UserContext | null): void {
    if (!user) {
      this.clearUser();
      return;
    }

    Bugsnag.setUser(user.id, user.email, user.username);

    // Add additional user data as metadata
    Bugsnag.addMetadata('user_profile', {
      subscription_status: user.subscription_status,
      subscription_product: user.subscription_product,
      app_version: user.app_version,
      device_id: user.device_id,
    });
  }

  captureException(error: Error, context?: ErrorContext): void {
    if (!this.isInitialized) return;

    Bugsnag.notify(error, (event) => {
      // Set severity
      if (context?.severity) {
        event.severity = SEVERITY_MAP[context.severity];
      }

      // Set unhandled flag
      if (context?.handled === false) {
        event.unhandled = true;
      }

      // Add error category
      if (context?.category) {
        event.addMetadata('error_info', { category: context.category });
      }

      // Add tags as metadata
      if (context?.tags) {
        event.addMetadata('tags', context.tags);
      }

      // Add extra context
      if (context?.extra) {
        event.addMetadata('context', context.extra);
      }

      // Set fingerprint for grouping
      if (context?.fingerprint) {
        event.groupingHash = context.fingerprint.join('_');
      }
    });
  }

  captureMessage(message: string, severity: ErrorSeverity = 'info'): void {
    if (!this.isInitialized) return;

    // Bugsnag doesn't have a direct message capture, so we create an error
    const messageError = new Error(message);
    messageError.name = 'Message';

    Bugsnag.notify(messageError, (event) => {
      event.severity = SEVERITY_MAP[severity];
      event.addMetadata('message_info', { is_message: true });
    });
  }

  addBreadcrumb(breadcrumb: Breadcrumb): void {
    if (!this.isInitialized) return;

    Bugsnag.leaveBreadcrumb(
      breadcrumb.message,
      breadcrumb.data || {},
      BREADCRUMB_TYPE_MAP[breadcrumb.type] || 'manual'
    );
  }

  setTag(key: string, value: string): void {
    if (!this.isInitialized) return;
    Bugsnag.addMetadata('tags', { [key]: value });
  }

  setExtra(key: string, value: unknown): void {
    if (!this.isInitialized) return;
    Bugsnag.addMetadata('extra', { [key]: value });
  }

  clearUser(): void {
    Bugsnag.setUser(undefined, undefined, undefined);
    Bugsnag.clearMetadata('user_profile');
  }

  async flush(): Promise<void> {
    // Bugsnag automatically manages event delivery
    // This method is here for interface compatibility
    if (!this.isInitialized) return;
  }

  /**
   * Start a new session (useful for tracking session-based crash rates)
   */
  startSession(): void {
    if (!this.isInitialized) return;
    Bugsnag.startSession();
  }

  /**
   * Pause session tracking (e.g., when app goes to background)
   */
  pauseSession(): void {
    if (!this.isInitialized) return;
    Bugsnag.pauseSession();
  }

  /**
   * Resume session tracking
   */
  resumeSession(): boolean {
    if (!this.isInitialized) return false;
    return Bugsnag.resumeSession();
  }

  /**
   * Add metadata section
   */
  addMetadata(section: string, data: Record<string, unknown>): void {
    if (!this.isInitialized) return;
    Bugsnag.addMetadata(section, data);
  }

  /**
   * Clear metadata section
   */
  clearMetadata(section: string): void {
    if (!this.isInitialized) return;
    Bugsnag.clearMetadata(section);
  }

  /**
   * Get the Bugsnag client for advanced usage
   */
  getClient(): typeof Bugsnag {
    return Bugsnag;
  }
}

// Export singleton instance
export const bugsnagProvider = new BugsnagProvider();

/**
 * Higher-order component for Bugsnag error boundary
 */
export function createBugsnagErrorBoundary() {
  return Bugsnag.getPlugin('react')?.createErrorBoundary();
}

/**
 * Utility to notify Bugsnag of an error directly
 */
export function notifyBugsnag(
  error: Error,
  onError?: (event: { severity: string; addMetadata: (section: string, data: unknown) => void }) => void
): void {
  Bugsnag.notify(error, onError);
}

/**
 * Utility to leave a breadcrumb directly
 */
export function leaveBugsnagBreadcrumb(
  message: string,
  metadata?: Record<string, unknown>,
  type?: BugsnagBreadcrumbType
): void {
  Bugsnag.leaveBreadcrumb(message, metadata, type || 'manual');
}

/**
 * Add feature flag for Bugsnag feature flags integration
 */
export function addBugsnagFeatureFlag(name: string, variant?: string): void {
  Bugsnag.addFeatureFlag(name, variant);
}

/**
 * Clear all feature flags
 */
export function clearBugsnagFeatureFlags(): void {
  Bugsnag.clearFeatureFlags();
}

export default bugsnagProvider;
