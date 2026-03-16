# App Spec: Scripture Streak — AI Chat Layer + Paywall Overhaul
## candidate: ALPHA_BIBLECHAT_001
## target: app factory/scripture-streak
## generated: 2026-03-16
## roi_potential: HIGHEST
## score: 179
## execution_lane: ITERATE_EXISTING_NOW
## status: READY_TO_BUILD

---

## Why This Now

BibleChat (Romanian 2-man team) hit $750K/mo net in March 2025 with this exact pattern:
- AI chat on scripture corpus
- 3-tier paywall with weekly anchor
- Character persona TikTok (1 video: 60M views)

Scripture Streak already has:
- React Native/Expo codebase with full tab nav
- `ai-helper.ts` with OpenRouter/DeepSeek integration
- Paywall screen (demo mode, RevenueCat commented out)
- Onboarding, streak tracking, Bible reader

**The gap is 3 things.** Nothing else matters right now.

---

## Gap Analysis: What's Missing vs BibleChat Pattern

| Gap | Current State | Required State |
|-----|--------------|----------------|
| AI Chat UI | `askBibleQuestion()` function exists, no chat screen | Dedicated chat tab with conversation history, persona |
| Paywall pricing | $0.99/mo + lifetime, ad-free model | $4.99/wk anchor, $12.99/mo, $59.99/yr, 7-day trial |
| RevenueCat | Commented out (demo mode) | Live — blocks all revenue |
| Review prompt | None | Post-7-day-streak milestone trigger only |

---

## Build Scope (Minimum Viable Iteration)

### 1. AI Chat Screen (`app/(tabs)/chat.tsx`)

**What it does:**
- Persistent conversation with a named persona ("Grace" for the generic build, denomination-specific names later)
- Each message in context of: current day's verse + user's streak count
- Pre-seeded conversation starters: "What does this verse mean for my life?", "Help me understand [reference]", "I'm struggling with faith today"
- Streaming responses (show typing indicator, then stream text)
- Conversation history stored locally (AsyncStorage, last 20 messages)
- Free tier: 3 AI messages/day before paywall gate
- Premium: unlimited

**Persona system prompt:**
```
You are Grace, a warm and knowledgeable Bible study companion. You help Christians understand Scripture deeply and apply it to their daily lives. You speak with warmth but precision. You reference specific verses. You are not a pastor — you are a study partner. Keep responses to 2-3 paragraphs unless the user asks for more. Today's focus verse is: {verse}. The user has maintained a {streak}-day streak.
```

**UI requirements:**
- Dark background (midnight blue: `#0F1729`)
- User messages: right-aligned, warm gold pill (`#D4AF37` bg, white text)
- AI messages: left-aligned, card with subtle border (`#1E2D50` bg)
- Persona avatar: small circular icon (letter "G" or flame icon)
- Input bar pinned to bottom, keyboard-aware
- Free tier indicator: "2 of 3 free messages used today" below input

**Files to create/modify:**
- `app/(tabs)/chat.tsx` — new chat screen
- `app/(tabs)/_layout.tsx` — add chat tab (message-bubble icon)
- `src/lib/ai-chat.ts` — chat history management, persona config, daily limit tracking
- `src/lib/ai-helper.ts` — extend `askBibleQuestion` to support streaming + persona

---

### 2. Paywall Overhaul (`app/paywall.tsx`)

**Pricing structure (matches BibleChat):**

| Plan | Price | Display |
|------|-------|---------|
| Weekly | $4.99/wk | Anchor plan — shown first |
| Monthly | $12.99/mo | Middle option |
| Annual | $59.99/yr | "Best value" — $1.15/wk |

**7-day trial on annual plan only.** No lifetime option (removes one-time payment drain on LTV).

**Paywall trigger logic:**
- Show after user taps AI chat for the 4th time (not on app open, not during onboarding)
- Soft paywall: small "Maybe Later" text link at bottom (de-emphasized, small font)
- No fake countdown timers

**RevenueCat product IDs to create:**
- `scripture_weekly_499`
- `scripture_monthly_1299`
- `scripture_annual_5999` (with 7-day free trial)

**Entitlement:** `premium`

**Files to modify:**
- `app/paywall.tsx` — full pricing overhaul
- `src/lib/purchases.ts` — uncomment RevenueCat, wire up 3 packages
- Remove ad-based free tier (no more AdBanner dependency on paywall)

