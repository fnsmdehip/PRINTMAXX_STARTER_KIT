# Competitor Tracking Workflow

**Purpose:** Monitor competitor social accounts, track content performance, generate weekly summaries.

**Workflow ID:** `competitor_tracking_v1`
**Trigger:** Daily (for data collection) + Weekly (for summary)
**Est. Run Time:** 2-5 minutes per competitor

---

## Architecture Overview

```
Daily Collection Flow:
    Schedule (daily 9am)
            |
            v
    Load Competitor List
            |
            v
    For Each Competitor:
        |
        +-> Scrape X Profile
        +-> Scrape LinkedIn
        +-> Scrape Website/Blog
            |
            v
    Extract Content Metrics
            |
            v
    Save to COMPETITOR_INTEL.csv

Weekly Summary Flow:
    Schedule (Monday 8am)
            |
            v
    Load Week's Data
            |
            v
    Claude: Analyze Trends
            |
            v
    Generate Summary Report
            |
            v
    Send to Slack/Email
```

---

## Competitor Configuration

### Define Competitors
Store in `LEDGER/COMPETITORS.csv`:

```csv
competitor_id,name,x_handle,linkedin_url,website,blog_url,category,priority
COMP001,Zapier,@zapier,https://linkedin.com/company/zapier,https://zapier.com,https://zapier.com/blog,automation,HIGH
COMP002,Make,@make_hq,https://linkedin.com/company/make-formerly-integromat,https://make.com,https://make.com/blog,automation,HIGH
COMP003,Buffer,@buffer,https://linkedin.com/company/buffer,https://buffer.com,https://buffer.com/resources,social,MEDIUM
COMP004,Hootsuite,@hootsuite,https://linkedin.com/company/hootsuite,https://hootsuite.com,https://blog.hootsuite.com,social,MEDIUM
```

---

## Node Configuration

### Daily Collection Workflow

#### Node 1: Daily Schedule
**Type:** `n8n-nodes-base.scheduleTrigger`

```json
{
  "rule": {
    "interval": [{"field": "days", "triggerAtHour": 9}]
  }
}
```

---

#### Node 2: Load Competitors
**Type:** `n8n-nodes-base.googleSheets`

```json
{
  "operation": "read",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "COMPETITORS",
  "range": "A:H"
}
```

---

#### Node 3: Split by Competitor
**Type:** `n8n-nodes-base.splitInBatches`

```json
{
  "batchSize": 1,
  "options": {}
}
```

---

#### Node 4: Scrape X Profile
**Type:** `n8n-nodes-base.httpRequest`
**Purpose:** Get recent tweets and metrics

```json
{
  "method": "GET",
  "url": "https://api.twitter.com/2/users/by/username/{{ $json.x_handle.replace('@', '') }}",
  "authentication": "oAuth2Api",
  "qs": {
    "user.fields": "public_metrics,description,created_at",
    "tweet.fields": "created_at,public_metrics"
  }
}
```

Then fetch recent tweets:
```json
{
  "method": "GET",
  "url": "https://api.twitter.com/2/users/{{ $json.user_id }}/tweets",
  "qs": {
    "max_results": 10,
    "tweet.fields": "created_at,public_metrics,context_annotations"
  }
}
```

---

#### Node 5: Parse X Data
**Type:** `n8n-nodes-base.code`

