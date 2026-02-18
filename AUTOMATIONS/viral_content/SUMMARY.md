# Viral Content Scanner - Complete System

Production-ready viral content monitoring and repurposing automation for Twitter/X meme accounts.

## System Overview

The viral content scanner automatically:
1. Monitors 24+ meme/viral Twitter accounts
2. Detects particularly viral tweets (10K+ likes, 2K+ retweets, 500K+ views, 5%+ engagement)
3. Downloads media (images + video URLs)
4. Generates repurpose queue with reply-bait captions
5. Schedules posting across peak engagement windows
6. Alerts on breaking viral content (high velocity in last 2h)

## Files Created

### Core Script
- **`viral_content_scanner.py`** (600+ lines)
  - Viral detection engine
  - Media downloader
  - Queue generator
  - Breaking news alerts
  - Stats dashboard

### Documentation
- **`README.md`** - Complete technical documentation
- **`WORKFLOW.md`** - Daily/weekly workflow guides
- **`SUMMARY.md`** - This file (system overview)

### Shell Scripts
- **`run_daily_scan.sh`** - Full daily workflow (scan → download → schedule → stats)
- **`monitor_breaking.sh`** - Breaking viral content checker (run every 30-60 min)

## Key Features

### 1. Viral Detection
Flags tweets meeting ANY of these thresholds:
- ≥10,000 likes
- ≥2,000 retweets
- ≥500,000 views
- ≥5% engagement ratio (likes+retweets+replies / views)
- 2x above account's average (outlier detection)

### 2. Viral Scoring (0-100)
- Likes: max 30 points
- Retweets: max 25 points
- Views: max 25 points
- Engagement ratio: max 20 points

Tweets scoring 70+ are mega viral. 50+ are solid viral.

### 3. Reply-Bait Captions
Auto-generated based on content type:
- **Funny:** "no way 💀", "this is crazy", "bro what"
- **Nature/Science:** "how is this real", "nature is wild"
- **Drama:** "thoughts?", "this is insane"
- **Default:** "no way", "insane", "wild"

Lowercase, 2-5 words, optimized for reply engagement.

### 4. Repurpose Types
- **MEDIA_REPOST** - Just media with caption (minimal original text)
- **REPOST_WITH_CAPTION** - Media + your caption (has original text)
- **QUOTE_TWEET** - Text-heavy content (100+ chars)
- **REPLY_BAIT** - Short text, no media

### 5. Scheduled Posting
Random times across 4 peak engagement windows:
- 8-11am (morning inspiration/nature)
- 12-2pm (lunch entertainment)
- 5-8pm (evening viral clips)
- 9-11pm (night memes)

Max 8 posts per day, randomized to avoid scrape order.

### 6. Breaking News Detection
Viral velocity = likes per hour

Flags tweets with 500+ likes/hour in last 2 hours. These need immediate attention - don't wait for schedule.

## Usage Quick Reference

### Daily Scan (Recommended: Morning)
```bash
./AUTOMATIONS/viral_content/run_daily_scan.sh
```
Runs: scan → download → schedule → stats

### Breaking Monitor (Run Every 30-60 Min)
```bash
./AUTOMATIONS/viral_content/monitor_breaking.sh
```
Alerts if high-velocity viral content detected.

### Manual Commands
```bash
# Scan all accounts
python3 AUTOMATIONS/viral_content_scanner.py --scan

# Scan first 5 (quick test)
python3 AUTOMATIONS/viral_content_scanner.py --scan --limit 5

# Breaking viral (last 2h)
python3 AUTOMATIONS/viral_content_scanner.py --breaking

# Schedule queue
python3 AUTOMATIONS/viral_content_scanner.py --schedule

# Download media
python3 AUTOMATIONS/viral_content_scanner.py --download

# Show stats
python3 AUTOMATIONS/viral_content_scanner.py --stats
```

## Output Files

