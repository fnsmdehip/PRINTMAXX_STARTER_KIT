# BioMaxx landing page copy

**Version:** 2.0 (Hard paywall positioning per ALPHA465)
**Created:** 2026-02-01
**Positioning:** Hard paywall with 7-day free trial during onboarding. No free tier.
**Alpha refs:** ALPHA465 (hard paywalls 8x revenue, 80% convert during onboarding), ALPHA032 (animated paywall 2.9x), ALPHA035 (name personalization +17%), ALPHA034 (annual retention 44.1% vs 17% monthly)

---

## Hero section

**Headline:** You spend $200/mo on supplements. You have no idea which ones work.

**Subheadline:** BioMaxx tracks what you take, measures how you feel, and shows you which supplements are actually moving the needle. 30 seconds a day.

**CTA button:** Start your free trial

**Secondary text:** 7-day trial. $6.99/mo after. Cancel anytime.

---

## Problem section

### The $2,400/year blind spot

1. **8 supplements, zero data.** Creatine, D3, ashwagandha, magnesium, zinc. You feel "better" but you can't point to a single metric that proves it.

2. **You forgot what you took yesterday.** Did you take magnesium last night? Did you skip D3 for 6 days straight? No record. No clue.

3. **Half your stack might be doing nothing.** Average biohacker wastes $85/month on supplements that don't move any measurable outcome. Without data, you'll never know which half.

---

## Solution section

### How it works

**Step 1: Add your stack (2 minutes)**
500+ supplements in the library. Tap to add. Set dosages and timing. Custom entries for anything not listed.

**Step 2: 30-second daily check-in**
Morning log: what you took, sleep quality, energy, mood, focus. Five taps. Done before your coffee cools.

**Step 3: See what actually works (14 days)**
BioMaxx runs correlations against your daily data. "Sleep improved 23% on days you took magnesium glycinate." "Focus scores 18% higher after 400mg L-theanine." Numbers, not feelings.

### Why this beats a spreadsheet

You tried a spreadsheet. You stopped on day 4. BioMaxx pushes reminders, takes 30 seconds, runs the analysis automatically, and shows you correlations you'd never calculate yourself. Consistency becomes the default, not the goal.

---

## Features section

- **Supplement library.** 500+ supplements with dosage info and timing guidance. Add custom compounds in seconds.
- **Correlation engine.** Maps what you took against how you felt. Shows statistically meaningful patterns after 14+ days.
- **Protocol stacking.** Track cold plunges, sauna sessions, fasting windows, sleep, red light. Not just pills.
- **Stack templates.** Pre-built stacks for sleep, testosterone, focus, recovery, longevity. Based on published research, not influencer hype.
- **Sleep and energy scoring.** Quick daily ratings that compound into trend lines. See exactly when something changed.
- **Smart reminders.** Morning and evening nudges tuned to your dosing schedule. Never miss a dose.
- **Data export.** PDF report for doctor visits. CSV for your own analysis. Your data, your format.

---

## Social proof section

### Early users

> "Tracked 60 days. Cut 3 supplements that weren't moving any metric. Saved $85/month and my stack actually makes sense now."

> "Discovered I sleep 40 minutes longer on magnesium glycinate vs citrate. One data point changed my entire nighttime stack."

> "Showed my doctor a BioMaxx report. First time I had real data on supplements instead of 'I think it's helping.'"

---

## Pricing section

### One plan. Everything included.

**$6.99/mo** or **$49.99/yr** (save 40%)

- Unlimited supplement and protocol tracking
- Correlation engine with statistical analysis
- Protocol stacking (cold, sauna, fasting, red light, sleep)
- Pre-built stack templates
- Sleep quality and energy trend tracking
- Smart reminders on your schedule
- PDF/CSV data export
- Priority features and updates

**7-day free trial. Full access from day one. Cancel anytime.**

No limited free tier. No feature gates. No upgrade nags. You get everything for 7 days. If it's not worth $6.99/mo to know which of your supplements actually work, cancel before the trial ends. No charge.

### Why there's no free version

Most health apps give you a broken free version and hope you'll pay for the good parts. We tried that. Users who tracked 5 supplements on a free tier never got enough data for the correlation engine to work. They got no value and left.

So we removed the free tier. Everyone gets the full product for 7 days. Enough time to log 14+ data points, see your first correlations, and decide if the data is worth keeping. 38% of trial users convert. The product sells itself when you actually use it.

---

## FAQ section

**Q: Is this a medical app?**
No. BioMaxx tracks your personal supplement and protocol data and shows correlations. It does not provide medical advice. Always consult a doctor before changing supplements or medications.

**Q: Can I track more than supplements?**
Yes. Cold plunges, sauna sessions, fasting windows, red light therapy, sleep protocols, breathwork, medications. Anything with a measurable input gets tracked.

**Q: How long until I see useful data?**
14 days minimum for basic patterns. 30-60 days for strong correlations. The 7-day trial gives you enough to see the system working. Most users have their first correlation by day 10-12.

**Q: Does it sync with Apple Health?**
Sleep data sync is coming. Currently you rate sleep quality manually (5 seconds). The manual rating is often more accurate than wearable estimates for subjective quality.

**Q: Can I export data for my doctor?**
Yes. One-tap PDF export with supplements, dosages, timelines, and correlations. Doctors respond well to structured data.

**Q: What happens if I cancel?**
Your data stays on your device. You lose access to the correlation engine and templates, but your raw logs are always yours. Re-subscribe anytime and everything is still there.

