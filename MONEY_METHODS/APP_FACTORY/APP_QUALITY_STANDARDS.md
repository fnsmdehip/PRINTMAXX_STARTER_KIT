# App quality standards

**Last updated:** 2026-02-15
**Purpose:** This is THE institutional process document for building apps in the PRINTMAXX factory. Every agent building an app reads this first. No exceptions.
**Stack:** PWA (Next.js/React) + Capacitor.js + RevenueCat + Stripe

---

## 1. Quality philosophy

We are a high-powered AI factory, not a slop factory.

Every app that ships under any PRINTMAXX brand must look like it cost $50K to build. Users should never open the app and think "this looks AI-generated" or "this feels like a tutorial project." The standard is: would a design-conscious user pay money for this? If the answer is "maybe," it's not ready.

Three rules:

1. **Every screen must be intentional.** No screen exists because "apps usually have this." Every screen earns its place by solving a user problem or driving a business outcome.
2. **Details signal quality.** Micro-interactions, loading states, empty states, error messages. These are the difference between a $2.99/week app and an uninstall on day 1.
3. **Native first, web never.** The user is on an iPhone. The app must feel like it belongs on an iPhone. If it feels like a mobile website, it fails.

---

## 2. UI/UX quality checklist (non-negotiable)

Every app must pass all of these before submission. Not most. All.

### Screen requirements

**Minimum 7 unique screens:**
1. Splash screen (branded, animated logo, under 2 seconds)
2. Onboarding screen 1: Value proposition
3. Onboarding screen 2: Personalization (quiz, preferences, or goal setting)
4. Onboarding screen 3: Social proof (ratings, user count, testimonials)
5. Onboarding screen 4: Paywall (animated, with trial)
6. Main app screen (the core experience)
7. Settings screen (subscription management, restore purchases, privacy policy, support)

**Additional screens as needed:**
- Detail/drill-down screens for main content
- Profile/progress screen
- History/analytics screen
- Empty states for every list/feed (designed, not just "No items")
- Error states (designed, not browser default)

### Animation requirements

- [ ] Splash logo animates in (scale + fade, or custom animation)
- [ ] Screen transitions use spring physics (not linear CSS transitions)
- [ ] Buttons have press states (scale down 0.95 + haptic)
- [ ] Tab bar icons animate on selection
- [ ] Progress indicators use animated fills, not jumps
- [ ] Lists use staggered entry animations
- [ ] Pull-to-refresh has custom animation (not default browser)
- [ ] All animations run at 60fps (test with Chrome DevTools Performance tab)
- [ ] No animation exceeds 400ms (users perceive >400ms as laggy)
- [ ] Loading states use skeleton screens, not spinners

### Design system requirements

Every app must have a defined design system before any screen is built:

**Typography scale (minimum):**
- Display: 34px bold (hero numbers, scores)
- H1: 28px bold (screen titles)
- H2: 22px semibold (section headers)
- Body: 17px regular (default text, matches iOS body)
- Caption: 13px regular (secondary info)
- Overline: 11px medium uppercase (labels, categories)

**Color palette (minimum):**
- Primary: Main brand color
- Primary variant: Lighter/darker version for states
- Background: Main background
- Surface: Card/container background
- Text primary: Main text (87% opacity on light, 100% on dark)
- Text secondary: Supporting text (60% opacity)
- Accent: CTA buttons, key interactions
- Success: Green for positive states
- Warning: Amber for caution states
- Error: Red for errors and destructive actions

**Spacing scale:**
- Use 4px base unit: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64
- Never use arbitrary spacing values
- Consistent padding inside cards (16px minimum)
- Section spacing: 24-32px between sections

**Border radius scale:**
- Small: 8px (buttons, inputs)
- Medium: 12px (cards, containers)
- Large: 16px (modals, sheets)
- Full: 9999px (pills, avatars)

### State coverage

Every interactive element needs all states designed:

- [ ] Default state
- [ ] Pressed/active state (with haptic feedback)
- [ ] Disabled state (reduced opacity, no interaction)
- [ ] Loading state (skeleton or inline spinner)
- [ ] Success state (brief confirmation)
- [ ] Error state (with clear error message and recovery action)

Every list/feed needs:

- [ ] Loading state (skeleton screens)
- [ ] Populated state (normal)
- [ ] Empty state (illustration + message + CTA)
- [ ] Error state (retry button)
- [ ] Pull-to-refresh (custom animation)

### Haptic feedback patterns

Use Capacitor Haptics plugin (`@capacitor/haptics`). Map these interactions:

