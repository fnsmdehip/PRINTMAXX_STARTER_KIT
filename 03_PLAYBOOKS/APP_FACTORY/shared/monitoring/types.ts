/**
 * Monitoring Types
 *
 * Shared type definitions for crash reporting and performance monitoring.
 */

// Error severity levels
export type ErrorSeverity = 'fatal' | 'error' | 'warning' | 'info' | 'debug';

// Error categories for taxonomy
export type ErrorCategory =
  | 'network'
  | 'authentication'
  | 'validation'
  | 'storage'
  | 'navigation'
  | 'rendering'
  | 'state'
  | 'api'
  | 'payment'
  | 'permission'
  | 'unknown';

// Crash reporting provider interface
export interface CrashReportingProvider {
  name: string;
  initialize(config: CrashReportingConfig): Promise<void>;
  setUser(user: UserContext | null): void;
  captureException(error: Error, context?: ErrorContext): void;
  captureMessage(message: string, severity?: ErrorSeverity): void;
  addBreadcrumb(breadcrumb: Breadcrumb): void;
  setTag(key: string, value: string): void;
  setExtra(key: string, value: unknown): void;
  clearUser(): void;
  flush(): Promise<void>;
}

// Provider configuration
export interface CrashReportingConfig {
  dsn?: string;
  apiKey?: string;
  projectId?: string;
  environment: 'development' | 'staging' | 'production';
  release?: string;
  debug?: boolean;
  enabled?: boolean;
  sampleRate?: number;
  tracesSampleRate?: number;
  attachStacktrace?: boolean;
  maxBreadcrumbs?: number;
  beforeSend?: (event: ErrorEvent) => ErrorEvent | null;
}

// User context for error attribution
export interface UserContext {
  id: string;
  email?: string;
  username?: string;
  subscription_status?: string;
  subscription_product?: string;
  app_version?: string;
  device_id?: string;
  [key: string]: unknown;
}

// Additional context for errors
export interface ErrorContext {
  severity?: ErrorSeverity;
  category?: ErrorCategory;
  tags?: Record<string, string>;
  extra?: Record<string, unknown>;
  fingerprint?: string[];
  handled?: boolean;
}

// Breadcrumb for tracking user actions
export interface Breadcrumb {
  type: BreadcrumbType;
  category: string;
  message: string;
  data?: Record<string, unknown>;
  level?: ErrorSeverity;
  timestamp?: number;
}

export type BreadcrumbType =
  | 'navigation'
  | 'user'
  | 'http'
  | 'ui'
  | 'console'
  | 'error'
  | 'transaction'
  | 'query';

// Error event structure
export interface ErrorEvent {
  event_id: string;
  timestamp: string;
  platform: 'ios' | 'android' | 'web';
  environment: string;
  release?: string;
  exception: {
    type: string;
    value: string;
    stacktrace?: StackFrame[];
  };
  user?: UserContext;
  tags?: Record<string, string>;
  extra?: Record<string, unknown>;
  breadcrumbs?: Breadcrumb[];
  contexts?: {
    device?: DeviceContext;
    os?: OSContext;
    app?: AppContext;
  };
}

// Stack frame for error traces
export interface StackFrame {
  filename?: string;
  function?: string;
  lineno?: number;
  colno?: number;
  in_app?: boolean;
  context_line?: string;
  pre_context?: string[];
  post_context?: string[];
}

// Device context
export interface DeviceContext {
  model?: string;
  manufacturer?: string;
  brand?: string;
  screen_resolution?: string;
  screen_density?: number;
  memory_size?: number;
  free_memory?: number;
  battery_level?: number;
  charging?: boolean;
  online?: boolean;
  orientation?: 'portrait' | 'landscape';
}

// OS context
export interface OSContext {
  name: string;
  version: string;
  build?: string;
  kernel_version?: string;
  rooted?: boolean;
}

// App context
export interface AppContext {
  app_identifier: string;
  app_name: string;
  app_version: string;
  app_build: string;
  app_start_time?: string;
}

// Performance metrics
export interface PerformanceMetrics {
  app_startup_time_ms: number;
  time_to_interactive_ms?: number;
  screen_render_times: Record<string, number>;
  network_requests: NetworkRequestMetric[];
  memory_usage: MemoryMetric[];
  js_thread_blocked_ms?: number;
  ui_thread_blocked_ms?: number;
}

// Network request metric
export interface NetworkRequestMetric {
  url: string;
  method: string;
  status_code?: number;
  duration_ms: number;
  request_size_bytes?: number;
  response_size_bytes?: number;
  timestamp: string;
  success: boolean;
  error?: string;
}

// Memory metric
export interface MemoryMetric {
  timestamp: string;
  used_bytes: number;
  available_bytes: number;
  percentage: number;
}

// Screen render metric
export interface ScreenRenderMetric {
  screen_name: string;
  render_time_ms: number;
  timestamp: string;
  is_initial_render: boolean;
}

// Alert configuration
export interface AlertConfig {
  id: string;
  name: string;
  enabled: boolean;
  condition: AlertCondition;
  threshold: number;
  window_minutes: number;
  channels: AlertChannel[];
  severity: ErrorSeverity;
}

// Alert condition types
export type AlertCondition =
  | 'error_count'
  | 'error_rate'
  | 'crash_free_rate'
  | 'latency_p50'
  | 'latency_p95'
  | 'latency_p99'
  | 'throughput'
  | 'apdex';

// Alert channel types
export type AlertChannel = 'email' | 'slack' | 'pagerduty' | 'webhook';

// Incident structure
export interface Incident {
  id: string;
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  status: 'open' | 'investigating' | 'identified' | 'monitoring' | 'resolved';
  created_at: string;
  resolved_at?: string;
  affected_users?: number;
  affected_sessions?: number;
  error_events: string[];
  timeline: IncidentTimelineEntry[];
  postmortem?: PostMortem;
}

// Incident timeline entry
export interface IncidentTimelineEntry {
  timestamp: string;
  action: string;
  actor: string;
  details?: string;
}

// Post-mortem structure
export interface PostMortem {
  summary: string;
  impact: string;
  root_cause: string;
  timeline: string;
  resolution: string;
  action_items: ActionItem[];
  lessons_learned: string[];
}

// Action item from post-mortem
export interface ActionItem {
  id: string;
  description: string;
  owner: string;
  due_date: string;
  status: 'pending' | 'in_progress' | 'completed';
  priority: 'high' | 'medium' | 'low';
}
