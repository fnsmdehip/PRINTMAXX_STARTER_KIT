import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { JournalEntry, JournalState } from '../types';
import { STORAGE_KEYS } from '../utils/constants';

function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

export const useJournalStore = create<JournalState>((set, get) => ({
  entries: [],

  addEntry: (entryData) => {
    const now = new Date().toISOString();
    const entry: JournalEntry = {
      ...entryData,
      id: generateId(),
      createdAt: now,
      updatedAt: now,
    };

    set((state) => {
      // Replace if entry for this date exists
      const existingIndex = state.entries.findIndex(
        (e) => e.date === entry.date
      );

      let newEntries: JournalEntry[];
      if (existingIndex >= 0) {
        newEntries = [...state.entries];
        newEntries[existingIndex] = {
          ...entry,
          id: state.entries[existingIndex].id,
          createdAt: state.entries[existingIndex].createdAt,
        };
      } else {
        newEntries = [...state.entries, entry];
      }

      saveEntries(newEntries);
      return { entries: newEntries };
    });
  },

  updateEntry: (id, updates) => {
    set((state) => {
      const newEntries = state.entries.map((e) => {
        if (e.id === id) {
          return {
            ...e,
            ...updates,
            updatedAt: new Date().toISOString(),
          };
        }
        return e;
      });

      saveEntries(newEntries);
      return { entries: newEntries };
    });
  },

  getEntryForDate: (date) => {
    const { entries } = get();
    return entries.find((e) => e.date === date);
  },

  loadFromStorage: async () => {
    try {
      const entriesJson = await AsyncStorage.getItem(STORAGE_KEYS.JOURNAL);
      const entries: JournalEntry[] = entriesJson
        ? JSON.parse(entriesJson)
        : [];

      set({ entries });
    } catch (error) {
      console.error('Failed to load journal from storage:', error);
    }
  },
}));

async function saveEntries(entries: JournalEntry[]): Promise<void> {
  try {
    await AsyncStorage.setItem(STORAGE_KEYS.JOURNAL, JSON.stringify(entries));
  } catch (error) {
    console.error('Failed to save journal entries:', error);
  }
}
