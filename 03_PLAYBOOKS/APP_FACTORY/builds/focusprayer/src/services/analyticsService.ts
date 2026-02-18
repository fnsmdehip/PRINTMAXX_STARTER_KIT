/**
 * Analytics Service for PrayerLock
 */

export type AnalyticsEvent =
  | 'app_opened'
  | 'onboarding_started'
  | 'onboarding_completed'
  | 'devotion_started'
  | 'devotion_completed'
  | 'prayer_timer_started'
  | 'prayer_timer_completed'
  | 'scripture_viewed'
  | 'scripture_completed'
  | 'emergency_unlock_used'
  | 'apps_unlocked'
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
  | 'Timer'
  | 'Scripture'
  | 'Stats'
  | 'Settings'
  | 'Paywall'
  | 'Onboarding'
  | 'EmergencyUnlock'
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

  trackDevotion(action: 'started' | 'completed', durationMinutes?: number): void {
    this.track(action === 'started' ? 'devotion_started' : 'devotion_completed', {
      duration: durationMinutes,
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
