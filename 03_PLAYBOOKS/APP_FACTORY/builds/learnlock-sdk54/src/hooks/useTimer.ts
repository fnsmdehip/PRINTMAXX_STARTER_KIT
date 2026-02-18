import { useEffect, useRef, useCallback } from 'react';
import { AppState, AppStateStatus } from 'react-native';
import { useTimerStore } from '../stores/timerStore';
import { useStreakStore } from '../stores/streakStore';
import { useUserStore } from '../stores/userStore';

/**
 * Custom hook to manage the Pomodoro timer
 * Handles background state, tick updates, and session recording
 */
export function useTimer() {
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const backgroundTimeRef = useRef<number | null>(null);

  const {
    timerState,
    remainingSeconds,
    totalSeconds,
    currentSessionType,
    todayStudyTime,
    todaySessions,
    workDuration,
    breakDuration,
    startSession,
    pauseSession,
    resumeSession,
    endSession,
    startBreak,
    skipBreak,
    tick,
    getCurrentSession,
    getProgress,
  } = useTimerStore();

  const { recordStudySession } = useStreakStore();
  const { setBlocked, soundEnabled, vibrationEnabled } = useUserStore();

  // Start interval timer
  const startTimer = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }

    timerRef.current = setInterval(() => {
      tick();
    }, 1000);
  }, [tick]);

  // Stop interval timer
  const stopTimer = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  // Handle app state changes (background/foreground)
  useEffect(() => {
    const handleAppStateChange = (nextAppState: AppStateStatus) => {
      if (nextAppState === 'background' || nextAppState === 'inactive') {
        // App going to background
        if (timerState === 'studying' || timerState === 'break') {
          backgroundTimeRef.current = Date.now();
          stopTimer();
        }
      } else if (nextAppState === 'active') {
        // App coming to foreground
        if (backgroundTimeRef.current && (timerState === 'studying' || timerState === 'break')) {
          // Calculate elapsed time while in background
          const elapsedSeconds = Math.floor((Date.now() - backgroundTimeRef.current) / 1000);
          const newRemaining = Math.max(0, remainingSeconds - elapsedSeconds);

          // Update timer state
          if (newRemaining <= 0) {
            // Timer completed while in background
            if (currentSessionType === 'work') {
              endSession(true);
            } else {
              skipBreak();
            }
          } else {
            // Resume with adjusted time
            useTimerStore.setState({ remainingSeconds: newRemaining });
            startTimer();
          }

          backgroundTimeRef.current = null;
        }
      }
    };

    const subscription = AppState.addEventListener('change', handleAppStateChange);

    return () => {
      subscription.remove();
    };
  }, [timerState, remainingSeconds, currentSessionType, endSession, skipBreak, startTimer, stopTimer]);

  // Start/stop timer based on state
  useEffect(() => {
    if (timerState === 'studying' || timerState === 'break') {
      startTimer();
    } else {
      stopTimer();
    }

    return () => {
      stopTimer();
    };
  }, [timerState, startTimer, stopTimer]);

  // Update blocking state based on timer
  useEffect(() => {
    // Block apps when NOT studying (reversed logic - apps blocked until timer completes)
    const shouldBlock = timerState !== 'idle' && currentSessionType === 'work';
    setBlocked(shouldBlock);
  }, [timerState, currentSessionType, setBlocked]);

  // Record session when completed
  useEffect(() => {
    if (todaySessions.length > 0) {
      const lastSession = todaySessions[todaySessions.length - 1];
      if (lastSession.completed && lastSession.endTime) {
        recordStudySession(lastSession);
      }
    }
  }, [todaySessions, recordStudySession]);

  // Public interface
  return {
    // State
    timerState,
    remainingSeconds,
    totalSeconds,
    currentSessionType,
    todayStudyTime,
    todaySessions,
    workDuration,
    breakDuration,
    progress: getProgress(),

    // Actions
    startSession,
    pauseSession,
    resumeSession,
    endSession,
    startBreak,
    skipBreak,

    // Computed
    isStudying: timerState === 'studying',
    isOnBreak: timerState === 'break',
    isPaused: timerState === 'paused',
    isIdle: timerState === 'idle',
    sessionsCompletedToday: todaySessions.filter((s) => s.completed).length,
  };
}
