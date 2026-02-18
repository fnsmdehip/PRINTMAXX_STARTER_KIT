// Notifications for DevotionFlow
// Uses expo-notifications for daily devotional reminders

import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

// Configure notification behavior
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
  }),
});

/**
 * Request notification permissions
 */
export async function requestPermissions(): Promise<boolean> {
  try {
    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;

    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }

    if (finalStatus !== 'granted') {
      console.log('Notification permissions not granted');
      return false;
    }

    // iOS specific setup
    if (Platform.OS === 'ios') {
      await Notifications.setNotificationCategoryAsync('devotion', [
        {
          identifier: 'read',
          buttonTitle: 'Read Now',
          options: { opensAppToForeground: true },
        },
      ]);
    }

    return true;
  } catch (error) {
    console.error('Error requesting notification permissions:', error);
    return false;
  }
}

/**
 * Schedule daily devotional reminder
 * @param hour - Hour of day (0-23)
 * @param minute - Minute of hour (0-59)
 */
export async function scheduleDailyReminder(
  hour: number,
  minute: number
): Promise<string | null> {
  try {
    // Cancel existing reminders first
    await cancelAllReminders();

    const identifier = await Notifications.scheduleNotificationAsync({
      content: {
        title: 'Good morning',
        body: 'Your daily devotional is waiting for you.',
        sound: 'default',
        categoryIdentifier: 'devotion',
        data: { type: 'daily_devotion' },
      },
      trigger: {
        hour,
        minute,
        repeats: true,
      },
    });

    console.log(`Daily reminder scheduled for ${hour}:${minute}`);
    return identifier;
  } catch (error) {
    console.error('Error scheduling daily reminder:', error);
    return null;
  }
}

/**
 * Schedule streak reminder (if user misses a day)
 */
export async function scheduleStreakReminder(): Promise<string | null> {
  try {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(20, 0, 0, 0); // 8 PM

    const identifier = await Notifications.scheduleNotificationAsync({
      content: {
        title: 'Keep your streak going',
        body: "Don't forget to read today's devotional.",
        sound: 'default',
        data: { type: 'streak_reminder' },
      },
      trigger: {
        date: tomorrow,
      },
    });

    return identifier;
  } catch (error) {
    console.error('Error scheduling streak reminder:', error);
    return null;
  }
}

/**
 * Cancel all scheduled notifications
 */
export async function cancelAllReminders(): Promise<void> {
  try {
    await Notifications.cancelAllScheduledNotificationsAsync();
    console.log('All reminders cancelled');
  } catch (error) {
    console.error('Error cancelling reminders:', error);
  }
}

/**
 * Get all scheduled notifications
 */
export async function getScheduledReminders(): Promise<Notifications.NotificationRequest[]> {
  try {
    return await Notifications.getAllScheduledNotificationsAsync();
  } catch (error) {
    console.error('Error getting scheduled notifications:', error);
    return [];
  }
}

/**
 * Add listener for received notifications
 */
export function addNotificationReceivedListener(
  callback: (notification: Notifications.Notification) => void
): Notifications.Subscription {
  return Notifications.addNotificationReceivedListener(callback);
}

/**
 * Add listener for notification responses (user tapped)
 */
export function addNotificationResponseListener(
  callback: (response: Notifications.NotificationResponse) => void
): Notifications.Subscription {
  return Notifications.addNotificationResponseReceivedListener(callback);
}

/**
 * Send immediate local notification (for testing)
 */
export async function sendTestNotification(): Promise<void> {
  await Notifications.scheduleNotificationAsync({
    content: {
      title: 'DevotionFlow',
      body: 'This is a test notification.',
      sound: 'default',
    },
    trigger: null, // Send immediately
  });
}

// Preset notification times
export const notificationPresets = [
  { label: 'Early morning (6:00 AM)', hour: 6, minute: 0 },
  { label: 'Morning (7:00 AM)', hour: 7, minute: 0 },
  { label: 'Mid-morning (8:00 AM)', hour: 8, minute: 0 },
  { label: 'Lunch (12:00 PM)', hour: 12, minute: 0 },
  { label: 'Evening (6:00 PM)', hour: 18, minute: 0 },
  { label: 'Night (9:00 PM)', hour: 21, minute: 0 },
];
