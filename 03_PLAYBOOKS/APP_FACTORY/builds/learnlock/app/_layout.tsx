import React, { useEffect } from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { useStreakStore } from '../src/stores/streakStore';
import { useTimerStore } from '../src/stores/timerStore';
import { useUserStore } from '../src/stores/userStore';
import { COLORS } from '../src/utils/constants';

export default function RootLayout() {
  const { checkAndUpdateStreak } = useStreakStore();
  const { resetDaily } = useTimerStore();
  const { hasCompletedOnboarding, canAccessApp } = useUserStore();

  // Check streak status and reset daily data on app launch
  useEffect(() => {
    checkAndUpdateStreak();
    resetDaily();
  }, [checkAndUpdateStreak, resetDaily]);

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <StatusBar style="dark" backgroundColor={COLORS.background} />
      <Stack
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: COLORS.background },
        }}
      >
        <Stack.Screen name="index" options={{ headerShown: false }} />
        <Stack.Screen name="onboarding" options={{ headerShown: false }} />
        <Stack.Screen name="paywall" options={{ headerShown: false, presentation: 'modal' }} />
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="privacy" options={{ headerShown: false }} />
        <Stack.Screen name="terms" options={{ headerShown: false }} />
      </Stack>
    </GestureHandlerRootView>
  );
}
