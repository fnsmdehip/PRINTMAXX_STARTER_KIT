/**
 * CrashReportingService.ts
 * Core crash reporting service for React Native apps
 * Handles error capture, user context, breadcrumbs, and provider management
 */

import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import type {
  CrashReportingProvider,
  CrashReportingConfig,
  UserContext,
  ErrorContext,
  ErrorSeverity,
  ErrorCategory,
  Breadcrumb,
  BreadcrumbType,
} from './types';

// Storage keys
const STORAGE_KEYS = {
  USER_CONTEXT: '@crash_reporting_user',
  OFFLINE_EVENTS: '@crash_reporting_offline_events',
  SESSION_ID: '@crash_reporting_session_id',
} as const;

// Default configuration
const DEFAULT_CONFIG: Partial<CrashReportingConfig> = {
  enabled: true,
  debug: __DEV__,
  sampleRate: 1.0,
  tracesSampleRate: 0.2,
  attachStacktrace: true,
  maxBreadcrumbs: 100,
};

// Error categorization rules
const ERROR_PATTERNS: Array<{ pattern: RegExp; category: ErrorCategory }> = [
  { pattern: /network|fetch|timeout|connection/i, category: 'network' },
  { pattern: /auth|login|token|unauthorized|forbidden/i, category: 'authentication' },
  { pattern: /validation|invalid|required|format/i, category: 'validation' },
  { pattern: /storage|asyncstorage|persist|cache/i, category: 'storage' },
  { pattern: /navigation|route|screen|navigate/i, category: 'navigation' },
  { pattern: /render|component|hook|state/i, category: 'rendering' },
  { pattern: /api|endpoint|response|request/i, category: 'api' },
  { pattern: /payment|purchase|subscription|billing/i, category: 'payment' },
  { pattern: /permission|denied|access/i, category: 'permission' },
];

class CrashReportingService {
  private providers: CrashReportingProvider[] = [];
  private config: CrashReportingConfig | null = null;
  private userContext: UserContext | null = null;
  private breadcrumbs: Breadcrumb[] = [];
  private sessionId: string | null = null;
  private isInitialized = false;
  private offlineEvents: Array<{ error: Error; context?: ErrorContext }> = [];

  /**
   * Initialize the crash reporting service with providers
   */
  async initialize(
    config: CrashReportingConfig,
    providers: CrashReportingProvider[]
  ): Promise<void> {
    if (this.isInitialized) {
      console.warn('CrashReportingService already initialized');
      return;
    }

    this.config = { ...DEFAULT_CONFIG, ...config };
    this.providers = providers;

    // Generate or load session ID
    this.sessionId = await this.getOrCreateSessionId();

    // Initialize all providers
    const initPromises = providers.map(async (provider) => {
      try {
        await provider.initialize(this.config!);
        if (this.config?.debug) {
          console.log(`[CrashReporting] ${provider.name} initialized`);
        }
      } catch (error) {
        console.error(`[CrashReporting] Failed to initialize ${provider.name}:`, error);
      }
    });

    await Promise.all(initPromises);

    // Load stored user context
    await this.loadUserContext();

    // Process any offline events
    await this.processOfflineEvents();

    // Set up global error handler
    this.setupGlobalErrorHandler();

    this.isInitialized = true;

    // Add initialization breadcrumb
    this.addBreadcrumb({
      type: 'navigation',
      category: 'app.lifecycle',
      message: 'Crash reporting initialized',
      data: {
        providers: providers.map((p) => p.name),
        environment: config.environment,
      },
    });
  }

  /**
   * Set up global error handlers
   */
  private setupGlobalErrorHandler(): void {
    // Handle unhandled JS errors
    const originalHandler = ErrorUtils.getGlobalHandler();
    ErrorUtils.setGlobalHandler((error: Error, isFatal?: boolean) => {
      this.captureException(error, {
        severity: isFatal ? 'fatal' : 'error',
        handled: false,
        tags: { unhandled: 'true', fatal: String(isFatal) },
      });

      // Call original handler
      if (originalHandler) {
        originalHandler(error, isFatal);
      }
    });

    // Handle unhandled promise rejections
    if (typeof global !== 'undefined') {
      const rejectionHandler = (id: string, error: Error) => {
        this.captureException(error, {
          severity: 'error',
          handled: false,
          tags: { type: 'unhandled_promise_rejection', rejection_id: id },
        });
      };

      // @ts-ignore - React Native specific
      if (global.HermesInternal) {
        // @ts-ignore
        global.HermesInternal.enablePromiseRejectionTracker?.(
          { allRejections: true },
          rejectionHandler
        );
      }
    }
  }

