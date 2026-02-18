import { create } from 'zustand';
import { QuizQuestion, Subject, QuizState } from '../types';
import quizQuestions from '../data/quizQuestions.json';

interface QuizStore {
  state: QuizState;
  availableQuestions: QuizQuestion[];
  answeredQuestionIds: Set<string>;

  // Actions
  loadQuestions: (subject?: Subject) => void;
  getRandomQuestion: (subject?: Subject) => QuizQuestion | null;
  submitAnswer: (questionId: string, selectedIndex: number) => boolean;
  startQuiz: () => void;
  endQuiz: () => { correct: number; total: number };
  resetQuiz: () => void;
  clearAnsweredQuestions: () => void;
}

const initialState: QuizState = {
  currentQuestion: null,
  questionsAnswered: 0,
  correctAnswers: 0,
  isActive: false,
  lastQuestionTime: 0,
};

export const useQuizStore = create<QuizStore>((set, get) => ({
  state: initialState,
  availableQuestions: quizQuestions as QuizQuestion[],
  answeredQuestionIds: new Set(),

  loadQuestions: (subject) => {
    const allQuestions = quizQuestions as QuizQuestion[];
    const filtered = subject && subject !== 'general'
      ? allQuestions.filter((q) => q.subject === subject)
      : allQuestions;

    set({ availableQuestions: filtered });
  },

  getRandomQuestion: (subject) => {
    const { availableQuestions, answeredQuestionIds } = get();

    let pool = availableQuestions;

    if (subject && subject !== 'general') {
      pool = availableQuestions.filter((q) => q.subject === subject);
    }

    // Filter out already answered questions
    const unanswered = pool.filter((q) => !answeredQuestionIds.has(q.id));

    // If all questions answered, reset the pool
    if (unanswered.length === 0) {
      set({ answeredQuestionIds: new Set() });
      return pool[Math.floor(Math.random() * pool.length)] || null;
    }

    const randomIndex = Math.floor(Math.random() * unanswered.length);
    const question = unanswered[randomIndex];

    set((state) => ({
      state: {
        ...state.state,
        currentQuestion: question,
        lastQuestionTime: Date.now(),
      },
    }));

    return question;
  },

  submitAnswer: (questionId, selectedIndex) => {
    const { state, answeredQuestionIds } = get();

    if (!state.currentQuestion || state.currentQuestion.id !== questionId) {
      return false;
    }

    const isCorrect = selectedIndex === state.currentQuestion.correctAnswer;

    const newAnsweredIds = new Set(answeredQuestionIds);
    newAnsweredIds.add(questionId);

    set((prevState) => ({
      state: {
        ...prevState.state,
        questionsAnswered: prevState.state.questionsAnswered + 1,
        correctAnswers: prevState.state.correctAnswers + (isCorrect ? 1 : 0),
        currentQuestion: null,
      },
      answeredQuestionIds: newAnsweredIds,
    }));

    return isCorrect;
  },

  startQuiz: () => {
    set((state) => ({
      state: {
        ...state.state,
        isActive: true,
        questionsAnswered: 0,
        correctAnswers: 0,
      },
    }));
  },

  endQuiz: () => {
    const { state } = get();
    const result = {
      correct: state.correctAnswers,
      total: state.questionsAnswered,
    };

    set({ state: { ...initialState } });

    return result;
  },

  resetQuiz: () => {
    set({ state: initialState });
  },

  clearAnsweredQuestions: () => {
    set({ answeredQuestionIds: new Set() });
  },
}));
