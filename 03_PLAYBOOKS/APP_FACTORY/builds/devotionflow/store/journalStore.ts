import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

export type PrayerStatus = 'active' | 'answered' | 'archived';

export interface PrayerEntry {
  id: string;
  title: string;
  content: string;
  status: PrayerStatus;
  createdAt: string;
  updatedAt: string;
  answeredAt?: string;
  category?: string;
  isFavorite: boolean;
}

export interface JournalEntry {
  id: string;
  devotionId?: string;
  content: string;
  reflections: string[];
  verse?: string;
  verseReference?: string;
  createdAt: string;
  updatedAt: string;
  mood?: 'grateful' | 'peaceful' | 'seeking' | 'struggling' | 'joyful';
}

interface JournalState {
  // Prayer entries
  prayers: PrayerEntry[];

  // Journal entries
  journalEntries: JournalEntry[];

  // Prayer actions
  addPrayer: (title: string, content: string, category?: string) => string;
  updatePrayer: (id: string, updates: Partial<PrayerEntry>) => void;
  deletePrayer: (id: string) => void;
  markPrayerAnswered: (id: string) => void;
  archivePrayer: (id: string) => void;
  togglePrayerFavorite: (id: string) => void;

  // Journal actions
  addJournalEntry: (entry: Omit<JournalEntry, 'id' | 'createdAt' | 'updatedAt'>) => string;
  updateJournalEntry: (id: string, updates: Partial<JournalEntry>) => void;
  deleteJournalEntry: (id: string) => void;

  // Getters
  getActivePrayers: () => PrayerEntry[];
  getAnsweredPrayers: () => PrayerEntry[];
  getFavoritePrayers: () => PrayerEntry[];
  getJournalEntriesByDate: (date: string) => JournalEntry[];
  getJournalEntryByDevotionId: (devotionId: string) => JournalEntry | undefined;

  // Stats
  getPrayerStats: () => {
    total: number;
    active: number;
    answered: number;
    archived: number;
  };
}

function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

export const useJournalStore = create<JournalState>()(
  persist(
    (set, get) => ({
      prayers: [],
      journalEntries: [],

      // Prayer actions
      addPrayer: (title, content, category) => {
        const id = generateId();
        const now = new Date().toISOString();

        set((state) => ({
          prayers: [
            {
              id,
              title,
              content,
              status: 'active',
              createdAt: now,
              updatedAt: now,
              category,
              isFavorite: false,
            },
            ...state.prayers,
          ],
        }));

        return id;
      },

      updatePrayer: (id, updates) => {
        set((state) => ({
          prayers: state.prayers.map((prayer) =>
            prayer.id === id
              ? { ...prayer, ...updates, updatedAt: new Date().toISOString() }
              : prayer
          ),
        }));
      },

      deletePrayer: (id) => {
        set((state) => ({
          prayers: state.prayers.filter((prayer) => prayer.id !== id),
        }));
      },

      markPrayerAnswered: (id) => {
        set((state) => ({
          prayers: state.prayers.map((prayer) =>
            prayer.id === id
              ? {
                  ...prayer,
                  status: 'answered' as PrayerStatus,
                  answeredAt: new Date().toISOString(),
                  updatedAt: new Date().toISOString(),
                }
              : prayer
          ),
        }));
      },

      archivePrayer: (id) => {
        set((state) => ({
          prayers: state.prayers.map((prayer) =>
            prayer.id === id
              ? {
                  ...prayer,
                  status: 'archived' as PrayerStatus,
                  updatedAt: new Date().toISOString(),
                }
              : prayer
          ),
        }));
      },

      togglePrayerFavorite: (id) => {
        set((state) => ({
          prayers: state.prayers.map((prayer) =>
            prayer.id === id
              ? {
                  ...prayer,
                  isFavorite: !prayer.isFavorite,
                  updatedAt: new Date().toISOString(),
                }
              : prayer
          ),
        }));
      },

      // Journal actions
      addJournalEntry: (entry) => {
        const id = generateId();
        const now = new Date().toISOString();

        set((state) => ({
          journalEntries: [
            {
              ...entry,
              id,
              createdAt: now,
              updatedAt: now,
            },
            ...state.journalEntries,
          ],
        }));

        return id;
      },

      updateJournalEntry: (id, updates) => {
        set((state) => ({
          journalEntries: state.journalEntries.map((entry) =>
            entry.id === id
              ? { ...entry, ...updates, updatedAt: new Date().toISOString() }
              : entry
          ),
        }));
      },

      deleteJournalEntry: (id) => {
        set((state) => ({
          journalEntries: state.journalEntries.filter((entry) => entry.id !== id),
        }));
      },

      // Getters
      getActivePrayers: () => {
        return get().prayers.filter((p) => p.status === 'active');
      },

      getAnsweredPrayers: () => {
        return get().prayers.filter((p) => p.status === 'answered');
      },

      getFavoritePrayers: () => {
        return get().prayers.filter((p) => p.isFavorite);
      },

      getJournalEntriesByDate: (date) => {
        return get().journalEntries.filter((entry) =>
          entry.createdAt.startsWith(date)
        );
      },

      getJournalEntryByDevotionId: (devotionId) => {
        return get().journalEntries.find((entry) => entry.devotionId === devotionId);
      },

      // Stats
      getPrayerStats: () => {
        const prayers = get().prayers;
        return {
          total: prayers.length,
          active: prayers.filter((p) => p.status === 'active').length,
          answered: prayers.filter((p) => p.status === 'answered').length,
          archived: prayers.filter((p) => p.status === 'archived').length,
        };
      },
    }),
    {
      name: 'devotionflow-journal-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);

// Prayer categories
export const prayerCategories = [
  { id: 'personal', label: 'Personal', icon: 'person' },
  { id: 'family', label: 'Family', icon: 'people' },
  { id: 'health', label: 'Health', icon: 'heart' },
  { id: 'work', label: 'Work', icon: 'briefcase' },
  { id: 'relationships', label: 'Relationships', icon: 'heart-circle' },
  { id: 'guidance', label: 'Guidance', icon: 'compass' },
  { id: 'gratitude', label: 'Gratitude', icon: 'sunny' },
  { id: 'world', label: 'World', icon: 'globe' },
];
