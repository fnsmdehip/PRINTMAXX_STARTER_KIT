import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface OnboardingPreferences {
  useCases: string[];
  experience: string | null;
  onboardingCompleted: boolean;
  completedAt: string | null;
}

interface OnboardingStore extends OnboardingPreferences {
  // Actions
  setUseCases: (useCases: string[]) => void;
  setExperience: (experience: string) => void;
  completeOnboarding: () => void;
  resetOnboarding: () => void;
  getPreferredCategories: () => string[];
}

const STORAGE_KEY = 'promptvault_onboarding';

export const useOnboardingStore = create<OnboardingStore>()(
  persist(
    (set, get) => ({
      useCases: [],
      experience: null,
      onboardingCompleted: false,
      completedAt: null,

      setUseCases: (useCases) => {
        set({ useCases });
      },

      setExperience: (experience) => {
        set({ experience });
      },

      completeOnboarding: () => {
        set({
          onboardingCompleted: true,
          completedAt: new Date().toISOString(),
        });
      },

      resetOnboarding: () => {
        set({
          useCases: [],
          experience: null,
          onboardingCompleted: false,
          completedAt: null,
        });
      },

      // Map use cases to prompt categories for personalization
      getPreferredCategories: () => {
        const { useCases } = get();
        const categoryMap: Record<string, string[]> = {
          writing: ['Writing', 'Content'],
          coding: ['Coding', 'Development'],
          marketing: ['Marketing', 'Sales'],
          creative: ['Creative', 'Design'],
          business: ['Business', 'Strategy'],
          learning: ['Learning', 'Education'],
        };

        const preferredCategories: string[] = [];
        useCases.forEach((useCase) => {
          const categories = categoryMap[useCase];
          if (categories) {
            preferredCategories.push(...categories);
          }
        });

        return preferredCategories;
      },
    }),
    {
      name: STORAGE_KEY,
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);

// Utility function to check if user should see personalized content
export const shouldShowPersonalized = (): boolean => {
  const store = useOnboardingStore.getState();
  return store.onboardingCompleted && store.useCases.length > 0;
};

// Utility to get complexity level based on experience
export const getPromptComplexity = (): 'simple' | 'moderate' | 'advanced' => {
  const store = useOnboardingStore.getState();
  switch (store.experience) {
    case 'beginner':
      return 'simple';
    case 'intermediate':
      return 'moderate';
    case 'advanced':
      return 'advanced';
    default:
      return 'moderate';
  }
};
