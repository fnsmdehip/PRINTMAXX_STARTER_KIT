import { useEffect } from 'react';
import { Redirect } from 'expo-router';
import { useUserStore } from '../src/stores/userStore';

export default function Index() {
  const { hasCompletedOnboarding, canAccessApp, checkTrialStatus } = useUserStore();

  // Check trial status on mount
  useEffect(() => {
    checkTrialStatus();
  }, [checkTrialStatus]);

  // Route based on app state
  if (!hasCompletedOnboarding) {
    return <Redirect href="/onboarding" />;
  }

  if (!canAccessApp()) {
    return <Redirect href="/paywall" />;
  }

  return <Redirect href="/(tabs)" />;
}
