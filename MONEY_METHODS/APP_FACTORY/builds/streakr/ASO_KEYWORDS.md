# Streakr — ASO Keywords & Pricing Config
generated: 2026-03-29

## App Store Metadata

**Name:** Streakr: Swipe Habits That Stick
**Subtitle (30 chars):** One swipe. Real streaks. No fluff.
**Category:** Health & Fitness
**Secondary category:** Productivity
**Age rating:** 4+

---

## Primary Keywords (App Store Search Ads + keyword field)

Tier 1 — Direct intent (highest conversion):
- habit tracker app
- streak tracker
- daily habit app
- simple habit tracker
- habit streak counter

Tier 2 — Competitor displacement:
- habit tracker no account
- offline habit tracker
- private habit app
- habit app no subscription required (ironic — show ours IS worth it)
- swipe habit tracker

Tier 3 — Adjacent intent:
- minimum viable day app
- daily routine tracker
- productivity streak app
- accountability app
- 3 habits tracker

Tier 4 — Long tail (App Store keyword field):
habit,streak,tracker,daily,routine,offline,private,swipe,simple,mvd,accountability

---

## App Store Description (first 252 chars shown before "more")

"The habit app for people who hate habit apps. Pick 3 non-negotiables. Swipe to complete. No account. Nothing leaves your device. That's a win."

---

## Full App Store Description

**Streakr — Swipe Habits That Stick**

Stop downloading habit apps and quitting after 3 days.

Streakr is different: one swipe per habit, three non-negotiables, and a satisfying daily win. No 10-step systems. No productivity cult. Just the habits you actually want to keep.

**Why people quit habit apps:**
- Too many features
- Feels like homework after a week
- Account required before you can do anything
- Shame when you miss a day

**How Streakr fixes all of that:**

✓ Swipe up to complete — like clearing a notification, but for your habits
✓ Minimum Viable Day mode — define your 3 non-negotiables, declare a win when all 3 are done
✓ Zero account required — open the app and start on Day 1 immediately
✓ Nothing leaves your phone — all data stored locally, zero servers
✓ Streak repair (Pro) — forgive one slip per 30-day window, stay motivated

**Features:**
• Swipe-to-complete habit cards with satisfying haptic feedback
• Minimum Viable Day mode — the viral framework for people who hate streaks
• Progress heatmap — GitHub-style 30-day view per habit
• Milestone rewards at 3, 7, 14, 30, 90, 180, 365 days
• Habit packs — Morning Routine, Deep Work, Fitness, Mindfulness (Pro)
• Share milestone cards — organic growth trigger at key streaks
• Works offline — zero internet required after install

**Streakr Pro — $29.99/year (7-day free trial)**
• Unlimited habits (free tier: 3 habits)
• Streak repair — 1 forgiveness per 30 days
• Milestone sharing cards
• Habit packs (5 pre-built collections)
• Full history export (CSV)

Streakr is not Fabulous. It's not designed to upsell you a life coaching program or send you 8 notifications per day. It's a quiet app that makes one daily check-in feel satisfying instead of shameful.

---

## Screenshots Spec (6 required for App Store, 6.9" iPhone 16 Pro Max)

1. **Hero** — Main screen with 3 habit cards, mid-swipe animation on Exercise card
   Caption: "One swipe. Day counted."

2. **Completion** — All 3 cards completed, green glow, confetti animation
   Caption: "Daily win. See you tomorrow."

3. **MVD Mode** — MVD section visible, 2/3 goals checked, gold badge
   Caption: "Minimum Viable Day. Define your 3."

4. **Streak History** — Progress tab, 30-day heatmap with 19-day streak
   Caption: "Watch your streaks grow."

5. **Milestones** — Progress screen, 30d and 7d milestone badges achieved
   Caption: "14 milestones. Every one earned."

6. **Paywall** — Annual plan selected, 7-day trial highlighted
   Caption: "7 days free. Keep every streak."

---

## Pricing Configuration

| Plan | Price | Trial | App Store product ID |
|------|-------|-------|----------------------|
| Annual | $29.99/yr | 7 days | streakr.pro.annual.2999 |
| Monthly | $4.99/mo | None | streakr.pro.monthly.499 |

**Pricing rationale:**
- Annual at $29.99 = $2.50/mo — cheaper than a coffee, positioned as "impulse buy" tier
- HabitSwipe reference: $800 at 2.5K users = $0.32/user. Streakr targets $15+ LTV via annual
- Test sequence: start $29.99/yr → if <5% trial start rate, test $19.99/yr → if strong, test $39.99/yr

**Stripe Payment Links (create in Stripe dashboard):**
- Annual: https://buy.stripe.com/[CREATE_LINK] → product: Streakr Pro Annual, $29.99
- Monthly: https://buy.stripe.com/[CREATE_LINK] → product: Streakr Pro Monthly, $4.99

---

## A/B Tests to Run at 200 Installs

| Test | Variant A | Variant B | Metric |
|------|-----------|-----------|--------|
| Paywall timing | After 5 completions | After onboarding exit | Trial start rate |
| Price | $29.99/yr annual | $19.99/yr annual | Trial conversion |
| Onboarding length | 5 screens (current) | 3 screens (fast path) | Day-3 retention |
| Review prompt | Day 3 streak | Day 7 streak | App Store rating |

---

## Reddit Launch Copy

**r/productivity post (mirror HabitSwipe strategy):**

Title: "I quit every habit app after 3 days. So I built one that makes that impossible."

Body: "I've downloaded Streaks, Habitica, Fabulous, Done, Streaks (the other one), and about 8 others. I quit all of them by day 3. Not because they were bad — because they required too much. Too many habits. Too many prompts. Too much shame when I missed.

So I built Streakr. One swipe per habit. Three non-negotiables. If all 3 are done, the day is a win. No account. Everything stays on your phone.

Built it for myself last month. Putting it out there in case it helps anyone else who's given up on habit apps: [streakr.surge.sh]"

**r/nosurf / r/getdisciplined variant:**
Focus on the "no account, nothing leaves your device" privacy angle — resonates strongly with these communities.

---

## Distribution Checklist

- [ ] Deploy: `surge MONEY_METHODS/APP_FACTORY/builds/streakr/ streakr.surge.sh`
- [ ] Post on r/productivity with "built for myself" narrative
- [ ] Post on r/habittracking
- [ ] Reply to "best habit app" threads in r/selfimprovement, r/nosurf, r/getdisciplined
- [ ] Twitter thread: "Stop tracking 10 habits. Define your minimum viable day instead."
- [ ] Cross-link from SoberStreak and Scripture Streak landing pages
- [ ] Add to OPS/DEPLOYMENT_URLS.md after deploy
- [ ] Submit to Product Hunt (after App Store listing is live)
- [ ] Create Stripe payment links and replace placeholder URLs in index.html
