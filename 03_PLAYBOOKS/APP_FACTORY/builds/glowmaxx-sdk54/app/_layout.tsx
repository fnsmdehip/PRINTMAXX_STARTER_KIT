import { useEffect, useState } from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import * as SplashScreen from 'expo-splash-screen';

import { useUserStore } from '../src/stores/userStore';
import { initializeSubscriptions } from '../src/services/subscriptionService';
import { requestNotificationPermissions } from '../src/services/notificationService';
import { COLORS } from '../src/utils/constants';

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [isLoading, setIsLoading] = useState(true);
  const { checkTrialStatus } = useUserStore();

  useEffect(() => {
    async function initialize() {
      try {
        // Initialize RevenueCat
        await initializeSubscriptions();

        // Check trial status
        checkTrialStatus();

        // Request notification permissions
        await requestNotificationPermissions();
      } catch (error) {
        console.error('Initialization error:', error);
      } finally {
        await SplashScreen.hideAsync();
        setIsLoading(false);
      }
    }

    initialize();
  }, [checkTrialStatus]);

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <>
      <StatusBar style="dark" backgroundColor={COLORS.background} />
      <Stack
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: COLORS.background },
          animation: 'slide_from_right',
        }}
      >
        <Stack.Screen name="index" />
        <Stack.Screen name="onboarding" options={{ gestureEnabled: false }} />
        <Stack.Screen name="(tabs)" options={{ gestureEnabled: false }} />
        <Stack.Screen
          name="paywall"
          options={{
            presentation: 'modal',
            headerShown: false,
          }}
        />
        <Stack.Screen
          name="routine-player"
          options={{
            presentation: 'modal',
            headerShown: true,
            headerTitle: 'Routine',
          }}
        />
        <Stack.Screen
          name="privacy-policy"
          options={{
            presentation: 'modal',
            headerShown: true,
            headerTitle: 'Privacy Policy',
          }}
        />
        <Stack.Screen
          name="terms"
          options={{
            presentation: 'modal',
            headerShown: true,
            headerTitle: 'Terms of Service',
          }}
        />
      </Stack>
    </>
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
