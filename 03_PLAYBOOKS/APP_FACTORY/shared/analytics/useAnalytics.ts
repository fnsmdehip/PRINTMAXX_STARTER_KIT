/**
 * useAnalytics Hook
 *
 * Provides a simple interface for tracking analytics events,
 * setting user properties, and tracking revenue.
 */

import { useCallback, useMemo } from 'react';
import { useAnalyticsContext } from './AnalyticsProvider';
import type { AnalyticsEventName, AnalyticsEventMap, EVENT_METADATA } from './events';
import type { UserTraits, UserProperties, RevenueData } from './types';

/**
 * Analytics hook return type
 */
interface UseAnalyticsReturn {
  // Status
  isInitialized: boolean;
  isEnabled: boolean;

  // Core tracking
  track: <T extends AnalyticsEventName>(
    event: T,
    properties: AnalyticsEventMap[T]
  ) => Promise<void>;

  // User management
  identify: (userId: string, traits?: UserTraits) => Promise<void>;
  setUserProperties: (properties: UserProperties) => Promise<void>;
  reset: () => Promise<void>;

  // Revenue
  trackRevenue: (revenue: RevenueData) => Promise<void>;
  trackPurchase: (
    productId: string,
    price: number,
    currency: string,
    isTrial?: boolean
  ) => Promise<void>;

  // Convenience methods
  trackScreen: (screenName: string, properties?: Record<string, unknown>) => Promise<void>;
  trackFeature: (featureName: string, properties?: Record<string, unknown>) => Promise<void>;
  trackError: (
    errorType: string,
    errorMessage: string,
    properties?: Record<string, unknown>
  ) => Promise<void>;
  trackPaywall: (
    paywallId: string,
    action: 'viewed' | 'dismissed',
    properties?: Record<string, unknown>
  ) => Promise<void>;

  // Session
  startSession: () => void;
  endSession: () => void;

  // Settings
  setEnabled: (enabled: boolean) => void;
  flush: () => Promise<void>;
}

/**
 * Main analytics hook
 */
export function useAnalytics(): UseAnalyticsReturn {
  const {
    isInitialized,
    isEnabled,
    track,
    identify,
    setUserProperties,
    trackRevenue,
    reset,
    flush,
    startSession,
    endSession,
    setEnabled,
  } = useAnalyticsContext();

  /**
   * Track purchase convenience method
   */
  const trackPurchase = useCallback(
    async (
      productId: string,
      price: number,
      currency: string,
      isTrial: boolean = false
    ): Promise<void> => {
      await track('purchase_completed', {
        product_id: productId,
        price,
        currency,
        is_trial: isTrial,
        transaction_id: `txn_${Date.now()}`,
      });

      await trackRevenue({
        amount: price,
        currency,
        product_id: productId,
        is_trial_conversion: isTrial,
      });
    },
    [track, trackRevenue]
  );

  /**
   * Track screen view convenience method
   */
  const trackScreen = useCallback(
    async (
      screenName: string,
      properties?: Record<string, unknown>
    ): Promise<void> => {
      await track('screen_viewed', {
        screen_name: screenName,
        screen_class: screenName,
        navigation_method: 'tap',
        ...properties,
      } as AnalyticsEventMap['screen_viewed']);
    },
    [track]
  );

  /**
   * Track feature usage convenience method
   */
  const trackFeature = useCallback(
    async (
      featureName: string,
      properties?: Record<string, unknown>
    ): Promise<void> => {
      await track('feature_used', {
        feature_name: featureName,
        usage_count: 1,
        ...properties,
      } as AnalyticsEventMap['feature_used']);
    },
    [track]
  );

  /**
   * Track error convenience method
   */
  const trackError = useCallback(
    async (
      errorType: string,
      errorMessage: string,
      properties?: Record<string, unknown>
    ): Promise<void> => {
      await track('error_occurred', {
        error_type: errorType as 'crash' | 'network' | 'validation' | 'permission' | 'unknown',
        error_code: errorType,
        error_message: errorMessage,
        screen_name: 'unknown',
        ...properties,
      } as AnalyticsEventMap['error_occurred']);
    },
    [track]
  );

  /**
   * Track paywall convenience method
   */
  const trackPaywall = useCallback(
    async (
      paywallId: string,
      action: 'viewed' | 'dismissed',
      properties?: Record<string, unknown>
    ): Promise<void> => {
      if (action === 'viewed') {
        await track('paywall_viewed', {
          paywall_id: paywallId,
          trigger: 'feature_gate',
          products_shown: [],
          ...properties,
        } as AnalyticsEventMap['paywall_viewed']);
      } else {
        await track('paywall_dismissed', {
          paywall_id: paywallId,
          time_on_paywall_ms: 0,
          scroll_depth_percent: 0,
          ...properties,
        } as AnalyticsEventMap['paywall_dismissed']);
      }
    },
    [track]
  );

  return useMemo(
    () => ({
      isInitialized,
      isEnabled,
      track,
      identify,
      setUserProperties,
      reset,
      trackRevenue,
      trackPurchase,
      trackScreen,
      trackFeature,
      trackError,
      trackPaywall,
      startSession,
      endSession,
      setEnabled,
      flush,
    }),
    [
      isInitialized,
      isEnabled,
      track,
      identify,
      setUserProperties,
      reset,
      trackRevenue,
      trackPurchase,
      trackScreen,
      trackFeature,
      trackError,
      trackPaywall,
      startSession,
      endSession,
      setEnabled,
      flush,
    ]
  );
}

