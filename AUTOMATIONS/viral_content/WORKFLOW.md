# Viral Content Repurposing Workflow

Complete workflow for scanning, downloading, and repurposing viral content from meme accounts.

## Quick Start (5 Minutes)

```bash
# 1. Scan first 3 accounts (test run)
python3 AUTOMATIONS/viral_content_scanner.py --scan --limit 3

# 2. Download media
python3 AUTOMATIONS/viral_content_scanner.py --download

# 3. Check results
python3 AUTOMATIONS/viral_content_scanner.py --stats

# 4. Review queue
head -20 AUTOMATIONS/viral_content/repurpose_queue.csv
```

## Full Daily Workflow (30 Minutes)

### Morning: Scan All Accounts
```bash
# Scan all 24 meme accounts for viral content
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
python3 AUTOMATIONS/viral_content_scanner.py --scan

# Expected output:
# - 50-200 viral tweets found
# - repurpose_queue.csv generated
# - Account stats (average engagement per account)
```

### Download Media
```bash
# Download images and log video URLs
python3 AUTOMATIONS/viral_content_scanner.py --download

# Expected output:
# - Images saved to media/{handle}/{tweet_id}/
# - Video URLs logged for yt-dlp
# - metadata.json per tweet
```

### Generate Scheduled Queue
```bash
# Add random posting times across the day
python3 AUTOMATIONS/viral_content_scanner.py --schedule

# Expected output:
# - repurpose_queue.csv updated with scheduled_time column
# - Times spread across 4 peak engagement windows
# - Max 8 posts per day
```

### Review & Curate
```bash
# 1. Check stats
python3 AUTOMATIONS/viral_content_scanner.py --stats

# 2. Open queue in spreadsheet app
open AUTOMATIONS/viral_content/repurpose_queue.csv

# 3. Manual curation:
#    - Remove content that doesn't fit brand
#    - Edit suggested_caption if needed
#    - Adjust scheduled_time if needed
#    - Mark status as APPROVED for posts you want to use
```

### Post to Social (Manual or Automated)

**Option 1: Manual posting**
1. Open `repurpose_queue.csv`
2. For each APPROVED row:
   - Open `media_path` folder
   - Copy `suggested_caption`
   - Upload media to Twitter
   - Post with caption

**Option 2: Buffer/Publer bulk upload**
1. Filter `repurpose_queue.csv` for APPROVED rows
2. Convert to Buffer CSV format
3. Bulk upload to Buffer
4. Let Buffer post on schedule

**Option 3: API automation** (future enhancement)
- Script reads APPROVED rows
- Auto-uploads to Twitter API
- Posts on scheduled_time
- Updates status to POSTED

## Breaking News Monitor (Every 30 Minutes)

```bash
# Check for breaking viral content (last 2h)
python3 AUTOMATIONS/viral_content_scanner.py --breaking

# Review breaking_alerts.json
cat AUTOMATIONS/viral_content/breaking_alerts.json

# If breaking content found:
# 1. Download media immediately
# 2. Post ASAP (don't wait for schedule)
# 3. Capitalize on viral velocity
```

## Weekly Review

### Sunday Night: Full Scan + Schedule Week
```bash
# 1. Full scan of all accounts
python3 AUTOMATIONS/viral_content_scanner.py --scan

# 2. Download all media
python3 AUTOMATIONS/viral_content_scanner.py --download

# 3. Generate scheduled queue for the week
python3 AUTOMATIONS/viral_content_scanner.py --schedule

# 4. Review stats
python3 AUTOMATIONS/viral_content_scanner.py --stats

# 5. Curate queue (remove off-brand content)
# 6. Export to Buffer for the week
```

### Performance Analysis
1. Open `scan_history/` folder
2. Compare viral tweets found week-over-week
3. Identify which accounts produce most viral content
4. Adjust scanning frequency per account

## Content Curation Guidelines

### APPROVE if:
- Content fits brand voice (casual, meme energy)
- Media quality is good (not blurry, pixelated)
- No controversial/risky content
- Engagement is genuine (not botted)
- Caption makes sense for the content

