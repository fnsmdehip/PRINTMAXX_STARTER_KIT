# Competitive Intelligence: Habit Tracking, Screen Time, Productivity Apps
**Date:** 2026-03-08
**Analyst:** PRINTMAXX CI Agent
**Method:** Web search, App Store data, Sensor Tower estimates, review articles, official changelogs
**Scope:** 10 named targets + new entrants + market trends

---

## 1. STREAKS (Apple) -- THREAT LEVEL: MEDIUM

| Metric | Data | Source |
|--------|------|--------|
| **Latest Version** | 11.2.0 (Jan 30, 2026) | App Store |
| **Price** | $5.99 one-time | App Store |
| **Rating** | 4.8 stars (20K+ ratings) | App Store |
| **Habit Limit** | Up to 24 tasks (was 12) | streaksapp.com |
| **Platform** | Apple only (iPhone, iPad, Watch, Mac, Vision Pro) | streaksapp.com |

**Apple Intelligence Integration (NEW -- iOS 26):**
Streaks now uses Apple's Foundation Models framework (3B parameter on-device model) to intelligently suggest and auto-categorize tasks. This is a significant AI upgrade at zero cost to users -- the on-device LLM runs locally, offline, and free. Apple specifically featured Streaks as a showcase app for their Foundation Models framework.

**What Changed Since Feb 2026:**
- Version bump from 11.0 to 11.2 (steady iteration)
- Apple Intelligence integration is the headline feature
- No pricing change (still one-time $5.99)
- No Android or cross-platform expansion

**Competitive Implication:**
Apple Intelligence gives Streaks AI features for free that competitors charge $20-40/yr for. However, it remains Apple-only, which means our PWA cross-platform approach still has a lane. The AI task suggestion feature is something we should monitor -- if it drives retention, we need an equivalent.

---

## 2. OPAL -- THREAT LEVEL: HIGH

| Metric | Data | Source |
|--------|------|--------|
| **Latest Version** | 3.151 (tracked in competitor_monitor) | COMPETITOR_CHANGES.csv |
| **Previous Version** | 3.149 | COMPETITOR_CHANGES.csv |
| **Rating** | 4.79 stars (68K+ ratings) | App Store / competitor_monitor |
| **Revenue Est** | $400K/month (~$10M ARR) | Sensor Tower / Speedinvest |
| **Team Size** | 11 people | Speedinvest |
| **Platform** | iOS + macOS only | opal.so |

**Pricing (UPDATED -- March 2026):**
Conflicting data sources. The existing COMPETITOR_REAL_DATA.md lists $99.99/yr. Current search results show:
- Annual: $239/year billed annually (a significant INCREASE from $99.99)
- Weekly: $9.99/week (~$520/yr equivalent)
- Some sources still reference $99.99/yr -- this may be a grandfathered legacy rate
- Community forum thread titles: "Pricing is too high" -- confirms user pushback on price increase

**Key Insight:** If Opal raised annual pricing from $99.99 to $239, that is a 139% price increase. This opens a massive pricing gap for alternatives. Our Vault at $19.99/yr would be 92% cheaper than Opal.

**iOS 26 / Liquid Glass:** No specific "Liquid Glass" branding found in Opal updates. iOS 26 itself introduced visual changes (Liquid Glass is the iOS 26 design language), and Opal v3.151 likely adopted the new UI paradigm. The version jump from 3.149 to 3.151 (minor) suggests incremental updates, not a major redesign.

**Active Development Signal:** HIGH. Two version bumps tracked in the last monitoring cycle.

---

## 3. BEPRESENT -- THREAT LEVEL: MEDIUM-HIGH

| Metric | Data | Source |
|--------|------|--------|
| **Latest Version** | 0.18.61 (updated Feb 19, 2026) | App Store / competitor_monitor |
| **Previous Version** | 0.18.56 | COMPETITOR_CHANGES.csv |
| **Rating** | 4.85 stars (38K+ ratings) | App Store / competitor_monitor |
| **Users** | 1M+ (claimed) | App Store marketing |
| **Price** | Free (freemium) | App Store |

