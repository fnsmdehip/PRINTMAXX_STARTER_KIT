# MASTER KPI LIST
# Backend data spec. Control panel (localhost:9999) is the UI.
# Updated: 2026-04-06

---

## CRITICAL PATH: 5 KPIs THAT MATTER RIGHT NOW ($0 Revenue)

These are the only KPIs worth checking daily until first dollar hits the bank. Everything else is noise until these move.

| # | KPI | Current | Week 1 Target | Week 2 Target | Week 3 Target | Week 4 Target (M1) | Type | Why It Matters |
|---|-----|---------|---------------|---------------|---------------|--------------------|----- |----------------|
| CP-1 | Stripe balance (available + pending) | $0 | $0 | $0-50 | $50-200 | $200-500 | LAGGING | Only real measure of revenue. Everything else is a proxy. |
| CP-2 | Affiliate clicks/day | 0 | 10-20 | 30-50 | 50-100 | 100-200 | LEADING | Clicks predict conversions. No clicks = no revenue, period. |
| CP-3 | Cold emails sent/day | 0 | 20-30 | 50-80 | 80-100 | 100+ | LEADING | Direct outbound is fastest path to service revenue. More sent = more replies = more deals. |
| CP-4 | Freelance proposals sent/day | 0 | 3-5 | 5-8 | 8-10 | 10+ | LEADING | Each proposal is a lottery ticket. 10%+ conversion at $200-500/deal. |
| CP-5 | Content pieces published/day | ~1-2 | 3-5 | 5-8 | 8-10 | 10+ | LEADING | Content drives affiliate clicks and SEO. Compounds. Every day without content is lost traffic forever. |

**Reading this table:** LEADING indicators predict future revenue (if these move, money follows in 1-4 weeks). CP-1 is the only LAGGING indicator -- it tells you what already happened. If CP-2 through CP-5 are hitting targets but CP-1 stays at $0 past week 3, the funnel is broken somewhere between click and conversion.

**Weekly check ritual (5 min):** Pull CP-1 from Stripe. Pull CP-2 from affiliate dashboards. Pull CP-3 from Instantly.ai. Count CP-4 from Fiverr/Upwork. Count CP-5 from posting queue. If any LEADING indicator is at zero, that's the priority for the day.

---

## 1. REVENUE

