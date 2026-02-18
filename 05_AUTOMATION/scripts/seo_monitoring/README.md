# SEO Monitoring Script

Tracks keyword rankings over time, logs position changes, and alerts on significant ranking shifts.

## Setup

Set one of these SERP API keys (in order of recommendation):

```bash
# Serper.dev - 2,500 free searches (RECOMMENDED)
export SERPER_API_KEY="your_key"

# SerpApi - 100 free searches/month
export SERPAPI_KEY="your_key"

# ValueSERP - pay-as-you-go
export VALUESERP_KEY="your_key"
```

## Usage

```bash
# Check all keywords from longtail slugs
python3 track_rankings.py --from-slugs

# Check specific keywords
python3 track_rankings.py --keywords "prayer app, fitness timer, AI workflow"

# Load keywords from CSV
python3 track_rankings.py --from-csv my_keywords.csv

# Limit number of keywords (for API quota management)
python3 track_rankings.py --from-slugs --limit 20

# Set alert threshold (default: 5 position change)
python3 track_rankings.py --alert-threshold 3

# Generate ranking report
python3 track_rankings.py --report

# Report for last 60 days
python3 track_rankings.py --report --days 60
```

## Output

- `rankings_history.csv` - Cumulative ranking data over time
- `reports/seo_report_YYYYMMDD.md` - Generated ranking report

## Tracked Domains

Monitors rankings for:
- printmaxx.com
- printmaxx.io
- printmaxx.co

Edit `OUR_DOMAINS` in the script to add more.

## Alerts

Alerts are logged when a keyword moves more than the threshold (default: 5 positions) in either direction.

## Demo Mode

Without API keys, creates template entries in rankings_history.csv for tracking setup verification.

## Dependencies

None (stdlib only).
