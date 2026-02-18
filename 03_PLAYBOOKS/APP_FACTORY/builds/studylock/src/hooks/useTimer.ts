import { useEffect, useRef, useCallback } from 'react';
import { AppState, AppStateStatus } from 'react-native';
import { useStudyStore } from '../stores/studyStore';

export const useTimer = () => {
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const backgroundTimeRef = useRef<number>(0);
  const { timer, tick, pauseSession } = useStudyStore();

  const startInterval = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }

    intervalRef.current = setInterval(() => {
      tick();
    }, 1000);
  }, [tick]);

  const stopInterval = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }, []);

  // Handle app state changes (background/foreground)
  useEffect(() => {
    const handleAppStateChange = (nextAppState: AppStateStatus) => {
      if (nextAppState === 'background' && timer.isRunning && !timer.isPaused) {
        // App going to background, record time
        backgroundTimeRef.current = Date.now();
        stopInterval();
      } else if (nextAppState === 'active' && backgroundTimeRef.current > 0) {
        // App coming to foreground, calculate elapsed time
        const elapsedSeconds = Math.floor((Date.now() - backgroundTimeRef.current) / 1000);
        backgroundTimeRef.current = 0;

        // Apply elapsed time by ticking
        for (let i = 0; i < elapsedSeconds; i++) {
          tick();
        }

        if (timer.isRunning && !timer.isPaused) {
          startInterval();
        }
      }
    };

    const subscription = AppState.addEventListener('change', handleAppStateChange);

    return () => {
      subscription.remove();
    };
  }, [timer.isRunning, timer.isPaused, tick, startInterval, stopInterval]);

  // Manage timer interval
  useEffect(() => {
    if (timer.isRunning && !timer.isPaused) {
      startInterval();
    } else {
      stopInterval();
    }

    return () => {
      stopInterval();
    };
  }, [timer.isRunning, timer.isPaused, startInterval, stopInterval]);

  return {
    timeRemaining: timer.timeRemaining,
    totalTime: timer.totalTime,
    isRunning: timer.isRunning,
    isPaused: timer.isPaused,
    isBreak: timer.isBreak,
    currentCycle: timer.currentCycle,
    focusMode: timer.focusMode,
  };
};

export default useTimer;