| # | KPI | Current | Wk1 | Wk2 | Wk3 | M1 | M3 | How to Measure | Freq | Type |
|---|-----|---------|-----|-----|-----|----|----|----------------|------|------|
| 1.1 | Gross revenue (total) | $0 | $0 | $0-100 | $100-300 | $500-1K | $5K | FINANCIALS/REVENUE_TRACKER.csv sum(amount) | Daily | LAGGING |
| 1.2 | Revenue: Services | $0 | $0 | $0-200 | $200-400 | $500 | $2K | REVENUE_TRACKER.csv source=SERVICE | Daily | LAGGING |
| 1.3 | Revenue: Digital Products | $0 | $0 | $0-30 | $30-60 | $100 | $500 | REVENUE_TRACKER.csv source=PRODUCT | Daily | LAGGING |
| 1.4 | Revenue: Apps | $0 | $0 | $0 | $0-50 | $100 | $1K | Stripe dashboard + RevenueCat | Daily | LAGGING |
| 1.5 | Revenue: Affiliate | $0 | $0 | $0 | $0-50 | $100 | $500 | Affiliate dashboards (see Section 6) | Daily | LAGGING |
| 1.6 | Revenue: Personas | $0 | $0 | $0-50 | $50-100 | $200 | $1K | Platform dashboards (Fanvue/Fansly/CashApp) | Daily | LAGGING |
| 1.7 | Revenue: Content | $0 | $0 | $0 | $0 | $0 | $200 | REVENUE_TRACKER.csv source=CONTENT | Daily | LAGGING |
| 1.8 | Revenue: E-Commerce | $0 | $0 | $0 | $0 | $0 | $200 | Etsy/Amazon/TikTok Shop dashboards | Daily | LAGGING |
| 1.9 | Revenue: Community | $0 | $0 | $0 | $0 | $0 | $100 | Skool/Discord/Telegram payment logs | Daily | LAGGING |
| 1.10 | Deals in pipeline (count) | 0 | 2-3 | 5-8 | 8-12 | 10-20 | 30+ | AUTOMATIONS/leads/ CSV count where status=ACTIVE | Daily | LEADING |
| 1.11 | Deals in pipeline (value) | $0 | $500 | $1-2K | $2-5K | $5-10K | $20K+ | AUTOMATIONS/leads/ CSV sum(deal_value) | Daily | LEADING |
| 1.12 | Proposals outstanding | 0 | 5-8 | 10-15 | 15-20 | 20+ | 30+ | Fiverr/Upwork active proposals | Daily | LEADING |
| 1.13 | Conversion: proposals to gigs | 0% | N/A | 5-8% | 8-12% | 10-15% | 15-20% | gigs_won / proposals_sent | Weekly | LAGGING |
| 1.14 | Average deal size | $0 | N/A | $150-300 | $200-400 | $200-500 | $500+ | total_revenue / total_deals | Weekly | LAGGING |
| 1.15 | Revenue per hour of human time | $0 | N/A | N/A | N/A | $50-200 | $100+ | gross_revenue / human_hours_logged | Monthly | LAGGING |
| 1.16 | Revenue per $1 infra cost | $0 | N/A | N/A | N/A | $2-5 | $15-20 | gross_revenue / monthly_infra_spend | Monthly | LAGGING |
| 1.17 | CAC by channel | N/A | N/A | N/A | N/A | Track | Track | ad_spend_per_channel / customers_per_channel | Monthly | LAGGING |
| 1.18 | Customer LTV | N/A | N/A | N/A | N/A | Track | Track | avg_revenue_per_customer * avg_months_retained | Monthly | LAGGING |
| 1.19 | Burn rate vs revenue | -$280/mo | -$280 | -$250 | -$200 | -$100 to $0 | +$2K | infra_cost - gross_revenue | Monthly | LAGGING |
| 1.20 | Margin by venture | N/A | N/A | N/A | N/A | 80%+ digital | 80%+ | (revenue - cost) / revenue per venture | Monthly | LAGGING |
| 1.21 | Stripe balance (available) | $0 | $0 | $0-50 | $50-200 | $200-500 | $2K+ | mcp__Stripe__retrieve_balance | Daily | LAGGING |
| 1.22 | Stripe balance (pending) | $0 | $0 | $0-100 | $50-200 | $100-500 | $1K+ | mcp__Stripe__retrieve_balance | Daily | LAGGING |
| 1.23 | Total paying customers | 0 | 0-1 | 1-3 | 3-8 | 5-20 | 100-500 | Stripe customer count + platform counts | Weekly | LAGGING |
| 1.24 | Repeat customers | 0 | N/A | N/A | N/A | 0-2 | 5-20 | Customers with 2+ purchases | Monthly | LAGGING |
| 1.25 | Referral rate | 0% | N/A | N/A | N/A | N/A | 5-10% | referred_customers / total_customers | Monthly | LAGGING |
| 1.26 | Churn (subscriptions) | N/A | N/A | N/A | N/A | N/A | 5-15% | cancelled_subs / total_subs per month | Monthly | LAGGING |
| 1.27 | NPS score | N/A | N/A | N/A | N/A | N/A | 40-60 | Survey responses | Quarterly | LAGGING |

**M1 target note:** $1K/mo from $0 is realistic IF services (freelance gigs) carry most of the weight in weeks 1-3. Digital products and apps take longer to ramp. The weekly breakdown above reflects this: services revenue front-loaded, passive income back-loaded.

---

## 2. CONTENT

| # | KPI | Current | Target | How to Measure | Freq | Batchable | Type |
|---|-----|---------|--------|----------------|------|-----------|------|
| 2.1 | Content pieces published (all platforms) | ~40 | 5-10/day M1, 10-20/day M2+ | CONTENT/social/posting_queue/ published count | Daily | YES (30d) | LEADING |
| 2.2 | Content pieces generated (backlog) | 588 | Track | Count files in CONTENT/social/ | Daily | YES (30d) | LEADING |
| 2.3 | Tweets posted | ~40 | 3-5/day | Twitter analytics | Daily | YES (30d) | LEADING |
| 2.4 | Threads posted | 0 | 1/day | Twitter analytics | Daily | YES (30d) | LEADING |
| 2.5 | Reddit posts | 0 | 3-5/day | Reddit post history | Daily | YES (30d) | LEADING |
| 2.6 | Reddit comments (engagement) | 0 | 5-10/day | Reddit comment history | Daily | Daily-only | LEADING |
| 2.7 | YouTube videos published | 0 | 2-3/week | YouTube Studio | Weekly | YES (30d) | LEADING |
| 2.8 | YouTube Shorts published | 0 | 5-7/week | YouTube Studio | Weekly | YES (30d) | LEADING |
| 2.9 | TikTok videos published | 0 | 1-3/day | TikTok analytics | Daily | YES (30d) | LEADING |
| 2.10 | Pinterest pins published | 0 | 5-10/day | Pinterest analytics | Daily | YES (30d) | LEADING |
| 2.11 | Newsletter issues sent | 0 | 1/week | Beehiiv dashboard | Weekly | YES (30d) | LEADING |
| 2.12 | Blog articles published | 17 | 2-3/week | Count files in LANDING/research-blog/ | Weekly | YES (30d) | LEADING |
| 2.13 | Content engagement rate (avg) | 0% | 2-3% M1, 5%+ M3 | (likes+comments+shares) / impressions | Daily | No | LAGGING |
| 2.14 | Content-to-sale conversion rate | 0% | 0.5-1% M1, 2-3% M3 | sales_from_content / content_clicks | Weekly | No | LAGGING |
| 2.15 | Creative variations generated/week | 0 | 50+ | Count generated assets | Weekly | YES (30d) | LEADING |

