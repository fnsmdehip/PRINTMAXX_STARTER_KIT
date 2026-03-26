import AsyncStorage from '@react-native-async-storage/async-storage';
import { BibleBook, Verse } from '../types';
import { BIBLE_BOOKS } from '../constants/bible';
import { getVerseOfTheDay as getVOTD, formatVerseRef, formatVerseForSharing } from '../data/verses';

/**
 * Map from BIBLE_BOOKS display names to bible-api.com compatible names.
 * bible-api.com uses lowercase, mostly matches, but numbered books
 * need specific formatting (e.g. "1 Samuel" -> "1samuel", "Song of Solomon" -> "song of solomon").
 * The API is fairly flexible with naming but we normalize to be safe.
 */
const BOOK_NAME_MAP: Record<string, string> = {
  'Genesis': 'genesis',
  'Exodus': 'exodus',
  'Leviticus': 'leviticus',
  'Numbers': 'numbers',
  'Deuteronomy': 'deuteronomy',
  'Joshua': 'joshua',
  'Judges': 'judges',
  'Ruth': 'ruth',
  '1 Samuel': '1samuel',
  '2 Samuel': '2samuel',
  '1 Kings': '1kings',
  '2 Kings': '2kings',
  '1 Chronicles': '1chronicles',
  '2 Chronicles': '2chronicles',
  'Ezra': 'ezra',
  'Nehemiah': 'nehemiah',
  'Esther': 'esther',
  'Job': 'job',
  'Psalms': 'psalms',
  'Proverbs': 'proverbs',
  'Ecclesiastes': 'ecclesiastes',
  'Song of Solomon': 'song of solomon',
  'Isaiah': 'isaiah',
  'Jeremiah': 'jeremiah',
  'Lamentations': 'lamentations',
  'Ezekiel': 'ezekiel',
  'Daniel': 'daniel',
  'Hosea': 'hosea',
  'Joel': 'joel',
  'Amos': 'amos',
  'Obadiah': 'obadiah',
  'Jonah': 'jonah',
  'Micah': 'micah',
  'Nahum': 'nahum',
  'Habakkuk': 'habakkuk',
  'Zephaniah': 'zephaniah',
  'Haggai': 'haggai',
  'Zechariah': 'zechariah',
  'Malachi': 'malachi',
  'Matthew': 'matthew',
  'Mark': 'mark',
  'Luke': 'luke',
  'John': 'john',
  'Acts': 'acts',
  'Romans': 'romans',
  '1 Corinthians': '1corinthians',
  '2 Corinthians': '2corinthians',
  'Galatians': 'galatians',
  'Ephesians': 'ephesians',
  'Philippians': 'philippians',
  'Colossians': 'colossians',
  '1 Thessalonians': '1thessalonians',
  '2 Thessalonians': '2thessalonians',
  '1 Timothy': '1timothy',
  '2 Timothy': '2timothy',
  'Titus': 'titus',
  'Philemon': 'philemon',
  'Hebrews': 'hebrews',
  'James': 'james',
  '1 Peter': '1peter',
  '2 Peter': '2peter',
  '1 John': '1john',
  '2 John': '2john',
  '3 John': '3john',
  'Jude': 'jude',
  'Revelation': 'revelation',
};

/**
 * Real verse counts per chapter for the KJV Bible.
 * For books/chapters not listed, we fall back to the API response
 * or a reasonable default.
 */
