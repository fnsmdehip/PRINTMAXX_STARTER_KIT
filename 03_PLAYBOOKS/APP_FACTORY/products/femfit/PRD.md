# FemFit - Product Requirements Document

**App Name:** FemFit
**Tagline:** Your workout bestie with a cute cat coach
**Niche:** Women's Fitness
**Clone Model:** Strong app (workout tracking)
**Mascot:** Animated cat coach named "Luna"
**Monetization:** Hard Paywall - $7.99/week or $59.99/year

---

## Overview

FemFit is a workout tracker designed for women. Clean UI, encouraging tone, exercises relevant to women's fitness goals. The cat mascot Luna provides motivation without being annoying.

Core insight: Strong app works but feels clinical. Women want tracking that feels supportive, not like a drill sergeant. Add personality with Luna the cat, focus on exercises women actually do.

---

## Problem Statement

Women's workout tracking pain points:
1. Generic apps designed for men (heavy powerlifting focus)
2. Intimidating interfaces with aggressive language
3. Missing exercises common in women's routines (hip thrusts, glute bridges, pilates moves)
4. No emotional support or encouragement
5. Streak systems that shame instead of motivate

---

## Solution

A workout tracker that:
- Focuses on exercises women actually do
- Uses encouraging language and soft design
- Features Luna the cat as a cheerful mascot
- Tracks streaks positively (celebration, not punishment)
- Provides progress tracking that feels supportive

---

## Target User

**Primary:** Women 18-35 who:
- Go to gym 2-5x per week
- Want to track workouts but find Strong/JEFIT too masculine
- Motivated by cute aesthetics and encouragement
- Care about glutes, toning, strength without bulk

**Secondary:** Women starting fitness journey who need guidance on exercises

---

## Competitive Analysis

| App | Monthly | Weakness | Our Angle |
|-----|---------|----------|-----------|
| Strong | $9.99 | Clinical, masculine feel | Soft, encouraging |
| JEFIT | $12.99 | Cluttered, complex | Clean, simple |
| Fitbod | $12.99 | AI picks exercises (less control) | User picks, we suggest |
| Hevy | Free/Premium | Generic, not women-focused | Women-first |

---

## User Stories (MVP)

### US001: Exercise Library
**As a** user
**I want to** browse exercises by muscle group
**So that** I can find moves for my workout

**Acceptance Criteria:**
- Categories: Glutes, Legs, Arms, Core, Back, Chest, Shoulders, Full Body
- Each exercise has: name, gif/illustration, muscles worked, tips
- Search functionality
- Favorite exercises for quick access
- Women-focused selection (hip thrusts, glute bridges, cable kickbacks, etc.)

**Implementation Notes:**
- Static exercise data in JSON
- Animated illustrations (Lottie or static images)
- Local storage for favorites

---

### US002: Create Workout
**As a** user
**I want to** create a custom workout
**So that** I can log my gym sessions

**Acceptance Criteria:**
- Name workout (default: date + muscle group)
- Add exercises from library
- Reorder exercises via drag-drop
- Save as template for reuse
- Luna says encouraging message when creating

**Implementation Notes:**
- Workout stored in local DB (AsyncStorage or SQLite)
- Template system for recurring workouts

---

### US003: Log Sets During Workout
**As a** user
**I want to** log weight and reps during my workout
**So that** I track my progress

**Acceptance Criteria:**
- Active workout screen shows current exercise
- Input fields: weight (lb/kg toggle), reps
- Previous performance shown for reference
- Rest timer between sets (optional)
- Swipe to complete set
- Luna animations for milestones (first set, PR, workout complete)

**Implementation Notes:**
- Keep screen awake during workout
- Auto-save every set
- Haptic feedback on set completion

---

### US004: Progress Tracking
**As a** user
**I want to** see my progress over time
**So that** I stay motivated

**Acceptance Criteria:**
- View history of each exercise
- Charts showing weight/reps progression
- Personal records (PRs) highlighted
- Weekly/monthly volume summaries
- Luna celebrates PRs with special animation

**Implementation Notes:**
- Simple line charts (Victory Charts or similar)
- PR detection on each exercise
- Confetti animation for PRs

---

### US005: Streak Tracking
**As a** user
**I want to** track my workout streak
**So that** I maintain consistency

**Acceptance Criteria:**
- Current streak displayed on home
- Calendar view showing workout days
- Weekly goal setting (e.g., 4 workouts/week)
- Luna encouragement based on streak status
- Gentle language for missed days (not punishing)

**Language Examples:**
- Streak active: "5 days strong! Luna's so proud!"
- Missed day: "Rest days matter too. Ready when you are!"
- Comeback: "Welcome back! Luna missed you!"

