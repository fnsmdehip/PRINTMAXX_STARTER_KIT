/**
 * Mock implementation for analytics services
 *
 * Usage in tests:
 *   import mockAnalytics, { getTrackedEvents } from '@testing/mocks/mockAnalytics';
 *
 *   test('tracks button click', () => {
 *     // ... trigger action
 *     expect(getTrackedEvents()).toContainEqual({
 *       name: 'button_pressed',
 *       properties: { button: 'subscribe' }
 *     });
 *   });
 */

// ============================================================================
// Types
// ============================================================================

export interface TrackedEvent {
  name: string;
  properties?: Record<string, unknown>;
  timestamp: Date;
}

export interface IdentifyCall {
  userId: string;
  traits?: Record<string, unknown>;
  timestamp: Date;
}

export interface ScreenCall {
  name: string;
  properties?: Record<string, unknown>;
  timestamp: Date;
}

export interface GroupCall {
  groupId: string;
  traits?: Record<string, unknown>;
  timestamp: Date;
}

// ============================================================================
// Mock State
// ============================================================================

let trackedEvents: TrackedEvent[] = [];
let identifyCalls: IdentifyCall[] = [];
let screenCalls: ScreenCall[] = [];
let groupCalls: GroupCall[] = [];
let currentUserId: string | null = null;
let isEnabled = true;

// ============================================================================
// Test Utilities
// ============================================================================

/**
 * Get all tracked events
 */
export function getTrackedEvents(): TrackedEvent[] {
  return [...trackedEvents];
}

/**
 * Get events by name
 */
export function getEventsByName(name: string): TrackedEvent[] {
  return trackedEvents.filter((e) => e.name === name);
}

/**
 * Check if an event was tracked
 */
export function wasEventTracked(name: string, properties?: Record<string, unknown>): boolean {
  return trackedEvents.some((e) => {
    if (e.name !== name) return false;
    if (!properties) return true;
    return Object.entries(properties).every(
      ([key, value]) => e.properties?.[key] === value
    );
  });
}

/**
 * Get all identify calls
 */
export function getIdentifyCalls(): IdentifyCall[] {
  return [...identifyCalls];
}

/**
 * Get all screen calls
 */
export function getScreenCalls(): ScreenCall[] {
  return [...screenCalls];
}

/**
 * Get all group calls
 */
export function getGroupCalls(): GroupCall[] {
  return [...groupCalls];
}

/**
 * Get current user ID
 */
export function getCurrentUserId(): string | null {
  return currentUserId;
}

/**
 * Reset all mock state
 */
export function resetMockAnalytics(): void {
  trackedEvents = [];
  identifyCalls = [];
  screenCalls = [];
  groupCalls = [];
  currentUserId = null;
  isEnabled = true;
}

/**
 * Disable analytics (for testing disabled state)
 */
export function setAnalyticsEnabled(enabled: boolean): void {
  isEnabled = enabled;
}

// ============================================================================
// Mock Implementation
// ============================================================================

const mockAnalytics = {
  /**
   * Track an event
   */
  track: jest.fn((name: string, properties?: Record<string, unknown>): void => {
    if (!isEnabled) return;
    trackedEvents.push({
      name,
      properties,
      timestamp: new Date(),
    });
  }),

  /**
   * Identify a user
   */
  identify: jest.fn((userId: string, traits?: Record<string, unknown>): void => {
    if (!isEnabled) return;
    currentUserId = userId;
    identifyCalls.push({
      userId,
      traits,
      timestamp: new Date(),
    });
  }),

  /**
   * Track a screen view
   */
  screen: jest.fn((name: string, properties?: Record<string, unknown>): void => {
    if (!isEnabled) return;
    screenCalls.push({
      name,
      properties,
      timestamp: new Date(),
    });
  }),

  /**
   * Associate user with a group
   */
  group: jest.fn((groupId: string, traits?: Record<string, unknown>): void => {
    if (!isEnabled) return;
    groupCalls.push({
      groupId,
      traits,
      timestamp: new Date(),
    });
  }),

  /**
   * Alias user IDs
   */
  alias: jest.fn((newId: string, _previousId?: string): void => {
    if (!isEnabled) return;
    currentUserId = newId;
  }),

  /**
   * Reset analytics (logout)
   */
  reset: jest.fn((): void => {
    currentUserId = null;
  }),

  /**
   * Flush events to server
   */
  flush: jest.fn(async (): Promise<void> => {
    // No-op in mock
  }),

  /**
   * Enable/disable analytics
   */
  setEnabled: jest.fn((enabled: boolean): void => {
    isEnabled = enabled;
  }),

  /**
   * Check if analytics is enabled
   */
  isEnabled: jest.fn((): boolean => isEnabled),

  /**
   * Get anonymous ID
   */
  getAnonymousId: jest.fn(async (): Promise<string> => 'anonymous-id-123'),
};

