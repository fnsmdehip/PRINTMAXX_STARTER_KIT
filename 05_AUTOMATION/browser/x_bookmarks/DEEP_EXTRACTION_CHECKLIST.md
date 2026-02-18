# Deep X Bookmarks Extraction Checklist

**Purpose:** Comprehensive guide for extracting maximum alpha value from X/Twitter bookmarks
**Last Updated:** 2026-01-22
**Status:** Active

---

## Part A: Data Fields to Capture

### Standard Fields (Every Bookmark)

| Field | Type | Description | How to Extract |
|-------|------|-------------|----------------|
| `post_url` | string | Full URL including status ID | `https://x.com/{handle}/status/{id}` |
| `status_id` | string | Numeric tweet ID | Extract from URL or data attribute |
| `author_handle` | string | @username without @ | `[data-testid="User-Name"]` second line |
| `author_display_name` | string | Display name | `[data-testid="User-Name"]` first line |
| `post_text` | string | Full text (click "Show more" if truncated) | `[data-testid="tweetText"]` |
| `post_date` | ISO string | When posted | `time[datetime]` attribute |
| `likes` | number | Like count | `[data-testid="like"]` aria-label |
| `retweets` | number | Retweet count | `[data-testid="retweet"]` aria-label |
| `replies` | number | Reply count | `[data-testid="reply"]` aria-label |
| `views` | number | View count | Look for views metric element |
| `has_images` | boolean | Contains images | Check for `[data-testid="tweetPhoto"]` |
| `image_urls` | array | All image URLs | Extract src from tweet images |
| `has_video` | boolean | Contains video | Check for video player element |
| `external_link` | string | Link if shared | Card URL or `[data-testid="card.wrapper"]` |
| `is_thread` | boolean | Part of thread | Check for "Show this thread" |
| `is_quote_tweet` | boolean | Quotes another tweet | Check for quoted tweet container |

### Extended Fields (High-Value Posts Only)

Capture these for posts with revenue numbers, case studies, playbooks, or high engagement.

#### Author Profile Data

| Field | Type | Description | How to Extract |
|-------|------|-------------|----------------|
| `author_bio` | string | Full bio text | Navigate to profile, extract from bio element |
| `author_bio_link` | string | Link in bio | Profile link element |
| `author_profile_pic` | string | Profile image URL | Extract src, get original size (remove _normal, _bigger) |
| `author_banner` | string | Banner image URL | Profile banner element src |
| `author_followers` | number | Follower count | Profile stats |
| `author_following` | number | Following count | Profile stats |
| `author_verified` | boolean | Blue checkmark | Check verification badge |
| `author_created_at` | string | Account creation date | Profile joined date |

#### Top Replies Data

| Field | Type | Description | How to Extract |
|-------|------|-------------|----------------|
| `top_replies` | array | Top 3-5 replies sorted by engagement | Navigate to tweet, scroll replies |
| `author_reply` | object | If author replied with more context | Filter replies by original author |
| `funnel_replies` | array | Replies containing funnel keywords | Filter for "link", "DM", "bio" etc. |

### Reply Object Structure

```json
{
  "reply_url": "https://x.com/user/status/123",
  "author_handle": "@username",
  "text": "Full reply text",
  "likes": 150,
  "contains_link": true,
  "link_url": "https://example.com",
  "is_author_reply": false,
  "funnel_type": "bio_link"
}
```

---

## Part B: Funnel Detection Patterns

### Keywords to Watch For (in post text AND replies)

#### Bio/Link Patterns
- "link in bio"
- "bio link"
- "check my bio"
- "link below"
- "linktree"
- "stan.store"
- "gumroad"
- "lemonsqueezy"
- "whop.com"

#### DM Funnel Patterns
- "DM me"
- "send me a DM"
- "DM for"
- "message me"
- "comment X and I'll DM"
- "comment [word] for"

#### Product Mention Patterns
- "just launched"
- "I built"
- "I made"
- "check out"
- "try it free"
- "sign up"
- "join the waitlist"
- "early access"

#### Course/Info Product Patterns
- "cohort"
- "masterclass"
- "workshop"
- "course"
- "template"
- "playbook"
- "guide"
- "framework"

#### Booking/Call Patterns
- "calendly"
- "book a call"
- "schedule"
- "15 min"
- "free call"
- "let's chat"

#### Newsletter Patterns
- "newsletter"
- "subscribe"
- "weekly email"
- "join [number]+ subscribers"

---

## Part C: Revenue Signal Indicators

Posts with these patterns should be flagged as HIGH-VALUE:

