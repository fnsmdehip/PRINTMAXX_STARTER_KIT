import { useCallback } from 'react';
import { router } from 'expo-router';
import * as Haptics from 'expo-haptics';
import { useSubscriptionStore } from '../stores/subscriptionStore';

/**
 * Hook for gating premium content.
 * Returns isPremium status and a gate function that
 * either executes the callback (if premium) or opens paywall.
 */
export function usePremiumGate() {
  const canAccess = useSubscriptionStore((s) => s.canAccessPremiumContent);

  const isPremium = canAccess();

  const gate = useCallback(
    (onPremium: () => void) => {
      if (canAccess()) {
        onPremium();
      } else {
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
        router.push('/paywall');
      }
    },
    [canAccess]
  );

  return { isPremium, gate };
}
