# Social Monitoring Workflow

**Purpose:** Monitor keywords on X/Reddit, filter for buying intent, alert for engagement opportunities.

**Workflow ID:** `social_monitoring_v1`
**Trigger:** Schedule (every 30 minutes)
**Est. Run Time:** 30-60 seconds per run

---

## Architecture Overview

```
Schedule Trigger (every 30 min)
              |
              v
    +-------------------+
    |                   |
    v                   v
X Search API     Reddit Search API
    |                   |
    v                   v
Parse Mentions    Parse Mentions
    |                   |
    +-------------------+
              |
              v
    Filter by Intent Keywords
              |
              v
    Classify Intent Level
    (HIGH/MEDIUM/LOW)
              |
              v
    Dedupe Against History
              |
              v
    HIGH Intent -> Slack Alert (Immediate)
    MEDIUM Intent -> Queue for Daily Review
    LOW Intent -> Log Only
              |
              v
    Save to LEDGER/SOCIAL_MENTIONS.csv
```

---

## Monitoring Keywords

### Primary Keywords (Product/Service)
```javascript
const PRIMARY_KEYWORDS = [
  // Your product/service terms
  "AI automation",
  "content automation",
  "solopreneur tools",
  "indie hacker",
  "side project",

  // Competitor mentions (opportunity)
  "looking for zapier alternative",
  "make.com vs",
  "n8n alternative",

  // Pain point keywords
  "hate manual posting",
  "tired of writing content",
  "need help with social media",
  "automate my business"
];
```

### Buying Intent Signals
```javascript
const BUYING_INTENT = {
  HIGH: [
    "looking for",
    "need a tool",
    "can anyone recommend",
    "what do you use for",
    "best tool for",
    "paying for",
    "budget for",
    "want to buy",
    "ready to invest"
  ],
  MEDIUM: [
    "how do you",
    "what's the best way",
    "anyone using",
    "experience with",
    "thoughts on",
    "considering"
  ],
  LOW: [
    "just launched",
    "check out my",
    "i built",
    "announcing"
  ]
};
```

---

## Node Configuration

### Node 1: Schedule Trigger
**Type:** `n8n-nodes-base.scheduleTrigger`
**Purpose:** Run every 30 minutes during active hours

```json
{
  "rule": {
    "interval": [
      {
        "field": "minutes",
        "triggerAtMinute": [0, 30]
      }
    ]
  }
}
```

**Note:** Consider reducing frequency to hourly during 11pm-6am to save API calls.

---

### Node 2: Get Monitoring Keywords
**Type:** `n8n-nodes-base.code`
**Purpose:** Define keywords to monitor

```javascript
const keywords = [
  // Core keywords
  'AI automation solopreneur',
  'automate content creation',
  'indie hacker tools',
  'side project automation',

  // Pain points
  'hate manual posting',
  'social media is exhausting',
  'content creation takes forever',

  // Buying signals
  'looking for automation tool',
  'recommend content tool',
  'best tool for scheduling',

  // Competitor alternatives
  'zapier alternative',
  'buffer alternative for',
  'hootsuite too expensive'
];

// Return each keyword as separate item for parallel processing
return keywords.map(kw => ({json: {keyword: kw}}));
```

---

### Node 3a: X/Twitter Search
**Type:** `n8n-nodes-base.httpRequest`
**Purpose:** Search X for keyword mentions

```json
{
  "method": "GET",
  "url": "https://api.twitter.com/2/tweets/search/recent",
  "authentication": "oAuth2Api",
  "qs": {
    "query": "={{ $json.keyword }} -is:retweet lang:en",
    "max_results": 20,
    "tweet.fields": "created_at,author_id,public_metrics,context_annotations",
    "expansions": "author_id",
    "user.fields": "username,name,public_metrics"
  }
}
```

**Note:** Requires Twitter API v2 access (Basic tier: $100/mo for 10k tweets/month)

**Alternative (Free):** Use Nitter or third-party scrapers, but check ToS.

---

### Node 3b: Reddit Search
**Type:** `n8n-nodes-base.httpRequest`
**Purpose:** Search Reddit for keyword mentions

