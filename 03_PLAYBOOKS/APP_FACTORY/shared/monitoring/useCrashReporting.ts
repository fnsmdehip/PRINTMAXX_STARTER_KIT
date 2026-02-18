/**
 * useCrashReporting.ts
 * React hook for crash reporting integration
 * Provides error boundary integration, manual logging, and breadcrumb tracking
 */

import { useEffect, useCallback, useRef, useMemo } from 'react';
import { AppState, AppStateStatus } from 'react-native';
import crashReportingService from './CrashReportingService';
import type {
  ErrorContext,
  ErrorSeverity,
  ErrorCategory,
  UserContext,
  Breadcrumb,
  BreadcrumbType,
} from './types';

interface UseCrashReportingOptions {
  // Automatically track screen views
  screenName?: string;
  screenParams?: Record<string, unknown>;

  // Component identification for error context
  componentName?: string;

  // Auto-track app state changes
  trackAppState?: boolean;
}

interface UseCrashReportingReturn {
  // Error capture
  captureError: (error: Error, context?: ErrorContext) => void;
  captureWarning: (message: string, data?: Record<string, unknown>) => void;
  captureInfo: (message: string, data?: Record<string, unknown>) => void;

  // User management
  setUser: (user: UserContext) => Promise<void>;
  clearUser: () => Promise<void>;

  // Breadcrumbs
  addBreadcrumb: (breadcrumb: Breadcrumb) => void;
  trackAction: (action: string, data?: Record<string, unknown>) => void;
  trackNavigation: (screenName: string, params?: Record<string, unknown>) => void;

  // Tags and extras
  setTag: (key: string, value: string) => void;
  setExtra: (key: string, value: unknown) => void;

  // Utilities
  wrapAsync: <T>(fn: () => Promise<T>, context?: string) => Promise<T>;
  wrapCallback: <T extends (...args: unknown[]) => unknown>(
    fn: T,
    context?: string
  ) => T;
}

export function useCrashReporting(
  options: UseCrashReportingOptions = {}
): UseCrashReportingReturn {
  const { screenName, screenParams, componentName, trackAppState = true } = options;

  // Track previous app state
  const appStateRef = useRef(AppState.currentState);

  // Track component mount for error context
  const componentContextRef = useRef({
    componentName,
    mountedAt: new Date().toISOString(),
  });

  // Track screen view on mount
  useEffect(() => {
    if (screenName) {
      crashReportingService.trackScreen(screenName, screenParams);
    }
  }, [screenName, screenParams]);

  // Track app state changes
  useEffect(() => {
    if (!trackAppState) return;

    const handleAppStateChange = (nextState: AppStateStatus) => {
      crashReportingService.addBreadcrumb({
        type: 'navigation',
        category: 'app.lifecycle',
        message: `App state changed: ${appStateRef.current} -> ${nextState}`,
        data: {
          previous: appStateRef.current,
          current: nextState,
        },
      });

      appStateRef.current = nextState;
    };

    const subscription = AppState.addEventListener('change', handleAppStateChange);
    return () => subscription.remove();
  }, [trackAppState]);

  // Capture error with component context
  const captureError = useCallback(
    (error: Error, context?: ErrorContext) => {
      const enrichedContext: ErrorContext = {
        ...context,
        extra: {
          ...context?.extra,
          component: componentContextRef.current.componentName,
          component_mounted_at: componentContextRef.current.mountedAt,
        },
      };

      crashReportingService.captureException(error, enrichedContext);
    },
    []
  );

  // Capture warning message
  const captureWarning = useCallback(
    (message: string, data?: Record<string, unknown>) => {
      crashReportingService.captureMessage(message, 'warning');
      if (data) {
        crashReportingService.addBreadcrumb({
          type: 'console',
          category: 'warning',
          message,
          data,
          level: 'warning',
        });
      }
    },
    []
  );

  // Capture info message
  const captureInfo = useCallback(
    (message: string, data?: Record<string, unknown>) => {
      crashReportingService.captureMessage(message, 'info');
      if (data) {
        crashReportingService.addBreadcrumb({
          type: 'console',
          category: 'info',
          message,
          data,
          level: 'info',
        });
      }
    },
    []
  );

  // Set user context
  const setUser = useCallback(async (user: UserContext) => {
    await crashReportingService.setUser(user);
  }, []);

  // Clear user context
  const clearUser = useCallback(async () => {
    await crashReportingService.clearUser();
  }, []);

  // Add breadcrumb
  const addBreadcrumb = useCallback((breadcrumb: Breadcrumb) => {
    crashReportingService.addBreadcrumb(breadcrumb);
  }, []);

  // Track user action
  const trackAction = useCallback((action: string, data?: Record<string, unknown>) => {
    crashReportingService.trackAction(action, data);
  }, []);

  // Track navigation
  const trackNavigation = useCallback(
    (screen: string, params?: Record<string, unknown>) => {
      crashReportingService.trackScreen(screen, params);
    },
    []
  );

  // Set tag
  const setTag = useCallback((key: string, value: string) => {
    crashReportingService.setTag(key, value);
  }, []);

  // Set extra data
  const setExtra = useCallback((key: string, value: unknown) => {
    crashReportingService.setExtra(key, value);
  }, []);

  // Wrap async function with error handling
  const wrapAsync = useCallback(
    async <T>(fn: () => Promise<T>, context?: string): Promise<T> => {
      try {
        return await fn();
      } catch (error) {
        captureError(error instanceof Error ? error : new Error(String(error)), {
          tags: { wrapped_context: context || 'async_operation' },
        });
        throw error;
      }
    },
    [captureError]
  );

  // Wrap callback with error handling
  const wrapCallback = useCallback(
    <T extends (...args: unknown[]) => unknown>(fn: T, context?: string): T => {
      return ((...args: unknown[]) => {
        try {
          const result = fn(...args);

          // Handle async callbacks
          if (result instanceof Promise) {
            return result.catch((error) => {
              captureError(error instanceof Error ? error : new Error(String(error)), {
                tags: { wrapped_context: context || 'callback' },
              });
              throw error;
            });
          }

          return result;
        } catch (error) {
          captureError(error instanceof Error ? error : new Error(String(error)), {
            tags: { wrapped_context: context || 'callback' },
          });
          throw error;
        }
      }) as T;
    },
    [captureError]
  );

  return useMemo(
    () => ({
      captureError,
      captureWarning,
      captureInfo,
      setUser,
      clearUser,
      addBreadcrumb,
      trackAction,
      trackNavigation,
      setTag,
      setExtra,
      wrapAsync,
      wrapCallback,
    }),
    [
      captureError,
      captureWarning,
      captureInfo,
      setUser,
      clearUser,
      addBreadcrumb,
      trackAction,
      trackNavigation,
      setTag,
      setExtra,
      wrapAsync,
      wrapCallback,
    ]
  );
}