### REJECT if:
- Off-brand (too corporate, too serious)
- Controversial (politics, religion, sensitive topics)
- Low quality media
- Engagement looks suspicious (10K likes, 3 comments)
- Content is already overused (everyone's posted it)

### EDIT CAPTION if:
- Suggested caption doesn't fit
- Better reply-bait angle exists
- Content needs context

## Video Download (yt-dlp)

After running `--download`, video URLs are logged in `video_url.txt` files.

### Download videos for all viral tweets:
```bash
# Install yt-dlp if needed
brew install yt-dlp

# Download all videos
find AUTOMATIONS/viral_content/media -name "video_url.txt" | while read f; do
    dir=$(dirname "$f")
    yt-dlp -a "$f" -o "${dir}/%(id)s.%(ext)s"
done
```

### Download videos for specific account:
```bash
# Example: Download all videos from @videosinfolder
cd AUTOMATIONS/viral_content/media/videosinfolder
find . -name "video_url.txt" | while read f; do
    dir=$(dirname "$f")
    yt-dlp -a "$f" -o "${dir}/%(id)s.%(ext)s"
done
```

## Posting Strategy

### Timing
- **Morning (8-11am):** Inspirational, nature, science content
- **Lunch (12-2pm):** Funny clips, memes, light content
- **Evening (5-8pm):** Viral clips, trending content
- **Night (9-11pm):** Funny memes, relatable content

### Caption Strategy
- Keep it lowercase (casual energy)
- 2-5 words max
- Reply bait (encourages comments)
- No context needed (content speaks for itself)

### Frequency
- Max 8 repurposed posts per day
- Mix with original content (70% original, 30% repurposed)
- Don't post same account twice in one day
- Space posts 2-3 hours apart

## File Organization

```
viral_content/
├── repurpose_queue.csv          # Main queue (edit this)
├── breaking_alerts.json         # Breaking viral content
├── media/                       # Downloaded media
│   ├── videosinfolder/         # Organized by account
│   │   ├── 123456789/          # Organized by tweet
│   │   │   ├── metadata.json
│   │   │   ├── image_1.jpg
│   │   │   └── video_url.txt
├── scan_history/               # Historical scans
│   └── scan_20260206_143022.json
└── README.md                   # Full documentation
```

## Integration with Content Farm

Viral content scanner feeds into the broader content farm strategy:

1. **Viral scanner** → finds viral content from meme accounts
2. **Content farm** → reposts with captions across niche accounts
3. **Engagement farming** → reply bait drives comments
4. **Cross-promotion** → use engagement to promote owned products

### Example: Faith Niche
1. Scan @AMAZlNGNATURE for nature clips
2. Repost with "how is this real" caption
3. Add faith angle in replies: "creation is beautiful"
4. Drive traffic to PrayerLock app

### Example: Fitness Niche
1. Scan @PublicFreakout for gym clips
2. Repost with "this is crazy" caption
3. Add fitness angle: "consistency > motivation"
4. Drive traffic to WalkToUnlock app

## Automation Opportunities

### Already Automated
- Viral detection (engagement thresholds)
- Media download (images + video URLs)
- Caption generation (content-type-based)
- Scheduled time slots (random distribution)

### Could Automate (Future)
- Twitter API posting (post on schedule)
- Video download (yt-dlp integration)
- Content type classification (ML model)
- Engagement prediction (which will work for our audience)
- Cross-platform repurposing (TikTok, IG Reels)
- Performance tracking (which viral content got engagement)

## Metrics to Track

### Per Viral Tweet
- Original engagement (likes, retweets, views)
- Viral score (0-100)
- Your engagement (after reposting)
- ROI (your engagement / original engagement)

### Per Account
- Average viral tweets per week
- Best content type (funny, nature, drama)
- Best posting times
- Engagement rate

### Overall
- Total viral tweets found per week
- Conversion rate (found → posted)
- Average engagement on repurposed content
- Best performing content types

## Troubleshooting

### No viral tweets found
- Accounts may not be posting viral content this week
- Try lowering thresholds (edit script constants)
- Scan more accounts (remove `--limit`)

### Download fails
- Check internet connection
- Twitter CDN may be rate limiting (wait 30 min)
- Video URLs logged for manual download with yt-dlp

### Login issues
- Make sure logged into Twitter in Brave
- Delete `.brave_cookie_key` and re-run
- Check Brave profile path in script

### Queue not scheduling
- Run `--schedule` after `--scan`
- Check `scheduled_time` column in CSV
- Times should be ISO format (YYYY-MM-DDTHH:MM:SS)

## Best Practices

1. **Scan daily** - Viral content goes stale fast (24-48h window)
2. **Download immediately** - Media may be deleted by original poster
3. **Curate carefully** - Off-brand content hurts engagement
4. **Track performance** - Learn what works for your audience
5. **Mix with original** - Don't become pure repost account
6. **Credit when appropriate** - Quote tweet > steal without attribution
7. **Don't overpost** - Max 8 per day maintains quality

## Example Daily Schedule

**8:00 AM** - Scan for viral content
```bash
python3 viral_content_scanner.py --scan
```

**8:15 AM** - Download media
```bash
python3 viral_content_scanner.py --download
```

**8:30 AM** - Review & curate queue
- Open `repurpose_queue.csv`
- Mark APPROVED for good content
- Edit captions if needed

**9:00 AM** - Schedule for the day
```bash
python3 viral_content_scanner.py --schedule
```

**Throughout day** - Breaking news check (every 2h)
```bash
python3 viral_content_scanner.py --breaking
```

**11:00 PM** - Stats review
```bash
python3 viral_content_scanner.py --stats
```

## Advanced: Multi-Niche Repurposing

Same viral content can be repurposed across multiple niches with different angles:

**Example: Nature clip of bird**
- **Faith niche:** "creation is beautiful"
- **Fitness niche:** "nature's perfect form"
- **General niche:** "how is this real"

Create separate queues per niche:
1. Copy `repurpose_queue.csv` to `repurpose_queue_faith.csv`
2. Edit captions for faith angle
3. Schedule different times per niche
4. Track which angle performs best

This 3x's your content output from the same viral source.
