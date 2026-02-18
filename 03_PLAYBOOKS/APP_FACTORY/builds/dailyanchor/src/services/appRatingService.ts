/**
 * App Rating Service for DailyAnchor
 * Non-manipulative, user-friendly app rating prompts
 */

import { Platform, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { analytics } from './analyticsService';

const STORAGE_KEY = '@dailyanchor/app_rating';
const MIN_DAYS_BETWEEN_PROMPTS = 30;
const MIN_STREAK_FOR_PROMPT = 7;
const MIN_JOURNAL_ENTRIES = 5;

interface RatingState {
  lastPromptDate: string | null;
  promptCount: number;
  hasRated: boolean;
  journalEntries: number;
}

class AppRatingService {
  private state: RatingState = {
    lastPromptDate: null,
    promptCount: 0,
    hasRated: false,
    journalEntries: 0,
  };

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

  private async saveState(): Promise<void> {
    try {
      await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(this.state));
    } catch (error) {
      console.error('[AppRating] Failed to save state:', error);
    }
  }

  async recordJournalEntry(): Promise<void> {
    this.state.journalEntries++;
    await this.saveState();
  }

  shouldPrompt(currentStreak: number): boolean {
    if (this.state.hasRated) return false;
    if (this.state.journalEntries < MIN_JOURNAL_ENTRIES) return false;
    if (currentStreak < MIN_STREAK_FOR_PROMPT) return false;

    if (this.state.lastPromptDate) {
      const lastPrompt = new Date(this.state.lastPromptDate);
      const daysSincePrompt = Math.floor(
        (Date.now() - lastPrompt.getTime()) / (1000 * 60 * 60 * 24)
      );
      if (daysSincePrompt < MIN_DAYS_BETWEEN_PROMPTS) return false;
    }

    if (this.state.promptCount >= 3) return false;

    return true;
  }

  async showRatingPrompt(): Promise<void> {
    this.state.lastPromptDate = new Date().toISOString();
    this.state.promptCount++;
    await this.saveState();

    analytics.track('app_rating_prompted');

    Alert.alert(
      'Enjoying DailyAnchor?',
      'Your feedback helps others discover this app. Would you like to leave a review?',
      [
        {
          text: 'Not now',
          style: 'cancel',
          onPress: () => analytics.track('app_rating_declined'),
        },
        {
          text: 'Rate app',
          onPress: async () => {
            this.state.hasRated = true;
            await this.saveState();
            analytics.track('app_rating_accepted');
            // TODO: Open store URL
          },
        },
      ]
    );
  }

  async maybeShowPrompt(currentStreak: number): Promise<void> {
    if (this.shouldPrompt(currentStreak)) {
      await this.showRatingPrompt();
    }
  }
}

export const appRating = new AppRatingService();
