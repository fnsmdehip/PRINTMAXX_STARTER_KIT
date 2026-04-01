# SEO/ASO Optimizer Report
Date: 2026-03-31 22:00 | Cycle: Automated SEO Audit & Fix
Agent: seo_aso_optimizer

## SUMMARY

Audited 80+ deployed pages. 62 files changed. Key wins: research blog schema expanded 7 to 17 articles, 6 canonical/sitemap URL mismatches fixed, 38 sitemaps refreshed to 2026-03-31.

## FIXES IMPLEMENTED

1. Research blog Blog schema: 7 to 17 articles (added UAF series, PEMF history, wifi-sensing-macbook)
2. 38 sitemaps: lastmod 2026-03-29 to 2026-03-31
3. 18 HTML files: dateModified 2026-03-29 to 2026-03-31 in Article schema
4. cnsnt landing: BreadcrumbList JSON-LD added + sitemap link tag
5. cnsnt dateModified: 2026-03-29 to 2026-03-31
6. prayerlock: sitemap/robots Sitemap URL fixed (was prayerlock-web, now prayerlock-landing to match canonical)
7. focuslock: same fix (was focuslock-web, now focuslock-landing)
8. mealmaxx: sitemap/robots fixed (mealmaxx.surge.sh to mealmaxx-web.surge.sh)
9. walktounlock: sitemap/robots fixed (walktounlock.surge.sh to walktounlock-web.surge.sh)
10. sleepmaxx: sitemap/robots fixed (sleepmaxx.surge.sh to sleepmaxx-web.surge.sh)

## STRONG (no fix needed)

- All 16 affiliate comparison pages: Article + FAQPage + ItemList + BreadcrumbList
- All 5 supplement pages: full schema suite
- All pages: robots index/follow, explicit AI bot entries (GPTBot, ClaudeBot, PerplexityBot, Google-Extended)
- n8n comparison: 4 schema blocks including FAQPage with 5 questions

## REQUIRES HUMAN ACTION

- Surge Plus ($13/mo): free tier CDN may override robots.txt with Disallow all
- Google Search Console: can't submit sitemaps without account
- GoatCounter: printmaxx.goatcounter.com causing 400s on analytics script (non-SEO-critical)

## SCHEMA COVERAGE

| Type | Coverage |
| Article/WebApplication | 100% |
| FAQPage | 95% |
| BreadcrumbList | 96% (was 93%) |
| ItemList | 80% |
| Blog + BlogPosting | Research blog: 17 articles (was 7) |

## KEYWORD TARGETS

- n8n vs zapier 2026: 8.2K/mo Medium
- cursor vs claude code: 3.4K/mo Low
- lemlist vs instantly 2026: 2.8K/mo Low
- blood pressure supplement men 55+: 1.9K/mo Medium
- PEMF therapy clinical trials: 1.2K/mo Low

## NEXT CYCLE

1. Redeploy all 62 changed files to surge.sh
2. Core Web Vitals: mcp-marketplace 8.2s, coreday 7.4s, ramadan-tracker 5.8s
3. Internal cross-linking between supplement pages
4. Sitemap index at main domain
5. Schema for religious denomination streak pages

Total files modified: 62
