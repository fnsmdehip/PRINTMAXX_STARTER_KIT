import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Types
export interface WorkoutSet {
  id: string;
  weight: number;
  reps: number;
  completed: boolean;
  isPersonalRecord?: boolean;
}

export interface WorkoutExercise {
  exerciseId: string;
  sets: WorkoutSet[];
}

export interface Workout {
  id: string;
  name: string;
  date: string; // ISO string
  duration: number; // minutes
  exercises: WorkoutExercise[];
  completed: boolean;
}

export interface Template {
  id: string;
  name: string;
  exercises: {
    exerciseId: string;
    targetSets: number;
  }[];
}

export interface PersonalRecord {
  exerciseId: string;
  weight: number;
  reps: number;
  date: string;
}

interface WorkoutState {
  // Active workout
  activeWorkout: Workout | null;
  activeExerciseIndex: number;

  // History
  workoutHistory: Workout[];

  // Templates
  templates: Template[];

  // Personal records
  personalRecords: Record<string, PersonalRecord>;

  // Favorite exercises
  favoriteExercises: string[];

  // Actions
  startWorkout: (name?: string) => void;
  endWorkout: () => void;
  cancelWorkout: () => void;
  addExerciseToWorkout: (exerciseId: string) => void;
  removeExerciseFromWorkout: (index: number) => void;
  addSet: (exerciseIndex: number) => void;
  updateSet: (
    exerciseIndex: number,
    setIndex: number,
    data: Partial<WorkoutSet>
  ) => void;
  completeSet: (exerciseIndex: number, setIndex: number) => void;
  removeSet: (exerciseIndex: number, setIndex: number) => void;
  setActiveExerciseIndex: (index: number) => void;

  // Templates
  saveAsTemplate: (name: string) => void;
  deleteTemplate: (id: string) => void;
  startWorkoutFromTemplate: (templateId: string) => void;

  // Favorites
  toggleFavorite: (exerciseId: string) => void;

  // Helpers
  getLastPerformance: (exerciseId: string) => WorkoutExercise | null;
  checkPersonalRecord: (
    exerciseId: string,
    weight: number,
    reps: number
  ) => boolean;
}

const generateId = () => Math.random().toString(36).substring(2, 9);

