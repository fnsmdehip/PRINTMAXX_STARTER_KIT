# TikTok Viral Scraper Setup (Virlo API)

**Purpose:** Daily morning report of viral TikTok/Shorts/Reels content for alpha extraction
**API:** Virlo (dev.virlo.ai) - "Bloomberg for Short-Form Data"

---

## Quick Start

### 1. Get API Access

**Contact:** nic@virlo.ai
**Dev Portal:** https://dev.virlo.ai

Virlo collects millions of videos per day from TikTok, YouTube Shorts, and Instagram Reels. It ranks using:
- Velocity (how fast it's growing)
- Niche patterns
- Creator history
- Keyword matching

### 2. API Workflow

```
1. POST search query with keywords/niche
2. Get orbitId (job queued)
3. Poll for results (job processing)
4. When ready: structured list of videos with metrics
```

### 3. What You Get Per Video

- Platform (TikTok/Shorts/Reels)
- Performance metrics (views, likes, shares, comments)
- Upload timestamp
- Engagement rate
- Early velocity scoring
- Keyword match data
- Creator info

---

## Daily Scraper Script

### morning_viral_report.py

```python
#!/usr/bin/env python3
"""
Daily TikTok/Shorts/Reels Viral Report via Virlo API
Run: python morning_viral_report.py
Schedule: 6 AM daily via cron
"""

import os
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# Config
VIRLO_API_KEY = os.getenv('VIRLO_API_KEY')
VIRLO_BASE_URL = 'https://api.virlo.ai/v1'  # Adjust based on actual API
OUTPUT_DIR = Path('/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/AUTOMATIONS/tiktok_viral_scraper/reports')

# Niches to track (aligned with PRINTMAXX niches)
TRACKED_NICHES = [
    # Primary niches
    'faith christian prayer',
    'fitness workout gym',
    'tech ai automation',

    # Content farm niches
    'motivation quotes success',
    'relaxation sleep asmr',
    'true crime mystery',
    'history documentary',
    'animal pets cats',

    # Trending product niches
    'tiktok shop viral product',
    'amazon finds must have',

    # YouTube automation niches
    'faceless youtube automation',
    'ai generated content',
]

def search_virlo(keyword: str) -> dict:
    """Submit search job to Virlo API"""
    headers = {
        'Authorization': f'Bearer {VIRLO_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'query': keyword,
        'platforms': ['tiktok', 'youtube_shorts', 'instagram_reels'],
        'time_range': '24h',  # Last 24 hours
        'sort_by': 'velocity',  # Fastest growing
        'limit': 50
    }

    response = requests.post(
        f'{VIRLO_BASE_URL}/search',
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error searching {keyword}: {response.status_code}')
        return None

def poll_results(orbit_id: str, max_attempts: int = 10) -> dict:
    """Poll for search results"""
    headers = {'Authorization': f'Bearer {VIRLO_API_KEY}'}

    for attempt in range(max_attempts):
        response = requests.get(
            f'{VIRLO_BASE_URL}/results/{orbit_id}',
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ready':
                return data.get('results', [])

        time.sleep(5)  # Wait 5 seconds between polls

    return []

def calculate_virality_score(video: dict) -> float:
    """Calculate our own virality score"""
    views = video.get('views', 0)
    likes = video.get('likes', 0)
    comments = video.get('comments', 0)
    shares = video.get('shares', 0)
    hours_since_upload = video.get('hours_since_upload', 24)

    # Engagement rate
    if views > 0:
        engagement_rate = (likes + comments * 2 + shares * 3) / views
    else:
        engagement_rate = 0

    # Velocity (views per hour)
    velocity = views / max(hours_since_upload, 1)

    # Combined score
    score = (velocity * 0.4) + (engagement_rate * 100 * 0.3) + (shares * 0.3)

    return round(score, 2)

def generate_morning_report(all_results: dict) -> str:
    """Generate formatted morning report"""
    report_date = datetime.now().strftime('%Y-%m-%d')

    report = f"""# Viral Content Report - {report_date}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Source: Virlo API (TikTok, YouTube Shorts, Instagram Reels)

---

## Top Viral by Niche

"""

    for niche, videos in all_results.items():
        if not videos:
            continue

        report += f"### {niche.title()}\n\n"

        # Sort by our virality score
        sorted_videos = sorted(videos, key=lambda x: calculate_virality_score(x), reverse=True)[:10]

        for i, video in enumerate(sorted_videos, 1):
            score = calculate_virality_score(video)
            platform = video.get('platform', 'unknown')
            views = video.get('views', 0)
            likes = video.get('likes', 0)
            url = video.get('url', '')
            creator = video.get('creator', {}).get('username', 'unknown')

            report += f"""**{i}. [{platform}] @{creator}**
- Views: {views:,} | Likes: {likes:,}
- Virality Score: {score}
- URL: {url}

"""

    report += """---

## Alpha Extraction Checklist

For each high-potential video, ask:

1. **Format:** What makes this work? (hook, pacing, visual style)
2. **Niche:** Can we adapt this to faith/fitness/tech?
3. **Product:** Is there a product being sold? TikTok Shop?
4. **Bot Check:** Is engagement ratio normal? (likes:comments)
5. **Repurpose:** Can we make our version?

---

## Action Items

- [ ] Top 3 formats to test this week
- [ ] Products to research for affiliate
- [ ] Creator patterns to study
- [ ] Content ideas generated

"""

    return report

def save_report(report: str, raw_data: dict):
    """Save report and raw data"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime('%Y-%m-%d')

    # Save markdown report
    report_path = OUTPUT_DIR / f'viral_report_{date_str}.md'
    with open(report_path, 'w') as f:
        f.write(report)

    # Save raw JSON for further analysis
    json_path = OUTPUT_DIR / f'viral_raw_{date_str}.json'
    with open(json_path, 'w') as f:
        json.dump(raw_data, f, indent=2)

    print(f'Report saved: {report_path}')
    print(f'Raw data saved: {json_path}')

def main():
    """Run daily viral content scan"""
    print(f"Starting viral scan at {datetime.now()}")

    all_results = {}

    for niche in TRACKED_NICHES:
        print(f"Scanning: {niche}")

        # Submit search
        search_response = search_virlo(niche)
        if not search_response:
            continue

        orbit_id = search_response.get('orbit_id')
        if orbit_id:
            results = poll_results(orbit_id)
            all_results[niche] = results

        time.sleep(2)  # Rate limiting

    # Generate and save report
    report = generate_morning_report(all_results)
    save_report(report, all_results)

    print("Viral scan complete!")

if __name__ == '__main__':
    main()
```

---

## Cron Setup (Daily 6 AM)

```bash
# Edit crontab
crontab -e

# Add this line (runs at 6 AM daily)
0 6 * * * cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/AUTOMATIONS/tiktok_viral_scraper && /usr/bin/python3 morning_viral_report.py >> /tmp/viral_report.log 2>&1
```

---

## Alternative: Apify TikTok Scraper

If Virlo API not available, use Apify:

**URL:** https://apify.com/clockworks/tiktok-scraper

```python
from apify_client import ApifyClient

client = ApifyClient(os.getenv('APIFY_API_KEY'))

run_input = {
    "hashtags": ["viral", "trending", "fyp"],
    "resultsPerPage": 50,
    "shouldDownloadVideos": False,
}

run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

---

## Output Location

Reports saved to:
- `AUTOMATIONS/tiktok_viral_scraper/reports/viral_report_YYYY-MM-DD.md`
- `AUTOMATIONS/tiktok_viral_scraper/reports/viral_raw_YYYY-MM-DD.json`

---

## Integration with PRINTMAXX

### Auto-Extract to ALPHA_STAGING

After report generates, run extraction:

```python
def extract_alpha_from_viral(report_path: str):
    """Extract actionable alpha from viral report to ALPHA_STAGING.csv"""
    # Read report
    # Identify patterns
    # Generate alpha entries
    # Append to LEDGER/ALPHA_STAGING.csv with category=VIRAL_CONTENT
    pass
```

### Zero Waste Protocol

For each high-viral video discovered:
1. Note the format → Can we replicate?
2. Note the product → Can we affiliate?
3. Note the creator → Can we study their funnel?
4. Generate content → Posts about "what's trending"

---

## Sources

- [Virlo Official](https://virlo.ai/)
- [Virlo API Launch](https://finance.yahoo.com/news/virlo-launches-trends-virality-api-150000183.html)
- [Virlo Dev Community Post](https://dev.to/virlobuilder/i-built-an-api-that-tracks-viral-tiktok-reels-and-youtube-shorts-content-in-real-time-3593)
- [Apify TikTok Scraper](https://apify.com/clockworks/tiktok-scraper)
