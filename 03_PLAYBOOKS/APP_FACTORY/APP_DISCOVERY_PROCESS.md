# App Discovery & Style Extraction Process

**Purpose:** Reusable methodology for finding trending app concepts, extracting design patterns, and creating competitive differentiation.

---

## Phase 1: Market Research (Find Winners)

### 1.1 Revenue Tracking Sources

| Source | What It Shows | How to Use |
|--------|---------------|------------|
| **SensorTower** | App revenue estimates, downloads | Filter by category, sort by revenue |
| **AppMagic** | Detailed revenue breakdowns | Track month-over-month growth |
| **MobileAction** | ASO data + revenue | Good for keyword research too |
| **ScreensDesign** | Design teardowns | Extract UI patterns from winners |
| **ProductHunt** | New launches with traction | Find emerging concepts early |
| **App Store Top Charts** | Current winners | Check Grossing charts, not just Downloads |

### 1.2 Revenue Signals to Track

```
Indicators of $100k+/mo apps:
- Top 50 in category grossing chart
- 4.5+ star rating with 10k+ reviews
- Weekly subscription option ($3-5/week = $156-260/year per user)
- Active TikTok/Instagram presence
- Multiple copycat apps appearing
```

### 1.3 Social Proof Research

**TikTok/Instagram:**
- Search hashtags: #{concept}app, #{concept}maxxing
- Note: 1B+ views = saturated but proven demand
- Look for: what users complain about, what they want added

**Reddit:**
- r/{niche} communities
- Search "{app name} alternative"
- Find pain points with existing apps

**X/Twitter:**
- Search: "{app name}" filter:links
- Find reviews, complaints, feature requests

---

## Phase 2: Competitive Analysis

### 2.1 App Teardown Checklist

For each top 3-5 competitor, document:

**Monetization:**
- [ ] Price points (weekly/monthly/annual)
- [ ] Free tier limitations
- [ ] Paywall placement (hard vs soft)
- [ ] Trial length
- [ ] Viral loop mechanics (invite friends)

**Onboarding:**
- [ ] Number of screens
- [ ] When gender/personalization asked
- [ ] Social proof placement
- [ ] Value demo before signup

**Core Features:**
- [ ] Main 3-5 features
- [ ] What's free vs premium
- [ ] Daily engagement hooks
- [ ] Notification strategy

**Design:**
- [ ] Color scheme (primary, secondary, accent)
- [ ] Typography (headline, body)
- [ ] Dark/light mode
- [ ] Icon style (filled, outline, custom)
- [ ] Animation patterns
- [ ] Card/component styles

### 2.2 Design Extraction Template

```markdown
## [App Name] Design System

### Colors
- Primary: #HEXCODE (describe use)
- Secondary: #HEXCODE
- Background: #HEXCODE
- Text Primary: #HEXCODE
- Text Secondary: #HEXCODE
- Success/Error/Warning: #HEXCODE

### Typography
- Headlines: [Font Family], [Weight], [Size Range]
- Body: [Font Family], [Weight], [Size]
- Caption: [Font Family], [Size]

### Components
- Card style: [rounded corners, shadows, borders]
- Button style: [gradient, solid, outline]
- Input style: [rounded, underline, boxed]

### Animations
- Screen transitions: [fade, slide, none]
- Button interactions: [scale, shadow, color]
- Loading states: [skeleton, spinner, shimmer]
- Progress indicators: [rings, bars, counters]

### Iconography
- Style: [SF Symbols, Material, custom]
- Weight: [regular, bold]
- Size: [small, medium, large in px]
```

---

## Phase 3: Differentiation Strategy

### 3.1 Gap Analysis Framework

For each competitor, identify:

| Gap Type | Question | Opportunity |
|----------|----------|-------------|
| **Audience** | Who's underserved? | Women, specific age, country |
| **Feature** | What's missing? | Daily habits, education, community |
| **UX** | What's frustrating? | Slow, confusing, too many steps |
| **Price** | Who's priced out? | Students, budget-conscious |
| **Aesthetic** | What's the vibe? | Cold/masculine → warm/inclusive |
| **Language** | What markets ignored? | Non-English speaking countries |

### 3.2 Differentiation Options

