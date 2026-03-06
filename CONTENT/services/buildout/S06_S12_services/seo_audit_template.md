# SEO Audit — Deliverable Template

## How to Use This

This is the deliverable you send to clients after completing an SEO audit. Fill in the [BRACKETS].
Price for this deliverable: $497-997 one-time audit, or $299/mo ongoing monitoring retainer.
Sell the audit → find problems → sell the fix. Most audits reveal $3K-10K in billable work.

---

# SEO AUDIT REPORT
## [Client Company Name]
**Prepared by:** [Your Name/Agency]
**Date:** [Date]
**Site audited:** [domain.com]
**Scope:** Full technical + on-page + off-page audit

---

## Executive Summary

**Overall SEO Health Score: [X]/100**

| Category | Score | Priority |
|----------|-------|----------|
| Technical SEO | [X]/25 | [HIGH/MED/LOW] |
| On-Page Optimization | [X]/25 | [HIGH/MED/LOW] |
| Content Quality | [X]/25 | [HIGH/MED/LOW] |
| Off-Page / Authority | [X]/25 | [HIGH/MED/LOW] |

**Top 3 issues costing you traffic right now:**
1. [Issue 1 — specific, e.g., "47 pages have duplicate meta descriptions — affecting 30% of indexed pages"]
2. [Issue 2 — e.g., "Core Web Vitals failing on mobile — LCP 4.2s vs 2.5s target = ranking penalty"]
3. [Issue 3 — e.g., "0 backlinks from domain authority 40+ sites — trust deficit vs. competitors ranking #1-3"]

**Estimated traffic upside if issues fixed:** [X]% increase in organic sessions within 90 days based on comparable site improvements.

---

## Section 1: Technical SEO Audit

### 1.1 Crawlability & Indexation

**Current Status:**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Pages indexed (Google Search Console) | [X] | [X] | [PASS/FAIL] |
| Pages crawled but not indexed | [X] | <10 | [PASS/FAIL] |
| Crawl errors | [X] | 0 | [PASS/FAIL] |
| Sitemap submitted to GSC | [YES/NO] | YES | [PASS/FAIL] |
| Robots.txt configured correctly | [YES/NO] | YES | [PASS/FAIL] |
| Canonical tags present | [X]% pages | 100% | [PASS/FAIL] |

**Issues Found:**
- [Specific issue — e.g., "14 pages blocked by robots.txt that should be indexed"]
- [Specific issue — e.g., "Sitemap contains 23 redirected URLs — remove these"]

**Fix Instructions:**
```
Robots.txt fix:
1. Go to [CMS/domain]/robots.txt
2. Remove Disallow rules for: [list URLs]
3. Add: Sitemap: https://[domain].com/sitemap.xml

Sitemap fix:
1. Regenerate sitemap in [Yoast/Rank Math/RankMath/plugin name]
2. Exclude: redirected pages, noindex pages, paginated pages (/page/2/)
3. Resubmit to Google Search Console → Sitemaps
```

---

### 1.2 Site Speed & Core Web Vitals

**Test results** (run via Google PageSpeed Insights + Chrome UX Report):

| Metric | Desktop | Mobile | Target | Status |
|--------|---------|--------|--------|--------|
| LCP (Largest Contentful Paint) | [X]s | [X]s | <2.5s | [PASS/FAIL] |
| INP (Interaction to Next Paint) | [X]ms | [X]ms | <200ms | [PASS/FAIL] |
| CLS (Cumulative Layout Shift) | [X] | [X] | <0.1 | [PASS/FAIL] |
| TTFB (Time to First Byte) | [X]ms | [X]ms | <800ms | [PASS/FAIL] |
| PageSpeed Score | [X]/100 | [X]/100 | >90 | [PASS/FAIL] |

**Issues Found:**
- [e.g., "Hero image is 2.3MB uncompressed PNG — should be WebP under 100KB"]
- [e.g., "Render-blocking scripts in <head>: [list scripts] — defer these"]
- [e.g., "No image lazy loading — all images load on page open"]

**Fix Instructions:**
```
Image optimization:
1. Convert all images to WebP format (use Squoosh.app or ImageOptim)
2. Target: hero images < 100KB, thumbnails < 30KB
3. Add loading="lazy" attribute to all <img> tags below the fold
4. Use Next.js Image or Cloudflare Image Resizing for automatic optimization

Script optimization:
1. Add defer attribute to non-critical JS: <script defer src="...">
2. Move analytics scripts (GA4, Hotjar, etc.) to Google Tag Manager
3. Remove unused plugins/scripts: [list found]

Server/hosting:
1. Enable Cloudflare (free tier) — dramatically improves TTFB
2. Enable Brotli compression in hosting settings
3. Set cache headers: static assets = 1 year, HTML = 1 hour
```

