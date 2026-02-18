# Cursor App Rebuild Prompt Template

## Overview
This prompt template is designed for use with Cursor AI to rebuild low-quality apps with superior functionality. Based on Greg Isenberg's "App Rebuild Flips" strategy from PRINTMAXX Master Doc v26.

---

## Core Prompt Structure

### Initial Context Setting

```
You are an expert mobile app developer specializing in React Native and Expo.
I need you to help me build a superior version of an existing app that currently
has poor ratings and outdated features.

COMPETITIVE APP ANALYSIS:
- App Name: [TARGET_APP_NAME]
- Category: [CATEGORY]
- Current Rating: [RATING] stars ([RATINGS_COUNT] ratings)
- Release Date: [RELEASE_DATE]
- Price Model: [FREE/PAID/SUBSCRIPTION]
- Key Keywords: [KEYWORD_LIST with Pop/Diff scores]
- Main Weaknesses: [LIST FROM USER REVIEWS]
- Estimated MRR: [EST_MRR]

USER COMPLAINTS (From Reviews):
1. [COMPLAINT_1]
2. [COMPLAINT_2]
3. [COMPLAINT_3]
4. [COMPLAINT_4]
5. [COMPLAINT_5]

OUR REBUILD GOALS:
- Modern, clean UI/UX (2026 design standards)
- Fast performance (optimized from scratch)
- AI-powered features where applicable
- Cross-platform (iOS + Android via React Native)
- Cloud sync capabilities
- In-app subscription monetization
- Accessibility compliant
- Offline-first architecture

TECH STACK:
- React Native + Expo (latest)
- TypeScript
- Supabase (backend + auth)
- Zustand or Redux (state management)
- React Navigation
- RevenueCat (subscriptions)
- Sentry (error tracking)
- React Native Reanimated (animations)

Let's build this app step-by-step, starting with project structure.
```

---

## Detailed Build Prompts

### 1. Project Initialization

```
Create a new React Native Expo app with the following structure:

PROJECT NAME: [app-name]-pro

FOLDER STRUCTURE:
src/
├── components/          # Reusable UI components
│   ├── common/         # Buttons, inputs, cards
│   └── features/       # Feature-specific components
├── screens/            # App screens
├── navigation/         # Navigation configuration
├── services/           # API calls, external services
│   ├── api/
│   ├── auth/
│   └── analytics/
├── store/              # State management
├── hooks/              # Custom React hooks
├── utils/              # Helper functions
├── constants/          # Colors, fonts, config
├── types/              # TypeScript types
└── assets/             # Images, fonts, icons

DEPENDENCIES TO INSTALL:
- expo
- react-navigation (v6+)
- @supabase/supabase-js
- zustand
- react-native-reanimated
- expo-font
- expo-splash-screen
- @react-native-async-storage/async-storage
- react-native-purchases (RevenueCat)

Initialize the project with TypeScript and provide the package.json.
```

### 2. Design System Setup

```
Create a comprehensive design system for the app with:

COLORS (Modern, accessible palette):
- Primary: [COLOR_HEX] - Main brand color
- Secondary: [COLOR_HEX] - Accent color
- Success: #10B981 - Green
- Error: #EF4444 - Red
- Warning: #F59E0B - Amber
- Background: #FFFFFF (light) / #1F2937 (dark)
- Text Primary: #111827 (light) / #F9FAFB (dark)
- Text Secondary: #6B7280 (light) / #D1D5DB (dark)

TYPOGRAPHY:
- Font Family: Inter or SF Pro (system default)
- Heading 1: 32px, bold
- Heading 2: 24px, semibold
- Heading 3: 20px, semibold
- Body: 16px, regular
- Caption: 14px, regular
- Small: 12px, regular

SPACING (Consistent 8px grid):
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px

COMPONENT TOKENS:
- Border Radius: 12px (cards), 8px (buttons), 20px (pills)
- Shadow: Subtle elevation for cards
- Button Height: 48px (touch-friendly)
- Input Height: 48px

Create: src/constants/theme.ts with all tokens.
Create: src/components/common/Button.tsx (primary, secondary, ghost variants)
Create: src/components/common/Input.tsx (with label, error state)
Create: src/components/common/Card.tsx
```

### 3. Core Feature Development

