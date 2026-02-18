import { useEffect } from 'react';
import { Redirect } from 'expo-router';
import { useUserStore } from '../src/stores/userStore';

export default function Index() {
  const { settings } = useUserStore();

  // Redirect based on onboarding status
  if (!settings.hasCompletedOnboarding) {
    return <Redirect href="/onboarding" />;
  }

  return <Redirect href="/(tabs)" />;
}
