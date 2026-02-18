/**
 * NotificationService.ts
 * Core notification service for React Native apps
 * Handles permissions, tokens, local scheduling, and remote notifications
 */

import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Storage keys
const STORAGE_KEYS = {
  PUSH_TOKEN: '@notification_push_token',
  PERMISSION_STATUS: '@notification_permission_status',
  USER_PREFERENCES: '@notification_preferences',
  SCHEDULED_IDS: '@notification_scheduled_ids',
  ENGAGEMENT_LOG: '@notification_engagement_log',
} as const;

// Notification channel IDs (Android)
const CHANNELS = {
  REMINDERS: 'reminders',
  STREAKS: 'streaks',
  CONTENT: 'content',
  ACHIEVEMENTS: 'achievements',
  COMMUNITY: 'community',
} as const;

export interface NotificationPreferences {
  enabled: boolean;
  morningReminders: boolean;
  streakAlerts: boolean;
  newContent: boolean;
  achievements: boolean;
  quietHoursStart: number; // Hour in 24h format
  quietHoursEnd: number;
  timezone: string;
}

export interface ScheduledNotification {
  id: string;
  title: string;
  body: string;
  scheduledTime: Date;
  type: keyof typeof CHANNELS;
  data?: Record<string, unknown>;
}

export interface NotificationEngagement {
  notificationId: string;
  type: string;
  receivedAt: string;
  openedAt?: string;
  actionTaken?: string;
}

const DEFAULT_PREFERENCES: NotificationPreferences = {
  enabled: true,
  morningReminders: true,
  streakAlerts: true,
  newContent: true,
  achievements: true,
  quietHoursStart: 22, // 10 PM
  quietHoursEnd: 7, // 7 AM
  timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
};

class NotificationService {
  private pushToken: string | null = null;
  private preferences: NotificationPreferences = DEFAULT_PREFERENCES;
  private scheduledIds: string[] = [];

  constructor() {
    this.init();
  }

  private async init(): Promise<void> {
    await this.loadPreferences();
    await this.loadScheduledIds();
    this.setupNotificationHandler();
    await this.setupAndroidChannels();
  }

  /**
   * Set up notification handlers
   */
  private setupNotificationHandler(): void {
    // Handle notifications when app is in foreground
    Notifications.setNotificationHandler({
      handleNotification: async () => ({
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: true,
      }),
    });
  }

  /**
   * Create Android notification channels
   */
  private async setupAndroidChannels(): Promise<void> {
    if (Platform.OS !== 'android') return;

    const channelConfigs = [
      {
        id: CHANNELS.REMINDERS,
        name: 'Daily Reminders',
        description: 'Your daily activity reminders',
        importance: Notifications.AndroidImportance.HIGH,
      },
      {
        id: CHANNELS.STREAKS,
        name: 'Streak Alerts',
        description: 'Notifications about your streaks',
        importance: Notifications.AndroidImportance.HIGH,
      },
      {
        id: CHANNELS.CONTENT,
        name: 'New Content',
        description: 'Updates when new content is available',
        importance: Notifications.AndroidImportance.DEFAULT,
      },
      {
        id: CHANNELS.ACHIEVEMENTS,
        name: 'Achievements',
        description: 'Celebrate your milestones',
        importance: Notifications.AndroidImportance.DEFAULT,
      },
      {
        id: CHANNELS.COMMUNITY,
        name: 'Community',
        description: 'Activity from the community',
        importance: Notifications.AndroidImportance.LOW,
      },
    ];

    for (const config of channelConfigs) {
      await Notifications.setNotificationChannelAsync(config.id, {
        name: config.name,
        description: config.description,
        importance: config.importance,
        vibrationPattern: [0, 250, 250, 250],
        lightColor: '#FF6B35',
      });
    }
  }

  /**
   * Request notification permissions
   * Returns true if granted, false otherwise
   */
  async requestPermissions(): Promise<boolean> {
    if (!Device.isDevice) {
      console.log('Push notifications require a physical device');
      return false;
    }

    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;

    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }

    const granted = finalStatus === 'granted';
    await AsyncStorage.setItem(STORAGE_KEYS.PERMISSION_STATUS, finalStatus);

    if (granted) {
      await this.registerForPushNotifications();
    }