```javascript
const user = $('Scrape X Profile').first().json.data;
const tweets = $('Scrape X Tweets').first().json.data || [];

// Calculate engagement metrics
const totalEngagement = tweets.reduce((sum, t) => {
  const metrics = t.public_metrics || {};
  return sum + (metrics.like_count || 0) + (metrics.retweet_count || 0) + (metrics.reply_count || 0);
}, 0);

const avgEngagement = tweets.length > 0 ? totalEngagement / tweets.length : 0;

// Find top performing tweet
const topTweet = tweets.reduce((best, t) => {
  const score = (t.public_metrics?.like_count || 0) + (t.public_metrics?.retweet_count || 0) * 2;
  const bestScore = (best.public_metrics?.like_count || 0) + (best.public_metrics?.retweet_count || 0) * 2;
  return score > bestScore ? t : best;
}, tweets[0] || {});

return [{
  json: {
    platform: 'X',
    competitor: $('Load Competitors').first().json.name,
    handle: user.username,
    followers: user.public_metrics?.followers_count || 0,
    following: user.public_metrics?.following_count || 0,
    tweets_count: user.public_metrics?.tweet_count || 0,
    posts_analyzed: tweets.length,
    avg_engagement: Math.round(avgEngagement),
    top_post_text: topTweet.text || '',
    top_post_likes: topTweet.public_metrics?.like_count || 0,
    top_post_url: topTweet.id ? `https://x.com/${user.username}/status/${topTweet.id}` : '',
    posting_frequency: tweets.length > 0 ? `${tweets.length} posts in last fetch` : 'Unknown',
    collected_at: new Date().toISOString()
  }
}];
```

---

#### Node 6: Scrape Blog/RSS
**Type:** `n8n-nodes-base.rssFeedRead`

```json
{
  "url": "={{ $json.blog_url }}/rss",
  "options": {}
}
```

**Fallback if no RSS:**
Use HTTP Request + Code node to parse HTML for recent posts.

---

#### Node 7: Parse Blog Data
**Type:** `n8n-nodes-base.code`

```javascript
const items = $input.all();

// Get last 5 posts
const recentPosts = items.slice(0, 5).map(item => ({
  title: item.json.title,
  link: item.json.link,
  pubDate: item.json.pubDate,
  description: item.json.description?.substring(0, 200) || ''
}));

// Analyze posting frequency
const dates = recentPosts.map(p => new Date(p.pubDate));
const daysBetween = dates.length > 1
  ? (dates[0] - dates[dates.length - 1]) / (1000 * 60 * 60 * 24) / (dates.length - 1)
  : 0;

return [{
  json: {
    platform: 'Blog',
    competitor: $('Load Competitors').first().json.name,
    recent_posts: recentPosts,
    posts_per_month: daysBetween > 0 ? Math.round(30 / daysBetween) : 0,
    latest_post_date: dates[0]?.toISOString() || '',
    latest_post_title: recentPosts[0]?.title || '',
    topics: recentPosts.map(p => p.title).join(' | '),
    collected_at: new Date().toISOString()
  }
}];
```

---

#### Node 8: Combine Platform Data
**Type:** `n8n-nodes-base.code`

```javascript
const xData = $('Parse X Data').first().json;
const blogData = $('Parse Blog Data').first().json;
const competitor = $('Load Competitors').first().json;

return [{
  json: {
    competitor_id: competitor.competitor_id,
    competitor_name: competitor.name,
    date: new Date().toISOString().split('T')[0],

    // X metrics
    x_followers: xData.followers,
    x_avg_engagement: xData.avg_engagement,
    x_top_post: xData.top_post_text?.substring(0, 200),
    x_top_post_likes: xData.top_post_likes,

    // Blog metrics
    blog_posts_month: blogData.posts_per_month,
    blog_latest_title: blogData.latest_post_title,
    blog_topics: blogData.topics?.substring(0, 300),

    // Meta
    priority: competitor.priority,
    collected_at: new Date().toISOString()
  }
}];
```

---

#### Node 9: Save to Intel Sheet
**Type:** `n8n-nodes-base.googleSheets`

```json
{
  "operation": "append",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "COMPETITOR_INTEL",
  "columns": {
    "mappingMode": "autoMapInputData"
  }
}
```

---

### Weekly Summary Workflow

#### Node W1: Weekly Schedule
**Type:** `n8n-nodes-base.scheduleTrigger`

```json
{
  "rule": {
    "interval": [{
      "field": "weeks",
      "triggerAtDay": 1,
      "triggerAtHour": 8
    }]
  }
}
```

---

#### Node W2: Load Week's Data
**Type:** `n8n-nodes-base.googleSheets`

```json
{
  "operation": "read",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "COMPETITOR_INTEL",
  "range": "A:N",
  "options": {
    "dataLocationOnSheet": "lastNRows",
    "lastNRows": 100
  }
}
```

---

#### Node W3: Filter to Last 7 Days
**Type:** `n8n-nodes-base.code`

```javascript
const data = $input.all();
const weekAgo = new Date();
weekAgo.setDate(weekAgo.getDate() - 7);