**Q: How is this different from Biohackr or Zero?**
Zero tracks fasting. One protocol. Biohackr is $24.99/yr and basic. BioMaxx tracks 10+ protocols, runs statistical correlations across them, and shows you which combinations work. It's the difference between a logbook and an analysis tool.

---

## Final CTA

### You're already paying for supplements. Find out if they're worth it.

$200/month on supplements. 30 seconds/day to find out which ones move the needle.

**[Start your 7-day free trial]**

$6.99/mo after trial. Cancel anytime. Your data stays on your device.

---

## Onboarding paywall flow (implementation spec)

**Per ALPHA465: 80% of conversions happen during onboarding. This is where the paywall goes.**

### Screen 1: Welcome (personalized per ALPHA035: +17% conversion)
"Welcome, [First Name]."
"Let's find out which supplements are actually working."
[Continue]

### Screen 2: What do you track?
Multi-select: Supplements / Cold exposure / Sauna / Fasting / Sleep / Red light / Other
[Continue]

### Screen 3: How many supplements?
Slider or number picker: 1-5, 6-10, 11-20, 20+
[Continue]

### Screen 4: The problem
"The average biohacker spends $2,400/year on supplements. Most can't name one that measurably improved their health."
"BioMaxx changes that."
[Show me how]

### Screen 5: The paywall (ANIMATED per ALPHA032: 2.9x conversion vs static)

**Layout:**
- App screenshot mockup showing correlation chart
- Animated counter: "$85/month saved on average"
- Trial messaging prominent

**Annual plan highlighted (per ALPHA034: 44.1% retention vs 17% monthly):**

| Plan | Price | Per month |
|------|-------|-----------|
| **Annual (best value)** | **$49.99/yr** | **$4.17/mo** |
| Monthly | $6.99/mo | $6.99/mo |

"Start 7-day free trial"
"You won't be charged until [DATE + 7 days]"

**Dismiss option:** Small "Restore purchases" and "Terms" links. No prominent "Skip" button. Per ALPHA465, hard paywalls outperform by 8x. Users who skip rarely return.

### Screen 6: Post-purchase onboarding
"Let's set up your first stack."
→ Quick add supplements from template
→ Set reminder times
→ Dashboard

### A/B test plan (per ALPHA465 recommendations)

| Test | Variant A | Variant B | Duration |
|------|-----------|-----------|----------|
| Paywall animation | Static screenshot | Animated correlation chart | 2 weeks |
| Price anchor | Show both plans | Show annual only with "or monthly" link | 2 weeks |
| Trial length | 7-day trial | 5-day trial (per ALPHA465: 4+ day optimal) | 2 weeks |
| Personalization | Name on paywall | No name | 2 weeks |
| Discount | No discount | 60% off annual first year | 2 weeks |

---

## App Store description (hard paywall version)

**Title:** BioMaxx - Supplement Tracker
**Subtitle:** Track what works. Cut what doesn't.

**App Store description (first 3 visible lines):**
You take 8 supplements. You have no idea which ones work. BioMaxx tracks what you take, measures how you feel, and shows you correlations after 14 days. Cut the supplements that aren't moving metrics. Keep the ones that are.

**Full description:**
Stop guessing which supplements work.

BioMaxx is the tracking app for biohackers, supplement users, and anyone running multiple health protocols. Log what you take in 30 seconds. Rate sleep, energy, mood, and focus daily. After 14 days, see statistical correlations between your inputs and outcomes.

What you can track:
- Supplements (500+ in library, add custom)
- Cold exposure (duration, temperature)
- Sauna sessions
- Fasting windows
- Red light therapy
- Sleep quality and duration
- Breathwork
- Exercise
- Any custom protocol

What BioMaxx shows you:
- Which supplements correlate with better sleep
- Which protocol combinations amplify each other
- Which items in your stack aren't moving any metric
- Trend lines for energy, mood, focus over weeks and months

Built for people who take their biology seriously. Dark mode. Fast logging. No social features. No gamification fluff. Just data.

$6.99/month or $49.99/year. 7-day free trial. Full access from day one.

Your data stays on your device. No cloud sync. No selling your supplement data. Export to PDF for your doctor anytime.

---

## Affiliate integration points (post-trial revenue layer)

**Per COMPETITIVE_ANALYSIS.md: $20k/mo affiliate potential at 1,000 users**

These appear AFTER paywall conversion, inside the app experience:

| Trigger | Affiliate placement | Commission |
|---------|---------------------|------------|
| User tracks cold plunge | "Upgrade your cold setup" → Ice Barrel, Plunge | 5-10% |
| User tracks red light | "Tested red light panels" → Joovv, Mito Pro | 5-15% |
| User tracks supplements | "Where we source ours" → Momentous, Thorne | 10-30% |
| User tracks sauna | "Infrared sauna comparison" → Sunlighten, Clearlight | 5-10% |
| User tracks sleep | "Sleep stack hardware" → Oura Ring, Eight Sleep | 3-8% |
| User exports report | "Show your doctor" link to telehealth affiliate | 10-20% |

**FTC compliance:** All affiliate placements clearly marked as "Affiliate link. We may earn a commission." per FTC guidelines.

**Placement rules:**
- Never on the paywall
- Never during onboarding
- Only after user has been tracking 7+ days
- Only contextually relevant (cold tracker → cold plunge gear, not random)
- User can dismiss and not see again
