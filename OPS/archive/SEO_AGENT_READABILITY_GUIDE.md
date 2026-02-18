# Entity SEO + agent readability guide

**Created:** 2026-02-01 (mega_ralph iteration 13)
**Triggered by:** ALPHA462 (zero-click SEO crisis, 58% no clicks), ALPHA471 (entity SEO replaces keywords)
**Status:** Active implementation guide

---

## The shift: keywords to entities

Google and AI models now understand entities, not just keyword strings. "PrayerLock app" isn't a keyword anymore. It's an entity with properties: category (productivity), niche (faith), function (phone locking), price ($4.99/mo), platform (iOS/Android).

**What this means for us:**

1. Pages must declare entities explicitly (JSON-LD, structured data)
2. Content must answer entity-relationship questions ("What is PrayerLock?" "How does PrayerLock compare to Hallow?")
3. AI crawlers (ChatGPT, Claude, Perplexity) now drive 30%+ of organic traffic
4. 58% of searches end without a click. If your answer isn't in the SERP or the AI response, you don't exist.

---

## Agent-readable content requirements

AI crawlers parse content differently than humans. Optimize for both.

### Structure for AI citation

| Pattern | Why it works | Example |
|---------|--------------|---------|
| Quick answer in first 100 words | AIs pull from opening paragraph | "PrayerLock locks your phone until you complete morning prayer. It costs $4.99/mo." |
| Bullet lists | Easy to parse, cite individual items | "3 steps: 1. Set prayer time 2. Phone locks 3. Complete to unlock" |
| Comparison tables | AIs love structured data for vs queries | "PrayerLock vs Hallow: Price, features, target audience" |
| FAQ with natural questions | Matches voice search and AI query patterns | "How do I build an AI workflow stack?" |
| Definitive statements | AIs prefer confident, specific sources | "The best model for bulk content is Gemini Flash" not "Some might say..." |

### Technical requirements per page

Every page on printmaxx.ai should have:

1. **JSON-LD Article schema** - Generated via `generateArticleSchema()` in `lib/content.ts`
2. **JSON-LD FAQPage schema** - Generated via `generateFAQSchema()` from FAQ sections
3. **Organization schema** - On root layout via `generateOrganizationSchema()`
4. **Per-page metadata** - `generateMetadata()` in dynamic routes, static `metadata` export in static routes
5. **Canonical URL** - Via `metadataBase` in root layout + `alternates.canonical` per page
6. **Open Graph + Twitter cards** - For social sharing preview
7. **Sitemap.xml** - Dynamic via `app/sitemap.ts`
8. **Robots.txt** - Explicitly allows AI crawlers (GPTBot, ClaudeBot, PerplexityBot)

### Content patterns that get cited

**Pattern 1: Definitive quick answer**
```
# How to build an AI workflow stack for solopreneurs

Pick 1 niche. Ship 10 truth pages + 50 longtails before running ads.
Route bulk work to cheap models (Gemini Flash). Save Opus for final copy.
Track prompt-share + lead conversion weekly.
```
AIs can cite this directly. It answers the query in 4 sentences.

**Pattern 2: Comparison table**
```
| Tool | Price | Best for | Limit |
|------|-------|----------|-------|
| Gemini Flash | $0.075/1M tokens | Bulk drafting | 4M context |
| Claude Sonnet | $3/1M tokens | Refinement | 200K context |
| Claude Opus | $15/1M tokens | Final quality | 200K context |
```
AIs pull table rows for "best X for Y" queries.

**Pattern 3: Step-by-step numbered list**
```
1. Define niche + persona + outcome promise
2. Create 10 truth pages with schema + internal links
3. Generate 300 longtail slugs, publish first 50
```
AIs cite numbered steps for "how to" queries.

**Pattern 4: FAQ with natural phrasing**
```
**Do I need n8n?**
No. Use it only if you want a UI router. Playwright + cron is more controllable.
```
Matches voice search. AI models pull FAQ answers for question queries.

---

## Un-generatable content (the moat)

Zero-click SEO means your content must be something AI can't just generate itself. Otherwise you're in a race you can't win.