**RevenueCat setup steps (human action required):**
1. Create RevenueCat account + app at app.revenuecat.com
2. Add iOS app (bundle ID from `app.json`)
3. Create 3 products in App Store Connect, then in RevenueCat
4. Set `EXPO_PUBLIC_REVENUECAT_IOS_KEY` in env
5. Uncomment `import { makePurchase, getOfferings } from '../src/lib/purchases'` in paywall

---

### 3. Post-Value Review Prompt

**Trigger:** User completes 7-day streak (day 7 check-in)

**Logic in `src/lib/notifications.ts`:**
```typescript
export async function checkReviewMilestone(currentStreak: number): Promise<void> {
  if (currentStreak === 7) {
    // Fire iOS review request via expo-store-review
    // Only once ever — store flag in AsyncStorage
    const alreadyRequested = await AsyncStorage.getItem('review_requested');
    if (!alreadyRequested) {
      await StoreReview.requestReview();
      await AsyncStorage.setItem('review_requested', 'true');
    }
  }
}
```

Fire this from `app/(tabs)/index.tsx` after streak increment.

---

## Tab Layout Change

Current tabs: Home | Bible | Progress | Share | Settings

New tabs: Home | Bible | Chat (AI) | Progress | Settings

Remove Share tab (low value, replaced by AI chat). This follows BibleChat's pattern of making AI the center of the experience.

---

## Monetization Config

```
Primary: RevenueCat subscription ($59.99/yr annual = $5/mo effective)
Paywall trigger: 4th AI message
Trial: 7-day on annual plan
Review prompt: day-7 streak milestone
```

**Revenue math at BibleChat's 1-2% conversion:**
- 1,000 downloads → 10-20 paying users
- Average $30/yr (mix of plans) → $300-600/mo per 1,000 downloads
- Need ~3,300 downloads/mo to hit $1K MRR

---

## ASO Keywords for This Build

Primary: `bible study ai`, `scripture chat`, `daily bible devotional`
Long-tail: `bible verse explainer app`, `christian ai companion`, `daily devotional streak`
Category: Books & Reference (not Lifestyle — less competition, matches BibleChat)

---

## Growth Hook (Post-Build)

Character persona TikTok account: "GraceStudies" or similar
- Post format: Screen recording of AI chat answering a hard Bible question
- Hook: "I asked an AI about [controversial Bible topic] and..."
- Start organic, scale winners as paid

---

## Build Sequence

1. `src/lib/ai-chat.ts` — history, persona, daily limit
2. `app/(tabs)/chat.tsx` — chat UI
3. `app/(tabs)/_layout.tsx` — add chat tab
4. `app/paywall.tsx` — pricing overhaul
5. `src/lib/purchases.ts` — uncomment RevenueCat (human sets API key)
6. `app/(tabs)/index.tsx` — add review milestone check

**Estimated build time:** 1 session (4-6 hours)

---

## Human Blockers (required before revenue flows)

| Action | Time | Unlocks |
|--------|------|---------|
| Create RevenueCat account | 15 min | Paywall goes live |
| Create 3 App Store Connect products | 30 min | IAP available |
| Set `EXPO_PUBLIC_REVENUECAT_IOS_KEY` in env | 5 min | Purchases SDK activates |
| App Store Connect developer account (if not yet) | varies | Submission |

---

## Success Metrics

| Metric | Target | Timeframe |
|--------|--------|-----------|
| AI chat sessions/day | >50% of DAU | Week 1 |
| Paywall view rate | >30% of users | Week 1 |
| Trial start rate | >10% of paywall views | Week 2 |
| Trial-to-paid conversion | >40% | Week 4 |
| App Store rating | >4.5 via milestone prompt | Month 1 |

---

## Files To Create

- `app/(tabs)/chat.tsx`
- `src/lib/ai-chat.ts`

## Files To Modify

- `app/(tabs)/_layout.tsx` (add chat tab)
- `app/paywall.tsx` (full pricing overhaul)
- `src/lib/purchases.ts` (uncomment RevenueCat)
- `app/(tabs)/index.tsx` (review milestone hook)
- `src/lib/notifications.ts` (add checkReviewMilestone)

---

## Next Step

Build step: `app/(tabs)/chat.tsx` + `src/lib/ai-chat.ts`
Then: paywall overhaul
Then: wire review prompt

**Blocker before ship:** RevenueCat account + App Store products (human action, ~45 min total)
