/**
 * Push Notification System
 *
 * Complete notification infrastructure for React Native apps.
 *
 * Usage:
 *
 * import {
 *   notificationService,
 *   notificationScheduler,
 *   useNotifications
 * } from '@/shared/notifications';
 *
 * // In component
 * const { requestPermissions, scheduleNotification } = useNotifications();
 *
 * // Schedule a notification
 * await scheduleNotification({
 *   title: 'Time to pray',
 *   body: 'Your daily devotion is ready.',
 *   scheduledTime: new Date(Date.now() + 60000),
 *   type: 'reminders',
 * });
 *
 * // Use smart scheduling
 * notificationScheduler.setAppCategory('faith');
 * await notificationScheduler.scheduleSmartNotification({
 *   type: 'morning_reminder',
 *   title: 'Good morning',
 *   body: 'Start your day with reflection.',
 * });
 */

// Core service
export {
  default as notificationService,
  notificationService as NotificationServiceInstance,
} from './NotificationService';

export type {
  NotificationPreferences,
  ScheduledNotification,
  NotificationEngagement,
} from './NotificationService';

// React hook
export {
  useNotifications,
  useNotificationNavigation,
  useStreakNotifications,
} from './useNotifications';

// Smart scheduler
export {
  default as notificationScheduler,
  notificationScheduler as NotificationSchedulerInstance,
} from './notification_scheduler';