---

## 3. APPS

| # | KPI | Current | Target | How to Measure | Freq | Batchable | Type |
|---|-----|---------|--------|----------------|------|-----------|------|
| 3.1 | Apps deployed (total) | 114 sites + 4 native | 120+ | Count in DEPLOYMENT_URLS.md + App Store | Weekly | No | LEADING |
| 3.2 | Apps submitted to App Store | 0 | 5 M1 | App Store Connect | Weekly | No | LEADING |
| 3.3 | Apps live on App Store | 0 | 5 M1, 15 M3 | App Store Connect | Weekly | No | LEADING |
| 3.4 | App MRR (total portfolio) | $0 | $100 M1, $1K M3 | RevenueCat + Stripe | Daily | No | LAGGING |
| 3.5 | App downloads (total) | 0 | 500 M1 | App Store Connect analytics | Daily | No | LEADING |
| 3.6 | App premium conversion rate | 0% | 2-5% | premium_users / total_downloads | Weekly | No | LAGGING |
| 3.7 | ARPD (avg revenue per download) | $0 | $0.03-0.10 | total_app_revenue / total_downloads | Monthly | No | LAGGING |
| 3.8 | App Store rating (avg) | N/A | 4.5+ | App Store Connect | Weekly | No | LAGGING |
| 3.9 | Apps killed (underperforming) | 0 | Track | Apps removed: <$100 MRR after 60d | Monthly | No | LAGGING |
| 3.10 | Apps doubled-down (scaling) | 0 | Track | Apps with 20%+ MoM growth at $500+ | Monthly | No | LAGGING |
| 3.11 | PWA monthly active users | 0 | Track | Analytics per PWA | Weekly | No | LAGGING |
| 3.12 | Deep QA pass rate | 44/44 static, 47/47 deep | 100% | test_runner.py + deep_qa.py | Per build | No | LEADING |
| 3.13 | Stripe Payment Links active (apps) | 4 | Track | OPS/STRIPE_PRODUCTS.md count | Weekly | No | LEADING |

---

## 4. LEADS & OUTBOUND

| # | KPI | Current | Target | How to Measure | Freq | Batchable | Type |
|---|-----|---------|--------|----------------|------|-----------|------|
| 4.1 | Cold emails sent | 0 | 50-100/day M1, 200-500/day M2+ | Instantly.ai dashboard | Daily | Daily-only | LEADING |
| 4.2 | Cold email reply rate | 0% | 1-2% M1, 3-5% M3 | replies / emails_sent | Daily | No | LAGGING |
| 4.3 | Cold email open rate | 0% | 30-50% | opens / emails_sent | Daily | No | LAGGING |
| 4.4 | AI calls made (Bland) | 0 | 20-50/day M1, 100/day M2+ | Bland.ai dashboard | Daily | Daily-only | LEADING |
| 4.5 | Freelance proposals sent | 0 | 5-10/day | Fiverr/Upwork sent proposals | Daily | Daily-only | LEADING |
| 4.6 | Leads generated (total) | 1,110 | 50-100/mo M1, 200-500/mo M3 | AUTOMATIONS/leads/ CSV row count | Daily | No | LEADING |
| 4.7 | Leads scored (pipeline) | 15 | 20-50 active M1, 100+ M3 | leads where status=SCORED | Daily | No | LEADING |
| 4.8 | Outreach drafts pending | 6 | Track | AUTOMATIONS/leads/outreach_drafts/ count | Daily | No | LEADING |
| 4.9 | Email list size | 0 | 100-500 M1, 2K-5K M6 | Beehiiv subscriber count | Daily | No | LEADING |
| 4.10 | Email CTR | 0% | 15%+ | Beehiiv analytics | Daily | No | LAGGING |
| 4.11 | LinkedIn connections/outreach | 0 | 10-20/day | LinkedIn activity | Daily | Daily-only | LEADING |
| 4.12 | Affiliate recruitment emails sent | 0 | 20/week | Tracking CSV | Weekly | Daily-only | LEADING |

---

