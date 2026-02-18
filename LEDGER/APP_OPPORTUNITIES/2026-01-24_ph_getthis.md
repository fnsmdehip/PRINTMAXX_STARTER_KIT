# GetThis - Voice/Screenshot to Tasks

**Source:** Product Hunt
**URL:** https://www.producthunt.com/posts/getthis
**Date Found:** 2026-01-24
**Upvotes:** 141+ (Day Rank #3)

---

## What It Does

AI-powered task generator that converts voice, text, or screenshots into organized task lists. Users can speak their brain dump or snap a screenshot of a chat/list, and GetThis uses AI to:
- Parse and categorize tasks
- Organize grocery runs
- Extract action items from conversations
- Sort brain dumps into actionable lists

**Tagline:** "Don't Write. Just Say It."

---

## Clone Difficulty

**Rating:** EASY

**Why:**
- Core functionality is voice-to-text + GPT API parsing
- React Native + Whisper API + Claude/GPT for task extraction
- No complex integrations required
- Similar to existing todo apps but with AI layer

**Tech Stack Estimate:**
- React Native (Expo)
- Whisper API or native speech-to-text
- Claude API for task parsing/categorization
- Local storage or simple backend

---

## Niche Angles

| Niche | App Name Ideas | Unique Hook |
|-------|---------------|-------------|
| **Faith** | PrayerTasks, FaithDump | Voice prayer requests to organized prayer lists, Scripture memory tasks |
| **Students** | StudyDump, ClassCapture | Screenshot syllabus to task list, lecture notes to study tasks |
| **ADHD** | BrainDump Pro, FocusTasks | Extra simple UI, dopamine-friendly categorization, body doubling reminders |
| **Moms** | MomBrain, FamilyTasks | Family meal planning, kid activity scheduling, shared household tasks |
| **Fitness** | WorkoutDump, GymCapture | Screenshot workout plan to daily tasks, voice log exercises |
| **Seniors** | SimpleTask, VoiceTodo | Large text, super simple voice interface, medication reminders |

---

## Monetization Model

**Primary:** Subscription
- Free: 10 voice captures/month
- Pro ($4.99/mo): Unlimited captures, advanced categorization
- Family ($9.99/mo): Shared lists, multiple profiles

**Secondary:**
- Affiliate links to productivity tools mentioned in tasks
- Premium AI models (GPT-4o vs GPT-4o-mini)

---

## Competitive Landscape

- **Wispr Flow** (4.7 rating, similar concept)
- **Otter.ai** (meeting transcription, different use case)
- **Todoist** (manual task entry, no voice AI)

**Differentiation opportunity:** Niche-specific task categories and integrations (e.g., faith app auto-categorizes "pray for X" vs "call X")

---

## Implementation Priority

**Score:** 9/10

**Reasons:**
- Simple to build (2-3 week MVP)
- Clear subscription monetization
- Multiple niche angles
- Proven demand (141+ upvotes on Day 1)
- Low competition in niche versions

---

## Next Steps

1. Build MVP with voice-to-task core feature
2. Choose one niche (recommend: ADHD or Moms - underserved)
3. Add screenshot parsing as v1.1
4. Launch on App Store with niche-specific ASO