const VERSE_COUNTS: Record<string, number[]> = {
  'Genesis': [31,25,24,26,32,22,24,22,29,32,32,20,18,24,21,16,27,33,38,18,34,24,20,67,34,35,46,22,35,43,55,32,20,31,29,43,36,30,23,23,57,38,34,34,28,34,31,22,33,26],
  'Exodus': [22,25,22,31,23,30,25,32,35,29,10,51,22,31,27,36,16,27,25,26,36,31,33,18,40,37,21,43,46,38,18,35,23,35,35,38,29,31,43,38],
  'Leviticus': [17,16,17,35,19,30,38,36,24,20,47,8,59,57,33,34,16,30,37,27,24,33,44,23,55,46,34],
  'Numbers': [54,34,51,49,31,27,89,26,23,36,35,16,33,45,41,50,13,32,22,29,35,41,30,25,18,65,23,31,40,16,54,42,56,29,34,13],
  'Deuteronomy': [46,37,29,49,33,25,26,20,29,22,32,32,18,29,23,22,20,22,21,20,23,30,25,22,19,19,26,68,29,20,30,52,29,12],
  'Joshua': [18,24,17,24,15,27,26,35,27,43,23,24,33,15,63,10,18,28,51,9,45,34,16,33],
  'Judges': [36,23,31,24,31,40,25,35,57,18,40,15,25,20,20,31,13,31,30,48,25],
  'Ruth': [22,23,18,22],
  '1 Samuel': [28,36,21,22,12,21,17,22,27,27,15,25,23,52,35,23,58,30,24,42,15,23,29,22,44,25,12,25,11,31,13],
  '2 Samuel': [27,32,39,12,25,23,29,18,13,19,27,31,39,33,37,23,29,33,43,26,22,51,39,25],
  '1 Kings': [53,46,28,34,18,38,51,66,28,29,43,33,34,31,34,34,24,46,21,43,29,53],
  '2 Kings': [18,25,27,44,27,33,20,29,37,36,21,21,25,29,38,20,41,37,37,21,26,20,37,20,30],
  '1 Chronicles': [54,55,24,43,26,81,40,40,44,14,47,40,14,17,29,43,27,17,19,8,30,19,32,31,31,32,34,21,30],
  '2 Chronicles': [17,18,17,22,14,42,22,18,31,19,23,16,22,15,19,14,19,34,11,37,20,12,21,27,28,23,9,27,36,27,21,33,25,33,27,23],
  'Ezra': [11,70,13,24,17,22,28,36,15,44],
  'Nehemiah': [11,20,32,23,19,19,73,18,38,39,36,47,31],
  'Esther': [22,23,15,17,14,14,10,17,32,3],
  'Job': [22,13,26,21,27,30,21,22,35,22,20,25,28,22,35,22,16,21,29,29,34,30,17,25,6,14,23,28,25,31,40,22,33,37,16,33,24,41,30,24,34,17],
  'Psalms': [6,12,8,8,12,10,17,9,20,18,7,8,6,7,5,11,15,50,14,9,13,31,6,10,22,12,14,9,11,12,24,11,22,22,28,12,40,22,13,17,13,11,5,26,17,11,9,14,20,23,19,9,6,7,23,13,11,11,17,12,8,12,11,10,13,20,7,35,36,5,24,20,28,23,10,12,20,72,13,19,16,8,18,12,13,17,7,18,52,17,16,15,5,23,11,13,12,9,9,5,8,28,22,35,45,48,43,13,31,7,10,10,9,8,18,19,2,29,176,7,8,9,4,8,5,6,5,6,8,8,3,18,3,3,21,26,9,8,24,13,10,7,12,15,21,10,20,14,9,6],
  'Proverbs': [33,22,35,27,23,35,27,36,18,32,31,28,25,35,33,33,28,24,29,30,31],
  'Ecclesiastes': [18,26,22,16,20,12,29,17,18,20,10,14],
  'Song of Solomon': [17,17,11,16,16,13,13,14],
  'Isaiah': [31,22,26,6,30,13,25,22,21,34,16,6,22,32,9,14,14,7,25,6,17,25,18,23,12,21,13,29,24,33,9,20,24,17,10,22,38,22,8,31,29,25,28,28,25,13,15,22,26,11,23,15,12,17,13,12,21,14,21,22,11,12,19,12,25,24],
  'Jeremiah': [19,37,25,31,31,30,34,22,26,25,23,17,27,22,21,21,27,23,15,18,14,30,40,10,38,24,22,17,32,24,40,44,26,22,19,32,21,28,18,16,18,22,13,30,5,28,7,47,39,46,64,34],
  'Lamentations': [22,22,66,22,22],
  'Ezekiel': [28,10,27,17,17,14,27,18,11,22,25,28,23,23,8,63,24,32,14,49,32,31,49,27,17,21,36,26,21,26,18,32,33,31,15,38,28,23,29,49,26,20,27,31,25,24,23,35],
  'Daniel': [21,49,30,37,31,28,28,27,27,21,45,13],
  'Hosea': [11,23,5,19,15,11,16,14,17,15,12,14,16,9],
  'Joel': [20,32,21],
  'Amos': [15,16,15,13,27,14,17,14,15],
  'Obadiah': [21],
  'Jonah': [17,10,10,11],
  'Micah': [16,13,12,13,15,16,20],
  'Nahum': [15,13,19],
  'Habakkuk': [17,20,19],
  'Zephaniah': [18,15,20],
  'Haggai': [15,23],
  'Zechariah': [21,13,10,14,11,15,14,23,17,12,17,14,9,21],
  'Malachi': [14,17,18,6],
  'Matthew': [25,23,17,25,48,34,29,34,38,42,30,50,58,36,39,28,27,35,30,34,46,46,39,51,46,75,66,20],
  'Mark': [45,28,35,41,43,56,37,38,50,52,33,44,37,72,47,20],
  'Luke': [80,52,38,44,39,49,50,56,62,42,54,59,35,35,32,31,37,43,48,47,38,71,56,53],
  'John': [51,25,36,54,47,71,53,59,41,42,57,50,38,31,27,33,26,40,42,31,25],
  'Acts': [26,47,26,37,42,15,60,40,43,48,30,25,52,28,41,40,34,28,41,38,40,30,35,27,27,32,44,31],
  'Romans': [32,29,31,25,21,23,25,39,33,21,36,21,14,23,33,27],
  '1 Corinthians': [31,16,23,21,13,20,40,13,27,33,34,31,13,40,58,24],
  '2 Corinthians': [24,17,18,18,21,18,16,24,15,18,33,21,14],
  'Galatians': [24,21,29,31,26,18],
  'Ephesians': [23,22,21,32,33,24],
  'Philippians': [30,30,21,23],
  'Colossians': [29,23,25,18],
  '1 Thessalonians': [10,20,13,18,28],
  '2 Thessalonians': [12,17,18],
  '1 Timothy': [20,15,16,16,25,21],
  '2 Timothy': [18,26,17,22],
  'Titus': [16,15,15],
  'Philemon': [25],
  'Hebrews': [14,18,19,16,14,20,28,13,28,39,40,29,25],
  'James': [27,26,18,17,20],
  '1 Peter': [25,25,22,19,14],
  '2 Peter': [21,22,18],
  '1 John': [10,29,24,21,21],
  '2 John': [13],
  '3 John': [14],
  'Jude': [25],
  'Revelation': [20,29,22,11,14,17,17,13,21,11,19,17,18,20,8,21,18,24,21,15,27,21],
};

