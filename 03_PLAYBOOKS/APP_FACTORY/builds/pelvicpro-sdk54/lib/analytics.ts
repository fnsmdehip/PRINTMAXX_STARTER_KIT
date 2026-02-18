/**
 * Analytics Service for FemFit
 */

export type AnalyticsEvent =
  | 'app_opened'
  | 'onboarding_started'
  | 'onboarding_completed'
  | 'onboarding_skipped'
  | 'workout_started'
  | 'workout_completed'
  | 'workout_paused'
  | 'workout_cancelled'
  | 'exercise_completed'
  | 'streak_milestone'
  | 'weekly_goal_achieved'
  | 'paywall_viewed'
  | 'subscription_started'
  | 'subscription_cancelled'
  | 'trial_started'
  | 'trial_expired'
  | 'settings_changed'
  | 'screen_viewed'
  | 'luna_toggled'
  | 'app_rating_prompted'
  | 'app_rating_accepted'
  | 'app_rating_declined';

export type ScreenName =
  | 'Home'
  | 'Exercises'
  | 'Progress'
  | 'History'
  | 'Settings'
  | 'Paywall'
  | 'Onboarding'
  | 'Privacy'
  | 'Terms'
  | 'Workout';

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

  trackWorkout(action: 'started' | 'completed' | 'paused' | 'cancelled', durationSeconds?: number): void {
    this.track(`workout_${action}` as AnalyticsEvent, {
      duration: durationSeconds,
    });
  }

  trackStreak(days: number): void {
    this.track('streak_milestone', { days });
  }

  trackSubscription(
    event: 'subscription_started' | 'subscription_cancelled' | 'trial_started' | 'trial_expired',
    type?: 'monthly' | 'annual'
  ): void {
    this.track(event, type ? { type } : undefined);
  }

  trackRatingPrompt(accepted: boolean): void {
    this.track(accepted ? 'app_rating_accepted' : 'app_rating_declined');
  }
}

export const analytics = new AnalyticsService();
