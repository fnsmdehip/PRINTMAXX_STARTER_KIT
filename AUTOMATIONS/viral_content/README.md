# Viral Content Scanner

Production-ready automation for monitoring meme/viral Twitter accounts, detecting particularly viral content, and preparing repurposing queues.

## What It Does

1. **Viral Detection** - Flags tweets that meet viral thresholds:
   - 10,000+ likes OR
   - 2,000+ retweets OR
   - 500,000+ views OR
   - 5%+ engagement ratio (likes+retweets+replies / views) OR
   - 2x above account's average (outlier detection)

2. **Media Download** - Downloads images and logs video URLs from viral tweets
   - Images saved directly
   - Videos logged for yt-dlp batch download

3. **Repurpose Queue** - Generates CSV with:
   - Original tweet metadata
   - Engagement stats
   - Viral score (0-100)
   - Reply-bait captions (lowercase casual energy)
   - Repurpose type (QUOTE_TWEET, REPOST_WITH_CAPTION, MEDIA_REPOST, REPLY_BAIT)
   - Optional scheduled posting times

4. **Breaking News Detection** - Flags tweets with high viral velocity in last 2 hours
   - Viral velocity = likes per hour
   - Breaking threshold: 500+ likes/hour

5. **Stats Dashboard** - Shows viral content breakdown by account and type

## Usage

### Scan All Meme Accounts
```bash
python3 viral_content_scanner.py --scan
```

### Scan First 5 Accounts (Quick Test)
```bash
python3 viral_content_scanner.py --scan --limit 5
```

### Breaking Viral Content (Last 2 Hours)
```bash
python3 viral_content_scanner.py --breaking
```

### Generate Scheduled Queue
```bash
python3 viral_content_scanner.py --schedule
```
- Assigns random posting times across peak engagement windows:
  - 8am-11am
  - 12pm-2pm
  - 5pm-8pm
  - 9pm-11pm
- Max 8 posts per day
- Randomized to avoid posting in scrape order

### Download Media from Viral Queue
```bash
python3 viral_content_scanner.py --download
```

### Show Stats
```bash
python3 viral_content_scanner.py --stats
```

## Output Files

### `repurpose_queue.csv`
Main repurposing queue with columns:
- `original_handle` - Source account (@handle)
- `original_tweet_id` - Tweet ID
- `original_url` - Full Twitter URL
- `content_text` - Tweet text (first 500 chars)
- `media_path` - Path to downloaded media
- `engagement_score` - Likes, retweets, views formatted
- `viral_score` - 0-100 viral score
- `suggested_caption` - Reply-bait caption (2-5 words, lowercase)
- `repurpose_type` - QUOTE_TWEET | REPOST_WITH_CAPTION | MEDIA_REPOST | REPLY_BAIT
- `status` - PENDING (ready for posting)
- `scheduled_time` - ISO timestamp (if --schedule used)

### `breaking_alerts.json`
High viral velocity tweets from last 2 hours. JSON array sorted by velocity.

### `media/{handle}/{tweet_id}/`
Downloaded media organized by account and tweet:
- `metadata.json` - Full tweet metadata
- `image_1.jpg`, `image_2.jpg`, etc. - Downloaded images
- `video_url.txt` - Video URL for yt-dlp download

### `scan_history/scan_YYYYMMDD_HHMMSS.json`
Scan results with:
- Timestamp
- Accounts scanned
- Viral tweets found
- Account stats (average engagement per account)
- Full tweet data

## Reply-Bait Caption Templates

The scanner generates captions based on content type:

**Funny content:**
- "no way 💀"
- "this is crazy"
- "bro what"
- "i can't 😭"
- "not this"
- "lmaooo"

**Nature/science:**
- "how is this real"
- "nature is wild"
- "mind blown"
- "insane"

**Drama:**
- "thoughts?"
- "wild"
- "this is insane"
- "what do you think"

**Default:**
- "no way"
- "this is crazy"
- "insane"
- "wild"

Lowercase, 2-5 words max, casual energy - optimized for reply bait.

## Viral Scoring

Viral score (0-100) based on:
- Likes (max 30 points)
- Retweets (max 25 points)
- Views (max 25 points)
- Engagement ratio (max 20 points)

100 = mega viral. 70+ = very viral. 50+ = solid viral. Below 50 shouldn't appear (thresholds filter these out).

## Repurpose Types

**MEDIA_REPOST** - Has media, minimal text. Just repost the media with caption.

**REPOST_WITH_CAPTION** - Has media + text. Repost media with your own caption.

**QUOTE_TWEET** - Text-heavy (100+ chars). Quote tweet format works best.

**REPLY_BAIT** - Short text, no media. Just post as reply bait.

## Browser Authentication

