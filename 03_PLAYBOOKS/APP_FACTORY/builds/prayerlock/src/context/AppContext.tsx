import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import {
  getSettings,
  saveSettings,
  getStreakData,
  updateStreak,
  getLockState,
  setLockState,
  getPremiumStatus,
  incrementEmergencyUnlock,
  getOnboardingComplete,
  setOnboardingComplete,
  getSalahDailyStatus,
  markSalahComplete as markSalahCompleteStorage,
  UserSettings,
  StreakData,
  SalahDailyStatus,
} from '../utils/storage';
import { DEFAULT_SETTINGS, FaithType } from '../constants';
import { initRevenueCat, checkPremiumStatus as rcCheckPremium } from '../services/subscriptionService';

interface AppContextType {
  settings: UserSettings;
  streakData: StreakData;
  salahStatus: SalahDailyStatus;
  isLocked: boolean;
  isPremium: boolean;
  isLoading: boolean;
  hasOnboarded: boolean;
  updateSettings: (newSettings: Partial<UserSettings>) => Promise<void>;
  completePrayer: (minutes: number) => Promise<void>;
  completeSalah: (salahName: 'fajr' | 'dhuhr' | 'asr' | 'maghrib' | 'isha', minutes: number) => Promise<void>;
  triggerLock: () => Promise<void>;
  unlock: () => Promise<void>;
  emergencyUnlock: () => Promise<number>;
  refreshData: () => Promise<void>;
  completeOnboarding: (faith: FaithType) => Promise<void>;
  setPremium: (premium: boolean) => Promise<void>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [settings, setSettings] = useState<UserSettings>(DEFAULT_SETTINGS);
  const [streakData, setStreakData] = useState<StreakData>({
    currentStreak: 0,
    longestStreak: 0,
    lastPrayerDate: null,
    totalPrayerMinutes: 0,
    emergencyUnlockCount: 0,
  });
  const [salahStatus, setSalahStatus] = useState<SalahDailyStatus>({
    date: new Date().toISOString().split('T')[0],
    fajr: false,
    dhuhr: false,
    asr: false,
    maghrib: false,
    isha: false,
  });
  const [isLocked, setIsLocked] = useState(false);
  const [isPremium, setIsPremium] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [hasOnboarded, setHasOnboarded] = useState(false);

  const refreshData = async () => {
    try {
      const [loadedSettings, loadedStreak, locked, premium, onboarded, salah] = await Promise.all([
        getSettings(),
        getStreakData(),
        getLockState(),
        getPremiumStatus(),
        getOnboardingComplete(),
        getSalahDailyStatus(),
      ]);
      setSettings(loadedSettings);
      setStreakData(loadedStreak);
      setIsLocked(locked);
      setIsPremium(premium);
      setHasOnboarded(onboarded);
      setSalahStatus(salah);
    } catch (error) {
      // Data refresh failed, keep current state
    }
  };

  useEffect(() => {
    const loadData = async () => {
      await initRevenueCat();
      const rcPremium = await rcCheckPremium();
      if (rcPremium) {
        setIsPremium(true);
      }
      await refreshData();
      setIsLoading(false);
    };
    loadData();
  }, []);

  const updateSettings = async (newSettings: Partial<UserSettings>) => {
    const updated = { ...settings, ...newSettings };
    setSettings(updated);
    await saveSettings(updated);
  };

  const completePrayer = async (minutes: number) => {
    const newStreakData = await updateStreak(minutes);
    setStreakData(newStreakData);
    await unlock();
  };

  const completeSalah = async (
    salahName: 'fajr' | 'dhuhr' | 'asr' | 'maghrib' | 'isha',
    minutes: number
  ) => {
    const newStatus = await markSalahCompleteStorage(salahName);
    setSalahStatus(newStatus);
    const newStreakData = await updateStreak(minutes);
    setStreakData(newStreakData);
    await unlock();
  };

  const triggerLock = async () => {
    setIsLocked(true);
    await setLockState(true);
  };

  const unlock = async () => {
    setIsLocked(false);
    await setLockState(false);
  };

  const emergencyUnlock = async () => {
    const count = await incrementEmergencyUnlock();
    setStreakData(prev => ({ ...prev, emergencyUnlockCount: count }));
    await unlock();
    return count;
  };

  const completeOnboarding = async (faith: FaithType) => {
    await updateSettings({ faith });
    await setOnboardingComplete(true);
    setHasOnboarded(true);
  };

  const setPremium = async (premium: boolean) => {
    setIsPremium(premium);
    const { setPremiumStatus } = await import('../utils/storage');
    await setPremiumStatus(premium);
  };

  return (
    <AppContext.Provider
      value={{
        settings,
        streakData,
        salahStatus,
        isLocked,
        isPremium,
        isLoading,
        hasOnboarded,
        updateSettings,
        completePrayer,
        completeSalah,
        triggerLock,
        unlock,
        emergencyUnlock,
        refreshData,
        completeOnboarding,
        setPremium,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}
