/**
 * sentry_setup.ts
 * Sentry crash reporting provider for React Native
 *
 * Installation:
 * npx expo install @sentry/react-native
 */

import * as Sentry from '@sentry/react-native';
import type {
  CrashReportingProvider,
  CrashReportingConfig,
  UserContext,
  ErrorContext,
  ErrorSeverity,
  Breadcrumb,
} from '../types';

// Map our severity to Sentry severity
const SEVERITY_MAP: Record<ErrorSeverity, Sentry.SeverityLevel> = {
  fatal: 'fatal',
  error: 'error',
  warning: 'warning',
  info: 'info',
  debug: 'debug',
};

// Map our breadcrumb types to Sentry types
const BREADCRUMB_TYPE_MAP: Record<string, string> = {
  navigation: 'navigation',
  user: 'user',
  http: 'http',
  ui: 'ui',
  console: 'console',
  error: 'error',
  transaction: 'transaction',
  query: 'query',
};

class SentryProvider implements CrashReportingProvider {
  name = 'Sentry';
  private isInitialized = false;
  private config: CrashReportingConfig | null = null;

  async initialize(config: CrashReportingConfig): Promise<void> {
    if (this.isInitialized) {
      console.warn('[Sentry] Already initialized');
      return;
    }

    if (!config.dsn) {
      throw new Error('[Sentry] DSN is required for initialization');
    }

    this.config = config;

    Sentry.init({
      dsn: config.dsn,
      environment: config.environment,
      release: config.release,
      debug: config.debug,
      enabled: config.enabled ?? true,

      // Sample rates
      sampleRate: config.sampleRate ?? 1.0,
      tracesSampleRate: config.tracesSampleRate ?? 0.2,

      // Attach stack traces to all events
      attachStacktrace: config.attachStacktrace ?? true,

      // Max breadcrumbs to keep
      maxBreadcrumbs: config.maxBreadcrumbs ?? 100,

      // Filter events before sending
      beforeSend: (event) => {
        // Apply custom beforeSend if provided
        if (config.beforeSend) {
          // Transform Sentry event to our format for the filter
          const customEvent = config.beforeSend({
            event_id: event.event_id || '',
            timestamp: event.timestamp || new Date().toISOString(),
            platform: 'ios',
            environment: config.environment,
            release: config.release,
            exception: {
              type: event.exception?.values?.[0]?.type || 'Error',
              value: event.exception?.values?.[0]?.value || '',
            },
          });

          if (!customEvent) {
            return null;
          }
        }

        // Don't send events in development unless explicitly enabled
        if (__DEV__ && !config.debug) {
          console.log('[Sentry] Event captured (not sent in dev):', event);
          return null;
        }

        return event;
      },

      // Integrations
      integrations: [
        // Enable native crash reporting
        new Sentry.ReactNativeTracing({
          routingInstrumentation: new Sentry.ReactNavigationInstrumentation(),
        }),
      ],
    });

    this.isInitialized = true;
  }

  setUser(user: UserContext | null): void {
    if (!user) {
      Sentry.setUser(null);
      return;
    }

    Sentry.setUser({
      id: user.id,
      email: user.email,
      username: user.username,
      ...user,
    });
  }

  captureException(error: Error, context?: ErrorContext): void {
    if (!this.isInitialized) return;

    Sentry.withScope((scope) => {
      // Set severity
      if (context?.severity) {
        scope.setLevel(SEVERITY_MAP[context.severity]);
      }

      // Set tags
      if (context?.tags) {
        for (const [key, value] of Object.entries(context.tags)) {
          scope.setTag(key, value);
        }
      }

      // Set category tag
      if (context?.category) {
        scope.setTag('error_category', context.category);
      }

      // Set handled flag
      if (context?.handled !== undefined) {
        scope.setTag('handled', String(context.handled));
      }

      // Set extra context
      if (context?.extra) {
        for (const [key, value] of Object.entries(context.extra)) {
          scope.setExtra(key, value);
        }
      }

      // Set fingerprint for grouping
      if (context?.fingerprint) {
        scope.setFingerprint(context.fingerprint);
      }

      Sentry.captureException(error);
    });
  }

  captureMessage(message: string, severity: ErrorSeverity = 'info'): void {
    if (!this.isInitialized) return;

    Sentry.captureMessage(message, SEVERITY_MAP[severity]);
  }

  addBreadcrumb(breadcrumb: Breadcrumb): void {
    if (!this.isInitialized) return;

    Sentry.addBreadcrumb({
      type: BREADCRUMB_TYPE_MAP[breadcrumb.type] || 'default',
      category: breadcrumb.category,
      message: breadcrumb.message,
      data: breadcrumb.data,
      level: breadcrumb.level ? SEVERITY_MAP[breadcrumb.level] : undefined,
      timestamp: breadcrumb.timestamp ? breadcrumb.timestamp / 1000 : undefined,
    });
  }

  setTag(key: string, value: string): void {
    if (!this.isInitialized) return;
    Sentry.setTag(key, value);
  }

  setExtra(key: string, value: unknown): void {
    if (!this.isInitialized) return;
    Sentry.setExtra(key, value);
  }

  clearUser(): void {
    Sentry.setUser(null);
  }

  async flush(): Promise<void> {
    if (!this.isInitialized) return;
    await Sentry.flush(2000);
  }
}

// Export singleton instance
export const sentryProvider = new SentryProvider();

/**
 * Higher-order component for Sentry error boundary
 */
export function withSentryErrorBoundary<P extends object>(
  Component: React.ComponentType<P>,
  fallback: React.ReactNode
): React.ComponentType<P> {
  return Sentry.withErrorBoundary(Component, { fallback });
}

/**
 * Navigation container wrapper for Sentry routing instrumentation
 */
export function getSentryNavigationIntegration() {
  return new Sentry.ReactNavigationInstrumentation();
}

/**
 * Create Sentry-wrapped navigation container
 */
export const SentryNavigationContainer = Sentry.wrap;

/**
 * Start a Sentry transaction for performance monitoring
 */
export function startTransaction(name: string, operation: string) {
  return Sentry.startTransaction({ name, op: operation });
}

/**
 * Utility to capture exception with Sentry directly
 */
export function captureSentryException(
  error: Error,
  captureContext?: Sentry.CaptureContext
): string {
  return Sentry.captureException(error, captureContext);
}

export default sentryProvider;