```
Build the core features of the app:

FEATURE 1: [PRIMARY_FEATURE]
- Description: [WHAT IT DOES]
- User Flow:
  1. [STEP_1]
  2. [STEP_2]
  3. [STEP_3]
- Data Model:
  - [FIELD_1]: type
  - [FIELD_2]: type
  - [FIELD_3]: type
- Components Needed:
  - [COMPONENT_1]
  - [COMPONENT_2]
- API Endpoints:
  - GET /[resource]
  - POST /[resource]
  - PUT /[resource]/:id
  - DELETE /[resource]/:id

Implement:
1. Data types (src/types/[feature].ts)
2. API service (src/services/api/[feature].ts)
3. Store (src/store/[feature]Store.ts)
4. Components (src/components/features/[feature]/)
5. Screen (src/screens/[Feature]Screen.tsx)

Make it polished, with loading states, error handling, and empty states.
```

### 4. AI Enhancement Layer (Competitive Edge)

```
Add AI-powered features to differentiate from competitors:

AI FEATURE 1: Smart [FEATURE] Suggestions
- Use case: [DESCRIBE PROBLEM AI SOLVES]
- Implementation:
  - Call Claude/OpenAI API
  - Process user data: [DATA_POINTS]
  - Generate suggestions: [OUTPUT_FORMAT]
  - Display in UI: [WHERE/HOW]
- Prompt template: "[AI_PROMPT_TEMPLATE]"
- Fallback: [WHAT HAPPENS IF API FAILS]

AI FEATURE 2: Personalized [FEATURE]
- Analyze user patterns over time
- Provide insights and recommendations
- Adaptive difficulty/content based on usage

Create:
- src/services/ai/[feature]AI.ts
- src/components/features/AIInsights.tsx
- Proper loading/error UX

Make sure AI features have a "Pro" badge and are part of the subscription upsell.
```

### 5. Subscription & Monetization

```
Implement RevenueCat for subscriptions:

TIERS:
1. Free Tier:
   - [LIMITED_FEATURE_1]
   - [LIMITED_FEATURE_2]
   - Ads (optional)
   - Basic functionality

2. Pro Tier ($4.99/month or $39.99/year):
   - [UNLIMITED_FEATURE_1]
   - [UNLIMITED_FEATURE_2]
   - AI-powered features
   - Cloud sync across devices
   - No ads
   - Priority support
   - [EXCLUSIVE_FEATURE]

IMPLEMENTATION:
- Set up RevenueCat project
- Configure entitlements: "pro_features"
- Create paywall screen (beautiful, compelling)
- Add "Upgrade to Pro" CTAs throughout app
- Implement restore purchases
- Handle subscription status in app state

Create:
- src/services/subscriptions/revenueCat.ts
- src/screens/PaywallScreen.tsx
- src/components/ProBadge.tsx
- src/hooks/useSubscription.ts

Make the paywall visually appealing with:
- Clear value propositions
- Testimonials or social proof (later)
- Comparison table (Free vs Pro)
- Money-back guarantee note
```

### 6. Authentication & User Management

```
Set up Supabase authentication:

AUTH METHODS:
- Email + Password
- Magic Link (passwordless)
- Google Sign-In
- Apple Sign-In (iOS requirement)

FLOWS:
- Onboarding: Welcome → Auth → Profile Setup → Main App
- Sign Up: Email validation, password requirements
- Sign In: Remember me, forgot password
- Profile: Edit name, email, avatar, preferences
- Delete Account: GDPR compliance

Create:
- src/services/auth/supabase.ts
- src/screens/WelcomeScreen.tsx
- src/screens/SignInScreen.tsx
- src/screens/SignUpScreen.tsx
- src/screens/ProfileScreen.tsx
- src/store/authStore.ts

Use AsyncStorage for token persistence.
Implement proper error handling (network, invalid credentials, etc.).
```

### 7. Data Sync & Offline Support

```
Implement offline-first architecture with cloud sync:

STRATEGY:
- Local SQLite database (via expo-sqlite)
- AsyncStorage for small data
- Supabase for cloud sync
- Sync when online, queue when offline
- Conflict resolution (last-write-wins or custom)

IMPLEMENTATION:
- Local CRUD operations work always
- Background sync on app foreground
- Manual sync button in settings
- Sync status indicator (synced, syncing, offline)
- Handle sync errors gracefully

Create:
- src/services/database/sqlite.ts
- src/services/sync/syncManager.ts
- src/hooks/useSyncStatus.ts

Make sure users never lose data, even if offline for days.
```

