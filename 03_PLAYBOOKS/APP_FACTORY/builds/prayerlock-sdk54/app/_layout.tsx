import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useEffect } from 'react';
import { useUserStore } from '../src/stores/userStore';
import { useDevotionStore } from '../src/stores/devotionStore';
import { notificationService } from '../src/services/notificationService';

export default function RootLayout() {
  const hasCompletedOnboarding = useUserStore((state) => state.hasCompletedOnboarding);
  const hydrateUser = useUserStore((state) => state.hydrate);
  const hydrateDevotion = useDevotionStore((state) => state.hydrate);
  const settings = useUserStore((state) => state.settings);

  useEffect(() => {
    hydrateUser();
    hydrateDevotion();
  }, []);

  // Schedule daily notification based on user's reset time
  useEffect(() => {
    if (hasCompletedOnboarding && settings.notificationsEnabled) {
      const [hourStr, minuteStr] = settings.dailyResetTime.split(':');
      const hour = parseInt(hourStr, 10);
      const minute = parseInt(minuteStr, 10);
      notificationService.scheduleDailyReminder(hour, minute);
      notificationService.scheduleStreakReminder();
    }
  }, [hasCompletedOnboarding, settings.notificationsEnabled, settings.dailyResetTime]);

  return (
    <>
      <StatusBar style="light" />
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: '#1a1a2e' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: '600' },
          contentStyle: { backgroundColor: '#1a1a2e' },
        }}
      >
        <Stack.Screen name="index" options={{ headerShown: false }} />
        <Stack.Screen name="onboarding" options={{ headerShown: false }} />
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="timer" options={{ title: 'Prayer Time', presentation: 'fullScreenModal' }} />
        <Stack.Screen name="scripture" options={{ title: 'Daily Scripture', presentation: 'fullScreenModal' }} />
        <Stack.Screen name="paywall" options={{ headerShown: false, presentation: 'modal' }} />
        <Stack.Screen name="emergency-unlock" options={{ title: 'Emergency Unlock', presentation: 'modal' }} />
      </Stack>
    </>
  );
}
