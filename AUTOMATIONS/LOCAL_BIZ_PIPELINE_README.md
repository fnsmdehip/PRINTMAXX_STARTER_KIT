# Local Business Website Redesign Pipeline

**Complete automation:** Scrape → Generate → Host → Outreach

## What It Does

This master pipeline script chains together the full local business website redesign workflow:

1. **SCRAPE**: Analyzes business websites (mobile responsiveness, SEO, SSL, tech stack, contact info)
2. **GENERATE**: Creates custom landing pages for HIGH priority prospects (site score < 40)
3. **HOST**: Provides ready-to-deploy directory structure
4. **OUTREACH**: Generates personalized cold email CSV ready for Instantly.ai (3-step sequence)

## Quick Start

```bash
# 1. Install dependencies (one time)
pip install requests beautifulsoup4 tqdm

# 2. Run the pipeline with sample URLs
cd AUTOMATIONS
python3 local_biz_pipeline.py --urls-file sample_local_biz_urls.csv

# 3. Preview the generated pages
cd output/pipeline_run/landing_pages
python3 -m http.server 8000
# Open: http://localhost:8000/index.html

# 4. Upload cold_emails_instantly.csv to Instantly.ai
```

## Usage Examples

### From URLs file
```bash
python3 local_biz_pipeline.py --urls-file sample_local_biz_urls.csv
```

### Dry run (analyze only, no emails)
```bash
python3 local_biz_pipeline.py --urls-file sample_local_biz_urls.csv --dry-run
```

### Custom output directory
```bash
python3 local_biz_pipeline.py --urls-file my_prospects.csv --output-dir custom_output
```

### Custom preview URL (after deploying)
```bash
python3 local_biz_pipeline.py \
  --urls-file my_prospects.csv \
  --preview-url https://mypreview.vercel.app
```

### Slower rate limit (be more polite)
```bash
python3 local_biz_pipeline.py \
  --urls-file my_prospects.csv \
  --rate-limit 5.0
```

## Input CSV Format

Your URLs file should have these columns:

```csv
url,business_name,category,city
https://example.com,Joe's Plumbing,plumber,Austin TX
https://example2.com,Bright Dental,dentist,Dallas TX
```

**Supported categories:**
- dentist
- plumber
- electrician
- hvac
- restaurant
- law_firm
- real_estate
- salon
- gym
- auto_repair
- landscaping
- cleaning_service
- contractor
- accountant
- chiropractor

## Output Structure

```
output/pipeline_run/
├── prospects.csv              # Full analysis of all scraped sites
├── landing_pages/
│   ├── index.html            # Directory of all generated pages
│   ├── joes-plumbing.html    # Individual landing pages
│   ├── bright-dental.html
│   └── ...
└── cold_emails_instantly.csv  # Ready to import to Instantly.ai
```

## Email Sequence

The pipeline generates a 3-step email sequence for each HIGH priority prospect:

### Day 1: Initial outreach with preview link
```
Subject: I built a new website for {business_name}

Hi {first_name},

I was looking at {business_name}'s website and noticed a few things:

{specific_issues} — which means you're likely losing customers who browse
on their phone or search online.

I went ahead and built a preview of what a modern version could look like:

{preview_link}

If you like what you see, I can have the full site live for $500 — includes
mobile optimization, SEO setup, hosting, and 30 days of support.

Want me to walk you through it?

Best,
[Your Name]
```

### Day 3: Gentle reminder
```
Subject: Re: I built a new website for {business_name}

Hi {first_name},

Just wanted to make sure you saw the site I built for {business_name}:

{preview_link}

Happy to jump on a quick call if you have questions.

Best,
[Your Name]
```

### Day 7: Final follow-up with scarcity
```
Subject: Re: I built a new website for {business_name}

Hi {first_name},

Last follow-up — the preview site for {business_name} is still live at:

{preview_link}

I have 2 spots left this month for new builds. Let me know if you're interested.

Best,
[Your Name]
```

## Scoring System

Sites are scored 0-100 (lower = more likely prospect):

**HIGH priority** (score < 40):
- Not mobile responsive (-25)
- No SSL certificate (-20)
- Poor SEO (-30)
- No AI-SEO/schema markup (-25)
- Outdated (pre-2020 copyright) (-15)
- Has active business signals (phone, email, social)

**MEDIUM priority** (score 40-60):
- Some issues but not critical
- May still convert with good pitch

**LOW priority** (score > 60):
- Modern site, likely not interested

## Deployment Options

### Option 1: Local server (testing)
```bash
cd output/pipeline_run/landing_pages
python3 -m http.server 8000
```
Preview URL: `http://localhost:8000`

### Option 2: Vercel (recommended)
```bash
cd output/pipeline_run/landing_pages
npm i -g vercel
vercel --prod
```
Get deployed URL, then re-run pipeline:
```bash
python3 local_biz_pipeline.py \
  --urls-file my_prospects.csv \
  --preview-url https://your-project.vercel.app
```

### Option 3: Netlify
```bash
cd output/pipeline_run/landing_pages
npm i -g netlify-cli
netlify deploy --prod --dir .
```

### Option 4: GitHub Pages
```bash
cd output/pipeline_run/landing_pages
git init
git add .
git commit -m "Landing pages"
git branch -M main
git remote add origin https://github.com/yourusername/local-biz-previews.git
git push -u origin main
# Enable GitHub Pages in repo settings
```

## Instantly.ai Import

