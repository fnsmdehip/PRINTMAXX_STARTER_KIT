/**
 * Root Layout
 * Main entry point with app initialization
 */

import { useEffect, useState } from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import * as SplashScreen from 'expo-splash-screen';

import { useUserStore } from '@/stores/userStore';
import { useDevotionStore } from '@/stores/devotionStore';
import { initializeSubscriptions } from '@/services/subscriptionService';
import { COLORS } from '@/utils/constants';

// Prevent splash screen from auto-hiding
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [isReady, setIsReady] = useState(false);
  const { loadSettings, loadSubscription } = useUserStore();
  const { loadTodayStatus, loadStreak } = useDevotionStore();

  useEffect(() => {
    initializeApp();
  }, []);

  async function initializeApp() {
    try {
      // Initialize RevenueCat
      await initializeSubscriptions();

      // Load all stored data
      await Promise.all([
        loadSettings(),
        loadSubscription(),
        loadTodayStatus(),
        loadStreak(),
      ]);
    } catch (error) {
      console.error('Failed to initialize app:', error);
    } finally {
      setIsReady(true);
      await SplashScreen.hideAsync();
    }
  }

  if (!isReady) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <SafeAreaProvider>
      <StatusBar style="dark" />
      <Stack
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: COLORS.background },
        }}
      >
        <Stack.Screen name="index" />
        <Stack.Screen name="onboarding" />
        <Stack.Screen name="(tabs)" />
        <Stack.Screen
          name="timer"
          options={{
            gestureEnabled: false,
          }}
        />
        <Stack.Screen
          name="scripture"
          options={{
            gestureEnabled: false,
          }}
        />
        <Stack.Screen
          name="paywall"
          options={{
            presentation: 'modal',
          }}
        />
        <Stack.Screen
          name="emergency-unlock"
          options={{
            presentation: 'modal',
          }}
        />
        <Stack.Screen name="privacy-policy" />
        <Stack.Screen name="terms" />
      </Stack>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
  },
});