/**
 * Get the real verse count for a book/chapter from our static data.
 * Falls back to 25 if the book/chapter is unknown (should not happen
 * for standard KJV books).
 */
function getVerseCount(book: string, chapter: number): number {
  const chapters = VERSE_COUNTS[book];
  if (chapters && chapter >= 1 && chapter <= chapters.length) {
    return chapters[chapter - 1];
  }
  return 25;
}

/**
 * Convert a display book name to the bible-api.com URL-safe name.
 */
function getApiBookName(displayName: string): string {
  return BOOK_NAME_MAP[displayName] || displayName.toLowerCase();
}

/**
 * Fetch chapter verses from bible-api.com, with AsyncStorage caching
 * for offline use after first load. Returns placeholder text on failure.
 */
async function fetchChapterFromApi(book: string, chapter: number): Promise<Verse[]> {
  const cacheKey = `@ss_bible_${book}_${chapter}`;

  // 1. Check AsyncStorage cache first (instant, works offline)
  try {
    const cached = await AsyncStorage.getItem(cacheKey);
    if (cached) {
      return JSON.parse(cached) as Verse[];
    }
  } catch {
    // Cache read failed, proceed to API
  }

  // 2. Fetch from bible-api.com (free, no key needed, KJV is public domain)
  const apiBook = getApiBookName(book);
  const verseCount = getVerseCount(book, chapter);
  const url = `https://bible-api.com/${encodeURIComponent(apiBook)}+${chapter}:1-${verseCount}?translation=kjv`;

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000);

    const response = await fetch(url, { signal: controller.signal });
    clearTimeout(timeout);

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    const data = await response.json();

    if (data.verses && Array.isArray(data.verses) && data.verses.length > 0) {
      const verses: Verse[] = data.verses.map((v: { book_name: string; chapter: number; verse: number; text: string }) => ({
        book,
        chapter: v.chapter,
        verse: v.verse,
        text: v.text.replace(/\n/g, ' ').trim(),
        translation: 'KJV',
      }));

      // 3. Cache for offline use
      try {
        await AsyncStorage.setItem(cacheKey, JSON.stringify(verses));
      } catch {
        // Cache write failed, not critical
      }

      return verses;
    }

    throw new Error('No verses in response');
  } catch {
    // 4. Fallback: return placeholder verses with real count
    return buildPlaceholderVerses(book, chapter, verseCount);
  }
}