## 5. SOCIAL MEDIA

| # | KPI | Current | Target | How to Measure | Freq | Batchable | Type |
|---|-----|---------|--------|----------------|------|-----------|------|
| 5.1 | Twitter followers | 0 | 500 M1, 5K M3 | Twitter analytics | Daily | No | LAGGING |
| 5.2 | Twitter impressions | 0 | 10K/week | Twitter analytics | Daily | No | LEADING |
| 5.3 | Twitter engagement rate | 0% | 2-3% M1, 5%+ M3 | (likes+RT+replies) / impressions | Daily | No | LAGGING |
| 5.4 | Twitter warmup day | 0 | Day 21 = full posting | twitter_warmup_state.json | Daily | No | LEADING |
| 5.5 | TikTok followers | 0 | 1K M1, 10K M3 | TikTok analytics | Daily | No | LAGGING |
| 5.6 | TikTok views (total) | 0 | 100K M1 | TikTok analytics | Daily | No | LEADING |
| 5.7 | Reddit karma | 0 | Track | Reddit profile | Daily | No | LAGGING |
| 5.8 | Reddit post upvotes (avg) | 0 | 10+ avg | Reddit analytics | Daily | No | LAGGING |
| 5.9 | Pinterest monthly views | 0 | 10K M3 | Pinterest analytics | Weekly | No | LEADING |
| 5.10 | Pinterest click-through rate | 0% | 1-3% | Pinterest analytics | Weekly | No | LAGGING |
| 5.11 | YouTube subscribers | 0 | 100 M1, 1K M3 | YouTube Studio | Weekly | No | LAGGING |
| 5.12 | YouTube watch hours | 0 | 4,000 (monetization threshold) | YouTube Studio | Weekly | No | LEADING |
| 5.13 | Profile views (all platforms) | 0 | 2K-5K M1, 10K-20K M3 | Sum across platform analytics | Daily | No | LEADING |
| 5.14 | Followers gained (all platforms) | 0 | 500-2K M1, 5K-10K M3 | Sum across platform analytics | Daily | No | LAGGING |
| 5.15 | Instagram followers | 0 | Track | IG analytics | Daily | No | LAGGING |

---

## 6. AFFILIATE (Health/Telehealth/Supplement Vertical)

| # | KPI | Current | Target | How to Measure | Freq | Batchable | Type |
|---|-----|---------|--------|----------------|------|-----------|------|
| 6.1 | Affiliate clicks per day | 0 | 50/day M1, 200/day M3 | Affiliate dashboard click reports (all programs) | Daily | No | LEADING |
| 6.2 | Affiliate conversions per day | 0 | 1-2/day M1, 5-10/day M3 | Affiliate dashboard conversion reports | Daily | No | LAGGING |
| 6.3 | Affiliate revenue per day | $0 | $5-10/day M1, $30-50/day M3 | Sum across affiliate dashboards | Daily | No | LAGGING |
| 6.4 | Affiliate revenue per week | $0 | $35-70/wk M1, $200-350/wk M3 | Sum across affiliate dashboards | Weekly | No | LAGGING |
| 6.5 | Affiliate revenue per month | $0 | $140-300 M1, $1K-1.5K M3 | Sum across affiliate dashboards | Monthly | No | LAGGING |
| 6.6 | CPA by program: Instantly | N/A | Track | Instantly affiliate portal: revenue / conversions | Monthly | No | LAGGING |
| 6.7 | CPA by program: Beehiiv | N/A | Track | Beehiiv affiliate portal: revenue / conversions | Monthly | No | LAGGING |
| 6.8 | CPA by program: SEMrush | N/A | Track | SEMrush affiliate portal: revenue / conversions | Monthly | No | LAGGING |
| 6.9 | CPA by program: Saleshandy | N/A | Track | Saleshandy affiliate portal | Monthly | No | LAGGING |
| 6.10 | CPA by program: Supplement (each) | N/A | Track | Per-supplement affiliate portal | Monthly | No | LAGGING |
| 6.11 | CPA by program: Telehealth (each) | N/A | Track | Per-telehealth affiliate portal | Monthly | No | LAGGING |
| 6.12 | Top converting page | N/A | Identify by M1 | Analytics: page with highest conversion rate | Weekly | No | LAGGING |
| 6.13 | Top converting traffic source | N/A | Identify by M1 | Analytics: utm_source with highest conversions | Weekly | No | LAGGING |
| 6.14 | SEO article count (affiliate) | 8 landing pages | 20 M1, 50 M3 | Count files in LANDING/affiliate-pages/ | Weekly | YES (30d) | LEADING |
| 6.15 | Keyword rankings: top 20 keywords | Unranked | Page 1 for 5+ by M6 | Google Search Console / Ahrefs / SEMrush | Weekly | No | LAGGING |
| 6.16 | Reddit post engagement (affiliate) | 0 | 10+ upvotes avg | Reddit analytics on affiliate-related posts | Daily | No | LEADING |
| 6.17 | Twitter post engagement (affiliate) | 0 | 50+ impressions avg | Twitter analytics on affiliate-related tweets | Daily | No | LEADING |
| 6.18 | Affiliate programs active | 0 | 5+ | Count of signed-up affiliate programs | Monthly | No | LEADING |
| 6.19 | Affiliate cookie utilization | 0% | Track | conversions_within_cookie_window / total_clicks | Monthly | No | LAGGING |
| 6.20 | Affiliate page organic traffic | 0 | 500/mo M3, 5K/mo M6 | Google Search Console impressions+clicks | Weekly | No | LEADING |
| 6.21 | Supplement commission per sale (avg) | $0 | $10-42 | total_supplement_revenue / supplement_conversions | Monthly | No | LAGGING |
| 6.22 | Telehealth commission per sale (avg) | $0 | Track | total_telehealth_revenue / telehealth_conversions | Monthly | No | LAGGING |
| 6.23 | Affiliate link click-through rate | 0% | 3-5% | affiliate_clicks / page_visits | Weekly | No | LAGGING |
| 6.24 | Affiliate content pieces published | 0 | 5/week | Count affiliate-related posts across platforms | Weekly | YES (30d) | LEADING |

