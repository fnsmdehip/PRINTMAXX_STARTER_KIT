import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface FavoriteState {
  favoriteIds: string[];

  // Actions
  addFavorite: (promptId: string) => void;
  removeFavorite: (promptId: string) => void;
  toggleFavorite: (promptId: string) => void;
  isFavorite: (promptId: string) => boolean;
  clearAllFavorites: () => void;
}

export const useFavoriteStore = create<FavoriteState>()(
  persist(
    (set, get) => ({
      favoriteIds: [],

      addFavorite: (promptId) => {
        set((state) => ({
          favoriteIds: state.favoriteIds.includes(promptId)
            ? state.favoriteIds
            : [...state.favoriteIds, promptId],
        }));
      },

      removeFavorite: (promptId) => {
        set((state) => ({
          favoriteIds: state.favoriteIds.filter((id) => id !== promptId),
        }));
      },

      toggleFavorite: (promptId) => {
        const { favoriteIds } = get();
        if (favoriteIds.includes(promptId)) {
          set({ favoriteIds: favoriteIds.filter((id) => id !== promptId) });
        } else {
          set({ favoriteIds: [...favoriteIds, promptId] });
        }
      },

      isFavorite: (promptId) => {
        return get().favoriteIds.includes(promptId);
      },

      clearAllFavorites: () => {
        set({ favoriteIds: [] });
      },
    }),
    {
      name: 'promptvault-favorites',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
