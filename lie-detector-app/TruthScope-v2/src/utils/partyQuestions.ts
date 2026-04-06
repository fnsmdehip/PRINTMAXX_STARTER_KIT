import { PartyQuestion } from './types';

export const PARTY_QUESTIONS: PartyQuestion[] = [
  // MILD - Safe for all groups
  { id: 'm1', text: "Have you ever pretended to like a gift you actually hated?", category: 'mild', isPremium: false },
  { id: 'm2', text: "Have you ever blamed a fart on someone else?", category: 'mild', isPremium: false },
  { id: 'm3', text: "Have you ever called in sick when you weren't actually sick?", category: 'mild', isPremium: false },
  { id: 'm4', text: "Have you ever lied about your age?", category: 'mild', isPremium: false },
  { id: 'm5', text: "Have you ever pretended to know a song you'd never heard?", category: 'mild', isPremium: false },
  { id: 'm6', text: "Have you ever eaten food that someone else ordered?", category: 'mild', isPremium: false },
  { id: 'm7', text: "Have you ever said 'I'm on my way' when you hadn't left yet?", category: 'mild', isPremium: false },
  { id: 'm8', text: "Have you ever pretended your phone died to avoid someone?", category: 'mild', isPremium: false },
  { id: 'm9', text: "Have you ever regifted something?", category: 'mild', isPremium: false },
  { id: 'm10', text: "Have you ever lied about reading a book you never finished?", category: 'mild', isPremium: false },
  { id: 'm11', text: "Have you ever taken credit for someone else's cooking?", category: 'mild', isPremium: false },
  { id: 'm12', text: "Have you ever pretended to understand something you didn't?", category: 'mild', isPremium: false },

  // SPICY - Gets interesting
  { id: 's1', text: "Have you ever gone through someone's phone without permission?", category: 'spicy', isPremium: false },
  { id: 's2', text: "Have you ever lied to get out of a date?", category: 'spicy', isPremium: false },
  { id: 's3', text: "Have you ever had a crush on a friend's partner?", category: 'spicy', isPremium: false },
  { id: 's4', text: "Have you ever lied on your resume?", category: 'spicy', isPremium: false },
  { id: 's5', text: "Have you ever kept a secret that could ruin a friendship?", category: 'spicy', isPremium: false },
  { id: 's6', text: "Have you ever stolen something from a store?", category: 'spicy', isPremium: false },
  { id: 's7', text: "Have you ever lied about how many people you've dated?", category: 'spicy', isPremium: false },
  { id: 's8', text: "Have you ever pretended to be happy in a relationship you wanted to leave?", category: 'spicy', isPremium: false },
  { id: 's9', text: "Have you ever lied to the police?", category: 'spicy', isPremium: true },
  { id: 's10', text: "Have you ever cheated on a test?", category: 'spicy', isPremium: true },
  { id: 's11', text: "Have you ever told someone you loved them when you didn't mean it?", category: 'spicy', isPremium: true },
  { id: 's12', text: "Have you ever sabotaged a coworker?", category: 'spicy', isPremium: true },

  // RANDOM - Unexpected and fun
  { id: 'r1', text: "Is your current hairstyle your actual preference?", category: 'random', isPremium: false },
  { id: 'r2', text: "Do you actually enjoy your job?", category: 'random', isPremium: false },
  { id: 'r3', text: "Have you ever peed in a pool?", category: 'random', isPremium: false },
  { id: 'r4', text: "Do you think you're a good driver?", category: 'random', isPremium: false },
  { id: 'r5', text: "Have you ever pretended to be asleep to avoid something?", category: 'random', isPremium: false },
  { id: 'r6', text: "Do you wash your hands every time after using the bathroom?", category: 'random', isPremium: false },
  { id: 'r7', text: "Have you ever cried during a movie and tried to hide it?", category: 'random', isPremium: true },
  { id: 'r8', text: "Do you secretly judge people's music taste?", category: 'random', isPremium: true },
  { id: 'r9', text: "Have you ever worn the same outfit two days in a row hoping nobody would notice?", category: 'random', isPremium: true },
  { id: 'r10', text: "Do you actually floss as often as you tell your dentist?", category: 'random', isPremium: true },
];

export function getRandomQuestion(
  category?: PartyQuestion['category'],
  includePremium = false,
  excludeIds: string[] = [],
): PartyQuestion | null {
  let pool = PARTY_QUESTIONS.filter(q => !excludeIds.includes(q.id));
  if (category) pool = pool.filter(q => q.category === category);
  if (!includePremium) pool = pool.filter(q => !q.isPremium);
  if (pool.length === 0) return null;
  return pool[Math.floor(Math.random() * pool.length)];
}

export function getQuestionsByCategory(
  category: PartyQuestion['category'],
  includePremium = false,
): PartyQuestion[] {
  return PARTY_QUESTIONS.filter(
    q => q.category === category && (includePremium || !q.isPremium)
  );
}
