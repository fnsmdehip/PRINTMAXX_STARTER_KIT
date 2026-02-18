/**
 * ErrorBoundary.tsx
 * React error boundary component for catching render errors
 * Integrates with crash reporting service for error tracking
 */

import React, { Component, ErrorInfo, ReactNode } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
} from 'react-native';
import crashReportingService from './CrashReportingService';
import type { ErrorContext, ErrorCategory } from './types';

interface ErrorBoundaryProps {
  children: ReactNode;

  // Custom fallback UI
  fallback?: ReactNode | ((error: Error, resetError: () => void) => ReactNode);

  // Component name for error context
  componentName?: string;

  // Error category for classification
  errorCategory?: ErrorCategory;

  // Callback when error occurs
  onError?: (error: Error, errorInfo: ErrorInfo) => void;

  // Whether to show error details (useful in development)
  showErrorDetails?: boolean;

  // Custom error report button handler
  onReportError?: (error: Error) => void;

  // Auto-reset after this many ms (0 = don't auto-reset)
  autoResetMs?: number;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  private autoResetTimeout: NodeJS.Timeout | null = null;

  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return {
      hasError: true,
      error,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    this.setState({ errorInfo });

    // Report to crash reporting service
    const context: ErrorContext = {
      severity: 'error',
      category: this.props.errorCategory || 'rendering',
      handled: true,
      tags: {
        error_boundary: 'true',
        component: this.props.componentName || 'unknown',
      },
      extra: {
        componentStack: errorInfo.componentStack,
      },
    };

    crashReportingService.captureException(error, context);

    // Call custom error handler
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }

    // Set up auto-reset if configured
    if (this.props.autoResetMs && this.props.autoResetMs > 0) {
      this.autoResetTimeout = setTimeout(() => {
        this.resetError();
      }, this.props.autoResetMs);
    }
  }

  componentWillUnmount(): void {
    if (this.autoResetTimeout) {
      clearTimeout(this.autoResetTimeout);
    }
  }

  resetError = (): void => {
    if (this.autoResetTimeout) {
      clearTimeout(this.autoResetTimeout);
      this.autoResetTimeout = null;
    }

    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });

    crashReportingService.addBreadcrumb({
      type: 'user',
      category: 'error_boundary',
      message: 'Error boundary reset',
      data: { component: this.props.componentName },
    });
  };

  handleReportError = (): void => {
    if (this.state.error) {
      if (this.props.onReportError) {
        this.props.onReportError(this.state.error);
      } else {
        // Default: re-capture with user feedback flag
        crashReportingService.captureException(this.state.error, {
          severity: 'error',
          tags: { user_reported: 'true' },
        });
      }
    }
  };

  render(): ReactNode {
    const { hasError, error, errorInfo } = this.state;
    const { children, fallback, showErrorDetails = __DEV__ } = this.props;

    if (!hasError || !error) {
      return children;
    }

    // Custom fallback
    if (fallback) {
      if (typeof fallback === 'function') {
        return fallback(error, this.resetError);
      }
      return fallback;
    }

    // Default fallback UI
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.content}>
          <Text style={styles.title}>Something went wrong</Text>
          <Text style={styles.message}>
            We encountered an unexpected error. Our team has been notified.
          </Text>

          {showErrorDetails && (
            <ScrollView style={styles.errorDetails}>
              <Text style={styles.errorTitle}>{error.name}</Text>
              <Text style={styles.errorMessage}>{error.message}</Text>
              {errorInfo?.componentStack && (
                <Text style={styles.stackTrace}>
                  {errorInfo.componentStack}
                </Text>
              )}
            </ScrollView>
          )}

          <View style={styles.buttonContainer}>
            <TouchableOpacity
              style={styles.primaryButton}
              onPress={this.resetError}
              accessibilityRole="button"
              accessibilityLabel="Try again"
            >
              <Text style={styles.primaryButtonText}>Try Again</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.secondaryButton}
              onPress={this.handleReportError}
              accessibilityRole="button"
              accessibilityLabel="Report this error"
            >
              <Text style={styles.secondaryButtonText}>Report Error</Text>
            </TouchableOpacity>
          </View>
        </View>
      </SafeAreaView>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: '#1A1A1A',
    marginBottom: 12,
    textAlign: 'center',
  },
  message: {
    fontSize: 16,
    color: '#666666',
    textAlign: 'center',
    marginBottom: 24,
    lineHeight: 24,
  },
  errorDetails: {
    maxHeight: 200,
    width: '100%',
    backgroundColor: '#F5F5F5',
    borderRadius: 8,
    padding: 12,
    marginBottom: 24,
  },
  errorTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#DC2626',
    marginBottom: 4,
  },
  errorMessage: {
    fontSize: 12,
    color: '#666666',
    marginBottom: 8,
  },
  stackTrace: {
    fontSize: 10,
    fontFamily: 'monospace',
    color: '#888888',
  },
  buttonContainer: {
    width: '100%',
    gap: 12,
  },
  primaryButton: {
    backgroundColor: '#3B82F6',
    paddingVertical: 14,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
  },
  primaryButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  secondaryButton: {
    backgroundColor: '#F3F4F6',
    paddingVertical: 14,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
  },
  secondaryButtonText: {
    color: '#374151',
    fontSize: 16,
    fontWeight: '500',
  },
});