**BEAST MODE Details:**
BEAST MODE is a session type that prevents users from ending a focus session early. It serves as a hard-lock commitment device -- once activated, the user cannot exit the session until the timer completes. This is a direct competitor to Opal's "Deep Focus" and our proposed Vault phone-lock mechanic.

**Group Sessions Details:**
Users can create or join group focus sessions with friends, adding social accountability. Combined with weekly leaderboards and friend challenges, this creates a social layer that most screen time apps lack.

**Growth Signal:** Still on version 0.x (pre-1.0), which means they consider themselves still in active development. Despite this, 1M+ users and 4.85 rating is strong. The version jump from 0.18.56 to 0.18.61 shows active iteration.

**Competitive Implication:** BePresent is doing exactly what we planned for Vault -- phone lock + social accountability + gamification. They have first-mover advantage with 1M users. Our differentiation needs to be sharper (Pomodoro integration, ambient sounds, or faith-specific variants).

---

## 4. SCREENZEN -- THREAT LEVEL: MEDIUM

| Metric | Data | Source |
|--------|------|--------|
| **Latest Version** | 1.2.175 (Feb 24, 2026) | App Store |
| **Price** | FREE (donation-supported, no premium tier) | screenzen.co |
| **Platform** | iOS + Android | App Store / Google Play |

**Dynamic Island Features (NEW):**
ScreenZen added Live Activity support showing the unlock countdown in Dynamic Island. Users can quickly re-lock apps with one tap from the Dynamic Island UI. This is a smart use of Apple's Live Activities API that creates constant visual friction against mindless phone use.

**Other Updates:**
- Redesigned app group settings: combine strict blocking, limits, and break times in a single group
- Daily screen time challenge re-enabled
- Shield enhancements: launch interventions directly from the shield screen
- Improved unlock flow

**Physical Product: Halo Device ($49)**
ScreenZen launched a physical companion device called "halo" for $49. This is a hardware play that no other screen time app is making.

**Competitive Implication:** ScreenZen being completely free undercuts every paid screen time app. Their business model is donation + physical hardware ($49 halo device). This makes it impossible to compete on price with ScreenZen -- differentiation must come from features, UX, or niche targeting.

---

## 5. HABITICA -- THREAT LEVEL: LOW

| Metric | Data | Source |
|--------|------|--------|
| **Price** | Free / $4.99-47.99/yr subscription | App Store |
| **Platform** | iOS + Android + Web | habitica.com |
| **Model** | Open-source, community-driven | habitica.com |

**VR Raids / AI Guild Matchmaking:**
One roundup article (gamificationplus.uk) mentions "a 2026 update included AI guild matchmaking and VR raids" for Habitica. However, NO primary source confirms this -- Habitica's own wiki, blog, and app store listing make no mention of VR or AI matchmaking. The Habitica fandom wiki shows standard guild functionality with no VR integration.

**Verdict:** The VR raids / AI guild matchmaking claim appears to be speculative or fabricated by a third-party article. Habitica's actual 2026 updates appear to be incremental (standard RPG mechanics, bug fixes). Mark this as UNVERIFIED.

**Competitive Implication:** Habitica remains the default "gamified habit" recommendation but hasn't innovated significantly. Their open-source model means slow feature development. Opportunity remains open for a modern gamified habit app.

---

## 6. HABITIFY -- THREAT LEVEL: LOW-MEDIUM

| Metric | Data | Source |
|--------|------|--------|
| **Pricing** | $4.99/mo OR $21.99-39.99/yr OR $64.99-89.99 lifetime | habitify.me / various sources |
| **Users** | 2.5M+ over 7 years | habitify.me |
| **Rating** | 4.7 stars (15K+ ratings) | App Store |
| **Platform** | iOS, Android, Mac, Web, Watch | habitify.me |

**Predictive AI Features:**
Habitify added "Smart Habit Suggestions (AI-Powered)" to help users discover new habits. However, deeper predictive AI (forecasting slumps using biometrics) is described as aspirational/future, not currently available. One review explicitly notes: "There are no AI features, no routine builder, and no way to measure whether your habits are actually driving outcomes."