---

## 7. SEO

| # | KPI | Current | Target | How to Measure | Freq | Batchable | Type |
|---|-----|---------|--------|----------------|------|-----------|------|
| 7.1 | Pages indexed (Google) | 0 (surge blocks) | 50+ M1 post-migration | Google Search Console | Weekly | No | LEADING |
| 7.2 | Organic impressions | 0 | 5K/mo M1, 50K/mo M6 | Google Search Console | Weekly | No | LEADING |
| 7.3 | Organic clicks | 0 | 200/mo M1, 5K/mo M6 | Google Search Console | Weekly | No | LEADING |
| 7.4 | Average position (top keywords) | Unranked | Top 20 for 10+ keywords | Google Search Console | Weekly | No | LEADING |
| 7.5 | Sites deployed (total) | 114 | Track | DEPLOYMENT_URLS.md count | Weekly | No | LEADING |
| 7.6 | Sites with working robots.txt | 0 (surge blocks) | 100% post-migration | curl robots.txt on each domain | Weekly | No | LEADING |
| 7.7 | Sitemap URLs (total) | 188 | 300+ | Count URLs across all sitemaps | Weekly | YES (30d) | LEADING |
| 7.8 | Pages with structured data (JSON-LD) | 21 | 50+ | Grep for application/ld+json across builds | Weekly | YES (30d) | LEADING |
| 7.9 | Backlinks (total) | 0 | Track | Ahrefs/SEMrush | Monthly | No | LEADING |
| 7.10 | Domain authority (main domains) | 0 | Track | Ahrefs/SEMrush | Monthly | No | LAGGING |
| 7.11 | Bounce rate (avg across sites) | N/A | <60% | Analytics | Weekly | No | LAGGING |
| 7.12 | Time on page (avg) | N/A | >2 min | Analytics | Weekly | No | LAGGING |
| 7.13 | Hosting platform (post-migration) | surge.sh (blocked) | Cloudflare/Netlify | Deployment config | One-time | No | LEADING |

---

## 8. EMAIL

| # | KPI | Current | Target | How to Measure | Freq | Batchable | Type |
|---|-----|---------|--------|----------------|------|-----------|------|
| 8.1 | Email list size (total) | 0 | 500 M1, 2K M3, 5K M6 | Beehiiv subscriber count | Daily | No | LEADING |
| 8.2 | Email open rate | 0% | 30-40% | Beehiiv analytics | Per send | No | LAGGING |
| 8.3 | Email click rate | 0% | 3-5% | Beehiiv analytics | Per send | No | LAGGING |
| 8.4 | Email sequences active | 0 | 5+ | Count active drip sequences | Weekly | YES (30d) | LEADING |
| 8.5 | Email unsubscribe rate | N/A | <2% | Beehiiv analytics | Per send | No | LAGGING |
| 8.6 | Email revenue per send | $0 | $0.10-0.50 | revenue / emails_sent | Per send | No | LAGGING |
| 8.7 | Email ROI | N/A | $42/$1 (DMA benchmark) | email_revenue / email_cost | Monthly | No | LAGGING |
| 8.8 | Cold email sequences deployed | 9 | 15+ | Count files in EMAIL/sequences/ | Weekly | YES (30d) | LEADING |
| 8.9 | Triggering event sequences | Track | 10+ | Count files in EMAIL/triggering_events/ | Weekly | YES (30d) | LEADING |

