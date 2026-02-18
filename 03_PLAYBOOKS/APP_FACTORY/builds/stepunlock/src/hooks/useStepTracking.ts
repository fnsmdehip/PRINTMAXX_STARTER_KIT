import { useEffect, useCallback, useRef } from 'react';
import { AppState, AppStateStatus } from 'react-native';
import { useStepStore } from '../stores/stepStore';
import { useUserStore } from '../stores/userStore';
import { getTodaySteps } from '../services/stepService';
import { updateBlockingState } from '../services/blockerService';
import { BACKGROUND_REFRESH_INTERVAL_MS } from '../utils/constants';

/**
 * Hook to manage step tracking and auto-refresh
 * Handles:
 * - Initial step fetch on mount
 * - Periodic background refresh
 * - App state changes (foreground/background)
 * - Auto-unlock when goal is reached
 */
export function useStepTracking() {
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const {
    currentSteps,
    stepGoal,
    todayCompleted,
    isUnlocked,
    setCurrentSteps,
    markTodayCompleted,
    setLoading,
    setError,
    refreshSteps,
  } = useStepStore();

  const { settings, updateStreak } = useUserStore();

  const fetchSteps = useCallback(async () => {
    setLoading(true);
    setError(null);

    const result = await getTodaySteps();

    if (result.error) {
      setError(result.error);
      setLoading(false);
      return;
    }

    setCurrentSteps(result.steps);

    // Check if goal was just met (not already completed)
    if (result.steps >= stepGoal && !todayCompleted) {
      markTodayCompleted();
      updateStreak(true);
      await updateBlockingState(true, settings.blockedApps);
    }

    setLoading(false);
  }, [
    stepGoal,
    todayCompleted,
    settings.blockedApps,
    setCurrentSteps,
    markTodayCompleted,
    updateStreak,
    setLoading,
    setError,
  ]);

  // Handle app state changes
  const handleAppStateChange = useCallback(
    (nextAppState: AppStateStatus) => {
      if (nextAppState === 'active') {
        // App came to foreground, refresh steps
        refreshSteps();
        fetchSteps();
      }
    },
    [fetchSteps, refreshSteps]
  );

  // Initial fetch and setup interval
  useEffect(() => {
    fetchSteps();

    // Set up periodic refresh
    intervalRef.current = setInterval(fetchSteps, BACKGROUND_REFRESH_INTERVAL_MS);

    // Listen for app state changes
    const subscription = AppState.addEventListener('change', handleAppStateChange);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      subscription.remove();
    };
  }, [fetchSteps, handleAppStateChange]);

  // Update blocking state when unlock status changes
  useEffect(() => {
    updateBlockingState(isUnlocked, settings.blockedApps);
  }, [isUnlocked, settings.blockedApps]);

  return {
    currentSteps,
    stepGoal,
    isUnlocked,
    todayCompleted,
    refreshSteps: fetchSteps,
  };
}