export default ErrorBoundary;

/**
 * Higher-order component to wrap a component with error boundary
 */
export function withErrorBoundary<P extends object>(
  WrappedComponent: React.ComponentType<P>,
  errorBoundaryProps?: Omit<ErrorBoundaryProps, 'children'>
): React.ComponentType<P> {
  const displayName = WrappedComponent.displayName || WrappedComponent.name || 'Component';

  const WithErrorBoundary: React.FC<P> = (props) => (
    <ErrorBoundary {...errorBoundaryProps} componentName={displayName}>
      <WrappedComponent {...props} />
    </ErrorBoundary>
  );

  WithErrorBoundary.displayName = `WithErrorBoundary(${displayName})`;

  return WithErrorBoundary;
}

/**
 * Minimal error boundary for critical sections
 */
export class MinimalErrorBoundary extends Component<
  { children: ReactNode; fallback: ReactNode },
  { hasError: boolean }
> {
  constructor(props: { children: ReactNode; fallback: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(): { hasError: boolean } {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    crashReportingService.captureException(error, {
      severity: 'error',
      category: 'rendering',
      extra: { componentStack: errorInfo.componentStack },
    });
  }

  render(): ReactNode {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}

/**
 * Error boundary with retry functionality
 */
export class RetryErrorBoundary extends Component<
  {
    children: ReactNode;
    maxRetries?: number;
    retryDelay?: number;
    onExhausted?: () => void;
  },
  { hasError: boolean; retryCount: number }
> {
  constructor(props: {
    children: ReactNode;
    maxRetries?: number;
    retryDelay?: number;
    onExhausted?: () => void;
  }) {
    super(props);
    this.state = { hasError: false, retryCount: 0 };
  }

  static getDerivedStateFromError(): { hasError: boolean } {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    const { maxRetries = 3, retryDelay = 1000, onExhausted } = this.props;
    const { retryCount } = this.state;

    crashReportingService.captureException(error, {
      severity: 'error',
      category: 'rendering',
      extra: {
        componentStack: errorInfo.componentStack,
        retryCount,
        maxRetries,
      },
    });

    if (retryCount < maxRetries) {
      setTimeout(() => {
        this.setState((prev) => ({
          hasError: false,
          retryCount: prev.retryCount + 1,
        }));
      }, retryDelay);
    } else if (onExhausted) {
      onExhausted();
    }
  }

  render(): ReactNode {
    const { hasError, retryCount } = this.state;
    const { children, maxRetries = 3 } = this.props;

    if (hasError && retryCount >= maxRetries) {
      return (
        <View style={styles.content}>
          <Text style={styles.message}>
            Unable to load this section after {maxRetries} attempts.
          </Text>
        </View>
      );
    }

    if (hasError) {
      return (
        <View style={styles.content}>
          <Text style={styles.message}>
            Retrying... ({retryCount + 1}/{maxRetries})
          </Text>
        </View>
      );
    }

    return children;
  }
}

export { ErrorBoundary };
