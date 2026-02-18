import { useState, useEffect, useRef, useCallback } from 'react';

interface UseTimerProps {
  initialSeconds: number;
  onComplete?: () => void;
  autoStart?: boolean;
}

interface UseTimerReturn {
  secondsRemaining: number;
  isRunning: boolean;
  isPaused: boolean;
  isComplete: boolean;
  progress: number;
  start: () => void;
  pause: () => void;
  resume: () => void;
  reset: () => void;
}

export function useTimer({
  initialSeconds,
  onComplete,
  autoStart = true,
}: UseTimerProps): UseTimerReturn {
  const [secondsRemaining, setSecondsRemaining] = useState(initialSeconds);
  const [isRunning, setIsRunning] = useState(autoStart);
  const [isPaused, setIsPaused] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const onCompleteRef = useRef(onComplete);

  // Keep onComplete ref updated
  useEffect(() => {
    onCompleteRef.current = onComplete;
  }, [onComplete]);

  const clearTimer = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  const start = useCallback(() => {
    setIsRunning(true);
    setIsPaused(false);
  }, []);

  const pause = useCallback(() => {
    setIsRunning(false);
    setIsPaused(true);
    clearTimer();
  }, [clearTimer]);

  const resume = useCallback(() => {
    setIsRunning(true);
    setIsPaused(false);
  }, []);

  const reset = useCallback(() => {
    clearTimer();
    setSecondsRemaining(initialSeconds);
    setIsRunning(false);
    setIsPaused(false);
    setIsComplete(false);
  }, [clearTimer, initialSeconds]);

  useEffect(() => {
    if (isRunning && !isComplete) {
      timerRef.current = setInterval(() => {
        setSecondsRemaining((prev) => {
          if (prev <= 1) {
            clearTimer();
            setIsRunning(false);
            setIsComplete(true);
            onCompleteRef.current?.();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }

    return clearTimer;
  }, [isRunning, isComplete, clearTimer]);

  const progress = 1 - secondsRemaining / initialSeconds;

  return {
    secondsRemaining,
    isRunning,
    isPaused,
    isComplete,
    progress,
    start,
    pause,
    resume,
    reset,
  };
}