**Implementation Notes:**
- Streak count in local storage
- Weekly goal tracked separately from daily streak

---

### US006: Cat Mascot (Luna)
**As a** user
**I want to** see Luna the cat mascot
**So that** working out feels fun

**Acceptance Criteria:**
- Luna appears on home screen
- Different animations for:
  - Idle (sitting, blinking)
  - Encouraging (waving paw, hearts)
  - Celebrating (jumping, confetti)
  - Sleeping (rest day)
- Luna says contextual messages
- Option to disable in settings (sad Luna "I'll wait here")

**Luna Personality:**
- Cheerful but not annoying
- Supportive without toxic positivity
- Cat-like behaviors (stretching, napping)
- Speaks in short encouraging phrases

**Implementation Notes:**
- Lottie animations for Luna
- 4-6 animation states
- Message bank for contextual text

---

### US007: Hard Paywall
**As a** new user
**I want to** try before buying
**So that** I know the app works for me

**Acceptance Criteria:**
- 3-day free trial with full features
- Paywall appears after trial or after 3 workouts (whichever first)
- Clear pricing display
- Feature highlights
- Luna on paywall ("Let's keep training together!")
- Restore purchases option

**Pricing:**
- Weekly: $7.99/week
- Annual: $59.99/year (save 63%)

**Implementation Notes:**
- RevenueCat integration
- Trial tracked via local storage + RevenueCat

---

### US008: Onboarding
**As a** new user
**I want** a smooth introduction
**So that** I understand the app quickly

**Onboarding Flow:**
```
Screen 1: "Meet Luna, your workout bestie"
         - Luna waving animation
         - "She's here to cheer you on"

Screen 2: "What are your goals?"
         - Build glutes / Tone arms / Get stronger / General fitness
         - (Used for exercise suggestions, not gatekeeping)

Screen 3: "How often do you work out?"
         - 1-2x / 3-4x / 5+ per week
         - Sets default weekly goal

Screen 4: "You're all set!"
         - Luna celebrating
         - "Let's crush your first workout"

Screen 5: PAYWALL
         - 3-day free trial CTA
```

---

## Design System