### 8. Onboarding & UX Polish

```
Create a beautiful onboarding experience:

ONBOARDING FLOW:
1. Splash Screen: Animated logo (1-2 seconds)
2. Welcome Screens (3-4 slides):
   - Slide 1: Main value prop + hero image
   - Slide 2: Key feature 1 + screenshot
   - Slide 3: Key feature 2 + screenshot
   - Slide 4: CTA to sign up
3. Quick Tutorial:
   - Interactive tooltips on first use
   - "Got it" to dismiss
   - Skip option

UX POLISH:
- Smooth animations (React Native Reanimated)
- Haptic feedback on important actions
- Skeleton loaders while fetching data
- Empty states with helpful CTAs
- Success/error toasts (subtle, auto-dismiss)
- Pull-to-refresh on lists
- Swipe gestures where intuitive
- Dark mode support

Create:
- src/screens/SplashScreen.tsx
- src/screens/OnboardingScreen.tsx
- src/components/common/Tooltip.tsx
- src/components/common/Toast.tsx
- src/components/common/SkeletonLoader.tsx
- src/utils/haptics.ts

Make every interaction feel premium and polished.
```

### 9. Analytics & Crash Reporting

```
Set up analytics and error tracking:

ANALYTICS (Choose one):
- Mixpanel (recommended)
- PostHog (open source)
- Amplitude

TRACK THESE EVENTS:
- App Opened
- Feature Used: [feature_name]
- Paywall Viewed
- Subscription Started
- Subscription Cancelled
- [Custom Event 1]
- [Custom Event 2]

CRASH REPORTING:
- Sentry (recommended)
- Track all JS errors
- Track native crashes
- Add user context (id, subscription status)
- Add breadcrumbs for debugging

Create:
- src/services/analytics/analytics.ts
- src/services/analytics/sentry.ts

Initialize in App.tsx.
Add event tracking to all key user actions.
Never track PII without consent.
```

### 10. ASO & Store Optimization

```
Prepare assets for app store submission:

APP METADATA:
- Name: [APP_NAME] (keyword-rich, < 30 chars)
- Subtitle: [SUBTITLE] (value prop, < 30 chars)
- Description:
  - First 3 lines: Hook + key benefits
  - Bullet points: Features
  - Social proof: "Join X users..."
  - Keywords naturally integrated
  - Call to action
- Keywords: [KEYWORD_LIST] (comma-separated, no spaces)
- Category: [PRIMARY] + [SECONDARY]

VISUAL ASSETS:
- App Icon: 1024x1024px, iOS and Android variants
- Screenshots:
  - 6.5" iPhone (1284x2778)
  - 5.5" iPhone (1242x2208)
  - Android (1080x1920)
  - Annotated with text overlays
  - Show key features
  - Use app UI (not mockups)
- Preview Video: 15-30 seconds
  - Show app in action
  - Highlight unique features
  - End with logo + tagline

Create a checklist:
- [ ] App icon finalized
- [ ] Screenshots with annotations
- [ ] Description optimized for keywords
- [ ] Privacy policy URL ready
- [ ] Support email/URL ready
- [ ] App Store Connect profile complete
- [ ] Google Play Console profile complete
```

---

## Example: Full Rebuild Prompt (Prayer Tracker)

