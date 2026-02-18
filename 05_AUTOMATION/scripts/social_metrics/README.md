# Social Metrics Collector

Collects social media metrics (followers, engagement) and tracks growth over time in LEDGER/SOCIAL_METRICS.csv.

## Setup

```bash
# Twitter API v2 (for X metrics)
export TWITTER_BEARER_TOKEN="your_bearer_token"

# RapidAPI (for Instagram/TikTok metrics)
export RAPIDAPI_KEY="your_key"
```

## Usage

```bash
# Collect metrics for all default accounts
python3 collect_metrics.py

# Specific platform only
python3 collect_metrics.py --platform x

# Specific accounts
python3 collect_metrics.py --accounts "@handle1,@handle2"

# Manual entry mode (no API needed)
python3 collect_metrics.py --manual

# Generate growth report
python3 collect_metrics.py --report

# Growth report for last 60 days
python3 collect_metrics.py --report --days 60
```

## Default Accounts Tracked

| Handle | Platform | Niche |
|--------|----------|-------|
| @DailyGraceQuotes | X, Instagram, TikTok | Faith |
| @5AMGainsClub | X, Instagram, TikTok | Fitness |
| @TheStackReport | X, Instagram, TikTok | AI |

## Manual Entry Mode

When API keys aren't set, use `--manual` to enter metrics interactively:

```
--- @DailyGraceQuotes (x) ---
  Last recorded: 2026-01-27 - 1,234 followers
  Followers: 1,567
  Following: 203
  Posts: 89
  Avg likes/post: 45
```

## Output

- `LEDGER/SOCIAL_METRICS.csv` - Cumulative metrics history
- `reports/social_report_YYYYMMDD.md` - Growth reports

## Growth Report Includes

- Current follower counts per account
- Period growth (absolute and percentage)
- Daily growth rate
- 30-day projection
- Overall cross-platform summary

## Dependencies

None (stdlib only).
