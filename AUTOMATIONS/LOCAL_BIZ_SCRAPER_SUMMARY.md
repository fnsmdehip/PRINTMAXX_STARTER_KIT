# Local Business Website Scraper - Complete Package

## Files Created

### 1. Main Script
**`AUTOMATIONS/local_biz_website_scraper.py`** (534 lines)

Python script that scrapes and analyzes local business websites.

**Key features:**
- Checks 15+ site quality signals (mobile, SSL, SEO, AI-SEO, tech stack, contact info)
- Scores sites 0-100 (lower = more likely prospect)
- Estimates budget potential based on business category
- Extracts email/phone for outreach
- Outputs prioritized prospect list (HIGH/MEDIUM/LOW)
- Rate limiting and error handling built-in

**Usage:**
```bash
python3 AUTOMATIONS/local_biz_website_scraper.py --demo  # See output format
python3 AUTOMATIONS/local_biz_website_scraper.py --urls-file urls.csv  # Real usage
```

### 2. Documentation
**`AUTOMATIONS/LOCAL_BIZ_SCRAPER_README.md`** (Full technical docs)
- Complete feature list
- Scoring formulas
- Budget estimation logic
- Advanced usage examples
- Troubleshooting
- Future enhancements

**`AUTOMATIONS/LOCAL_BIZ_SCRAPER_QUICKSTART.md`** (Fast start guide)
- 30-second setup
- 3-step workflow
- Email templates
- ROI math
- Scaling tips

### 3. Email Templates
**`AUTOMATIONS/LOCAL_BIZ_EMAIL_TEMPLATES.md`** (10 templates + phone script)
- Mobile-responsive issue
- No SSL certificate
- Poor SEO score
- Old/outdated site
- No AI-SEO readiness
- DIY platform limitations
- High priority prospect
- Direct offer
- Local competitor angle
- Follow-up templates
- Phone script
- Response handling

### 4. Sample Data
**`AUTOMATIONS/sample_business_urls.csv`**

Example input CSV with 8 sample businesses showing correct format.

### 5. Output Directory
**`AUTOMATIONS/output/`**

Where results are saved: `local_biz_prospects.csv`

---

## Quick Start (Copy/Paste)

```bash
# Install dependencies
pip install requests beautifulsoup4 tqdm

# Test with demo
python3 AUTOMATIONS/local_biz_website_scraper.py --demo

# Create your prospect list (urls.csv)
# Then run:
python3 AUTOMATIONS/local_biz_website_scraper.py --urls-file urls.csv

# Review results
open AUTOMATIONS/output/local_biz_prospects.csv
```

---

## How It Works

### Input
CSV with business URLs:
```csv
url,business_name,category,city
https://example-dental.com,Main St Dental,dentist,Austin TX
```

### Processing (Per URL)
1. **Load site** - Request with timeout, follow redirects
2. **Check SSL** - Valid certificate?
3. **Parse HTML** - BeautifulSoup extraction
4. **Mobile check** - Viewport meta tag present?
5. **SEO audit** - Title, meta description, H1, OG tags, image alt text
6. **AI-SEO audit** - Schema.org, FAQ schema, breadcrumbs, structured headings
7. **Tech detection** - WordPress, Wix, Squarespace, custom
8. **Freshness** - Copyright year, last modified header, content dates
9. **Activity check** - Phone visible, email visible, social links, recent content
10. **Contact extraction** - Email addresses, phone numbers
11. **Scoring** - Calculate 0-100 score (lower = needs more help)
12. **Budget estimation** - Based on category and site quality
13. **Prioritization** - HIGH/MEDIUM/LOW based on score + activity + contact found

### Output
CSV with 17 columns:
- Business info (name, url, city, category)
- Technical scores (site_score, seo_score, ai_seo_score)
- Feature flags (mobile_ready, has_ssl, appears_active)
- Technical details (tech_stack, last_updated_estimate)
- Contact info (email_if_found, phone_if_found)
- Outreach data (budget_estimate, outreach_priority, notes)