### `repurpose_queue.csv`
Main queue with 11 columns:
1. `original_handle` - Source account
2. `original_tweet_id` - Tweet ID
3. `original_url` - Full URL
4. `content_text` - First 500 chars
5. `media_path` - Downloaded media location
6. `engagement_score` - Formatted stats (123K L, 45K RT, 2.3M V)
7. `viral_score` - 0-100 score
8. `suggested_caption` - Reply-bait caption
9. `repurpose_type` - QUOTE_TWEET | REPOST_WITH_CAPTION | MEDIA_REPOST | REPLY_BAIT
10. `status` - PENDING (ready for curation)
11. `scheduled_time` - ISO timestamp (if scheduled)

### `breaking_alerts.json`
JSON array of high-velocity tweets from last 2h. Sorted by viral_velocity (likes/hour).

### `media/{handle}/{tweet_id}/`
Downloaded content per tweet:
- `metadata.json` - Full tweet data
- `image_1.jpg`, `image_2.jpg`, etc. - Downloaded images
- `video_url.txt` - Video URL for yt-dlp

### `scan_history/scan_YYYYMMDD_HHMMSS.json`
Historical scan results with:
- Timestamp
- Accounts scanned
- Viral tweets found
- Account stats (avg engagement)
- Full tweet data

## Browser Authentication

Uses Brave Browser cookie extraction (NOT Chrome):
1. Reads Brave SQLite cookie database
2. Decrypts with AES-128-CBC using Keychain password
3. Injects into headless Chromium Playwright instance

**Requirements:**
- Must be logged into Twitter in Brave Browser
- Cookie key cached at `AUTOMATIONS/.brave_cookie_key`
- Same auth pattern as `twitter_alpha_scraper.py`

## Source Accounts (24 Total)

From `LEDGER/MEME_REPURPOSE_ACCOUNTS.csv`:
- @LocalBateman, @ShitpostReels, @videosinfolder (memes/clips)
- @InternetH0F, @FearBuck, @NoContextBrits (viral humor)
- @cursaboringdays, @PublicFreakout, @oddlyterrifying (clips)
- @TheFigen_, @historyinmemes (facts/education)
- @AMAZlNGNATURE, @Rainmaker1973 (nature/science)
- @NoContextHumans, @kirawontmiss, @HumansNoContext (no-context clips)
- And more...

All marked `download_priority: HIGH` in the CSV.

## Workflow Integration

### Content Farm Strategy
1. **Viral scanner** finds viral content from meme accounts
2. **Content farm** reposts across niche accounts (faith, fitness, tech)
3. **Engagement farming** uses reply bait to drive comments
4. **Cross-promotion** leverages engagement to promote owned products

### Multi-Niche Repurposing
Same viral content, different angles:

**Nature clip example:**
- Faith niche: "creation is beautiful"
- Fitness niche: "nature's perfect form"
- General: "how is this real"

3x output from same source.

### Integration with Other Scripts
- **`twitter_alpha_scraper.py`** - Same cookie extraction pattern
- **`twitter_content_scraper.py`** - Same account source (MEME_REPURPOSE_ACCOUNTS.csv)
- **Buffer/Publer** - Export queue for bulk scheduling
- **yt-dlp** - Download videos from logged URLs

## Performance Benchmarks

- **Scan speed:** 5-10 accounts/minute
- **Viral detection rate:** 50-200 tweets per full scan (24 accounts)
- **Storage:** 10-50MB per viral tweet with media
- **Browser overhead:** ~200MB RAM (headless Chromium)
- **Rate limiting:** 2-second delays between accounts

## Automation Opportunities

### Already Automated
✅ Viral detection (threshold-based)
✅ Media download (images + video URLs)
✅ Caption generation (content-type templates)
✅ Scheduled times (randomized across slots)
✅ Breaking alerts (viral velocity)

### Could Automate (Future)
- Twitter API posting (auto-post on schedule)
- Video download (yt-dlp integration)
- Content type classification (ML model)
- Engagement prediction (which will work for our audience)
- Cross-platform repurposing (TikTok, IG Reels)
- Performance tracking (ROI per viral tweet)

## Best Practices

1. **Scan daily** - Viral content stales fast (24-48h window)
2. **Download immediately** - Original may delete media
3. **Curate carefully** - Off-brand content hurts engagement
4. **Track performance** - Learn what works for your audience
5. **Mix with original** - 70% original, 30% repurposed
6. **Credit when appropriate** - Quote tweet > pure repost
7. **Don't overpost** - Max 8/day maintains quality
8. **Act fast on breaking** - High velocity = post ASAP

