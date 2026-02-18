/**
 * Bible Service
 * Fetches daily passages and scripture content
 */

import { DailyPassage } from '../stores/devotionStore';

// Daily verses - sample set that cycles through
const DAILY_VERSES = [
  { reference: 'Philippians 4:13', text: 'I can do all things through Christ who strengthens me.' },
  { reference: 'Psalm 23:1-3', text: 'The Lord is my shepherd; I shall not want. He makes me lie down in green pastures. He leads me beside still waters. He restores my soul.' },
  { reference: 'Proverbs 3:5-6', text: 'Trust in the Lord with all your heart, and do not lean on your own understanding. In all your ways acknowledge him, and he will make straight your paths.' },
  { reference: 'Romans 8:28', text: 'And we know that for those who love God all things work together for good, for those who are called according to his purpose.' },
  { reference: 'Isaiah 41:10', text: 'Fear not, for I am with you; be not dismayed, for I am your God; I will strengthen you, I will help you, I will uphold you with my righteous right hand.' },
  { reference: 'Jeremiah 29:11', text: 'For I know the plans I have for you, declares the Lord, plans for welfare and not for evil, to give you a future and a hope.' },
  { reference: 'John 3:16', text: 'For God so loved the world, that he gave his only Son, that whoever believes in him should not perish but have eternal life.' },
  { reference: 'Matthew 11:28-30', text: 'Come to me, all who labor and are heavy laden, and I will give you rest. Take my yoke upon you, and learn from me, for I am gentle and lowly in heart, and you will find rest for your souls. For my yoke is easy, and my burden is light.' },
  { reference: 'Psalm 46:1', text: 'God is our refuge and strength, a very present help in trouble.' },
  { reference: 'Romans 12:2', text: 'Do not be conformed to this world, but be transformed by the renewal of your mind, that by testing you may discern what is the will of God, what is good and acceptable and perfect.' },
  { reference: 'Galatians 5:22-23', text: 'But the fruit of the Spirit is love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, self-control; against such things there is no law.' },
  { reference: 'Joshua 1:9', text: 'Have I not commanded you? Be strong and courageous. Do not be frightened, and do not be dismayed, for the Lord your God is with you wherever you go.' },
  { reference: 'Psalm 119:105', text: 'Your word is a lamp to my feet and a light to my path.' },
  { reference: 'Ephesians 2:8-9', text: 'For by grace you have been saved through faith. And this is not your own doing; it is the gift of God, not a result of works, so that no one may boast.' },
  { reference: '2 Timothy 1:7', text: 'For God gave us a spirit not of fear but of power and love and self-control.' },
  { reference: 'Psalm 27:1', text: 'The Lord is my light and my salvation; whom shall I fear? The Lord is the stronghold of my life; of whom shall I be afraid?' },
  { reference: 'Hebrews 11:1', text: 'Now faith is the assurance of things hoped for, the conviction of things not seen.' },
  { reference: 'Romans 5:8', text: 'But God shows his love for us in that while we were still sinners, Christ died for us.' },
  { reference: '1 Corinthians 10:13', text: 'No temptation has overtaken you that is not common to man. God is faithful, and he will not let you be tempted beyond your ability, but with the temptation he will also provide the way of escape, that you may be able to endure it.' },
  { reference: 'Psalm 37:4', text: 'Delight yourself in the Lord, and he will give you the desires of your heart.' },
  { reference: 'Matthew 6:33', text: 'But seek first the kingdom of God and his righteousness, and all these things will be added to you.' },
  { reference: '1 Peter 5:7', text: 'Casting all your anxieties on him, because he cares for you.' },
  { reference: 'Isaiah 40:31', text: 'But they who wait for the Lord shall renew their strength; they shall mount up with wings like eagles; they shall run and not be weary; they shall walk and not faint.' },
  { reference: 'James 1:2-4', text: 'Count it all joy, my brothers, when you meet trials of various kinds, for you know that the testing of your faith produces steadfastness. And let steadfastness have its full effect, that you may be perfect and complete, lacking in nothing.' },
  { reference: 'Psalm 139:14', text: 'I praise you, for I am fearfully and wonderfully made. Wonderful are your works; my soul knows it very well.' },
  { reference: 'Colossians 3:23', text: 'Whatever you do, work heartily, as for the Lord and not for men.' },
  { reference: 'Philippians 4:6-7', text: 'Do not be anxious about anything, but in everything by prayer and supplication with thanksgiving let your requests be made known to God. And the peace of God, which surpasses all understanding, will guard your hearts and your minds in Christ Jesus.' },
  { reference: 'Deuteronomy 31:6', text: 'Be strong and courageous. Do not fear or be in dread of them, for it is the Lord your God who goes with you. He will not leave you or forsake you.' },
  { reference: 'John 14:6', text: 'Jesus said to him, "I am the way, and the truth, and the life. No one comes to the Father except through me."' },
  { reference: 'Romans 6:23', text: 'For the wages of sin is death, but the free gift of God is eternal life in Christ Jesus our Lord.' },
  { reference: 'Psalm 91:1-2', text: 'He who dwells in the shelter of the Most High will abide in the shadow of the Almighty. I will say to the Lord, "My refuge and my fortress, my God, in whom I trust."' },
];

/**
 * Fetch daily passage based on day of year
 */
export async function fetchDailyPassage(): Promise<DailyPassage> {
  // Get day of year to determine which verse to show
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const diff = now.getTime() - start.getTime();
  const oneDay = 1000 * 60 * 60 * 24;
  const dayOfYear = Math.floor(diff / oneDay);

  // Use modulo to cycle through verses
  const verseIndex = dayOfYear % DAILY_VERSES.length;
  const verse = DAILY_VERSES[verseIndex];

  return {
    reference: verse.reference,
    text: verse.text,
    translation: 'ESV',
  };
}

/**
 * Fetch verse from Bible API (optional external source)
 */
export async function fetchVerseFromApi(reference: string): Promise<DailyPassage | null> {
  try {
    const response = await fetch(
      `https://bible-api.com/${encodeURIComponent(reference)}?translation=web`
    );

    if (!response.ok) {
      throw new Error('Failed to fetch verse');
    }

    const data = await response.json();

    return {
      reference: data.reference,
      text: data.text.trim(),
      translation: data.translation_name || 'WEB',
    };
  } catch (error) {
    console.error('Failed to fetch from Bible API:', error);
    return null;
  }
}
