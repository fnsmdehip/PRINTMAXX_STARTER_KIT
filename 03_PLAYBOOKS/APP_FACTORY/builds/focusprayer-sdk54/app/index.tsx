/**
 * Index Route
 * Redirects based on onboarding status
 */

import { Redirect } from 'expo-router';
import { useUserStore } from '@/stores/userStore';

export default function Index() {
  const { settings } = useUserStore();

  // If onboarding not complete, show onboarding
  if (!settings.onboardingComplete) {
    return <Redirect href="/onboarding" />;
  }

  // Otherwise, show main tabs
  return <Redirect href="/(tabs)" />;
}
