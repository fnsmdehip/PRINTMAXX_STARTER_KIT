/**
 * Bible API Service
 * Fetches scripture passages from bible-api.com
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import { BiblePassage } from '../types';
import { BIBLE_API_BASE, STORAGE_KEYS } from '../utils/constants';
import { getDayOfYear } from '../utils/dateUtils';

// 365 carefully selected passages for daily reading
// Mix of encouragement, wisdom, and foundational scripture
const DAILY_PASSAGES: string[] = [
  // January (1-31)
  'Psalm 23',
  'Proverbs 3:5-6',
  'Isaiah 40:31',
  'Jeremiah 29:11',
  'Philippians 4:13',
  'Romans 8:28',
  'Joshua 1:9',
  'Psalm 91:1-2',
  'Matthew 11:28-30',
  'John 3:16-17',
  'Psalm 46:1-3',
  'Proverbs 16:3',
  'Isaiah 41:10',
  'Romans 12:2',
  'Psalm 27:1',
  'Colossians 3:23-24',
  'James 1:5',
  'Psalm 119:105',
  '1 Peter 5:7',
  'Hebrews 11:1',
  'Psalm 34:8',
  'Matthew 6:33',
  'Ephesians 2:8-10',
  'Psalm 37:4-5',
  'Galatians 5:22-23',
  'Psalm 139:14',
  'Romans 5:8',
  '2 Timothy 1:7',
  'Psalm 118:24',
  'John 14:6',
  'Psalm 121',

  // February (32-59)
  'Lamentations 3:22-23',
  'Proverbs 4:23',
  'Isaiah 26:3',
  'Romans 15:13',
  'Psalm 51:10',
  'Matthew 5:14-16',
  'Ephesians 6:10-11',
  'Psalm 103:1-5',
  '1 Corinthians 10:13',
  'Psalm 19:14',
  'John 15:5',
  'Proverbs 18:10',
  'Psalm 32:8',
  'Romans 6:23',
  'Isaiah 43:2',
  'Psalm 16:8',
  'Matthew 7:7-8',
  'Ephesians 3:20',
  'Psalm 73:26',
  'James 4:7-8',
  'Psalm 86:5',
  'Proverbs 22:6',
  '1 John 4:19',
  'Psalm 94:18-19',
  'Colossians 3:12-14',
  'Psalm 40:1-3',
  'Romans 10:9',
  'Psalm 147:3',

  // March (60-90)
  'Hebrews 4:16',
  'Psalm 145:18-19',
  'Matthew 28:19-20',
  'Proverbs 11:25',
  'Psalm 62:1-2',
  'John 10:10',
  'Isaiah 55:8-9',
  'Psalm 18:2',
  '2 Corinthians 5:17',
  'Psalm 30:5',
  'Philippians 4:6-7',
  'Psalm 63:1-3',
  'Romans 8:38-39',
  'Psalm 84:11',
  'Matthew 22:37-39',
  'Proverbs 12:25',
  'Psalm 100',
  '1 Thessalonians 5:16-18',
  'Psalm 25:4-5',
  'John 8:32',
  'Isaiah 53:5',
  'Psalm 143:8',
  'Ephesians 4:32',
  'Psalm 55:22',
  'Romans 12:12',
  'Proverbs 17:17',
  'Psalm 5:3',
  'Matthew 6:25-27',
  '1 Peter 2:24',
  'Psalm 138:3',
  'John 16:33',

  // April (91-120)
  'Psalm 42:11',
  'Hebrews 13:5-6',
  'Proverbs 19:21',
  'Psalm 57:1',
  'Romans 14:8',
  'Isaiah 40:29',
  'Psalm 90:12',
  'Colossians 1:16-17',
  'Psalm 46:10',
  'Matthew 11:28',
  'James 1:12',
  'Psalm 77:11-12',
  '2 Corinthians 12:9',
  'Proverbs 31:25',
  'Psalm 112:7',
  'John 1:12',
  'Isaiah 58:11',
  'Psalm 56:3-4',
  'Ephesians 1:7',
  'Psalm 29:11',
  'Romans 3:23-24',
  'Proverbs 27:17',
  'Psalm 107:1',
  'Matthew 5:6',
  '1 Corinthians 13:4-7',
  'Psalm 68:19',
  'John 6:35',
  'Isaiah 61:1-3',
  'Psalm 23:1-3',
  'Hebrews 10:24-25',

  // May (121-151)
  'Psalm 66:16-20',
  'Proverbs 2:6',
  'Romans 11:33',
  'Psalm 119:11',
  'Matthew 19:26',
  'Galatians 2:20',
  'Psalm 31:24',
  'John 13:34-35',
  'Isaiah 46:9-10',
  'Psalm 4:8',
  '1 John 1:9',
  'Proverbs 3:9-10',
  'Psalm 89:1-2',
  'Ephesians 5:1-2',
  'Psalm 95:1-3',
  'Romans 8:1',
  'Matthew 18:20',
  'Psalm 28:7',
  'Colossians 2:6-7',
  'Proverbs 10:22',
  'Psalm 71:5-6',
  'John 11:25-26',
  'Isaiah 12:2',
  'Psalm 92:1-2',
  'Hebrews 12:1-2',
  'Psalm 13:5-6',
  'Romans 4:20-21',
  'Proverbs 15:1',
  'Psalm 136:1',
  'Matthew 17:20',
  '2 Peter 3:9',

  // June (152-181)
  'Psalm 141:3',
  'James 2:17',
  'Isaiah 30:21',
  'Psalm 20:4',
  'John 4:14',
  'Proverbs 14:29',
  'Psalm 48:14',
  'Romans 13:8',
  'Philippians 1:6',
  'Psalm 33:4-5',
  'Matthew 24:35',
  '1 Timothy 6:11-12',
  'Psalm 115:1',
  'Colossians 3:2',
  'Proverbs 21:2',
  'Psalm 9:1-2',
  'John 17:17',
  'Isaiah 64:8',
  'Psalm 85:12',
  'Hebrews 6:19',
  'Proverbs 25:11',
  'Psalm 111:10',
  'Romans 1:16',
  'Matthew 10:31',
  '1 John 3:1',
  'Psalm 126:3',
  'Galatians 6:9',
  'Proverbs 28:13',
  'Psalm 59:16',
  'John 20:29',

  // July (182-212)
  'Psalm 8:3-4',
  'Isaiah 6:8',
  'Romans 2:4',
  'Psalm 102:25-27',
  'Matthew 12:36',
  'Proverbs 6:6-8',
  'Psalm 69:30',
  'Ephesians 4:26-27',
  '1 Corinthians 15:58',
  'Psalm 116:1-2',
  'John 7:37-38',
  'Colossians 4:2',
  'Proverbs 29:25',
  'Psalm 75:1',
  'Romans 9:20-21',
  'Matthew 4:4',
  'Psalm 34:4-5',
  'Hebrews 3:13',
  'Isaiah 49:15-16',
  'Psalm 131:1-2',
  'James 3:17',
  'Proverbs 13:20',
  'Psalm 47:1',
  'John 5:24',
  '2 Corinthians 1:3-4',
  'Psalm 78:4',
  'Romans 7:24-25',
  'Matthew 25:21',
  'Proverbs 24:16',
  'Psalm 150',
  'Ephesians 2:4-5',

  // August (213-243)
  'Psalm 10:14',
  'Isaiah 35:4',
  '1 Peter 4:8',
  'Proverbs 1:7',
  'Psalm 44:8',
  'John 12:46',
  'Romans 5:3-5',
  'Psalm 61:2',
  'Matthew 16:24-26',
  'Colossians 3:17',
  'Proverbs 20:7',
  'Psalm 22:26',
  'Hebrews 9:28',
  'Isaiah 42:16',
  'Psalm 97:10-11',
  '1 Corinthians 6:19-20',
  'Proverbs 23:17-18',
  'Psalm 132:13-14',
  'John 2:5',
  'Romans 6:6-7',
  'Psalm 74:12',
  'Matthew 9:37-38',
  'Galatians 3:26-28',
  'Proverbs 30:5',
  'Psalm 67:1-2',
  'Ephesians 5:15-16',
  'Isaiah 25:9',
  'Psalm 14:2-3',
  'James 5:16',
  '1 John 5:14-15',
  'Proverbs 8:17',

  // September (244-273)
  'Psalm 105:1-4',
  'John 9:25',
  'Romans 8:18',
  'Psalm 119:165',
  'Matthew 13:44',
  'Colossians 1:27',
  'Proverbs 9:10',
  'Psalm 1:1-3',
  'Hebrews 1:3',
  'Isaiah 54:10',
  'Psalm 80:18-19',
  '1 Corinthians 1:9',
  'Proverbs 16:9',
  'Psalm 124:8',
  'John 21:25',
  'Romans 12:1',
  'Psalm 35:28',
  'Matthew 20:26-28',
  'Galatians 5:1',
  'Proverbs 4:7',
  'Psalm 88:1',
  'Ephesians 6:18',
  'Isaiah 40:8',
  'Psalm 108:4-5',
  '2 Timothy 3:16-17',
  'Proverbs 11:3',
  'Psalm 2:11-12',
  'John 18:37',
  'Romans 10:17',
  '1 Peter 1:8-9',

  // October (274-304)
  'Psalm 129:4',
  'Matthew 15:28',
  'Colossians 2:9-10',
  'Proverbs 12:18',
  'Psalm 135:5-6',
  'Hebrews 7:25',
  'Isaiah 43:19',
  'Psalm 36:7-9',
  '1 Corinthians 3:16',
  'Proverbs 17:22',
  'Psalm 72:18-19',
  'John 6:68',
  'Romans 11:36',
  'Psalm 24:1',
  'Matthew 3:17',
  'Galatians 4:6-7',
  'Proverbs 20:24',
  'Psalm 99:9',
  'Ephesians 1:18-19',
  'Isaiah 48:17',
  'Psalm 110:1',
  '2 Corinthians 3:17-18',
  'Proverbs 13:12',
  'Psalm 6:9',
  'John 14:26-27',
  'Romans 12:21',
  'Psalm 119:71',
  'Matthew 6:9-13',
  '1 John 2:17',
  'Proverbs 21:21',
  'Psalm 134:1-3',

  // November (305-334)
  'Hebrews 2:18',
  'Isaiah 60:1',
  'Psalm 17:8',
  '1 Corinthians 2:9',
  'Proverbs 14:12',
  'Psalm 54:4',
  'John 19:30',
  'Romans 8:26-27',
  'Psalm 82:3-4',
  'Matthew 21:22',
  'Colossians 3:1',
  'Proverbs 22:4',
  'Psalm 113:3',
  'Galatians 6:2',
  'Isaiah 33:6',
  'Psalm 39:4-5',
  'Ephesians 3:16-17',
  'Proverbs 27:1',
  'Psalm 142:3',
  'John 8:12',
  'Romans 14:17-18',
  'Psalm 50:15',
  'Matthew 7:24-25',
  '2 Corinthians 4:16-18',
  'Proverbs 19:17',
  'Psalm 96:1-3',
  'Hebrews 11:6',
  '1 Peter 3:15',
  'Isaiah 50:7',
  'Psalm 122:1',

  // December (335-365/366)
  'John 1:1-5',
  'Romans 15:4',
  'Proverbs 16:18',
  'Psalm 130:5-6',
  'Matthew 1:21',
  'Colossians 3:15-16',
  'Psalm 87:3',
  'Galatians 4:4-5',
  'Isaiah 9:6',
  'Psalm 98:1',
  'Luke 2:10-11',
  'Proverbs 18:24',
  'Psalm 104:24',
  'John 1:14',
  'Romans 16:25-27',
  'Psalm 148:1-4',
  'Matthew 2:10-11',
  'Ephesians 1:3-4',
  'Proverbs 23:24',
  'Psalm 33:18-19',
  'Isaiah 7:14',
  'Luke 1:37',
  'Psalm 111:2-4',
  'John 3:30',
  'Romans 8:31-32',
  'Psalm 146:5-6',
  'Matthew 28:20',
  'Colossians 1:13-14',
  'Proverbs 31:30',
  'Psalm 117',
  'Revelation 21:4',
];

interface CachedPassage {
  passage: BiblePassage;
  cachedAt: number;
  dayOfYear: number;
}

const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours

export async function fetchDailyPassage(): Promise<BiblePassage> {
  const dayOfYear = getDayOfYear();
  const passageIndex = (dayOfYear - 1) % DAILY_PASSAGES.length;
  const reference = DAILY_PASSAGES[passageIndex];

  // Check cache first
  try {
    const cached = await AsyncStorage.getItem(STORAGE_KEYS.CACHED_PASSAGES);
    if (cached) {
      const cachedData: CachedPassage = JSON.parse(cached);
      const isValidCache =
        cachedData.dayOfYear === dayOfYear &&
        Date.now() - cachedData.cachedAt < CACHE_DURATION;

      if (isValidCache) {
        return cachedData.passage;
      }
    }
  } catch (error) {
    console.log('Cache miss, fetching fresh');
  }

  // Fetch from API
  const passage = await fetchPassage(reference);

  // Cache the result
  try {
    const cacheData: CachedPassage = {
      passage,
      cachedAt: Date.now(),
      dayOfYear,
    };
    await AsyncStorage.setItem(
      STORAGE_KEYS.CACHED_PASSAGES,
      JSON.stringify(cacheData)
    );
  } catch (error) {
    console.error('Failed to cache passage:', error);
  }

  return passage;
}

export async function fetchPassage(reference: string): Promise<BiblePassage> {
  const encodedRef = encodeURIComponent(reference);
  const url = `${BIBLE_API_BASE}/${encodedRef}`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();

    return {
      reference: data.reference,
      verses: data.verses || [],
      text: data.text,
      translation_id: data.translation_id || 'web',
    };
  } catch (error) {
    console.error('Failed to fetch passage:', error);
    // Return fallback passage
    return {
      reference: 'Psalm 23:1',
      verses: [
        {
          book_id: 'PSA',
          book_name: 'Psalms',
          chapter: 23,
          verse: 1,
          text: 'The LORD is my shepherd; I shall not want.',
        },
      ],
      text: 'The LORD is my shepherd; I shall not want.',
      translation_id: 'web',
    };
  }
}

export function getPassageForDay(dayOfYear: number): string {
  const index = (dayOfYear - 1) % DAILY_PASSAGES.length;
  return DAILY_PASSAGES[index];
}

export { DAILY_PASSAGES };
