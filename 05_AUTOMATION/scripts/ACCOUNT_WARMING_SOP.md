# Account Warming SOP

Strategy for warming social accounts before automation.

---

## The Core Problem

New accounts + automation = instant ban. Platforms detect:
1. New account behavior patterns
2. API calls without human behavior
3. Inconsistent IP addresses
4. Inhuman posting speed/timing

---

## Warming Strategy: 3-Tier Approach

### Tier 1: Manual Warm (New Accounts) - Weeks 1-2

**Daily actions (do yourself, no automation):**

| Day | Actions |
|-----|---------|
| 1-3 | Create account, complete profile, follow 5-10 accounts, scroll 10min |
| 4-7 | Like 20-30 posts, reply to 3-5 posts, follow 10-20 accounts |
| 8-14 | First posts (2-3/day), engage more actively, DM 1-2 people |

**Rules:**
- Same IP address (home wifi or dedicated proxy)
- Same device
- Human timing (gaps between actions)
- Engage before posting
- No links in first 10 posts

**X (Twitter) Specific:**
- Don't use API for 14 days minimum
- First tweets: Text only, no links
- Quote tweet and reply before original posts
- Join 2-3 relevant Spaces (just listen)

**TikTok Specific:**
- Watch videos before posting (algorithm training)
- Complete all profile fields
- First posts: Duets or stitches (engagement signals)
- No links in bio for first week

**Instagram Specific:**
- Follow/unfollow slowly (50 max/day even when warm)
- Stories before feed posts
- Use all features: Stories, Reels, Posts
- Respond to every comment/DM

---

### Tier 2: Buy Warmed Accounts - Faster Path

**Where to buy:**

1. **AccsMarket** - Best reputation
   - Aged X accounts: $15-50
   - Aged IG accounts: $20-80
   - Aged TikTok: $10-40
   - Check reviews before buying
   - accsmarket.com

2. **Fameswap** - Instagram focus
   - Higher quality, verified accounts
   - More expensive ($100+)
   - fameswap.com

3. **SocialTradia** - Multi-platform
   - X, IG, TikTok, YouTube
   - Escrow included
   - socialtradia.com

4. **Z2U / PlayerAuctions** - Gaming focus but has social
   - Variable quality
   - Use escrow
   - z2u.com

5. **Telegram groups** - Risky but cheap
   - High scam rate
   - Always escrow
   - Never pay crypto first
   - Search: "aged accounts" in Telegram

6. **Private sellers** (Reddit, forums)
   - r/redditbay (check carefully)
   - BlackHatWorld forum
   - Ask for account age proof
   - Check follower quality
   - Verify with video call if high value

7. **Bulk providers** (for scale)
   - bulkaccountsbuy.com
   - pvafarm.com (phone verified accounts)
   - Lower quality but cheap for testing

**What to look for:**
- Account age: 6+ months minimum
- Post history: Should have some activity
- Follower/following ratio: Should look natural
- No previous violations: Check account status
- Original email access: Critical for recovery

**After buying:**
1. Change password immediately
2. Add your 2FA
3. Change email gradually (some platforms flag this)
4. Continue manual activity for 3-5 days
5. Then slowly introduce automation

**Red flags:**
- Seller wants crypto only
- No escrow available
- Account age doesn't match claim
- Suspicious follower patterns (bot followers)
- Recent password changes in account

---

### Tier 3: Residential Proxies - For Automation

**Decodo (formerly Smartproxy) Setup:**

```
1. Sign up: smartproxy.com
2. Get residential rotating proxies
3. Pricing: $12.50/GB minimum
4. Best for: Social media automation
```

**Configuration:**
```
Proxy format: username:password@gate.smartproxy.com:port
Rotation: Sticky sessions (same IP for 10-30 min)
Location: Match account's "home" location
```

**Soax Alternative:**
```
1. Sign up: soax.com
2. Minimum: $6.60/GB
3. Cleaner IP pool
4. Good dashboard
```

**Which to use when:**

| Scenario | Proxy Type |
|----------|-----------|
| New account warming | Dedicated residential |
| Posting automation | Rotating residential (sticky 30min) |
| Scraping/research | Datacenter (cheaper) |
| High-value accounts | Mobile proxy |

**IP Consistency Rules:**
- One proxy per account
- Same geographic region as account "home"
- Don't mix datacenter and residential
- Log proxy assignments

---

## Platform-Specific Warming

### X (Twitter)

**Week 1-2 (Manual Only):**
```
Day 1-3: Profile setup, follow 20 accounts in niche
Day 4-7: Like 50/day, reply to 10 tweets, retweet 5
Day 8-14: First tweets (3/day), continue engagement
```