**Pricing Discrepancy:** Our existing data shows $7.49/mo and $39.99/yr. Current search results show $4.99/mo and $21.99/yr. This could indicate a PRICE DECREASE (47% cut on annual), or tiered pricing with different feature sets. Needs verification.

**Competitive Implication:** If Habitify dropped prices, they're feeling competitive pressure. Their AI features are superficial. Cross-platform availability is their main strength. Our Streakr can compete on better AI + social features at equivalent or lower price.

---

## 7. FOREST -- THREAT LEVEL: MEDIUM

| Metric | Data | Source |
|--------|------|--------|
| **Latest Version** | 5.9.0 (tracked) / 5.8.0 (App Store listing) | COMPETITOR_CHANGES.csv / App Store |
| **Price (iOS)** | $3.99 one-time + Forest Plus subscription (NEW) | App Store |
| **Rating** | 4.82 stars (47K+ ratings) | competitor_monitor |
| **Users** | 4M+ active, 2M+ paying | forestapp.cc |
| **Revenue Est** | $200-500K/month | Industry estimates |
| **Trees Planted** | 1.5M+ real trees | Trees for the Future |

**2026 Updates:**
- Version jumped from 5.6.0 to 5.9.0 (3 minor versions = HIGH development signal)
- Added pause button (coffee/tea cup icon) -- addresses a top user complaint
- Improved shop navigation for challenge plants
- Multiple focus modes: Timer mode + Stopwatch mode (count-up as habit tracker)
- Enhanced App Block + Healing Sounds & Breathing added

**Forest Plus (NEW -- Critical Change):**
Forest launched a subscription tier called "Forest Plus" globally on December 9, 2025. This shifts Forest from a one-time $3.99 purchase to a freemium + subscription model. Specific subscription pricing not confirmed in search results, but this is a major business model change.

**Competitive Implication:** Forest moving to subscription validates the subscription model for focus apps. The addition of "Healing Sounds & Breathing" means Forest is expanding beyond pure focus timing into wellness -- encroaching on meditation/relaxation territory. Their rapid version iteration (3 minors in one monitoring period) shows aggressive development.

---

## 8. FINCH (Self-Care Pet) -- THREAT LEVEL: HIGH (Revenue Benchmark)

| Metric | Data | Source |
|--------|------|--------|
| **Latest Update** | Feb 26, 2026 | App Store |
| **Rating** | 4.9 stars (530K+ ratings) -- CONFIRMED 4.9, approaching 4.92 | App Store / justuseapp |
| **Downloads** | 13M+ lifetime, ~650K/month (400K iOS + 300K Android est.) | Sensor Tower / paywallscreens |
| **Revenue** | ~$1.75-3M/month ($21-36M ARR) | Sensor Tower / paywallscreens |
| **Pricing** | $9.99/mo OR $69.99/yr (Finch Plus) | finchcare.com |
| **Current Event** | "Blossoming Birbs" (March 2026 seasonal event) | App Store |

**Key Data Points:**
- One source (paywallscreens.com) headlines Finch at "$900K/mo" -- this may be iOS-only or an older snapshot
- Dan from DSfiix (Twitter/X) posted: "From 0 to $2M in 4 years" with detailed growth analysis
- Pratt IXD published a design critique of Finch in Feb 2026, indicating academic/design community attention
- PitchBook has a 2026 company profile for Finch, suggesting institutional investor interest

**New Features:**
- March event: "Blossoming Birbs" -- seasonal content keeps users engaged
- Recent updates: bug fixes and visual improvements (incremental, not major feature adds)
- Core loop unchanged: complete self-care tasks, grow pet bird, earn coins, buy accessories

**Competitive Implication:** Finch proves the virtual pet + self-care mechanic is a $20M+ ARR business. Their 4.9 rating at 530K+ reviews is nearly unprecedented retention quality. Any app we build with a companion/pet mechanic should study Finch's onboarding and reward loop.

---

## 9. ONE SEC -- THREAT LEVEL: MEDIUM-HIGH (Innovation Leader)

