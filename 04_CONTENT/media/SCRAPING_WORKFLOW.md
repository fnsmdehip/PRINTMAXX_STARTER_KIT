# Media Scraping Workflow

**Purpose:** Capture viral images and videos for repurposing on niche accounts

---

## Directory Structure

```
CONTENT/media/
├── memes/              # Meme templates and edits
├── infographics/       # Flow charts, comparisons, data viz
├── reaction_clips/     # Short clips for quote tweets
├── scraped_videos/     # Full videos from TikTok/Twitter
└── scrape_log.csv      # Tracking all scraped content
```

---

## Quick Scrape Commands

### Twitter Video/Image
```bash
# Video download
yt-dlp "https://twitter.com/user/status/xxxxx" -o "CONTENT/media/scraped_videos/%(id)s.%(ext)s"

# Image - right click save or use:
curl -o "CONTENT/media/memes/filename.jpg" "image_url"
```

### TikTok Video
```bash
yt-dlp "https://tiktok.com/@user/video/xxxxx" -o "CONTENT/media/scraped_videos/%(id)s.%(ext)s"
```

### Reddit Video
```bash
# Use redditsave.com or:
yt-dlp "https://reddit.com/r/sub/comments/xxxxx" -o "CONTENT/media/scraped_videos/%(id)s.%(ext)s"
```

### Bulk Twitter Search Scrape
```bash
# Find viral content in niche (last 24h, 1000+ likes)
# Search: [niche] min_faves:1000 filter:media since:2026-01-22
# Then download individually
```

---

## Content Types to Target

### Memes (High Priority)
- **Iced watch/diamond grill edits** - Trump, tech bros, public figures
- **Rich family dinner format** - "How did we get so rich?" narrative
- **Looksmaxx edits** - Before/after transformations
- **Sigma male edits** - White Monster, grindset content
- **"We are so back" / "It's over"** - Reaction format

### Infographics
- Tech stack comparisons
- Revenue breakdowns
- Growth charts
- Process flowcharts

### Reaction Clips
- Short (3-10 sec) reaction videos
- Celebration clips
- Shock/surprise reactions
- Use for quote tweets

---

## Scrape Log Format

When adding to `scrape_log.csv`:

| Field | Description |
|-------|-------------|
| scrape_id | SCRAPE[NNN] |
| source_url | Original post URL |
| source_platform | twitter/tiktok/reddit/instagram |
| content_type | meme_image/video/infographic/reaction_clip |
| original_views | View count at scrape time |
| original_likes | Like count at scrape time |
| niche | tech/faith/fitness/general |
| potential_use | How we'll use it |
| scraped_date | YYYY-MM-DD |
| local_path | Path to downloaded file |
| status | IDENTIFIED/DOWNLOADED/USED |
| notes | Any additional context |

---

## Daily Scrape Routine (15 min)

1. **Check trending in each niche:**
   - Tech: Search `AI OR "indie hacker" OR solopreneur min_faves:1000 filter:media since:[yesterday]`
   - Faith: Search `prayer OR Christian OR Muslim min_faves:500 filter:media since:[yesterday]`
   - Fitness: Search `gym OR workout OR fitness min_faves:1000 filter:media since:[yesterday]`

2. **Log promising content** to scrape_log.csv with status IDENTIFIED

3. **Download top 3-5 pieces** per niche

4. **Organize by type** into appropriate folders

---

## Meme Formats Currently Trending (Update Weekly)

### Tech (Week of 2026-01-23)
- Rich family dinner meme (Claude Code Max $200/mo)
- "Permanent underclass" developer replacement jokes
- Ralph loops / autonomous agent memes
- Claude vs GPT vs Cursor debates

### General/Cross-Niche
- Agartha/hollow earth edits
- Looksmaxx transformations
- White Monster sigma male
- Iced out watch/grill edits
- "We are so back" / "It's over"

---

## Legal Notes

- Only use for inspiration/format reference
- Create original versions, don't repost directly
- Meme formats are fair game, specific art isn't
- Credit original creator when appropriate
- Avoid watermarked content

---

## Tools

- `yt-dlp` - Video downloads (Twitter, TikTok, Reddit, YouTube)
- `curl` - Direct image downloads
- ssstwitter.com - Twitter video (web fallback)
- redditsave.com - Reddit video (web fallback)
- Pinterest downloader - Pinterest images