**Week 3-4 (Light Automation):**
```
- Schedule posts via Hypefury (official API)
- Continue manual engagement
- Max 10 tweets/day
- Human-like timing (not on the hour)
```

**Week 5+ (Full Automation):**
```
- Can use Playwright for posting
- Keep engagement manual or light
- Monitor for shadowban (check via shadowban checker)
```

**Shadowban Recovery:**
- Stop all automation
- Manual engagement only for 7 days
- Don't delete flagged tweets (makes it worse)
- Appeal if obvious false positive

---

### TikTok

**Week 1-2 (Manual Only):**
```
Day 1-3: Watch 30min of content, complete profile
Day 4-7: Like 100/day, follow 20-30 accounts, first 3 videos
Day 8-14: Post daily, respond to all comments
```

**TikTok Anti-Detection:**
- Always use official app (not web) for critical actions
- Same device fingerprint
- Location services on
- Don't use VPN (they detect this hard)

**Week 3+ (Semi-Automation):**
```
- Schedule via Later or Buffer (official API)
- Batch record, post throughout day
- Caption variations (don't copy/paste same text)
```

---

### LinkedIn

**Week 1-2:**
```
- Complete all profile sections (100% completion)
- Connect with 20-30 real people
- Engage on 10 posts/day
- First post: Text only, personal story
```

**LinkedIn is Strict:**
- Max 100 connection requests/week
- Don't use Chrome extensions (detection)
- Sales Navigator if doing outbound
- Never automate connection requests

---

## A/B Testing Strategy (Manual First)

You mentioned A/B testing. Here's the approach:

**Phase 1: Manual Accounts (First 30 Days)**
- Use your personal accounts or fresh manual-warmed accounts
- Test content formats, hooks, posting times
- Document what works
- Build baseline metrics

**Phase 2: Warmed Accounts (Day 30+)**
- Buy 2-3 aged accounts
- Apply winning formulas from Phase 1
- Test at higher volume
- Compare performance to manual accounts

**Phase 3: Scaled Automation (Day 60+)**
- Automate posting on proven content
- Keep 1-2 "manual" accounts for testing new ideas
- Monitor all accounts for platform action

---

## Proxy Comparison: Decodo vs Soax

| Feature | Decodo (Smartproxy) | Soax |
|---------|---------------------|------|
| Min price | $12.50/GB | $6.60/GB |
| Pool size | 40M+ IPs | 8M+ IPs |
| Sticky sessions | Yes (up to 30min) | Yes (up to 30min) |
| Mobile proxies | Yes ($$$) | Yes ($$) |
| Dashboard | Good | Better |
| Support | Good | Good |
| Best for | Social media | Scraping |

**Recommendation:** Start with Decodo for social automation. Cheaper per GB for the quality level needed.

---

## Budget Scenarios

### Minimal ($50/mo):
- 3 manual accounts (free)
- Decodo 1GB ($12.50)
- Buffer free tier
- Time: 1hr/day manual engagement

### Standard ($150/mo):
- 3 manual + 3 bought aged accounts (~$100 one-time)
- Decodo 5GB ($50)
- Hypefury ($29)
- Make.com free tier
- Time: 30min/day manual

### Scale ($400/mo):
- 10+ accounts mix
- Decodo 20GB ($150)
- Mobile proxies for main accounts ($100)
- Full automation suite
- Time: 15min/day monitoring

---

## Warning Signs (Stop Automation If You See)

- Account flagged for suspicious activity
- Sudden follower drop
- Posts not showing in hashtags
- Engagement rate drops 50%+
- Login challenges appearing
- Action blocks (IG "try again later")

**Recovery Protocol:**
1. Stop all automation immediately
2. Switch to manual only
3. Wait 48-72 hours
4. Slowly resume if no further issues
5. Check IP reputation (may need new proxy)

---

## Daily Checklist

Morning:
- [ ] Check all accounts for flags/blocks
- [ ] Review overnight engagement
- [ ] Respond to any DMs/comments

Afternoon:
- [ ] Post scheduled content (automated)
- [ ] 15min manual engagement per platform
- [ ] Check analytics

Evening:
- [ ] Plan tomorrow's content
- [ ] Engage with trending topics
- [ ] Update tracking sheet

---

## Related Documents

- `AUTOMATIONS/SOAX_MOBILE_PROXIES.md` - Mobile proxies for IG/TikTok (recommended for main accounts)
- `AUTOMATIONS/PROXY_COMPARISON.md` - Full proxy provider comparison
- `AUTOMATIONS/SOCIAL_AUTOMATION_STRATEGY.md` - Playwright scripts and automation
- `MONEY_METHODS/AI_INFLUENCER/` - AI persona playbooks
- `MONEY_METHODS/CONTENT_FARM/` - Content scaling strategies

---

Last updated: 2026-01-21
