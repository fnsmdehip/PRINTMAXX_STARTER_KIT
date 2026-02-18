# App Rebuild Flips - Quick Reference Cheat Sheet

## Greg's 6 Filters (ALL Required)

```
✅ Keyword Pop > 20        (High search volume)
✅ Keyword Diff < 50       (Low competition)
✅ Ratings < 99            (Weak incumbent)
✅ Released < 2 years      (Not established)
✅ ≥2 apps match above     (Validated opportunity)
✅ Category ~$10k+ MRR     (Market size exists)
```

## Daily Checklist (15 min)

```bash
[ ] Check AppTweak movers
[ ] Browse "New & Updated" in target categories
[ ] Log 1-2 apps in APP_OPPORTUNITIES.csv
[ ] Run: python app_monitor.py (validate)
```

## Target Categories

```
🎯 Health & Fitness (Religion/Prayer)
🎯 Productivity (Habits/Journals/Timers)
🎯 Wellness (Meditation/Mood/Gratitude)
🎯 Lifestyle (Routines/Planning)
```

## Red Flags (Skip These)

```
❌ > 500 ratings         (Too established)
❌ Big company          (Legal risk)
❌ Patent/trademark     (Legal risk)
❌ Declining category   (No future)
❌ Specialist domain    (Too complex)
❌ Heavy regulation     (Healthcare, finance)
```

## Green Flags (Pursue These)

```
✅ Simple utility        (Easy to rebuild)
✅ Indie developer      (No VC backing)
✅ Poor UI/UX           (Visible in screenshots)
✅ Old tech stack       (Outdated frameworks)
✅ 3-4 star rating      (Room for improvement)
✅ Review complaints    (Clear pain points)
✅ Missing features     (Low-hanging fruit)
```

## Rebuild Tech Stack

```typescript
// React Native + Expo (latest)
// TypeScript
// Supabase (backend + auth)
// Zustand (state management)
// RevenueCat (subscriptions)
// Claude API (AI features)
// Sentry (error tracking)
// Mixpanel (analytics)
```

## Pricing Strategy

```
FREE:
- Limited features
- Show value
- Clear upgrade CTAs

PRO ($4.99-9.99/mo):
- Unlimited usage
- AI features
- Cloud sync
- No ads
- Export

TARGET: 10% conversion on active users
```

## Launch Sequence

```
1. Soft Launch    → New Zealand (2 weeks)
2. Iterate        → Fix bugs, improve onboarding
3. Full Launch    → US + major markets
4. Community      → IndieHackers, ProductHunt
5. Cross-Promote  → Link between your apps
```

## ASO Formula

```
App Name:      [Problem] + [Solution] (< 30 chars)
               Example: "Prayer Streak - Daily Tracker"

Subtitle:      [Value Prop] (< 30 chars)
               Example: "Build Your Spiritual Habit"

Description:   Hook (3 lines) + Features (bullets) + Social Proof + CTA

Keywords:      [main keyword], [variant 1], [variant 2], ...
               Example: prayer tracker,prayer journal,prayer list

Screenshots:   6.5" iPhone, annotated with text overlays
               Show: Problem → Solution → Results
```

## Cursor Prompt Formula

```
You are an expert mobile app developer.
Build a [CATEGORY] app to replace [TARGET_APP].

TARGET APP ANALYSIS:
- Name: [NAME]
- Rating: [RATING] ([COUNT] ratings)
- Released: [DATE]
- Weaknesses: [LIST FROM REVIEWS]

OUR REBUILD: [NEW_NAME]
- Modern UI (2026 standards)
- AI-powered features
- Fast performance
- Cloud sync
- Subscription model

TECH STACK: [LIST]

Let's build step-by-step...
```

## File Locations

```bash
AUTOMATIONS/app_factory/
├── README.md                      # Full overview
├── monitoring_setup.md            # Detailed monitoring guide
├── cursor_app_rebuild_prompt.md   # Cursor prompts
├── APP_OPPORTUNITIES.csv          # Opportunity tracker
├── app_monitor.py                 # Python monitoring script
├── requirements.txt               # Python dependencies
└── QUICK_REFERENCE.md            # This file
```

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run monitor
python app_monitor.py