```json
{
  "method": "GET",
  "url": "https://www.reddit.com/search.json",
  "qs": {
    "q": "={{ $json.keyword }}",
    "sort": "new",
    "limit": 25,
    "t": "day"
  },
  "headers": {
    "User-Agent": "PRINTMAXX-Monitor/1.0"
  }
}
```

**Response Fields:**
- `data.children[].data.title`
- `data.children[].data.selftext`
- `data.children[].data.permalink`
- `data.children[].data.author`
- `data.children[].data.subreddit`
- `data.children[].data.created_utc`

---

### Node 4a: Parse X Results
**Type:** `n8n-nodes-base.code`
**Purpose:** Normalize X data

```javascript
const response = $input.first().json;
const tweets = response.data || [];
const users = response.includes?.users || [];

// Create user lookup
const userMap = {};
users.forEach(u => {
  userMap[u.id] = u;
});

const mentions = tweets.map(tweet => {
  const user = userMap[tweet.author_id] || {};
  return {
    platform: 'X',
    id: tweet.id,
    text: tweet.text,
    author: user.username || 'unknown',
    author_name: user.name || '',
    author_followers: user.public_metrics?.followers_count || 0,
    url: `https://x.com/${user.username}/status/${tweet.id}`,
    likes: tweet.public_metrics?.like_count || 0,
    replies: tweet.public_metrics?.reply_count || 0,
    retweets: tweet.public_metrics?.retweet_count || 0,
    created_at: tweet.created_at,
    keyword: $('Get Monitoring Keywords').first().json.keyword
  };
});

return mentions.map(m => ({json: m}));
```

---

### Node 4b: Parse Reddit Results
**Type:** `n8n-nodes-base.code`
**Purpose:** Normalize Reddit data

```javascript
const response = $input.first().json;
const posts = response.data?.children || [];

const mentions = posts.map(post => {
  const d = post.data;
  return {
    platform: 'Reddit',
    id: d.id,
    text: `${d.title}\n\n${d.selftext || ''}`.trim(),
    author: d.author,
    author_name: d.author,
    author_followers: 0, // Reddit doesn't expose this easily
    url: `https://reddit.com${d.permalink}`,
    likes: d.ups || 0,
    replies: d.num_comments || 0,
    retweets: 0,
    created_at: new Date(d.created_utc * 1000).toISOString(),
    keyword: $('Get Monitoring Keywords').first().json.keyword,
    subreddit: d.subreddit
  };
});

return mentions.map(m => ({json: m}));
```

---

### Node 5: Merge All Mentions
**Type:** `n8n-nodes-base.merge`
**Purpose:** Combine X and Reddit results

```json
{
  "mode": "append"
}
```

---

### Node 6: Classify Intent
**Type:** `n8n-nodes-base.code`
**Purpose:** Determine buying intent level

```javascript
const HIGH_INTENT = [
  'looking for',
  'need a tool',
  'can anyone recommend',
  'what do you use for',
  'best tool for',
  'paying for',
  'budget for',
  'want to buy',
  'ready to invest',
  'willing to pay',
  'shopping for',
  'in the market for'
];

const MEDIUM_INTENT = [
  'how do you',
  "what's the best way",
  'anyone using',
  'experience with',
  'thoughts on',
  'considering',
  'thinking about',
  'exploring options',
  'any recommendations'
];

const SPAM_INDICATORS = [
  'check out my',
  'i just launched',
  'use my referral',
  'dm me',
  'link in bio',
  'free trial',
  'limited time',
  'act now'
];

const items = $input.all();

