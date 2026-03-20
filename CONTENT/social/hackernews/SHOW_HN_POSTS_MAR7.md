STATUS: PENDING_REVIEW
DATE: 2026-03-07
BATCH: Hacker News Show HN posts

---

# SHOW HN POST 1

TITLE: Show HN: ShopMetrics Pro, paste any Shopify store URL, see their tech stack and apps

URL: https://shopmetrics-pro.surge.sh

---

BODY:

ShopMetrics Pro analyzes any Shopify store from a URL.

What it returns:
- Theme (name, version)
- Installed apps (detected from DOM, scripts, meta tags)
- Analytics tools in use
- Product count estimate
- Third-party integrations (chat, reviews, email capture, loyalty)

No login. No email. Paste URL, get data.

Technical approach: static frontend on surge.sh, client-side analysis of publicly accessible store data via DOM inspection and script tag parsing. No server-side scraping, everything runs in-browser against what the store makes publicly available.

I built this because I was manually reading Shopify source code before client pitches and wanted to stop doing that by hand. The 47-point version (SiteScore Pro) extends this to full SEO and performance auditing.

Would be curious what additional signals people would find useful. Klaviyo/Postscript detection, price range analysis, and review volume are on the roadmap.

---

# SHOW HN POST 2

TITLE: Show HN: SiteScore, free website performance scorer (47 signals, results in under 2 seconds)

URL: https://sitescore-free.surge.sh

---

BODY:

SiteScore scores any website across 47 signals across performance, SEO, UX, and technical health.

Free tier: 5 key signals, instant results.
Pro tier: All 47 signals, $19/mo at sitescore-pro.surge.sh.

Both load in under 2 seconds.

What the 47-point audit checks:
- Core Web Vitals proxy metrics (LCP, CLS, FID estimates)
- Meta tag completeness and quality
- Heading structure
- Image optimization signals
- Mobile viewport configuration
- Schema markup presence
- Canonical tag usage
- Robots.txt and sitemap presence
- Third-party script load weight
- HTTPS and security headers
- Social meta tags (OG, Twitter Card)
- Internal link structure
- Page weight estimate
- Font loading strategy

Built as a static app on surge.sh. The analysis runs client-side using Fetch API + DOMParser against publicly accessible page content.

Use cases I've seen: agency owners sending free scores in cold outreach ("your site scored 34/100"), developers benchmarking competitor pages, founders doing pre-launch audits.

The free tier is genuinely free with no email wall. The 5 signals it returns are the 5 highest-signal ones. Pro unlocks the rest.

Feedback welcome, especially on what signals are most useful vs. noise.
