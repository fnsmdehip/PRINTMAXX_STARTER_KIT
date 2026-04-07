import React, { useState, useEffect, useCallback } from 'react';
import { View, StyleSheet } from 'react-native';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import * as SplashScreen from 'expo-splash-screen';
import * as Linking from 'expo-linking';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { colors } from '../src/constants/theme';
import { getOnboardingState } from '../src/services/storage';
import { initPurchases, checkEntitlements } from '../src/services/purchases';
import { initSounds } from '../src/sounds/SoundEngine';
import AnimatedSplash from '../src/components/AnimatedSplash';
import OnboardingScreen from '../src/screens/OnboardingFlow';

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [isReady, setIsReady] = useState(false);
  const [showSplash, setShowSplash] = useState(true);
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [hasChecked, setHasChecked] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        await initPurchases();
        await checkEntitlements();
        const state = await getOnboardingState();
        setShowOnboarding(!state.completed);
      } catch {
        setShowOnboarding(true);
      } finally {
        setHasChecked(true);
        await SplashScreen.hideAsync();
      }
    })();
    initSounds().catch(() => {});
  }, []);

  // Deep link handler: pocket-alexandria://premium-activated activates pro entitlement
  useEffect(() => {
    const sub = Linking.addEventListener('url', ({ url }) => {
      if (url.includes('premium-activated') || url.includes('payment-success')) {
        AsyncStorage.setItem(
          '@pocket_alexandria_premium',
          JSON.stringify({ isPremium: true, purchasedAt: new Date().toISOString(), plan: 'deep-link' })
        ).catch(() => {});
      }
    });
    return () => sub.remove();
  }, []);

  const handleSplashFinish = useCallback(() => {
    setShowSplash(false);
    setIsReady(true);
  }, []);

  const handleOnboardingComplete = useCallback(() => {
    setShowOnboarding(false);
  }, []);

  if (!hasChecked) {
    return (
      <View style={styles.loading}>
        <StatusBar style="light" />
      </View>
    );
  }

  if (showSplash) {
    return (
      <View style={styles.loading}>
        <StatusBar style="light" />
        <AnimatedSplash onFinish={handleSplashFinish} />
      </View>
    );
  }

  if (showOnboarding) {
    return (
      <View style={styles.loading}>
        <StatusBar style="light" />
        <OnboardingScreen onComplete={handleOnboardingComplete} />
      </View>
    );
  }

  return (
    <>
      <StatusBar style="light" />
      <Stack
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: colors.background },
          animation: 'slide_from_right',
        }}
      >
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen
          name="reader/[bookId]"
          options={{
            headerShown: false,
            presentation: 'fullScreenModal',
            animation: 'slide_from_bottom',
          }}
        />
      </Stack>
    </>
  );
}

const styles = StyleSheet.create({
  loading: {
    flex: 1,
    backgroundColor: colors.background,
  },
});