### Revenue Numbers
- `$X` or `$Xk` or `$XM` patterns
- "MRR" or "ARR" mentions
- "k/mo" or "k/month"
- "/month" or "/year" revenue
- "made X in" patterns
- Specific percentages (conversion rates, growth)

### Case Study Signals
- "Here's how"
- "Step by step"
- "Breakdown:"
- "Thread on how"
- "0 to X"
- "from scratch"
- "in X days/weeks/months"

### Validation Signals
- High engagement (>1k likes for smaller accounts, >10k for big accounts)
- Many saves/bookmarks (can't see but infer from engagement ratio)
- Quote tweets showing the tactic worked for others

---

## Part D: ALPHA_STAGING.csv Template Row Format

```csv
alpha_id,source,source_url,category,title,description,actionable_steps,effort_level,roi_potential,risk_level,applies_to_niches,status,reviewed_date,reviewer_notes
```

### Field Guidelines

| Field | Format | Example |
|-------|--------|---------|
| `alpha_id` | ALPHA[NNN] | ALPHA086 (increment from last) |
| `source` | @handle or "X Bookmark" | @levelsio |
| `source_url` | Full tweet URL | https://x.com/levelsio/status/123 |
| `category` | One of: APP_FACTORY, CONTENT_FORMAT, OUTBOUND, GROWTH_HACK, TOOL_ALPHA, MONETIZATION, AI_INFLUENCER, COMPLIANCE | APP_FACTORY |
| `title` | Short descriptive title (5-10 words) | Screen Time Blocker Apps Making $600k/mo |
| `description` | Full context (tweet text + key context) | Raw tweet text or summary |
| `actionable_steps` | Numbered steps to execute | 1. Do X 2. Do Y 3. Do Z |
| `effort_level` | LOW, MEDIUM, HIGH | MEDIUM |
| `roi_potential` | LOW, MEDIUM, HIGH, HIGHEST | HIGHEST |
| `risk_level` | LOW, MEDIUM, HIGH | LOW |
| `applies_to_niches` | Comma-separated: AI, Faith, Fitness, ALL | ALL |
| `status` | PENDING_REVIEW | PENDING_REVIEW |
| `reviewed_date` | Leave empty | |
| `reviewer_notes` | Leave empty | |

---

## Part E: HIGH_SIGNAL_SOURCES.csv Discovery

When extracting bookmarks, identify new accounts to add to sources list.

### Criteria for Adding to HIGH_SIGNAL_SOURCES

1. **Revenue Transparency** - Shares real numbers
2. **Actionable Content** - Provides how-to not just results
3. **Consistent Posting** - Active in last 30 days
4. **Relevant Niche** - App building, outbound, growth hacking, AI, solopreneur
5. **Not Already in List** - Check existing sources first

### New Source Row Format

```csv
source_id,source_type,source_name,platform,url,focus_area,signal_quality,update_frequency,last_checked,notes,auto_monitor
SRC057,Twitter Account,@newhandle,X,https://x.com/newhandle,"Focus area description",HIGH,Daily,,"Brief note on why added.",TRUE
```

---

## Part F: Extraction Workflow

### Phase 1: Initial Scan (5 min)

1. Navigate to https://x.com/i/bookmarks
2. Run basic scraper to get all bookmark URLs
3. Export to JSON with standard fields

### Phase 2: High-Value Identification (10 min)

1. Filter exported bookmarks by:
   - Revenue signals in text
   - High engagement (>500 likes)
   - Contains "how", "step", "thread"
2. Create list of HIGH-VALUE post URLs

### Phase 3: Deep Extraction (2-5 min per high-value post)

For each HIGH-VALUE post:

1. **Navigate to post** - Open in new tab
2. **Check for "Show more"** - Click to get full text
3. **Scroll replies** - Capture top 5 by likes
4. **Check author profile** - Extract bio, link, images
5. **Document funnel** - What are they selling? How?

### Phase 4: Alpha Processing (15 min)

1. Format findings as ALPHA_STAGING.csv rows
2. Check for duplicates against existing source_urls
3. Categorize appropriately
4. Set status to PENDING_REVIEW

### Phase 5: Source Discovery (5 min)

1. Review all unique handles from extraction
2. Check which are NOT in HIGH_SIGNAL_SOURCES.csv
3. Evaluate against criteria
4. Add qualified new sources

---

## Part G: JavaScript Snippets for Manual Extraction

### Get Full Tweet Text (handles "Show more")

```javascript
// Click Show more if present, then get text
const showMore = document.querySelector('[data-testid="tweet-text-show-more-link"]');
if (showMore) showMore.click();
await new Promise(r => setTimeout(r, 500));
const text = document.querySelector('[data-testid="tweetText"]')?.innerText;
console.log(text);
```

### Get Engagement Metrics

```javascript
const metrics = {};
document.querySelectorAll('[data-testid="tweet"] [role="group"] button').forEach(btn => {
    const label = btn.getAttribute('aria-label') || '';
    if (label.includes('like')) metrics.likes = parseInt(label.match(/\d+/)?.[0] || '0');
    if (label.includes('Repost')) metrics.retweets = parseInt(label.match(/\d+/)?.[0] || '0');
    if (label.includes('repl')) metrics.replies = parseInt(label.match(/\d+/)?.[0] || '0');
});
console.log(metrics);
```

### Get Author Profile Data

```javascript
// Must be on profile page
const profile = {
    bio: document.querySelector('[data-testid="UserDescription"]')?.innerText,
    bioLink: document.querySelector('[data-testid="UserUrl"] a')?.href,
    followers: document.querySelector('a[href$="/followers"] span')?.innerText,
    following: document.querySelector('a[href$="/following"] span')?.innerText,
    profilePic: document.querySelector('img[src*="profile_images"]')?.src.replace('_normal', '_400x400'),
    banner: document.querySelector('img[src*="profile_banners"]')?.src
};
console.log(JSON.stringify(profile, null, 2));
```

### Get Top Replies

```javascript
// Must be on tweet detail page, scrolled to show replies
const replies = [];
document.querySelectorAll('[data-testid="cellInnerDiv"]').forEach((cell, i) => {
    if (i === 0) return; // Skip original tweet
    const text = cell.querySelector('[data-testid="tweetText"]')?.innerText;
    const handle = cell.querySelector('[data-testid="User-Name"] a')?.href.split('/').pop();
    const likes = cell.querySelector('[data-testid="like"]')?.getAttribute('aria-label')?.match(/\d+/)?.[0];
    if (text) replies.push({ handle, text, likes: parseInt(likes || '0') });
});
replies.sort((a, b) => b.likes - a.likes).slice(0, 5).forEach(r => console.log(r));
```

---

## Part H: Duplicate Prevention

### Before Adding to ALPHA_STAGING.csv

1. Check `source_url` column for exact URL match
2. Check `title` column for similar concepts
3. If similar concept exists but new URL has MORE detail, update existing row

### Existing Source URLs (Last 10 for Reference)

Check ALPHA_STAGING.csv before adding. Current entries include:
- https://x.com/knoxtwts/*
- https://x.com/pipelineabuser/*
- https://x.com/gregisenberg/*
- https://x.com/tatealax/*
- https://x.com/levelsio/*

Run this to get all existing source_urls:
```bash
cut -d',' -f3 /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LEDGER/ALPHA_STAGING.csv | tail -n +2 | sort | uniq
```

---

## Part I: Quality Control Checklist

Before marking extraction complete:

- [ ] All HIGH-VALUE posts have full text (no truncation)
- [ ] Author bios captured for posts with funnel signals
- [ ] Top replies checked for additional context/links
- [ ] External links captured and categorized
- [ ] No duplicate URLs in ALPHA_STAGING.csv
- [ ] Categories assigned correctly
- [ ] New high-signal accounts added to sources list
- [ ] Extraction log updated with session info

---

## Part J: Category Decision Tree

```
Post about...

Building apps/products?
  ├── Revenue numbers + how-to → APP_FACTORY
  ├── Tool stack/tech → TOOL_ALPHA
  └── Launch strategy → GROWTH_HACK

Selling/monetizing?
  ├── Course/info product → MONETIZATION
  ├── SaaS pricing → MONETIZATION
  └── Affiliate/ads → MONETIZATION

Getting users/customers?
  ├── Cold email/DM → OUTBOUND
  ├── Content strategy → CONTENT_FORMAT
  ├── Paid ads → GROWTH_HACK
  └── SEO/organic → GROWTH_HACK

AI-specific?
  ├── AI influencer/avatar → AI_INFLUENCER
  ├── AI tools → TOOL_ALPHA
  └── AI automation → APP_FACTORY

Legal/compliance?
  └── FTC/disclosure/legal → COMPLIANCE
```

---

## Quick Commands Reference

```bash
# Run basic extraction
python3 /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks/extract_alpha_from_bookmarks.py --latest

# Run deep analysis
python3 /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks/analyze_deep_bookmarks.py --latest

# Check for duplicates
cut -d',' -f3 /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LEDGER/ALPHA_STAGING.csv | sort | uniq -d

# Count current alpha entries
wc -l /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LEDGER/ALPHA_STAGING.csv

# Get last alpha_id
tail -1 /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LEDGER/ALPHA_STAGING.csv | cut -d',' -f1
```