return items.map(item => {
  const text = item.json.text.toLowerCase();

  // Check for spam first
  const isSpam = SPAM_INDICATORS.some(s => text.includes(s));
  if (isSpam) {
    return {json: {...item.json, intent_level: 'SPAM', intent_reason: 'Promotional content'}};
  }

  // Check high intent
  const highMatch = HIGH_INTENT.find(s => text.includes(s));
  if (highMatch) {
    return {json: {...item.json, intent_level: 'HIGH', intent_reason: `Matched: "${highMatch}"`}};
  }

  // Check medium intent
  const medMatch = MEDIUM_INTENT.find(s => text.includes(s));
  if (medMatch) {
    return {json: {...item.json, intent_level: 'MEDIUM', intent_reason: `Matched: "${medMatch}"`}};
  }

  // Default to low
  return {json: {...item.json, intent_level: 'LOW', intent_reason: 'General mention'}};
});
```

---

### Node 7: Check Duplicates
**Type:** `n8n-nodes-base.googleSheets`
**Purpose:** Load existing mentions to dedupe

```json
{
  "operation": "read",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "SOCIAL_MENTIONS",
  "range": "B:B"
}
```

---

### Node 8: Filter New Only
**Type:** `n8n-nodes-base.code`
**Purpose:** Remove already-seen mentions

```javascript
const existingIds = $('Check Duplicates').all().map(n => n.json.id);
const existingSet = new Set(existingIds);

const mentions = $('Classify Intent').all();
const newMentions = mentions.filter(m => !existingSet.has(m.json.id));

return newMentions;
```

---

### Node 9: Route by Intent
**Type:** `n8n-nodes-base.switch`
**Purpose:** Different handling based on intent

```json
{
  "rules": {
    "rules": [
      {
        "outputKey": "HIGH",
        "conditions": {
          "conditions": [
            {
              "leftValue": "={{ $json.intent_level }}",
              "rightValue": "HIGH",
              "operator": "equals"
            }
          ]
        }
      },
      {
        "outputKey": "MEDIUM",
        "conditions": {
          "conditions": [
            {
              "leftValue": "={{ $json.intent_level }}",
              "rightValue": "MEDIUM",
              "operator": "equals"
            }
          ]
        }
      },
      {
        "outputKey": "LOW_OR_SPAM",
        "conditions": {
          "conditions": [
            {
              "leftValue": "={{ $json.intent_level }}",
              "rightValue": "HIGH",
              "operator": "notEquals"
            },
            {
              "leftValue": "={{ $json.intent_level }}",
              "rightValue": "MEDIUM",
              "operator": "notEquals"
            }
          ]
        }
      }
    ]
  }
}
```

---

### Node 10a: HIGH Intent - Immediate Alert
**Type:** `n8n-nodes-base.slack`
**Purpose:** Alert immediately for engagement

```json
{
  "channel": "#high-intent-leads",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*HIGH INTENT DETECTED*\n\n*Platform:* {{ $json.platform }}\n*Author:* @{{ $json.author }} ({{ $json.author_followers }} followers)\n*Keyword:* {{ $json.keyword }}\n*Intent Signal:* {{ $json.intent_reason }}\n\n>>> {{ $json.text.substring(0, 300) }}...\n\n<{{ $json.url }}|View & Engage>"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "Engage Now"},
          "url": "{{ $json.url }}",
          "style": "primary"
        },
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "Skip"},
          "action_id": "skip_mention"
        }
      ]
    }
  ]
}
```

---

### Node 10b: MEDIUM Intent - Queue for Review
**Type:** `n8n-nodes-base.googleSheets`
**Purpose:** Add to daily review queue

```json
{
  "operation": "append",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "SOCIAL_MENTIONS",
  "columns": {
    "value": {
      "status": "QUEUED_REVIEW",
      "alert_sent": "FALSE"
    }
  }
}
```

---

### Node 10c: LOW/SPAM - Log Only
**Type:** `n8n-nodes-base.googleSheets`
**Purpose:** Store for analytics, no action

```json
{
  "operation": "append",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "SOCIAL_MENTIONS",
  "columns": {
    "value": {
      "status": "LOGGED",
      "alert_sent": "FALSE"
    }
  }
}
```

---

### Node 11: Save All Mentions
**Type:** `n8n-nodes-base.googleSheets`
**Purpose:** Central log of all mentions

```json
{
  "operation": "append",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "SOCIAL_MENTIONS",
  "columns": {
    "mappingMode": "defineBelow",
    "value": {
      "timestamp": "={{ $now.toISO() }}",
      "id": "={{ $json.id }}",
      "platform": "={{ $json.platform }}",
      "author": "={{ $json.author }}",
      "author_followers": "={{ $json.author_followers }}",
      "text": "={{ $json.text.substring(0, 500) }}",
      "url": "={{ $json.url }}",
      "keyword_matched": "={{ $json.keyword }}",
      "intent_level": "={{ $json.intent_level }}",
      "intent_reason": "={{ $json.intent_reason }}",
      "likes": "={{ $json.likes }}",
      "replies": "={{ $json.replies }}",
      "subreddit": "={{ $json.subreddit || '' }}",
      "status": "NEW",
      "engaged": "FALSE",
      "engagement_result": ""
    }
  }
}
```

---

## Human Approval Checkpoint

For HIGH intent mentions, the Slack alert includes:
1. Full context of the mention
2. Direct link to engage
3. Skip button if not relevant

**After engaging:**
Manually update `SOCIAL_MENTIONS` sheet:
- `engaged`: TRUE
- `engagement_result`: Replied / DM'd / Booked call / Not relevant

---

## Required Credentials

| Credential | Purpose | Cost |
|------------|---------|------|
| `twitterApi` | X/Twitter search | $100/mo (Basic) |
| `googleSheetsOAuth2Api` | Data storage | Free |
| `slackApi` | Alerts | Free |

**Free Alternative for Twitter:**
- Use Nitter instances + scraping
- Or Social Searcher free tier (100 mentions/day)

---

## Environment Variables

```bash
TWITTER_BEARER_TOKEN=your_bearer_token
LEDGER_SHEET_ID=1abc...xyz
```

---

## Engagement Templates

When HIGH intent alert fires, use these response templates:

### X/Twitter
```
Hey! Saw you're looking for [solution]. I've been using [your tool/approach] - saved me X hours/week.

