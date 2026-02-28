# Meme Page Automation Playbook

**Created:** 2026-02-27
**Status:** READY TO EXECUTE (after account acquisition)
**Companion script:** `AUTOMATIONS/content_repurposer.py`
**Related docs:** `OPS/SAFE_WARMUP_AUTOMATION_GUIDE.md`, `OPS/CURATED_BEAUTY_PAGE_PLAYBOOK.md`

---

## Strategy Overview

Buy pre-warmed Twitter account → repurpose trending meme/entertainment content → monetize via ad revenue sharing + affiliate + driving to products. Zero original content creation needed. Content repurposing with AI-rewritten captions to avoid duplicate detection.

---

## 1. Twitter Shadowban Triggers (Feb 2026)

### Confirmed Triggers
- **Rapid following/unfollowing:** >50 follows/day or follow/unfollow cycling
- **Duplicate content:** Exact same text/media posted across accounts
- **Link spam:** Same link posted repeatedly (especially shortlinks)
- **Engagement pods:** Coordinated like/RT groups detected by ML
- **New account + high volume:** Posting >10/day on account <30 days old
- **Mass DMs:** Automated DM patterns
- **API abuse:** Exceeding rate limits via automation tools
- **Reported content:** Multiple reports in short window
- **Aggressive automation:** Detectable bot patterns (exact intervals, no variation)

### Anti-Shadowban Rules (Baked Into Operations)
1. **Random posting intervals:** Never post at exact intervals. Use 45-180 min gaps with random jitter.
2. **Human-like patterns:** Post more during 9AM-11PM, less at night. Mimic real usage.
3. **Engagement ratio:** Maintain at least 1:3 ratio of own posts to replies/likes on others.
4. **No duplicate text:** Every caption must be unique. Use AI rewriting.
5. **Warmup new accounts:** Follow the schedule in SAFE_WARMUP_AUTOMATION_GUIDE.md strictly.
6. **Max 15-20 posts/day:** Never exceed this even on warmed accounts.
7. **Vary content types:** Mix images, videos, text-only, polls. Don't post only one type.
8. **No automation tells:** Vary caption length, tone, and emoji usage.
9. **Engage authentically:** Reply to comments on your posts within 2-6 hours.
10. **2-day posting break** every 2 weeks. Real accounts don't post 365 days/year.

---

## 2. How Top Meme Pages Operate

### Posting Frequency
- Top pages: 8-15 posts/day
- Sweet spot for growth: 10-12/day
- Don't exceed 20 — diminishing returns + ban risk

### Content Sourcing
- **Reddit:** r/memes, r/funny, r/dankmemes, r/me_irl, r/shitposting (sort by hot/rising)
- **Instagram:** Reels explore page, meme accounts with 100K-1M followers
- **TikTok:** Trending sounds, trending formats, viral clips
- **9GAG/iFunny:** Legacy meme aggregators (less competitive for sourcing)
- **Discord:** Meme servers, niche community servers
- **Twitter itself:** Quote tweet trending topics with meme angle

### Monetization (ordered by ease)
1. **Twitter Ad Revenue Sharing:** Requires X Premium ($8/mo) + 500 followers + 5M impressions in last 3 months. Pays $2-8 per 1M impressions.
2. **Affiliate links in bio:** Promote Amazon products, tech gadgets, etc. Change weekly.
3. **Drive to products:** Link to Gumroad/Etsy products in bio.
4. **Sponsored posts:** At 50K+ followers, brands DM for placement ($50-500/post).
5. **Cross-promote other accounts:** Shoutout swaps with other pages.
6. **Thread bait → newsletter:** "50 crazy facts" threads → newsletter CTA at end.

---

## 3. Pre-Warmed Account Buying

### Marketplace Comparison

| Platform | Price Range | Quality | Risk Level | Notes |
|----------|------------|---------|------------|-------|
| Fameswap | $30-500 | Medium-High | Low | Escrow protection, verified sellers |
| Swapd | $50-1000 | High | Low | Premium marketplace, vetted sellers |
| AccsMarket | $5-100 | Low-Medium | Medium | Cheaper but higher scam risk |
| PlayerUp | $20-300 | Medium | Medium | Gaming-focused but has social |
| Direct (Discord) | $10-200 | Varies | HIGH | No protection, scam heavy |

### What to Look For
- **Age:** 1+ year old (newer = higher ban risk)
- **Followers:** 1K-10K sweet spot (enough social proof, not suspicious if content changes)
- **Niche:** Entertainment/meme/general (easy pivot)
- **Engagement:** Real comments, not just likes
- **No violations:** Check for past strikes/warnings
- **Email access:** Must transfer full email access (not just login)

### Post-Purchase Security (Do IMMEDIATELY)
1. Change email to your catch-all domain
2. Change password (generate with password manager)
3. Enable 2FA (use auth app, not SMS)
4. Change phone number to your burner
5. Update bio with your content direction
6. Do NOT post for 48 hours (let login from new IP settle)
7. Start warmup protocol from SAFE_WARMUP_AUTOMATION_GUIDE.md

---

## 4. Multi-Account Management (Safe in 2026)