    return granted;
  }

  /**
   * Check if permissions are granted
   */
  async hasPermission(): Promise<boolean> {
    const { status } = await Notifications.getPermissionsAsync();
    return status === 'granted';
  }

  /**
   * Register for push notifications and get token
   */
  async registerForPushNotifications(): Promise<string | null> {
    try {
      const token = await Notifications.getExpoPushTokenAsync({
        projectId: process.env.EXPO_PROJECT_ID,
      });

      this.pushToken = token.data;
      await AsyncStorage.setItem(STORAGE_KEYS.PUSH_TOKEN, this.pushToken);

      // Send token to your backend
      await this.sendTokenToBackend(this.pushToken);

      return this.pushToken;
    } catch (error) {
      console.error('Failed to get push token:', error);
      return null;
    }
  }

  /**
   * Send push token to backend for remote notifications
   */
  private async sendTokenToBackend(token: string): Promise<void> {
    // Replace with your actual backend endpoint
    const BACKEND_URL = process.env.NOTIFICATION_API_URL;
    if (!BACKEND_URL) return;

    try {
      await fetch(`${BACKEND_URL}/api/notifications/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token,
          platform: Platform.OS,
          timezone: this.preferences.timezone,
        }),
      });
    } catch (error) {
      console.error('Failed to register token with backend:', error);
    }
  }

  /**
   * Schedule a local notification
   */
  async scheduleNotification(notification: Omit<ScheduledNotification, 'id'>): Promise<string> {
    // Check if in quiet hours
    if (this.isInQuietHours(notification.scheduledTime)) {
      const adjustedTime = this.getNextValidTime(notification.scheduledTime);
      notification.scheduledTime = adjustedTime;
    }

    const trigger = new Date(notification.scheduledTime);

    const id = await Notifications.scheduleNotificationAsync({
      content: {
        title: notification.title,
        body: notification.body,
        data: notification.data || {},
        sound: true,
        priority: Notifications.AndroidNotificationPriority.HIGH,
      },
      trigger,
    });

    this.scheduledIds.push(id);
    await this.saveScheduledIds();

    return id;
  }

  /**
   * Schedule a repeating notification
   */
  async scheduleRepeatingNotification(params: {
    title: string;
    body: string;
    hour: number;
    minute: number;
    weekdays?: number[]; // 1-7, Sunday = 1
    type: keyof typeof CHANNELS;
    data?: Record<string, unknown>;
  }): Promise<string[]> {
    const ids: string[] = [];
    const weekdays = params.weekdays || [1, 2, 3, 4, 5, 6, 7];

    for (const weekday of weekdays) {
      const id = await Notifications.scheduleNotificationAsync({
        content: {
          title: params.title,
          body: params.body,
          data: params.data || {},
          sound: true,
        },
        trigger: {
          hour: params.hour,
          minute: params.minute,
          weekday,
          repeats: true,
        },
      });
      ids.push(id);
    }

    this.scheduledIds.push(...ids);
    await this.saveScheduledIds();

    return ids;
  }

  /**
   * Cancel a scheduled notification
   */
  async cancelNotification(id: string): Promise<void> {
    await Notifications.cancelScheduledNotificationAsync(id);
    this.scheduledIds = this.scheduledIds.filter((i) => i !== id);
    await this.saveScheduledIds();
  }

  /**
   * Cancel all scheduled notifications
   */
  async cancelAllNotifications(): Promise<void> {
    await Notifications.cancelAllScheduledNotificationsAsync();
    this.scheduledIds = [];
    await this.saveScheduledIds();
  }

  /**
   * Get all scheduled notifications
   */
  async getScheduledNotifications(): Promise<Notifications.NotificationRequest[]> {
    return Notifications.getAllScheduledNotificationsAsync();
  }

  /**
   * Handle notification received (foreground)
   */
  addNotificationReceivedListener(
    callback: (notification: Notifications.Notification) => void
  ): Notifications.Subscription {
    return Notifications.addNotificationReceivedListener(callback);
  }

  /**
   * Handle notification response (user tapped)
   */
  addNotificationResponseListener(
    callback: (response: Notifications.NotificationResponse) => void
  ): Notifications.Subscription {
    return Notifications.addNotificationResponseReceivedListener(async (response) => {
      // Log engagement
      await this.logEngagement({
        notificationId: response.notification.request.identifier,
        type: response.notification.request.content.data?.type as string || 'unknown',
        receivedAt: new Date().toISOString(),
        openedAt: new Date().toISOString(),
        actionTaken: response.actionIdentifier,
      });

      callback(response);
    });
  }

  /**
   * Send immediate local notification
   */
  async sendImmediateNotification(params: {
    title: string;
    body: string;
    data?: Record<string, unknown>;
  }): Promise<string> {
    return Notifications.scheduleNotificationAsync({
      content: {
        title: params.title,
        body: params.body,
        data: params.data || {},
        sound: true,
      },
      trigger: null, // Immediate
    });
  }

  /**
   * Update badge count
   */
  async setBadgeCount(count: number): Promise<void> {
    await Notifications.setBadgeCountAsync(count);
  }

  /**
   * Get current badge count
   */
  async getBadgeCount(): Promise<number> {
    return Notifications.getBadgeCountAsync();
  }

  /**
   * Check if time is in quiet hours
   */
  private isInQuietHours(time: Date): boolean {
    const hour = time.getHours();
    const { quietHoursStart, quietHoursEnd } = this.preferences;

    if (quietHoursStart > quietHoursEnd) {
      // Quiet hours span midnight (e.g., 22:00 - 07:00)
      return hour >= quietHoursStart || hour < quietHoursEnd;
    } else {
      // Quiet hours within same day
      return hour >= quietHoursStart && hour < quietHoursEnd;
    }
  }

  /**
   * Get next valid time outside quiet hours
   */
  private getNextValidTime(time: Date): Date {
    const adjusted = new Date(time);
    const { quietHoursEnd } = this.preferences;

    if (this.isInQuietHours(time)) {
      // Move to end of quiet hours
      adjusted.setHours(quietHoursEnd, 0, 0, 0);
      if (adjusted <= time) {
        // If we're past quiet hours end today, move to tomorrow
        adjusted.setDate(adjusted.getDate() + 1);
      }
    }

    return adjusted;
  }

  /**
   * Update user preferences
   */
  async updatePreferences(updates: Partial<NotificationPreferences>): Promise<void> {
    this.preferences = { ...this.preferences, ...updates };
    await AsyncStorage.setItem(
      STORAGE_KEYS.USER_PREFERENCES,
      JSON.stringify(this.preferences)
    );

    // If notifications disabled, cancel all
    if (!this.preferences.enabled) {
      await this.cancelAllNotifications();
    }
  }

  /**
   * Get user preferences
   */
  getPreferences(): NotificationPreferences {
    return { ...this.preferences };
  }

  /**
   * Load preferences from storage
   */
  private async loadPreferences(): Promise<void> {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.USER_PREFERENCES);
      if (stored) {
        this.preferences = { ...DEFAULT_PREFERENCES, ...JSON.parse(stored) };
      }
    } catch (error) {
      console.error('Failed to load notification preferences:', error);
    }
  }

  /**
   * Load scheduled IDs from storage
   */
  private async loadScheduledIds(): Promise<void> {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.SCHEDULED_IDS);
      if (stored) {
        this.scheduledIds = JSON.parse(stored);
      }
    } catch (error) {
      console.error('Failed to load scheduled IDs:', error);
    }
  }

  /**
   * Save scheduled IDs to storage
   */
  private async saveScheduledIds(): Promise<void> {
    await AsyncStorage.setItem(
      STORAGE_KEYS.SCHEDULED_IDS,
      JSON.stringify(this.scheduledIds)
    );
  }

  /**
   * Log notification engagement for analytics
   */
  private async logEngagement(engagement: NotificationEngagement): Promise<void> {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.ENGAGEMENT_LOG);
      const logs: NotificationEngagement[] = stored ? JSON.parse(stored) : [];

      logs.push(engagement);

      // Keep last 100 engagements
      const trimmed = logs.slice(-100);
      await AsyncStorage.setItem(STORAGE_KEYS.ENGAGEMENT_LOG, JSON.stringify(trimmed));

      // Send to analytics backend
      await this.sendEngagementToBackend(engagement);
    } catch (error) {
      console.error('Failed to log engagement:', error);
    }
  }

  /**
   * Send engagement data to backend
   */
  private async sendEngagementToBackend(engagement: NotificationEngagement): Promise<void> {
    const BACKEND_URL = process.env.NOTIFICATION_API_URL;
    if (!BACKEND_URL) return;

    try {
      await fetch(`${BACKEND_URL}/api/notifications/engagement`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(engagement),
      });
    } catch (error) {
      // Silently fail - engagement logging is non-critical
    }
  }

  /**
   * Get engagement statistics
   */
  async getEngagementStats(): Promise<{
    totalReceived: number;
    totalOpened: number;
    openRate: number;
    byType: Record<string, { received: number; opened: number }>;
  }> {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.ENGAGEMENT_LOG);
      const logs: NotificationEngagement[] = stored ? JSON.parse(stored) : [];

      const totalReceived = logs.length;
      const totalOpened = logs.filter((l) => l.openedAt).length;
      const openRate = totalReceived > 0 ? totalOpened / totalReceived : 0;

      const byType: Record<string, { received: number; opened: number }> = {};
      for (const log of logs) {
        if (!byType[log.type]) {
          byType[log.type] = { received: 0, opened: 0 };
        }
        byType[log.type].received++;
        if (log.openedAt) byType[log.type].opened++;
      }

      return { totalReceived, totalOpened, openRate, byType };
    } catch {
      return { totalReceived: 0, totalOpened: 0, openRate: 0, byType: {} };
    }
  }

  /**
   * Get push token
   */
  getPushToken(): string | null {
    return this.pushToken;
  }
}

// Export singleton instance
export const notificationService = new NotificationService();
export default notificationService;
