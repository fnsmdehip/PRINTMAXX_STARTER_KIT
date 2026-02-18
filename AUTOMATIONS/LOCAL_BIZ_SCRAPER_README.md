# Local Business Website Scraper

## Purpose

Identifies local businesses that need website redesigns for $500-$2000 service offerings.

The script analyzes websites and scores them 0-100 (lower = more likely to need help). It checks:
- Mobile responsiveness
- SSL certificates
- SEO fundamentals
- AI-SEO readiness (schema.org, structured data)
- Technology stack
- Last updated date
- Contact information
- Overall site quality

## Installation

```bash
pip install requests beautifulsoup4 tqdm
```

## Usage

### Demo Mode (See Output Format)

```bash
python AUTOMATIONS/local_biz_website_scraper.py --demo
```

### Analyze URLs from CSV

```bash
python AUTOMATIONS/local_biz_website_scraper.py --urls-file AUTOMATIONS/sample_business_urls.csv
```

### Manual Category Search (Limited Without API)

```bash
python AUTOMATIONS/local_biz_website_scraper.py --category "dentist" --city "Austin TX"
```

Note: Direct Google Maps scraping requires API access. For best results, manually compile URLs.

## Input CSV Format

Create a CSV with these columns:
- `url` (required)
- `business_name` (optional)
- `category` (optional - helps with budget estimation)
- `city` (optional)

Example:
```csv
url,business_name,category,city
https://example-dental.com,Main Street Dental,dentist,Austin TX
https://example-plumbing.com,Joe's Plumbing,plumber,Dallas TX
```

## Output

Results saved to: `AUTOMATIONS/output/local_biz_prospects.csv`

### Output Columns

| Column | Description |
|--------|-------------|
| business_name | Business name |
| url | Website URL |
| city | City location |
| category | Business category |
| site_score | 0-100 score (lower = needs more help) |
| mobile_ready | TRUE/FALSE - has viewport meta tag |
| has_ssl | TRUE/FALSE - valid SSL certificate |
| seo_score | 0-100 SEO basics score |
| ai_seo_score | 0-100 AI-SEO readiness score |
| tech_stack | WordPress, Wix, custom, etc. |
| last_updated_estimate | Estimated last update date |
| appears_active | TRUE/FALSE - business seems active |
| budget_estimate | Estimated redesign budget potential |
| email_if_found | Email addresses found on site |
| phone_if_found | Phone numbers found on site |
| notes | Issues identified |
| outreach_priority | HIGH/MEDIUM/LOW |

## Scoring System

### Site Score (0-100, lower = better prospect)

Starts at 100, penalized for:
- No mobile viewport: -25 points
- No SSL: -20 points
- Poor SEO: up to -30 points
- No AI-SEO: up to -25 points
- Old site (pre-2020): -15 points

**Target prospects: Score < 40**

### SEO Score (0-100, lower = needs help)

Points awarded for:
- Title tag: 20 points
- Meta description: 20 points
- H1 tag: 20 points
- Open Graph tags: 20 points
- Image alt text: 20 points

### AI-SEO Score (0-100, lower = needs help)

Points awarded for:
- Schema.org markup: 40 points
- FAQ schema: 20 points
- Breadcrumbs: 20 points
- Structured headings: 20 points

### Outreach Priority

**HIGH:**
- Site score < 40
- Business appears active
- Email found on site

**MEDIUM:**
- Site score < 60
- Business appears active

**LOW:**
- Everything else

## Budget Estimation

Base budgets by category:
- Lawyers/Doctors: $1,500-$2,000
- Real estate: $1,200
- Restaurants: $800
- Home services (plumbing, HVAC): $700
- Salons/Gyms: $600-$1,000

Adjusted based on:
- Very poor site (score < 30): +30%
- DIY platform (Wix, Squarespace): -30%

## Finding Business URLs

### Manual Sources (Recommended)

1. **Google Maps** - Search "{category} in {city}", click through to websites
2. **Yelp** - Filter by category and location
3. **Yellow Pages** - Online directory
4. **Local chamber of commerce** - Member directories
5. **Industry associations** - Member listings

### Automated (Requires API)

- Google Places API
- Yelp Fusion API
- Data.com / ZoomInfo (paid)

## Rate Limiting

Default: 2 seconds between requests

Change with `--rate-limit` flag:
```bash
python AUTOMATIONS/local_biz_website_scraper.py --urls-file urls.csv --rate-limit 3.0
```