### Colors
- Primary: Soft coral (#FF7B7B)
- Secondary: Lavender (#B8A9C9)
- Accent: Mint (#98D7C2)
- Background: Cream (#FFF9F5)
- Text: Soft black (#2D2D2D)

### Typography
- Headings: Rounded sans-serif (Nunito or similar)
- Body: Clean sans-serif (Inter)
- Numbers: Monospace for workout data

### Tone
- Encouraging, not demanding
- Casual, like a friend
- Celebratory for achievements
- Gentle for missed goals

### No-Go Language
- "No pain no gain"
- "Beast mode"
- "Crush it"
- "Destroy"
- Any shaming language

### Yes Language
- "You've got this"
- "Nice work!"
- "Luna's proud"
- "Ready when you are"
- "Progress is progress"

---

## Luna Animation States

| State | Trigger | Animation |
|-------|---------|-----------|
| Idle | Home screen default | Sitting, slow blink |
| Happy | Set completed | Tail wag, smile |
| Excited | PR achieved | Jump, hearts float |
| Celebrating | Workout complete | Confetti, dance |
| Sleeping | Rest day | Curled up, zzz |
| Waving | App open, onboarding | Paw wave |
| Stretching | Before workout | Cat stretch pose |
| Cheering | During workout | Pom poms (cute) |

---

## Exercise Library (MVP - 50 Exercises)

### Glutes (12)
- Hip Thrust
- Glute Bridge
- Cable Kickback
- Romanian Deadlift
- Sumo Deadlift
- Bulgarian Split Squat
- Step Up
- Fire Hydrant
- Donkey Kick
- Frog Pump
- Cable Pull Through
- Banded Walk

### Legs (10)
- Squat
- Goblet Squat
- Leg Press
- Leg Curl
- Leg Extension
- Calf Raise
- Lunge
- Walking Lunge
- Wall Sit
- Good Morning

### Arms (8)
- Bicep Curl
- Hammer Curl
- Tricep Pushdown
- Tricep Dip
- Overhead Tricep Extension
- Concentration Curl
- Cable Curl
- Skull Crusher

### Back (6)
- Lat Pulldown
- Seated Row
- Bent Over Row
- Face Pull
- Single Arm Row
- Pull Up

### Chest (4)
- Bench Press
- Incline Press
- Chest Fly
- Push Up

### Shoulders (5)
- Shoulder Press
- Lateral Raise
- Front Raise
- Rear Delt Fly
- Arnold Press

### Core (5)
- Plank
- Crunch
- Russian Twist
- Leg Raise
- Dead Bug

---

## Database Schema

```sql
-- Exercises (static, bundled with app)
exercises: {
  id: string,
  name: string,
  category: string,
  muscles: string[],
  description: string,
  tips: string[],
  imageUrl: string
}

-- User Workouts
workouts: {
  id: string,
  name: string,
  date: timestamp,
  duration: number, // minutes
  exercises: WorkoutExercise[]
}

-- Workout Exercise
workoutExercise: {
  exerciseId: string,
  sets: Set[]
}

-- Set
set: {
  weight: number,
  reps: number,
  completed: boolean
}

-- User Profile
profile: {
  id: string,
  name: string,
  goals: string[],
  weeklyGoal: number,
  currentStreak: number,
  longestStreak: number,
  totalWorkouts: number,
  joined: timestamp
}

-- Templates
templates: {
  id: string,
  name: string,
  exercises: {
    exerciseId: string,
    targetSets: number
  }[]
}
```

---

## MVP Feature Matrix

| Feature | Priority | Effort | In MVP |
|---------|----------|--------|--------|
| Exercise Library | P0 | Medium | Yes |
| Create Workout | P0 | Medium | Yes |
| Log Sets | P0 | Medium | Yes |
| Progress Charts | P1 | Medium | Yes |
| Streak Tracking | P1 | Low | Yes |
| Luna Mascot | P1 | Medium | Yes |
| Hard Paywall | P0 | Low | Yes |
| Onboarding | P0 | Low | Yes |
| Templates | P2 | Low | Yes |
| Rest Timer | P2 | Low | Yes |
| Export Data | P3 | Medium | No |
| Apple Watch | P3 | High | No |
| Social Features | P4 | High | No |

---

## Technical Stack

- **Framework:** Expo (React Native)
- **Navigation:** Expo Router
- **State:** Zustand (lightweight)
- **Storage:** AsyncStorage + MMKV for performance
- **Animations:** Lottie (Luna), Reanimated (UI)
- **Charts:** Victory Native
- **Payments:** RevenueCat
- **Analytics:** Mixpanel (free tier)

---

## Success Metrics

| Metric | Target | How |
|--------|--------|-----|
| Trial to Paid | >12% | RevenueCat |
| Day 7 Retention | >35% | Analytics |
| Workouts/User/Week | >2.5 | In-app tracking |
| App Store Rating | >4.7 | Reviews |
| Luna Interaction | >80% keep enabled | Settings tracking |

---

## Launch Plan

### Pre-Launch
- [ ] MVP complete
- [ ] 20+ beta testers (women's fitness communities)
- [ ] Luna animations finalized
- [ ] App Store screenshots (show Luna, soft colors)
- [ ] ASO optimized description

### Launch Channels
- TikTok: @femfit.app (workout clips with Luna overlays)
- Instagram: Aesthetic gym content
- Reddit: r/xxfitness, r/StrongCurves
- Facebook: Women's fitness groups

### Content Strategy
- "Workout with me" videos featuring app
- Luna reaction videos to workouts
- Before/after progress (with permission)
- Exercise tutorial clips

---

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Luna feels gimmicky | Medium | Make her optional, keep personality subtle |
| Not enough exercises | Low | Launch with 50, add based on requests |
| Strong app is free tier | High | Compete on experience, not features |
| Women don't want "women's app" | Low | Marketing focuses on UX, Luna, not gender |

---

## Future Features

**v1.1:**
- Apple Watch companion
- More Luna outfits/customization
- Body measurements tracking

**v1.2:**
- Workout plans (4-week programs)
- Period cycle integration (adjust recommendations)
- Progress photos

**v2.0:**
- Social features (share workouts)
- Challenges with friends
- Luna friends (unlock different mascots)

---

## Appendix: Luna Message Bank

**Workout Start:**
- "Let's do this!"
- "Ready to get strong?"
- "Luna believes in you!"

**Set Complete:**
- "Nice!"
- "Solid!"
- "Keep going!"
- (purr sound)

**PR Achieved:**
- "NEW PR! You're amazing!"
- "Look at you getting stronger!"
- "Luna's doing a happy dance!"

**Workout Complete:**
- "Crushed it! Time for recovery."
- "Another one in the books!"
- "Luna's so proud of you!"

**Streak Milestones:**
- 7 days: "One week strong! You're building a habit!"
- 30 days: "A whole month! Luna's impressed!"
- 100 days: "100 DAYS! You're basically a legend now."

**Rest Day:**
- "Rest day = growth day. Luna's napping too."
- "Recovery is part of the process!"
- "Your muscles are thanking you."

**Comeback After Break:**
- "Welcome back! Luna missed you!"
- "Ready when you are. No judgment here."
- "Let's pick up where we left off!"
