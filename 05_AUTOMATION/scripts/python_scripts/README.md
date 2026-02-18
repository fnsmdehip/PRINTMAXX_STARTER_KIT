# PRINTMAXX Python Automation Scripts

Scripts for content generation, scraping, validation, and scheduling.

## Setup

```bash
# Install dependencies
cd AUTOMATIONS/python_scripts
pip install -r requirements.txt

# Install Playwright browsers (for scraping scripts)
playwright install chromium
```

## Environment Variables

Create a `.env` file or export these variables:

```bash
# Required for content generation
export ANTHROPIC_API_KEY=sk-ant-...

# Optional for email validation
export HUNTER_API_KEY=your_hunter_key
export NEVERBOUNCE_API_KEY=your_neverbounce_key

# Optional for content scheduling
export BUFFER_ACCESS_TOKEN=your_buffer_token
export TWITTER_BEARER_TOKEN=your_twitter_token
export LINKEDIN_ACCESS_TOKEN=your_linkedin_token
export LINKEDIN_PERSON_ID=your_person_id
```

---

## Scripts

### scrape_tweets.py

Scrape tweets from HIGH_SIGNAL_SOURCES.csv accounts using Playwright.

```bash
# Scrape all X accounts
python scrape_tweets.py

# Specific accounts
python scrape_tweets.py --handles @levelsio @tdinh_me

# Only HIGHEST signal accounts
python scrape_tweets.py --tier HIGHEST

# Limit to 5 accounts
python scrape_tweets.py --max 5

# Show browser window (debug)
python scrape_tweets.py --show-browser
```

**Output:** `LEDGER/SCRAPED_TWEETS.csv`

---

### generate_longtails.py

Generate SEO-optimized longtail pages using Claude.

```bash
# Generate 10 pages (default)
python generate_longtails.py

# Generate 25 pages
python generate_longtails.py --count 25

# Use Sonnet for higher quality
python generate_longtails.py --model sonnet

# Filter by niche
python generate_longtails.py --niche "AI workflows"

# Filter by template type
python generate_longtails.py --template best

# Preview without generating
python generate_longtails.py --dry-run
```

**Output:** `CONTENT/longtail_pages/*.md`

**Cost:** ~$0.003/page (Haiku), ~$0.05/page (Sonnet)

---

### analyze_competitors.py

Scrape and analyze competitor content from X and blogs.

```bash
# Analyze all competitors
python analyze_competitors.py

# Specific competitor
python analyze_competitors.py --competitor zapier

# Only X content
python analyze_competitors.py --platform x

# Only blog content
python analyze_competitors.py --platform blog

# Content from last 7 days
python analyze_competitors.py --days 7

# Generate analysis report
python analyze_competitors.py --analyze
```

**Output:**
- `LEDGER/COMPETITOR_CONTENT.csv`
- `LEDGER/COMPETITOR_ANALYSIS.md` (with --analyze)

---

### email_validator.py

Validate email lists before sending campaigns.

```bash
# Validate CSV file
python email_validator.py emails.csv

# Specify email column
python email_validator.py emails.csv --column email_address

# Use Hunter.io API for verification
python email_validator.py emails.csv --api hunter

# Use NeverBounce API
python email_validator.py emails.csv --api neverbounce

# Validate single email
python email_validator.py --email test@example.com

# Include SMTP check (can be unreliable)
python email_validator.py emails.csv --smtp
```

**Output:** `emails_validated.csv` with status columns

---

### content_scheduler.py

Schedule approved content across platforms.

```bash
# Schedule all approved posts
python content_scheduler.py

# Only X posts
python content_scheduler.py --platform x

# Preview without posting
python content_scheduler.py --dry-run

# Add to queue CSV (no API posting)
python content_scheduler.py --queue-only

# Schedule from custom CSV
python content_scheduler.py --from-csv content.csv
```

**Output:**
- Updates `CONTENT_PIPELINE.csv` with scheduled status
- Creates `SCHEDULED_QUEUE.csv` if --queue-only

---

## Common Workflows

### Daily Content Pipeline

```bash
# 1. Scrape latest tweets
python scrape_tweets.py --tier HIGHEST --max 10

# 2. Generate longtail content
python generate_longtails.py --count 5 --model haiku

# 3. Schedule approved posts
python content_scheduler.py --dry-run  # Preview first
python content_scheduler.py            # Then execute
```

### Weekly Competitor Analysis

```bash
# Scrape competitor content
python analyze_competitors.py --days 7 --analyze

# Review COMPETITOR_ANALYSIS.md for insights
```

### Email List Cleanup

```bash
# Validate before campaign
python email_validator.py leads.csv --api hunter

# Filter to only valid
# (manually filter emails_validated.csv for status='valid')
```

---

## File Locations

| Script | Reads From | Writes To |
|--------|------------|-----------|
| scrape_tweets.py | LEDGER/HIGH_SIGNAL_SOURCES.csv | LEDGER/SCRAPED_TWEETS.csv |
| generate_longtails.py | LEDGER/GEO_LONGTAIL_SLUGS_300.csv | CONTENT/longtail_pages/*.md |
| analyze_competitors.py | LEDGER/COMPETITORS.csv | LEDGER/COMPETITOR_CONTENT.csv |
| email_validator.py | User-provided CSV | *_validated.csv |
| content_scheduler.py | LEDGER/CONTENT_PIPELINE.csv | LEDGER/SCHEDULED_QUEUE.csv |

---

## Troubleshooting

### Playwright Issues

```bash
# Reinstall browsers
playwright install --force chromium

# Check installation
playwright show-installed-browsers
```

### API Rate Limits

- Anthropic: 60 requests/minute (Haiku)
- Hunter: 50 requests/month (free)
- Twitter: Varies by plan

### Memory Issues

For large CSV files, process in batches:

```bash
# Split large files
split -l 1000 large_file.csv batch_

# Process each batch
for f in batch_*; do python email_validator.py "$f"; done
```