/**
 * Hook for tracking onboarding events
 */
export function useOnboardingAnalytics() {
  const { track } = useAnalytics();

  const trackOnboardingStart = useCallback(
    async (source: 'organic' | 'paid' | 'referral' | 'unknown' = 'organic') => {
      await track('onboarding_started', { source });
    },
    [track]
  );

  const trackOnboardingScreen = useCallback(
    async (screenIndex: number, screenName: string, timeOnPreviousMs?: number) => {
      await track('onboarding_screen_viewed', {
        screen_index: screenIndex,
        screen_name: screenName,
        time_on_previous_screen_ms: timeOnPreviousMs,
      });
    },
    [track]
  );

  const trackOnboardingSkip = useCallback(
    async (screenIndex: number, screenName: string) => {
      await track('onboarding_screen_skipped', {
        screen_index: screenIndex,
        screen_name: screenName,
      });
    },
    [track]
  );

  const trackOnboardingComplete = useCallback(
    async (totalScreens: number, totalTimeMs: number, screensSkipped: number) => {
      await track('onboarding_completed', {
        total_screens: totalScreens,
        total_time_ms: totalTimeMs,
        screens_skipped: screensSkipped,
      });
    },
    [track]
  );

  const trackOnboardingAbandoned = useCallback(
    async (lastScreenIndex: number, lastScreenName: string, totalTimeMs: number) => {
      await track('onboarding_abandoned', {
        last_screen_index: lastScreenIndex,
        last_screen_name: lastScreenName,
        total_time_ms: totalTimeMs,
      });
    },
    [track]
  );

  const trackPermission = useCallback(
    async (
      permissionType: 'notifications' | 'tracking' | 'camera' | 'photos' | 'location',
      granted: boolean,
      screenName: string
    ) => {
      await track('permission_requested', {
        permission_type: permissionType,
        screen_name: screenName,
      });

      if (granted) {
        await track('permission_granted', { permission_type: permissionType });
      } else {
        await track('permission_denied', { permission_type: permissionType });
      }
    },
    [track]
  );

  return useMemo(
    () => ({
      trackOnboardingStart,
      trackOnboardingScreen,
      trackOnboardingSkip,
      trackOnboardingComplete,
      trackOnboardingAbandoned,
      trackPermission,
    }),
    [
      trackOnboardingStart,
      trackOnboardingScreen,
      trackOnboardingSkip,
      trackOnboardingComplete,
      trackOnboardingAbandoned,
      trackPermission,
    ]
  );
}

/**
 * Hook for tracking conversion events
 */
export function useConversionAnalytics() {
  const { track, trackRevenue } = useAnalytics();

  const trackPaywallViewed = useCallback(
    async (
      paywallId: string,
      trigger: 'feature_gate' | 'settings' | 'onboarding' | 'prompt' | 'deeplink',
      productsShown: string[]
    ) => {
      await track('paywall_viewed', {
        paywall_id: paywallId,
        trigger,
        products_shown: productsShown,
      });
    },
    [track]
  );

  const trackPaywallDismissed = useCallback(
    async (paywallId: string, timeOnPaywallMs: number, scrollDepthPercent: number) => {
      await track('paywall_dismissed', {
        paywall_id: paywallId,
        time_on_paywall_ms: timeOnPaywallMs,
        scroll_depth_percent: scrollDepthPercent,
      });
    },
    [track]
  );

  const trackProductSelected = useCallback(
    async (
      productId: string,
      productType: 'subscription' | 'lifetime' | 'consumable',
      price: number,
      currency: string
    ) => {
      await track('product_selected', {
        product_id: productId,
        product_type: productType,
        price,
        currency,
      });
    },
    [track]
  );

  const trackTrialStarted = useCallback(
    async (productId: string, trialDurationDays: number, paywallId: string) => {
      await track('trial_started', {
        product_id: productId,
        trial_duration_days: trialDurationDays,
        paywall_id: paywallId,
      });
    },
    [track]
  );

  const trackPurchaseCompleted = useCallback(
    async (
      productId: string,
      price: number,
      currency: string,
      isTrial: boolean,
      transactionId: string
    ) => {
      await track('purchase_completed', {
        product_id: productId,
        price,
        currency,
        is_trial: isTrial,
        transaction_id: transactionId,
      });

      await trackRevenue({
        amount: price,
        currency,
        product_id: productId,
        receipt: transactionId,
        is_trial_conversion: isTrial,
      });
    },
    [track, trackRevenue]
  );

  const trackPurchaseFailed = useCallback(
    async (productId: string, errorCode: string, errorMessage: string) => {
      await track('purchase_failed', {
        product_id: productId,
        error_code: errorCode,
        error_message: errorMessage,
      });
    },
    [track]
  );

  return useMemo(
    () => ({
      trackPaywallViewed,
      trackPaywallDismissed,
      trackProductSelected,
      trackTrialStarted,
      trackPurchaseCompleted,
      trackPurchaseFailed,
    }),
    [
      trackPaywallViewed,
      trackPaywallDismissed,
      trackProductSelected,
      trackTrialStarted,
      trackPurchaseCompleted,
      trackPurchaseFailed,
    ]
  );
}