```
You are an expert mobile app developer. I need you to build a modern, AI-powered
prayer tracker app to compete with existing low-quality apps in the iOS App Store.

COMPETITIVE ANALYSIS:
- Target App: "Daily Prayer Companion"
- Category: Health & Fitness (Religion)
- Current Rating: 3.2 stars (67 ratings)
- Released: August 2024
- Price: Free with $4.99/month subscription
- Keywords: "prayer tracker" (Pop: 45, Diff: 35), "prayer journal" (Pop: 38, Diff: 40)
- Estimated MRR: $12,000
- Main Weaknesses:
  1. Crashes when adding long prayer entries
  2. No cloud sync (data lost on device change)
  3. Outdated UI (looks like iOS 10)
  4. No reminders work consistently
  5. Limited customization options
  6. No AI features

USER PAIN POINTS (From 1-2 Star Reviews):
- "Lost all my prayers when I got a new phone"
- "App crashes every time I try to edit"
- "Reminders don't work at all"
- "UI is so ugly compared to other apps"
- "Wish it could suggest prayers based on my situation"
- "Can't organize prayers into categories"

OUR REBUILD: "Scripture Streak Pro"

CORE FEATURES:
1. Prayer List Management
   - Add prayers with title, description, category
   - Mark as answered, in progress, or waiting
   - Archive old prayers
   - Search and filter
   - Custom categories

2. Daily Reminders
   - Customizable reminder times
   - Different reminders for different days
   - Gentle notifications with prayer preview
   - Snooze options

3. Prayer Journal
   - Daily entries with mood tracking
   - Reflect on answered prayers
   - Gratitude section
   - Photo attachments

4. AI-Powered Features (PRO):
   - AI prayer suggestions based on situation
   - Scripture recommendations for each prayer
   - Insights from prayer patterns
   - Weekly reflection summaries

5. Cloud Sync (PRO)
   - Supabase backend
   - Sync across devices
   - Backup and restore
   - Export to PDF

6. Community Features (Future)
   - Share prayer requests (anonymous option)
   - Pray for others' requests
   - Encouragement notes

TECH STACK:
- React Native + Expo (SDK 50+)
- TypeScript
- Supabase (auth + database + storage)
- Zustand (state management)
- React Navigation v6
- RevenueCat (subscriptions)
- Anthropic Claude API (AI features)
- Sentry (error tracking)
- Mixpanel (analytics)

MONETIZATION:
- Free Tier: 10 active prayers, basic features, ads
- Pro Tier ($4.99/month or $39.99/year):
  - Unlimited prayers
  - AI prayer assistant
  - Cloud sync
  - No ads
  - Prayer export (PDF)
  - Custom categories
  - Advanced analytics

DESIGN VIBE:
- Calm, peaceful, spiritual aesthetics
- Soft gradients (purple to blue)
- Sans-serif fonts (Inter)
- Generous whitespace
- Subtle animations (fade, slide)
- Dark mode support
- Accessible colors (WCAG AA)

Let's build this app step-by-step:

STEP 1: Initialize the project with proper folder structure and dependencies.
STEP 2: Set up the design system (colors, typography, components).
STEP 3: Build authentication flow with Supabase.
STEP 4: Create the prayer list feature (CRUD operations).
STEP 5: Implement reminders with expo-notifications.
STEP 6: Build the prayer journal screen.
STEP 7: Add AI features with Claude API.
STEP 8: Integrate RevenueCat for subscriptions.
STEP 9: Implement cloud sync with Supabase.
STEP 10: Polish UX with animations and empty states.
STEP 11: Add analytics and crash reporting.
STEP 12: Prepare for app store submission.

Start with STEP 1. After each step, I'll review and we'll proceed to the next.
```

---

## Vibe Coding Best Practices

### 1. Always Specify Output Format
```
"Generate the complete PrayerListScreen.tsx component with:
- TypeScript types
- Proper imports
- FlatList with pull-to-refresh
- Add prayer FAB button
- Empty state
- Loading skeleton
- Error boundary
- Inline comments"
```

### 2. Request Idiomatic Code
```
"Write this using React Native best practices:
- Functional components with hooks
- TypeScript strict mode
- Proper error handling
- Accessible components
- Performance optimized (memo, useCallback)
- Proper cleanup in useEffect"
```

### 3. Ask for Complete Files
```
"Don't give me snippets. Give me the complete, production-ready file that I can
copy-paste directly into my project. Include all imports, types, and exports."
```

### 4. Iterate with Context
```
"The button component you generated looks good, but:
- Make the primary variant have a gradient background
- Add a loading state with a spinner
- Increase touch target to 48x48
- Add haptic feedback on press
- Ensure proper TypeScript types for all props

Regenerate the complete Button.tsx file with these changes."
```

### 5. Request Tests (Optional but Good)
```
"Also generate a test file Button.test.tsx with:
- Render tests for all variants
- Press event tests
- Disabled state tests
- Loading state tests
- Accessibility tests
Use React Native Testing Library."
```

---

## Prompt Modifiers for Different Scenarios

