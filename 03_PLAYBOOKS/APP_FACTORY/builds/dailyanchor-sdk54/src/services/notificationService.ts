/**
 * Notification Service Template
 *
 * Copy this to: src/services/notificationService.ts
 *
 * Dependencies: expo-notifications
 * Install: npx expo install expo-notifications
 * Also add to app.json plugins: ["expo-notifications"]
 */

import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

// Configure notification handler
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
    priority: Notifications.AndroidNotificationPriority.HIGH,
  }),
});

class NotificationService {
  async requestPermissions(): Promise<boolean> {
    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;

    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }

    if (finalStatus !== 'granted') {
      return false;
    }

    if (Platform.OS === 'android') {
      await Notifications.setNotificationChannelAsync('default', {
        name: 'Default',
        importance: Notifications.AndroidImportance.HIGH,
        vibrationPattern: [0, 250, 250, 250],
      });
    }

    return true;
  }

  async scheduleDailyReminder(hour: number, minute: number, title: string, body: string): Promise<string | null> {
    try {
      const id = await Notifications.scheduleNotificationAsync({
        content: {
          title,
          body,
          sound: true,
        },
        trigger: {
          type: Notifications.SchedulableTriggerInputTypes.DAILY,
          hour,
          minute,
        },
      });
      return id;
    } catch (error) {
      console.error('Failed to schedule daily reminder:', error);
      return null;
    }
  }

  async scheduleStreakReminder(hour: number, minute: number, streakCount: number): Promise<string | null> {
    const body = streakCount > 0
      ? `You're on a ${streakCount}-day streak. Keep it going!`
      : `Start your streak today. Every day counts.`;

    return this.scheduleDailyReminder(
      hour,
      minute,
      'Keep your streak alive',
      body
    );
  }

  async cancelAllNotifications(): Promise<void> {
    await Notifications.cancelAllScheduledNotificationsAsync();
  }

  async cancelNotification(id: string): Promise<void> {
    await Notifications.cancelScheduledNotificationAsync(id);
  }

  async getScheduledNotifications(): Promise<Notifications.NotificationRequest[]> {
    return Notifications.getAllScheduledNotificationsAsync();
  }
}

export const notificationService = new NotificationService();
export default notificationService;
