/**
 * useNotifications.ts
 * React Native hook for notification management
 * Handles permissions, scheduling, and engagement tracking
 */

import { useEffect, useState, useCallback, useRef } from 'react';
import { AppState, AppStateStatus } from 'react-native';
import * as Notifications from 'expo-notifications';
import notificationService, {
  NotificationPreferences,
  ScheduledNotification,
} from './NotificationService';

interface UseNotificationsReturn {
  // Permission state
  hasPermission: boolean;
  permissionRequested: boolean;
  requestPermissions: () => Promise<boolean>;

  // Preferences
  preferences: NotificationPreferences;
  updatePreferences: (updates: Partial<NotificationPreferences>) => Promise<void>;

  // Scheduling
  scheduleNotification: (notification: Omit<ScheduledNotification, 'id'>) => Promise<string>;
  scheduleRepeating: (params: {
    title: string;
    body: string;
    hour: number;
    minute: number;
    weekdays?: number[];
    type: 'reminders' | 'streaks' | 'content' | 'achievements' | 'community';
  }) => Promise<string[]>;
  cancelNotification: (id: string) => Promise<void>;
  cancelAll: () => Promise<void>;
  scheduledNotifications: Notifications.NotificationRequest[];

  // Immediate
  sendNow: (title: string, body: string, data?: Record<string, unknown>) => Promise<string>;

  // Badge
  badgeCount: number;
  setBadgeCount: (count: number) => Promise<void>;
  clearBadge: () => Promise<void>;

  // Engagement
  engagementStats: {
    totalReceived: number;
    totalOpened: number;
    openRate: number;
  } | null;

  // Last notification
  lastNotification: Notifications.Notification | null;
  lastResponse: Notifications.NotificationResponse | null;

  // State
  isLoading: boolean;
  error: Error | null;
}

interface UseNotificationsOptions {
  onNotificationReceived?: (notification: Notifications.Notification) => void;
  onNotificationOpened?: (response: Notifications.NotificationResponse) => void;
  autoRequestPermissions?: boolean;
}

