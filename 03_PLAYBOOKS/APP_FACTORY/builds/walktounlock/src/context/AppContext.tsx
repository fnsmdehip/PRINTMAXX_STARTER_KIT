import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import {
  getSettings,
  saveSettings,
  getUserStats,
  saveUserStats,
  getLockState,
  saveLockState,
  getTodaySteps,
  saveTodaySteps,
  updateStreak,
} from '../utils/storage';
import { initRevenueCat, checkPremiumStatus } from '../services/subscriptionService';
import type { Settings, UserStats, LockState } from '../constants/types';

interface AppContextType {
  isLoading: boolean;
  hasOnboarded: boolean;
  settings: Settings;
  stats: UserStats;
  lockState: LockState;
  isPremium: boolean;
  todaySteps: number;
  updateSettings: (updates: Partial<Settings>) => Promise<void>;
  updateStats: (updates: Partial<UserStats>) => Promise<void>;
  setLockState: (state: LockState) => Promise<void>;
  setPremium: (value: boolean) => Promise<void>;
  completeOnboarding: (stepGoal: number) => Promise<void>;
  completeUnlock: (steps: number) => Promise<void>;
  refreshData: () => Promise<void>;
}

const AppContext = createContext<AppContextType | null>(null);

const ONBOARDED_KEY = '@walktounlock_onboarded';

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [isLoading, setIsLoading] = useState(true);
  const [hasOnboarded, setHasOnboarded] = useState(false);
  const [settings, setSettings] = useState<Settings>({
    stepGoal: 500,
    lockEnabled: true,
    lockStartTime: '06:00',
    lockEndTime: '22:00',
    weekendStepGoal: 300,
    hapticFeedback: true,
    notifications: true,
    isPremium: false,
    whitelistedApps: [],
  });
  const [stats, setStats] = useState<UserStats>({
    totalSteps: 0,
    currentStreak: 0,
    longestStreak: 0,
    totalDaysActive: 0,
    lastActiveDate: '',
    achievements: [],
    weeklySteps: [],
    monthlySteps: [],
    personalRecords: {
      mostStepsInDay: 0,
      mostStepsInWeek: 0,
      longestStreak: 0,
      fastestUnlock: 0,
    },
  });
  const [lockState, setLockStateLocal] = useState<LockState>({
    isLocked: false,
    currentSteps: 0,
    requiredSteps: 500,
  });
  const [isPremium, setIsPremiumLocal] = useState(false);
  const [todaySteps, setTodaySteps] = useState(0);

  const loadData = useCallback(async () => {
    try {
      const AsyncStorage = require('@react-native-async-storage/async-storage').default;
      const [savedSettings, savedStats, savedLock, savedSteps, onboardedFlag] = await Promise.all([
        getSettings(),
        getUserStats(),
        getLockState(),
        getTodaySteps(),
        AsyncStorage.getItem(ONBOARDED_KEY),
      ]);

      setSettings(savedSettings);
      setStats(savedStats);
      setLockStateLocal(savedLock);
      setTodaySteps(savedSteps);
      setHasOnboarded(onboardedFlag === 'true');
      setIsPremiumLocal(savedSettings.isPremium);

      try {
        await initRevenueCat();
        const rcPremium = await checkPremiumStatus();
        if (rcPremium && !savedSettings.isPremium) {
          const updated = { ...savedSettings, isPremium: true };
          await saveSettings(updated);
          setSettings(updated);
          setIsPremiumLocal(true);
        }
      } catch (e) {
        // RevenueCat not available, use local premium state
      }
    } catch (error) {
      // Use defaults
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const updateSettings = useCallback(async (updates: Partial<Settings>) => {
    setSettings(prev => {
      const updated = { ...prev, ...updates };
      saveSettings(updated);
      return updated;
    });
  }, []);

  const updateStats = useCallback(async (updates: Partial<UserStats>) => {
    setStats(prev => {
      const updated = { ...prev, ...updates };
      saveUserStats(updated);
      return updated;
    });
  }, []);

  const setLockStatePersisted = useCallback(async (state: LockState) => {
    setLockStateLocal(state);
    await saveLockState(state);
  }, []);

  const setPremium = useCallback(async (value: boolean) => {
    setIsPremiumLocal(value);
    setSettings(prev => {
      const updated = { ...prev, isPremium: value };
      saveSettings(updated);
      return updated;
    });
  }, []);

  const completeOnboarding = useCallback(async (stepGoal: number) => {
    const AsyncStorage = require('@react-native-async-storage/async-storage').default;
    await AsyncStorage.setItem(ONBOARDED_KEY, 'true');
    setHasOnboarded(true);

    const updated = { ...settings, stepGoal };
    setSettings(updated);
    await saveSettings(updated);

    const newLock: LockState = {
      isLocked: true,
      currentSteps: 0,
      requiredSteps: stepGoal,
    };
    setLockStateLocal(newLock);
    await saveLockState(newLock);
  }, [settings]);

  const completeUnlock = useCallback(async (steps: number) => {
    await saveTodaySteps(steps);
    setTodaySteps(steps);

    const newStreak = await updateStreak();

    setStats(prev => {
      const updated = {
        ...prev,
        currentStreak: newStreak,
        longestStreak: Math.max(prev.longestStreak, newStreak),
      };
      return updated;
    });

    const newLock: LockState = {
      isLocked: false,
      currentSteps: steps,
      requiredSteps: settings.stepGoal,
      unlockTime: new Date().toISOString(),
    };
    setLockStateLocal(newLock);
    await saveLockState(newLock);
  }, [settings.stepGoal]);

  const refreshData = useCallback(async () => {
    const [savedSettings, savedStats, savedSteps] = await Promise.all([
      getSettings(),
      getUserStats(),
      getTodaySteps(),
    ]);
    setSettings(savedSettings);
    setStats(savedStats);
    setTodaySteps(savedSteps);
    setIsPremiumLocal(savedSettings.isPremium);
  }, []);

  return (
    <AppContext.Provider
      value={{
        isLoading,
        hasOnboarded,
        settings,
        stats,
        lockState,
        isPremium,
        todaySteps,
        updateSettings,
        updateStats,
        setLockState: setLockStatePersisted,
        setPremium,
        completeOnboarding,
        completeUnlock,
        refreshData,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}