| Metric | Data | Source |
|--------|------|--------|
| **Price** | $2.99/mo OR $19/yr OR Family $24.99/yr | one-sec.app / App Store |
| **Lifetime** | EUR 99.99 (European pricing) | one-sec.app/store |
| **Student Discount** | 50% off | one-sec.app |
| **Platform** | iOS + Android + Desktop | one-sec.app |

**Redesigned Reflection Intervention (MAJOR UPDATE -- one sec 5.0):**
One sec completely redesigned its conversational reflection intervention with:
- **On-device LLM integration** -- uses Apple's new on-device language model to power conversational reflections
- Users now have an AI-powered conversation about WHY they're opening an app, not just a breathing exercise delay
- New "block tab" showing upcoming and past blocks at a glance
- New "tips tab" with hands-on guidance
- Completely redesigned tech stack underneath

**Why This Matters:**
One sec is the first screen time app to ship a meaningful on-device LLM feature. The reflection intervention is no longer just "breathe for 10 seconds" -- it's a personalized AI conversation about your intention. This raises the bar for the entire category.

**B2B Expansion:**
One sec now offers enterprise pricing ("for companies" page exists), indicating they're moving beyond consumer into workplace digital wellness.

**Competitive Implication:** One sec at $19/yr with on-device AI reflections is extremely competitive. Our Vault needs to differentiate on a different axis (phone locking, Pomodoro, ambient sounds) because one sec owns the "friction/intervention" mechanic with AI now.

---

## 10. NEW ENTRANTS GAINING TRACTION

### Pattrn -- WATCH CLOSELY

| Metric | Data | Source |
|--------|------|--------|
| **Type** | Discipline tracker / habit tracker with AI | pattrn.io |
| **Price** | Free for almost everything; premium for advanced AI | App Store |
| **Key Feature** | AI coach that spots patterns, dynamic goal adjustment, "alignment score" | pattrn.io |

**What Makes It Different:**
- Tracks habits, goals, AND metrics in one place, then shows correlations
- AI reviews all progress and finds hidden patterns
- Provides a single "alignment score" combining progress, precision, consistency
- Gamification: streaks, focus score, levels
- Positions itself as "the best habit tracker for 2026" in its own content marketing

**Threat Assessment:** LOW-MEDIUM. New entrant with smart positioning but unclear traction data. Worth monitoring for feature ideas (correlation tracking, alignment scores).

### BeeDone -- WATCH

| Metric | Data | Source |
|--------|------|--------|
| **Users** | 50,000+ | beedone.co |
| **Revenue** | $1K (2023 -- bootstrapped, 1 person) | getlatka.com |
| **Price** | Freemium | App Store |
| **Key Feature** | AI coaching + gamification + 3 coaching styles | beedone.co |

**What Makes It Different:**
- AI Task Splitting (breaks big tasks into smaller ones)
- Task Roulette (random task selection for decision fatigue)
- Three AI coaching styles (customizable personality)
- Full gamification: XP, levels, achievements

**Threat Assessment:** LOW. Tiny revenue, tiny team, small user base. But interesting feature ideas (Task Roulette, AI coaching styles).

### Jomo -- RISING COMPETITOR

| Metric | Data | Source |
|--------|------|--------|
| **Price** | $5.99/mo OR $29.99/yr OR $99.99 lifetime | jomo.so |
| **Student Price** | $14.99/yr | jomo.so |
| **Free Tier** | 1 session, 1 action/limit, 1 screen-time budget | jomo.so |
| **Platform** | iPhone + iPad + Mac | jomo.so |

**What Makes It Different:**
- "Inexpensive, high-quality, and feature-rich" positioning directly against Opal's high pricing
- Gallery of ready-to-use templates (one-tap setup)
- Apple Health integration
- Squads feature (social accountability)
- Plans big improvements for 2026

**Threat Assessment:** MEDIUM. Positioned perfectly in the gap between free (ScreenZen) and expensive (Opal). If Opal really raised prices to $239/yr, Jomo at $29.99 captures the price-sensitive segment.

### Refocus -- RISING COMPETITOR

| Metric | Data | Source |
|--------|------|--------|
| **Latest Version** | 2.0.26 (Feb 24, 2026) | App Store |
| **Price** | Free + IAP $7.99-$79.99 range | App Store |
| **Platform** | iOS + Android (Pomodoro version on Android) | App Store / Google Play |