| Interaction | Haptic type | When |
|-------------|-------------|------|
| Button press | `ImpactStyle.Light` | Every primary button tap |
| Toggle switch | `ImpactStyle.Medium` | On state change |
| Achievement/milestone | `NotificationType.Success` | Score increases, streaks |
| Error/invalid | `NotificationType.Error` | Form validation, blocked action |
| Pull-to-refresh | `ImpactStyle.Light` | When threshold reached |
| Delete/destructive | `NotificationType.Warning` | Before destructive action |
| Navigation | `ImpactStyle.Light` | Tab switches (subtle) |
| Long press | `ImpactStyle.Heavy` | Context menu trigger |

### Dark mode

- [ ] Full dark mode support (not just inverted colors)
- [ ] System preference detection (respects iOS settings)
- [ ] Manual toggle in Settings
- [ ] Dark mode uses true black (#000000) for OLED battery savings
- [ ] All assets work on both light and dark backgrounds
- [ ] No hardcoded colors in components (use CSS variables or theme tokens)

### Accessibility (WCAG 2.1 AA minimum)

- [ ] All text meets 4.5:1 contrast ratio (body) or 3:1 (large text)
- [ ] Touch targets minimum 44x44pt
- [ ] All images have alt text
- [ ] Screen reader labels on all interactive elements
- [ ] Reduce Motion respected (check `prefers-reduced-motion`)
- [ ] Font scaling supported up to 200%
- [ ] No information conveyed by color alone

### Offline capability

- [ ] Service worker caches app shell and critical assets
- [ ] Core features work without internet
- [ ] Offline indicator (subtle banner, not blocking modal)
- [ ] Queued actions sync when connection returns
- [ ] No blank screens when offline

---

## 3. Onboarding flow template

Based on analysis of top-converting apps (CoinStats, Cal.ai, Headspace, Duolingo). The goal: get users to the "aha moment" fast, then monetize.

### Screen 1: Value proposition (5 seconds)

**Layout:**
- Hero illustration or animated graphic (top 50% of screen)
- Headline: One sentence, specific benefit with a number
- Subheadline: Who it's for + what changes
- "Continue" button (full width, accent color)
- Page dots at bottom (4 dots)

**Example (PrayerLock):**
- Illustration: Animated prayer scene or crescent moon
- Headline: "Never miss a prayer again"
- Subheadline: "Join 12,000+ Muslims who track all 5 daily prayers"
- Button: "Get started"

**Rules:**
- No login on this screen
- No feature lists
- One benefit, one emotion
- The illustration sets the premium tone for the entire app

### Screen 2: Personalization (15-30 seconds)

**Layout:**
- Question or prompt at top
- 3-6 selectable options (cards or chips)
- Selections animate with checkmark + color change + haptic
- "Continue" button (activates after 1+ selection)

**Example (PrayerLock):**
- "What's your prayer goal?"
- Options: "Pray all 5 daily" / "Build consistency" / "Learn prayer times" / "Track with family"
- Selection triggers `ImpactStyle.Light` haptic

**Why this matters:**
- Personalization increases paywall conversion by 20-30%
- It creates investment (sunk cost makes them less likely to leave)
- You can use their answers to customize the app experience
- It makes the paywall feel earned, not forced

### Screen 3: Social proof (5 seconds)

**Layout:**
- Large number or rating (animated counter: "47,000+ users" counting up)
- App Store rating (4.8 stars with actual star icons)
- 2-3 short testimonials (real quotes, first names, locations)
- "Continue" button

**Elements that convert:**
- Animated number counter (more impactful than static)
- Real App Store rating (even if you just launched, use beta tester feedback)
- Short quotes, not paragraphs
- Mix of demographics in testimonials

### Screen 4: Paywall (this is where the money is)

**Critical stat:** Animated paywalls convert 2.9x better than static ones.

**Layout:**
- Animated hero element (Lottie animation, not just CSS)
- Clear value proposition headline
- Plan options (2-3 plans, annual highlighted as "best value")
- Price anchoring (show weekly price for annual: "$0.57/day")
- Free trial badge (prominent, above the fold)
- "Start free trial" button (full width, accent color, animated)
- "Restore purchases" link (small, below main CTA)
- Terms link (small, bottom)

**Plan display strategy:**

| Position | Plan | Pricing | Display |
|----------|------|---------|---------|
| Left | Weekly | $2.99/week | Small card, no highlight |
| Center | Annual | $29.99/year ($0.57/day) | Large card, "BEST VALUE" badge, border highlight |
| Right | Monthly | $4.99/month | Small card, no highlight |

**Conversion tactics:**
- Annual plan in center, visually larger
- Show savings vs weekly: "Save 67%"
- Price anchoring: show per-day cost ($0.57/day vs $2.99/week)
- Animate the "Start free trial" button (subtle pulse or glow)
- Countdown timer for limited offer (use sparingly, don't be scammy)
- Trial callout: "7 days free, then $29.99/year. Cancel anytime."

**What NOT to do:**
- Don't block the entire app behind the paywall on first launch
- Don't show paywall before onboarding
- Don't use dark patterns (pre-selected expensive plan hidden in UI)
- Don't make it hard to dismiss the paywall (always have a clear close/skip option)

---

## 4. Asset generation workflow

### App icon

**Technical specs:**
- Primary: 1024x1024px (App Store)
- Additional: 180x180 (iPhone), 167x167 (iPad Pro), 152x152 (iPad)
- Format: PNG, sRGB, no transparency, no alpha, no rounded corners
- NO text in icon (Apple rejects text)
- Must be recognizable at 29x29px (notification icon size)

**Quality test:** Scale your icon to 29x29. Can you still tell what app this is? If not, simplify.

**Generation prompts (5 examples for different niches):**

**Faith app (PrayerLock):**
```
Modern 3D app icon, 1024x1024px, no text, no rounded corners.
Central element: Islamic geometric 8-pointed star with beveled metallic gold edges.
Background: gradient from deep teal (#0d9488) to lighter teal (#14b8a6).
Gold accent: #e0b87a with subtle shine.
Soft purple-tinted shadows for depth. Ambient occlusion.
Soft glow around star. Top-left light source.
Premium spiritual aesthetic. Clean precise edges.
PNG, sRGB color space, no alpha channel.
```

**Fitness app (WalkToUnlock):**
```
Modern 3D app icon, 1024x1024px, no text, no rounded corners.
Central element: Stylized 3D footprint with tread texture, angled 15 degrees for dynamism.
Background: gradient from light blue (#60a5fa) to vibrant green (#22c55e), 45 degree angle.
Footprint: solid blue (#3b82f6) with white highlights on tread ridges.
Subtle motion lines behind footprint. Energetic athletic feel.
Sharp highlights from top-right light source.
PNG, sRGB color space, no alpha channel.
```

**Sleep app (SleepMaxx):**
```
Modern 3D app icon, 1024x1024px, no text, no rounded corners.
Central element: crescent moon with 2 small stars, 3D with soft edges and gentle glow.
Background: gradient from deep midnight blue (#1e1b4b) to soft purple (#7c3aed).
Moon: soft white (#e2e8f0) with subtle blue tint and ambient shadow.
Stars: warm white with tiny glow halos. Dreamy, calming atmosphere.
Soft overhead lighting, gentle diffused shadows.
PNG, sRGB color space, no alpha channel.
```

**Productivity app (FocusLock):**
```
Modern 3D app icon, 1024x1024px, no text, no rounded corners.
Central element: bullseye target with 3 concentric rings, 3D depth between each ring.
Background: gradient from deep red (#dc2626) to bright orange (#fb923c).
Rings: alternating red (#ef4444) and orange (#f97316), center dot has white glow.
Strong directional lighting from top creating dramatic highlights.
Bold, intense, motivating feel. Geometric precision.
PNG, sRGB color space, no alpha channel.
```

**Health tracker (biomaxx):**
```
Modern 3D app icon, 1024x1024px, no text, no rounded corners.
Central element: circular progress ring at 75% completion, thick stroke, 3D beveled edges.
Background: gradient from dark navy (#0f172a) to teal (#0d9488).
Ring: cyan to green gradient (#06b6d4 to #22c55e), glowing trail at progress head.
Small sun icon inside ring, gold (#fbbf24) with subtle rays.
Clean biohacking aesthetic. Tech-forward but warm.
PNG, sRGB color space, no alpha channel.
```

### App Store screenshots

**Required device sizes:**
- 6.7" (iPhone 15 Pro Max): 1290 x 2796px - REQUIRED
- 6.5" (iPhone 14 Plus): 1284 x 2778px - maps from 6.7"
- 5.5" (iPhone 8 Plus): 1242 x 2208px - optional
- iPad Pro 12.9": 2048 x 2732px - optional but recommended

**Screenshot count:** Minimum 3, target 6, maximum 10.

**Screenshot formula (6-screenshot sequence):**

| # | Purpose | Content |
|---|---------|---------|
| 1 | Hero shot | Main app screen with headline benefit + large score/stat |
| 2 | Core feature 1 | Primary feature in action with value callout |
| 3 | Core feature 2 | Secondary feature showing depth |
| 4 | Progress/tracking | Charts, streaks, history showing long-term value |
| 5 | Social/community | Leaderboards, sharing, or social proof element |
| 6 | Paywall/pricing | Show the value they get (optional, some prefer not to show paywall) |

**Each screenshot must have:**
- Device frame (optional but recommended)
- Headline text above or below device (2-5 words)
- Subheadline (one sentence max)
- Actual app screen (not mockup, must match submitted build)
- Consistent background color/gradient across all screenshots

**Screenshot generation prompt (for AI image tools):**
```
App Store screenshot for [app name], iPhone 15 Pro Max frame.
Screen shows: [describe actual app screen].
Above device: "[Headline text]" in [font weight] white text.
Below: "[Subheadline]" in lighter weight.
Background: gradient from [color 1] to [color 2].
Style: clean, premium, Apple-quality marketing material.
1290 x 2796px, PNG.
```

### Color psychology by niche

| Niche | Primary | Secondary | Accent | Emotion |
|-------|---------|-----------|--------|---------|
| Faith | Deep teal (#0d9488) | Gold (#e0b87a) | Warm white | Spiritual, calm, premium |
| Fitness | Vibrant green (#22c55e) | Blue (#3b82f6) | Orange (#f97316) | Energy, health, movement |
| Sleep | Deep purple (#7c3aed) | Midnight blue (#1e1b4b) | Soft lavender (#c4b5fd) | Calm, dreamy, restorative |
| Productivity | Blue (#3b82f6) | White (#ffffff) | Amber (#f59e0b) | Focus, clarity, trust |
| Health/Bio | Teal (#0d9488) | Navy (#0f172a) | Cyan (#06b6d4) | Scientific, tech-forward |
| Meme/Social | Hot pink (#ec4899) | Black (#000000) | Yellow (#eab308) | Fun, viral, bold |

---

## 5. Monetization strategy matrix

### Revenue model by app type

| App type | Primary | Secondary | Tertiary | Trial | Price anchor |
|----------|---------|-----------|----------|-------|-------------|
| Utility (PrayerLock, FocusLock) | Subscription $2.99/wk or $29.99/yr | Interstitial ads (after key actions) | Affiliate links (related products) | 7-day free | "$0.57/day" |
| Tracker (Hilal, HabitForge) | Freemium + Premium $4.99/mo | Affiliate (books, supplements) | Banner ads (non-intrusive) | 3-day free | "$0.16/day" |
| Health (SleepMaxx, MealMaxx) | Subscription $49.99/yr | Affiliate (supplements, devices) | Data insights upsell | 7-day free | "$0.95/week" |
| Fitness (WalkToUnlock) | Subscription $3.99/wk | Challenge IAPs ($0.99-$4.99) | Brand partnerships | 3-day free | "$0.57/day" |
| Education (StudyLock) | Subscription $2.99/wk or $19.99/yr | Course upsells | Study material IAPs | 7-day free | "$0.38/day" |

### Subscription data (2025-2026 benchmarks)

Key numbers to internalize:

- **Weekly plans** are now the most popular plan type (~50% of all subscriptions)
- Weekly plans churn 3x faster than monthly. 65% cancel within 30 days.
- Yearly plans have highest retention: 44.1%
- Monthly retention: 17.0%
- Weekly retention: 3.4%
- **Free trial conversion average:** 24%
- Trials with credit card upfront: 43% conversion
- Trials without credit card: 14% conversion
- Trials under 4 days convert 30% worse than 4+ day trials
- After 4 days, trial length doesn't significantly affect conversion (7-day = 14-day = 30-day)
- **Animated paywalls convert 2.9x better than static**

**Recommended strategy:** Offer weekly as default display (low commitment drives trial starts), but highlight annual as "best value" (higher LTV). 7-day free trial minimum.

### RevenueCat setup checklist

- [ ] RevenueCat account created
- [ ] App configured in RevenueCat dashboard
- [ ] `@revenuecat/purchases-capacitor` installed
- [ ] `@revenuecat/purchases-capacitor-ui` installed (for paywalls)
- [ ] Products created in App Store Connect
- [ ] Products mirrored in RevenueCat dashboard
- [ ] Entitlements configured (map products to feature access)
- [ ] Offerings configured (group products for paywall display)
- [ ] Sandbox testing completed on real device
- [ ] Restore purchases verified on fresh install
- [ ] Webhook configured for server-side receipt validation (if backend exists)
- [ ] RevenueCat attribution configured (if using ads)

### Stripe integration (web version)

- [ ] Stripe account created
- [ ] Products/prices created in Stripe dashboard
- [ ] Stripe Checkout or Payment Links configured
- [ ] Webhook endpoint for subscription events
- [ ] Customer portal for subscription management
- [ ] RevenueCat Stripe integration configured (syncs both platforms)

### Apple/Google IAP compliance

- [ ] "Restore Purchases" button visible in Settings
- [ ] Subscription auto-renewal disclosure in App Store description
- [ ] Pricing shown before purchase confirmation
- [ ] Trial period clearly stated on paywall
- [ ] Cancel instructions accessible from Settings
- [ ] Link to Apple subscription management
- [ ] No language pressuring users to subscribe ("your trial is running out!" with countdown = fine. "Subscribe NOW or lose ALL your data!" = not fine)

### Paywall design patterns

**Tier 1 (highest conversion): Animated hero paywall**
- Lottie animation or video at top (2-4 seconds loop)
- 3 plan cards (weekly, annual highlighted, monthly)
- "Start free trial" as primary CTA
- 2.9x conversion vs static

**Tier 2: Feature comparison paywall**
- Free vs Premium comparison table
- Checkmarks for premium features, X for free limitations
- Good for apps with clear free tier

**Tier 3: Social proof paywall**
- User testimonials + ratings
- "Join 50,000+ users" counter
- Good for apps with existing user base

**Tier 4: Hard paywall (use sparingly)**
- No free tier at all
- Only works for apps with strong brand/word-of-mouth
- Must still offer free trial
- Cal.ai uses this model successfully

### Trial period recommendations

| App type | Recommended trial | Reasoning |
|----------|-------------------|-----------|
| Utility/habit | 7 days | User needs full week to form habit |
| Tracker | 3 days | Core value visible immediately |
| Health/fitness | 7 days | Need time to see results/data |
| Productivity | 7 days | Need full work week to evaluate |
| Education | 14 days | Learning outcomes take longer |

### Price anchoring tactics

1. **Per-day pricing:** "$0.57/day" sounds cheaper than "$3.99/week"
2. **Coffee comparison:** "Less than a coffee per week"
3. **Savings badge:** "Save 67%" on annual vs weekly
4. **Strikethrough pricing:** Show full price crossed out next to discounted trial
5. **Center bias:** Put the plan you want them to pick in the center, make it visually larger

---

## 6. Technical quality requirements

### Performance benchmarks

| Metric | Target | Reject if |
|--------|--------|-----------|
| Lighthouse Performance | > 90 | < 80 |
| Lighthouse Accessibility | > 90 | < 85 |
| Lighthouse Best Practices | > 90 | < 85 |
| Lighthouse SEO | > 90 | < 80 |
| First Contentful Paint | < 1.5s | > 2.5s |
| Time to Interactive | < 3.0s | > 5.0s |
| Largest Contentful Paint | < 2.5s | > 4.0s |
| Cumulative Layout Shift | < 0.1 | > 0.25 |
| First Input Delay | < 100ms | > 300ms |
| Total Bundle Size (PWA) | < 500KB | > 1MB |
| JavaScript Bundle | < 300KB gzipped | > 500KB gzipped |
| CSS Bundle | < 50KB | > 100KB |

### Service worker requirements

- [ ] App shell cached on install
- [ ] Static assets cached with content hashing (1-year TTL)
- [ ] API responses cached with stale-while-revalidate strategy
- [ ] Offline fallback page designed (not browser default)
- [ ] Cache version increments on deploy
- [ ] Old caches cleaned up on activation
- [ ] Background sync for queued actions (if applicable)

### Error handling

- [ ] Global error boundary catches all unhandled errors
- [ ] User-facing error messages are helpful (not "Error: undefined")
- [ ] Network errors show retry option
- [ ] Form validation shows inline errors (not alerts)
- [ ] No console.error in production (errors logged to service, not console)
- [ ] 404 states designed for missing content
- [ ] API timeout handling with retry logic

### Analytics integration

- [ ] Privacy-compliant analytics installed (Plausible, PostHog, or Mixpanel)
- [ ] Key events tracked:
  - App open
  - Onboarding completion rate (per screen)
  - Paywall view
  - Trial start
  - Subscription purchase
  - Feature usage (each core feature)
  - Retention (D1, D7, D30)
  - Churn events
- [ ] No PII in analytics events
- [ ] ATT compliance if using ad-related analytics
- [ ] Analytics dashboard configured and accessible

---

## 7. Pre-submission checklist

This is the final gate. Run through every item before clicking "Submit for Review."

### Design completeness
- [ ] All screens designed (minimum 7 unique screens)
- [ ] No placeholder content anywhere (zero "lorem ipsum", zero stock photos)
- [ ] Onboarding flow complete (4 screens: value, personalization, proof, paywall)
- [ ] Empty states designed for all lists/feeds
- [ ] Error states designed for all failure scenarios
- [ ] Loading states use skeleton screens (not spinners)
- [ ] Dark mode fully functional
- [ ] Accessibility audit passed (WCAG 2.1 AA)

### Assets
- [ ] App icon at 1024x1024 (no text, no transparency, no rounded corners)
- [ ] App icon recognizable at 29x29
- [ ] App icon generated at all required sizes (1024, 180, 167, 152)
- [ ] 6 screenshots for 6.7" display (1290 x 2796)
- [ ] Screenshots show app in use (not splash or login)
- [ ] Screenshots match submitted build exactly
- [ ] App preview video (optional but 20-30% conversion boost)

### Monetization
- [ ] RevenueCat SDK integrated and configured
- [ ] Apple IAP products configured in App Store Connect
- [ ] Paywall animated (not static)
- [ ] Free trial tested end-to-end in sandbox
- [ ] Restore purchases works on fresh install
- [ ] Subscription terms visible on paywall
- [ ] Auto-renewal disclosure in App Store description
- [ ] "Manage subscription" link in Settings

### Technical
- [ ] Lighthouse scores > 90 on all metrics
- [ ] Zero console errors in production build
- [ ] Tested on real iPhone device (not just simulator)
- [ ] Tested on 3+ screen sizes (SE, standard, Pro Max)
- [ ] Offline mode works (service worker caching)
- [ ] No memory leaks (profile in Safari Web Inspector)
- [ ] All animations 60fps
- [ ] Bundle size < 500KB

### Native features (Capacitor-specific)
- [ ] 3+ native plugins integrated and working
- [ ] Haptic feedback on all key interactions
- [ ] Push or local notifications configured
- [ ] Deep links working
- [ ] Native share sheet integrated
- [ ] No web-only UI patterns (hover states, horizontal scrollbars)
- [ ] Safe area insets respected (notch, Dynamic Island, home indicator)
- [ ] Rubber-band scrolling disabled where inappropriate

### App Store metadata
- [ ] App name final (no competitor names)
- [ ] Subtitle under 30 characters
- [ ] Keywords under 100 characters (relevant, no competitor names)
- [ ] Description complete (mentions all features, subscription terms, health disclaimers)
- [ ] Category selected (primary + secondary)
- [ ] Age rating questionnaire completed (2026 requirement)
- [ ] Privacy policy URL live and complete
- [ ] Terms of Service URL live
- [ ] Privacy Nutrition Label accurate
- [ ] Support URL provided

### Review preparation
- [ ] App Review Notes written with:
  - Step-by-step testing instructions
  - Demo account (if login required)
  - List of native features used
  - Subscription details
  - Privacy explanation
  - Health disclaimers (if applicable)
- [ ] Demo account credentials tested and working
- [ ] Backend servers confirmed running

### Post-submission
- [ ] TestFlight build tested by 2+ people
- [ ] Crash monitoring configured (Sentry or similar)
- [ ] Marketing assets prepared (Product Hunt, Twitter thread, Reddit posts)
- [ ] Launch day schedule planned
- [ ] App Store search ads budget allocated ($50-100/day test)

---

## 8. Common "AI slop" patterns to AVOID

These are the tells that instantly signal "this was vibe-coded by someone who doesn't care." Avoid all of them.

### Visual slop

| Pattern | Why it's bad | Fix |
|---------|-------------|-----|
| Generic gradient backgrounds | Looks like every AI-generated mockup ever | Use solid colors or purposeful gradients that match your design system |
| Stock photo placeholders | Screams "I didn't finish this" | Use custom illustrations, icons, or real product shots |
| Default system fonts only | San Francisco is fine, but using ONLY system font with no typographic hierarchy = lazy | Define a type scale with clear hierarchy. Consider 1 custom display font. |
| No micro-interactions | App feels dead and static | Add press states, transitions, completion animations |
| Identical layout to tutorial apps | "I followed a YouTube tutorial and shipped it" energy | Customize the layout. Rethink information architecture for YOUR use case. |
| Cookie-cutter onboarding | 3 slides with icons and "Next" buttons | Use personalization quiz, animated illustrations, social proof |
| Generic app icon (letter or emoji) | Zero brand recognition | Use AI generation with specific prompts (see Section 4) |
| No loading animations | White screens or frozen UI during data fetch | Skeleton screens, shimmer effects, branded loading animations |
| No empty state designs | "No items" text on blank white screen | Custom illustrations + helpful message + CTA to populate |
| Inconsistent spacing | Some elements have 8px margin, others 23px, others 41px | Use a spacing scale. 4px base unit. No arbitrary values. |

### Functional slop

| Pattern | Why it's bad | Fix |
|---------|-------------|-----|
| No error handling | App crashes or shows blank screen on network failure | Error boundaries, retry buttons, offline mode |
| Alert() for everything | Native alert dialogs for confirmations, errors, info | Custom modals, toast notifications, inline messages |
| No haptic feedback | App feels like a mobile website | Map haptics to all key interactions (see Section 2) |
| Console.log in production | Unprofessional, potential data leak | Remove all console statements before build |
| No analytics | Flying blind, can't optimize anything | Add privacy-compliant event tracking |
| Paywall is an afterthought | Static text list of features with a "Subscribe" button | Animated paywall with social proof, price anchoring, trial badge |
| Settings is just a list of links | Privacy policy link, terms link, that's it | Full settings with theme toggle, notification preferences, subscription management, about section |

### Copy slop

| Pattern | Why it's bad | Fix |
|---------|-------------|-----|
| AI vocabulary in app copy | "Leverage your productivity journey" gives it away instantly | Write like you're texting a smart friend |
| Generic feature descriptions | "Track your habits easily" | Specific: "Log morning sunlight in 1 tap. Get your circadian score." |
| No personality in empty states | "No data available" | "You haven't logged anything yet. Tap + to start your first entry." |
| Error messages that blame the user | "Invalid input" | "That doesn't look like an email. Check for typos?" |
| Button text that's too generic | "Submit", "OK", "Continue" everywhere | "Start tracking", "Save my progress", "See my score" |

---

## 9. Quality gate process

Before any app moves to submission, it passes through 3 gates:

### Gate 1: Design review (before any code)
- All screens designed in Figma or as component specs
- Design system defined (colors, type, spacing, radius)
- Onboarding flow mapped with copy
- Paywall designed with pricing
- All states covered (loading, empty, error, success)
- Approved by human or senior agent

### Gate 2: Build review (before TestFlight)
- All checklist items from Section 2 pass
- Lighthouse scores > 90
- Tested on real device
- Analytics tracking verified
- RevenueCat integration tested in sandbox
- Zero console errors
- **RevylAI Greenlight scan passes** (`greenlight preflight /path/to/ios/project` -- zero FAIL results)

### Gate 3: Submission review (before App Store)
- Full pre-submission checklist (Section 7) passes
- App Review Notes written
- All metadata complete
- IOS_REJECTION_PREVENTION.md checklist passes
- **RevylAI Greenlight scan passes with IPA** (`greenlight preflight . --ipa build.ipa` -- zero FAIL results, all WARN reviewed)
- TestFlight tested by 2+ people
- Marketing assets ready for launch day

No app ships without passing all 3 gates. An app that gets rejected wastes 3-7 days minimum. Getting it right before submission saves more time than it costs.

### Automated compliance scanning (RevylAI Greenlight)

RevylAI Greenlight (`https://github.com/RevylAI/greenlight`) is MANDATORY for every app before it clears Gate 2 or Gate 3. It is an open-source Apple App Store pre-submission compliance scanner that catches metadata issues, 30+ rejection-risk code patterns, privacy manifest gaps, and IPA binary problems.

**Run at Gate 2 (pre-TestFlight):**
```bash
greenlight preflight /path/to/ios/project --format json
```

**Run at Gate 3 (pre-submission, with IPA):**
```bash
greenlight preflight /path/to/ios/project --ipa build/App.ipa --format json
```

**Run across entire PRINTMAXX portfolio:**
```bash
python3 AUTOMATIONS/greenlight_checker.py --all
```

**Gate criteria:**
- Zero FAIL results at Gate 2 and Gate 3
- All WARN results reviewed and either fixed or documented
- JSON report saved for audit trail (`greenlight_report.json` in each app directory)

See `IOS_SUBMISSION_PROCESS.md` Section 3.10 for detailed Greenlight checklist and installation instructions.

---

## References

- [RevenueCat State of Subscription Apps 2025](https://www.revenuecat.com/state-of-subscription-apps-2025/)
- [Adapty - Trial Conversion Rates for In-App Subscriptions](https://adapty.io/blog/trial-conversion-rates-for-in-app-subscriptions/)
- [Adapty - State of In-App Subscriptions 2025](https://adapty.io/blog/state-of-in-app-subscriptions-2025-in-10-minutes/)
- [Business of Apps - App Subscription Trial Benchmarks 2026](https://www.businessofapps.com/data/app-subscription-trial-benchmarks/)
- [RevenueCat - Video Paywalls for Subscription Apps](https://www.revenuecat.com/blog/growth/video-paywalls/)
- [RevenueCat - Guide to Mobile Paywalls](https://www.revenuecat.com/blog/growth/guide-to-mobile-paywalls-subscription-apps/)
- [RevenueCat - Paywall Conversion Boosters](https://www.revenuecat.com/blog/growth/paywall-conversion-boosters/)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Capacitor.js Haptics Plugin](https://capacitorjs.com/docs/apis/haptics)
- [Capacitor.js Push Notifications Plugin](https://capacitorjs.com/docs/apis/push-notifications)
- [Adapty - iOS Paywall Design Guide](https://adapty.io/blog/how-to-design-ios-paywall/)

---

## EXIT VALUE MAXIMIZATION (ASO + Organic Growth + Content — Non-Negotiable)

**Source:** Real app seller post-mortem. These mistakes directly lowered their exit multiple. Every PRINTMAXX app must avoid them from Day 1.

### The 3 Valuation Killers (Avoid All Three)

**1. Over-reliance on paid ads = lower exit multiple.**
- Buyers see paid-ads-only traffic as RISKY — if you stop paying, revenue stops.
- Apps with strong organic traffic get 3-5x higher multiples than paid-only apps.
- **PRINTMAXX rule:** Every app must have organic growth BEFORE any paid spend. Use our 13 social accounts, content farm, and cross-pollination network first. Paid ads are fuel on an existing fire, not the fire itself.
- **Automation:** Content posting via Tweetlio/Fedica feeds organic downloads. Cron job: daily social posts per app using app-specific content packages.

**2. Weak ASO = leaving downloads on the table.**
- Most users discover apps by searching the App Store directly. If you don't rank for niche keywords, you're invisible.
- **PRINTMAXX rule:** Every app gets ASO optimization BEFORE submission:
  - [ ] Title includes primary keyword (e.g., "FocusLock: Focus Timer & Blocker" not just "FocusLock")
  - [ ] Subtitle uses secondary keywords (30 chars max)
  - [ ] Keyword field uses ALL 100 characters (no spaces, comma-separated, no duplicates of title words)
  - [ ] Description front-loads keywords in first 3 lines (visible before "more" tap)
  - [ ] Screenshots show features with keyword-rich captions
  - [ ] Category selection matches highest-traffic relevant category
  - [ ] Localize title/subtitle/keywords for top 5 markets (US, UK, CA, AU, DE)
- **Automation:** Build ASO keyword tracker script that monitors ranking for target keywords weekly. Track competitor keyword changes. Alert when ranking drops.

**3. Stopping content creation = organic growth dies = valuation drops.**
- The app seller stopped posting TikTok for a year. Couldn't find a creator. Organic growth flatlined. Valuation suffered.
- **PRINTMAXX rule:** Content NEVER stops. This is why we have:
  - 13 social accounts with first-week content packages already built
  - Buffer/Fedica/Tweetlio for automated posting
  - AI-generated content pipeline (carousel_factory.py, daily_research_pipeline.py)
  - Ralph loops for continuous content generation
- **For each app:** Maintain a dedicated content stream (minimum 3 posts/week about the app across relevant accounts). Use our cross-pollination network — fitness app content on @repscheme, faith app content on @selahmoments, productivity on @PRINTMAXXER.
- **Automation:** Cron job generates weekly app update/tip content from app usage data. Auto-post to relevant niche accounts.

### Organic Growth Metrics to Track Per App

| Metric | Target | Frequency |
|--------|--------|-----------|
| Organic vs paid download ratio | >60% organic | Weekly |
| ASO keyword rankings (top 5 keywords) | Top 50 | Weekly |
| Content pieces posted about app | 3+/week | Weekly |
| App Store rating | 4.5+ | Ongoing |
| Review count | 10+ in first month | Monthly |
| Referral/share rate | >5% of users share | Monthly |

### Content-to-App Flywheel (Automate This)

```
App launches
  → Content about app posted on 3+ niche accounts (automated via cron)
  → Users download from organic discovery
  → Users rate/review (in-app prompt after 3rd session)
  → Higher rating = higher ASO ranking
  → More organic downloads
  → More content about "X users, Y rating"
  → Repeat
```

This flywheel must run autonomously. No human intervention needed after initial setup. Each app's content pipeline is a cron job, not a manual task.
