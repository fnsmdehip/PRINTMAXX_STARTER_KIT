// Luna the Cat - Mascot messages and states

export type LunaState =
  | 'idle'
  | 'happy'
  | 'excited'
  | 'celebrating'
  | 'sleeping'
  | 'waving'
  | 'stretching'
  | 'cheering';

export interface LunaMessage {
  state: LunaState;
  messages: string[];
}

// Context-specific message banks
export const lunaMessages = {
  // Home screen greetings
  homeGreeting: [
    "Hey! Ready to get strong?",
    "Let's crush it today!",
    "Luna's here for you!",
    "Time to move that body!",
    "Another day, another workout!",
  ],

  // Workout start
  workoutStart: [
    "Let's do this!",
    "Ready to get strong?",
    "Luna believes in you!",
    "Time to work!",
    "You've got this!",
  ],

  // Set completed
  setComplete: [
    "Nice!",
    "Solid!",
    "Keep going!",
    "Yesss!",
    "That's it!",
    "Perfect form!",
    "Crushing it!",
  ],

  // PR achieved
  prAchieved: [
    "NEW PR! You're amazing!",
    "Look at you getting stronger!",
    "Luna's doing a happy dance!",
    "Personal best! So proud!",
    "New record! You're a star!",
  ],

  // Workout complete
  workoutComplete: [
    "Crushed it! Time for recovery.",
    "Another one in the books!",
    "Luna's so proud of you!",
    "Amazing workout! Rest up.",
    "You showed up. That's everything.",
  ],

  // Streak milestones
  streak7: [
    "One week strong! You're building a habit!",
    "7 days! Luna's impressed!",
  ],
  streak30: [
    "A whole month! You're incredible!",
    "30 days of showing up. Legend.",
  ],
  streak100: [
    "100 DAYS! You're basically a legend now.",
    "Triple digits! Luna's crying happy tears!",
  ],

  // Rest day
  restDay: [
    "Rest day = growth day. Luna's napping too.",
    "Recovery is part of the process!",
    "Your muscles are thanking you.",
    "Taking a break? Smart move.",
  ],

  // Comeback after break
  comeback: [
    "Welcome back! Luna missed you!",
    "Ready when you are. No judgment here.",
    "Let's pick up where we left off!",
    "Breaks happen. What matters is you're back!",
  ],

  // During workout encouragement
  midWorkout: [
    "You're doing great!",
    "Stay focused!",
    "One rep at a time!",
    "Feel the burn!",
    "Almost there!",
  ],

  // Low energy
  motivation: [
    "Even small workouts count!",
    "Progress isn't always linear.",
    "Show up for yourself today.",
    "One good rep > zero reps.",
  ],

  // Paywall
  paywall: [
    "Let's keep training together!",
    "Luna wants to see you succeed!",
    "We're just getting started!",
  ],

  // Exercise browsing
  browsing: [
    "Find your favorites!",
    "So many moves to try!",
    "Building your perfect workout!",
  ],
};

// Get random message from category
export function getLunaMessage(
  category: keyof typeof lunaMessages
): string {
  const messages = lunaMessages[category];
  return messages[Math.floor(Math.random() * messages.length)];
}

// Get streak-appropriate message
export function getStreakMessage(streak: number): string {
  if (streak >= 100) {
    return getLunaMessage('streak100');
  } else if (streak >= 30) {
    return getLunaMessage('streak30');
  } else if (streak >= 7) {
    return getLunaMessage('streak7');
  }
  return getLunaMessage('homeGreeting');
}

// Luna animation durations (ms)
export const lunaAnimationDurations: Record<LunaState, number> = {
  idle: 3000,
  happy: 1500,
  excited: 2000,
  celebrating: 3000,
  sleeping: 5000,
  waving: 2000,
  stretching: 2500,
  cheering: 2000,
};