export function useNotifications(
  options: UseNotificationsOptions = {}
): UseNotificationsReturn {
  const {
    onNotificationReceived,
    onNotificationOpened,
    autoRequestPermissions = false,
  } = options;

  // State
  const [hasPermission, setHasPermission] = useState(false);
  const [permissionRequested, setPermissionRequested] = useState(false);
  const [preferences, setPreferences] = useState<NotificationPreferences>(
    notificationService.getPreferences()
  );
  const [scheduledNotifications, setScheduledNotifications] = useState<
    Notifications.NotificationRequest[]
  >([]);
  const [badgeCount, setBadgeCountState] = useState(0);
  const [engagementStats, setEngagementStats] = useState<{
    totalReceived: number;
    totalOpened: number;
    openRate: number;
  } | null>(null);
  const [lastNotification, setLastNotification] =
    useState<Notifications.Notification | null>(null);
  const [lastResponse, setLastResponse] =
    useState<Notifications.NotificationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  // Refs for callbacks
  const onNotificationReceivedRef = useRef(onNotificationReceived);
  const onNotificationOpenedRef = useRef(onNotificationOpened);

  useEffect(() => {
    onNotificationReceivedRef.current = onNotificationReceived;
    onNotificationOpenedRef.current = onNotificationOpened;
  }, [onNotificationReceived, onNotificationOpened]);

  // Initialize
  useEffect(() => {
    async function init() {
      try {
        setIsLoading(true);

        // Check existing permission
        const permission = await notificationService.hasPermission();
        setHasPermission(permission);
        setPermissionRequested(permission);

        // Load scheduled notifications
        const scheduled = await notificationService.getScheduledNotifications();
        setScheduledNotifications(scheduled);

        // Load badge count
        const badge = await notificationService.getBadgeCount();
        setBadgeCountState(badge);

        // Load engagement stats
        const stats = await notificationService.getEngagementStats();
        setEngagementStats({
          totalReceived: stats.totalReceived,
          totalOpened: stats.totalOpened,
          openRate: stats.openRate,
        });

        // Auto request permissions if enabled
        if (autoRequestPermissions && !permission) {
          const granted = await notificationService.requestPermissions();
          setHasPermission(granted);
          setPermissionRequested(true);
        }
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to initialize notifications'));
      } finally {
        setIsLoading(false);
      }
    }

    init();
  }, [autoRequestPermissions]);

  // Set up notification listeners
  useEffect(() => {
    const receivedSubscription = notificationService.addNotificationReceivedListener(
      (notification) => {
        setLastNotification(notification);
        onNotificationReceivedRef.current?.(notification);
      }
    );

    const responseSubscription = notificationService.addNotificationResponseListener(
      (response) => {
        setLastResponse(response);
        onNotificationOpenedRef.current?.(response);
      }
    );

    return () => {
      receivedSubscription.remove();
      responseSubscription.remove();
    };
  }, []);

  // Refresh scheduled notifications when app comes to foreground
  useEffect(() => {
    const handleAppStateChange = async (nextState: AppStateStatus) => {
      if (nextState === 'active') {
        const scheduled = await notificationService.getScheduledNotifications();
        setScheduledNotifications(scheduled);
        const badge = await notificationService.getBadgeCount();
        setBadgeCountState(badge);
      }
    };

    const subscription = AppState.addEventListener('change', handleAppStateChange);
    return () => subscription.remove();
  }, []);

  // Request permissions
  const requestPermissions = useCallback(async (): Promise<boolean> => {
    try {
      setIsLoading(true);
      const granted = await notificationService.requestPermissions();
      setHasPermission(granted);
      setPermissionRequested(true);
      return granted;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to request permissions'));
      return false;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Update preferences
  const updatePreferences = useCallback(
    async (updates: Partial<NotificationPreferences>): Promise<void> => {
      try {
        await notificationService.updatePreferences(updates);
        setPreferences(notificationService.getPreferences());

        // Refresh scheduled if preferences affect scheduling
        const scheduled = await notificationService.getScheduledNotifications();
        setScheduledNotifications(scheduled);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to update preferences'));
        throw err;
      }
    },
    []
  );

  // Schedule notification
  const scheduleNotification = useCallback(
    async (notification: Omit<ScheduledNotification, 'id'>): Promise<string> => {
      try {
        const id = await notificationService.scheduleNotification(notification);
        const scheduled = await notificationService.getScheduledNotifications();
        setScheduledNotifications(scheduled);
        return id;
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to schedule notification'));
        throw err;
      }
    },
    []
  );

  // Schedule repeating
  const scheduleRepeating = useCallback(
    async (params: {
      title: string;
      body: string;
      hour: number;
      minute: number;
      weekdays?: number[];
      type: 'reminders' | 'streaks' | 'content' | 'achievements' | 'community';
    }): Promise<string[]> => {
      try {
        const ids = await notificationService.scheduleRepeatingNotification(params);
        const scheduled = await notificationService.getScheduledNotifications();
        setScheduledNotifications(scheduled);
        return ids;
      } catch (err) {
        setError(
          err instanceof Error ? err : new Error('Failed to schedule repeating notification')
        );
        throw err;
      }
    },
    []
  );

  // Cancel notification
  const cancelNotification = useCallback(async (id: string): Promise<void> => {
    try {
      await notificationService.cancelNotification(id);
      const scheduled = await notificationService.getScheduledNotifications();
      setScheduledNotifications(scheduled);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to cancel notification'));
      throw err;
    }
  }, []);

  // Cancel all
  const cancelAll = useCallback(async (): Promise<void> => {
    try {
      await notificationService.cancelAllNotifications();
      setScheduledNotifications([]);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to cancel notifications'));
      throw err;
    }
  }, []);

  // Send immediate notification
  const sendNow = useCallback(
    async (
      title: string,
      body: string,
      data?: Record<string, unknown>
    ): Promise<string> => {
      try {
        return await notificationService.sendImmediateNotification({ title, body, data });
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to send notification'));
        throw err;
      }
    },
    []
  );

  // Set badge count
  const setBadgeCount = useCallback(async (count: number): Promise<void> => {
    try {
      await notificationService.setBadgeCount(count);
      setBadgeCountState(count);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to set badge count'));
      throw err;
    }
  }, []);

  // Clear badge
  const clearBadge = useCallback(async (): Promise<void> => {
    await setBadgeCount(0);
  }, [setBadgeCount]);

  return {
    // Permission
    hasPermission,
    permissionRequested,
    requestPermissions,

    // Preferences
    preferences,
    updatePreferences,

    // Scheduling
    scheduleNotification,
    scheduleRepeating,
    cancelNotification,
    cancelAll,
    scheduledNotifications,

    // Immediate
    sendNow,

    // Badge
    badgeCount,
    setBadgeCount,
    clearBadge,

    // Engagement
    engagementStats,

    // Last notification
    lastNotification,
    lastResponse,

    // State
    isLoading,
    error,
  };
}

/**
 * Hook for handling deep links from notifications
 */
export function useNotificationNavigation(
  navigator: {
    navigate: (screen: string, params?: Record<string, unknown>) => void;
  }
): void {
  useEffect(() => {
    const subscription = notificationService.addNotificationResponseListener((response) => {
      const data = response.notification.request.content.data;

      if (data?.screen && typeof data.screen === 'string') {
        navigator.navigate(data.screen, data.params as Record<string, unknown>);
      }
    });

    return () => subscription.remove();
  }, [navigator]);
}

/**
 * Hook for scheduling streak notifications
 */
export function useStreakNotifications(params: {
  currentStreak: number;
  lastActivityDate: Date | null;
  enabled?: boolean;
}) {
  const { currentStreak, lastActivityDate, enabled = true } = params;
  const { scheduleNotification, cancelAll, preferences } = useNotifications();

  useEffect(() => {
    if (!enabled || !preferences.streakAlerts) return;

    async function scheduleStreakReminder() {
      if (!lastActivityDate) return;

      // Check if user completed today's activity
      const today = new Date();
      const lastActivity = new Date(lastActivityDate);
      const isCompletedToday =
        lastActivity.toDateString() === today.toDateString();

      if (isCompletedToday) {
        // No reminder needed today
        return;
      }

      // Schedule "streak at risk" notification for evening
      const reminderTime = new Date();
      reminderTime.setHours(20, 0, 0, 0); // 8 PM

      if (reminderTime > today) {
        await scheduleNotification({
          title: `${currentStreak} day streak at risk`,
          body: "You haven't checked in today. Don't break your streak!",
          scheduledTime: reminderTime,
          type: 'streaks',
          data: { type: 'streak_reminder', streak: currentStreak },
        });
      }
    }

    // Clear previous reminders and reschedule
    cancelAll().then(scheduleStreakReminder);
  }, [
    currentStreak,
    lastActivityDate,
    enabled,
    preferences.streakAlerts,
    scheduleNotification,
    cancelAll,
  ]);
}

export default useNotifications;
