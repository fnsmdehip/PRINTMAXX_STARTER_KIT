import { renderHook, act } from '@testing-library/react-hooks';
import { useUserStore } from '../src/stores/userStore';
import { useStepStore } from '../src/stores/stepStore';
import { DEFAULT_STEP_GOAL, DEFAULT_BLOCKED_APPS } from '../src/utils/constants';

// Reset stores before each test
beforeEach(() => {
  useUserStore.getState().updateSettings({
    stepGoal: DEFAULT_STEP_GOAL,
    blockedApps: DEFAULT_BLOCKED_APPS,
    hasCompletedOnboarding: false,
    trialStartDate: null,
    notificationsEnabled: true,
    emergencyUnlockEnabled: true,
    dailyResetTime: '00:00',
  });

  useStepStore.setState({
    currentSteps: 0,
    stepGoal: DEFAULT_STEP_GOAL,
    isUnlocked: false,
    lastUpdated: 0,
    todayCompleted: false,
    isLoading: false,
    error: null,
    stepHistory: {},
  });
});

describe('useUserStore', () => {
  describe('settings', () => {
    it('has default step goal', () => {
      const { result } = renderHook(() => useUserStore());
      expect(result.current.settings.stepGoal).toBe(DEFAULT_STEP_GOAL);
    });

    it('updates step goal', () => {
      const { result } = renderHook(() => useUserStore());

      act(() => {
        result.current.setStepGoal(8000);
      });

      expect(result.current.settings.stepGoal).toBe(8000);
    });

    it('adds blocked app', () => {
      const { result } = renderHook(() => useUserStore());
      const initialCount = result.current.settings.blockedApps.length;

      act(() => {
        result.current.addBlockedApp({
          id: '100',
          name: 'TestApp',
          bundleId: 'com.test.app',
        });
      });

      expect(result.current.settings.blockedApps.length).toBe(initialCount + 1);
    });

    it('removes blocked app', () => {
      const { result } = renderHook(() => useUserStore());
      const appToRemove = result.current.settings.blockedApps[0];

      act(() => {
        result.current.removeBlockedApp(appToRemove.id);
      });

      expect(
        result.current.settings.blockedApps.find((a) => a.id === appToRemove.id)
      ).toBeUndefined();
    });
  });

  describe('onboarding', () => {
    it('starts with onboarding not completed', () => {
      const { result } = renderHook(() => useUserStore());
      expect(result.current.settings.hasCompletedOnboarding).toBe(false);
    });

    it('completes onboarding', () => {
      const { result } = renderHook(() => useUserStore());

      act(() => {
        result.current.completeOnboarding();
      });

      expect(result.current.settings.hasCompletedOnboarding).toBe(true);
    });
  });

  describe('trial', () => {
    it('starts trial', () => {
      const { result } = renderHook(() => useUserStore());

      act(() => {
        result.current.startTrial();
      });

      expect(result.current.subscription.isInTrial).toBe(true);
      expect(result.current.settings.trialStartDate).not.toBeNull();
    });
  });

  describe('streak', () => {
    it('starts with zero streak', () => {
      const { result } = renderHook(() => useUserStore());
      expect(result.current.streak.currentStreak).toBe(0);
    });

    it('updates streak when goal met', () => {
      const { result } = renderHook(() => useUserStore());

      act(() => {
        result.current.updateStreak(true);
      });

      expect(result.current.streak.currentStreak).toBe(1);
      expect(result.current.streak.totalDaysCompleted).toBe(1);
    });

    it('resets streak', () => {
      const { result } = renderHook(() => useUserStore());

      act(() => {
        result.current.updateStreak(true);
        result.current.resetStreak();
      });

      expect(result.current.streak.currentStreak).toBe(0);
    });
  });
});

describe('useStepStore', () => {
  describe('steps', () => {
    it('starts with zero steps', () => {
      const { result } = renderHook(() => useStepStore());
      expect(result.current.currentSteps).toBe(0);
    });

    it('updates current steps', () => {
      const { result } = renderHook(() => useStepStore());

      act(() => {
        result.current.setCurrentSteps(3000);
      });

      expect(result.current.currentSteps).toBe(3000);
    });

    it('unlocks when goal is met', () => {
      const { result } = renderHook(() => useStepStore());

      act(() => {
        result.current.setStepGoal(5000);
        result.current.setCurrentSteps(5000);
      });

      expect(result.current.isUnlocked).toBe(true);
    });

    it('stays locked when goal not met', () => {
      const { result } = renderHook(() => useStepStore());

      act(() => {
        result.current.setStepGoal(5000);
        result.current.setCurrentSteps(4999);
      });

      expect(result.current.isUnlocked).toBe(false);
    });
  });

  describe('completion', () => {
    it('marks today completed', () => {
      const { result } = renderHook(() => useStepStore());

      act(() => {
        result.current.markTodayCompleted();
      });

      expect(result.current.todayCompleted).toBe(true);
      expect(result.current.isUnlocked).toBe(true);
    });

    it('marks emergency unlock', () => {
      const { result } = renderHook(() => useStepStore());

      act(() => {
        result.current.setCurrentSteps(1000);
        result.current.markTodayCompleted(true);
      });

      expect(result.current.todayCompleted).toBe(true);
    });
  });

  describe('history', () => {
    it('calculates weekly average', () => {
      const { result } = renderHook(() => useStepStore());

      // Set some history
      act(() => {
        result.current.setCurrentSteps(5000);
      });

      // Should return a number (may be 0 if no history yet)
      expect(typeof result.current.getWeeklyAverage()).toBe('number');
    });

    it('calculates monthly total', () => {
      const { result } = renderHook(() => useStepStore());

      expect(typeof result.current.getMonthlyTotal()).toBe('number');
    });
  });

  describe('loading state', () => {
    it('tracks loading state', () => {
      const { result } = renderHook(() => useStepStore());

      act(() => {
        result.current.setLoading(true);
      });

      expect(result.current.isLoading).toBe(true);

      act(() => {
        result.current.setLoading(false);
      });

      expect(result.current.isLoading).toBe(false);
    });

    it('tracks error state', () => {
      const { result } = renderHook(() => useStepStore());

      act(() => {
        result.current.setError('Test error');
      });

      expect(result.current.error).toBe('Test error');

      act(() => {
        result.current.setError(null);
      });

      expect(result.current.error).toBeNull();
    });
  });
});