---

## 9. NSFW / AI CHARACTER CONTENT

| # | KPI | Current | Target | How to Measure | Freq | Batchable | Type |
|---|-----|---------|--------|----------------|------|-----------|------|
| 9.1 | Platform accounts active | 0 | 3-5 (Fanvue/Fansly/CashApp/Telegram/Patreon) | Manual count of active accounts | Weekly | No | LEADING |
| 9.2 | Total subscribers/followers | 0 | 200 M1, 2K M3 | Sum across platform dashboards | Daily | No | LEADING |
| 9.3 | Content pieces per day | 0 | 3-5/day per persona | Count published items across platforms | Daily | YES (30d) | LEADING |
| 9.4 | Revenue per platform: Fanvue | $0 | $500 M1, $3K M3 | Fanvue creator dashboard | Daily | No | LAGGING |
| 9.5 | Revenue per platform: Fansly | $0 | $200 M1, $1K M3 | Fansly creator dashboard | Daily | No | LAGGING |
| 9.6 | Revenue per platform: CashApp/Crypto | $0 | $50-200 M1 | CashApp transaction history | Daily | No | LAGGING |
| 9.7 | Revenue per platform: Telegram Stars | $0 | Track | Telegram creator tools | Daily | No | LAGGING |
| 9.8 | Revenue per platform: Patreon | $0 | Track | Patreon creator dashboard | Daily | No | LAGGING |
| 9.9 | Average tribute/tip amount | $0 | $20-100 | total_tributes / tribute_count | Weekly | No | LAGGING |
| 9.10 | Subscriber conversion rate | 0% | 5-10% | paying_subs / total_followers | Weekly | No | LAGGING |
| 9.11 | Compliance: FTC disclosures in place | No | Yes (all profiles) | Manual audit: AI disclosure visible on all bios/profiles | Weekly | No | LEADING |
| 9.12 | Compliance: platform ToS adherence | N/A | 100% | Manual audit per platform rules | Weekly | No | LEADING |
| 9.13 | Compliance: age verification active | N/A | Yes (all platforms) | Platform settings check | Weekly | No | LEADING |
| 9.14 | AI persona count (active) | 0 | 5-10 | Count of personas posting regularly | Weekly | No | LEADING |
| 9.15 | DMs answered per day | 0 | Track | Platform message analytics | Daily | Daily-only | LEADING |
| 9.16 | Churn rate (monthly) | N/A | <20% | cancelled_subs / total_subs | Monthly | No | LAGGING |

---

## 10. AUTOMATION HEALTH

