# App Factory - Priority Matrix

This matrix ranks all potential app opportunities across the PRINTMAXX niches by effort vs. reward.

---

## Scoring Methodology

### Effort Score (1-5, lower is easier)
- **1:** 1-7 days to MVP, minimal native code
- **2:** 1-2 weeks, some platform-specific work
- **3:** 2-4 weeks, moderate complexity
- **4:** 1-2 months, significant native integration
- **5:** 2+ months, complex architecture

### Reward Score (1-5, higher is better)
- **1:** <$1k MRR potential
- **2:** $1-5k MRR potential
- **3:** $5-15k MRR potential
- **4:** $15-50k MRR potential
- **5:** $50k+ MRR potential

### Priority Score = Reward / Effort
Higher score = better opportunity

---

## Priority Rankings

### Tier 1: Build Now (Score 2.0+)

| Rank | App | Niche | Effort | Reward | Score | Method | Status |
|------|-----|-------|--------|--------|-------|--------|--------|
| 1 | **PrayerLock** | Faith | 2 | 4 | 2.00 | AFM012 | Specced |
| 2 | **WalkToUnlock** | Fitness | 2 | 4 | 2.00 | AFM012 | Specced |
| 3 | **PromptVault** | AI | 2 | 4 | 2.00 | AFM007 | Specced |

**Rationale:** All three apps have proven market demand (competitors making money), low technical risk, and clear differentiation through niche focus.

---

### Tier 2: Build Next (Score 1.5-1.99)

| Rank | App | Niche | Effort | Reward | Score | Method | Notes |
|------|-----|-------|--------|--------|-------|--------|-------|
| 4 | FastToUnlock | Faith | 2 | 3 | 1.50 | AFM012 | Lock until intermittent fasting window complete |
| 5 | ReadToUnlock | Faith | 2 | 3 | 1.50 | AFM012 | Lock until Bible reading complete |
| 6 | WorkoutUnlock | Fitness | 3 | 4 | 1.33 | AFM012 | Lock until workout logged (needs gym API) |
| 7 | FaithGPT Wrapper | Faith | 2 | 3 | 1.50 | AFM009 | Christian-focused ChatGPT interface |
| 8 | AI Meal Planner | Fitness | 3 | 4 | 1.33 | AFM009 | Generate meal plans with macros |

---

### Tier 3: Consider Later (Score 1.0-1.49)

| Rank | App | Niche | Effort | Reward | Score | Method | Notes |
|------|-----|-------|--------|--------|-------|--------|-------|
| 9 | Church CRM | Faith | 4 | 5 | 1.25 | AFM006 | Vertical SaaS, high effort |
| 10 | Gym Member CRM | Fitness | 4 | 5 | 1.25 | AFM006 | Vertical SaaS for small gyms |
| 11 | AI Agent Builder | AI | 4 | 5 | 1.25 | AFM008 | Aggregate multiple AI tools |
| 12 | Prayer Journal | Faith | 3 | 3 | 1.00 | AFM003 | Solve Hallow complaints |
| 13 | Fitness AI Coach | Fitness | 4 | 4 | 1.00 | AFM009 | AI personal trainer |
| 14 | Prompt Marketplace | AI | 3 | 3 | 1.00 | AFM007 | Compete with PromptBase |

---

### Tier 4: Low Priority (Score <1.0)

| Rank | App | Niche | Effort | Reward | Score | Method | Notes |
|------|-----|-------|--------|--------|-------|--------|-------|
| 15 | Sermon Notes App | Faith | 3 | 2 | 0.67 | AFM003 | Niche, limited market |
| 16 | Water Tracker | Fitness | 2 | 1 | 0.50 | AFM003 | Commoditized market |
| 17 | AI Chatbot Builder | AI | 5 | 4 | 0.80 | AFM008 | High competition |
| 18 | Sleep Tracker | Fitness | 4 | 3 | 0.75 | AFM003 | Apple/Fitbit dominance |

---

## Detailed Analysis: Tier 1 Apps

### 1. PrayerLock (Faith)

**Effort: 2/5**
- React Native codebase
- Screen Time/Accessibility APIs documented
- Opal/BePresent prove it's buildable
- Bible API is free
- 2-week MVP realistic

**Reward: 4/5**
- Opal doing $600k MRR proves demand
- Faith niche unserved
- $9.99/mo pricing validated
- Church partnerships = B2B upside
- Scaling to $40k+ MRR realistic

**Why Build First:**
- Clear white space (no faith blocker exists)
- Proven monetization model (hard paywall)
- Can reuse code for WalkToUnlock
- TikTok marketing is free and effective

---

### 2. WalkToUnlock (Fitness)

**Effort: 2/5**
- Same architecture as PrayerLock
- HealthKit/Google Fit well-documented
- Shared codebase potential
- 2-week MVP after PrayerLock