1. Login to Instantly.ai
2. Go to **Campaigns** → **Import Leads**
3. Upload `cold_emails_instantly.csv`
4. Map columns:
   - `email` → Email
   - `first_name` → First Name
   - `company_name` → Company
   - `custom_variable_1` → Preview Link
   - `custom_variable_2` → Issues Found
   - `sequence_step` → Sequence Step
5. Create campaign with 3-step sequence
6. Launch

## Finding Prospects

### Manual (recommended for quality)
1. Google: `"plumber" + "austin tx"`
2. Check Google Maps listings
3. Visit each website
4. Copy to CSV if site looks old/broken

### Automated (requires API)
- Google Places API
- Yelp Fusion API
- YellowPages scraping (check ToS)

### Buying leads
- Hunter.io (emails for domains)
- Apollo.io (B2B database)
- Local business directories

## Expected Conversion Rates

Based on typical cold email + preview page funnel:

- **Email open rate:** 40-60% (good subject lines)
- **Preview link clicks:** 10-20% (curiosity factor)
- **Replies:** 5-10% (personalized + visual proof)
- **Qualified conversations:** 2-5%
- **Close rate:** 20-40% of conversations

**Example:**
- 100 prospects → 50 opens → 10 clicks → 5 replies → 2 qualified → 1 closed deal ($500)
- Need ~100 prospects per deal
- 1,000 prospects = 10 deals = $5,000 revenue

## Cost Per Acquisition

**Time investment:**
- 1 hour to collect 100 URLs
- 30 min pipeline run (scrape + generate)
- 1 hour deploy + test
- 30 min Instantly.ai setup
- **Total: 3 hours per 100 prospects**

**Hard costs:**
- Instantly.ai: $30-97/mo (unlimited emails)
- Vercel hosting: Free (or $20/mo Pro)
- Domain: $12/year
- **Total: ~$50/mo**

**Per deal:**
- 100 prospects = 1 deal
- 3 hours + $50 hard costs
- Sell for $500
- **Profit: $450 per deal**
- **Hourly rate: $150/hour**

## Scaling

### 10 deals/month ($5,000)
- 1,000 prospects
- 30 hours work
- 2-3 hours/day

### 20 deals/month ($10,000)
- 2,000 prospects
- 60 hours work
- Hire VA to collect URLs ($5/hour)
- You handle: pipeline + sales calls

### 50+ deals/month ($25,000+)
- Hire VA for prospecting
- Hire VA for cold calling follow-ups
- You handle: closing + fulfillment
- Or: Hire designer for fulfillment ($200/site)
- Net: $300/deal × 50 = $15,000/mo profit

## Fulfillment After Close

Once they say yes to $500:

1. **Collect details** (15 min call):
   - Services offered
   - Target customers
   - Preferred colors
   - Photos/branding assets
   - Any existing copy they like

2. **Generate final site** (30-60 min):
   - Use `bulk_landing_page_generator.py` with real content
   - Replace placeholder testimonials
   - Add real business hours
   - Add Google Maps embed
   - Test mobile + desktop

3. **Deploy** (15 min):
   - Vercel/Netlify with custom domain
   - Setup SSL (automatic)
   - Connect to their existing domain (or buy new one)

4. **30-day support**:
   - Minor copy changes
   - Add/remove sections
   - Basic SEO adjustments

**Total fulfillment time: 1-2 hours per deal**

**Profit: $500 revenue - $0 COGS - 2 hours work = $250/hour**

## Upsells

After initial $500 site:

- **Google Ads setup**: $300 + 15% monthly management
- **SEO package**: $200/mo retainer (content + backlinks)
- **Social media**: $150/mo (3 posts/week)
- **Email marketing**: $100/mo (newsletters)
- **Maintenance**: $50/mo (updates + hosting)

**Lifetime value:** $500 initial + $500-2,000 upsells = $1,000-2,500 per customer

## Troubleshooting

### "No HIGH priority prospects found"
- Lower score threshold in code (line ~350)
- Or generate for MEDIUM priority manually
- Or scrape more sites (need larger sample)

### "Email not found on site"
- Use Hunter.io to find emails by domain
- Or switch to cold calling (phone numbers extracted)
- Or use LinkedIn for contact info

### "Sites timing out"
- Increase `--rate-limit` to 5-10 seconds
- Some sites block scrapers (normal, skip them)
- Or use residential proxies (Bright Data)

### "Generated pages look generic"
- That's intentional for demo
- They'll customize after seeing preview
- Or: add more category templates to code

### "Low reply rates"
- Test different subject lines
- Personalize first line more
- Follow up with phone call
- Or: run retargeting ads to preview site visitors

## Legal Notes

- **CAN-SPAM compliance:** Include unsubscribe link, physical address
- **Terms of service:** Don't claim their site without permission in preview
- **Copyright:** Use placeholders for testimonials/photos
- **FTC:** Don't make income claims ("I'll get you 50 more customers")

## Next Steps

1. Run pipeline on sample URLs (test)
2. Manually collect 20-50 real prospects
3. Run pipeline on real prospects
4. Deploy preview pages
5. Import to Instantly.ai
6. Launch campaign
7. Track replies in spreadsheet
8. Close deals
9. Fulfill sites
10. Scale

## Support

Questions? Check:
- `local_biz_website_scraper.py` - Scraping logic
- `bulk_landing_page_generator.py` - Page generation logic
- `local_biz_pipeline.py` - This master script

Modify as needed for your specific use case.
