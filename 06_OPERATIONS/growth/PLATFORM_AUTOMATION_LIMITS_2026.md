# Platform Automation Limits 2026

**Last Updated:** 2026-01-25
**Purpose:** Comprehensive reference for automation limits, ban triggers, warmup protocols, and recovery options across all major platforms.
**Update Cadence:** Weekly audit required. Check UPDATE_LOG at bottom for changes.

---

## TABLE OF CONTENTS

1. [Quick Reference Matrix](#quick-reference-matrix)
2. [Instagram](#instagram)
3. [TikTok](#tiktok)
4. [Twitter/X](#twitterx)
5. [LinkedIn](#linkedin)
6. [YouTube](#youtube)
7. [Email Platforms](#email-platforms)
8. [Proxy Requirements](#proxy-requirements)
9. [Tools Status](#tools-status)
10. [Ban Recovery Protocols](#ban-recovery-protocols)
11. [Update Log](#update-log)

---

## QUICK REFERENCE MATRIX

### Daily Action Limits (Safe vs Risky)

| Platform | Action | New Account | Warmed Account | Aggressive (Risk) |
|----------|--------|-------------|----------------|-------------------|
| **Instagram** | Follows | 10-20 | 30-50 | 80-100 |
| | Unfollows | 10-20 | 30-50 | 100+ |
| | Likes | 50-80 | 100-150 | 300+ |
| | Comments | 5-10 | 20-30 | 50+ |
| | DMs | 5-10 | 10-20 | 50+ |
| | Story views | Unlimited | Unlimited | Unlimited |
| **TikTok** | Follows | 30-50 | 100-200 | 300+ (very risky) |
| | Likes | 100-200 | 300-500 | 800+ |
| | Comments | 20-30 | 50-100 | 150+ |
| | Videos/day | 1-3 | 3-5 | 8+ |
| **X/Twitter** | Follows | 50-100 | 200-400 | 500+ |
| | Likes | 200-300 | 500-1000 | 1500+ |
| | Tweets | 5-10 | 20-50 | 100+ |
| | DMs | 20-30 | 50-100 | 150+ |
| | Retweets | 50-100 | 200-300 | 400+ |
| **LinkedIn** | Connections | 10-20 | 20-30 | 50+ (danger zone) |
| | Messages | 25-50 | 50-100 | 150+ |
| | Profile views | 100-200 | 300-500 | 800+ |
| | InMails/mo | 0 (free) | 50 (Core) | 150 (Advanced) |
| **YouTube** | Subscriptions | 20-30 | 50-100 | 150+ |
| | Comments | 10-20 | 30-50 | 80+ |
| | Likes | 50-100 | 150-300 | 500+ |
| **Email** | New inbox | 5-10 | 25-30 | 50+ |
| | Warmed inbox | 25-30 | 50-80 | 100+ |
| | Multi-inbox | 150-250/day | 300-500/day | 750+ |

### Hourly Action Limits (Conservative)

| Platform | Follows | Likes | Comments | DMs |
|----------|---------|-------|----------|-----|
| Instagram | 5-8 | 15-25 | 3-5 | 2-5 |
| TikTok | 15-25 | 40-60 | 8-12 | 5-10 |
| X/Twitter | 15-30 | 50-80 | 10-20 | 5-10 |
| LinkedIn | 3-5 | 10-15 | 3-5 | 3-5 |
| YouTube | 8-15 | 20-40 | 5-10 | N/A |

---

## INSTAGRAM

### Current Safe Limits (January 2026)

**CRITICAL:** Instagram limits are now personalized per account based on trust score and history. These are general guidelines.

#### Action Limits Table

| Action | New (<2mo) | Established (2-6mo) | Aged (6mo+) | Aggressive |
|--------|------------|---------------------|-------------|------------|
| Follows/day | 10-20 | 30-50 | 50-80 | 100+ |
| Unfollows/day | 10-20 | 30-50 | 50-100 | 150+ |
| Likes/day | 50-80 | 100-150 | 200-300 | 400+ |
| Comments/day | 5-10 | 20-30 | 40-60 | 80+ |
| DMs/day | 5-10 | 10-20 | 30-50 | 80+ |
| Story views | Unlimited | Unlimited | Unlimited | Unlimited |
| Posts/day | 1-2 | 3-5 | 5-10 | 15+ |
| Reels/day | 1-2 | 3-5 | 5-8 | 10+ |

#### Hourly Limits (Never Exceed)

| Action | Safe | Maximum |
|--------|------|---------|
| Follows | 5-8 | 15 |
| Unfollows | 5-8 | 15 |
| Likes | 15-25 | 50 |
| Comments | 3-5 | 10 |
| DMs | 2-5 | 10 |

#### Time Spacing Requirements

- **Between actions:** 30-90 seconds (randomized)
- **Between follow/unfollow:** 12-24 hours minimum
- **Active hours:** 8-16 hours/day (not 24/7)
- **Burst prevention:** Max 10 actions, then 5-10 min break

### Account Age Requirements

| Age | Status | Recommendations |
|-----|--------|-----------------|
| 0-14 days | New | Manual only, no automation, no links |
| 14-30 days | Fresh | Light scheduling, manual engagement |
| 1-3 months | Developing | Can introduce light automation |
| 3-6 months | Established | Standard automation limits |
| 6+ months | Aged | Full limits, more lenient |

### Warmup Protocol

```
WEEK 1-2: Manual Foundation
Day 1-3: Create account, complete profile 100%, follow 5-10, scroll 10+ min
Day 4-7: Like 30-50, reply 5-10 genuinely, follow 10-20, first story (no links)
Day 8-14: Like 50-80, reply 10-20, follow 20-30, first posts (images only)

WEEK 3-4: Light Automation
Day 15-21: Introduce scheduling only, 50% manual engagement continues
Day 22-28: Story viewing automation OK, keep engagement manual

MONTH 2+: Scaled Automation (if no blocks)
- 30-50 follows/day max
- 100-150 likes/day
- 20-30 comments/day
- Monitor constantly for action blocks
```

### Known Ban Triggers

**INSTANT BAN RISK:**
- Chrome extensions (any that access IG)
- Using same proxy for multiple accounts
- Follow/unfollow same users repeatedly
- Posting identical content across accounts
- Automated DMs with links
- Using unauthorized API access

**SHADOWBAN TRIGGERS:**
- Banned hashtags (check before using)
- Rapid follow/unfollow (same day)
- Mass actions from hashtag pages
- Low engagement rate (bot detection)
- Reporting by multiple users
- Content policy violations

**ACTION BLOCK TRIGGERS:**
- Exceeding hourly limits
- Inconsistent activity patterns
- New account + aggressive actions
- Multiple violations in 24 hours
- Using web instead of app for actions

### Recovery Options

**Action Block Recovery:**
1. STOP all automation immediately
2. Do NOT log out (makes it worse)
3. Wait 24-72 hours (check periodically)
4. Clear app cache and data
5. Resume at 50% previous volume
6. If persists 7+ days, change proxy IP

**Shadowban Recovery:**
1. Stop ALL automation
2. Remove banned hashtags from recent posts
3. Post quality content daily for 14 days
4. Heavy manual engagement
5. Do NOT delete flagged content
6. Check status: shadowban.app/instagram

**Disabled Account Recovery:**
1. Appeal immediately via app
2. Provide ID if requested
3. Wait 24-48 hours for response
4. If denied, wait and appeal again (max 3 attempts)
5. Don't create new account with same details

### Tools Still Working (January 2026)

| Tool | Status | Notes |
|------|--------|-------|
| Jarvee | RISKY | Desktop automation, detection rate high |
| Kicksta | SAFE | AI-targeted, managed service |
| Growthoid | SAFE | Human team, best for quality |
| Upleap | SAFE | Managed, hands-off |
| Buffer/Later | SAFE | Scheduling only, no engagement |
| Story viewer bots | SAFE | Low detection, use residential proxies |

**AVOID:**
- Any Chrome extension
- Mobile automation apps
- Anything promising 1000+ followers/week
- Free automation tools

---

## TIKTOK

### Current Safe Limits (January 2026)

**CRITICAL:** TikTok has the most aggressive detection. Automation is NOT recommended.

#### Action Limits Table

| Action | New (<30d) | Established (30-90d) | Aged (90d+) |
|--------|------------|----------------------|-------------|
| Follows/day | 30-50 | 100-200 | 200-300 |
| Likes/day | 100-200 | 300-500 | 500-800 |
| Comments/day | 20-30 | 50-100 | 100-150 |
| Videos/day | 1-3 | 3-5 | 5-8 |
| DMs/day | 10-20 | 30-50 | 50-80 |

#### Hourly Limits

| Action | Safe | Maximum |
|--------|------|---------|
| Follows | 10-15 | 25 |
| Likes | 30-50 | 80 |
| Comments | 8-12 | 20 |

### Account Age Requirements

| Age | Status | Actions Allowed |
|-----|--------|-----------------|
| 0-7 days | Probation | Watch only, no posting, no links |
| 7-14 days | New | First posts (duets/stitches), no bio link |
| 14-30 days | Fresh | Regular posting, can add bio link |
| 30-90 days | Established | Full features, standard limits |
| 90+ days | Aged | Highest trust, more lenient |

### Warmup Protocol

```
WEEK 1: Watch Only Phase
Day 1-3: Watch 30+ min, like 50-100, follow 10-20
Day 4-7: Watch 20+ min, like 100-150, follow 20-30, comment 10-20

WEEK 2: Engagement Phase
Day 8-10: First posts (DUETS/STITCHES ONLY), continue engagement
Day 11-14: More original posts, heavy engagement

WEEK 3-4: Content Phase
Day 15-21: 2-3 posts/day, optimize for FYP
Day 22-28: Scale to 3-5 posts/day

MONTH 2+: Growth Phase
- Consistent posting 3-5x/day
- Engage on trending videos
- NO automation (manual or nothing)
```

### Known Ban Triggers

**INSTANT BAN RISK:**
- VPN usage (any VPN = flag)
- Location services OFF
- Multiple accounts on same device
- Browser automation (detected immediately)
- Using web version for posting
- Buying followers/views from bad providers

**SHADOWBAN TRIGGERS:**
- Posting too frequently (>10/day)
- Using the same sounds/hashtags repeatedly
- Low watch time on videos
- High skip rate on content
- Sudden follower spikes
- Template caption patterns (detected by AI)

**ACCOUNT RESTRICTION:**
- Copyright strikes (3 = permanent)
- Community guideline violations
- Spam reports from users
- Duplicate content detection

### Recovery Options

**Shadowban Recovery:**
1. Stop posting for 24-48 hours
2. Watch content normally (train algorithm)
3. Resume with 1 post/day only
4. Use different sounds and hashtags
5. Check shadowban status via reach metrics

**Account Restriction Recovery:**
1. Appeal in-app immediately
2. Wait for review (24-72 hours)
3. If denied, wait 30 days and appeal again
4. Don't create new account on same device

### Tools Status (January 2026)

| Tool | Status | Notes |
|------|--------|-------|
| Any automation | NOT RECOMMENDED | TikTok detection is too aggressive |
| TokUpgrade | RISKY | Mixed results, high ban rate |
| Manual growth | SAFE | Only recommended approach |
| Scheduling (native) | SAFE | TikTok's built-in scheduler |

**CRITICAL:** For TikTok, manual is the only safe approach. Use real phone + mobile proxy if needed.

---

## TWITTER/X

### Current Safe Limits (January 2026)

**X is the most lenient platform for automation.** Still requires caution.

#### Action Limits Table

| Action | New (<14d) | Established (14-30d) | Aged (30d+) |
|--------|------------|----------------------|-------------|
| Follows/day | 50-100 | 200-400 | 400-600 |
| Likes/day | 200-300 | 500-1000 | 1000-1500 |
| Tweets/day | 5-10 | 20-50 | 50-100 |
| DMs/day | 20-30 | 50-100 | 100-150 |
| Retweets/day | 50-100 | 200-300 | 300-500 |
| Quote tweets/day | 20-30 | 50-100 | 100-150 |

#### Hourly Limits

| Action | Safe | Maximum |
|--------|------|---------|
| Follows | 15-30 | 50 |
| Likes | 50-80 | 150 |
| Tweets | 5-10 | 20 |
| DMs | 5-10 | 20 |

### API Rate Limits (For Developers)

| Endpoint | Free Tier | Basic ($100/mo) | Pro ($5000/mo) |
|----------|-----------|-----------------|----------------|
| Tweets/month (read) | 10,000 | 10,000 | 1,000,000 |
| Tweets/month (post) | 1,500 | 3,000 | 300,000 |
| User lookups | 100/day | 10,000/mo | 500,000/mo |

### Account Age Requirements

| Age | Status | Recommendations |
|-----|--------|-----------------|
| 0-7 days | New | Engage only, no posting, no links |
| 7-14 days | Fresh | Text-only posts, continue engagement |
| 14-30 days | Developing | Add images/links, light scheduling |
| 30+ days | Established | Full automation possible |

### Warmup Protocol

```
WEEK 1: Engagement Only
Day 1-3: Follow 20-30, like 50-80, reply 10-15
Day 4-7: Follow 30-50, like 80-120, reply 15-25, join Spaces (listen)

WEEK 2: Light Posting
Day 8-10: First tweets (TEXT ONLY), continue engagement
Day 11-14: More tweets, quote tweets, reply threads

WEEK 3-4: Content Phase
Day 15-21: Posts with images, can add links
Day 22-28: Introduce scheduling (Hypefury, Buffer)

MONTH 2+: Automation Phase
- Can use TweetHunter/Hypefury
- Maintain 30% manual engagement
- Monitor for shadowban
```

### Known Ban Triggers

**SUSPENSION TRIGGERS:**
- Mass follow/unfollow same day
- Automated DMs with links (spam filter)
- Posting identical content across accounts
- Coordinated inauthentic behavior
- Evading previous suspension
- Platform manipulation (fake engagement)

**SHADOWBAN TRIGGERS:**
- Using banned/sensitive keywords
- High ratio of promotional content
- Low engagement relative to posting frequency
- Aggressive following without engagement
- Multiple reports from users

### Recovery Options

**Suspension Recovery:**
1. Appeal immediately via support
2. Be honest, claim misunderstanding
3. Never mention automation
4. Wait 24-72 hours
5. If denied, wait 30 days and appeal again

**Shadowban Recovery:**
1. Check status: shadowban.eu
2. Stop all automation 48 hours
3. Manual engagement only
4. Avoid sensitive/political keywords
5. Post quality content daily
6. Usually clears in 7-14 days

### Tools Still Working (January 2026)

| Tool | Status | Notes |
|------|--------|-------|
| Hypefury | SAFE | Best for creators, scheduling + engagement |
| TweetHunter | SAFE | AI tweets + CRM, growth-focused |
| Buffer | SAFE | Scheduling only |
| Hootsuite | SAFE | Scheduling only |
| Phantombuster | RISKY | Powerful but detection possible |
| Jarvee | RISKY | Desktop automation |

---

## LINKEDIN

### Current Safe Limits (January 2026)

**CRITICAL:** LinkedIn has the strictest enforcement. NO Chrome extensions. Cloud automation only.

#### Action Limits Table

| Action | Free Account | Sales Navigator |
|--------|--------------|-----------------|
| Connection requests/day | 20-30 | 50-100 |
| Connection requests/week | 100 max | 200 max |
| Messages/day | 25-50 | 100-150 |
| Profile views/day | 100-200 | 300-500 |
| InMails/month | 0 | 50 (Core) / 150 (Advanced) |
| Post engagement/day | 30-50 | 50-100 |

#### Hourly Limits

| Action | Safe | Maximum |
|--------|------|---------|
| Connection requests | 3-5 | 8 |
| Messages | 5-10 | 15 |
| Profile views | 15-25 | 50 |

### Account Age Requirements

| Age | Status | Actions |
|-----|--------|---------|
| 0-14 days | New | Profile completion only, no outreach |
| 14-30 days | Fresh | Light engagement, 10 connections/day max |
| 30-90 days | Developing | Standard limits, can use Sales Nav |
| 90+ days | Established | Full limits, automation possible |

### Warmup Protocol

```
WEEK 1: Profile Foundation
Day 1-3: Complete profile 100%, add professional photo
Day 4-7: Connect with 50+ real contacts (colleagues, classmates)

WEEK 2: Engagement Phase
Day 8-14: Engage on 10-20 posts/day, publish 1-2 text posts

WEEK 3-4: Outreach Introduction
Day 15-21: 10-15 connection requests/day (personalized)
Day 22-28: Increase to 20-25/day with messaging

MONTH 2+: Scaling
- Max 30/day connections (free), 50-100 (Sales Nav)
- Use voice notes in DMs (3x response rate)
- Cloud automation only (Expandi, Dripify)
```

### Known Ban Triggers

**INSTANT RESTRICTION:**
- Chrome extensions (ANY - instant detection)
- Desktop automation (Jarvee, Phantombuster)
- Connection request without personalization
- High rejection rate (>50%)
- Rapid profile viewing

**ACCOUNT RESTRICTION:**
- Exceeding weekly connection limits
- Spam reports from users
- Low SSI score + automation signals
- Using LinkedIn from multiple locations

### Recovery Options

**Connection Limit Restriction:**
1. Stop all outreach immediately
2. Wait 7 days
3. Resume at 10/day only
4. Add more personalization

**Account Restriction Recovery:**
1. Appeal via LinkedIn Help
2. Provide ID if requested
3. Wait 2-4 weeks
4. Resume with extreme caution

### Tools Status (January 2026)

| Tool | Status | Notes |
|------|--------|-------|
| Expandi | SAFEST | Cloud-based, best for automation |
| Dripify | SAFE | Good sequences, cloud-based |
| Waalaxy | MODERATE | Multi-channel, some risk |
| Phantombuster | RISKY | Powerful but desktop = risk |
| Any Chrome extension | BANNED | Instant detection, account restriction |
| Manual | SAFEST | Time-intensive but 0 risk |

---

## YOUTUBE

### Current Safe Limits (January 2026)

#### Action Limits Table

| Action | New Channel | Established Channel |
|--------|-------------|---------------------|
| Subscriptions/day | 20-30 | 50-100 |
| Likes/day | 50-100 | 150-300 |
| Comments/day | 10-20 | 30-50 |
| Video uploads/day | 1-2 | 3-5 |
| Playlist additions/day | 20-30 | 50-100 |

#### Channel Requirements

| Status | Requirements |
|--------|--------------|
| Upload videos | Channel verification (phone) |
| Custom thumbnails | Channel verification |
| External links | 1000+ subscribers |
| Community posts | 500+ subscribers |
| Monetization | 1000 subs + 4000 watch hours |

### Warmup Protocol (Engagement Accounts)

```
WEEK 1: Watch Phase
Day 1-7: Watch 30+ min/day, like 20-30, subscribe 10-20

WEEK 2: Engagement Phase
Day 8-14: Comment 10-20 (genuine, detailed), more subs/likes

WEEK 3-4: Active Phase
Day 15-28: Comment 20-30/day, subscribe 30-50/day

For Channel Accounts:
- Post 3-5 videos before any automation
- Complete channel setup fully
- Engage with community
```

### Known Ban Triggers

**TERMINATION RISK:**
- Buying subscribers (low quality providers)
- Automated comment spam
- Copyright strikes (3 = termination)
- Community guideline strikes (3 = termination)
- Sub4sub schemes (detected)

**SHADOWBAN/DEMONETIZATION:**
- Mass subscribing/unsubscribing
- Comment spam patterns
- Click farms / artificial traffic
- Metadata spam (tags, descriptions)

### Recovery Options

**Strike Recovery:**
1. Wait 90 days (strike expires)
2. Appeal if false positive
3. Complete Creator Academy (sometimes removes strike)

**Termination Recovery:**
1. Appeal via YouTube Studio
2. Provide evidence of innocence
3. Wait 7-14 days for review
4. If denied, usually permanent

---

## EMAIL PLATFORMS

### Sending Limits by Provider (January 2026)

| Provider | Technical Daily Limit | Safe Cold Email Limit | Notes |
|----------|----------------------|----------------------|-------|
| Gmail (new) | 500 | 30-40 | 14-day warmup required |
| Gmail (mature) | 2,000 | 50-80 | Continue warmup at 20% |
| Google Workspace | 2,000 | 50-80 | Per user |
| Outlook.com | 300-1,000 | 20-30 | Variable limits |
| Microsoft 365 | 10,000 | 50-100 | Enterprise features |
| Zoho Mail | 500-1,000 | 30-50 | Budget alternative |
| Custom SMTP | Variable | Based on ESP | Check provider limits |

### Warmup Requirements (2026 Standards)

**CRITICAL UPDATE:** 30/day is the new safe limit (down from 50 in 2025). ESPs are more aggressive.

| Phase | Duration | Warmup Volume | Cold Email |
|-------|----------|---------------|------------|
| Initial | Days 1-7 | 10-15/day | 0 |
| Ramp | Days 8-14 | 20-30/day | 5-10 (optional) |
| Build | Days 15-21 | 30-40/day | 15-20 |
| Launch | Days 22-30 | 40-50/day | 25-30 |
| Maintain | Forever | 20-30/day | 30-80 max |

### Authentication Requirements (MANDATORY)

**All three required for deliverability in 2026:**

| Record | Purpose | Status |
|--------|---------|--------|
| SPF | Sender authorization | REQUIRED |
| DKIM | Email signing | REQUIRED |
| DMARC | Policy enforcement | REQUIRED (new 2026) |

**Setup:**
```
SPF: v=spf1 include:_spf.google.com ~all
DKIM: Generate from Google Workspace Admin
DMARC: v=DMARC1; p=none; rua=mailto:dmarc@domain.com
```

### Multi-Inbox Strategy

**For 500+ emails/day:**
```
Goal: 500 cold emails/day
Inboxes needed: 20 (5 domains x 4 inboxes each)
Per inbox: 25 emails/day
Warmup maintained: 10-15 per inbox daily
Rotation: Mandatory (use Instantly/Smartlead)
```

### Known Spam Triggers

**DELIVERABILITY KILLERS:**
- Open tracking pixels (Gmail warning label)
- HTML formatting (use plain text)
- Multiple links per email
- Generic personalization ({{firstName}})
- Inconsistent sending volume
- Single inbox campaigns
- Missing authentication records

**BEST PRACTICES:**
- Plain text only
- 4-6 lines max (50-125 words)
- Subject lines 3-5 words
- Disable open tracking
- Personalize with business context
- Consistent daily volume
- Hybrid warmup (70% auto + 30% manual)

### Tools Status (January 2026)

| Tool | Status | Best For |
|------|--------|----------|
| Instantly | BEST | All-in-one, warmup + sending |
| Smartlead | GREAT | Multi-inbox rotation |
| Lemlist | GOOD | Personalization focus |
| Apollo | GOOD | Data + sending combined |
| Mailforge | GOOD | Pre-warmed inboxes cheap |
| DeliverOn | GOOD | Skip warmup completely |
| Warmbox | GOOD | Dedicated warmup |

---

## PROXY REQUIREMENTS

### Platform-Specific Proxy Recommendations

| Platform | Proxy Type | Provider | Cost |
|----------|------------|----------|------|
| Instagram | Mobile REQUIRED | Soax Mobile, The Social Proxy | $90-150/mo |
| TikTok | Mobile REQUIRED | Real phone recommended | $90-200/mo |
| X/Twitter | Residential OK | Soax, Smartproxy | $6-15/GB |
| LinkedIn | Residential OK | Soax, Bright Data | $6-15/GB |
| YouTube | Residential OK | Any reputable | $6-15/GB |
| Email | Residential/DC | Depends on ESP | $6-15/GB |

### Proxy Provider Quick Reference

| Provider | Type | Price | Best For |
|----------|------|-------|----------|
| Soax | Residential/Mobile | $6.60/GB, $150/mo mobile | Social media |
| Smartproxy | Residential/Mobile | $12.50/GB, $200/mo mobile | Scale |
| Bright Data | All types | $15/GB | Enterprise |
| IPRoyal | Residential | $7/GB | Budget |
| The Social Proxy | Mobile | $90/mo | IG/TikTok specific |
| Proxy-Seller | Mobile | $90/mo | Single account |

### Configuration Rules

1. **One proxy per account** (never share)
2. **Match geography** (US proxy for US account)
3. **Sticky sessions** for social (30+ min)
4. **Mobile for IG/TikTok** (residential gets flagged)
5. **Test before use** (check IP reputation)
6. **Log assignments** (track which proxy = which account)

---

## TOOLS STATUS

### Automation Tools Matrix (January 2026)

| Tool | Platforms | Safety | Cost | Notes |
|------|-----------|--------|------|-------|
| **Hypefury** | X | SAFE | $19-49/mo | Best for X creators |
| **TweetHunter** | X | SAFE | $49/mo | AI + CRM |
| **Buffer** | All | SAFE | $5-15/mo | Scheduling only |
| **Later** | IG, TikTok | SAFE | $15-40/mo | Scheduling only |
| **Kicksta** | IG | SAFE | $49-99/mo | Managed growth |
| **Growthoid** | IG | SAFE | $49-99/mo | Human team |
| **Expandi** | LinkedIn | SAFEST | $99/mo | Cloud automation |
| **Dripify** | LinkedIn | SAFE | $59/mo | Sequences |
| **Instantly** | Email | BEST | $37-97/mo | Warmup + sending |
| **Smartlead** | Email | GREAT | $39-94/mo | Multi-inbox |
| **Jarvee** | Multi | RISKY | $30-70/mo | Desktop, detected often |
| **Phantombuster** | Multi | RISKY | $56/mo | Powerful but risky |

### What Got Patched/Banned (2025-2026)

| Tool/Method | Status | When | Notes |
|-------------|--------|------|-------|
| All Chrome extensions | DEAD | 2024 | Instant detection on all platforms |
| Mass follow apps | DEAD | 2024 | IG/TikTok detect immediately |
| Bot engagement | DEAD | 2025 | AI detection sophisticated |
| LinkedIn desktop automation | DEAD | 2025 | Only cloud works now |
| Single-inbox cold email | DEAD | 2026 | Must rotate 3-5+ inboxes |

---

## BAN RECOVERY PROTOCOLS

### Instagram Recovery

**Action Block:**
1. STOP automation immediately
2. Don't log out
3. Wait 24-72 hours
4. Clear cache
5. Resume at 50% volume
6. Change proxy if persists

**Shadowban:**
1. Stop automation
2. Remove banned hashtags
3. Post quality content 14 days
4. Heavy manual engagement
5. Check: shadowban.app/instagram

**Disabled:**
1. Appeal via app
2. Provide ID
3. Wait 24-48 hours
4. Don't create new account same details

### TikTok Recovery

**Shadowban:**
1. Stop posting 24-48 hours
2. Watch content normally
3. Resume 1 post/day
4. New sounds/hashtags

**Restriction:**
1. Appeal in-app
2. Wait 24-72 hours
3. If denied, wait 30 days
4. Don't create new on same device

### X/Twitter Recovery

**Suspension:**
1. Appeal via support
2. Be honest, no automation mentions
3. Wait 24-72 hours
4. If denied, wait 30 days

**Shadowban:**
1. Check: shadowban.eu
2. Stop automation 48 hours
3. Manual engagement only
4. Avoid sensitive keywords
5. Clears in 7-14 days usually

### LinkedIn Recovery

**Connection Limit:**
1. Stop outreach
2. Wait 7 days
3. Resume at 10/day
4. More personalization

**Restriction:**
1. Appeal via Help
2. Provide ID
3. Wait 2-4 weeks
4. Extreme caution after

### Email Recovery

**Deliverability Issues:**
1. Stop cold sending
2. Increase warmup to 80%
3. Warmup-only 2 weeks
4. Check SPF/DKIM/DMARC
5. Resume at 50% volume

**Blacklist:**
1. Check: mxtoolbox.com/blacklists
2. Request removal from each list
3. Fix underlying issue
4. Wait 7-14 days
5. Monitor closely

---

## UPDATE LOG

| Date | Change | Source |
|------|--------|--------|
| 2026-01-25 | Initial comprehensive guide created | Research compilation |
| 2026-01-25 | Instagram limits now personalized per account trust score | Industry reports |
| 2026-01-25 | TikTok automation NOT recommended - detection too aggressive | BHW, Reddit |
| 2026-01-25 | LinkedIn connection limits reduced to 100/week free | LinkedIn updates |
| 2026-01-25 | Email 30/day new safe limit (down from 50) | Deliverability experts |
| 2026-01-25 | DMARC now required alongside SPF/DKIM | Gmail/Yahoo enforcement |
| 2026-01-25 | Chrome extensions dead on all platforms | Multiple confirmations |
| 2026-01-25 | Mobile proxies REQUIRED for IG/TikTok (residential flagged) | User reports |

---

## RELATED DOCUMENTS

| Document | Purpose |
|----------|---------|
| `OPS/EDGE_GROWTH_TACTICS.md` | Legal grey-hat tactics, services comparison |
| `OPS/ULTIMATE_ACCOUNT_WARMUP_GUIDE.md` | Detailed warmup protocols |
| `OPS/GREY_HAT_SOURCE_FILTERING.md` | Filtering tactics from forums |
| `MONEY_METHODS/COLD_OUTBOUND/EMAIL_SEQUENCES.md` | Email templates |
| `MONEY_METHODS/COLD_OUTBOUND/LINKEDIN_TEMPLATES.md` | LinkedIn templates |
| `AUTOMATIONS/SOAX_MOBILE_PROXIES.md` | Proxy setup guide |

---

*This document requires weekly updates. Last verified: 2026-01-25*