**Reward: 4/5**
- Same blocker economics
- Fitness market is larger than faith
- Step goals are universal
- Corporate wellness potential

**Why Build Second:**
- Can build faster by reusing PrayerLock code
- Validates multi-niche app factory approach
- Different marketing channels (fitness TikTok)

---

### 3. PromptVault (AI)

**Effort: 2/5**
- Next.js + Supabase = fast
- OpenAI API is simple
- No native mobile needed initially (web first)
- Prompt curation is content work, not code

**Reward: 4/5**
- AI adoption growing rapidly
- PromptBase proves prompt market exists
- Freemium allows viral growth
- SEO traffic potential is massive

**Why Build:**
- Different tech stack = parallel development possible
- Web-first = faster to market
- Content moat builds over time
- Product Hunt launch potential

---

## Expansion Opportunities

### After Tier 1 Success

**Within niches (horizontal expansion):**

| Current | Expansion | Effort |
|---------|-----------|--------|
| PrayerLock | FastToUnlock (fasting) | Low (same code) |
| WalkToUnlock | WorkoutUnlock, CalorieUnlock | Medium |
| PromptVault | Chrome extension | Low |

**Cross-niche (apply to other verticals):**

| Pattern | New Niche | Example |
|---------|-----------|---------|
| [X]ToUnlock | Productivity | TaskToUnlock |
| [X]ToUnlock | Education | StudyToUnlock |
| Prompt Library | Specific job | PromptVault for Marketers |

---

## Resource Allocation Recommendation

### Phase 1: Weeks 1-4
- **Primary:** PrayerLock MVP
- **Secondary:** PromptVault landing page + waitlist
- **Marketing:** PrayerLock TikTok content

### Phase 2: Weeks 5-8
- **Primary:** WalkToUnlock MVP (reuse PrayerLock code)
- **Secondary:** PromptVault MVP
- **Marketing:** Launch PrayerLock, WalkToUnlock content

### Phase 3: Weeks 9-12
- **Primary:** PromptVault full launch
- **Secondary:** PrayerLock/WalkToUnlock iteration
- **Marketing:** Product Hunt for PromptVault

---

## Key Decision Points

### Build vs. Buy
- All Tier 1 apps should be built in-house
- Tier 3+ consider acquiring existing products

### Kill Criteria
If after 60 days an app has:
- < 100 downloads
- < $500 MRR
- < 5% trial conversion

Consider pivoting or sunsetting.

### Scale Criteria
If after 60 days an app has:
- > $2k MRR
- > 15% trial conversion
- Growing week-over-week

Double down on marketing, consider paid acquisition.

---

## Additional App Ideas (Unscored)

### Faith Niche
- **GratitudeUnlock:** Lock until writing 3 gratitudes
- **DevotionalAI:** AI-generated daily devotionals
- **ChurchFinder:** Find churches by denomination
- **TitheTracker:** Track giving, get tax reports

### Fitness Niche
- **MeditateToUnlock:** Lock until meditation complete
- **GymBuddyAI:** AI workout partner
- **FormChecker:** AI form analysis for exercises
- **MacroSnap:** Photo-based macro tracking

### AI Niche
- **ClaudeTemplates:** Prompt templates for Claude specifically
- **AITranslator:** Document translation with AI
- **MeetingSummarizer:** AI meeting notes
- **CodeReviewer:** AI code review tool

---

## Summary

### Build Order
1. **PrayerLock** - Faith blocker, hard paywall
2. **WalkToUnlock** - Fitness blocker, hard paywall
3. **PromptVault** - AI prompts, freemium

### Expected Timeline
- Week 4: PrayerLock MVP live
- Week 8: WalkToUnlock MVP live
- Week 10: PromptVault MVP live

### Expected Results (Month 3)
- PrayerLock: $2-5k MRR
- WalkToUnlock: $1-3k MRR
- PromptVault: $2-5k MRR
- **Total: $5-13k MRR**

### Reinvestment Strategy
- First $5k MRR: Reinvest in content marketing
- $10k MRR: Test paid acquisition
- $20k MRR: Consider hiring VA for support
- $50k MRR: Full-time focus, potential team

---

## Appendix: Method Reference

| Method ID | Name | Best For |
|-----------|------|----------|
| AFM007 | Free Tier Extraction | PromptVault |
| AFM009 | API Wrapper | FaithGPT, AI Meal Planner |
| AFM012 | Screen Time Blocker | PrayerLock, WalkToUnlock |
| AFM006 | Vertical SaaS | Church CRM, Gym CRM |
| AFM003 | Review Mining | Prayer Journal |

See LEDGER/APP_FACTORY_METHODS.csv for full method details.
