import { useEffect, useState } from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { useUserStore } from '../src/stores/userStore';
import { initializeSubscriptions } from '../src/services/subscriptionService';
import { requestNotificationPermissions } from '../src/services/notificationService';
import { COLORS } from '../src/utils/constants';

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
    <GestureHandlerRootView style={styles.container}>
      <SafeAreaProvider>
        <StatusBar style="dark" backgroundColor={COLORS.background} />
        <Stack
          screenOptions={{
            headerShown: false,
          }}
        >
          <Stack.Screen name="index" options={{ headerShown: false }} />
          <Stack.Screen name="onboarding" options={{ headerShown: false }} />
          <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
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
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
  },
});