# Add opportunity
python app_monitor.py
# → Select: 1. Add opportunities manually

# Generate report
python app_monitor.py
# → Select: 2. Generate analysis report

# Validate filters
python app_monitor.py
# → Select: 3. Validate against Greg's filters
```

## Scoring System (Script Output)

```
Score: 0-100 points

Keyword Pop:    Max 30 pts  (>40 = 30, >30 = 20, >20 = 10)
Keyword Diff:   Max 25 pts  (<30 = 25, <40 = 15, <50 = 5)
Ratings Count:  Max 25 pts  (<50 = 25, <75 = 15, <99 = 5)
Recency:        Max 20 pts  (<6mo = 20, <1yr = 15, <2yr = 10)

GRADES:
A (80+): EXCELLENT OPPORTUNITY - Build immediately
B (60+): GOOD OPPORTUNITY - Validate further
C (40+): MODERATE OPPORTUNITY - Watch and wait
D (<40): WEAK OPPORTUNITY - Skip
```

## Revenue Expectations

```
Per Greg's Strategy:
- EV: High (70% probability)
- Revenue: $10-50k/month per app
- Risk: Low
- Startup: $50 (free tier tools)

REALITY CHECK:
- Month 1: $0-500 (soft launch)
- Month 2: $500-2k (full launch)
- Month 3: $2-5k (organic growth)
- Month 6: $5-10k (stable)
- Month 12: $10-50k (scale)

Build portfolio of 3-5 apps for diversification.
```

## Key URLs

```
Tools:
- AppTweak: https://www.apptweak.com
- data.ai: https://www.data.ai
- Cursor: https://cursor.sh
- Expo: https://expo.dev
- RevenueCat: https://www.revenuecat.com
- Supabase: https://supabase.com

Community:
- IndieHackers: https://www.indiehackers.com
- r/AppBusiness: https://reddit.com/r/AppBusiness
- ProductHunt: https://www.producthunt.com

Stores:
- App Store Connect: https://appstoreconnect.apple.com
- Google Play Console: https://play.google.com/console
```

## Success Metrics to Track

```
Discovery Phase:
[ ] 10+ opportunities logged
[ ] 3+ validated against filters
[ ] 1 selected for rebuild

Build Phase:
[ ] MVP completed in 2 weeks
[ ] 5+ friends tested
[ ] All bugs fixed
[ ] Submitted to stores

Launch Phase:
[ ] Soft launch (2 weeks)
[ ] 100+ downloads
[ ] 3+ reviews (4+ stars)
[ ] Full launch

Growth Phase:
[ ] 1,000 downloads (Month 1)
[ ] 10,000 downloads (Month 3)
[ ] $1,000 MRR (Month 3)
[ ] $10,000 MRR (Month 6)
```

## Master Doc Reference

```
Source: PRINTMAXX_MASTER_OPERATING_SYSTEM_v26_2026-01-19.md
Lines: 2174-2233
Strategy: App Rebuild Flips (Greg Isenberg Alpha)
EV: High (70% prob $10-50k/mo)
Risk: Low
```

## 3-Week Sprint Plan

```
WEEK 1: DISCOVERY
Mon-Fri: Monitor 30 min/day → Log 10 apps
Weekend: Deep dive top 3 → Validate

WEEK 2: VALIDATION
Mon-Wed: Download & test competitors
Thu-Fri: Design rebuild strategy
Weekend: Prep Cursor prompts

WEEK 3: BUILD
Mon-Fri: Build in Cursor (6-8 hrs/day)
Weekend: Test & polish

WEEK 4: LAUNCH
Mon-Tue: Submit to stores
Wed-Fri: Soft launch & iterate
Weekend: Plan next rebuild
```

---

**Print this and keep it visible while monitoring!**

Last Updated: 2026-01-19