**Audience Niches:**
- Gender-specific (women's version of male-focused app)
- Age-specific (teens, seniors)
- Faith-based (Christian, Muslim versions)
- Profession-specific (nurses, students, athletes)
- Country-specific (with cultural customization)

**Feature Differentiation:**
- Add daily engagement loop (competitors often one-time use)
- Add education/learning component
- Add community/social features
- Add gamification (streaks, achievements)
- Add AI personalization

**Aesthetic Differentiation:**
- Warm vs cold colors
- Cute mascot (higher retention proven)
- Gender-inclusive design
- Premium dark mode
- Playful vs serious tone

### 3.3 Localization Decision Tree

```
Q1: Is primary market English-speaking?
  Yes → Start with English
  No → Start with target language

Q2: Are competitors English-only?
  Yes → Opportunity for localized version
  No → Differentiate on features instead

Q3: Single app with language toggle OR separate apps?
  → ALWAYS single app with toggle
  → Separate apps fragment reviews, ratings
  → Apple/Google ASO supports multi-locale per app

Implementation:
  1. expo-localization + react-i18next
  2. Auto-detect device language
  3. Manual override in settings
  4. Start with: English → FIGS → Asian markets
```

---

## Phase 4: Style Guide Creation

### 4.1 Aggregate Method

Instead of copying one competitor:

1. Extract design elements from top 5 apps
2. Create aggregate that blends best elements
3. Add one unique twist (color, mascot, tone)

**Example (Looksmaxxing):**
- UMAX: Dark + blue + masculine
- LooksMax AI: Dark + rating colors + data-focused
- **GlowMaxx Aggregate:** Dark + warm coral/teal + encouraging tone

### 4.2 Style Guide Deliverables

For each new app, create:

1. **COMPETITIVE_ANALYSIS.md** - Market research, revenue data, competitor breakdown
2. **LANDING_PAGE_STYLE_GUIDE.md** - Web/marketing design system
3. **MOBILE_APP_STYLE_GUIDE.md** - React Native design system

---

## Phase 5: Validation Before Build

### 5.1 Quick Validation Checklist

- [ ] At least one competitor doing $100k+/mo
- [ ] Clear differentiation identified (not just a clone)
- [ ] Feature set is achievable in 2-4 weeks
- [ ] Monetization model proven in category
- [ ] No obvious legal/compliance issues

### 5.2 Build vs Skip Signals

**Build if:**
- Proven revenue in category ($100k+/mo competitor)
- Clear underserved audience
- Can ship MVP in <3 weeks
- Subscription model works in category

**Skip if:**
- Category dominated by free apps
- Requires hardware integration
- Heavy content licensing needed
- Regulatory complexity (health claims, financial advice)

---

## Quick Reference: Where Files Live

| Document | Location | Purpose |
|----------|----------|---------|
| App opportunities | `LEDGER/APP_CLONE_OPPORTUNITIES.csv` | Tracking app ideas |
| App methods | `LEDGER/APP_FACTORY_METHODS.csv` | Proven playbooks |
| Monetization | `APP_FACTORY/APP_MONETIZATION_STRATEGY.md` | IAP, subs, ads, affiliate |
| Assets | `APP_FACTORY/ASSET_GENERATION_GUIDE.md` | Icons, illustrations |
| Rejection avoidance | `APP_FACTORY/APP_STORE_REJECTION_GUIDE.md` | Compliance |
| Per-app analysis | `APP_FACTORY/builds/{app}/COMPETITIVE_ANALYSIS.md` | Market research |
| Per-app landing style | `APP_FACTORY/builds/{app}/marketing/LANDING_PAGE_STYLE_GUIDE.md` | Web design |
| Per-app mobile style | `APP_FACTORY/builds/{app}/MOBILE_APP_STYLE_GUIDE.md` | App design |

---

## Example: GlowMaxx Discovery Process

**Step 1: Found Winners**
- UMAX: $500k/mo, 1M+ users
- LooksMax AI: $100k+/mo
- Source: Yahoo Finance article, ScreensDesign teardowns

**Step 2: Extracted Patterns**
- Dark mode default
- Social proof prominent
- Soft paywall with viral loop
- Weekly subscription pricing

**Step 3: Found Gaps**
- Women underserved (apps focus on masculinity)
- No daily engagement (one-time scan model)
- No education (scores without explanations)

**Step 4: Created Differentiation**
- Warm coral/teal palette (vs cold blue)
- Daily habit tracking (vs one-time scan)
- Gender toggle with tailored routines
- Educational Learn tab

**Step 5: Created Style Guides**
- COMPETITIVE_ANALYSIS.md
- LANDING_PAGE_STYLE_GUIDE.md
- MOBILE_APP_STYLE_GUIDE.md (patterns for app UI)

---

## Automation Notes

When running this process with agents:

```bash
# Research phase
- Web search for "{category} app revenue"
- Fetch ScreensDesign teardowns
- Check App Store top charts

# Analysis phase
- Extract color palettes from screenshots
- Document pricing from App Store
- Note feature differences

# Creation phase
- Generate COMPETITIVE_ANALYSIS.md
- Generate style guides
- Update constants.ts with new colors
```

This process should take 2-4 hours for thorough research, or can be parallelized across multiple agents for faster execution.