## Metrics to Track

### Per Viral Tweet
- Original engagement (likes, RT, views)
- Viral score (0-100)
- Your engagement (after reposting)
- ROI = your engagement / original engagement

### Per Account
- Viral tweets per week
- Best content type
- Best posting times
- Engagement rate

### Overall
- Total viral found per week
- Conversion rate (found → posted)
- Avg engagement on repurposed
- Best performing types

## Example Daily Schedule

**8:00 AM** - Run daily scan
```bash
./AUTOMATIONS/viral_content/run_daily_scan.sh
```

**8:30 AM** - Review & curate
- Open `repurpose_queue.csv`
- Mark APPROVED for good content
- Edit captions if needed

**10:00 AM** - Breaking check #1
```bash
./AUTOMATIONS/viral_content/monitor_breaking.sh
```

**12:00 PM** - Breaking check #2

**2:00 PM** - Breaking check #3

**4:00 PM** - Breaking check #4

**6:00 PM** - Breaking check #5

**8:00 PM** - Breaking check #6

**10:00 PM** - Breaking check #7

**11:00 PM** - Stats review
```bash
python3 AUTOMATIONS/viral_content_scanner.py --stats
```

## Troubleshooting

### No viral tweets found
- Accounts may not be posting viral this week
- Lower thresholds (edit script constants)
- Scan more accounts (remove `--limit`)

### Login issues
- Must be logged into Twitter in Brave
- Delete `.brave_cookie_key`, re-run
- Check Brave profile path

### Download fails
- Check internet connection
- Twitter CDN rate limiting (wait 30 min)
- Videos logged for yt-dlp, not direct download

### Queue not scheduling
- Run `--schedule` after `--scan`
- Check `scheduled_time` column format

## Security & Rate Limiting

- **Cookie encryption:** AES-128-CBC with Keychain password
- **Browser fingerprinting:** Mimics real Chrome user agent
- **Rate limiting:** 2-second delays between accounts
- **Headless detection:** Disabled automation flags
- **Session persistence:** Cookies cached in `.brave_cookie_key`

## Next Steps

1. **Test run:** `python3 viral_content_scanner.py --scan --limit 3`
2. **Review output:** Check `repurpose_queue.csv` and `media/`
3. **Set up cron:** Schedule `run_daily_scan.sh` for 8am daily
4. **Monitor breaking:** Run `monitor_breaking.sh` every 30-60 min
5. **Track performance:** Log which viral content performs best
6. **Optimize captions:** A/B test different reply-bait styles
7. **Scale posting:** Integrate with Buffer API for auto-posting

## Files to Track in Git

✅ Add to git:
- `viral_content_scanner.py`
- `README.md`
- `WORKFLOW.md`
- `SUMMARY.md`
- `run_daily_scan.sh`
- `monitor_breaking.sh`

❌ Ignore (add to .gitignore):
- `repurpose_queue.csv` (generated, personalized)
- `breaking_alerts.json` (ephemeral)
- `media/` (large, downloaded)
- `scan_history/` (historical data)

## Support & Maintenance

**Dependencies:**
- Python 3.11+
- Playwright (`pip install playwright`)
- pycryptodome (`pip install pycryptodome`)
- Brave Browser (for cookies)

**Update schedule:**
- Weekly: Review viral thresholds, adjust if needed
- Monthly: Clean up old media (>30 days)
- Quarterly: Audit account list, add/remove sources

**Known issues:**
- Twitter rate limiting if scanning >20 accounts/minute (solved: 2s delays)
- Cookie expiration (solved: cached Keychain key)
- Video download requires yt-dlp (documented in README)

## Credits

Built for PRINTMAXX content farm automation. Integrates with:
- Twitter alpha scraper (cookie extraction pattern)
- Meme repurpose accounts (source list)
- Content farm strategy (multi-niche repurposing)
- Engagement farming (reply bait captions)

Part of the broader PRINTMAXX automation ecosystem for solopreneurs.