**What Makes It Different:**
- "Strict Mode" with multiple unlock mechanisms (passcode, NFC tag, duration wait, copy text challenge, Pomodoro)
- Location-based blocking (home, work, school)
- Limits unblocking to 5 times/day for 25 min each with 5-min cooldown
- Detailed analytics (daily, weekly, monthly)

**Threat Assessment:** MEDIUM. Strong feature set, multiple unlock mechanisms, and the NFC tag unlock is a unique physical element.

---

## MARKET-LEVEL FINDINGS

### Global Productivity App Market
- Reached $13.15 billion in 2025
- Projected $14.46 billion in 2026 (10% YoY growth)

### Habit Tracking App Market
- Valued at $13.06 billion in 2025
- Projected $14.94 billion in 2026 (14.4% YoY growth)

### iOS 26 Screen Time Changes (Platform-Level)
- Screen Time can now FULLY BLOCK apps (previously could only set 1-min limits)
- In-app browser disabled during Downtime
- These native improvements raise the floor for what Apple provides for free, pressuring third-party screen time apps

### Key Trends (March 2026)
1. **On-device AI is the new table stakes** -- Apple Foundation Models framework gives every iOS app free access to a 3B parameter model. Streaks and one sec already shipped features using it.
2. **Subscription model spreading** -- Forest (historically one-time purchase) added Forest Plus subscription. Market consensus moving toward recurring revenue.
3. **Physical hardware companions** -- ScreenZen's $49 halo device. Physical friction devices are an emerging product category.
4. **Social accountability features** -- BePresent (Group Sessions), Jomo (Squads), Habitica (Guilds/Parties). Social layers driving retention.
5. **Price polarization** -- ScreenZen is completely free. Opal may have raised to $239/yr. The middle market ($15-30/yr) is where opportunity lives.
6. **Virtual pet mechanics validated** -- Finch at $20-36M ARR proves the companion mechanic. Habits Garden (flowers), Finch (birds), Forest (trees) all use organic growth metaphors.

---

## THREAT RANKING SUMMARY

| Rank | App | Threat Level | Reason |
|------|-----|-------------|--------|
| 1 | **Finch** | HIGH | $20-36M ARR, 4.9 stars, 650K downloads/mo. Proves the model. |
| 2 | **Opal** | HIGH | $10M ARR, 11-person team, aggressive pricing. But price increase may create backlash. |
| 3 | **one sec** | MEDIUM-HIGH | First to ship on-device LLM reflection. Innovation leader at $19/yr. |
| 4 | **BePresent** | MEDIUM-HIGH | 1M+ users, social features (Group Sessions, BEAST MODE). Doing what we planned for Vault. |
| 5 | **Forest** | MEDIUM | 4M+ users, launched subscription tier, rapid iteration (3 versions in one cycle). |
| 6 | **Streaks** | MEDIUM | Apple Intelligence integration gives free AI. Apple-only limits TAM. |
| 7 | **ScreenZen** | MEDIUM | Free kills pricing competition. Hardware play is unique. |
| 8 | **Jomo** | MEDIUM | Well-positioned in mid-price gap. Rising. |
| 9 | **Habitify** | LOW-MEDIUM | Possible price decrease signals pressure. AI features shallow. |
| 10 | **Habitica** | LOW | No major innovation. Open-source = slow iteration. |
| 11 | **Pattrn** | LOW-MEDIUM | New entrant, smart features, unclear traction. |
| 12 | **BeeDone** | LOW | Tiny ($1K revenue, 1 person). Interesting feature ideas only. |

---

## ACTIONABLE IMPLICATIONS FOR PRINTMAXX

1. **Vault (Focus/Screen Time) must differentiate on a unique axis.** BePresent owns social lock. one sec owns AI reflection. ScreenZen is free. Opal owns premium. Our angle: faith-specific focus sessions (PrayerLock crossover), Pomodoro + ambient sounds, cross-platform PWA.

2. **Consider companion/pet mechanic.** Finch's $20-36M ARR proves virtual pet + self-care is massive. If any app in our portfolio adds a companion element, it should be Streakr (habit tracking + growing companion).

