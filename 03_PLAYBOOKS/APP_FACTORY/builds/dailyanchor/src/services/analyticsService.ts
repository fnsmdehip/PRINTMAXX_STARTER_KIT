/**
 * Analytics Service for DailyAnchor
 * Scaffold for tracking app events
 */

export type AnalyticsEvent =
  | 'app_opened'
  | 'onboarding_started'
  | 'onboarding_completed'
  | 'onboarding_skipped'
  | 'focus_area_selected'
  | 'habit_completed'
  | 'habit_missed'
  | 'journal_entry_created'
  | 'gratitude_added'
  | 'devotional_viewed'
  | 'verse_shared'
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
  | 'Today'
  | 'Journal'
  | 'Progress'
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
    // TODO: Initialize your analytics provider
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

  trackHabit(habitName: string, completed: boolean): void {
    this.track(completed ? 'habit_completed' : 'habit_missed', { habit: habitName });
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
}

export const analytics = new AnalyticsService();
