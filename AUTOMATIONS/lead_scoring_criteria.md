# Lead Scoring Criteria - Savvy Lead Scraper

**Script:** `AUTOMATIONS/savvy_lead_scraper.py`
**Version:** 1.0 (2026-02-10)
**Total possible score:** 100 points across 3 dimensions

---

## Scoring Philosophy

Most lead scrapers find businesses. This one finds businesses that are **likely to buy a website redesign**. The difference is signal stacking: a dental office with 80 Google reviews, no mobile site, active Facebook page, and a findable owner email is a 10x better lead than a random plumber with no web presence and no contact info.

Three dimensions, each measuring something different:

1. **Website Quality (40 pts):** How bad is their current web presence? Worse = more likely to need help.
2. **Business Viability (30 pts):** Can they actually afford to pay $500-$5,000? Established with revenue = yes.
3. **Conversion Likelihood (30 pts):** Can we actually reach them and close them? Contact info + timing.

---

## Dimension 1: Website Quality Signals (40 points max)

Measures how poor the business's current web presence is. Higher score = worse website = better prospect.

| Signal | Points | Detection Method | Rationale |
|--------|--------|-----------------|-----------|
| No website at all (just Facebook/Yelp) | +15 | URL returns 4xx/5xx or no URL discovered | Easiest sell. "You're invisible to 70% of customers." |
| Not mobile responsive | +12 | Missing `<meta name="viewport" content="width=device-width">` and no responsive CSS framework detected | 60%+ traffic is mobile. Non-responsive = losing customers daily. |
| Slow load time >5s | +10 | Timed HTTP GET request | Every 1s delay = 7% conversion drop (Google data). >5s is catastrophic. |
| Slow load time 3-5s | +5 | Timed HTTP GET request | Still bad but not crisis-level. |
| No SSL/HTTPS | +8 | SSL socket handshake to port 443 fails | Chrome shows "Not Secure" warning. Kills trust instantly. |
| Generic/free template | +8 | Detect Wix free tier (wixsite.com subdomain), default WordPress themes (twentytwenty etc.), Weebly, GoDaddy website builder, Jimdo, Site123 | Business owner built it themselves years ago. Ready for upgrade. |
| Cheap platform (no free tier indicators) | +4 | Detect Wix paid, Weebly paid, GoDaddy paid | Better than free tier but still limited. |
| 2+ broken images | +5 | HEAD request to first 10 img src URLs, check for 4xx | Neglected site. Owner not maintaining it. |
| 1 broken image | +2 | Same as above | Minor neglect signal. |
| No Google Analytics or tracking | +3 | Search HTML for GA/GTM/FB pixel/Hotjar/Clarity patterns | Not measuring = not optimizing = opportunity for us. |
| Copyright date 3+ years old | +5 | Regex extract copyright year from HTML | Site hasn't been touched. Owner knows it's outdated. |
| Copyright date 2 years old | +3 | Same regex | Slightly stale. |
| Poor SEO score (<30/100) | +5 | Check: title tag, meta desc, H1, H2s, OG tags, alt text, canonical, schema | Major SEO gaps = losing search traffic. |
| Weak SEO score (30-49/100) | +3 | Same checks | Some effort but room for improvement. |

**Cap:** 40 points max (even if signals add to more).

**Key insight:** A business with NO website gets 15 points here. That seems low, but it's offset by high conversion likelihood scores (social-only businesses are the easiest close). The scoring is calibrated so that "has a terrible website they paid for" scores higher total than "has no website" because the former has demonstrated willingness to pay for web presence.

---

## Dimension 2: Business Viability Signals (30 points max)

Measures whether this business can actually pay for services and will still be around in 6 months.

| Signal | Points | Detection Method | Rationale |
|--------|--------|-----------------|-----------|
| 50+ Google reviews | +10 | Extracted from Google Maps/search results | Established business with real customer flow. Can afford $500-$5,000. |
| 20-49 Google reviews | +5 | Same | Decent establishment. Probably viable. |
| 10-19 Google reviews | +3 | Same | Getting started but still viable. |
| Rating 3.5-4.5 stars | +5 | Extracted from Google results | Sweet spot: good enough to survive, not so good they're complacent. 5-star businesses often think they don't need help. |
| Rating 4.5+ with 50+ reviews | +3 | Combined check | Established and excellent. Still a prospect but may be harder to convince. |
| High-margin industry | +10 | Lookup against constant set: dental, legal, medical, HVAC, real estate, roofing, remodeling, accounting | These industries have high customer LTV. A dentist's patient is worth $3,000+/year. They can justify $2,000-$5,000 for a website. |
| Decent-margin industry (avg deal >= $1,000) | +5 | Lookup from INDUSTRY_CONFIG | Medium revenue per client. Can still afford $500-$1,500. |
| Has a website (trying to be online) | +3 | Successfully fetched a webpage | Demonstrated intent to have web presence = higher propensity to pay for improvement. |
| Phone number visible on site | +2 | Phone regex extraction from page text | Real business that wants calls. Not abandoned. |