Sorted by priority (HIGH first) and score (lowest first).

---

## Scoring System

### Site Score (0-100, lower = better prospect)

Starts at 100, penalized for missing features:

| Missing Feature | Penalty |
|----------------|---------|
| Not mobile responsive | -25 |
| No SSL | -20 |
| Poor SEO (inversed) | up to -30 |
| No AI-SEO (inversed) | up to -25 |
| Old site (pre-2020) | -15 |

**Target prospects: Score < 40**

### SEO Score (0-100)

Points awarded for:
- Title tag (20)
- Meta description (20)
- H1 tag (20)
- Open Graph tags (20)
- Image alt text (20)

### AI-SEO Score (0-100)

Points awarded for:
- Schema.org markup (40)
- FAQ schema (20)
- Breadcrumbs (20)
- Structured headings (20)

### Priority Tiers

**HIGH** = Site score < 40 + appears active + email found
**MEDIUM** = Site score < 60 + appears active
**LOW** = Everything else

---

## Budget Estimation

Base budget by category:

| Category | Base Budget |
|----------|-------------|
| Lawyers/Doctors | $1,500-$2,000 |
| Real Estate | $1,200 |
| Restaurants | $800 |
| Home Services | $700-$900 |
| Salons/Gyms | $600-$1,000 |

Adjustments:
- Very poor site (score < 30): +30%
- DIY platform (Wix/Squarespace): -30%

---

## ROI Example

### Scenario: Dentist Outreach in Austin

**Inputs:**
- 100 dentist URLs (compiled manually from Google Maps)
- 5 minutes to run scraper

**Outputs:**
- 22 HIGH priority prospects (score < 40, active, email found)
- 38 MEDIUM priority prospects

**Outreach:**
- Email 22 HIGH priority with Template 7
- 5 respond (23% response rate)
- 2 calls booked
- 1 closes at $1,500

**Results:**
- Revenue: $1,500
- Time invested: 5 min (scraping) + 30 min (emails) + 1 hour (calls) = 1.5 hours
- **Hourly rate: $1,000/hour**

**Scale to 10 cities:**
- 1,000 dentists scraped
- 220 HIGH priority
- 50 responses
- 10 closes
- **Revenue: $15,000**
- **Time: 15 hours**
- **Hourly rate: $1,000/hour**

---

## Best Categories (Highest Budget)

Based on budget estimation logic:

1. **Lawyers** ($2,000) - High value, poor DIY sites common
2. **Doctors/Dentists** ($1,500) - High value, often outdated
3. **Real Estate** ($1,200) - Many agents, competitive
4. **Home Services** ($700-$900) - Plumbers, HVAC, electricians
5. **Gyms/Fitness** ($1,000) - Growing market
6. **Salons/Spas** ($600-$800) - Volume play

---

## Integration with PRINTMAXX

### Add to Capital Genesis Revenue Lanes

This fits into **Cold Outbound** method (MM015).

**Location:** `MONEY_METHODS/COLD_OUTBOUND/LOCAL_BIZ/`

**Revenue tracking:** `FINANCIALS/REVENUE_TRACKER.csv`
```csv
date,method_id,revenue,notes
2026-02-06,MM015,$1500,Dentist website redesign - found via scraper
```

**Outreach pipeline:** `LEDGER/OUTREACH_PIPELINE.csv`
```csv
lead_source,business_name,category,url,contact_email,priority,status
local_biz_scraper,Main St Dental,dentist,https://example.com,info@mainst.com,HIGH,CONTACTED
```

**Content generation:** Use Zero Waste Protocol
- Scraper findings → Twitter posts about website red flags
- Case studies → "How I found 100 prospects in 5 minutes"
- Email templates → Gumroad product "Local Business Outreach Kit"

---

## Scaling Strategy

### Phase 1: Manual Validation (Week 1)
- Compile 50 URLs manually
- Run scraper
- Email top 10 HIGH priority
- Book 2-3 calls
- Close 1 deal
- **Goal: Validate method works**

