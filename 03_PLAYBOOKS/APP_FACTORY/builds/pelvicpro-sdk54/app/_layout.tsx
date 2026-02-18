import { useEffect, useState } from 'react';
import { Stack, useRouter, useSegments } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import * as SplashScreen from 'expo-splash-screen';
import { colors } from '@/constants/theme';
import { useUserStore } from '@/store/userStore';

// Prevent splash screen from auto-hiding
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const router = useRouter();
  const segments = useSegments();
  const [isReady, setIsReady] = useState(false);

  const { hasCompletedOnboarding, isSubscribed, isTrialActive } = useUserStore();

  useEffect(() => {
    // Initial app setup
    const prepare = async () => {
      try {
        // Add any async initialization here (fonts, etc.)
        await new Promise((resolve) => setTimeout(resolve, 500));
      } catch (e) {
        console.warn(e);
      } finally {
        setIsReady(true);
      }
    };

    prepare();
  }, []);

  useEffect(() => {
    if (!isReady) return;

    // Hide splash screen once ready
    SplashScreen.hideAsync();

    // Get current segment
    const inOnboarding = segments[0] === '(onboarding)';
    const inTabs = segments[0] === '(tabs)';
    const inAuth = segments[0] === '(auth)';

    // Route based on onboarding status
    if (!hasCompletedOnboarding) {
      // User hasn't completed onboarding, redirect to onboarding
      if (!inOnboarding) {
        router.replace('/(onboarding)/welcome');
      }
    } else {
      // User has completed onboarding
      if (inOnboarding || inAuth) {
        // Redirect away from onboarding to main app
        router.replace('/(tabs)');
      }
    }
  }, [isReady, hasCompletedOnboarding, segments]);

  if (!isReady) {
    return null;
  }

  return (
    <>
      <StatusBar style="dark" />
      <Stack
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: colors.background },
          animation: 'slide_from_right',
        }}
      >
        {/* Onboarding flow */}
        <Stack.Screen
          name="(onboarding)"
          options={{
            headerShown: false,
            gestureEnabled: false,
          }}
        />

        {/* Main app tabs */}
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />

        {/* Legacy onboarding (kept for compatibility) */}
        <Stack.Screen
          name="(auth)/onboarding"
          options={{ headerShown: false, gestureEnabled: false }}
        />

        {/* Paywall modal */}
        <Stack.Screen
          name="paywall"
          options={{
            presentation: 'modal',
            gestureEnabled: false,
          }}
        />

        {/* Active workout screen */}
        <Stack.Screen
          name="workout/active"
          options={{
            headerShown: false,
            gestureEnabled: false,
          }}
        />

        {/* Exercise detail */}
        <Stack.Screen
          name="exercise/[id]"
          options={{
            headerShown: true,
            headerTitle: 'Exercise',
            headerBackTitle: 'Back',
            headerStyle: { backgroundColor: colors.background },
            headerTintColor: colors.text,
          }}
        />

        {/* Legal pages */}
        <Stack.Screen
          name="privacy"
          options={{
            headerShown: true,
            headerTitle: 'Privacy Policy',
            headerBackTitle: 'Back',
            headerStyle: { backgroundColor: colors.background },
            headerTintColor: colors.text,
          }}
        />
        <Stack.Screen
          name="terms"
          options={{
            headerShown: true,
            headerTitle: 'Terms of Service',
            headerBackTitle: 'Back',
            headerStyle: { backgroundColor: colors.background },
            headerTintColor: colors.text,
          }}
        />
      </Stack>
    </>
  );
}
