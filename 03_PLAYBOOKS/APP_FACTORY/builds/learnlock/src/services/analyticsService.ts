/**
 * Analytics Service for StudyLock
 */

export type AnalyticsEvent =
  | 'app_opened'
  | 'onboarding_started'
  | 'onboarding_completed'
  | 'onboarding_skipped'
  | 'study_session_started'
  | 'study_session_completed'
  | 'study_session_paused'
  | 'study_session_cancelled'
  | 'break_started'
  | 'break_completed'
  | 'break_skipped'
  | 'emergency_unlock_used'
  | 'apps_blocked'
  | 'apps_unblocked'
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
  | 'Stats'
  | 'Settings'
  | 'Paywall'
  | 'Onboarding'
  | 'PrivacyPolicy'
  | 'Terms';

interface EventProperties {
  [key: string]: string | number | boolean | undefined;
}

class AnalyticsService {
  private initialized = false;

  async initialize(): Promise<void> {
    this.initialized = true;
    console.log('[Analytics] Initialized');
  }

  track(event: AnalyticsEvent, properties?: EventProperties): void {
    if (!this.initialized) return;
    console.log('[Analytics] Event:', event, properties || '');
  }

  trackScreen(screenName: ScreenName): void {
    this.track('screen_viewed', { screen: screenName });
  }

  trackStudySession(
    action: 'started' | 'completed' | 'paused' | 'cancelled',
    durationMinutes?: number
  ): void {
    this.track(`study_session_${action}` as AnalyticsEvent, {
      duration: durationMinutes,
    });
  }

  trackStreak(days: number): void {
    this.track('streak_milestone', { days });
  }

  trackSubscription(
    event: 'subscription_started' | 'subscription_cancelled' | 'trial_started' | 'trial_expired',
    type?: 'monthly' | 'annual' | 'lifetime'
  ): void {
    this.track(event, type ? { type } : undefined);
  }

  trackRatingPrompt(accepted: boolean): void {
    this.track(accepted ? 'app_rating_accepted' : 'app_rating_declined');
  }
}

export const analytics = new AnalyticsService();