const thisWeek = data.filter(item => {
  const date = new Date(item.json.date);
  return date >= weekAgo;
});

// Group by competitor
const byCompetitor = {};
thisWeek.forEach(item => {
  const name = item.json.competitor_name;
  if (!byCompetitor[name]) {
    byCompetitor[name] = [];
  }
  byCompetitor[name].push(item.json);
});

// Calculate week-over-week changes
const summaries = Object.entries(byCompetitor).map(([name, records]) => {
  const latest = records[records.length - 1];
  const earliest = records[0];

  return {
    competitor: name,
    x_followers_current: latest.x_followers,
    x_followers_change: latest.x_followers - earliest.x_followers,
    x_avg_engagement: Math.round(records.reduce((s, r) => s + r.x_avg_engagement, 0) / records.length),
    top_post_of_week: records.reduce((best, r) =>
      r.x_top_post_likes > (best.x_top_post_likes || 0) ? r : best, {}
    ).x_top_post,
    top_post_likes: Math.max(...records.map(r => r.x_top_post_likes)),
    blog_posts_this_week: records.reduce((s, r) => s + (r.blog_posts_month / 4), 0),
    notable_topics: [...new Set(records.flatMap(r => (r.blog_topics || '').split(' | ')))].slice(0, 5)
  };
});

return [{json: {summaries, weekStart: weekAgo.toISOString(), weekEnd: new Date().toISOString()}}];
```

---

#### Node W4: Claude Analysis
**Type:** `n8n-nodes-base.httpRequest`

```json
{
  "method": "POST",
  "url": "https://api.anthropic.com/v1/messages",
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": {
    "model": "claude-3-haiku-20240307",
    "max_tokens": 1500,
    "system": "You analyze competitor data and provide actionable insights. Be specific. No fluff. Focus on: 1) What content is working for them, 2) Gaps we can exploit, 3) Tactics to copy.",
    "messages": [{
      "role": "user",
      "content": "Analyze this week's competitor data and provide insights:\n\n{{ JSON.stringify($json.summaries, null, 2) }}\n\nProvide:\n1. Top performing competitor this week and why\n2. Content formats/topics that worked\n3. Engagement trends (up/down)\n4. Opportunities we should exploit\n5. Tactics to copy or avoid"
    }]
  }
}
```

---

#### Node W5: Format Report
**Type:** `n8n-nodes-base.code`

```javascript
const summaries = $('Filter to Last 7 Days').first().json.summaries;
const analysis = $('Claude Analysis').first().json.content[0].text;

// Build report
let report = `# Weekly Competitor Intelligence Report\n`;
report += `**Week of:** ${$('Filter to Last 7 Days').first().json.weekStart.split('T')[0]}\n\n`;

report += `## Quick Stats\n\n`;
report += `| Competitor | Followers | Change | Avg Engagement | Top Post Likes |\n`;
report += `|------------|-----------|--------|----------------|----------------|\n`;

summaries.forEach(s => {
  const change = s.x_followers_change >= 0 ? `+${s.x_followers_change}` : s.x_followers_change;
  report += `| ${s.competitor} | ${s.x_followers_current?.toLocaleString()} | ${change} | ${s.x_avg_engagement} | ${s.top_post_likes} |\n`;
});