Happy to share what worked. DM open if you want specifics.
```

### Reddit
```
I was in the same spot last month. Here's what worked for me:

1. [Specific tactic]
2. [Tool recommendation with why]
3. [Result you got]

The key thing that made the difference was [insight].
```

**Rules:**
- Don't pitch immediately
- Provide value first
- Be specific with results
- Match the platform tone

---

## Cost Estimation

| Component | Monthly Cost |
|-----------|--------------|
| Twitter API (Basic) | $100 |
| Reddit API | Free |
| n8n Cloud | $20 |
| **Total** | ~$120/mo |

**Cost Optimization:**
- Start with Reddit only (free)
- Add Twitter when ROI proven
- Monitor only during active hours

---

## Error Handling

### Twitter API Errors
- **429 Rate Limited:** Back off 15 minutes
- **401 Unauthorized:** Refresh OAuth tokens
- **503 Service Unavailable:** Retry in 5 minutes

### Reddit API Errors
- **429 Rate Limited:** Wait 60 seconds
- **403 Forbidden:** Check User-Agent header

### General
- Log errors to `MONITORING_ERRORS` sheet
- Alert if 3+ consecutive failures
- Continue with available platform if one fails

---

## Testing Checklist

- [ ] Schedule trigger fires correctly
- [ ] X search returns results
- [ ] Reddit search returns results
- [ ] Intent classification is accurate
- [ ] Duplicates are filtered
- [ ] HIGH intent triggers Slack alert
- [ ] MEDIUM intent queues for review
- [ ] All mentions save to sheet
- [ ] Links work and go to correct posts
- [ ] Error handling doesn't crash workflow

---

## Analytics Queries

**Weekly Engagement Report:**
```
=COUNTIFS(SOCIAL_MENTIONS!intent_level, "HIGH", engaged, "TRUE")
```

**Conversion from Mentions:**
```
=COUNTIFS(engagement_result, "Booked call")
```

**Top Performing Keywords:**
```
=QUERY(SOCIAL_MENTIONS, "SELECT keyword_matched, COUNT(id) WHERE intent_level='HIGH' GROUP BY keyword_matched ORDER BY COUNT(id) DESC")
```
