import { create } from 'zustand';
import { TimerState, FocusMode, Subject, StudySession } from '../types';
import { FOCUS_MODES, QUIZ_INTERVALS } from '../utils/constants';

interface StudyStore {
  // Timer State
  timer: TimerState;
  currentSession: StudySession | null;
  selectedSubject: Subject;
  customDuration: number;

  // Session Management
  startSession: (focusMode: FocusMode, subject: Subject, customMinutes?: number) => void;
  pauseSession: () => void;
  resumeSession: () => void;
  endSession: (completed: boolean) => StudySession | null;
  addPenaltyTime: (minutes: number) => void;

  // Timer Operations
  tick: () => void;
  startBreak: () => void;
  endBreak: () => void;
  resetTimer: () => void;

  // Settings
  setSelectedSubject: (subject: Subject) => void;
  setCustomDuration: (minutes: number) => void;

  // Quiz Integration
  shouldShowQuiz: () => boolean;
  recordQuizTime: () => void;
  lastQuizTime: number;
}

const generateSessionId = () => `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

const initialTimerState: TimerState = {
  isRunning: false,
  isPaused: false,
  timeRemaining: 25 * 60,
  totalTime: 25 * 60,
  currentCycle: 1,
  isBreak: false,
  focusMode: 'pomodoro',
};

export const useStudyStore = create<StudyStore>((set, get) => ({
  timer: initialTimerState,
  currentSession: null,
  selectedSubject: 'general',
  customDuration: 30,
  lastQuizTime: 0,

  startSession: (focusMode, subject, customMinutes) => {
    const mode = FOCUS_MODES[focusMode];
    const workMinutes = customMinutes || mode.workMinutes;
    const workSeconds = workMinutes * 60;

    const session: StudySession = {
      id: generateSessionId(),
      startTime: Date.now(),
      endTime: null,
      duration: 0,
      focusMode,
      subject,
      questionsAnswered: 0,
      correctAnswers: 0,
      completed: false,
      penaltyMinutesAdded: 0,
    };

    set({
      timer: {
        isRunning: true,
        isPaused: false,
        timeRemaining: workSeconds,
        totalTime: workSeconds,
        currentCycle: 1,
        isBreak: false,
        focusMode,
      },
      currentSession: session,
      selectedSubject: subject,
      lastQuizTime: Date.now(),
    });
  },

  pauseSession: () => {
    set((state) => ({
      timer: {
        ...state.timer,
        isPaused: true,
        isRunning: false,
      },
    }));
  },

  resumeSession: () => {
    set((state) => ({
      timer: {
        ...state.timer,
        isPaused: false,
        isRunning: true,
      },
    }));
  },

  endSession: (completed) => {
    const { currentSession, timer } = get();

    if (!currentSession) return null;

    const endTime = Date.now();
    const durationMs = endTime - currentSession.startTime;
    const durationMinutes = Math.floor(durationMs / 60000);

    const completedSession: StudySession = {
      ...currentSession,
      endTime,
      duration: durationMinutes,
      completed,
    };

    set({
      timer: initialTimerState,
      currentSession: null,
      lastQuizTime: 0,
    });

    return completedSession;
  },

  addPenaltyTime: (minutes) => {
    const { currentSession } = get();
    const penaltySeconds = minutes * 60;

    set((state) => ({
      timer: {
        ...state.timer,
        timeRemaining: state.timer.timeRemaining + penaltySeconds,
        totalTime: state.timer.totalTime + penaltySeconds,
      },
      currentSession: currentSession
        ? {
            ...currentSession,
            penaltyMinutesAdded: currentSession.penaltyMinutesAdded + minutes,
          }
        : null,
    }));
  },

  tick: () => {
    const { timer } = get();

    if (!timer.isRunning || timer.isPaused) return;

    const newTimeRemaining = timer.timeRemaining - 1;

    if (newTimeRemaining <= 0) {
      // Timer completed
      if (timer.isBreak) {
        // Break ended, start next work cycle
        const mode = FOCUS_MODES[timer.focusMode];
        const nextCycle = timer.currentCycle + 1;

        if (nextCycle > mode.cycles) {
          // All cycles completed
          set((state) => ({
            timer: {
              ...state.timer,
              isRunning: false,
              timeRemaining: 0,
            },
          }));
        } else {
          // Start next work cycle
          set((state) => ({
            timer: {
              ...state.timer,
              timeRemaining: mode.workMinutes * 60,
              totalTime: mode.workMinutes * 60,
              currentCycle: nextCycle,
              isBreak: false,
            },
          }));
        }
      } else {
        // Work period ended
        set((state) => ({
          timer: {
            ...state.timer,
            isRunning: false,
            timeRemaining: 0,
          },
        }));
      }
    } else {
      set((state) => ({
        timer: {
          ...state.timer,
          timeRemaining: newTimeRemaining,
        },
      }));
    }
  },

  startBreak: () => {
    const { timer } = get();
    const mode = FOCUS_MODES[timer.focusMode];

    set((state) => ({
      timer: {
        ...state.timer,
        isRunning: true,
        isPaused: false,
        timeRemaining: mode.breakMinutes * 60,
        totalTime: mode.breakMinutes * 60,
        isBreak: true,
      },
    }));
  },

  endBreak: () => {
    const { timer } = get();
    const mode = FOCUS_MODES[timer.focusMode];
    const nextCycle = timer.currentCycle + 1;

    if (nextCycle > mode.cycles) {
      // Session complete
      set({
        timer: initialTimerState,
      });
    } else {
      set((state) => ({
        timer: {
          ...state.timer,
          timeRemaining: mode.workMinutes * 60,
          totalTime: mode.workMinutes * 60,
          currentCycle: nextCycle,
          isBreak: false,
        },
      }));
    }
  },

  resetTimer: () => {
    set({
      timer: initialTimerState,
      currentSession: null,
      lastQuizTime: 0,
    });
  },

  setSelectedSubject: (subject) => {
    set({ selectedSubject: subject });
  },

  setCustomDuration: (minutes) => {
    set({ customDuration: minutes });
  },

  shouldShowQuiz: () => {
    const { timer, lastQuizTime } = get();

    if (!timer.isRunning || timer.isPaused || timer.isBreak) return false;

    const mode = FOCUS_MODES[timer.focusMode];
    const interval = QUIZ_INTERVALS[mode.quizFrequency];

    if (interval === 0) return false;

    const timeSinceLastQuiz = (Date.now() - lastQuizTime) / 1000;
    return timeSinceLastQuiz >= interval;
  },

  recordQuizTime: () => {
    set({ lastQuizTime: Date.now() });
  },
}));