export const useWorkoutStore = create<WorkoutState>()(
  persist(
    (set, get) => ({
      activeWorkout: null,
      activeExerciseIndex: 0,
      workoutHistory: [],
      templates: [],
      personalRecords: {},
      favoriteExercises: [],

      startWorkout: (name) => {
        const today = new Date().toLocaleDateString('en-US', {
          weekday: 'short',
          month: 'short',
          day: 'numeric',
        });
        set({
          activeWorkout: {
            id: generateId(),
            name: name || `Workout - ${today}`,
            date: new Date().toISOString(),
            duration: 0,
            exercises: [],
            completed: false,
          },
          activeExerciseIndex: 0,
        });
      },

      endWorkout: () => {
        const { activeWorkout, workoutHistory } = get();
        if (!activeWorkout) return;

        const completedWorkout: Workout = {
          ...activeWorkout,
          completed: true,
          duration: Math.round(
            (Date.now() - new Date(activeWorkout.date).getTime()) / 60000
          ),
        };

        set({
          activeWorkout: null,
          activeExerciseIndex: 0,
          workoutHistory: [completedWorkout, ...workoutHistory],
        });
      },

      cancelWorkout: () => {
        set({
          activeWorkout: null,
          activeExerciseIndex: 0,
        });
      },

      addExerciseToWorkout: (exerciseId) => {
        const { activeWorkout, getLastPerformance } = get();
        if (!activeWorkout) return;

        const lastPerformance = getLastPerformance(exerciseId);
        const defaultSets: WorkoutSet[] = lastPerformance
          ? lastPerformance.sets.map((s) => ({
              id: generateId(),
              weight: s.weight,
              reps: s.reps,
              completed: false,
            }))
          : [
              { id: generateId(), weight: 0, reps: 10, completed: false },
              { id: generateId(), weight: 0, reps: 10, completed: false },
              { id: generateId(), weight: 0, reps: 10, completed: false },
            ];

        set({
          activeWorkout: {
            ...activeWorkout,
            exercises: [
              ...activeWorkout.exercises,
              {
                exerciseId,
                sets: defaultSets,
              },
            ],
          },
        });
      },

      removeExerciseFromWorkout: (index) => {
        const { activeWorkout } = get();
        if (!activeWorkout) return;

        const exercises = [...activeWorkout.exercises];
        exercises.splice(index, 1);

        set({
          activeWorkout: {
            ...activeWorkout,
            exercises,
          },
        });
      },

      addSet: (exerciseIndex) => {
        const { activeWorkout } = get();
        if (!activeWorkout) return;

        const exercises = [...activeWorkout.exercises];
        const lastSet =
          exercises[exerciseIndex].sets[
            exercises[exerciseIndex].sets.length - 1
          ];

        exercises[exerciseIndex].sets.push({
          id: generateId(),
          weight: lastSet?.weight || 0,
          reps: lastSet?.reps || 10,
          completed: false,
        });

        set({
          activeWorkout: {
            ...activeWorkout,
            exercises,
          },
        });
      },

      updateSet: (exerciseIndex, setIndex, data) => {
        const { activeWorkout } = get();
        if (!activeWorkout) return;

        const exercises = [...activeWorkout.exercises];
        exercises[exerciseIndex].sets[setIndex] = {
          ...exercises[exerciseIndex].sets[setIndex],
          ...data,
        };

        set({
          activeWorkout: {
            ...activeWorkout,
            exercises,
          },
        });
      },

      completeSet: (exerciseIndex, setIndex) => {
        const { activeWorkout, checkPersonalRecord, personalRecords } = get();
        if (!activeWorkout) return;

        const exercises = [...activeWorkout.exercises];
        const currentSet = exercises[exerciseIndex].sets[setIndex];
        const exerciseId = exercises[exerciseIndex].exerciseId;

        const isPR = checkPersonalRecord(
          exerciseId,
          currentSet.weight,
          currentSet.reps
        );

        exercises[exerciseIndex].sets[setIndex] = {
          ...currentSet,
          completed: true,
          isPersonalRecord: isPR,
        };

        const newRecords = { ...personalRecords };
        if (isPR) {
          newRecords[exerciseId] = {
            exerciseId,
            weight: currentSet.weight,
            reps: currentSet.reps,
            date: new Date().toISOString(),
          };
        }

        set({
          activeWorkout: {
            ...activeWorkout,
            exercises,
          },
          personalRecords: newRecords,
        });
      },

      removeSet: (exerciseIndex, setIndex) => {
        const { activeWorkout } = get();
        if (!activeWorkout) return;

        const exercises = [...activeWorkout.exercises];
        exercises[exerciseIndex].sets.splice(setIndex, 1);

        set({
          activeWorkout: {
            ...activeWorkout,
            exercises,
          },
        });
      },

      setActiveExerciseIndex: (index) => {
        set({ activeExerciseIndex: index });
      },

      saveAsTemplate: (name) => {
        const { activeWorkout, templates } = get();
        if (!activeWorkout) return;

        const template: Template = {
          id: generateId(),
          name,
          exercises: activeWorkout.exercises.map((e) => ({
            exerciseId: e.exerciseId,
            targetSets: e.sets.length,
          })),
        };

        set({ templates: [template, ...templates] });
      },

      deleteTemplate: (id) => {
        const { templates } = get();
        set({ templates: templates.filter((t) => t.id !== id) });
      },

      startWorkoutFromTemplate: (templateId) => {
        const { templates, startWorkout, addExerciseToWorkout } = get();
        const template = templates.find((t) => t.id === templateId);
        if (!template) return;

        startWorkout(template.name);
        template.exercises.forEach((e) => {
          addExerciseToWorkout(e.exerciseId);
        });
      },

      toggleFavorite: (exerciseId) => {
        const { favoriteExercises } = get();
        const isFavorite = favoriteExercises.includes(exerciseId);

        set({
          favoriteExercises: isFavorite
            ? favoriteExercises.filter((id) => id !== exerciseId)
            : [...favoriteExercises, exerciseId],
        });
      },

      getLastPerformance: (exerciseId) => {
        const { workoutHistory } = get();

        for (const workout of workoutHistory) {
          const exercise = workout.exercises.find(
            (e) => e.exerciseId === exerciseId
          );
          if (exercise) return exercise;
        }
        return null;
      },

      checkPersonalRecord: (exerciseId, weight, reps) => {
        const { personalRecords } = get();
        const currentPR = personalRecords[exerciseId];

        if (!currentPR) return weight > 0;

        // Simple comparison: weight * reps as volume
        const currentVolume = currentPR.weight * currentPR.reps;
        const newVolume = weight * reps;

        return newVolume > currentVolume;
      },
    }),
    {
      name: 'femfit-workout-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
