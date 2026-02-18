/**
 * Analytics Service for PromptVault
 */

export type AnalyticsEvent =
  | 'app_opened'
  | 'onboarding_started'
  | 'onboarding_screen_viewed'
  | 'onboarding_screen_completed'
  | 'onboarding_completed'
  | 'onboarding_skipped'
  | 'onboarding_use_cases_selected'
  | 'onboarding_experience_selected'
  | 'onboarding_trial_started'
  | 'onboarding_free_selected'
  | 'prompt_viewed'
  | 'prompt_copied'
  | 'prompt_favorited'
  | 'prompt_unfavorited'
  | 'prompt_improved'
  | 'custom_prompt_created'
  | 'search_performed'
  | 'category_filtered'
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
  | 'PromptDetail'
  | 'Favorites'
  | 'Improve'
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

  trackPrompt(action: 'viewed' | 'copied' | 'favorited' | 'unfavorited' | 'improved', promptId: string, category?: string): void {
    this.track(`prompt_${action}` as AnalyticsEvent, {
      prompt_id: promptId,
      category,
    });
  }

  trackSearch(query: string, resultsCount: number): void {
    this.track('search_performed', {
      query_length: query.length,
      results: resultsCount,
    });
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

  // Onboarding-specific tracking
  trackOnboardingScreen(
    screenName: 'value' | 'use_case' | 'experience' | 'social_proof' | 'paywall',
    action: 'viewed' | 'completed' | 'skipped'
  ): void {
    this.track(`onboarding_screen_${action}` as AnalyticsEvent, {
      screen: screenName,
    });
  }

  trackOnboardingUseCases(useCases: string[]): void {
    this.track('onboarding_use_cases_selected', {
      use_cases: useCases.join(','),
      count: useCases.length,
    });
  }

  trackOnboardingExperience(experience: string): void {
    this.track('onboarding_experience_selected', { experience });
  }

  trackOnboardingConversion(withTrial: boolean, selectedPlan?: 'monthly' | 'annual'): void {
    this.track(withTrial ? 'onboarding_trial_started' : 'onboarding_free_selected', {
      plan: selectedPlan,
    });
  }
}

export const analytics = new AnalyticsService();
