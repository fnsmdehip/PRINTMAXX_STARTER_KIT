import React, { useState, useEffect, useCallback } from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { NavigationContainer } from '@react-navigation/native';
import * as Linking from 'expo-linking';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { TabNavigator } from './src/navigation/TabNavigator';
import { SplashScreen } from './src/screens/SplashScreen';
import { OnboardingFlow, isOnboardingComplete } from './src/screens/OnboardingFlow';
import { StorageService } from './src/services/storage';
import { initPurchases } from './src/services/purchases';
import { initSounds } from './src/sounds/SoundEngine';
import type { AppScreen } from './src/types';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<AppScreen>('splash');
  const [isReady, setIsReady] = useState(false);

  const checkOnboardingState = useCallback(async () => {
    // Check the new v2 onboarding flag first, then fall back to legacy
    const v2Done = await isOnboardingComplete();
    if (v2Done) {
      setCurrentScreen('main');
    } else {
      const legacyOnboarding = await StorageService.getOnboardingState();
      if (legacyOnboarding.completed) {
        setCurrentScreen('main');
      } else {
        setCurrentScreen('onboarding');
      }
    }
    setIsReady(true);
  }, []);

  const handleSplashFinish = useCallback(() => {
    if (isReady) {
      return;
    }
    checkOnboardingState();
  }, [isReady, checkOnboardingState]);

  useEffect(() => {
    checkOnboardingState();
  }, [checkOnboardingState]);

  useEffect(() => {
    initPurchases().catch(() => {});
    initSounds().catch(() => {});
  }, []);

  // Deep link handler: scripture-streak://premium-activated activates pro entitlement
  useEffect(() => {
    const sub = Linking.addEventListener('url', ({ url }) => {
      if (url.includes('premium-activated') || url.includes('payment-success')) {
        AsyncStorage.setItem(
          '@scripture_streak_premium',
          JSON.stringify({ isPremium: true, purchasedAt: new Date().toISOString(), plan: 'deep-link' })
        ).catch(() => {});
      }
    });
    return () => sub.remove();
  }, []);

  const handleOnboardingComplete = useCallback(() => {
    setCurrentScreen('main');
  }, []);

  if (currentScreen === 'splash') {
    return (
      <>
        <StatusBar style="light" />
        <SplashScreen onFinish={handleSplashFinish} />
      </>
    );
  }

  if (currentScreen === 'onboarding') {
    return (
      <SafeAreaProvider>
        <StatusBar style="light" />
        <OnboardingFlow onComplete={handleOnboardingComplete} />
      </SafeAreaProvider>
    );
  }

  // Main app (covers both 'main' and legacy 'paywall' states)
  return (
    <SafeAreaProvider>
      <NavigationContainer>
        <StatusBar style="dark" />
        <TabNavigator />
      </NavigationContainer>
    </SafeAreaProvider>
  );
}
