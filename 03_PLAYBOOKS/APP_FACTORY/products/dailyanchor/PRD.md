# DailyAnchor PRD

**Version:** 1.0
**Last updated:** 2026-01-21
**Status:** MVP Build Complete

---

## Product overview

DailyAnchor is a faith habit tracking app. Users track daily devotional habits, journal gratitude and prayers, and build streaks. The app delivers a daily Bible verse and offers premium features for deeper engagement.

**Tagline:** Start your day grounded

**Target users:**
- Christians building consistent devotional habits
- Busy professionals who want a 5-minute faith routine
- New believers looking for simple daily structure
- Church members participating in group reading plans

---

## Core value proposition

1. **Simple habit tracking** - Check off Bible reading, prayer, and gratitude in under 5 minutes
2. **Streak motivation** - Visual progress and streak counters drive consistency
3. **Daily verse** - Fresh scripture each day via bible-api.com
4. **Private journal** - Gratitude, prayer requests, and reflections stored locally
5. **No social distractions** - No feeds, no friends, just you and your habits

---

## MVP features (complete)

### Today screen
- Daily greeting with date
- Streak counter with emoji milestones
- Daily Bible verse from bible-api.com
- Habit checklist with completion tracking
- Pull-to-refresh

### Habit checklist
- 3 default habits: Read Bible, Pray, Gratitude
- Visual completion states (checkbox, green highlight)
- Progress bar showing day completion
- Premium habits locked for free users
- "All done" celebration banner

### Journal
- Gratitude input (up to 3 items)
- Prayer request text field
- Reflection text field
- Auto-save to local storage
- Privacy note ("stored locally")

### Progress
- Current streak counter
- Longest streak display
- Calendar view with completed days
- Stats grid: this week, perfect days, journal entries, total completions
- Month navigation

### Paywall
- Feature cards showing premium benefits
- Pricing options (monthly/yearly)
- "Best value" badge on yearly
- 7-day free trial CTA
- Restore purchases link
- Legal text for App Store compliance

### Settings
- Premium upgrade banner (if free)
- Reminder toggle and time picker
- Add premium habit option
- Contact, privacy, terms links
- Premium status display

---

## Premium features

**Yearly:** $49.99/year (7-day free trial)
**Monthly:** $9.99/month

Premium unlocks:
- Unlimited habits (meditation, fasting, scripture memory, church, serving)
- Reading plans (gratitude, peace, purpose)
- Advanced stats
- Audio devotionals (future)
- Cloud sync (future)

---

## Technical implementation

### Stack
- React Native 0.73.2
- TypeScript
- Zustand for state management
- AsyncStorage for persistence
- React Navigation 6.x
- date-fns for date utilities
- RevenueCat for payments (placeholder)

### Architecture
```
src/
  components/
    common/       - Button, Card, DailyVerse
    habits/       - HabitItem, HabitChecklist
    journal/      - GratitudeInput, JournalEntryForm
    streaks/      - StreakCounter, StreakCalendar
    paywall/      - PremiumFeatureCard, PricingOption, PaywallScreen
  screens/        - Today, Journal, Progress, Settings
  navigation/     - TabNavigator, RootNavigator
  store/          - habitStore, journalStore, settingsStore, verseStore
  types/          - TypeScript interfaces
  utils/          - constants, dateUtils
```

### Data models
- **Habit:** id, name, icon, isDefault, isPremium
- **HabitCompletion:** habitId, date, completedAt
- **JournalEntry:** id, date, gratitude[], prayerRequest, reflection
- **UserSettings:** reminderTime, reminderEnabled, focusArea, isPremium

### API integration
- Daily verse: `https://bible-api.com/{reference}?translation=kjv`
- 30 popular verses rotate based on date
- Caches verse locally for the day

---

## Monetization

### Free tier
- 3 default habits
- Basic streak tracking
- Journal
- Daily verse

### Premium tier ($49.99/year or $9.99/month)
- 5 additional habits
- Reading plans
- Advanced analytics
- Audio (future)
- Cloud sync (future)

### Revenue targets
- 10,000 Premium users at $50/year = $500K ARR
- Or 5,000 monthly at $10/month = $600K ARR

---

## Go-to-market

### Launch channels
1. **App Store Optimization** - Keywords: devotional app, Bible habit tracker, daily prayer
2. **Christian influencers** - Partner with faith-based YouTubers and podcasters
3. **Church partnerships** - Offer church license at $99/month
4. **Content marketing** - Blog posts on building faith habits

### Key differentiators vs competitors
- Simpler than YouVersion (no social, no 2000 plan options)
- Cheaper than Glorify ($50/year vs $70/year)
- Church features others lack (dashboard, custom content)
- Focus on habit building, not Bible reading

---

## Success metrics

| Metric | Target |
|--------|--------|
| Day 1 completion rate | > 70% |
| Day 7 retention | > 40% |
| Day 30 retention | > 20% |
| Average streak | > 5 days |
| Free to Premium conversion | > 5% |

---

## Roadmap

### Phase 1: MVP (complete)
- Habit tracking
- Streak display
- Journal
- Daily verse
- Paywall UI

### Phase 2: Core features (next)
- RevenueCat integration
- Push notifications
- Onboarding flow
- Reading plans
- Offline support

### Phase 3: Church features
- Church dashboard
- Member management
- Custom content upload
- Group reading plans

### Phase 4: Polish
- Audio devotionals
- Cloud sync
- Widget
- Apple Watch app

---

## Build location

```
/MONEY_METHODS/APP_FACTORY/builds/dailyanchor/
```

### Key files
- `App.tsx` - Main app entry
- `src/screens/TodayScreen.tsx` - Home screen
- `src/components/habits/HabitChecklist.tsx` - Habit tracking
- `src/components/paywall/PaywallScreen.tsx` - Monetization
- `src/store/*.ts` - State management

---

## Next steps

1. Install dependencies: `npm install`
2. Add RevenueCat API keys to constants.ts
3. Set up push notifications
4. Build onboarding flow
5. Test on iOS and Android simulators
6. Submit to TestFlight/Internal testing

---

## Related docs

- Tech spec: `/MONEY_METHODS/SAAS/products/dailyanchor-app/TECH_SPEC.md`
- Onboarding flow: `/MONEY_METHODS/SAAS/products/dailyanchor-app/ONBOARDING_FLOW.md`
- Competitor analysis: `/MONEY_METHODS/SAAS/products/dailyanchor-app/COMPETITOR_ANALYSIS.md`
