import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { DailyVerse, VerseState } from '../types';
import { STORAGE_KEYS, BIBLE_API_BASE } from '../utils/constants';
import { getToday } from '../utils/dateUtils';

// Popular verses for daily rotation
const VERSE_REFERENCES = [
  'John 3:16',
  'Philippians 4:13',
  'Jeremiah 29:11',
  'Psalm 23:1-6',
  'Proverbs 3:5-6',
  'Romans 8:28',
  'Isaiah 41:10',
  'Matthew 11:28-30',
  'Psalm 46:1',
  'Romans 12:2',
  'Galatians 5:22-23',
  'Joshua 1:9',
  'Psalm 119:105',
  '2 Corinthians 5:17',
  'Ephesians 2:8-9',
  'Hebrews 11:1',
  '1 Peter 5:7',
  'Psalm 37:4',
  'Matthew 6:33',
  'Romans 5:8',
  'Philippians 4:6-7',
  'Psalm 91:1-2',
  'Isaiah 40:31',
  '2 Timothy 1:7',
  'Psalm 27:1',
  'John 14:6',
  'Romans 10:9',
  'Psalm 139:14',
  'Matthew 28:19-20',
  'Colossians 3:23',
];

function getVerseForDate(dateString: string): string {
  // Use date to deterministically pick a verse
  const dateNum = parseInt(dateString.replace(/-/g, ''), 10);
  const index = dateNum % VERSE_REFERENCES.length;
  return VERSE_REFERENCES[index];
}

export const useVerseStore = create<VerseState>((set, get) => ({
  verse: null,
  isLoading: false,
  error: null,

  fetchVerse: async () => {
    const today = getToday();

    // Check cache first
    try {
      const cachedJson = await AsyncStorage.getItem(STORAGE_KEYS.VERSE_CACHE);
      if (cachedJson) {
        const cached: DailyVerse = JSON.parse(cachedJson);
        if (cached.date === today) {
          set({ verse: cached, isLoading: false, error: null });
          return;
        }
      }
    } catch (e) {
      // Cache miss or error, continue to fetch
    }

    set({ isLoading: true, error: null });

    const reference = getVerseForDate(today);

    try {
      const response = await fetch(
        `${BIBLE_API_BASE}/${encodeURIComponent(reference)}?translation=kjv`
      );

      if (!response.ok) {
        throw new Error('Failed to fetch verse');
      }

      const data = await response.json();

      const verse: DailyVerse = {
        reference: data.reference,
        text: data.text.trim(),
        translation: 'KJV',
        date: today,
      };

      // Cache the verse
      await AsyncStorage.setItem(
        STORAGE_KEYS.VERSE_CACHE,
        JSON.stringify(verse)
      );

      set({ verse, isLoading: false, error: null });
    } catch (error) {
      console.error('Failed to fetch verse:', error);

      // Fallback verse
      const fallback: DailyVerse = {
        reference: 'Proverbs 3:5-6',
        text: 'Trust in the LORD with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths.',
        translation: 'KJV',
        date: today,
      };

      set({ verse: fallback, isLoading: false, error: null });
    }
  },
}));
