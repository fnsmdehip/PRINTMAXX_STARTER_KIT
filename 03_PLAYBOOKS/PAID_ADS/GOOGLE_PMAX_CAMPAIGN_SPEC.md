# Google Ads Performance Max (PMax) campaign structure spec

Built from ALPHA972901 (Cody Schneider $1M ARR with 2 channels, 60% CPA decrease via structured testing), SYN033 (2-Channel Focus Revenue Engine, score 96), Day 5 priorities (PMax as revenue channel #3 at $100/mo test budget).

**Bottom line:** PMax is Google's AI-driven campaign type that runs across Search, Display, YouTube, Gmail, Maps, and Discover simultaneously. Google's AI optimizes creative combinations, bidding, and audience targeting. Our role: feed it good assets, set clear goals, and kill losers fast. $100/mo test budget. Day 7 kill threshold. 2x scale winners.

---

## Why PMax over standard Google campaigns

| Factor | Standard Search | PMax | Winner |
|--------|----------------|------|--------|
| Reach | Search only | Search + Display + YouTube + Gmail + Maps + Discover | PMax |
| Targeting | Manual keywords | AI audience signals + automated | PMax |
| Creative | Text only (Search) | Text + image + video combinations | PMax |
| Optimization | Manual bidding | AI bidding to goal (CPA/ROAS) | PMax |
| Setup effort | High (keyword research, match types) | Low (assets + signals + goal) | PMax |
| Control | Full | Limited (black box AI) | Standard |
| Data need | Low | High (needs conversion data to optimize) | Standard |
| Min budget | $5/day | $20-50/day effective minimum | Standard |

**Decision:** PMax for app installs and info product sales. Standard Search only for branded terms or very specific high-intent keywords where we want full control.

---

## Campaign architecture

```
ACCOUNT STRUCTURE
Google Ads Account (linked to Google Play + Firebase)
    ↓
CAMPAIGN 1: PMax - Lock Apps (App Installs)
    - Asset Group 1: PrayerLock (faith audience)
    - Asset Group 2: WalkToUnlock (fitness audience)
    - Asset Group 3: StudyLock (student audience)
    - Asset Group 4: biomaxx (self-improvement audience)
    ↓
CAMPAIGN 2: PMax - Digital Products (Lead Gen / Sales)
    - Asset Group 1: Paywall Playbook ($27)
    - Asset Group 2: Cold Email SOP ($12)
    - Asset Group 3: Clipping Army Guide ($37)
    ↓
CAMPAIGN 3: PMax - Services (Lead Gen)
    - Asset Group 1: Content distribution setup ($500-1,500)
    - Asset Group 2: Cold outbound setup ($1,000-2,000)
```

**Why separate campaigns per goal (not one mega campaign):**
- Different conversion actions per campaign (install vs purchase vs lead)
- Different budget allocation (apps get more because LTV is higher)
- Easier to kill underperformers without affecting winners
- Cleaner data for optimization decisions

---

## Phase 1: Account setup (Day 1)

### Prerequisites

- [ ] Google Ads account created (ads.google.com)
- [ ] Google Play Console linked (for app campaigns)
- [ ] Firebase SDK installed in all apps (conversion tracking)
- [ ] Google Analytics 4 property linked
- [ ] Conversion actions configured (see below)
- [ ] Payment method added ($100 initial deposit)

### Conversion tracking setup

**For apps (Firebase):**

```
Event: first_open           → Track as conversion
Event: in_app_purchase      → Track as conversion, assign value
Event: subscription_start   → Track as conversion, assign value ($4.99/mo or $29.99/yr)
Event: paywall_view         → Track as micro-conversion (don't optimize toward)
Event: onboarding_complete  → Track as micro-conversion
```

**For digital products (website):**

```
Event: purchase             → Track as conversion, assign value ($12-$37)
Event: add_to_cart          → Track as micro-conversion
Event: begin_checkout       → Track as micro-conversion
Event: page_view /thank-you → Track as conversion (backup)
```

**For services (lead gen):**

```
Event: form_submit          → Track as conversion
Event: calendly_booked      → Track as conversion (highest value)
Event: phone_click          → Track as conversion
```

### Budget allocation ($100/mo initial)

| Campaign | Daily Budget | Monthly | Rationale |
|----------|-------------|---------|-----------|
| Lock Apps (installs) | $2/day | $60/mo | Highest LTV potential ($29.99-$49.99/yr) |
| Digital Products (sales) | $1/day | $30/mo | Immediate revenue, low LTV |
| Services (leads) | $0.33/day | $10/mo | Highest per-lead value, lowest volume |

**Note:** $100/mo is bare minimum test budget. PMax needs conversion data to optimize. Below ~20 conversions/month, the AI won't have enough signal. Expect 2-4 weeks of learning phase.

---

## Phase 2: Asset creation (Day 1-3)

### Asset requirements per asset group

PMax requires a full asset package. Google's AI mixes and matches these automatically.

**Text assets:**
- 3-5 headlines (30 char max each)
- 5 long headlines (90 char max each)
- 1-5 descriptions (90 char max each)
- Business name
- Final URL
- Display path (2 parts, 15 char each)

**Image assets:**
- Square: 1200x1200 (1-20 images)
- Landscape: 1200x628 (1-20 images)
- Portrait: 960x1200 (1-20 images)
- Logo: 1200x1200 square + 1200x300 landscape

**Video assets:**
- 1-5 videos (YouTube hosted)
- 10+ seconds recommended
- Portrait (9:16) + landscape (16:9) + square (1:1)

**Note:** If you don't provide videos, Google will AUTO-GENERATE them from your images and text. These auto-generated videos typically underperform. Always provide real videos.

### PrayerLock asset group (example)

**Headlines (30 char max):**
```
1. Lock Phone Until You Pray
2. Prayer Before Screen Time
3. Faith-Based Phone Blocker
4. Your Phone Waits for Prayer
5. PrayerLock: Pray First
```

**Long headlines (90 char max):**
```
1. 86% of Gen Z wants less screen time. PrayerLock makes your phone wait for prayer.
2. Your phone doesn't unlock until you've prayed. Built for Christians who mean it.
3. Stop doom scrolling. Start your day with prayer. PrayerLock blocks everything else.
4. The app that locks your phone until prayer is complete. Join 10,000+ faithful users.
5. Replace your 6AM scroll with 6AM prayer. PrayerLock does it automatically.
```

**Descriptions (90 char max):**
```
1. Your phone locks until prayer is done. No cheating. No shortcuts. Faith first.
2. Built by Christians for Christians. Lock screen triggers prayer time.
3. Join the movement: phone doesn't unlock until you've connected with God.
4. Hard paywall on distraction. Your phone becomes a prayer tool.
5. Screen time down 47%. Prayer time up 3x. One app, one simple rule.
```

**Images to create (via Gemini or Leonardo):**
- App screenshots showing lock screen
- Before/after screen time comparison
- Person praying with phone locked
- App icon showcase
- Testimonial card (real user quote if available)
- Feature breakdown infographic

**Videos needed:**
- 15-second app demo (portrait + landscape)
- 30-second UGC-style testimonial
- 6-second bumper ad (YouTube)

### Asset quality rules

```
DO:
- Show the app in use (not just icon)
- Use real screen time numbers
- Show transformation (before/after)
- Include social proof (even early metrics)
- Match ad creative to app store listing (consistency)

DON'T:
- Use stock photos that look generic
- Make promises you can't substantiate
- Use clickbait that misrepresents the app
- Include phone numbers in image text (Google rejects)
- Use ALL CAPS in text overlays
```

---

## Phase 3: Campaign configuration (Day 3-4)

### Campaign 1: Lock Apps

```
Campaign name: PMAX_LockApps_Installs_v1
Objective: App promotion > App installs
Budget: $2/day
Bidding: Target CPA ($1.50 start, adjust after data)
Location: United States
Language: English

Asset Group 1: PrayerLock
- Audience signal: Custom segment "Christian apps", "prayer apps", "Bible apps"
- Audience signal: In-market "Religious & Spiritual"
- Audience signal: Similar to "Hallow", "Pray.com" users
- Final URL: App Store / Play Store listing

Asset Group 2: WalkToUnlock
- Audience signal: Custom segment "fitness apps", "step counter", "walk tracker"
- Audience signal: In-market "Fitness & Health"
- Audience signal: Similar to "Stepbet", "Charity Miles" users
- Final URL: App Store / Play Store listing

Asset Group 3: StudyLock
- Audience signal: Custom segment "study apps", "focus timer", "pomodoro"
- Audience signal: In-market "Education"
- Audience signal: Demographics: 18-24, College students
- Final URL: App Store / Play Store listing

Asset Group 4: biomaxx
- Audience signal: Custom segment "self improvement", "biohacking", "supplements"
- Audience signal: In-market "Health & Beauty"
- Final URL: App Store / Play Store listing
```

### Campaign 2: Digital Products

```
Campaign name: PMAX_DigitalProducts_Sales_v1
Objective: Sales
Budget: $1/day
Bidding: Maximize conversions (start), switch to Target ROAS after 30 conversions
Location: United States, United Kingdom, Canada, Australia
Language: English

Asset Group 1: Paywall Playbook
- Audience signal: Custom segment "app monetization", "mobile app revenue", "SaaS pricing"
- Audience signal: In-market "Business Services > Software"
- Final URL: Gumroad/Whop product page

Asset Group 2: Cold Email SOP
- Audience signal: Custom segment "cold email", "outbound sales", "lead generation"
- Audience signal: In-market "Business Services > Marketing"
- Final URL: Gumroad/Whop product page

Asset Group 3: Clipping Army Guide
- Audience signal: Custom segment "content creation", "YouTube growth", "TikTok marketing"
- Audience signal: In-market "Business Services > Media Production"
- Final URL: Gumroad/Whop product page
```

### Campaign 3: Services (defer until revenue funds it)

Only launch when cold email + digital products generate $500+/mo to fund ads. Same structure but optimizing for lead gen form submissions and Calendly bookings.

---

## Phase 4: Optimization framework (Week 1-4)

### Day 7 kill threshold (Cody Schneider's process)

```
RULE: After 7 days, evaluate every asset group.

IF spend > $14 AND conversions = 0:
    → KILL the asset group. Don't hope. Don't wait.

IF spend > $14 AND CPA > 3x target:
    → KILL. The AI had enough data to learn. It didn't.

IF spend > $14 AND CPA > 2x target:
    → WARNING. Give 7 more days. If still above 2x, kill.

IF CPA < 1.5x target AND conversions > 0:
    → KEEP. Let it optimize for another 7 days.

IF CPA < target:
    → SCALE. Increase budget 50% (not 2x, gradual).
```

### Day 14 scale decision

```
FOR each surviving asset group:

IF CPA < target AND 10+ conversions:
    → DOUBLE budget
    → Create 3 new creative variants
    → Test different headlines
    → Winner stays, new variants compete

IF CPA = target AND 5-10 conversions:
    → MAINTAIN budget
    → Test 2 new creative angles
    → Wait another 7 days

IF CPA > target after 14 days:
    → KILL. 14 days is enough signal for PMax.
```

### Day 30 portfolio review

```
SURVIVING CAMPAIGNS:
1. Rank by CPA (lowest first)
2. Rank by conversion volume
3. Calculate ROAS per asset group

ALLOCATE:
- Top performer gets 50% of total budget
- #2 gets 30%
- #3 gets 20%
- Everything else: killed

SCALE:
- If top performer CPA < 50% of target: increase total budget 2x
- If portfolio ROAS > 2x: increase total budget 50%
- If no asset group profitable after 30 days: pause all, revisit creative
```

### Negative keyword management (Search component)

PMax shows ads on Search. Control what searches trigger your ads:

**Account-level negative keywords (add immediately):**

```
Negative keyword list: "Brand Protection"
- free [app name]
- [app name] crack
- [app name] hack
- [app name] mod
- download [app name] free

Negative keyword list: "Irrelevant"
- how to
- what is
- definition
- review
- alternative
- vs
- reddit
```

**Why:** PMax's Search component will match broad queries. Negatives prevent waste on informational intent and freebie seekers.

---

## Phase 5: Creative testing (Ongoing)

### The 5-angle testing framework

For each product, create 5 different creative angles. Test all 5 as separate asset groups within one campaign.

**PrayerLock example:**

| Angle | Hook | Target Emotion |
|-------|------|---------------|
| 1. Problem-agitate | "Your phone steals your prayer time" | Guilt/conviction |
| 2. Transformation | "From 6AM scroll to 6AM prayer" | Aspiration |
| 3. Social proof | "10,000+ Christians locked their phones" | Belonging |
| 4. Fear of missing | "Every minute on social media is a minute not in prayer" | Loss aversion |
| 5. Simplicity | "One button. Phone locks. Prayer starts." | Ease/simplicity |

**Test process:**
1. Create 5 asset groups (one per angle)
2. Equal budget split ($0.40/day each for $2/day total)
3. Day 7: kill bottom 2 angles
4. Day 14: kill bottom 1 angle
5. Day 21: winner + runner-up get full budget
6. Day 30: create 3 new angles to challenge winner

### Creative refresh schedule

```
Week 1-2: Launch 5 angles
Week 3: Kill 2, add 0 (let winners breathe)
Week 4: Kill 1 more, champion + challenger identified
Week 5-6: Add 3 new challengers (different creative, same best angle)
Week 7-8: Kill bottom performers, champion evolves

RULE: Never run same creative for more than 6 weeks.
PMax creative fatigue hits around week 4-5.
Always have fresh creative in pipeline.
```

---

## Budget scaling path

| Monthly Revenue | Ad Budget | % of Revenue | Focus |
|----------------|-----------|-------------|-------|
| $0-500 | $100/mo | Test phase | Validate which asset groups convert |
| $500-2K | $200/mo | 10-20% | Scale winning asset groups only |
| $2K-5K | $500/mo | 10-25% | Add new campaigns, test new products |
| $5K-10K | $1,000/mo | 10-20% | Aggressive scaling of proven winners |
| $10K+ | $2,000-5,000/mo | 15-25% | Full portfolio optimization |

**Rule:** Never spend more than 25% of revenue on ads until ROAS is consistently >3x.

---

## Metrics and reporting

### Daily monitoring (2 minutes)

- [ ] Check spend vs budget (no runaway)
- [ ] Check any disapproved assets (fix immediately)
- [ ] Check conversion count (is tracking working?)

### Weekly reporting

```csv
week,campaign,asset_group,spend,impressions,clicks,ctr,conversions,cpa,roas,status
W1,LockApps,PrayerLock,$14,2800,42,1.5%,2,$7.00,TBD,KEEP
W1,LockApps,WalkToUnlock,$14,3100,38,1.2%,0,$0,N/A,KILL
W1,LockApps,StudyLock,$14,2500,55,2.2%,3,$4.67,TBD,KEEP
W1,LockApps,biomaxx,$14,2200,31,1.4%,1,$14.00,TBD,WARNING
```

### Key metrics by campaign type

| Metric | App Installs Target | Digital Products Target | Services Target |
|--------|--------------------|-----------------------|-----------------|
| CPI/CPA | <$2.00 | <$10.00 | <$50.00 |
| CTR | >1.0% | >1.5% | >2.0% |
| ROAS | >3x (30-day LTV) | >2x (immediate) | >5x (deal value) |
| Conversion rate | >3% (install) | >2% (purchase) | >5% (form fill) |

### Kill criteria (hard rules)

| Condition | Action | Timeline |
|-----------|--------|----------|
| $14 spent, 0 conversions | Kill asset group | Day 7 |
| CPA > 3x target after $20 spent | Kill asset group | Day 7 |
| CPA > 2x target after $40 spent | Kill asset group | Day 14 |
| ROAS < 1x after 30 conversions | Kill campaign | Day 30 |
| No conversions in 14 days | Kill campaign | Day 14 |
| CTR < 0.3% | Check creative quality | Day 7 |

---

## Cross-pollination with PRINTMAXX methods

| Method | PMax Integration |
|--------|-----------------|
| COLD_EMAIL | Retarget email openers who didn't reply with PMax Display |
| DIGITAL_PRODUCTS | PMax drives product page traffic. Winning organic content = ad creative. |
| APP_FACTORY | PMax App campaigns = primary paid install channel |
| CONTENT_FARM | Top-performing organic content repurposed as ad creative |
| NEWSLETTER | PMax lead gen feeds Beehiiv subscriber list |
| AI_INFLUENCER | AI UGC videos become PMax video assets |

**Organic-to-paid pipeline (from PAID_ADS_PLAYBOOK.md):**
1. Post same content with 10 different hooks organically
2. Wait 48 hours. Check which hook performs.
3. Take winning hook. Turn into PMax ad creative.
4. Scale with budget. Only spend on validated hooks.

---

## Human action items (CHECKPOINT)

- [ ] Google Ads account setup (free)
- [ ] Add payment method ($100 initial deposit)
- [ ] Link Google Play Console (for app campaigns)
- [ ] Install Firebase SDK in all apps (dev task)
- [ ] Create 5 Gemini-generated ad images per app (15-20 minutes per app)
- [ ] Record or generate 1 video per app (can use Remotion or HeyGen)
- [ ] Create Gumroad/Whop product pages for digital products (prerequisite for campaign 2)

**Total Day 1 cost: $0 setup + $100/mo ad spend**
**First data: Day 7 (kill/keep decisions)**
**First scaling: Day 14 (2x winners)**
**ROI determination: Day 30**

---

## Existing assets to leverage

| Asset | Location | Use For |
|-------|----------|---------|
| Google App Campaigns Playbook | `PAID_ADS/GOOGLE_APP_CAMPAIGNS_PLAYBOOK.md` | App-specific campaign setup |
| Paid Ads Playbook | `PAID_ADS/PAID_ADS_PLAYBOOK.md` | Meta/TikTok cross-reference |
| Paid Ads Deep Dive | `PAID_ADS/PAID_ADS_DEEP_DIVE.md` | Advanced tactics |
| Lock Apps icon prompts v3 | `APP_FACTORY/assets/LOCK_APPS_ICON_PROMPTS_V3.md` | Generate ad images |
| Remotion video infrastructure | `OPS/prompts/remotion/` | Generate video ad assets |
| UGC script templates | `AI_INFLUENCER/ugc_scripts/` | Video ad scripts |
| Digital product listings | `DIGITAL_PRODUCTS/listings/` | Landing page copy for ads |
| Service packages | `OPS/SERVICE_OFFERING_PACKAGES.md` | Service ad copy |
