import { useEffect, useState } from 'react';
import { Stack, useRouter, useSegments } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { View, ActivityIndicator } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import * as SecureStore from 'expo-secure-store';
import { useStore } from '../src/lib/store';
import { initializeNotifications } from '../src/lib/notifications';

export default function RootLayout() {
  console.log('🔍 DEBUG: RootLayout component loaded');
  console.log('🔍 DEBUG: RootLayout file path:', __filename);

  const router = useRouter();
  const segments = useSegments();
  const { setIsLoading, hasCompletedOnboarding, setHasCompletedOnboarding } = useStore();
  const [isReady, setIsReady] = useState(false);

  console.log('🔍 DEBUG: RootLayout hooks initialized');
  console.log('🔍 DEBUG: Current segments:', segments);

  // Initialize app on mount
  useEffect(() => {
    async function initialize() {
      try {
        // Check onboarding status
        const completed = await SecureStore.getItemAsync('onboarding_completed');
        setHasCompletedOnboarding(completed === 'true');
        
        // Initialize notifications
        await initializeNotifications();
      } catch (error) {
        console.log('Initialization error:', error);
        setHasCompletedOnboarding(false);
      } finally {
        setIsLoading(false);
        setIsReady(true);
      }
    }
    
    initialize();
  }, []);

  // Handle routing based on onboarding state
  useEffect(() => {
    if (!isReady) return;

    const inOnboarding = segments[0] === '(onboarding)';
    const inPaywall = segments[0] === 'paywall';

    // Not completed onboarding -> show onboarding
    if (!hasCompletedOnboarding && !inOnboarding) {
      router.replace('/(onboarding)');
      return;
    }

    // Completed onboarding, not in main tabs -> show paywall (they can skip to main)
    // This gives users a chance to upgrade but doesn't force it
    if (hasCompletedOnboarding && !inPaywall && segments[0] !== '(tabs)' && !inOnboarding) {
      router.replace('/paywall');
      return;
    }
  }, [isReady, hasCompletedOnboarding, segments]);

  if (!isReady) {
    return (
      <GestureHandlerRootView style={{ flex: 1 }}>
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#1a1a2e' }}>
          <ActivityIndicator size="large" color="#e94560" />
        </View>
      </GestureHandlerRootView>
    );
  }

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <StatusBar style="light" />
        <Stack
          screenOptions={{
            headerShown: false,
            contentStyle: { backgroundColor: '#1a1a2e' },
            animation: 'fade',
          }}
        >
          <Stack.Screen name="(onboarding)" options={{ gestureEnabled: false }} />
          <Stack.Screen name="paywall" options={{ presentation: 'modal' }} />
          <Stack.Screen name="(tabs)" options={{ gestureEnabled: false }} />
          <Stack.Screen name="(auth)" />
          <Stack.Screen name="faith-letter-wall" options={{ presentation: 'modal' }} />
        </Stack>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