**Cap:** 30 points max.

**Key insight:** High-margin industry is the single biggest viability signal (+10). A dental office with 0 reviews still scores better than a restaurant with 100 reviews because the dental office will pay 3-5x more per project. This is about deal economics, not just lead quality.

---

## Dimension 3: Conversion Likelihood Signals (30 points max)

Measures how likely we are to actually reach this person and close a deal.

| Signal | Points | Detection Method | Rationale |
|--------|--------|-----------------|-----------|
| Owner/personal email found | +10 | Email regex extraction, then filter out generic prefixes (info@, contact@, admin@, support@, etc.) | Direct line to decision maker. 3-5x higher response rate than info@. |
| Generic email found (info@, contact@) | +4 | Email regex, matches generic prefix list | At least we can reach someone. But it'll sit in a shared inbox. |
| Phone number prominent | +5 | Phone regex extraction from page text | Can cold call as backup. Also signals active business. |
| Active on social but weak website | +8 | Has Facebook/Instagram links on site AND (not mobile responsive OR generic template OR poor SEO OR no SSL) | This is the money signal. They CARE about marketing (active social). They just haven't fixed their website. Warm lead. |
| Has social media but NO website | +10 | Social links found via Google but no functioning website | Even better than above. They're marketing-aware and literally don't have a site. |
| Approaching peak season | +5 | Month-based lookup per industry (e.g., HVAC in May-Jul, accounting in Jan-Mar) | Urgency is higher. "You need this before summer rush." |
| Month before peak season | +3 | Same lookup, shifted -1 month | Building urgency. |
| Thin content (<200 words) | +3 | Word count of page text | Site exists but barely. Easy to demonstrate improvement. |
| No schema markup | +2 | Check for `<script type="application/ld+json">` | Modern SEO requirement they're missing. Good conversation opener about AI search. |

**Cap:** 30 points max.

---

## Score Tiers

| Tier | Score Range | Meaning | Action |
|------|------------|---------|--------|
| **HOT** | 70-100 | Multiple strong signals across all dimensions. High probability of converting. | Prioritize immediately. Build demo page. Email within 24 hours. |
| **WARM** | 50-69 | Good signals but missing some dimension. Still worth pursuing. | Email within 1 week. Follow up after 3 days. |
| **COOL** | 30-49 | Some signals but not enough urgency. | Add to nurture list. Email when batch is slow. |
| **COLD** | 0-29 | Few signals. Either well-optimized already or not viable. | Skip or deprioritize. |

---

## Email Template Routing

Based on scoring signals, the scraper recommends which cold email template to use:

| Template | Trigger Condition | Location |
|----------|------------------|----------|
| **A** - Direct demo | Has website, is mobile responsive (needs quality upgrade) | `MONEY_METHODS/LOCAL_BIZ/COLD_EMAIL_DEMO_TEMPLATE.md` Template A |
| **B** - Problem-first | Has website but NOT mobile responsive (clear problem to point out) | Template B |
| **C** - No website | No website at all | Template C |

Email variant (industry-specific language) is also assigned:
- `healthcare` (dental, medical, veterinary)
- `professional_services` (legal, accounting)
- `home_services` (HVAC, plumbing, electrical, roofing, remodeling)
- `real_estate`
- `hospitality` (restaurant)
- `fitness` (gym)
- `beauty` (salon)
- `automotive` (auto repair)
- `general` (fallback)

---

## Industry Economics

| Industry | Avg Deal Range | Est. Close Rate | Margin Tier | Seasonal Peaks |
|----------|---------------|-----------------|-------------|----------------|
| dental | $2,000-$5,000 | 20% | HIGH | Year-round |
| legal | $3,000-$10,000 | 15% | HIGH | Year-round |
| hvac | $1,500-$3,000 | 25% | HIGH | May-Jul, Nov-Dec |
| plumbing | $1,500-$3,000 | 25% | MEDIUM | Year-round |
| realestate | $1,000-$3,000 | 20% | HIGH | Feb-Jun |
| restaurant | $500-$2,000 | 12% | LOW | Mar-May, Nov |
| gym | $1,000-$2,500 | 18% | MEDIUM | Jan-Feb, Sep |
| medical | $2,000-$5,000 | 15% | HIGH | Year-round |
| autorepair | $800-$2,000 | 20% | MEDIUM | Year-round |
| roofing | $1,500-$3,000 | 22% | HIGH | Mar-May, Sep-Oct |
| electrician | $1,200-$2,500 | 22% | MEDIUM | Year-round |
| salon | $500-$1,500 | 15% | LOW | Year-round |
| remodeling | $2,000-$5,000 | 20% | HIGH | Feb-May |
| veterinary | $1,500-$3,000 | 18% | MEDIUM | Year-round |
| accounting | $1,500-$4,000 | 18% | HIGH | Jan-Mar, Oct |