  /**
   * Set user context for error attribution
   */
  async setUser(user: UserContext): Promise<void> {
    this.userContext = user;
    await AsyncStorage.setItem(STORAGE_KEYS.USER_CONTEXT, JSON.stringify(user));

    for (const provider of this.providers) {
      try {
        provider.setUser(user);
      } catch (error) {
        console.error(`[CrashReporting] Failed to set user in ${provider.name}:`, error);
      }
    }

    this.addBreadcrumb({
      type: 'user',
      category: 'auth',
      message: 'User context set',
      data: { user_id: user.id },
    });
  }

  /**
   * Clear user context (e.g., on logout)
   */
  async clearUser(): Promise<void> {
    this.userContext = null;
    await AsyncStorage.removeItem(STORAGE_KEYS.USER_CONTEXT);

    for (const provider of this.providers) {
      try {
        provider.clearUser();
      } catch (error) {
        console.error(`[CrashReporting] Failed to clear user in ${provider.name}:`, error);
      }
    }

    this.addBreadcrumb({
      type: 'user',
      category: 'auth',
      message: 'User context cleared',
    });
  }

  /**
   * Capture an exception
   */
  captureException(error: Error, context?: ErrorContext): void {
    if (!this.shouldCapture()) {
      return;
    }

    // Auto-categorize if not provided
    const category = context?.category || this.categorizeError(error);

    // Enrich context
    const enrichedContext: ErrorContext = {
      severity: context?.severity || 'error',
      category,
      handled: context?.handled ?? true,
      tags: {
        ...context?.tags,
        platform: Platform.OS,
        session_id: this.sessionId || 'unknown',
      },
      extra: {
        ...context?.extra,
        error_name: error.name,
        error_message: error.message,
        breadcrumbs_count: this.breadcrumbs.length,
      },
    };

    // Add error breadcrumb
    this.addBreadcrumb({
      type: 'error',
      category: category,
      message: error.message,
      level: enrichedContext.severity,
      data: { error_name: error.name },
    });

    // Send to all providers
    for (const provider of this.providers) {
      try {
        provider.captureException(error, enrichedContext);
      } catch (providerError) {
        console.error(
          `[CrashReporting] Failed to capture exception in ${provider.name}:`,
          providerError
        );
      }
    }

    if (this.config?.debug) {
      console.log('[CrashReporting] Exception captured:', {
        error: error.message,
        category,
        severity: enrichedContext.severity,
      });
    }
  }

  /**
   * Capture a message (non-exception event)
   */
  captureMessage(message: string, severity: ErrorSeverity = 'info'): void {
    if (!this.shouldCapture()) {
      return;
    }

    for (const provider of this.providers) {
      try {
        provider.captureMessage(message, severity);
      } catch (error) {
        console.error(`[CrashReporting] Failed to capture message in ${provider.name}:`, error);
      }
    }

    this.addBreadcrumb({
      type: 'console',
      category: 'log',
      message,
      level: severity,
    });
  }

  /**
   * Add a breadcrumb for tracking user flow
   */
  addBreadcrumb(breadcrumb: Breadcrumb): void {
    const maxBreadcrumbs = this.config?.maxBreadcrumbs || 100;

    const enrichedBreadcrumb: Breadcrumb = {
      ...breadcrumb,
      timestamp: breadcrumb.timestamp || Date.now(),
    };

    this.breadcrumbs.push(enrichedBreadcrumb);

    // Trim to max size
    if (this.breadcrumbs.length > maxBreadcrumbs) {
      this.breadcrumbs = this.breadcrumbs.slice(-maxBreadcrumbs);
    }

    // Send to providers
    for (const provider of this.providers) {
      try {
        provider.addBreadcrumb(enrichedBreadcrumb);
      } catch (error) {
        // Silently fail for breadcrumbs
      }
    }
  }

  /**
   * Track screen navigation
   */
  trackScreen(screenName: string, params?: Record<string, unknown>): void {
    this.addBreadcrumb({
      type: 'navigation',
      category: 'screen',
      message: `Navigated to ${screenName}`,
      data: params,
    });
  }

  /**
   * Track user action
   */
  trackAction(action: string, data?: Record<string, unknown>): void {
    this.addBreadcrumb({
      type: 'user',
      category: 'action',
      message: action,
      data,
    });
  }

