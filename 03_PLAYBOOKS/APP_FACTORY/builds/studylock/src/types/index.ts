// StudyLock Type Definitions

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correctAnswer: number;
  subject: Subject;
  difficulty: 'easy' | 'medium' | 'hard';
}

export type Subject =
  | 'general'
  | 'math'
  | 'science'
  | 'history'
  | 'geography'
  | 'literature'
  | 'vocabulary'
  | 'logic';

export type FocusMode = 'pomodoro' | 'deepWork' | 'examPrep' | 'custom';

export interface FocusModeConfig {
  id: FocusMode;
  name: string;
  description: string;
  workMinutes: number;
  breakMinutes: number;
  cycles: number;
  quizFrequency: 'none' | 'low' | 'medium' | 'high';
}

export interface StudySession {
  id: string;
  startTime: number;
  endTime: number | null;
  duration: number;
  focusMode: FocusMode;
  subject: Subject;
  questionsAnswered: number;
  correctAnswers: number;
  completed: boolean;
  penaltyMinutesAdded: number;
}

export interface DailyStats {
  date: string;
  totalMinutes: number;
  sessions: number;
  questionsAnswered: number;
  correctAnswers: number;
  subjectBreakdown: Record<Subject, number>;
}

export interface UserSettings {
  defaultSessionLength: number;
  defaultFocusMode: FocusMode;
  quizDuringSession: boolean;
  quizAfterSession: boolean;
  penaltyMinutes: number;
  notifications: boolean;
  haptics: boolean;
  soundEnabled: boolean;
}

export interface UserProgress {
  totalStudyMinutes: number;
  totalSessions: number;
  currentStreak: number;
  longestStreak: number;
  lastStudyDate: string | null;
  questionsAnswered: number;
  correctAnswers: number;
  isPremium: boolean;
  premiumExpiresAt: string | null;
}

export interface TimerState {
  isRunning: boolean;
  isPaused: boolean;
  timeRemaining: number;
  totalTime: number;
  currentCycle: number;
  isBreak: boolean;
  focusMode: FocusMode;
}

export interface QuizState {
  currentQuestion: QuizQuestion | null;
  questionsAnswered: number;
  correctAnswers: number;
  isActive: boolean;
  lastQuestionTime: number;
}