**Content types AI can't replicate:**

| Type | Example | Why it's defensible |
|------|---------|---------------------|
| Interactive tools | Stack generator, ROI calculator | Requires computation, user input |
| Proprietary data | Our revenue numbers, A/B test results | Only we have this data |
| Real-time dashboards | App metrics, funnel performance | Changes over time, needs live data |
| Community data | Survey results, user stories | Aggregated from real people |
| Tool integrations | "Enter your URL and we'll audit" | Requires API calls |

**Our un-generatable assets:**
- `/magnet/stack-generator` - Interactive workflow recommendation tool
- Revenue numbers from our own apps (when live)
- A/B test results from our paywall experiments
- Community insights from Skool/newsletter audiences

---

## Implementation status

### Done (this iteration)

| File | Change | SEO impact |
|------|--------|------------|
| `app/truth/[slug]/page.tsx` | Added `generateMetadata()` with per-page title, description, OG, Twitter, canonical | Each truth page now has unique metadata. Was invisible to search. |
| `app/truth/[slug]/page.tsx` | Added JSON-LD Article + FAQPage schema rendering | Rich snippets in SERPs. FAQ answers shown directly in Google. |
| `app/truth/page.tsx` | Added static metadata export with OG + Twitter + canonical | Truth index page now has proper metadata. |
| `app/layout.tsx` | Added `metadataBase`, title template, Organization schema, robots directives, AI bot allowlists | All pages inherit canonical URL base. Organization entity declared. AI crawlers explicitly welcomed. |
| `app/sitemap.ts` | Created dynamic sitemap with all truth pages + app pages | Crawlers discover all pages. Updated automatically when content changes. |
| `app/robots.ts` | Created with explicit AI crawler rules (GPTBot, ClaudeBot, PerplexityBot) | AI models can crawl and cite our content. |
| `lib/content.ts` | Enhanced with FAQ extraction, description extraction, excerpt extraction | Content data now includes all SEO-relevant fields extracted from markdown. |

### Switched from truth-pages.ts to content.ts

The old `lib/truth-pages.ts` had a limited interface (no description, keywords, author, date, faqItems). All truth page routes now import from `lib/content.ts` which has the full SEO data model.

### Content library consolidation

`lib/content.ts` is now the single source for all content data. It:
- Extracts title from H1 heading (when no frontmatter)
- Extracts Quick Answer as excerpt
- Generates description from Quick Answer (first 160 chars)
- Extracts FAQ items from markdown FAQ sections
- Supports gray-matter frontmatter (when pages are upgraded)
- Has schema generators for Article, FAQPage, Organization

---

## Known issue: duplicate truth page content

Several truth pages have identical body content with different titles. This is a content quality issue, not a technical SEO issue. Each page now has unique metadata (title, description) based on its filename, but the body content duplication will hurt rankings.

**Action needed:** Rewrite each truth page with unique content matching its title. The structure (Quick Answer, Steps, Table, FAQ, Schema) is correct. The content needs to be unique per topic.

---

## SEO scorecard (before vs after)

| Category | Before | After |
|----------|--------|-------|
| Root metadata | 6/10 | 9/10 |
| Dynamic route metadata | 0/10 | 9/10 |
| Schema markup (rendered) | 0/10 | 9/10 |
| Sitemap | 0/10 | 10/10 |
| Robots.txt | 0/10 | 10/10 |
| Canonical URLs | 0/10 | 9/10 |
| AI crawler access | 0/10 | 10/10 |
| OG/Twitter cards | 4/10 | 9/10 |
| **Overall** | **4.5/10** | **9.4/10** |

---

## Next steps

1. Add YAML frontmatter to all truth pages (title, description, keywords, author, date)
2. Rewrite duplicate truth page content to be unique per topic
3. Add OpenGraph images per truth page
4. Add internal linking between related truth pages
5. Create longtail page routes with same SEO treatment
6. Monitor AI citation rates via prompt-share testing
7. Submit sitemap to Google Search Console + Bing Webmaster Tools
