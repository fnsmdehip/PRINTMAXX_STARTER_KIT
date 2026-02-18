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
export async function requestNotificationPermissions(): Promise<boolean> {
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

  // Required for Android
  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('default', {
      name: 'Default',
      importance: Notifications.AndroidImportance.HIGH,
      vibrationPattern: [0, 250, 250, 250],
    });

    await Notifications.setNotificationChannelAsync('mewing', {
      name: 'Mewing Reminders',
      importance: Notifications.AndroidImportance.DEFAULT,
    });

    await Notifications.setNotificationChannelAsync('routine', {
      name: 'Routine Reminders',
      importance: Notifications.AndroidImportance.HIGH,
    });
  }

  return true;
}

/**
 * Schedule mewing reminder
 */
export async function scheduleMewingReminder(intervalMinutes: number): Promise<string> {
  // Cancel existing mewing reminders
  await cancelMewingReminders();

  const identifier = await Notifications.scheduleNotificationAsync({
    content: {
      title: 'Mewing Check',
      body: 'Tongue on roof of mouth? Check your posture too.',
      sound: true,
    },
    trigger: {
      seconds: intervalMinutes * 60,
      repeats: true,
    },
  });

  return identifier;
}

/**
 * Cancel mewing reminders
 */
export async function cancelMewingReminders(): Promise<void> {
  const scheduled = await Notifications.getAllScheduledNotificationsAsync();
  const mewingNotifications = scheduled.filter(
    (n) => n.content.title?.includes('Mewing')
  );

  for (const notification of mewingNotifications) {
    await Notifications.cancelScheduledNotificationAsync(notification.identifier);
  }
}

/**
 * Schedule morning routine reminder
 */
export async function scheduleMorningRoutineReminder(time: string): Promise<string> {
  const [hours, minutes] = time.split(':').map(Number);

  const identifier = await Notifications.scheduleNotificationAsync({
    content: {
      title: 'Morning Glow Routine',
      body: 'Time to start your skincare and facial exercises!',
      sound: true,
    },
    trigger: {
      hour: hours,
      minute: minutes,
      repeats: true,
    },
  });

  return identifier;
}

/**
 * Schedule evening routine reminder
 */
export async function scheduleEveningRoutineReminder(time: string): Promise<string> {
  const [hours, minutes] = time.split(':').map(Number);

  const identifier = await Notifications.scheduleNotificationAsync({
    content: {
      title: 'Evening Glow Routine',
      body: 'Wind down with your evening skincare routine.',
      sound: true,
    },
    trigger: {
      hour: hours,
      minute: minutes,
      repeats: true,
    },
  });

  return identifier;
}

/**
 * Cancel all scheduled notifications
 */
export async function cancelAllNotifications(): Promise<void> {
  await Notifications.cancelAllScheduledNotificationsAsync();
}

/**
 * Get all scheduled notifications
 */
export async function getScheduledNotifications() {
  return await Notifications.getAllScheduledNotificationsAsync();
}

/**
 * Send immediate notification (for testing)
 */
export async function sendTestNotification(): Promise<void> {
  await Notifications.scheduleNotificationAsync({
    content: {
      title: 'GlowMaxx',
      body: 'Notifications are working!',
    },
    trigger: null,
  });
}
