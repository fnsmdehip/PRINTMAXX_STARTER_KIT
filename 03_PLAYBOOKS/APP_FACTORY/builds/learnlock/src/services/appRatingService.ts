/**
 * App Rating Service for StudyLock
 */

import { Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { analytics } from './analyticsService';
import { STORAGE_KEYS } from '../utils/constants';

const RATING_STORAGE_KEY = STORAGE_KEYS.USER_SETTINGS + '/rating';
const MIN_DAYS_BETWEEN_PROMPTS = 30;
const MIN_SESSIONS_FOR_PROMPT = 10;
const MIN_STREAK_FOR_PROMPT = 5;

interface RatingState {
  lastPromptDate: string | null;
  promptCount: number;
  hasRated: boolean;
  sessionsCompleted: number;
}

class AppRatingService {
  private state: RatingState = {
    lastPromptDate: null,
    promptCount: 0,
    hasRated: false,
    sessionsCompleted: 0,
  };

  async initialize(): Promise<void> {
    try {
      const saved = await AsyncStorage.getItem(RATING_STORAGE_KEY);
      if (saved) {
        this.state = JSON.parse(saved);
      }
    } catch (error) {
      console.error('[AppRating] Failed to load state:', error);
    }
  }

  private async saveState(): Promise<void> {
    try {
      await AsyncStorage.setItem(RATING_STORAGE_KEY, JSON.stringify(this.state));
    } catch (error) {
      console.error('[AppRating] Failed to save state:', error);
    }
  }

  async recordSessionCompleted(): Promise<void> {
    this.state.sessionsCompleted++;
    await this.saveState();
  }

  shouldPrompt(currentStreak: number): boolean {
    if (this.state.hasRated) return false;
    if (this.state.sessionsCompleted < MIN_SESSIONS_FOR_PROMPT) return false;
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
      'Enjoying StudyLock?',
      'Your feedback helps other students discover this app. Would you like to leave a review?',
      [
        {
          text: 'Not now',
          style: 'cancel',
          onPress: () => analytics.trackRatingPrompt(false),
        },
        {
          text: 'Rate app',
          onPress: async () => {
            this.state.hasRated = true;
            await this.saveState();
            analytics.trackRatingPrompt(true);
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
