# Viral Content Scanner - Quick Start

## First Time Setup (2 Minutes)

1. **Install dependencies:**
```bash
pip3 install playwright pycryptodome
playwright install chromium
```

2. **Verify login:**
- Open Brave Browser
- Go to x.com and make sure you're logged in
- This script will use your Brave cookies

3. **Test run:**
```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
python3 AUTOMATIONS/viral_content_scanner.py --scan --limit 3
```

Expected: Scans first 3 meme accounts, finds viral tweets.

## Daily Usage (5 Minutes)

### Option 1: One Command
```bash
./AUTOMATIONS/viral_content/run_daily_scan.sh
```
Does everything: scan → download → schedule → stats

### Option 2: Manual Steps
```bash
# 1. Scan all accounts
python3 AUTOMATIONS/viral_content_scanner.py --scan

# 2. Download media
python3 AUTOMATIONS/viral_content_scanner.py --download

# 3. Schedule queue
python3 AUTOMATIONS/viral_content_scanner.py --schedule

# 4. Review
open AUTOMATIONS/viral_content/repurpose_queue.csv
```

## Breaking News Monitor (Every 30-60 Min)

```bash
./AUTOMATIONS/viral_content/monitor_breaking.sh
```

If breaking content found → post immediately (don't wait for schedule).

## Common Commands

```bash
# Quick test (3 accounts)
python3 AUTOMATIONS/viral_content_scanner.py --scan --limit 3

# Full scan (all 24 accounts)
python3 AUTOMATIONS/viral_content_scanner.py --scan

# Breaking viral (last 2h)
python3 AUTOMATIONS/viral_content_scanner.py --breaking

# Stats
python3 AUTOMATIONS/viral_content_scanner.py --stats
```

## Output Files

- `repurpose_queue.csv` - Main queue to review/curate
- `breaking_alerts.json` - Breaking viral content
- `media/{handle}/{tweet_id}/` - Downloaded images/videos
- `scan_history/` - Historical scans

## Curation Workflow

1. **Open queue:**
```bash
open AUTOMATIONS/viral_content/repurpose_queue.csv
```

2. **Review each row:**
- Check content_text (is it on-brand?)
- Check viral_score (higher = more viral)
- Check suggested_caption (edit if needed)
- Check media_path (images downloaded?)

3. **Mark status:**
- Change PENDING → APPROVED for content you want to post
- Delete rows for content you reject

4. **Post:**
- Upload to Buffer/Publer OR
- Post manually OR
- Wait for auto-posting integration (future)

## Video Downloads

Videos are logged in `video_url.txt` files. Download with yt-dlp:

```bash
# Download all videos
find AUTOMATIONS/viral_content/media -name "video_url.txt" | while read f; do
    dir=$(dirname "$f")
    yt-dlp -a "$f" -o "${dir}/%(id)s.%(ext)s"
done
```

## Troubleshooting

**"No Twitter cookies found"**
→ Make sure you're logged into Twitter in Brave Browser

**"No viral tweets found"**
→ Accounts may not be posting viral content this week. Try more accounts: remove `--limit`

**Download fails**
→ Check internet. Twitter CDN may be rate limiting (wait 30 min).

**Login fails**
→ Delete `.brave_cookie_key` and re-run to force fresh Keychain read

## Next Steps

After first successful scan:

1. ✅ Review `repurpose_queue.csv`
2. ✅ Curate content (mark APPROVED)
3. ✅ Set up daily cron: `crontab -e`
   ```
   0 8 * * * cd /path/to/PRINTMAXX && ./AUTOMATIONS/viral_content/run_daily_scan.sh
   */30 * * * * cd /path/to/PRINTMAXX && ./AUTOMATIONS/viral_content/monitor_breaking.sh
   ```
4. ✅ Track performance (which viral content works best)
5. ✅ Optimize captions (A/B test reply-bait styles)

## Documentation

- **README.md** - Complete technical docs
- **WORKFLOW.md** - Daily/weekly workflow guides
- **SUMMARY.md** - System overview
- **QUICKSTART.md** - This file

## Support

If stuck, check:
1. README.md for detailed docs
2. WORKFLOW.md for workflow examples
3. `--help` flag on any command
4. Scan history for what worked before

Built for PRINTMAXX content farm automation.
