import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

// Configure notification handler
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
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

    return finalStatus === 'granted';
  }

  async scheduleDailyReminder(hour: number, minute: number): Promise<void> {
    // Cancel existing reminders first
    await this.cancelAllReminders();

    const hasPermission = await this.requestPermissions();
    if (!hasPermission) return;

    const messages = [
      'Time to start your day with prayer. Your streak is counting on you.',
      'Good morning. God is waiting to hear from you.',
      'Your daily devotional is ready. Build that prayer habit.',
      'Rise and pray. Your spiritual growth matters.',
      'Another day, another chance to connect with God.',
      'Your prayer streak needs you. Start your devotional now.',
      'Morning prayer changes everything. Begin your day right.',
    ];

    const randomMessage = messages[Math.floor(Math.random() * messages.length)];

    await Notifications.scheduleNotificationAsync({
      content: {
        title: 'PrayerLock',
        body: randomMessage,
        sound: true,
        badge: 1,
      },
      trigger: {
        type: Notifications.SchedulableTriggerInputTypes.DAILY,
        hour,
        minute,
      },
    });
  }

  async scheduleStreakReminder(): Promise<void> {
    const hasPermission = await this.requestPermissions();
    if (!hasPermission) return;

    // Schedule evening reminder if devotional not done
    await Notifications.scheduleNotificationAsync({
      content: {
        title: 'PrayerLock',
        body: "You haven't done your devotional today. Don't break your streak.",
        sound: true,
        badge: 1,
      },
      trigger: {
        type: Notifications.SchedulableTriggerInputTypes.DAILY,
        hour: 20,
        minute: 0,
      },
    });
  }

  async cancelAllReminders(): Promise<void> {
    await Notifications.cancelAllScheduledNotificationsAsync();
  }
}

export const notificationService = new NotificationService();
