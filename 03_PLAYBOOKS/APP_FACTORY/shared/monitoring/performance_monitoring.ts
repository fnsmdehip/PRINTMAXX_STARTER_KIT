/**
 * performance_monitoring.ts
 * Performance monitoring utilities for React Native apps
 * Tracks app startup, screen renders, network requests, and memory usage
 */

import { Platform, NativeModules, AppState, AppStateStatus } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import crashReportingService from './CrashReportingService';
import type {
  PerformanceMetrics,
  NetworkRequestMetric,
  MemoryMetric,
  ScreenRenderMetric,
} from './types';

// Storage keys
const STORAGE_KEYS = {
  PERFORMANCE_LOG: '@performance_monitoring_log',
  APP_START_TIME: '@performance_app_start_time',
  SESSION_METRICS: '@performance_session_metrics',
} as const;

// Performance thresholds (in ms)
const THRESHOLDS = {
  APP_STARTUP: {
    good: 2000,
    acceptable: 4000,
    poor: 6000,
  },
  SCREEN_RENDER: {
    good: 100,
    acceptable: 300,
    poor: 500,
  },
  NETWORK_REQUEST: {
    good: 500,
    acceptable: 1000,
    poor: 3000,
  },
  TIME_TO_INTERACTIVE: {
    good: 3000,
    acceptable: 5000,
    poor: 8000,
  },
} as const;

class PerformanceMonitor {
  private appStartTime: number | null = null;
  private timeToInteractive: number | null = null;
  private screenRenderTimes: Map<string, number[]> = new Map();
  private networkRequests: NetworkRequestMetric[] = [];
  private memorySnapshots: MemoryMetric[] = [];
  private isInitialized = false;
  private memoryIntervalId: NodeJS.Timer | null = null;

  /**
   * Initialize performance monitoring
   */
  async initialize(): Promise<void> {
    if (this.isInitialized) return;

    // Record app start time
    this.appStartTime = Date.now();
    await AsyncStorage.setItem(STORAGE_KEYS.APP_START_TIME, String(this.appStartTime));

    // Start memory monitoring
    this.startMemoryMonitoring();

    // Track app state for TTI calculation
    this.trackTimeToInteractive();

    this.isInitialized = true;

    crashReportingService.addBreadcrumb({
      type: 'navigation',
      category: 'performance',
      message: 'Performance monitoring initialized',
      data: { start_time: this.appStartTime },
    });
  }

  /**
   * Track app becoming interactive
   */
  private trackTimeToInteractive(): void {
    const handleAppStateChange = (state: AppStateStatus) => {
      if (state === 'active' && this.appStartTime && !this.timeToInteractive) {
        this.timeToInteractive = Date.now() - this.appStartTime;

        crashReportingService.addBreadcrumb({
          type: 'navigation',
          category: 'performance',
          message: 'App became interactive',
          data: { tti_ms: this.timeToInteractive },
        });

        // Log if TTI is poor
        if (this.timeToInteractive > THRESHOLDS.TIME_TO_INTERACTIVE.poor) {
          crashReportingService.captureMessage(
            `Slow time to interactive: ${this.timeToInteractive}ms`,
            'warning'
          );
        }
      }
    };

    AppState.addEventListener('change', handleAppStateChange);
  }

  /**
   * Mark app startup complete and record time
   */
  markStartupComplete(): number {
    if (!this.appStartTime) {
      console.warn('[Performance] App start time not set');
      return 0;
    }

    const startupTime = Date.now() - this.appStartTime;

    crashReportingService.addBreadcrumb({
      type: 'navigation',
      category: 'performance',
      message: 'App startup complete',
      data: { startup_time_ms: startupTime },
    });

    // Log slow startups
    if (startupTime > THRESHOLDS.APP_STARTUP.poor) {
      crashReportingService.captureMessage(
        `Slow app startup: ${startupTime}ms`,
        'warning'
      );
    }

    return startupTime;
  }