/**
 * Hook for tracking retention events
 */
export function useRetentionAnalytics() {
  const { track } = useAnalytics();

  const trackStreakAchieved = useCallback(
    async (streakType: string, streakCount: number, previousBest: number) => {
      await track('streak_achieved', {
        streak_type: streakType,
        streak_count: streakCount,
        previous_best: previousBest,
      });
    },
    [track]
  );

  const trackStreakBroken = useCallback(
    async (streakType: string, streakCount: number, daysMissed: number) => {
      await track('streak_broken', {
        streak_type: streakType,
        streak_count: streakCount,
        days_missed: daysMissed,
      });
    },
    [track]
  );

  const trackMilestoneReached = useCallback(
    async (milestoneType: string, milestoneValue: number, daysToAchieve: number) => {
      await track('milestone_reached', {
        milestone_type: milestoneType,
        milestone_value: milestoneValue,
        days_to_achieve: daysToAchieve,
      });
    },
    [track]
  );

  const trackNotificationOpened = useCallback(
    async (notificationId: string, notificationType: string, timeToOpenMs: number) => {
      await track('notification_opened', {
        notification_id: notificationId,
        notification_type: notificationType,
        time_to_open_ms: timeToOpenMs,
      });
    },
    [track]
  );

  return useMemo(
    () => ({
      trackStreakAchieved,
      trackStreakBroken,
      trackMilestoneReached,
      trackNotificationOpened,
    }),
    [trackStreakAchieved, trackStreakBroken, trackMilestoneReached, trackNotificationOpened]
  );
}

/**
 * Hook for tracking engagement events
 */
export function useEngagementAnalytics() {
  const { track } = useAnalytics();

  const trackRatingPromptShown = useCallback(
    async (trigger: string, sessionCount: number, daysSinceInstall: number) => {
      await track('rating_prompt_shown', {
        trigger,
        session_count: sessionCount,
        days_since_install: daysSinceInstall,
      });
    },
    [track]
  );

  const trackRatingSubmitted = useCallback(
    async (rating: number, trigger: string) => {
      await track('rating_submitted', {
        rating,
        trigger,
      });
    },
    [track]
  );

  const trackFeedbackSubmitted = useCallback(
    async (
      feedbackType: 'bug' | 'feature' | 'general',
      feedbackLength: number,
      includesScreenshot: boolean
    ) => {
      await track('feedback_submitted', {
        feedback_type: feedbackType,
        feedback_length: feedbackLength,
        includes_screenshot: includesScreenshot,
      });
    },
    [track]
  );

  const trackShareApp = useCallback(
    async (source: string) => {
      await track('share_app_tapped', { source });
    },
    [track]
  );

  const trackReferralCodeGenerated = useCallback(
    async (code: string) => {
      await track('referral_code_generated', { code });
    },
    [track]
  );

  const trackReferralCodeUsed = useCallback(
    async (code: string, referrerId: string) => {
      await track('referral_code_used', {
        code,
        referrer_id: referrerId,
      });
    },
    [track]
  );

  return useMemo(
    () => ({
      trackRatingPromptShown,
      trackRatingSubmitted,
      trackFeedbackSubmitted,
      trackShareApp,
      trackReferralCodeGenerated,
      trackReferralCodeUsed,
    }),
    [
      trackRatingPromptShown,
      trackRatingSubmitted,
      trackFeedbackSubmitted,
      trackShareApp,
      trackReferralCodeGenerated,
      trackReferralCodeUsed,
    ]
  );
}

export default useAnalytics;
