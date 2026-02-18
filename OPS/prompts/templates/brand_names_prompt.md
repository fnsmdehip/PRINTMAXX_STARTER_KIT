# Brand Names Generation Prompt

**Last Updated:** 2026-01-21
**Use Case:** Generate branded account names across platforms for all niches

---

## Brand Naming Principles

### Requirements
1. **Available** - Check platform availability before finalizing
2. **Memorable** - Easy to say, spell, and remember
3. **Descriptive** - Hints at what the brand does
4. **Consistent** - Same name across all platforms
5. **No numbers or underscores** - Except when necessary for availability

### Naming Patterns That Work

**Pattern 1: Action + Benefit**
- PrayFirst, StepMore, BuildFast
- Direct, verb-first naming

**Pattern 2: Noun + Modifier**
- DailyAnchor, FaithLock, StepCounter
- Concrete, product-focused

**Pattern 3: Compound Words**
- PrintMaxx, WalkToUnlock, PrayerLock
- Unique, brandable

**Pattern 4: Short + Punchy**
- Opal, Brainrot, Sleek
- Single words that stick

---

## PRINTMAXX Brand Family

### Parent Brand
- **PRINTMAXX** - The holding company / content account
- Meaning: Print money to the max (hustle culture reference)
- Platforms: @PRINTMAXXER (X), printmaxx.io

### Sub-Brands by Niche

#### Faith Niche
| Product | Brand Name | Handles |
|---------|------------|---------|
| Screen blocker | PrayerLock | @prayerlock |
| Habit tracker | DailyAnchor | @dailyanchor |
| Devotional app | DevotionFlow | @devotionflow |
| Content account | FaithStack | @faithstack |

#### Fitness Niche
| Product | Brand Name | Handles |
|---------|------------|---------|
| Step blocker | WalkToUnlock | @walktounlock |
| Step tracker | StepStreak | @stepstreak |
| Pelvic health | PelvicPro | @pelvicpro |
| Content account | FitStack | @fitstack |

#### AI/Productivity Niche
| Product | Brand Name | Handles |
|---------|------------|---------|
| Study blocker | LearnLock | @learnlock |
| Prompt library | PromptVault | @promptvault |
| Focus timer | FocusBlock | @focusblock |
| Content account | AIStack | @aistack |

---

## Account Handle Strategy

### Platform-Specific Patterns

**X (Twitter):**
- Prefer: @brandname
- Fallback: @brandnameapp, @getbrandname, @brandnamehq

**Instagram:**
- Prefer: @brandname
- Fallback: @brandname.app, @get.brandname

**TikTok:**
- Prefer: @brandname
- Fallback: @brandnameapp, @brandname_app

**YouTube:**
- Channel name can be longer
- Include keyword: "BrandName - Category"

---

## Name Generation Prompt

```markdown
Generate 10 brand name options for a [PRODUCT_TYPE] in the [NICHE] niche.

Requirements:
- Under 15 characters
- Easy to spell and pronounce
- No numbers or special characters
- Suggests the core benefit
- Sounds professional but approachable

Product description: [DESCRIPTION]
Target audience: [AUDIENCE]
Key benefit: [BENEFIT]

For each name, provide:
1. Name
2. Available as .com? (check or X)
3. Available on X? (check or X)
4. Why it works
```

---

## Availability Check Process

1. Check domain: namecheckr.com or instantdomainsearch.com
2. Check X: twitter.com/[handle]
3. Check Instagram: instagram.com/[handle]
4. Check TikTok: tiktok.com/@[handle]
5. Check App Store: apps.apple.com/search (search name)

**Tool Recommendation:** namecheckr.com checks multiple platforms at once

---

## Name Validation Checklist

Before finalizing a brand name:

- [ ] Spellable when heard aloud
- [ ] No awkward abbreviations
- [ ] Doesn't mean something bad in other languages
- [ ] Domain available (.com preferred, .io acceptable)
- [ ] Handle available on primary platform (X)
- [ ] Handle available on Instagram
- [ ] Handle available on TikTok
- [ ] Doesn't conflict with existing trademark
- [ ] Fits brand family aesthetic

---

## Related Files

- `LEDGER/ACCOUNTS.csv` - Track all accounts and handles
- `AUTOMATIONS/ACCOUNT_WARMING_SOP.md` - Account warmup protocols
- `OPS/prompts/templates/remotion_video_prompt.md` - Brand video generation
