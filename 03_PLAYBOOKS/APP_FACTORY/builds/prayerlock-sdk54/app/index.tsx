import { Redirect } from 'expo-router';
import { useUserStore } from '../src/stores/userStore';
import { useDevotionStore } from '../src/stores/devotionStore';

export default function Index() {
  const hasCompletedOnboarding = useUserStore((state) => state.hasCompletedOnboarding);
  const isSubscribed = useUserStore((state) => state.isSubscribed);
  const isTrialActive = useUserStore((state) => state.isTrialActive);
  const trialEndsAt = useUserStore((state) => state.trialEndsAt);

  // Check if trial has expired
  const trialExpired = trialEndsAt ? Date.now() > trialEndsAt : false;
  const hasAccess = isSubscribed || (isTrialActive && !trialExpired);

  if (!hasCompletedOnboarding) {
    return <Redirect href="/onboarding" />;
  }

  if (!hasAccess) {
    return <Redirect href="/paywall" />;
  }

  return <Redirect href="/(tabs)" />;
}
