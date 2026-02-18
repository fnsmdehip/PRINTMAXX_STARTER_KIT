import { useEffect } from 'react';
import { router } from 'expo-router';
import { useUserStore } from '../src/stores/userStore';

export default function Index() {
  const { settings, subscription } = useUserStore();

  useEffect(() => {
    // Check if user has completed onboarding
    if (!settings.hasCompletedOnboarding) {
      router.replace('/onboarding');
    } else if (!subscription.isSubscribed && !subscription.isInTrial) {
      // No active subscription or trial, show paywall
      router.replace('/paywall');
    } else {
      // Go to main app
      router.replace('/(tabs)/home');
    }
  }, [settings.hasCompletedOnboarding, subscription.isSubscribed, subscription.isInTrial]);

  return null;
}
