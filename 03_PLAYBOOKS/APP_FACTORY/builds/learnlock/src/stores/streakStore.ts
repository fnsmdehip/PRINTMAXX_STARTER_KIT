import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { StreakData, DailyStudyData, StudySession } from '../types';
import { STORAGE_KEYS, MIN_STUDY_TIME_FOR_STREAK } from '../utils/constants';
import {
  getTodayDateString,
  formatDate,
  calculateStreak,
  isYesterday,
  getLastNDays,
} from '../utils/dateUtils';

interface StreakStore extends StreakData {
  // Daily history
  dailyHistory: Record<string, DailyStudyData>;

  // Actions
  recordStudySession: (session: StudySession) => void;
  checkAndUpdateStreak: () => void;
  getTodayData: () => DailyStudyData | null;
  getWeekData: () => DailyStudyData[];
  getMonthData: () => DailyStudyData[];
  getWeeklyAverage: () => number;
  getMonthlyTotal: () => number;
  resetStreak: () => void;
}

const createEmptyDailyData = (date: string): DailyStudyData => ({
  date,
  totalStudyTime: 0,
  sessionsCompleted: 0,
  streakMaintained: false,
  sessions: [],
});

export const useStreakStore = create<StreakStore>()(
  persist(
    (set, get) => ({
      // Initial streak data
      currentStreak: 0,
      longestStreak: 0,
      totalDaysStudied: 0,
      totalStudyHours: 0,
      completedDates: [],
      lastStudyDate: null,

      // Daily history
      dailyHistory: {},

      // Record a completed study session
      recordStudySession: (session: StudySession) => {
        const { dailyHistory, completedDates, totalStudyHours } = get();
        const date = session.date;

        // Get or create daily data
        const dayData = dailyHistory[date] || createEmptyDailyData(date);

        // Update daily data
        const updatedDayData: DailyStudyData = {
          ...dayData,
          totalStudyTime: dayData.totalStudyTime + session.duration,
          sessionsCompleted: dayData.sessionsCompleted + (session.completed ? 1 : 0),
          sessions: [...dayData.sessions, session],
        };

        // Check if streak threshold met for the day
        const streakMetToday = updatedDayData.totalStudyTime >= MIN_STUDY_TIME_FOR_STREAK;
        updatedDayData.streakMaintained = streakMetToday;

        // Update completed dates if threshold met
        let newCompletedDates = completedDates;
        if (streakMetToday && !completedDates.includes(date)) {
          newCompletedDates = [...completedDates, date].sort();
        }

        // Calculate new streak
        const newCurrentStreak = calculateStreak(newCompletedDates);
        const { longestStreak } = get();

        set({
          dailyHistory: { ...dailyHistory, [date]: updatedDayData },
          completedDates: newCompletedDates,
          currentStreak: newCurrentStreak,
          longestStreak: Math.max(longestStreak, newCurrentStreak),
          totalStudyHours: totalStudyHours + session.duration / 3600,
          lastStudyDate: date,
          totalDaysStudied: newCompletedDates.length,
        });
      },

      // Check streak status (call on app launch)
      checkAndUpdateStreak: () => {
        const { completedDates, currentStreak, lastStudyDate } = get();

        // If no study history, reset
        if (!lastStudyDate || completedDates.length === 0) {
          set({ currentStreak: 0 });
          return;
        }

        // Check if streak is still valid
        const today = getTodayDateString();
        const yesterday = formatDate(new Date(Date.now() - 86400000));

        // Streak is valid if last study was today or yesterday
        if (lastStudyDate !== today && lastStudyDate !== yesterday) {
          // Streak broken
          set({ currentStreak: 0 });
          return;
        }

        // Recalculate streak from completed dates
        const newStreak = calculateStreak(completedDates);
        if (newStreak !== currentStreak) {
          set({ currentStreak: newStreak });
        }
      },

      // Get today's study data
      getTodayData: () => {
        const { dailyHistory } = get();
        const today = getTodayDateString();
        return dailyHistory[today] || null;
      },

      // Get this week's study data
      getWeekData: () => {
        const { dailyHistory } = get();
        const weekDates = getLastNDays(7);

        return weekDates.map((date) => dailyHistory[date] || createEmptyDailyData(date));
      },

      // Get this month's study data
      getMonthData: () => {
        const { dailyHistory } = get();
        const monthDates = getLastNDays(30);

        return monthDates.map((date) => dailyHistory[date] || createEmptyDailyData(date));
      },

      // Get weekly average study time (seconds)
      getWeeklyAverage: () => {
        const weekData = get().getWeekData();
        const totalTime = weekData.reduce((sum, day) => sum + day.totalStudyTime, 0);
        return Math.round(totalTime / 7);
      },

      // Get monthly total study time (seconds)
      getMonthlyTotal: () => {
        const monthData = get().getMonthData();
        return monthData.reduce((sum, day) => sum + day.totalStudyTime, 0);
      },

      // Reset streak (used for emergency unlock)
      resetStreak: () => {
        set({ currentStreak: 0 });
      },
    }),
    {
      name: STORAGE_KEYS.STREAK_DATA,
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        currentStreak: state.currentStreak,
        longestStreak: state.longestStreak,
        totalDaysStudied: state.totalDaysStudied,
        totalStudyHours: state.totalStudyHours,
        completedDates: state.completedDates,
        lastStudyDate: state.lastStudyDate,
        dailyHistory: state.dailyHistory,
      }),
    }
  )
);