| # | KPI | Current | Target | How to Measure | Freq | Batchable | Type |
|---|-----|---------|--------|----------------|------|-----------|------|
| 10.1 | Cron jobs active | ~112 | 10+ required minimum | crontab -l \| grep -v '#' \| wc -l | Daily | No | LEADING |
| 10.2 | Launchd agents active | Track | Track | launchctl list \| grep printmaxx | Daily | No | LEADING |
| 10.3 | Loop closer: all 4 loops OK | Track | All OK | python3 AUTOMATIONS/loop_closer.py --status | Daily | No | LEADING |
| 10.4 | Loop: Decision Execution | Track | OK (not DEAD/STALE) | loop_closer.py --status | Daily | No | LEADING |
| 10.5 | Loop: Feedback Tracking | Track | OK | loop_closer.py --status | Daily | No | LEADING |
| 10.6 | Loop: Pipeline Advancement | Track | OK | loop_closer.py --status | Daily | No | LEADING |
| 10.7 | Loop: Soul Drift | Track | OK | loop_closer.py --status | Daily | No | LEADING |
| 10.8 | Alpha entries total | ~48,873 | Growing daily | LEDGER/ALPHA_STAGING.csv row count | Daily | No | LEADING |
| 10.9 | Alpha entries pending review | ~3,559 | <500 | ALPHA_STAGING.csv where status=PENDING_REVIEW | Daily | No | LAGGING |
| 10.10 | Alpha entries approved | Track | Track | ALPHA_STAGING.csv where status=APPROVED | Daily | No | LAGGING |
| 10.11 | Alpha entries processed per day | ~50-100 | 100/day | alpha_auto_processor.py output | Daily | No | LAGGING |
| 10.12 | CEO agent cycle count | Track | Every 2h | ceo_state.json cycle_count | Daily | No | LEADING |
| 10.13 | Swarm agents active | 3 (conservation) | 10+ in GROWTH mode | swarm_state.json active count | Daily | No | LEADING |
| 10.14 | Venture pipelines running | 8 types | 8 types healthy | venture_autonomy.py --status | Daily | No | LEADING |
| 10.15 | Scripts total (AUTOMATIONS/) | ~392 | <400 (consolidate) | ls AUTOMATIONS/*.py \| wc -l | Weekly | No | LAGGING |
| 10.16 | Dead scripts (no caller) | ~50% | <10% | Scripts not in cron or imported by others | Monthly | No | LAGGING |
| 10.17 | OAuth/API key failures | Track | 0 | grep ERROR in agent logs | Daily | No | LAGGING |
| 10.18 | Throttle mode | EFFICIENT | Match phase | throttle_toggle.py --json | Daily | No | LEADING |
| 10.19 | Token burn estimate (daily) | Track | <budget | throttle_toggle.py --estimate | Daily | No | LEADING |
| 10.20 | Quality gate pass rate | Track | 100% | quality_gate.py output | Per run | No | LAGGING |
| 10.21 | System health score | Track | All green | system_health_monitor.py --quick | Daily | No | LAGGING |
| 10.22 | Disk usage (project) | ~31GB | <50GB | du -sh on project root | Weekly | No | LAGGING |
| 10.23 | Intelligence catalog docs | 487 | Growing | INTELLIGENCE_CATALOG.json doc count | Weekly | No | LEADING |
| 10.24 | Cron watchdog status | Track | Running hourly | launchd com.printmaxx.cron-watchdog | Daily | No | LEADING |
| 10.25 | Guardian safety commits | Daily | Daily | git log --oneline \| grep Guardian | Daily | No | LAGGING |
| 10.26 | Backup status (last full) | Track | Weekly | ~/PRINTMAXX_BACKUPS/ latest timestamp | Weekly | No | LAGGING |
| 10.27 | Backup status (last incremental) | Track | Nightly | ~/PRINTMAXX_BACKUPS/ latest timestamp | Daily | No | LAGGING |

---

## 11. DIGITAL PRODUCTS

| # | KPI | Current | Target | How to Measure | Freq | Batchable | Type |
|---|-----|---------|--------|----------------|------|-----------|------|
| 11.1 | Products built | 16+ | Track | Count in DIGITAL_PRODUCTS/ready_to_sell/ | Weekly | No | LEADING |
| 11.2 | Products listed (Gumroad) | 0 | 14 | Gumroad dashboard | Weekly | No | LEADING |
| 11.3 | Products listed (Whop) | 0 | 8 | Whop dashboard | Weekly | No | LEADING |
| 11.4 | Products listed (Etsy) | 0 | 10+ | Etsy dashboard | Weekly | No | LEADING |
| 11.5 | Product page views | 0 | Track | Gumroad/Whop analytics | Daily | No | LEADING |
| 11.6 | Product conversion rate | 0% | 2-5% | purchases / page_views | Weekly | No | LAGGING |
| 11.7 | Average product price | $15-49 | $25-50 | total_revenue / units_sold | Monthly | No | LAGGING |
| 11.8 | Products with reviews | 0 | 5+ | Platform review counts | Weekly | No | LAGGING |
| 11.9 | Product Hunt launches completed | 0 | 1/2 weeks | PH dashboard | Monthly | No | LEADING |

---

## 12. SERVICES / FREELANCE

| # | KPI | Current | Target | How to Measure | Freq | Batchable | Type |
|---|-----|---------|--------|----------------|------|-----------|------|
| 12.1 | Fiverr active gigs | 0 | 10 | Fiverr dashboard | Weekly | No | LEADING |
| 12.2 | Upwork active proposals | 0 | 10-20 | Upwork dashboard | Daily | No | LEADING |
| 12.3 | Fiverr reviews count | 0 | 5 M1, 20 M3 | Fiverr profile | Weekly | No | LAGGING |
| 12.4 | Upwork job success score | N/A | 90%+ | Upwork profile | Weekly | No | LAGGING |
| 12.5 | Active freelance clients | 0 | 3-5 M1 | Manual tracking | Weekly | No | LAGGING |
| 12.6 | Freelance hourly rate (effective) | $0 | $50-100/hr M1, $100-200/hr M3 | revenue / hours_worked | Weekly | No | LAGGING |
| 12.7 | Local biz deals closed | 0 | 1-2/mo M1, 4-6/mo M3 | CRM/lead tracker | Monthly | No | LAGGING |
| 12.8 | MVP builds completed | 0 | 1-2/mo | Project tracker | Monthly | No | LAGGING |
| 12.9 | EAS pipeline leads | 0 | Track | eas_lead_pipeline.py output | Weekly | No | LEADING |

---

## 13. COMMUNITY

| # | KPI | Current | Target | How to Measure | Freq | Batchable | Type |
|---|-----|---------|--------|----------------|------|-----------|------|
| 13.1 | Discord members | 0 | 50 M1, 500 M3 | Discord server stats | Weekly | No | LEADING |
| 13.2 | Skool members | 0 | 20 M1, 100 M3 | Skool dashboard | Weekly | No | LEADING |
| 13.3 | Telegram VIP subscribers | 0 | 10 M1, 100 M3 | Telegram group stats | Weekly | No | LEADING |
| 13.4 | Paying community members (total) | 0 | 10 M1, 50 M3 | Sum across platforms | Weekly | No | LAGGING |
| 13.5 | Community churn rate | N/A | <15%/mo | cancelled / total per month | Monthly | No | LAGGING |
| 13.6 | Community engagement (messages/day) | 0 | 20+/day | Platform analytics | Daily | No | LEADING |

---

## 14. E-COMMERCE

| # | KPI | Current | Target | How to Measure | Freq | Batchable | Type |
|---|-----|---------|--------|----------------|------|-----------|------|
| 14.1 | Etsy listings active | 0 | 50+ M1 | Etsy dashboard | Weekly | YES (30d) | LEADING |
| 14.2 | Amazon KDP books published | 0 | 5+ M1 | KDP dashboard | Weekly | YES (30d) | LEADING |
| 14.3 | TikTok Shop products listed | 0 | 10+ | TikTok Shop dashboard | Weekly | No | LEADING |
| 14.4 | Print-on-demand designs active | 0 | 50+ | Redbubble/TeeSpring dashboard | Weekly | YES (30d) | LEADING |
| 14.5 | Average order value | $0 | $15-40 | total_revenue / total_orders | Weekly | No | LAGGING |
| 14.6 | PLR products rebranded and listed | 0 | 5-10 | Tracking CSV | Monthly | YES (30d) | LEADING |

---

## BATCHABLE CHECKLIST (30-day sprint items)

Items marked YES above can be pre-built in bulk. Sorted by category:

**Content (batch-create 30 days of content)**
- [ ] 90-150 tweets (3-5/day x 30d)
- [ ] 30 threads (1/day x 30d)
- [ ] 90-150 Reddit posts (3-5/day x 30d)
- [ ] 60-90 TikTok scripts (2-3/day x 30d)
- [ ] 150-300 Pinterest pin designs (5-10/day x 30d)
- [ ] 4 newsletter issues (1/week x 4wk)
- [ ] 8-12 blog articles (2-3/week x 4wk)
- [ ] 1,500+ creative variations (50/wk x 4wk)

**NSFW / AI Character Content (batch-create)**
- [ ] 90-150 content pieces per persona (3-5/day x 30d)

**Affiliate (batch-create)**
- [ ] 12-20 SEO articles for affiliate pages
- [ ] 20+ affiliate content pieces for social distribution

**SEO (batch-create)**
- [ ] Sitemaps for all new pages
- [ ] JSON-LD structured data for 30+ pages

**E-Commerce (batch-create)**
- [ ] 50+ Etsy digital download listings
- [ ] 5+ KDP book interiors
- [ ] 50+ POD designs
- [ ] 5-10 PLR rebrand packages

**Email (batch-create)**
- [ ] 6+ email drip sequences
- [ ] 10+ triggering event sequences

**NOT batchable (rate-limited or time-dependent)**
- All revenue metrics (real-time)
- Cold emails (platform daily limits)
- AI calls (Bland daily limits)
- Freelance proposals (per-opportunity)
- Reddit comments (must be contextual)
- LinkedIn outreach (platform limits)
- DM responses (real-time)
- All analytics/ranking data (time-dependent)
- Platform follower counts (organic growth)

---

---

## INDICATOR TYPE LEGEND

**LEADING** = Predicts future revenue. These are the inputs you control directly. If leading indicators are moving up, revenue will follow (with a delay). Focus daily effort here.

**LAGGING** = Measures past results. These confirm whether your leading indicators are actually working. If leading indicators are up but lagging indicators stay flat for 2+ weeks, something in the funnel is broken.

**Rule of thumb at $0 revenue:** Ignore all lagging indicators except Stripe balance (CP-1). Obsess over leading indicators. You can't optimize conversion rates when you have zero traffic. Get the volume first, optimize later.

---

*Consumed by: CEO Agent, Decision Engine, Daily Digest, Session Briefing, Control Panel (localhost:9999)*
*Source data: control_panel.py, KPI_DASHBOARD.md, PERSISTENT_TASK_TRACKER.md, REVENUE_TRACKER.csv, platform dashboards*
*Update: Weekly manual review. Daily automated via daily_digest.py + control_panel.py.*