---

### 1.3 HTTPS & Security

| Check | Status |
|-------|--------|
| HTTPS enabled | [PASS/FAIL] |
| HTTP → HTTPS redirect | [PASS/FAIL] |
| SSL certificate valid (expiry date) | [DATE] |
| Mixed content warnings | [X] found |
| Security headers (HSTS, CSP) | [PASS/FAIL] |

---

### 1.4 Mobile Friendliness

| Check | Status | Note |
|-------|--------|------|
| Mobile-friendly test (Google) | [PASS/FAIL] | |
| Viewport meta tag | [PASS/FAIL] | |
| Font size readable on mobile | [PASS/FAIL] | min 16px |
| Tap targets spaced (>48px) | [PASS/FAIL] | |
| No horizontal scroll | [PASS/FAIL] | |

---

## Section 2: On-Page SEO Audit

### 2.1 Title Tags

**Findings:**

| Issue | Count | Pages Affected | Impact |
|-------|-------|---------------|--------|
| Missing title tags | [X] | [list URLs] | HIGH |
| Duplicate title tags | [X] | [list URLs] | HIGH |
| Title too long (>60 chars) | [X] | [list URLs] | MED |
| Title too short (<30 chars) | [X] | [list URLs] | MED |
| Missing target keyword in title | [X] | [list URLs] | HIGH |

**Fix Formula:**
```
Ideal title tag format:
[Primary Keyword] - [Secondary Keyword] | [Brand Name]
Example: "Cold Email Templates That Get Replies | ColdCraft"
Max 60 characters. Put keyword first.
```

---

### 2.2 Meta Descriptions

| Issue | Count | Impact |
|-------|-------|--------|
| Missing meta descriptions | [X] | MED (affects CTR) |
| Duplicate meta descriptions | [X] | MED |
| Too long (>160 chars) | [X] | LOW |
| Missing target keyword | [X] | MED |

**Fix Formula:**
```
Ideal meta description format:
[Benefit statement]. [Social proof or specific claim]. [CTA].
Example: "Discover 50 cold email templates with 20%+ reply rates. Used by 2,300+ sales teams. Copy and use today."
Max 155 characters. Include primary keyword. Write for clicks, not robots.
```

---

### 2.3 Header Structure

**Issues on key pages:**

| Page | H1 Issues | H2 Issues | H3 Issues |
|------|-----------|-----------|-----------|
| [URL 1] | [e.g., Missing H1] | [e.g., Skipped to H3] | - |
| [URL 2] | [e.g., Multiple H1s: 3 found] | - | - |