report += `\n## Top Performing Content\n\n`;
summaries.forEach(s => {
  if (s.top_post_of_week) {
    report += `**${s.competitor}:** ${s.top_post_of_week.substring(0, 150)}... (${s.top_post_likes} likes)\n\n`;
  }
});

report += `## AI Analysis\n\n${analysis}\n`;

return [{json: {report, summaries}}];
```

---

#### Node W6: Send to Slack
**Type:** `n8n-nodes-base.slack`

```json
{
  "channel": "#competitor-intel",
  "text": "Weekly Competitor Report Ready",
  "attachments": [
    {
      "color": "#36a64f",
      "title": "Competitor Intelligence - Week Summary",
      "text": "{{ $json.report.substring(0, 3000) }}",
      "footer": "Auto-generated by n8n"
    }
  ]
}
```

---

#### Node W7: Archive Report
**Type:** `n8n-nodes-base.googleSheets`

```json
{
  "operation": "append",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "COMPETITOR_REPORTS",
  "columns": {
    "value": {
      "week_of": "={{ $('Filter to Last 7 Days').first().json.weekStart }}",
      "report": "={{ $json.report }}",
      "generated_at": "={{ $now.toISO() }}"
    }
  }
}
```

---

## Required Credentials

| Credential | Purpose | Cost |
|------------|---------|------|
| `twitterApi` | X profile/tweet data | $100/mo (Basic) |
| `anthropicApi` | Weekly analysis | ~$0.50/report |
| `googleSheetsOAuth2Api` | Data storage | Free |
| `slackApi` | Reports | Free |

---

## Environment Variables

```bash
TWITTER_BEARER_TOKEN=your_bearer_token
ANTHROPIC_API_KEY=sk-ant-...
LEDGER_SHEET_ID=1abc...xyz
```

---

## Human Approval Checkpoints

This workflow is primarily observational, but approval is needed for:

1. **Adding new competitors:** Review before adding to tracking
2. **Acting on insights:** Weekly report should prompt discussion on which tactics to adopt
3. **Removing competitors:** If competitor becomes irrelevant

---

## Error Handling

### Twitter API Errors
- **429 Rate Limited:** Skip competitor, try tomorrow
- **404 Not Found:** Account may be suspended, flag for review

### RSS/Blog Errors
- **No RSS found:** Try alternative blog URL formats
- **Empty feed:** May have changed URL, flag for update

### General
- Log all errors to `COMPETITOR_ERRORS` sheet
- Continue with available data if partial failure
- Alert if HIGH priority competitor fails

---

## Cost Estimation

| Component | Monthly Cost |
|-----------|--------------|
| Twitter API (Basic) | $100 |
| Claude Haiku (4 reports) | $2 |
| n8n Cloud | $20 |
| **Total** | ~$125/mo |

---

## Metrics to Track

**Per Competitor:**
- Follower growth rate (week over week)
- Average engagement per post
- Posting frequency
- Top performing content themes
- New product/feature announcements

**Cross-Competitor:**
- Who's growing fastest
- Which content formats dominate
- Common topics/themes
- Pricing changes
- Partnership announcements

---

## Testing Checklist

- [ ] Competitors CSV loads correctly
- [ ] X profile data fetches
- [ ] Tweet data fetches
- [ ] Blog/RSS parses correctly
- [ ] Data saves to COMPETITOR_INTEL
- [ ] Weekly filter works
- [ ] Claude analysis generates
- [ ] Report formats correctly
- [ ] Slack message sends
- [ ] Report archives to sheet

---

## Expansion Ideas

1. **LinkedIn tracking:** Add company page scraping
2. **Product Hunt monitoring:** Track competitor launches
3. **G2/Capterra reviews:** Monitor sentiment trends
4. **Pricing page monitoring:** Alert on pricing changes
5. **Job postings:** Track hiring as growth signal