/**
 * Build placeholder verses for when the API is unreachable.
 * Uses any hardcoded sample texts we have, otherwise shows a
 * helpful message indicating the verse reference.
 */
function buildPlaceholderVerses(book: string, chapter: number, count: number): Verse[] {
  const sampleTexts: Record<string, string> = {
    'Genesis-1-1': 'In the beginning God created the heaven and the earth.',
    'Genesis-1-2': 'And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters.',
    'Genesis-1-3': 'And God said, Let there be light: and there was light.',
    'Genesis-1-4': 'And God saw the light, that it was good: and God divided the light from the darkness.',
    'Genesis-1-5': 'And God called the light Day, and the darkness he called Night. And the evening and the morning were the first day.',
    'John-1-1': 'In the beginning was the Word, and the Word was with God, and the Word was God.',
    'John-1-2': 'The same was in the beginning with God.',
    'John-1-3': 'All things were made by him; and without him was not any thing made that was made.',
    'John-3-16': 'For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.',
    'Psalms-23-1': 'The LORD is my shepherd; I shall not want.',
    'Psalms-23-2': 'He maketh me to lie down in green pastures: he leadeth me beside the still waters.',
    'Psalms-23-3': 'He restoreth my soul: he leadeth me in the paths of righteousness for his name\'s sake.',
  };

  return Array.from({ length: count }, (_, i) => {
    const verseNum = i + 1;
    const key = `${book}-${chapter}-${verseNum}`;
    const text = sampleTexts[key] || `Loading ${book} ${chapter}:${verseNum}... Connect to the internet to download this chapter.`;
    return {
      book,
      chapter,
      verse: verseNum,
      text,
      translation: 'KJV',
    };
  });
}

export const VerseService = {
  getVerseOfTheDay(): Verse {
    return getVOTD();
  },

  formatReference(verse: Verse): string {
    return formatVerseRef(verse);
  },

  formatForSharing(verse: Verse): string {
    return formatVerseForSharing(verse);
  },

  searchBooks(query: string): BibleBook[] {
    if (!query.trim()) return [...BIBLE_BOOKS];
    const lower = query.toLowerCase();
    return BIBLE_BOOKS.filter((book) =>
      book.name.toLowerCase().includes(lower)
    );
  },

  /**
   * Fetch real KJV verses for a chapter from bible-api.com.
   * Results are cached in AsyncStorage for offline reading.
   * Returns placeholder text if API is unreachable.
   */
  async getChapterVerses(book: string, chapter: number): Promise<Verse[]> {
    return fetchChapterFromApi(book, chapter);
  },

  /**
   * Get the real verse count for a book/chapter.
   * Uses a complete static table of KJV verse counts.
   */
  getEstimatedVerseCount(book: string, chapter: number): number {
    return getVerseCount(book, chapter);
  },

  getBookByName(name: string) {
    return BIBLE_BOOKS.find((b) => b.name === name);
  },
};
