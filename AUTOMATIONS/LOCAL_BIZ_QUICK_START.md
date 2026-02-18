# Local Business Pipeline - Quick Start (5 Minutes)

## Install & Run (Copy-Paste)

```bash
# 1. Install dependencies
pip install requests beautifulsoup4 tqdm

# 2. Run pipeline with sample data
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS
python3 local_biz_pipeline.py --urls-file sample_local_biz_urls.csv --dry-run

# 3. View results
cd output/pipeline_run/landing_pages
python3 -m http.server 8000
# Open: http://localhost:8000/index.html
```

## What Happens

1. **SCRAPE**: Analyzes 20 sample business websites
2. **SCORE**: Rates each 0-100 (lower = worse site = better prospect)
3. **GENERATE**: Creates landing pages for HIGH priority (score < 40)
4. **EMAILS**: Ready-to-send cold email CSV (use `--dry-run` to skip)

## Output Files

```
output/pipeline_run/
├── prospects.csv              # All analyzed sites with scores
├── landing_pages/
│   ├── index.html            # View all generated pages
│   ├── bright-smile-dental.html
│   ├── quick-fix-plumbing.html
│   └── ...
└── cold_emails_instantly.csv  # Upload to Instantly.ai
```

## Real Usage (Production)

### Step 1: Collect real prospects (manual, 1 hour)

Create `my_real_prospects.csv`:
```csv
url,business_name,category,city
https://joesplumbing.com,Joe's Plumbing,plumber,Austin TX
https://smithdental.com,Smith Dental,dentist,Austin TX
```

Find prospects:
- Google: `"plumber austin tx"` → visit sites
- Check Google Maps
- Look for old/broken sites

### Step 2: Run pipeline (30 min)

```bash
python3 local_biz_pipeline.py --urls-file my_real_prospects.csv
```

### Step 3: Deploy preview pages (15 min)

```bash
cd output/pipeline_run/landing_pages
npm i -g vercel
vercel --prod
```

Copy deployed URL (e.g., `https://my-previews.vercel.app`)

### Step 4: Re-run with real URL (5 min)

```bash
python3 local_biz_pipeline.py \
  --urls-file my_real_prospects.csv \
  --preview-url https://my-previews.vercel.app
```

### Step 5: Upload to Instantly.ai (10 min)

1. Login to Instantly.ai
2. Campaigns → Import Leads
3. Upload `cold_emails_instantly.csv`
4. Launch campaign

### Step 6: Track replies & close deals

- Reply rate: ~5-10%
- Close rate: ~20-40% of replies
- Expected: 1 deal per 100 prospects
- Revenue: $500 per deal

## Economics

**Per 100 prospects:**
- Time: 3 hours
- Cost: ~$50/mo (Instantly.ai + hosting)
- Result: 1 deal ($500)
- Profit: $450
- Hourly rate: $150/hour

**Scale to 10 deals/month ($5,000):**
- 1,000 prospects
- 30 hours/month
- 2-3 hours/day

**Scale to 20+ deals/month ($10,000+):**
- Hire VA for prospecting ($5/hour)
- You handle: sales + fulfillment

## Quick Commands Reference

```bash
# Help
python3 local_biz_pipeline.py --help

# Dry run (no emails)
python3 local_biz_pipeline.py --urls-file sample.csv --dry-run

# Custom output dir
python3 local_biz_pipeline.py --urls-file sample.csv --output-dir results

# Slower scraping (more polite)
python3 local_biz_pipeline.py --urls-file sample.csv --rate-limit 5.0

# With deployed preview URL
python3 local_biz_pipeline.py \
  --urls-file sample.csv \
  --preview-url https://your-site.vercel.app
```

## Troubleshooting

**"No HIGH priority prospects found"**
→ Normal for sample data (example sites). Use real prospects.

**"Email not found"**
→ Use Hunter.io or call instead (phone numbers extracted).

**"Timeout errors"**
→ Increase `--rate-limit` to 5-10 seconds.

## Full Documentation

See `LOCAL_BIZ_PIPELINE_README.md` for:
- Detailed usage
- Scaling strategies
- Fulfillment workflow
- Upsell opportunities
- Legal compliance

## Next Steps

1. ✅ Run sample pipeline (this guide)
2. Collect 20-50 real prospects manually
3. Run pipeline on real data
4. Deploy preview pages
5. Launch Instantly.ai campaign
6. Close first deal
7. Scale

Start now. First deal in 1-2 weeks.