  /**
   * Track screen render time
   */
  trackScreenRender(screenName: string, renderTimeMs: number, isInitial = false): void {
    // Store render time
    if (!this.screenRenderTimes.has(screenName)) {
      this.screenRenderTimes.set(screenName, []);
    }
    this.screenRenderTimes.get(screenName)!.push(renderTimeMs);

    // Keep only last 50 render times per screen
    const times = this.screenRenderTimes.get(screenName)!;
    if (times.length > 50) {
      this.screenRenderTimes.set(screenName, times.slice(-50));
    }

    crashReportingService.addBreadcrumb({
      type: 'navigation',
      category: 'performance',
      message: `Screen rendered: ${screenName}`,
      data: {
        render_time_ms: renderTimeMs,
        is_initial: isInitial,
      },
      level: renderTimeMs > THRESHOLDS.SCREEN_RENDER.poor ? 'warning' : 'info',
    });

    // Log slow renders
    if (renderTimeMs > THRESHOLDS.SCREEN_RENDER.poor) {
      crashReportingService.captureMessage(
        `Slow screen render: ${screenName} took ${renderTimeMs}ms`,
        'warning'
      );
    }
  }

  /**
   * Create screen render tracker (for use with useEffect)
   */
  createScreenRenderTracker(screenName: string): {
    start: () => void;
    end: () => void;
  } {
    let startTime: number | null = null;
    let isInitial = true;

    return {
      start: () => {
        startTime = Date.now();
      },
      end: () => {
        if (startTime) {
          const renderTime = Date.now() - startTime;
          this.trackScreenRender(screenName, renderTime, isInitial);
          isInitial = false;
        }
      },
    };
  }

  /**
   * Track network request
   */
  trackNetworkRequest(metric: Omit<NetworkRequestMetric, 'timestamp'>): void {
    const fullMetric: NetworkRequestMetric = {
      ...metric,
      timestamp: new Date().toISOString(),
    };

    this.networkRequests.push(fullMetric);

    // Keep only last 100 requests
    if (this.networkRequests.length > 100) {
      this.networkRequests = this.networkRequests.slice(-100);
    }

    // Also track in crash reporting for context
    crashReportingService.trackNetworkRequest(
      metric.url,
      metric.method,
      metric.status_code,
      metric.duration_ms
    );

    // Log slow requests
    if (metric.duration_ms > THRESHOLDS.NETWORK_REQUEST.poor) {
      crashReportingService.captureMessage(
        `Slow network request: ${metric.method} ${metric.url} took ${metric.duration_ms}ms`,
        'warning'
      );
    }
  }

  /**
   * Create fetch wrapper for automatic network tracking
   */
  createTrackedFetch(): typeof fetch {
    const self = this;

    return async function trackedFetch(
      input: RequestInfo | URL,
      init?: RequestInit
    ): Promise<Response> {
      const url = typeof input === 'string' ? input : input.toString();
      const method = init?.method || 'GET';
      const startTime = Date.now();

      try {
        const response = await fetch(input, init);
        const durationMs = Date.now() - startTime;

        self.trackNetworkRequest({
          url,
          method,
          status_code: response.status,
          duration_ms: durationMs,
          success: response.ok,
        });

        return response;
      } catch (error) {
        const durationMs = Date.now() - startTime;

        self.trackNetworkRequest({
          url,
          method,
          duration_ms: durationMs,
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        });

        throw error;
      }
    };
  }

  /**
   * Start periodic memory monitoring
   */
  private startMemoryMonitoring(intervalMs = 60000): void {
    // Take initial snapshot
    this.takeMemorySnapshot();

    // Set up periodic snapshots
    this.memoryIntervalId = setInterval(() => {
      this.takeMemorySnapshot();
    }, intervalMs);
  }