export default mockAnalytics;

// ============================================================================
// Common Event Names
// ============================================================================

export const ANALYTICS_EVENTS = {
  // Onboarding
  ONBOARDING_STARTED: 'onboarding_started',
  ONBOARDING_STEP_COMPLETED: 'onboarding_step_completed',
  ONBOARDING_COMPLETED: 'onboarding_completed',
  ONBOARDING_SKIPPED: 'onboarding_skipped',

  // Authentication
  SIGN_UP_STARTED: 'sign_up_started',
  SIGN_UP_COMPLETED: 'sign_up_completed',
  SIGN_IN_COMPLETED: 'sign_in_completed',
  SIGN_OUT_COMPLETED: 'sign_out_completed',
  PASSWORD_RESET_REQUESTED: 'password_reset_requested',

  // Subscription
  PAYWALL_VIEWED: 'paywall_viewed',
  SUBSCRIPTION_STARTED: 'subscription_started',
  SUBSCRIPTION_COMPLETED: 'subscription_completed',
  SUBSCRIPTION_FAILED: 'subscription_failed',
  SUBSCRIPTION_CANCELLED: 'subscription_cancelled',
  SUBSCRIPTION_RESTORED: 'subscription_restored',
  TRIAL_STARTED: 'trial_started',

  // Content
  CONTENT_VIEWED: 'content_viewed',
  CONTENT_SHARED: 'content_shared',
  CONTENT_SAVED: 'content_saved',
  CONTENT_COMPLETED: 'content_completed',
  SEARCH_PERFORMED: 'search_performed',

  // Engagement
  BUTTON_PRESSED: 'button_pressed',
  LINK_CLICKED: 'link_clicked',
  SHARE_INITIATED: 'share_initiated',
  NOTIFICATION_OPENED: 'notification_opened',
  NOTIFICATION_PERMISSION_GRANTED: 'notification_permission_granted',
  NOTIFICATION_PERMISSION_DENIED: 'notification_permission_denied',

  // Errors
  ERROR_OCCURRED: 'error_occurred',
  CRASH_REPORTED: 'crash_reported',

  // App lifecycle
  APP_OPENED: 'app_opened',
  APP_BACKGROUNDED: 'app_backgrounded',
  APP_UPDATED: 'app_updated',
  DEEP_LINK_OPENED: 'deep_link_opened',
} as const;

// ============================================================================
// Helper Functions for Common Tracking Patterns
// ============================================================================

/**
 * Create event assertion helper
 */
export function expectEvent(name: string, properties?: Record<string, unknown>): void {
  expect(wasEventTracked(name, properties)).toBe(true);
}

/**
 * Create screen assertion helper
 */
export function expectScreen(name: string): void {
  expect(screenCalls.some((s) => s.name === name)).toBe(true);
}

/**
 * Create identify assertion helper
 */
export function expectIdentify(userId: string, traits?: Record<string, unknown>): void {
  const call = identifyCalls.find((c) => c.userId === userId);
  expect(call).toBeDefined();
  if (traits && call) {
    Object.entries(traits).forEach(([key, value]) => {
      expect(call.traits?.[key]).toBe(value);
    });
  }
}
