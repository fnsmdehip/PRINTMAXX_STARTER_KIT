# Content Posting Scheduler

Reads generated content from CONTENT_FARM and content_generation directories, formats for each platform, and creates a posting queue.

## Usage

```bash
# Process all content, schedule for 7 days
python3 post_scheduler.py

# Filter by niche
python3 post_scheduler.py --niche faith

# Filter by platform
python3 post_scheduler.py --platform x

# Custom schedule length
python3 post_scheduler.py --days 14

# Dry run (stats only, no file writes)
python3 post_scheduler.py --dry-run
```

## Output

- `posting_queue.csv` - Full schedule with date, time, platform, account, content, status
- `output/{platform}/{niche}/` - Ready-to-post text files organized by platform and date

## Platform Limits

| Platform | Character Limit |
|----------|----------------|
| X/Twitter | 280 |
| TikTok | 2,200 |
| Instagram | 2,200 |
| LinkedIn | 3,000 |
| Bluesky | 300 |
| Threads | 500 |

## Posting Schedule (EST)

| Niche | X | Instagram | TikTok |
|-------|---|-----------|--------|
| Faith | 6:30, 12:00, 19:30 | 7:00, 18:00 | 6:30, 11:00, 19:00 |
| Fitness | 5:30, 12:00, 18:00 | 6:00, 17:30 | 5:30, 12:00, 17:00 |
| AI | 8:00, 12:30, 17:00 | 9:00, 17:00 | 8:00, 12:00, 18:00 |

## Dependencies

None (stdlib only).