  /**
   * Take memory snapshot
   */
  private async takeMemorySnapshot(): Promise<void> {
    try {
      // Get memory info (platform-specific)
      const memoryInfo = await this.getMemoryInfo();

      if (memoryInfo) {
        this.memorySnapshots.push({
          timestamp: new Date().toISOString(),
          used_bytes: memoryInfo.used,
          available_bytes: memoryInfo.available,
          percentage: memoryInfo.percentage,
        });

        // Keep only last 60 snapshots (1 hour at 1/min)
        if (this.memorySnapshots.length > 60) {
          this.memorySnapshots = this.memorySnapshots.slice(-60);
        }

        // Warn if memory usage is high
        if (memoryInfo.percentage > 80) {
          crashReportingService.captureMessage(
            `High memory usage: ${memoryInfo.percentage.toFixed(1)}%`,
            'warning'
          );
        }
      }
    } catch (error) {
      // Silently fail - memory monitoring is non-critical
    }
  }

  /**
   * Get memory info (platform-specific)
   */
  private async getMemoryInfo(): Promise<{
    used: number;
    available: number;
    percentage: number;
  } | null> {
    try {
      if (Platform.OS === 'ios') {
        // iOS memory info via native module (if available)
        const PerformanceModule = NativeModules.PerformanceModule;
        if (PerformanceModule?.getMemoryInfo) {
          return await PerformanceModule.getMemoryInfo();
        }
      } else if (Platform.OS === 'android') {
        // Android memory info via native module (if available)
        const PerformanceModule = NativeModules.PerformanceModule;
        if (PerformanceModule?.getMemoryInfo) {
          return await PerformanceModule.getMemoryInfo();
        }
      }

      // Fallback: use JS heap info if available
      // @ts-ignore - performance.memory is non-standard
      if (typeof performance !== 'undefined' && performance.memory) {
        // @ts-ignore
        const { usedJSHeapSize, jsHeapSizeLimit } = performance.memory;
        return {
          used: usedJSHeapSize,
          available: jsHeapSizeLimit - usedJSHeapSize,
          percentage: (usedJSHeapSize / jsHeapSizeLimit) * 100,
        };
      }

      return null;
    } catch {
      return null;
    }
  }

  /**
   * Stop memory monitoring
   */
  stopMemoryMonitoring(): void {
    if (this.memoryIntervalId) {
      clearInterval(this.memoryIntervalId);
      this.memoryIntervalId = null;
    }
  }

  /**
   * Get current performance metrics
   */
  getMetrics(): PerformanceMetrics {
    // Calculate screen render averages
    const screenRenderTimes: Record<string, number> = {};
    for (const [screen, times] of this.screenRenderTimes) {
      const avg = times.reduce((a, b) => a + b, 0) / times.length;
      screenRenderTimes[screen] = Math.round(avg);
    }

    return {
      app_startup_time_ms: this.appStartTime
        ? Date.now() - this.appStartTime
        : 0,
      time_to_interactive_ms: this.timeToInteractive || undefined,
      screen_render_times: screenRenderTimes,
      network_requests: [...this.networkRequests],
      memory_usage: [...this.memorySnapshots],
    };
  }

