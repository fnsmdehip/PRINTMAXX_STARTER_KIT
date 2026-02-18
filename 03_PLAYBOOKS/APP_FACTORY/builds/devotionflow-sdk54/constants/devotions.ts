// DevotionFlow Content - Daily Devotionals and Bible Verses

export interface DailyVerse {
  id: string;
  verse: string;
  reference: string;
  theme: string;
}

export interface Devotional {
  id: string;
  title: string;
  verse: string;
  verseReference: string;
  content: string;
  prayer: string;
  reflection: string[];
  theme: string;
  dayOfYear: number;
}

// Verse of the Day collection (rotate based on day of year)
export const dailyVerses: DailyVerse[] = [
  {
    id: 'v1',
    verse: 'Trust in the Lord with all your heart and lean not on your own understanding.',
    reference: 'Proverbs 3:5',
    theme: 'trust',
  },
  {
    id: 'v2',
    verse: 'Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.',
    reference: 'Joshua 1:9',
    theme: 'courage',
  },
  {
    id: 'v3',
    verse: 'For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, plans to give you hope and a future.',
    reference: 'Jeremiah 29:11',
    theme: 'hope',
  },
  {
    id: 'v4',
    verse: 'I can do all things through Christ who strengthens me.',
    reference: 'Philippians 4:13',
    theme: 'strength',
  },
  {
    id: 'v5',
    verse: 'The Lord is my shepherd; I shall not want.',
    reference: 'Psalm 23:1',
    theme: 'provision',
  },
  {
    id: 'v6',
    verse: 'Cast all your anxiety on him because he cares for you.',
    reference: '1 Peter 5:7',
    theme: 'peace',
  },
  {
    id: 'v7',
    verse: 'But the fruit of the Spirit is love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control.',
    reference: 'Galatians 5:22-23',
    theme: 'fruit',
  },
  {
    id: 'v8',
    verse: 'Come to me, all you who are weary and burdened, and I will give you rest.',
    reference: 'Matthew 11:28',
    theme: 'rest',
  },
  {
    id: 'v9',
    verse: 'The Lord is near to the brokenhearted and saves the crushed in spirit.',
    reference: 'Psalm 34:18',
    theme: 'comfort',
  },
  {
    id: 'v10',
    verse: 'And we know that in all things God works for the good of those who love him.',
    reference: 'Romans 8:28',
    theme: 'purpose',
  },
  {
    id: 'v11',
    verse: 'Do not be anxious about anything, but in everything by prayer and supplication with thanksgiving let your requests be made known to God.',
    reference: 'Philippians 4:6',
    theme: 'prayer',
  },
  {
    id: 'v12',
    verse: 'He has made everything beautiful in its time.',
    reference: 'Ecclesiastes 3:11',
    theme: 'timing',
  },
  {
    id: 'v13',
    verse: 'Your word is a lamp to my feet and a light to my path.',
    reference: 'Psalm 119:105',
    theme: 'guidance',
  },
  {
    id: 'v14',
    verse: 'The joy of the Lord is your strength.',
    reference: 'Nehemiah 8:10',
    theme: 'joy',
  },
];