### Phase 2: Volume Test (Week 2-4)
- Compile 200 URLs (or hire VA at $5/hour)
- Run scraper
- Email top 40 HIGH priority
- Track response rates
- Close 3-5 deals
- **Goal: Prove repeatable**

### Phase 3: Systematize (Month 2)
- Document exact process
- Create SOPs for VA
- Hire VA for URL compilation ($5/hour)
- Hire VA for initial outreach ($8/hour)
- You handle calls and closing
- **Goal: Remove yourself from grunt work**

### Phase 4: Scale (Month 3+)
- Run 1,000+ businesses through scraper
- Multiple cities/categories in parallel
- VA does: URL finding, initial outreach, follow-ups
- You do: Calls, closing, delivery (or hire that too)
- **Goal: 10-20 deals/month**

---

## Next Steps

1. **Immediate (Today):**
   - [ ] Install dependencies
   - [ ] Run demo mode
   - [ ] Test with 5 real URLs

2. **This Week:**
   - [ ] Compile 50 prospect URLs
   - [ ] Run scraper
   - [ ] Email top 10 HIGH priority
   - [ ] Book 2 calls

3. **This Month:**
   - [ ] Close first deal
   - [ ] Document process
   - [ ] Scale to 200 prospects
   - [ ] Close 3-5 deals

4. **Long-term:**
   - [ ] Hire VA for URL compilation
   - [ ] Hire VA for outreach
   - [ ] Build case study portfolio
   - [ ] Raise prices as proof builds
   - [ ] Exit to SaaS or recurring service model

---

## Technical Requirements

**Dependencies:**
- Python 3.7+
- requests
- beautifulsoup4
- tqdm

**Optional but recommended:**
- Proxy service (for large-scale scraping)
- Google Places API (for automated URL discovery)
- Email sending service (SendGrid, Mailgun for bulk outreach)

---

## Limitations & Workarounds

### Limitation 1: No JavaScript Rendering
**Problem:** Sites built entirely in React/Vue may not render.
**Workaround:** These are typically newer sites (less likely prospects). Focus on WordPress/custom sites.

### Limitation 2: No Google Maps API
**Problem:** Can't automatically discover business URLs.
**Workaround:** Manual compilation is fast enough at small scale. At scale, use Google Places API ($5/1000 requests).

### Limitation 3: Contact Info in Images
**Problem:** Can't extract emails/phones from images.
**Workaround:** Use LinkedIn to find decision maker. Or call the business directly.

### Limitation 4: Rate Limiting
**Problem:** Too many requests = IP ban.
**Workaround:** Use 2-second rate limit (built-in). For large scale, use rotating proxies.

---

## Success Metrics to Track

After 30 days:

| Metric | Target | How to Track |
|--------|--------|--------------|
| Sites scraped | 200+ | CSV row count |
| HIGH priority found | 20-30% | Filter CSV |
| Email response rate | 20-25% | Email tracking |
| Call booking rate | 40-50% | Calendar |
| Close rate | 30-40% | CRM or spreadsheet |
| Average deal size | $800-$1,500 | Revenue tracker |
| Time per deal | <5 hours | Time tracking |
| Monthly revenue | $3,000-$5,000 | Revenue tracker |

---

## Support & Documentation

**Quick help:**
- Quick start: `LOCAL_BIZ_SCRAPER_QUICKSTART.md`
- Full docs: `LOCAL_BIZ_SCRAPER_README.md`
- Email templates: `LOCAL_BIZ_EMAIL_TEMPLATES.md`

**Run demo:**
```bash
python3 AUTOMATIONS/local_biz_website_scraper.py --demo
```

**Test with real URLs:**
```bash
python3 AUTOMATIONS/local_biz_website_scraper.py --urls-file AUTOMATIONS/sample_business_urls.csv
```

**Check output:**
```bash
open AUTOMATIONS/output/local_biz_prospects.csv
```

---

## Credits & License

Built for PRINTMAXX Capital Genesis project.

Part of Cold Outbound method (MM015) for $0→$1K/month revenue lane.

MIT License - use commercially, modify as needed.