## Example Workflow

### 1. Find Prospects Manually

Search Google Maps for "dentist austin tx", compile 20 URLs into `dental_prospects.csv`

### 2. Run Scraper

```bash
python AUTOMATIONS/local_biz_website_scraper.py --urls-file dental_prospects.csv
```

### 3. Filter Results

Open `AUTOMATIONS/output/local_biz_prospects.csv`, sort by `outreach_priority` (HIGH first)

### 4. Cold Outreach

Use HIGH priority prospects with:
- Site score < 40
- Email found
- Appears active

### 5. Email Template (From Scraper Data)

```
Subject: Quick question about [Business Name] website

Hi [Name/Team],

I was looking at [Category] businesses in [City] and came across your site at [URL].

I noticed [specific issue from notes - e.g., "it's not mobile-responsive" or "missing from Google"].

I help local [category] businesses get more customers through modern websites that:
- Work perfectly on phones (70% of your traffic)
- Show up in Google/AI search
- Convert visitors to calls/appointments

Would you be open to a quick 15-minute call to see if this makes sense for [Business Name]?

[Your Name]
[Your Phone]
```

## Advanced Usage

### Custom Output Path

```bash
python AUTOMATIONS/local_biz_website_scraper.py --urls-file urls.csv --output prospects_2026_02.csv
```

### Combine Multiple Categories

Create separate CSVs for each category, run scraper on each:

```bash
python AUTOMATIONS/local_biz_website_scraper.py --urls-file dental_urls.csv --output dental_prospects.csv
python AUTOMATIONS/local_biz_website_scraper.py --urls-file law_urls.csv --output law_prospects.csv
python AUTOMATIONS/local_biz_website_scraper.py --urls-file restaurant_urls.csv --output restaurant_prospects.csv
```

Then merge and sort by priority.

## Limitations

1. **No JavaScript rendering** - Sites that rely heavily on JS may not be fully analyzed
2. **No API integration** - Google Maps scraping requires manual URL compilation or API
3. **Basic contact extraction** - May miss emails/phones in images or obfuscated formats
4. **Tech stack detection** - Based on common patterns, may miss custom setups

## Next Steps

After identifying prospects:

1. **Validate manually** - Check top 10 HIGH priority sites yourself
2. **Research business** - Google the business, check reviews, verify they're active
3. **Personalize outreach** - Reference specific issues from the scraper notes
4. **Follow up** - Call if email bounces or no response in 3 days
5. **Track conversions** - Log which score ranges convert best

## Integration with PRINTMAXX

Add results to `LEDGER/OUTREACH_PIPELINE.csv`:

```csv
lead_source,business_name,category,url,contact_email,priority,notes,status
local_biz_scraper,[Business Name],[Category],[URL],[Email],HIGH,[Notes from scraper],PENDING_OUTREACH
```

Use cold email templates from `MONEY_METHODS/COLD_OUTBOUND/`.

Track revenue in `FINANCIALS/REVENUE_TRACKER.csv` when deals close.

## ROI Calculation

**Time saved:**
- Manual site audit: 15 minutes per site
- 100 sites = 25 hours
- Script: 3-5 minutes (with 2-second rate limit)

**Revenue potential:**
- 100 sites scraped
- 20 HIGH priority (20%)
- 5 conversions (25% of HIGH)
- $1,000 average project
- **= $5,000 revenue from 3 minutes of scraping**

## Troubleshooting

**"Missing dependencies" error:**
```bash
pip install requests beautifulsoup4 tqdm
```

**Connection timeout:**
- Increase `--rate-limit` to 3.0 or higher
- Check your internet connection
- Site may be blocking automated requests (use proxy)

**No email/phone found:**
- Common for WordPress sites using contact forms
- Check manually or call business
- Use LinkedIn to find decision maker

**SSL check fails:**
- Site may have self-signed certificate
- May have expired SSL
- This is actually a good signal (they need help!)

## Future Enhancements

- [ ] Google Places API integration for automated URL discovery
- [ ] Playwright integration for JavaScript-heavy sites
- [ ] Proxy rotation for large-scale scraping
- [ ] Automated email outreach integration
- [ ] LinkedIn scraping for decision maker contact info
- [ ] Competitive analysis (compare to competitors)
- [ ] Screenshot capture for visual comparison
- [ ] Page speed testing (Lighthouse API)