// Sample devotionals (in production, these would be loaded from a CMS or API)
export const devotionals: Devotional[] = [
  {
    id: 'd1',
    title: 'Finding Peace in the Storm',
    verse: 'Peace I leave with you; my peace I give you. I do not give to you as the world gives. Do not let your hearts be troubled and do not be afraid.',
    verseReference: 'John 14:27',
    content: `Life often feels like a storm. Deadlines press in, relationships challenge us, and uncertainty looms on the horizon. Yet in the midst of it all, Jesus offers us something remarkable: His peace.

This peace is different from the temporary calm the world offers. It is not dependent on our circumstances. It does not require everything to be perfect. It is a deep, abiding sense of well-being that comes from knowing we are held by the One who calms the seas.

Today, whatever storms you face, remember that you have access to a peace that transcends understanding. It is yours for the taking.`,
    prayer: 'Lord, I receive Your peace today. Help me to rest in Your presence, even when circumstances feel overwhelming. Anchor my heart in the truth that You are with me always. Amen.',
    reflection: [
      'What areas of your life feel stormy right now?',
      'How have you experienced God\'s peace in difficult times before?',
      'What is one step you can take today to rest in His peace?',
    ],
    theme: 'peace',
    dayOfYear: 1,
  },
  {
    id: 'd2',
    title: 'Walking in Faith',
    verse: 'Now faith is confidence in what we hope for and assurance about what we do not see.',
    verseReference: 'Hebrews 11:1',
    content: `Faith is not blind optimism. It is not wishful thinking or positive vibes. Faith is a confident trust in the character and promises of God, even when we cannot see the outcome.

Think of the heroes of faith in Scripture. Abraham left his home not knowing where he was going. Moses confronted Pharaoh with only a staff. David faced Goliath with a sling and stones. Each one stepped forward not because they were certain of success, but because they were certain of God.

What step of faith is God calling you to take today? It may feel small or it may feel impossibly large. Either way, He who calls you is faithful, and He will do it.`,
    prayer: 'Father, strengthen my faith today. Help me to trust Your character when I cannot see the path ahead. Give me courage to take the next step You are calling me to. Amen.',
    reflection: [
      'Where is God asking you to trust Him right now?',
      'What fears are holding you back from stepping out in faith?',
      'Who in your life models faithful trust in God?',
    ],
    theme: 'faith',
    dayOfYear: 2,
  },
  {
    id: 'd3',
    title: 'The Gift of Grace',
    verse: 'For it is by grace you have been saved, through faith - and this is not from yourselves, it is the gift of God.',
    verseReference: 'Ephesians 2:8',
    content: `Grace is the most scandalous word in the Christian vocabulary. It means receiving what we do not deserve. It means God pursuing us before we ever thought to turn to Him. It means our standing with God is not based on our performance but on His love.

We live in a world obsessed with earning. Earn your salary. Earn respect. Earn your place. But grace flips this upside down. You cannot earn it. You can only receive it.

Today, let grace wash over you. You do not have to perform for God. You do not have to prove yourself. You are already loved, already accepted, already His. Rest in that truth.`,
    prayer: 'Lord, thank You for Your grace that reaches me right where I am. Help me to stop striving and simply receive Your love. May Your grace flow through me to others today. Amen.',
    reflection: [
      'Do you find it difficult to receive grace? Why?',
      'How does understanding grace change how you view your failures?',
      'Who needs to receive grace from you today?',
    ],
    theme: 'grace',
    dayOfYear: 3,
  },
  {
    id: 'd4',
    title: 'The Power of Gratitude',
    verse: 'Give thanks in all circumstances; for this is God\'s will for you in Christ Jesus.',
    verseReference: '1 Thessalonians 5:18',
    content: `Gratitude is more than good manners. It is a spiritual practice that shifts our perspective and opens our hearts to God.

Notice the verse does not say to give thanks FOR all circumstances, but IN all circumstances. We do not have to be grateful for suffering or difficulty. But even in the darkest moments, we can find reasons to thank God: for His presence, His promises, His provision.

Gratitude is a choice. It is a discipline. And it has the power to transform our outlook on life. What if you started each day by naming three things you are grateful for? How might that change the way you see your world?`,
    prayer: 'Father, cultivate a heart of gratitude in me. Help me to see Your blessings even in difficult seasons. I choose to thank You today for Your faithfulness. Amen.',
    reflection: [
      'What are three things you are grateful for today?',
      'How does gratitude affect your mood and outlook?',
      'What circumstances make it hardest for you to be thankful?',
    ],
    theme: 'gratitude',
    dayOfYear: 4,
  },
  {
    id: 'd5',
    title: 'Abiding in Love',
    verse: 'As the Father has loved me, so have I loved you. Now remain in my love.',
    verseReference: 'John 15:9',
    content: `Jesus invites us not just to know about His love, but to abide in it. To make our home there. To let it become the atmosphere we breathe, the ground we walk on, the reality that shapes everything else.

Remaining in love means returning to it again and again. When we fail, we return to love. When we doubt, we return to love. When we are tired, anxious, or overwhelmed, we return to love.

His love is not a destination we reach once. It is a home we keep coming back to. Today, whatever you face, remember: you are deeply, completely, unconditionally loved. Remain there.`,
    prayer: 'Jesus, help me to abide in Your love today. When I wander, draw me back. Let Your love be the foundation of everything I do and say. Amen.',
    reflection: [
      'What does it mean to you to abide in Christ\'s love?',
      'What pulls you away from resting in His love?',
      'How can you return to His love throughout your day?',
    ],
    theme: 'love',
    dayOfYear: 5,
  },
];

// Get verse for today based on day of year
export function getTodaysVerse(): DailyVerse {
  const dayOfYear = getDayOfYear();
  const index = dayOfYear % dailyVerses.length;
  return dailyVerses[index];
}

// Get devotional for today based on day of year
export function getTodaysDevotional(): Devotional {
  const dayOfYear = getDayOfYear();
  const index = dayOfYear % devotionals.length;
  return devotionals[index];
}

// Helper to get day of year
function getDayOfYear(): number {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const diff = now.getTime() - start.getTime();
  const oneDay = 1000 * 60 * 60 * 24;
  return Math.floor(diff / oneDay);
}

// Get devotional by ID
export function getDevotionalById(id: string): Devotional | undefined {
  return devotionals.find(d => d.id === id);
}

// Themes for filtering/categorization
export const devotionalThemes = [
  { id: 'peace', label: 'Peace', icon: 'leaf' },
  { id: 'faith', label: 'Faith', icon: 'infinite' },
  { id: 'grace', label: 'Grace', icon: 'heart' },
  { id: 'gratitude', label: 'Gratitude', icon: 'sunny' },
  { id: 'love', label: 'Love', icon: 'heart-circle' },
  { id: 'hope', label: 'Hope', icon: 'star' },
  { id: 'strength', label: 'Strength', icon: 'fitness' },
  { id: 'courage', label: 'Courage', icon: 'shield' },
];
