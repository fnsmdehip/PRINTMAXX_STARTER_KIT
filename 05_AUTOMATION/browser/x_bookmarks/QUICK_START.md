# X Bookmarks Extraction - Quick Start

## Option 1: Basic Extraction (Fast)

Best for: Quick alpha extraction from bookmarks

### Step 1: Extract Bookmarks

1. **Open Brave/Chrome** and go to https://x.com/i/bookmarks
2. **Open DevTools**: Press `Cmd+Option+I` (Mac) or `F12`
3. **Paste this script** in Console and press Enter:

```javascript
// X Bookmarks Auto-Extractor
(async () => {
    console.log('🚀 Starting extraction...');
    const bookmarks = [];
    let scrollCount = 0, prevCount = 0;
    while (scrollCount < 100) {
        const tweets = document.querySelectorAll('[data-testid="tweet"]');
        for (const tweet of tweets) {
            try {
                const text = tweet.querySelector('[data-testid="tweetText"]')?.innerText || '';
                const author = tweet.querySelector('[data-testid="User-Name"]')?.innerText.split('\n')[0] || '';
                const timestamp = tweet.querySelector('time')?.getAttribute('datetime') || '';
                let url = tweet.querySelector('a[href*="/status/"]')?.getAttribute('href') || '';
                if (url && !url.startsWith('http')) url = \`https://x.com\${url}\`;
                if (text && url) bookmarks.push({ text, author, timestamp, url });
            } catch (e) {}
        }
        const unique = {}; bookmarks.forEach(b => unique[b.url] = b);
        const current = Object.keys(unique).length;
        console.log(\`📊 \${current} bookmarks...\`);
        if (current === prevCount) break;
        prevCount = current;
        window.scrollBy(0, window.innerHeight);
        await new Promise(r => setTimeout(r, 1500));
        scrollCount++;
    }
    const final = Object.values(bookmarks.reduce((acc, b) => { acc[b.url] = b; return acc; }, {}));
    const blob = new Blob([JSON.stringify(final, null, 2)], {type: 'application/json'});
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
    a.download = \`x_bookmarks_\${new Date().toISOString().split('T')[0]}.json\`; a.click();
    console.log(\`✅ Downloaded \${final.length} bookmarks!\`);
})();
```

### Step 2: Extract Alpha

\`\`\`bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks
mv ~/Downloads/x_bookmarks_*.json .
python3 extract_alpha_from_bookmarks.py --latest
\`\`\`

**Output:** New alpha added to \`LEDGER/ALPHA_STAGING.csv\`

---

## Option 2: Deep Analysis (Comprehensive)

Best for: Full funnel analysis, profile inspiration, image collection

### What Deep Analysis Extracts:

1. **Full post text** - Opens each tweet to get complete text (not truncated)
2. **Images** - Collects images from business/tech posts for repurposing
3. **Funnel detection** - Identifies which posts lead to products/services
4. **Profile analysis** - Captures bio copy, profile pics, banner images

### Step 1: Run Deep Scraper

1. Go to https://x.com/i/bookmarks
2. Open DevTools and paste contents of \`deep_bookmark_scraper.js\`
3. Wait for completion (takes 2-5 minutes for 100 bookmarks)
4. Downloads \`x_bookmarks_deep_YYYY-MM-DD.json\`

### Step 2: Analyze Deep Data

\`\`\`bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks
mv ~/Downloads/x_bookmarks_deep_*.json .
python3 analyze_deep_bookmarks.py --latest
\`\`\`

**Output files:**
- \`LEDGER/PROFILE_ANALYSIS.csv\` - Bio copy, profile pics, banners
- \`LEDGER/CONTENT_ASSETS.csv\` - Images organized for repurposing
- \`LEDGER/FUNNEL_PATTERNS.csv\` - What products pair with what content types

### Step 3: Profile Deep Scrape (Optional)

For detailed analysis of standout profiles:

1. Go to any X page
2. Open DevTools and paste contents of \`profile_scraper.js\`
3. Run: \`scrapeProfiles(['@levelsio', '@tdinh_me', '@dannypostmaa'])\`
4. Downloads \`x_profiles_YYYY-MM-DD.json\`

---

## Content Filtering

The scraper automatically filters out:

**EXCLUDED** (politics, memes, culture war):
- Political content (trump, biden, maga, etc.)
- Culture war topics (cancel culture, dei, etc.)
- Memes and jokes (ratio, based, cope, etc.)
- Celebrity gossip, Sports, Breaking news

**INCLUDED** (business/tech/solopreneur):
- Revenue numbers (mrr, arr, $, k/mo)
- Building and launching (shipped, launched, mvp)
- Growth tactics (seo, traffic, conversions)
- Tech tools (api, automation, ai, gpt)
- Apps and products (app store, ios, android)

---

## Funnel Pattern Analysis

The deep analyzer detects posts that funnel to:

| Category | Keywords |
|----------|----------|
| SaaS | app, tool, software, platform |
| Course | cohort, masterclass, workshop |
| Template | notion, airtable, figma |
| Agency | done for you, full service |
| Consulting | coaching, mentorship, 1:1 |
| Newsletter | subscribe, weekly, daily email |
| Community | discord, slack, membership |
| Ebook | guide, pdf, playbook |

---

## Profile Copy Patterns Detected

- \`action_verb_start\` - "Building...", "Shipping..."
- \`social_proof_numbers\` - "10K+ users"
- \`credibility_past_role\` - "Ex-Google"
- \`title_lead\` - "Founder of..."
- \`pipe_separator\` - Using | to separate items
- \`revenue_mention\` - "$10k MRR"
- \`cta_dms\` - "DM me"
- \`cta_link\` - "Link in bio"

---

## Quick Commands

\`\`\`bash
# Basic extraction (fast)
python3 extract_alpha_from_bookmarks.py --latest

# Deep analysis
python3 analyze_deep_bookmarks.py --latest

# Dry run (preview without saving)
python3 extract_alpha_from_bookmarks.py --latest --dry-run
\`\`\`
