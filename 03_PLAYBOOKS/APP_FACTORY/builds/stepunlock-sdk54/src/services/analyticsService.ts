/**
 * Analytics Service
 * Scaffold for tracking app events
 * Replace with your preferred analytics provider (Amplitude, Mixpanel, Firebase, etc.)
 */

// Event types for type safety
export type AnalyticsEvent =
  | 'app_opened'
  | 'onboarding_started'
  | 'onboarding_completed'
  | 'health_permission_granted'
  | 'health_permission_denied'
  | 'goal_set'
  | 'apps_selected'
  | 'blocking_enabled'
  | 'goal_reached'
  | 'emergency_unlock_used'
  | 'streak_milestone'
  | 'paywall_viewed'
  | 'subscription_started'
  | 'subscription_cancelled'
  | 'trial_started'
  | 'trial_expired'
  | 'settings_changed'
  | 'screen_viewed'
  | 'app_rating_prompted'
  | 'app_rating_accepted'
  | 'app_rating_declined';

export type ScreenName =
  | 'Home'
  | 'Progress'
  | 'Settings'
  | 'Paywall'
  | 'Onboarding'
  | 'EmergencyUnlock'
  | 'PrivacyPolicy'
  | 'Terms';

interface EventProperties {
  [key: string]: string | number | boolean | undefined;
}

interface UserProperties {
  isSubscribed?: boolean;
  subscriptionType?: 'monthly' | 'annual';
  stepGoal?: number;
  blockedAppsCount?: number;
  streakDays?: number;
  trialActive?: boolean;
}

class AnalyticsService {
  private initialized = false;
  private userId: string | null = null;

  /**
   * Initialize analytics service
   * Call this on app startup
   */
  async initialize(): Promise<void> {
    // TODO: Replace with actual analytics initialization
    // Example for Amplitude:
    // await Amplitude.init('YOUR_API_KEY');

    // Example for Firebase:
    // await analytics().setAnalyticsCollectionEnabled(true);

    this.initialized = true;
    console.log('[Analytics] Initialized');
  }

  /**
   * Set user ID for analytics
   */
  setUserId(userId: string): void {
    this.userId = userId;
    // TODO: Set user ID in your analytics provider
    // Amplitude.setUserId(userId);
    console.log('[Analytics] User ID set:', userId);
  }

  /**
   * Set user properties
   */
  setUserProperties(properties: UserProperties): void {
    // TODO: Set user properties in your analytics provider
    // Amplitude.setUserProperties(properties);
    console.log('[Analytics] User properties:', properties);
  }

  /**
   * Track an event
   */
  track(event: AnalyticsEvent, properties?: EventProperties): void {
    if (!this.initialized) {
      console.warn('[Analytics] Not initialized, skipping event:', event);
      return;
    }

    // TODO: Send event to your analytics provider
    // Amplitude.track(event, properties);
    // analytics().logEvent(event, properties);

    console.log('[Analytics] Event:', event, properties || '');
  }

  /**
   * Track screen view
   */
  trackScreen(screenName: ScreenName): void {
    this.track('screen_viewed', { screen: screenName });
  }

  /**
   * Track goal reached
   */
  trackGoalReached(stepGoal: number, stepsWalked: number): void {
    this.track('goal_reached', {
      goal: stepGoal,
      actual: stepsWalked,
      surplus: stepsWalked - stepGoal,
    });
  }

  /**
   * Track streak milestone
   */
  trackStreakMilestone(days: number): void {
    this.track('streak_milestone', { days });
  }

  /**
   * Track subscription event
   */
  trackSubscription(
    event: 'subscription_started' | 'subscription_cancelled' | 'trial_started' | 'trial_expired',
    type?: 'monthly' | 'annual'
  ): void {
    this.track(event, type ? { type } : undefined);
  }

  /**
   * Track onboarding progress
   */
  trackOnboarding(step: string, completed: boolean): void {
    this.track(completed ? 'onboarding_completed' : 'onboarding_started', {
      step,
    });
  }

  /**
   * Track paywall interaction
   */
  trackPaywall(action: 'viewed' | 'subscribed' | 'dismissed'): void {
    if (action === 'viewed') {
      this.track('paywall_viewed');
    } else if (action === 'subscribed') {
      this.track('subscription_started');
    }
  }

  /**
   * Track app rating prompt
   */
  trackRatingPrompt(accepted: boolean): void {
    this.track(accepted ? 'app_rating_accepted' : 'app_rating_declined');
  }

  /**
   * Reset analytics (e.g., on logout)
   */
  reset(): void {
    this.userId = null;
    // TODO: Reset user in analytics provider
    // Amplitude.reset();
    console.log('[Analytics] Reset');
  }
}

// Export singleton instance
export const analytics = new AnalyticsService();