  /**
   * Get performance summary for reporting
   */
  getSummary(): {
    startup: { value: number; rating: string };
    tti: { value: number; rating: string } | null;
    avgScreenRender: { value: number; rating: string };
    avgNetworkLatency: { value: number; rating: string };
    memoryUsage: { value: number; rating: string } | null;
  } {
    const metrics = this.getMetrics();

    const rateValue = (value: number, thresholds: { good: number; acceptable: number; poor: number }) => {
      if (value <= thresholds.good) return 'good';
      if (value <= thresholds.acceptable) return 'acceptable';
      return 'poor';
    };

    // Calculate averages
    const screenRenderValues = Object.values(metrics.screen_render_times);
    const avgScreenRender =
      screenRenderValues.length > 0
        ? screenRenderValues.reduce((a, b) => a + b, 0) / screenRenderValues.length
        : 0;

    const networkLatencies = metrics.network_requests.map((r) => r.duration_ms);
    const avgNetworkLatency =
      networkLatencies.length > 0
        ? networkLatencies.reduce((a, b) => a + b, 0) / networkLatencies.length
        : 0;

    const latestMemory = metrics.memory_usage[metrics.memory_usage.length - 1];

    return {
      startup: {
        value: metrics.app_startup_time_ms,
        rating: rateValue(metrics.app_startup_time_ms, THRESHOLDS.APP_STARTUP),
      },
      tti: metrics.time_to_interactive_ms
        ? {
            value: metrics.time_to_interactive_ms,
            rating: rateValue(
              metrics.time_to_interactive_ms,
              THRESHOLDS.TIME_TO_INTERACTIVE
            ),
          }
        : null,
      avgScreenRender: {
        value: Math.round(avgScreenRender),
        rating: rateValue(avgScreenRender, THRESHOLDS.SCREEN_RENDER),
      },
      avgNetworkLatency: {
        value: Math.round(avgNetworkLatency),
        rating: rateValue(avgNetworkLatency, THRESHOLDS.NETWORK_REQUEST),
      },
      memoryUsage: latestMemory
        ? {
            value: Math.round(latestMemory.percentage),
            rating:
              latestMemory.percentage < 50
                ? 'good'
                : latestMemory.percentage < 80
                ? 'acceptable'
                : 'poor',
          }
        : null,
    };
  }

  /**
   * Log performance summary to crash reporting
   */
  logPerformanceSummary(): void {
    const summary = this.getSummary();

    crashReportingService.addBreadcrumb({
      type: 'navigation',
      category: 'performance',
      message: 'Performance summary',
      data: {
        startup_ms: summary.startup.value,
        startup_rating: summary.startup.rating,
        tti_ms: summary.tti?.value,
        tti_rating: summary.tti?.rating,
        avg_screen_render_ms: summary.avgScreenRender.value,
        avg_network_latency_ms: summary.avgNetworkLatency.value,
        memory_percentage: summary.memoryUsage?.value,
      },
    });
  }

  /**
   * Cleanup
   */
  cleanup(): void {
    this.stopMemoryMonitoring();
    this.screenRenderTimes.clear();
    this.networkRequests = [];
    this.memorySnapshots = [];
  }
}

// Export singleton instance
export const performanceMonitor = new PerformanceMonitor();

/**
 * Hook for tracking screen render time
 */
export function useScreenRenderTracking(screenName: string) {
  const tracker = performanceMonitor.createScreenRenderTracker(screenName);

  return {
    onRenderStart: tracker.start,
    onRenderEnd: tracker.end,
  };
}

/**
 * Measure function execution time
 */
export async function measureAsync<T>(
  name: string,
  fn: () => Promise<T>
): Promise<T> {
  const startTime = Date.now();

  try {
    const result = await fn();
    const duration = Date.now() - startTime;

    crashReportingService.addBreadcrumb({
      type: 'transaction',
      category: 'performance',
      message: `Measured: ${name}`,
      data: { duration_ms: duration },
    });

    return result;
  } catch (error) {
    const duration = Date.now() - startTime;

    crashReportingService.addBreadcrumb({
      type: 'error',
      category: 'performance',
      message: `Measured (failed): ${name}`,
      data: { duration_ms: duration },
      level: 'error',
    });

    throw error;
  }
}

/**
 * Measure sync function execution time
 */
export function measureSync<T>(name: string, fn: () => T): T {
  const startTime = Date.now();

  try {
    const result = fn();
    const duration = Date.now() - startTime;

    crashReportingService.addBreadcrumb({
      type: 'transaction',
      category: 'performance',
      message: `Measured: ${name}`,
      data: { duration_ms: duration },
    });

    return result;
  } catch (error) {
    const duration = Date.now() - startTime;

    crashReportingService.addBreadcrumb({
      type: 'error',
      category: 'performance',
      message: `Measured (failed): ${name}`,
      data: { duration_ms: duration },
      level: 'error',
    });

    throw error;
  }
}

export default performanceMonitor;