---

## Expected Revenue Calculation

The pipeline summary calculates expected revenue as:

```
For each lead:
  avg_deal = (deal_low + deal_high) / 2
  base_close_rate = industry close rate
  score_multiplier = {HOT: 1.5, WARM: 1.0, COOL: 0.5, COLD: 0.2}
  expected = avg_deal * base_close_rate * score_multiplier

Pipeline value = sum of all expected values
```

This is a probabilistic estimate. 50 HOT dental leads at $3,500 avg deal, 20% close rate, 1.5x multiplier = $52,500 expected pipeline value. Actual results depend on outreach execution.

---

## Refinement Guide (for future agents)

### Signals to Add

These signals would improve scoring but require more infrastructure:

1. **Google Business Profile activity** - Requires Google Places API ($17/1000 requests). Check for recent posts, photos, Q&A. Active GBP = engaged business owner = better prospect.

2. **Competitor comparison** - Scrape top 3 competitors in same city+industry. If competitor has better website, prospect is losing business. +7 points.

3. **Social media follower count** - Requires platform API access. High followers + bad website = high conversion likelihood.

4. **Domain age via WHOIS** - Old domain + bad website = long-overdue upgrade. Python `python-whois` library.

5. **Page speed via Lighthouse** - More accurate than simple load time. Requires headless Chrome.

6. **Review sentiment analysis** - Negative reviews mentioning "couldn't find website" or "hard to book" = they know they have a problem.

### Signals to Adjust

After running 100+ leads through the pipeline and tracking actual conversions:

1. If close rate on "no website" leads is lower than expected, reduce the +15 to +10 (they may not be online-aware enough to value a website).

2. If HVAC/plumbing consistently close faster, increase seasonal boost from +5 to +7.

3. If generic email leads never convert, reduce from +4 to +1 (not worth the effort vs. owner email leads).

### Data Quality Improvements

1. Google sometimes blocks scraping. If discovery returns 0 results, the scraper should suggest manual URL compilation or an alternative data source (Yelp API, Google Places API).

2. Rate limiting should be adaptive: if getting 429s, increase delay automatically.

3. Add a deduplication layer that checks against previous scrape outputs to avoid emailing the same business twice.

---

## Integration with Existing Tools

| Existing Tool | How This Integrates |
|---------------|-------------------|
| `local_biz_pipeline.py` | Feed savvy scraper output CSV directly into pipeline for page generation + email creation |
| `local_biz_website_scraper.py` | Savvy scraper supersedes this for lead scoring. Old scraper still useful for deep single-site analysis. |
| `personalize_template.py` | Use savvy scraper output to personalize templates at scale |
| `COLD_EMAIL_DEMO_TEMPLATE.md` | Template recommendation maps to templates A/B/C in this doc |
| `LEDGER/OUTREACH_PIPELINE.csv` | Import scored leads into pipeline tracking |
| `FINANCIALS/REVENUE_TRACKER.csv` | Track closed deals from scored leads |

---

## FAQ

**Q: Why not use Google Places API?**
A: Costs money ($17/1000 requests = $0.85 for 50 leads). The free scraping approach works for bootstrapping. Upgrade to Places API when revenue justifies it.

**Q: Why the 2-second rate limit?**
A: Google will block faster requests. 2 seconds is the minimum polite interval. Increase to 3-5s if getting blocked.

**Q: What if Google returns 0 results?**
A: Use `--urls-file` mode instead. Manually compile URLs from Google Maps, Yelp, Yellow Pages, local chamber of commerce directories. The scraper still scores them.

**Q: How accurate is the scoring?**
A: Calibrated on heuristics, not historical conversion data (we have none yet). Track actual conversions and recalibrate after 100 leads. The signals are directionally correct.

**Q: Can this be a ralph loop?**
A: Yes. Create a ralph loop that runs `--full-blast` nightly and checks for new leads with score >60. Output to `ralph/loops/lead_gen/output/`. Human reviews and approves outreach.