Uses Brave Browser cookies (NOT Chrome). The script:
1. Extracts cookies from Brave's SQLite database
2. Decrypts with AES-128-CBC using Keychain password
3. Injects into headless Chromium Playwright instance

**Requirements:**
- Must be logged into Twitter in Brave Browser
- Brave must be the default browser for Twitter login
- Cookie extraction key cached at `AUTOMATIONS/.brave_cookie_key`

If login fails, check:
1. Are you logged into Twitter in Brave?
2. Is the Brave profile path correct?
3. Does the cached key file exist?

## Example Workflow

### Daily Viral Scan
```bash
# 1. Scan all meme accounts for viral content
python3 viral_content_scanner.py --scan

# 2. Download media from viral tweets
python3 viral_content_scanner.py --download

# 3. Generate scheduled posting queue
python3 viral_content_scanner.py --schedule

# 4. Check stats
python3 viral_content_scanner.py --stats
```

### Breaking News Monitor
```bash
# Run every 30 minutes to catch breaking viral content
python3 viral_content_scanner.py --breaking
```

Check `breaking_alerts.json` for high-velocity viral content.

### Quick Test (First 3 Accounts)
```bash
python3 viral_content_scanner.py --scan --limit 3 --download
```

## Integration with Existing Scripts

This script works alongside:
- `twitter_alpha_scraper.py` - Uses same cookie extraction pattern
- `twitter_content_scraper.py` - Both reference `MEME_REPURPOSE_ACCOUNTS.csv`

The viral scanner focuses on:
- **Viral detection** (engagement thresholds)
- **Media download** (images + video URLs)
- **Repurpose queue** (with captions and scheduling)

While `twitter_content_scraper.py` focuses on:
- **Content extraction** (text, media, metadata)
- **Account-wide scraping** (all recent posts)

Use both together:
- `twitter_content_scraper.py` for comprehensive account scraping
- `viral_content_scanner.py` for viral content detection and repurposing

## Source Accounts

Scans accounts from `LEDGER/MEME_REPURPOSE_ACCOUNTS.csv`:
- @LocalBateman (memes)
- @ShitpostReels (viral reels)
- @videosinfolder (viral clips)
- @InternetH0F (viral memes)
- @FearBuck (mixed viral)
- @NoContextBrits (UK humor clips)
- @cursaboringdays (viral content)
- @OldSchoolCool80 (nostalgia clips)
- @PublicFreakout (public freakout videos)
- @oddlyterrifying (oddly terrifying content)
- @TheFigen_ (viral facts)
- @historyinmemes (history memes)
- @NoContextHumans (no-context clips)
- @kirawontmiss (viral content)
- @HumansNoContext (similar to NoContextHumans)
- @AMAZlNGNATURE (nature clips)
- @Rainmaker1973 (science/nature)
- And more...

All accounts marked in the CSV with `download_priority: HIGH` get scanned.

## Performance

- **Scan speed:** ~5-10 accounts per minute (depends on scroll depth)
- **Storage:** ~10-50MB per viral tweet with media
- **Browser overhead:** Headless Chromium uses ~200MB RAM
- **Rate limiting:** 2-second delays between accounts to avoid Twitter rate limits

## Troubleshooting

**"No Twitter cookies found"**
- Make sure you're logged into Twitter in Brave Browser
- Check Brave profile path is correct
- Try deleting `.brave_cookie_key` and re-running (forces fresh Keychain read)

**"Not logged in"**
- Cookies may have expired. Log out and back in to Twitter in Brave
- Clear cache: Delete `AUTOMATIONS/.brave_cookie_key`

**"No viral tweets found"**
- Thresholds may be too high for smaller accounts
- Try scanning more accounts (`--limit 10` → `--limit 20`)
- Check if accounts are posting actively

**Download fails**
- Images require valid URLs from Twitter CDN
- Videos are logged for yt-dlp, not downloaded directly
- Check `media/` directory permissions

## Future Enhancements

Potential additions:
- Auto-posting to Buffer/Publer via API
- Video download with yt-dlp integration
- Viral trend analysis (what's going viral right now)
- Content type classification (funny vs drama vs nature)
- Engagement prediction (which viral content will work for our audience)
- Cross-platform repurposing (TikTok, Instagram Reels)

## Files Created

On first run, the script creates:
```
AUTOMATIONS/viral_content/
├── README.md (this file)
├── repurpose_queue.csv
├── breaking_alerts.json
├── media/
│   ├── {handle}/
│   │   ├── {tweet_id}/
│   │   │   ├── metadata.json
│   │   │   ├── image_1.jpg
│   │   │   └── video_url.txt
└── scan_history/
    └── scan_YYYYMMDD_HHMMSS.json
```

All directories created automatically if they don't exist.
