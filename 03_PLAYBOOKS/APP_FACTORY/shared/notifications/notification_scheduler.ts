/**
 * notification_scheduler.ts
 * Smart scheduling logic for notifications
 * Handles timezone, quiet hours, user preferences, and intelligent timing
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import notificationService, { NotificationPreferences } from './NotificationService';

// Storage keys
const STORAGE_KEYS = {
  USER_PATTERNS: '@notification_user_patterns',
  SCHEDULED_QUEUE: '@notification_scheduled_queue',
  LAST_SENT: '@notification_last_sent',
} as const;

// Notification types
type NotificationType =
  | 'morning_reminder'
  | 'streak_at_risk'
  | 'streak_milestone'
  | 'new_content'
  | 'community'
  | 'daily_goal'
  | 'inactivity_nudge'
  | 'goal_achieved'
  | 'workout_reminder'
  | 'focus_start'
  | 'session_complete'
  | 'daily_summary'
  | 'feature_discovery';

// App categories
type AppCategory = 'faith' | 'fitness' | 'productivity';

// Daily limits by notification type
const DAILY_LIMITS: Record<NotificationType, number> = {
  morning_reminder: 1,
  streak_at_risk: 2,
  streak_milestone: 1,
  new_content: 1,
  community: 5,
  daily_goal: 1,
  inactivity_nudge: 2,
  goal_achieved: 1,
  workout_reminder: 2,
  focus_start: 3,
  session_complete: 3,
  daily_summary: 1,
  feature_discovery: 1,
};

// Weekly limits by notification type
const WEEKLY_LIMITS: Record<NotificationType, number> = {
  morning_reminder: 7,
  streak_at_risk: 14,
  streak_milestone: 7,
  new_content: 2,
  community: 20,
  daily_goal: 7,
  inactivity_nudge: 10,
  goal_achieved: 7,
  workout_reminder: 14,
  focus_start: 21,
  session_complete: 21,
  daily_summary: 7,
  feature_discovery: 1,
};

// Default times by notification type and app category
const DEFAULT_TIMES: Record<AppCategory, Partial<Record<NotificationType, { hour: number; minute: number }>>> = {
  faith: {
    morning_reminder: { hour: 6, minute: 30 },
    streak_at_risk: { hour: 20, minute: 0 },
    new_content: { hour: 10, minute: 0 },
  },
  fitness: {
    daily_goal: { hour: 7, minute: 0 },
    inactivity_nudge: { hour: 12, minute: 0 },
    workout_reminder: { hour: 17, minute: 30 },
  },
  productivity: {
    daily_summary: { hour: 20, minute: 0 },
    feature_discovery: { hour: 10, minute: 0 },
  },
};

interface UserPatterns {
  typicalActivityTimes: Record<string, number[]>; // Day of week -> hours
  averageOpenDelay: number; // Minutes between notification and open
  preferredDays: number[]; // Days user is most active (1-7)
  ignoredTypes: NotificationType[]; // Types user doesn't engage with
  lastActivityByType: Record<NotificationType, string>; // ISO date strings
}

interface ScheduledItem {
  id: string;
  type: NotificationType;
  scheduledTime: string; // ISO date string
  title: string;
  body: string;
  data?: Record<string, unknown>;
}

interface SendHistory {
  type: NotificationType;
  sentAt: string;
  opened: boolean;
}

class NotificationScheduler {
  private patterns: UserPatterns | null = null;
  private queue: ScheduledItem[] = [];
  private sendHistory: SendHistory[] = [];
  private preferences: NotificationPreferences;
  private appCategory: AppCategory = 'productivity';

  constructor() {
    this.preferences = notificationService.getPreferences();
    this.init();
  }

  private async init(): Promise<void> {
    await this.loadPatterns();
    await this.loadQueue();
    await this.loadHistory();
  }

  /**
   * Set the app category for default timing
   */
  setAppCategory(category: AppCategory): void {
    this.appCategory = category;
  }

  /**
   * Get the optimal time to send a notification
   */
  getOptimalTime(type: NotificationType, preferredDate?: Date): Date {
    const baseDate = preferredDate || new Date();
    const result = new Date(baseDate);

    // Get default time for this type and category
    const defaultTime = DEFAULT_TIMES[this.appCategory]?.[type];
    if (defaultTime) {
      result.setHours(defaultTime.hour, defaultTime.minute, 0, 0);
    }

    // Adjust for weekend
    const dayOfWeek = result.getDay();
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
    if (isWeekend && type === 'morning_reminder') {
      result.setHours(result.getHours() + 1); // 1 hour later on weekends
    }

    // Adjust based on user patterns
    if (this.patterns) {
      const typicalTimes = this.patterns.typicalActivityTimes[dayOfWeek];
      if (typicalTimes && typicalTimes.length > 0) {
        // Use user's typical activity time if available
        const avgHour = Math.round(
          typicalTimes.reduce((a, b) => a + b, 0) / typicalTimes.length
        );

        // Only adjust for certain types
        if (['workout_reminder', 'focus_start'].includes(type)) {
          result.setHours(avgHour - 1); // Remind 1 hour before typical time
        }
      }
    }

    // Ensure not in quiet hours
    const adjustedTime = this.adjustForQuietHours(result);

    return adjustedTime;
  }

  /**
   * Adjust time to avoid quiet hours
   */
  private adjustForQuietHours(time: Date): Date {
    const hour = time.getHours();
    const { quietHoursStart, quietHoursEnd } = this.preferences;

    // Check if in quiet hours
    const inQuietHours = this.isInQuietHours(hour, quietHoursStart, quietHoursEnd);

    if (inQuietHours) {
      const adjusted = new Date(time);
      adjusted.setHours(quietHoursEnd, 0, 0, 0);

      // If that pushes to past, move to next day
      if (adjusted <= time) {
        adjusted.setDate(adjusted.getDate() + 1);
      }

      return adjusted;
    }

    return time;
  }

  /**
   * Check if hour is in quiet hours
   */
  private isInQuietHours(hour: number, start: number, end: number): boolean {
    if (start > end) {
      // Spans midnight (e.g., 22:00 - 07:00)
      return hour >= start || hour < end;
    }
    return hour >= start && hour < end;
  }

  /**
   * Check if we can send a notification of this type
   */
  async canSend(type: NotificationType): Promise<{ allowed: boolean; reason?: string }> {
    // Check if notifications are enabled
    if (!this.preferences.enabled) {
      return { allowed: false, reason: 'Notifications disabled' };
    }

    // Check type-specific preferences
    if (type === 'morning_reminder' && !this.preferences.morningReminders) {
      return { allowed: false, reason: 'Morning reminders disabled' };
    }
    if (type.includes('streak') && !this.preferences.streakAlerts) {
      return { allowed: false, reason: 'Streak alerts disabled' };
    }
    if (type === 'new_content' && !this.preferences.newContent) {
      return { allowed: false, reason: 'New content notifications disabled' };
    }

    // Check daily limit
    const todaySent = this.getTodayCountByType(type);
    if (todaySent >= DAILY_LIMITS[type]) {
      return { allowed: false, reason: `Daily limit reached for ${type}` };
    }

    // Check weekly limit
    const weekSent = this.getWeekCountByType(type);
    if (weekSent >= WEEKLY_LIMITS[type]) {
      return { allowed: false, reason: `Weekly limit reached for ${type}` };
    }

    // Check global daily limit
    const totalToday = this.getTodayTotalCount();
    if (totalToday >= 3) {
      return { allowed: false, reason: 'Global daily limit reached' };
    }

    // Check if user ignores this type
    if (this.patterns?.ignoredTypes.includes(type)) {
      return { allowed: false, reason: 'User ignores this notification type' };
    }

    return { allowed: true };
  }

  /**
   * Get count of notifications sent today by type
   */
  private getTodayCountByType(type: NotificationType): number {
    const today = new Date().toDateString();
    return this.sendHistory.filter(
      (h) => h.type === type && new Date(h.sentAt).toDateString() === today
    ).length;
  }

  /**
   * Get count of notifications sent this week by type
   */
  private getWeekCountByType(type: NotificationType): number {
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);

    return this.sendHistory.filter(
      (h) => h.type === type && new Date(h.sentAt) > weekAgo
    ).length;
  }

  /**
   * Get total notifications sent today
   */
  private getTodayTotalCount(): number {
    const today = new Date().toDateString();
    return this.sendHistory.filter(
      (h) => new Date(h.sentAt).toDateString() === today
    ).length;
  }

  /**
   * Schedule a notification with smart timing
   */
  async scheduleSmartNotification(params: {
    type: NotificationType;
    title: string;
    body: string;
    preferredTime?: Date;
    data?: Record<string, unknown>;
  }): Promise<string | null> {
    const { allowed, reason } = await this.canSend(params.type);

    if (!allowed) {
      console.log(`Notification blocked: ${reason}`);
      return null;
    }

    const scheduledTime = this.getOptimalTime(params.type, params.preferredTime);

    // Don't schedule if time is in the past
    if (scheduledTime <= new Date()) {
      console.log('Scheduled time is in the past, skipping');
      return null;
    }

    const id = await notificationService.scheduleNotification({
      title: params.title,
      body: params.body,
      scheduledTime,
      type: this.getChannelForType(params.type),
      data: { ...params.data, notificationType: params.type },
    });

    // Add to queue
    this.queue.push({
      id,
      type: params.type,
      scheduledTime: scheduledTime.toISOString(),
      title: params.title,
      body: params.body,
      data: params.data,
    });
    await this.saveQueue();

    return id;
  }

  /**
   * Map notification type to channel
   */
  private getChannelForType(type: NotificationType): 'reminders' | 'streaks' | 'content' | 'achievements' | 'community' {
    if (type.includes('streak')) return 'streaks';
    if (type.includes('content')) return 'content';
    if (type.includes('milestone') || type.includes('achieved')) return 'achievements';
    if (type.includes('community')) return 'community';
    return 'reminders';
  }

  /**
   * Schedule daily reminders for the week
   */
  async scheduleDailyReminders(params: {
    type: NotificationType;
    title: string;
    bodyVariants: string[];
    hour: number;
    minute: number;
  }): Promise<string[]> {
    const ids: string[] = [];

    for (let i = 0; i < 7; i++) {
      const date = new Date();
      date.setDate(date.getDate() + i);
      date.setHours(params.hour, params.minute, 0, 0);

      // Skip if in the past
      if (date <= new Date()) continue;

      // Rotate through body variants
      const body = params.bodyVariants[i % params.bodyVariants.length];

      const id = await this.scheduleSmartNotification({
        type: params.type,
        title: params.title,
        body,
        preferredTime: date,
      });

      if (id) ids.push(id);
    }

    return ids;
  }

  /**
   * Record that a notification was sent
   */
  async recordSent(type: NotificationType): Promise<void> {
    this.sendHistory.push({
      type,
      sentAt: new Date().toISOString(),
      opened: false,
    });

    // Keep only last 100 entries
    if (this.sendHistory.length > 100) {
      this.sendHistory = this.sendHistory.slice(-100);
    }

    await this.saveHistory();
  }

  /**
   * Record that a notification was opened
   */
  async recordOpened(type: NotificationType): Promise<void> {
    // Find most recent of this type and mark as opened
    for (let i = this.sendHistory.length - 1; i >= 0; i--) {
      if (this.sendHistory[i].type === type && !this.sendHistory[i].opened) {
        this.sendHistory[i].opened = true;
        break;
      }
    }

    await this.saveHistory();
    await this.updatePatterns(type);
  }

  /**
   * Update user patterns based on engagement
   */
  private async updatePatterns(type: NotificationType): Promise<void> {
    if (!this.patterns) {
      this.patterns = {
        typicalActivityTimes: {},
        averageOpenDelay: 0,
        preferredDays: [],
        ignoredTypes: [],
        lastActivityByType: {},
      };
    }

    const now = new Date();
    const dayOfWeek = now.getDay();
    const hour = now.getHours();

    // Update typical activity times
    if (!this.patterns.typicalActivityTimes[dayOfWeek]) {
      this.patterns.typicalActivityTimes[dayOfWeek] = [];
    }
    this.patterns.typicalActivityTimes[dayOfWeek].push(hour);

    // Keep only last 10 entries per day
    if (this.patterns.typicalActivityTimes[dayOfWeek].length > 10) {
      this.patterns.typicalActivityTimes[dayOfWeek] =
        this.patterns.typicalActivityTimes[dayOfWeek].slice(-10);
    }

    // Update last activity for this type
    this.patterns.lastActivityByType[type] = now.toISOString();

    // Update preferred days
    if (!this.patterns.preferredDays.includes(dayOfWeek)) {
      this.patterns.preferredDays.push(dayOfWeek);
    }

    await this.savePatterns();
  }

  /**
   * Check for ignored notification types
   */
  async updateIgnoredTypes(): Promise<void> {
    if (!this.patterns) return;

    // Get types with low open rates
    const typeStats: Record<NotificationType, { sent: number; opened: number }> = {} as any;

    for (const entry of this.sendHistory) {
      if (!typeStats[entry.type]) {
        typeStats[entry.type] = { sent: 0, opened: 0 };
      }
      typeStats[entry.type].sent++;
      if (entry.opened) typeStats[entry.type].opened++;
    }

    this.patterns.ignoredTypes = [];
    for (const [type, stats] of Object.entries(typeStats)) {
      if (stats.sent >= 5 && stats.opened / stats.sent < 0.1) {
        // Less than 10% open rate with at least 5 samples
        this.patterns.ignoredTypes.push(type as NotificationType);
      }
    }

    await this.savePatterns();
  }

  /**
   * Cancel all scheduled notifications of a type
   */
  async cancelByType(type: NotificationType): Promise<void> {
    const toCancel = this.queue.filter((item) => item.type === type);

    for (const item of toCancel) {
      await notificationService.cancelNotification(item.id);
    }

    this.queue = this.queue.filter((item) => item.type !== type);
    await this.saveQueue();
  }

  /**
   * Get engagement stats
   */
  getEngagementStats(): {
    overallOpenRate: number;
    byType: Record<string, { sent: number; opened: number; rate: number }>;
  } {
    const byType: Record<string, { sent: number; opened: number; rate: number }> = {};
    let totalSent = 0;
    let totalOpened = 0;

    for (const entry of this.sendHistory) {
      if (!byType[entry.type]) {
        byType[entry.type] = { sent: 0, opened: 0, rate: 0 };
      }
      byType[entry.type].sent++;
      totalSent++;
      if (entry.opened) {
        byType[entry.type].opened++;
        totalOpened++;
      }
    }

    // Calculate rates
    for (const type of Object.keys(byType)) {
      byType[type].rate = byType[type].sent > 0
        ? byType[type].opened / byType[type].sent
        : 0;
    }

    return {
      overallOpenRate: totalSent > 0 ? totalOpened / totalSent : 0,
      byType,
    };
  }

  // Storage methods
  private async loadPatterns(): Promise<void> {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.USER_PATTERNS);
      if (stored) this.patterns = JSON.parse(stored);
    } catch (error) {
      console.error('Failed to load patterns:', error);
    }
  }

  private async savePatterns(): Promise<void> {
    if (this.patterns) {
      await AsyncStorage.setItem(
        STORAGE_KEYS.USER_PATTERNS,
        JSON.stringify(this.patterns)
      );
    }
  }

  private async loadQueue(): Promise<void> {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.SCHEDULED_QUEUE);
      if (stored) this.queue = JSON.parse(stored);
    } catch (error) {
      console.error('Failed to load queue:', error);
    }
  }

  private async saveQueue(): Promise<void> {
    await AsyncStorage.setItem(
      STORAGE_KEYS.SCHEDULED_QUEUE,
      JSON.stringify(this.queue)
    );
  }

  private async loadHistory(): Promise<void> {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.LAST_SENT);
      if (stored) this.sendHistory = JSON.parse(stored);
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  }

  private async saveHistory(): Promise<void> {
    await AsyncStorage.setItem(
      STORAGE_KEYS.LAST_SENT,
      JSON.stringify(this.sendHistory)
    );
  }
}

// Export singleton
export const notificationScheduler = new NotificationScheduler();
export default notificationScheduler;
