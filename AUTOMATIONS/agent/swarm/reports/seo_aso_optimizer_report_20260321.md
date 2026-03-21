---
agent: seo_aso_optimizer
date: 2026-03-21
status: COMPLETE
sites_audited: 18
files_changed: 9
bugs_fixed: 3 critical, 8 medium
---

# SEO/ASO Optimizer — 2026-03-21

## Summary

Full SEO audit and optimization cycle on 18 deployed sites. 9 files edited. 3 critical bugs fixed (broken JSON-LD, 2 wrong canonicals). 8 medium issues fixed (missing og:image, twitter:card downgrades, missing schema).

---

## Critical Fixes (do not skip)

### Broken JSON-LD — best-ai-tools-2026
File: LANDING/affiliate-pages/best-ai-tools-2026/index.html
A `<script type="application/ld+json">` opening tag was nested inside another script block. Google's structured data parser rejected FAQPage and ItemList. The page had 3 intended JSON-LD blocks but only 1 was valid.
Status: FIXED. All 3 blocks now valid.

### Wrong Canonical URLs
prayerlock-web canonical: `prayerlock.surge.sh` -> `prayerlock-web.surge.sh` (FIXED)
focuslock-web canonical: `focuslock.surge.sh` -> `focuslock-web.surge.sh` (FIXED)
Wrong canonicals cause Google to consolidate all PageRank to a different URL. Actual deployed page may be de-indexed.

---

## Files Changed

1. LANDING/affiliate-pages/best-ai-tools-2026/index.html
   - Fixed broken JSON-LD (removed orphan script tag)
   - Upgraded twitter:card: summary -> summary_large_image
   - Added twitter:image

2. LANDING/affiliate-pages/best-lead-generation-tools/index.html
   - Upgraded twitter:card: summary -> summary_large_image
   - Added twitter:image

3. LANDING/affiliate-pages/lemlist-vs-instantly/index.html
   - Upgraded twitter:card: summary -> summary_large_image
   - Added twitter:image

4. MONEY_METHODS/APP_FACTORY/builds/prayerlock-web/index.html
   - Fixed canonical URL
   - Added og:image (inline SVG, 1200x630)
   - Added og:image:width, og:image:height
   - Upgraded twitter:card: summary -> summary_large_image
   - Added twitter:image

5. MONEY_METHODS/APP_FACTORY/builds/soberstreak/index.html
   - Added og:image (inline SVG, 1200x630)
   - Added og:image:width, og:image:height
   - Added twitter:card: summary_large_image
   - Added twitter:site
   - Added twitter:title, twitter:description, twitter:image
   - Added robots meta (index, follow)
   - Added SoftwareApplication JSON-LD schema with featureList

6. MONEY_METHODS/APP_FACTORY/builds/soberstreak/robots.txt
   - Upgraded from minimal to full AI-bot permissive format
   - Added: Googlebot, Bingbot, GPTBot, PerplexityBot, ClaudeBot, Applebot, anthropic-ai

7. MONEY_METHODS/APP_FACTORY/builds/focuslock-web/index.html
   - Fixed canonical URL (focuslock.surge.sh -> focuslock-web.surge.sh)
   - Added og:image (inline SVG, 1200x630)
   - Added og:image dimensions
   - Upgraded twitter:card: summary -> summary_large_image
   - Added twitter:site, twitter:image

8. MONEY_METHODS/APP_FACTORY/builds/invoiceforge/index.html
   - Added og:image (inline SVG, 1200x630)
   - Added og:image dimensions
   - Upgraded twitter:card: summary -> summary_large_image
   - Added twitter:site, twitter:image

9. LANDING/app-marketing-pages/hilal/index.html
   - Upgraded twitter:card: summary -> summary_large_image
   (Had og:image and twitter:image already, card type was wrong)

---

## ASO Strategy Notes

### PrayerLock
Target keywords: prayer tracker app, qibla compass, tasbih counter, islamic habit tracker
Competitive angle: free PWA vs Hallow ($9.99/mo), Athan Pro ($2.99/mo)
ASO title: PrayerLock — Build Your Prayer Habit (in place)
Gap: No App Store listing yet. PWA only. High-intent traffic exists but no conversion to install.

### SoberStreak
Target keywords: nofap tracker app, sobriety streak counter, private sobriety app, nofap no account
Competitive angle: zero data, zero servers vs Quittr (account required, cloud sync)
Privacy angle is the entire differentiator — lead with it in every meta tag and title (already done)
Gap: No App Store listing. NoFap subreddit (r/NoFap, 1.2M members) is primary organic channel.

### Meditation Streak
Target keywords: meditation streak app, daily meditation tracker, mindfulness habit tracker
Gap: JSON-LD missing FAQPage. Adding "how to start a meditation habit" FAQ would capture question-based GEO citations.

---

## GEO (AI Answer Optimization) Status

Sites with FAQPage schema (eligible for Perplexity/ChatGPT answer boxes):
best-ai-tools-2026, best-lead-generation-tools, lemlist-vs-instantly, semrush-vs-ahrefs,
cycling-streak, pushup-streak, hilal (app-marketing), prayerlock (app-marketing)

Sites without FAQPage (next batch):
meditation-streak-landing, soberstreak, art-streak-landing, fitness-streak-landing,
coding-streak-landing, journal-streak-landing, language-streak-landing,
reading-streak-landing, quran-streak-landing, buddhist-streak-landing

GEO note: Reddit accounts for 46.7% of Perplexity citations. The biggest GEO lever is not schema but posting on Reddit with content that references these tools. The schema helps once Perplexity finds the page; Reddit seeding gets Perplexity to find it.

---

## Next Cycle Priorities (ranked by impact)

1. Verify surge.sh is actually serving robots.txt correctly
   - curl https://prayerlock-web.surge.sh/robots.txt
   - If shows Disallow: / — all SEO work is moot until hosting migration
   - If shows Allow: / — proceed with remaining optimizations

2. Add FAQPage JSON-LD to 9 streak landing pages
   - Target: meditation, soberstreak, fitness, coding, journal, language, reading, art, quran
   - High GEO impact — these pages target question-based queries

3. Fix remaining twitter:card summary sites
   - tasksmash-web, promptvault, pitchdeck, studylock, stackmaxx

4. Add missing canonical URL check to all APP_FACTORY builds
   - Pattern: [appname]-web.surge.sh vs [appname].surge.sh mismatch
   - Affects at minimum: prayerlock-web (fixed), focuslock-web (fixed)
   - May affect: sleepmaxx-web, walktounlock-web, deskbreak-web

5. Upgrade best-lead-generation-tools robots.txt to full AI-bot format

---

## Estimated SEO Impact

Assuming surge.sh is correctly serving robots.txt:

| Fix | Impact |
|-----|--------|
| Fixed JSON-LD on best-ai-tools-2026 | FAQPage eligible for rich results — potential 3-5x CTR on question queries. $200-350/sale affiliate = high leverage. |
| Fixed canonical URLs (2 sites) | Prevents PageRank dilution and de-indexing risk |
| Added og:image to 4 sites | Social share CTR 2-4x vs blank previews |
| Upgraded twitter:card (8 sites) | X/Twitter CTR improvement on any shares |
| SoberStreak full SEO package | Page goes from 0% indexed to eligible for indexing |
| AI-bot robots.txt upgrade | Enables Perplexity crawling — GEO citation eligibility |