### Anti-Detect Browsers
- **AdsPower (FREE):** 5 free profiles. Use this. Already in our stack.
- **GoLogin ($24/mo):** Backup if need more profiles.
- **Multilogin ($29/mo):** Enterprise-grade, overkill for us currently.

### Key Rules for Multi-Account
- Each account gets its own browser profile (fingerprint, cookies, storage)
- Each account uses its own proxy IP (residential, not datacenter)
- Never log into 2+ accounts from the same browser/IP
- Different posting schedules per account (don't sync)
- Different content themes per account

### Scheduling Tools
- **Fedica ($10/mo):** Multi-account scheduling, our current stack choice
- **Tweetlio (FREE):** Unlimited X posts, great for single-account heavy posting
- **Buffer (if accessible):** Backup option

---

## 5. Content Repurposing Best Practices

### Making Content "Unique Enough"
1. **Rewrite caption entirely** — not paraphrasing, full rewrite with AI
2. **Crop/resize images** — change dimensions, add slight zoom
3. **Add watermark** — subtle page branding
4. **Change image format** — JPEG to PNG, different compression
5. **Metadata strip** — remove EXIF data (content_repurposer.py does this)
6. **Add/remove border** — slight visual modification
7. **Flip horizontally** — for images where it doesn't look weird
8. **Re-encode video** — different bitrate/codec via ffmpeg

### What NOT to Do
- Don't just save and repost (exact duplicate detection catches this)
- Don't only change 1-2 words in caption
- Don't repost within 24 hours of original
- Don't repost from accounts with >1M followers (too visible)

---

## 6. First 30-Day Playbook

### Week 1 (Days 1-7): Setup + Warmup
- Day 1: Buy pre-warmed account, secure it, set up anti-detect profile
- Day 2-3: Wait period (no posting, let new IP settle)
- Day 4-7: Warmup posting (3-5 posts/day, engaging with others)
- During week: Set up content_repurposer.py with source accounts

### Week 2 (Days 8-14): Ramp Up
- Increase to 8-10 posts/day
- Start using content_repurposer.py for AI-rewritten captions
- Engage in replies: 15-20/day on trending topics
- Join relevant engagement communities (genuinely)
- Enable X Premium ($8/mo) for ad revenue eligibility

### Week 3 (Days 15-21): Full Speed
- 12-15 posts/day
- Analyze first 2 weeks: which content types get most engagement?
- Double down on winners (content_repurposer.py --winners flag)
- Start adding affiliate link in bio
- Track follower growth rate

### Week 4 (Days 22-30): Optimize
- Review analytics: engagement rate, impression growth, follower growth
- Cut content types that underperform
- A/B test posting times
- If growing >100 followers/day → on track for monetization
- If flat → adjust content strategy (different sources, different niche angle)

### Milestones
| Day | Target | Action if Met |
|-----|--------|---------------|
| 7 | Account stable, no warnings | Start ramping content |
| 14 | 100+ new followers | Keep going |
| 21 | 500+ new followers | Optimize for winners |
| 30 | 1K+ new followers | Start monetization prep |
| 60 | 5K+ followers | Apply for ad revenue sharing |
| 90 | 10K+ followers | $50-200/mo from ads + affiliate |

---

## 7. Content Sourcing Strategy

### Source Accounts to Monitor
Set these as sources in `content_repurposer.py`:

**Meme/Entertainment:**
- @memezar, @laborwave, @reactjpg, @dloading
- r/memes (top/hour), r/me_irl (top/day)

**Engagement Bait Formats:**
- "Pick a number" polls
- "Caption this" images
- "Wrong answers only"
- Hot takes / unpopular opinions
- "Rate this X out of 10"

**Trending Format Detection:**
- Monitor Twitter trending topics every 2h
- Check which formats are getting 10K+ engagement
- Adapt trending format to your niche angle within 4 hours

---

## 8. Automation Script

**`AUTOMATIONS/content_repurposer.py`** handles:
- Scraping source accounts for trending content
- AI-rewriting captions via Claude API
- Scheduling with natural timing
- Duplicate tracking
- Winner detection
- Anti-shadowban safeguards

```bash
# Daily operations
python3 AUTOMATIONS/content_repurposer.py --sources --dry-run    # Preview what to repurpose
python3 AUTOMATIONS/content_repurposer.py --rewrite               # Rewrite captions
python3 AUTOMATIONS/content_repurposer.py --schedule              # Schedule posts
python3 AUTOMATIONS/content_repurposer.py --winners               # Show top performers

# Management
python3 AUTOMATIONS/content_repurposer.py --dry-run               # Preview all actions
```

---

## Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Shadowban | Medium | High | Anti-shadowban rules (Section 1) |
| Account suspension | Low | Very High | Warmup protocol + safe behavior |
| DMCA takedown | Low | Medium | Rewrite + modify, don't exact copy |
| Purchased account scam | Low | Medium | Use Fameswap/Swapd with escrow |
| Content quality drop | Medium | Medium | Winner detection + manual QA |
| Platform TOS change | Low | High | Diversify to TikTok, Instagram |