/**
 * Hook for tracking network requests with crash reporting
 */
export function useNetworkTracking() {
  const trackRequest = useCallback(
    (
      url: string,
      method: string,
      options?: {
        statusCode?: number;
        durationMs?: number;
        success?: boolean;
        error?: string;
      }
    ) => {
      crashReportingService.trackNetworkRequest(
        url,
        method,
        options?.statusCode,
        options?.durationMs
      );

      if (options?.error) {
        crashReportingService.captureMessage(
          `Network request failed: ${method} ${url}`,
          'warning'
        );
      }
    },
    []
  );

  // Create fetch wrapper
  const trackedFetch = useCallback(
    async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
      const url = typeof input === 'string' ? input : input.toString();
      const method = init?.method || 'GET';
      const startTime = Date.now();

      try {
        const response = await fetch(input, init);
        const durationMs = Date.now() - startTime;

        trackRequest(url, method, {
          statusCode: response.status,
          durationMs,
          success: response.ok,
        });

        return response;
      } catch (error) {
        const durationMs = Date.now() - startTime;

        trackRequest(url, method, {
          durationMs,
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        });

        throw error;
      }
    },
    [trackRequest]
  );

  return { trackRequest, trackedFetch };
}

/**
 * Hook for form error tracking
 */
export function useFormErrorTracking(formName: string) {
  const { captureError, addBreadcrumb } = useCrashReporting({
    componentName: `Form:${formName}`,
  });

  const trackFieldError = useCallback(
    (fieldName: string, error: string) => {
      addBreadcrumb({
        type: 'user',
        category: 'form',
        message: `Validation error on ${fieldName}`,
        data: { form: formName, field: fieldName, error },
        level: 'warning',
      });
    },
    [formName, addBreadcrumb]
  );

  const trackSubmitError = useCallback(
    (error: Error, formData?: Record<string, unknown>) => {
      captureError(error, {
        category: 'validation',
        tags: { form: formName },
        extra: { form_fields: Object.keys(formData || {}) },
      });
    },
    [formName, captureError]
  );

  const trackSubmitSuccess = useCallback(() => {
    addBreadcrumb({
      type: 'user',
      category: 'form',
      message: `Form submitted successfully: ${formName}`,
      data: { form: formName },
    });
  }, [formName, addBreadcrumb]);

  return { trackFieldError, trackSubmitError, trackSubmitSuccess };
}

/**
 * Hook for button/interaction tracking
 */
export function useInteractionTracking() {
  const { trackAction } = useCrashReporting();

  const trackPress = useCallback(
    (elementName: string, data?: Record<string, unknown>) => {
      trackAction(`Pressed: ${elementName}`, data);
    },
    [trackAction]
  );

  const trackLongPress = useCallback(
    (elementName: string, data?: Record<string, unknown>) => {
      trackAction(`Long pressed: ${elementName}`, data);
    },
    [trackAction]
  );

  const trackSwipe = useCallback(
    (direction: 'left' | 'right' | 'up' | 'down', context?: string) => {
      trackAction(`Swiped ${direction}`, { context });
    },
    [trackAction]
  );

  return { trackPress, trackLongPress, trackSwipe };
}

export default useCrashReporting;
