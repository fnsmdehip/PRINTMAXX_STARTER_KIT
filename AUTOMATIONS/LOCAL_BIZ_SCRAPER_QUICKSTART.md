# Local Business Scraper - Quick Start

## 30-Second Setup

```bash
# 1. Install dependencies (one time)
pip install requests beautifulsoup4 tqdm

# 2. See demo output
python3 AUTOMATIONS/local_biz_website_scraper.py --demo

# 3. Done. Now ready for real usage.
```

## Real Usage (3 Steps)

### Step 1: Find Business URLs

Google "{category} in {city}" (e.g., "dentist austin tx")

Compile 20-50 URLs into a CSV:

```csv
url,business_name,category,city
https://mainstreetdental.com,Main Street Dental,dentist,Austin TX
https://quickplumbing.com,Quick Plumbing,plumber,Dallas TX
```

Save as `my_prospects.csv`

### Step 2: Run Scraper

```bash
python3 AUTOMATIONS/local_biz_website_scraper.py --urls-file my_prospects.csv
```

Wait 2-5 minutes (2 seconds per URL).

### Step 3: Review Results

Open `AUTOMATIONS/output/local_biz_prospects.csv`

Sort by `outreach_priority` column (HIGH first).

**HIGH priority = Score < 40 + Active + Email found**

## What Gets Checked (Automatically)

✅ Mobile responsive?
✅ Has SSL?
✅ SEO basics (title, meta, h1)?
✅ AI-SEO ready (schema.org)?
✅ Tech stack (WordPress, Wix, custom)?
✅ Last updated when?
✅ Contact info (email, phone)?
✅ Overall site quality score 0-100

## Score Meaning

| Score | Meaning | Action |
|-------|---------|--------|
| 0-30 | Terrible site | **Call immediately** |
| 31-50 | Needs major help | **Email today** |
| 51-70 | Needs improvement | Email if niche matches |
| 71+ | Pretty good | Skip (not a prospect) |

## Email Template (Use Scraper Data)

```
Subject: [Business Name] website question

Hi [Team],

I found your site at [URL] while researching [category] businesses in [city].

Quick question: are you happy with how many customers find you online?

I noticed [specific issue]:
- Not showing up on mobile searches
- Missing from Google's AI results
- [other issues from notes]

I help [category] businesses fix this. Usually takes 2 weeks, costs $[budget_estimate from CSV].

5-minute call to see if it makes sense?

[Your name]
[Your phone]
```

## Pro Tips

**Best categories (highest budget):**
- Dentists ($1,500)
- Lawyers ($2,000)
- Doctors ($1,500)
- Real estate ($1,200)
- Home services ($700-900)

**Best prospects:**
- Score < 40
- Old copyright year (2019, 2020)
- WordPress or custom (not Wix/Squarespace)
- Email found on site
- Phone visible (means active)

**Avoid:**
- Franchises (corporate approval needed)
- Very new sites (just launched)
- Sites scoring 70+ (already good)
- No contact info (may be dead business)

## ROI Math

**100 sites scraped:**
- 20 HIGH priority (typical)
- 5 respond (25% response rate)
- 2 close (40% close rate)
- $1,000 average project
- **= $2,000 revenue from 5 minutes of scraping**

**Time comparison:**
- Manual audit: 15 min/site × 100 = 25 hours
- This script: 3-5 minutes total
- **Saved: 24+ hours**

## Scaling Up

Once you validate the method:

1. **Hire VA to compile URLs** ($5/hour on OnlineJobs.ph)
   - Task: "Find 100 dentist websites in Texas cities"
   - Deliverable: CSV with URLs

2. **Run script on 500+ businesses**
   - Overnight with higher rate limit
   - Filter to top 50 HIGH priority

3. **Batch cold email**
   - Use templates from `MONEY_METHODS/COLD_OUTBOUND/`
   - SendGrid/Mailgun for delivery
   - Track in `LEDGER/OUTREACH_PIPELINE.csv`

4. **Track conversions**
   - Which scores convert best?
   - Which categories pay most?
   - Which cities respond best?

5. **Optimize**
   - Focus on highest converting segments
   - Raise prices for easy conversions
   - Hire VA for outreach too

## Next Steps

After first deals close:

- [ ] Document process in `MONEY_METHODS/COLD_OUTBOUND/LOCAL_BIZ_PLAYBOOK.md`
- [ ] Track revenue in `FINANCIALS/REVENUE_TRACKER.csv`
- [ ] Build case studies (before/after)
- [ ] Create service packages (3 tiers)
- [ ] Scale with VAs

## Common Questions

**Q: Can I scrape Google Maps automatically?**
A: Requires API (costs money). Manually compiling URLs is faster at small scale.

**Q: What if email bounces?**
A: Call the phone number. Or find decision maker on LinkedIn.

**Q: What if they say no?**
A: Ask why. If price, offer smaller package. If timing, follow up in 3 months.

**Q: Can I charge more than $500?**
A: Yes. Lawyers/doctors can pay $2,000+. Test pricing.

**Q: Should I guarantee results?**
A: Guarantee deliverables (mobile-ready site, Google indexing), not revenue (you can't control their business).

## Full Documentation

See `AUTOMATIONS/LOCAL_BIZ_SCRAPER_README.md` for:
- All scoring formulas
- Budget estimation logic
- Advanced usage
- Troubleshooting
- Integration with PRINTMAXX system