**Fix Rule:** Every page must have exactly one H1 (the page's main topic = primary keyword). H2s are section headers. H3s are sub-sections. Never skip levels.

---

### 2.4 Keyword Optimization

**Top pages analyzed vs. competitor ranking #1:**

| Page | Your Keyword Density | Competitor's | Missing LSI Keywords |
|------|---------------------|--------------|----------------------|
| [Page 1] | [X]% | [Y]% | [keyword list] |
| [Page 2] | [X]% | [Y]% | [keyword list] |

**Content gap findings:**
- You rank for [X] keywords on page 1; competitors rank for [X×3] on similar topics
- [Specific missing content opportunity — e.g., "No page targeting 'cold email templates for SaaS' — 2,400 monthly searches, KD 28"]

---

### 2.5 Internal Linking

| Metric | Current | Target |
|--------|---------|--------|
| Orphan pages (0 internal links in) | [X] | 0 |
| Pages with >10 outbound internal links | [X] | varies |
| Homepage internal links to key money pages | [X] | 3-5 |
| Blog posts linking to product/service pages | [X]% | >80% |

**Fix:** Every blog post needs at least 2 internal links: 1 to a related blog post, 1 to a product/service page. Build a link map in a spreadsheet.

---

## Section 3: Content Quality Audit

### 3.1 Top Pages by Organic Traffic (Last 90 Days)

*(Pull from Google Search Console → Performance → Pages, sorted by Clicks)*

| Page | Clicks | Impressions | CTR | Avg Position | Opportunity |
|------|--------|-------------|-----|-------------|-------------|
| [Page 1] | [X] | [X] | [X]% | [X] | [note] |
| [Page 2] | [X] | [X] | [X]% | [X] | [note] |

**Quick wins (positions 5-15 → position 1-3):**

Pages ranking 5-15 have high intent but aren't converting. Improving content on these pages = 2-5x traffic without new links.

| Page | Current Position | Target Position | Expected Traffic Lift |
|------|-----------------|----------------|----------------------|
| [URL] | [X] | 1-3 | +[X]%/mo |

---

### 3.2 Thin Content Issues

| Issue | Pages | Action |
|-------|-------|--------|
| <300 words | [X] | Expand to 800+ words or noindex |
| No unique value vs. competitors | [X] | Rewrite with original data/research |
| Duplicate content (internal) | [X] | Canonical tag or merge |
| AI-generated content (unedited) | [X] | Review + humanize or Google may penalize |

---

## Section 4: Off-Page / Authority Audit

### 4.1 Backlink Profile

*(Pull from Ahrefs, Semrush, or Moz)*

| Metric | Your Site | Competitor 1 | Competitor 2 |
|--------|-----------|-------------|-------------|
| Domain Rating / Authority | [X] | [X] | [X] |
| Total referring domains | [X] | [X] | [X] |
| Dofollow links | [X] | [X] | [X] |
| Toxic/spammy links | [X] | - | - |

**Top link opportunities** (sites linking to competitors but not you):
- [Domain 1] (DA [X]) — linked to [competitor] for [topic] — reach out with better resource
- [Domain 2] (DA [X]) — linked to [competitor] for [topic]
- [Domain 3] (DA [X]) — linked to [competitor] for [topic]

### 4.2 Link Building Roadmap

**Tier 1 (high-authority, 1-3 month target):**
- Guest posts on [niche-specific publications]: DA 40-60
- HARO / Quoted.com: free PR links from journalists
- Podcast appearances: typically DA 30-50

**Tier 2 (medium-authority, 3-6 month target):**
- Resource page link building: find "[niche] resources" + contact webmasters
- Broken link building: find broken links on relevant pages, offer your content as replacement
- Digital PR: create original study/data piece, pitch to journalists

**Tier 3 (ongoing):**
- Internal community links (Reddit, Quora, forums)
- Social profiles + citations
- Business directories (Yelp, Clutch, G2, Capterra depending on business type)

---

## Section 5: Prioritized Action Plan

### Immediate (This Week — Free)

- [ ] Fix all 4xx errors in Google Search Console
- [ ] Add missing meta descriptions to top 20 traffic pages
- [ ] Submit updated sitemap
- [ ] Install/connect Google Search Console if not done (free, essential)

### Month 1 ($500-1,500 investment)

- [ ] Speed optimization: image compression + Cloudflare setup
- [ ] Fix all duplicate title tags
- [ ] Expand top 5 thin content pages to 800+ words
- [ ] Internal linking audit: connect orphan pages

### Month 2-3 ($1,500-5,000 investment)

- [ ] Rewrite top 10 pages targeting positions 5-15 for quick wins
- [ ] Build 5 guest post links (DA 40+)
- [ ] Create 1 original data study for PR links
- [ ] Technical structured data / schema markup (FAQ, Article, Product)

### Month 4-6 (Ongoing)

- [ ] 2 new content pieces/week targeting uncovered keywords
- [ ] 4 new backlinks/month minimum
- [ ] Monthly GSC + GA4 review with adjustments

---

## Expected ROI

| Scenario | Month 3 | Month 6 | Month 12 |
|----------|---------|---------|----------|
| Conservative | +[X]% traffic | +[X]% | +[X]% |
| Optimistic | +[X]% traffic | +[X]% | +[X]% |

At current conversion rate of [X]% and avg order/lead value of $[X], traffic increase translates to:
- Month 3: ~$[X] additional revenue/mo
- Month 12: ~$[X] additional revenue/mo

**Audit investment: $[X] → Expected ROI: [X]x in 12 months**

---

## Tools Used in This Audit

| Tool | Cost | What I Used It For |
|------|------|-------------------|
| Google Search Console | Free | Index status, crawl errors, keyword data |
| Google PageSpeed Insights | Free | Core Web Vitals, speed scores |
| Screaming Frog | Free (500 URLs) / $259/yr | Full site crawl, title/meta/header audit |
| Ahrefs / Semrush | $99-129/mo | Backlink profile, competitor gap, keyword data |
| MXToolbox | Free | DNS + HTTPS checks |
| Chrome DevTools | Free | Manual page inspection |

---

*Report prepared by [Your Name/Agency]. Questions? [email] | [calendly link for follow-up call]*