  /**
   * Track network request
   */
  trackNetworkRequest(
    url: string,
    method: string,
    statusCode?: number,
    durationMs?: number
  ): void {
    this.addBreadcrumb({
      type: 'http',
      category: 'network',
      message: `${method} ${url}`,
      data: {
        url,
        method,
        status_code: statusCode,
        duration_ms: durationMs,
      },
      level: statusCode && statusCode >= 400 ? 'error' : 'info',
    });
  }

  /**
   * Set a tag for all future events
   */
  setTag(key: string, value: string): void {
    for (const provider of this.providers) {
      try {
        provider.setTag(key, value);
      } catch (error) {
        console.error(`[CrashReporting] Failed to set tag in ${provider.name}:`, error);
      }
    }
  }

  /**
   * Set extra data for all future events
   */
  setExtra(key: string, value: unknown): void {
    for (const provider of this.providers) {
      try {
        provider.setExtra(key, value);
      } catch (error) {
        console.error(`[CrashReporting] Failed to set extra in ${provider.name}:`, error);
      }
    }
  }

  /**
   * Flush pending events (useful before app closes)
   */
  async flush(): Promise<void> {
    const flushPromises = this.providers.map(async (provider) => {
      try {
        await provider.flush();
      } catch (error) {
        console.error(`[CrashReporting] Failed to flush ${provider.name}:`, error);
      }
    });

    await Promise.all(flushPromises);
  }

  /**
   * Get current breadcrumbs
   */
  getBreadcrumbs(): Breadcrumb[] {
    return [...this.breadcrumbs];
  }

  /**
   * Clear breadcrumbs
   */
  clearBreadcrumbs(): void {
    this.breadcrumbs = [];
  }

  /**
   * Get current user context
   */
  getUser(): UserContext | null {
    return this.userContext;
  }

  /**
   * Get current session ID
   */
  getSessionId(): string | null {
    return this.sessionId;
  }

  /**
   * Check if service is initialized
   */
  isReady(): boolean {
    return this.isInitialized;
  }

  /**
   * Auto-categorize error based on message
   */
  private categorizeError(error: Error): ErrorCategory {
    const message = `${error.name} ${error.message}`;

    for (const { pattern, category } of ERROR_PATTERNS) {
      if (pattern.test(message)) {
        return category;
      }
    }

    return 'unknown';
  }

  /**
   * Check if should capture based on sample rate
   */
  private shouldCapture(): boolean {
    if (!this.config?.enabled) {
      return false;
    }

    const sampleRate = this.config.sampleRate || 1.0;
    return Math.random() < sampleRate;
  }

  /**
   * Get or create session ID
   */
  private async getOrCreateSessionId(): Promise<string> {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.SESSION_ID);
      if (stored) {
        return stored;
      }

      const newId = `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
      await AsyncStorage.setItem(STORAGE_KEYS.SESSION_ID, newId);
      return newId;
    } catch {
      return `session_${Date.now()}`;
    }
  }

  /**
   * Load user context from storage
   */
  private async loadUserContext(): Promise<void> {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.USER_CONTEXT);
      if (stored) {
        this.userContext = JSON.parse(stored);
        for (const provider of this.providers) {
          provider.setUser(this.userContext!);
        }
      }
    } catch (error) {
      console.error('[CrashReporting] Failed to load user context:', error);
    }
  }

  /**
   * Store event for offline processing
   */
  async storeOfflineEvent(error: Error, context?: ErrorContext): Promise<void> {
    this.offlineEvents.push({ error, context });
    try {
      await AsyncStorage.setItem(
        STORAGE_KEYS.OFFLINE_EVENTS,
        JSON.stringify(this.offlineEvents)
      );
    } catch {
      // Silently fail
    }
  }

  /**
   * Process stored offline events
   */
  private async processOfflineEvents(): Promise<void> {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.OFFLINE_EVENTS);
      if (stored) {
        const events = JSON.parse(stored) as Array<{ error: Error; context?: ErrorContext }>;
        for (const { error, context } of events) {
          this.captureException(error, {
            ...context,
            tags: { ...context?.tags, offline: 'true' },
          });
        }
        await AsyncStorage.removeItem(STORAGE_KEYS.OFFLINE_EVENTS);
      }
    } catch (error) {
      console.error('[CrashReporting] Failed to process offline events:', error);
    }
  }
}

// Export singleton instance
export const crashReportingService = new CrashReportingService();
export default crashReportingService;
