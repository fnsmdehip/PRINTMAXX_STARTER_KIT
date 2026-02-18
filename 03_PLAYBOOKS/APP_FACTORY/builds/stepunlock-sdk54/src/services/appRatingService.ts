/**
 * App Rating Service
 * Non-manipulative, user-friendly app rating prompts
 * Follows Apple and Google guidelines
 */

import { Platform, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { analytics } from './analyticsService';

const STORAGE_KEY = '@walktounlock/app_rating';
const MIN_DAYS_BETWEEN_PROMPTS = 30;
const MIN_GOALS_BEFORE_PROMPT = 5;
const MIN_STREAK_FOR_PROMPT = 3;

interface RatingState {
  lastPromptDate: string | null;
  promptCount: number;
  hasRated: boolean;
  goalsReached: number;
}

class AppRatingService {
  private state: RatingState = {
    lastPromptDate: null,
    promptCount: 0,
    hasRated: false,
    goalsReached: 0,
  };

  /**
   * Initialize rating service and load saved state
   */
  async initialize(): Promise<void> {
    try {
      const saved = await AsyncStorage.getItem(STORAGE_KEY);
      if (saved) {
        this.state = JSON.parse(saved);
      }
    } catch (error) {
      console.error('[AppRating] Failed to load state:', error);
    }
  }

  /**
   * Save state to storage
   */
  private async saveState(): Promise<void> {
    try {
      await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(this.state));
    } catch (error) {
      console.error('[AppRating] Failed to save state:', error);
    }
  }

  /**
   * Record a goal being reached
   */
  async recordGoalReached(): Promise<void> {
    this.state.goalsReached++;
    await this.saveState();
  }

  /**
   * Check if we should show rating prompt
   * Call this after positive moments (goal reached, streak milestone)
   */
  shouldPrompt(currentStreak: number): boolean {
    // Never prompt if user already rated
    if (this.state.hasRated) {
      return false;
    }

    // Check minimum goals reached
    if (this.state.goalsReached < MIN_GOALS_BEFORE_PROMPT) {
      return false;
    }

    // Check minimum streak
    if (currentStreak < MIN_STREAK_FOR_PROMPT) {
      return false;
    }

    // Check time since last prompt
    if (this.state.lastPromptDate) {
      const lastPrompt = new Date(this.state.lastPromptDate);
      const daysSincePrompt = Math.floor(
        (Date.now() - lastPrompt.getTime()) / (1000 * 60 * 60 * 24)
      );
      if (daysSincePrompt < MIN_DAYS_BETWEEN_PROMPTS) {
        return false;
      }
    }

    // Limit total prompts
    if (this.state.promptCount >= 3) {
      return false;
    }

    return true;
  }

  /**
   * Show rating prompt using native API
   * Call this after checking shouldPrompt()
   */
  async showRatingPrompt(): Promise<void> {
    // Update state
    this.state.lastPromptDate = new Date().toISOString();
    this.state.promptCount++;
    await this.saveState();

    // Track analytics
    analytics.track('app_rating_prompted');

    // Use native store review API
    if (Platform.OS === 'ios') {
      // For iOS, use StoreKit
      // Note: In production, use expo-store-review or react-native-store-review
      try {
        // const StoreReview = require('react-native-store-review');
        // StoreReview.requestReview();

        // Fallback for development
        this.showFallbackPrompt();
      } catch (error) {
        console.error('[AppRating] Store review failed:', error);
        this.showFallbackPrompt();
      }
    } else {
      // For Android, use In-App Review API
      try {
        // const InAppReview = require('react-native-in-app-review');
        // if (InAppReview.isAvailable()) {
        //   InAppReview.RequestInAppReview();
        // }

        // Fallback for development
        this.showFallbackPrompt();
      } catch (error) {
        console.error('[AppRating] In-app review failed:', error);
        this.showFallbackPrompt();
      }
    }
  }

  /**
   * Fallback prompt for development/testing
   */
  private showFallbackPrompt(): void {
    Alert.alert(
      'Enjoying WalkToUnlock?',
      'Your feedback helps us improve. Would you like to rate the app?',
      [
        {
          text: 'Not now',
          style: 'cancel',
          onPress: () => {
            analytics.trackRatingPrompt(false);
          },
        },
        {
          text: 'Rate app',
          onPress: () => {
            this.state.hasRated = true;
            this.saveState();
            analytics.trackRatingPrompt(true);
            // In production, open store URL
            // Linking.openURL('https://apps.apple.com/app/idXXXXXX');
          },
        },
      ]
    );
  }

  /**
   * Mark that user has rated the app
   * Call this if user rates through settings
   */
  async markAsRated(): Promise<void> {
    this.state.hasRated = true;
    await this.saveState();
  }

  /**
   * Check conditions and show prompt if appropriate
   * Best moments to call:
   * - After reaching daily goal
   * - After hitting a streak milestone (7, 14, 30 days)
   */
  async maybeShowPrompt(currentStreak: number): Promise<void> {
    if (this.shouldPrompt(currentStreak)) {
      await this.showRatingPrompt();
    }
  }
}

// Export singleton instance
export const appRating = new AppRatingService();