### For Simple Utility Apps
```
"Keep this app simple and focused. No over-engineering.
Just solve [PROBLEM] elegantly with minimal features."
```

### For Social Apps
```
"This app needs to feel alive and connected. Add:
- Real-time updates (Supabase realtime)
- Activity feeds
- User profiles
- Like/comment interactions
- Push notifications for social events"
```

### For Health/Wellness Apps
```
"This app should feel calming and supportive. Add:
- Positive reinforcement (streaks, achievements)
- Gentle reminders
- Progress visualizations
- Mood tracking
- Motivational quotes
- Soft color palette"
```

### For Productivity Apps
```
"This app should feel snappy and efficient. Add:
- Keyboard shortcuts (where applicable)
- Quick actions
- Batch operations
- Smart defaults
- Minimal friction
- Fast load times"
```

---

## Quality Checklist

Before submitting to app stores, ensure:

### Functionality
- [ ] All core features work on iOS and Android
- [ ] App works offline (where applicable)
- [ ] Data persists correctly
- [ ] Authentication flows work
- [ ] Subscriptions work (test in sandbox)
- [ ] Push notifications deliver
- [ ] Deep links work
- [ ] No crashes in production build

### Performance
- [ ] App starts in < 3 seconds
- [ ] Smooth 60fps animations
- [ ] No memory leaks
- [ ] Images optimized
- [ ] Bundle size < 50MB
- [ ] API calls optimized (caching, batching)

### UX/UI
- [ ] Consistent design throughout
- [ ] Dark mode implemented
- [ ] Accessibility labels on all interactive elements
- [ ] Loading states on all async operations
- [ ] Error states with helpful messages
- [ ] Empty states with CTAs
- [ ] Keyboard dismisses properly
- [ ] No visual glitches

### Legal/Compliance
- [ ] Privacy policy written and linked
- [ ] Terms of service written and linked
- [ ] GDPR compliance (data deletion, export)
- [ ] COPPA compliance (if under 13)
- [ ] App Store guidelines followed
- [ ] Google Play policies followed
- [ ] No trademark violations
- [ ] Proper attribution for assets

### ASO
- [ ] Keywords researched and integrated
- [ ] Screenshots annotated
- [ ] Description compelling
- [ ] Icon stands out
- [ ] Preview video recorded
- [ ] Localized for target markets

---

## Deployment Commands

### Build for Testing
```bash
# iOS (TestFlight)
eas build --platform ios --profile preview

# Android (Internal Testing)
eas build --platform android --profile preview
```

### Build for Production
```bash
# iOS
eas build --platform ios --profile production
eas submit --platform ios

# Android
eas build --platform android --profile production
eas submit --platform android
```

### Environment Setup
```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Configure project
eas build:configure
```

---

## Post-Launch Monitoring

### Week 1: Soft Launch
- Monitor crash reports (Sentry)
- Check analytics (Mixpanel)
- Read user reviews
- Fix critical bugs
- Iterate on onboarding

### Week 2-4: Growth
- Run ASO experiments (A/B test screenshots)
- Optimize paywall conversion
- Add user-requested features
- Improve retention (push notifications, emails)
- Launch on ProductHunt or IndieHackers

### Month 2+: Scale
- Cross-promote between apps
- Add referral program
- Expand to adjacent niches
- Build community features
- Consider partnerships

---

## Additional Cursor Tips

### For Complex Components
```
"Build this component in 3 parts:
1. First show me the TypeScript types
2. Then show me the logic (hooks, handlers)
3. Finally show me the JSX

Then combine into final component."
```

### For Refactoring
```
"This component is too large. Refactor it into:
- Main component: [Component]Screen.tsx
- Subcomponents: [Component]Header.tsx, [Component]List.tsx, [Component]Item.tsx
- Hooks: use[Component]Data.ts
- Utils: [component]Utils.ts

Show me the new structure and all files."
```

### For Debugging
```
"I'm getting this error: [ERROR]

In file: [FILE_PATH]

Here's the relevant code: [CODE_SNIPPET]

What's wrong and how do I fix it? Give me the corrected code."
```

---

**Last Updated**: 2026-01-19
**Version**: 1.0
**Status**: Ready for Production Use

Use this prompt template in Cursor to rapidly build superior app rebuilds!
