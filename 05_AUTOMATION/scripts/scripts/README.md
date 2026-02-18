# Daily Alpha Research System

Automated system for scanning high-signal sources and staging alpha findings for human review.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Run full scan
python3 daily_alpha_scanner.py

# Preview mode (no scraping)
python3 daily_alpha_scanner.py --dry-run
```

## Components

### Main Scanner
`daily_alpha_scanner.py` - Orchestrates the full alpha research process.

```bash
# Full scan (all auto_monitor sources)
python3 daily_alpha_scanner.py

# Platform-specific
python3 daily_alpha_scanner.py --platform X       # Twitter only
python3 daily_alpha_scanner.py --platform Reddit  # Reddit only
python3 daily_alpha_scanner.py --platform HN      # HackerNews only

# Filter by signal tier
python3 daily_alpha_scanner.py --tier HIGHEST

# Limit sources (for testing)
python3 daily_alpha_scanner.py --max 5

# Show browser window
python3 daily_alpha_scanner.py --no-headless

# Debug mode
python3 daily_alpha_scanner.py --debug
```

### Source Scrapers

Located in `source_scrapers/`:

- **twitter_scraper.py** - Scrapes X/Twitter profiles for tweets
- **reddit_scraper.py** - Scrapes subreddits for posts
- **hackernews_scraper.py** - Scrapes HN front page and Show HN

### Processing

- **alpha_processor.py** - Deduplicates, categorizes, and scores findings
- **daily_report_generator.py** - Creates markdown reports

## Configuration

### Proxy Setup

For production use with proxies, create `AUTOMATIONS/proxy_config.json`:

```json
{
  "twitter": {
    "server": "proxy.example.com:8080",
    "username": "user",
    "password": "pass"
  },
  "reddit": {
    "server": "proxy.example.com:8080",
    "username": "user",
    "password": "pass"
  }
}
```

Or use environment variables:
```bash
export PROXY_HOST=proxy.example.com
export PROXY_PORT=8080
export PROXY_USER=user
export PROXY_PASS=pass
```

### Source Configuration

Sources are loaded from `LEDGER/HIGH_SIGNAL_SOURCES.csv`.

Only rows with `auto_monitor=TRUE` are scanned.

## Output

### ALPHA_STAGING.csv

Findings are appended to `LEDGER/ALPHA_STAGING.csv` with:

| Field | Description |
|-------|-------------|
| alpha_id | Unique identifier (ALPHA_YYYYMMDDHHMMSS_XXX) |
| source | Where found (@handle, r/subreddit, etc.) |
| source_url | Direct link to content |
| category | Classification (APP_FACTORY, GROWTH_HACK, etc.) |
| title | First 60 chars of content |
| description | First 500 chars of content |
| actionable_steps | (Empty - human fills this) |
| effort_level | LOW, MEDIUM, HIGH |
| roi_potential | HIGHEST, HIGH, MEDIUM, LOW |
| risk_level | LOW, MEDIUM, HIGH |
| applies_to_niches | ALL, AI, Faith, Fitness |
| status | PENDING_REVIEW |
| reviewer_notes | Auto-staging reason and score |

### Daily Reports

Reports saved to `OPS/reports/alpha_research_YYYY-MM-DD.md` with:

- Scan summary and metrics
- Category and source breakdowns
- Top priority findings
- Findings by signal level
- ChatGPT ads update check
- Action items
- Errors and issues

## Categories

| Category | Keywords |
|----------|----------|
| APP_FACTORY | app, mobile, mrr, saas, paywall |
| CONTENT_FORMAT | hook, format, viral, algorithm |
| OUTBOUND | cold email, deliverability, lead gen |
| GROWTH_HACK | growth, organic, seo, distribution |
| TOOL_ALPHA | tool, automation, api, workflow |
| COMPLIANCE | ftc, disclosure, banned, legal |
| NICHE_INSIGHT | niche, market, demographic |
| MONETIZATION | pricing, funnel, conversion, revenue |
| COMPETITOR | competitor, vs, comparison |
| TREND | trend, emerging, future, prediction |

## Signal Scoring

### HIGHEST Signal
- Contains specific numbers ($, %, k, x)
- Has actionable language (how to, step by step)
- High engagement metrics

### HIGH Signal
- Contains specific numbers
- Good engagement

### MEDIUM Signal
- Actionable language but no specifics
- OR high engagement only

### LOW Signal (filtered out)
- Motivational/noise content
- Engagement farm patterns
- Generic content

## Human Review Workflow

1. Run daily scan
2. Review `LEDGER/ALPHA_STAGING.csv` entries with status=PENDING_REVIEW
3. Mark each as APPROVED or REJECTED
4. Run `/review-alpha` skill to integrate approved entries
5. Check daily report for action items

## Troubleshooting

### Rate Limiting
The scrapers include built-in rate limiting. If you hit platform limits:
- Reduce `--max` sources
- Add delays in scanner config
- Use proxies for production

### No Results
- Check if sources have `auto_monitor=TRUE`
- Verify URLs in HIGH_SIGNAL_SOURCES.csv
- Try `--no-headless` to debug visually

### Browser Issues
```bash
# Reinstall browsers
playwright install --force chromium
```

## Integration

This system integrates with:
- `/daily-research` skill
- `/review-alpha` skill
- `ralph_tasks/00_daily_alpha_research.md`

See `.claude/commands/` for skill definitions.