3. **On-device AI features are free.** Apple's Foundation Models framework means any iOS app can add AI suggestions, categorization, and coaching at zero API cost. Build this into all apps targeting iOS.

4. **Price positioning is our strongest advantage.** If Opal is $239/yr and one sec is $19/yr, our Vault at $19.99/yr and Streakr at $14.99/yr are correctly positioned. Keep lifetime options -- subscription fatigue is the #1 complaint.

5. **Forest moving to subscription validates our model.** The one-time purchase holdout is now offering subscriptions. The market has spoken: subscription + lifetime option is the right pricing structure.

6. **Opal potential price hike is our biggest opportunity.** If confirmed at $239/yr, every "Opal alternative" keyword becomes high-intent. Build comparison landing page: "Vault vs Opal" highlighting 92% cost savings.

---

## SOURCES

- [Apple Foundation Models Framework](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/)
- [Streaks App Store](https://apps.apple.com/us/app/streaks/id963034692)
- [Opal Pricing](https://www.opal.so/pricing)
- [Opal BeTIMEful Review ($120 worth it?)](https://www.betimeful.com/blogs/opal-app-review)
- [Opal Community Forum - Pricing Too High](https://community.opal.so/t/pricing-is-too-high/3246)
- [BePresent App Store](https://apps.apple.com/us/app/bepresent-screen-time-control/id1644737181)
- [BePresent Rich on Tech Interview](https://richontech.tv/p/interview-how-an-app-called-bepresent)
- [ScreenZen Official](https://screenzen.co/)
- [ScreenZen Halo Device](https://screenzen.co/products/halo)
- [Habitica G2 Reviews 2026](https://www.g2.com/products/habitica-habitica/reviews)
- [Habitify Pricing](https://habitify.me/pricing)
- [Habitify Review 2026 (CRM.org)](https://crm.org/news/habitify-review)
- [Forest App Store](https://apps.apple.com/us/app/forest-focus-for-productivity/id866450515)
- [Forest Plus Help](https://help.forest.me/en/articles/542-how-does-the-forest-plus-subscription-work)
- [Finch App Store](https://apps.apple.com/us/app/finch-self-care-pet/id1528595748)
- [Finch Paywall Screens ($900K/mo)](https://www.paywallscreens.com/apps/finch-mobile-paywall-c882)
- [Finch PitchBook Profile](https://pitchbook.com/profiles/company/493905-97)
- [Dan DSfiix on Finch Growth](https://x.com/dailystartupfix/status/1921942935446175875)
- [one sec Official](https://one-sec.app/)
- [one sec Pro Features](https://tutorials.one-sec.app/en/articles/3036418)
- [one sec Interventions](https://tutorials.one-sec.app/interventions)
- [Pattrn Official](https://pattrn.io/)
- [BeeDone Official](https://beedone.co/en/)
- [BeeDone Revenue (Latka)](https://getlatka.com/companies/what-is-beedone.web.app)
- [Jomo Pricing](https://jomo.so/pricing)
- [Refocus App Store](https://apps.apple.com/us/app/refocus-block-apps-websites/id1645639057)
- [Best Habit Trackers 2026 (Beyond Time)](https://beyondtime.ai/blog/best-habit-tracker-apps-2026-compared)
- [Best Habit Trackers 2026 (Reclaim)](https://reclaim.ai/blog/habit-tracker-apps)
- [Best Screen Time Apps 2026 (Refocus)](https://www.refocusapp.co/articles/best-screen-time-apps-for-iphone)
- [iOS 26 Screen Time Changes](https://www.techlockdown.com/articles/ios-26-screen-time-changes)
- [Productivity App Trends 2026 (Forem)](https://future.forem.com/matt_iscanner/7-productivity-app-trends-in-2026-59a7)
- [Gamified Habit Apps 2026 (Gamification+)](https://gamificationplus.uk/which-gamified-habit-building-app-do-i-think-is-best-in-2026/)
- [Habit Tracking Market Size (Straits Research)](https://straitsresearch.com/report/habit-tracking-apps-market)
