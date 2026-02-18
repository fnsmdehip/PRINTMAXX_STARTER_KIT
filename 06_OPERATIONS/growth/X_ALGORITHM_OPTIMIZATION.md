# X Algorithm Optimization Guide

**Source:** [github.com/xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) (12.8k stars)
**Released:** Jan 19, 2026
**Updated:** 2026-01-23

---

## How The Algorithm Works

The X "For You" feed uses a **Grok-based transformer model** that predicts engagement probabilities for each post.

### Scoring Formula
```
Final Score = Σ (weight × P(action))

Where actions include:
- P(like)
- P(reply)
- P(repost)
- P(click)
- P(dwell time) - how long users spend on post
- P(profile click) - users clicking to profile
- P(video watch) - for video content
```

### Key Components

1. **Thunder** - In-network content (from accounts you follow)
2. **Phoenix** - Out-of-network content (ML-discovered)
3. **Home Mixer** - Combines both into final feed

---

## What Gets FILTERED OUT (Avoid These)

**Pre-Scoring Filters remove posts that are:**
- Duplicates
- Too old (recency matters)
- From the viewer themselves (self-posts don't show in For You)
- From blocked/muted accounts
- Containing muted keywords
- Previously seen or recently served
- Ineligible subscription content

**Post-Selection Filters (VFFilter):**
- Deleted content
- Spam
- Violence/gore
- Policy violations

---

## What Gets BOOSTED (Optimize For These)

### Engagement Signals (Ranked by Weight)

Based on algorithm analysis, **replies and quotes are weighted higher than likes** because they indicate deeper engagement.

| Signal | Weight | Why |
|--------|--------|-----|
| Replies | HIGHEST | Shows conversation, deeper engagement |
| Quote tweets | HIGH | Shows thoughtful engagement |
| Reposts | HIGH | Distribution signal |
| Likes | MEDIUM | Low-effort engagement |
| Dwell time | HIGH | Shows content is compelling |
| Profile clicks | HIGH | Interest in author |
| Video watch time | HIGH | For video content |

### Author Factors

- **Verification status** matters (hydrated into scoring)
- **Author diversity** - algorithm attenuates repeated author scores
  - **Don't spam posts** - spacing matters
  - Posting too frequently hurts individual post scores

### Content Factors

- **Recency** - newer posts preferred
- **Media type** - videos get special handling
- **Text, media, etc.** enriched during hydration

---

## Tactical Recommendations

### 1. Optimize for Replies > Likes

The algorithm weights replies and quotes higher than likes because they indicate deeper engagement.

**Tactics:**
- Ask questions at end of posts
- Use controversial/contrarian takes that invite discussion
- Reply bait: "Comment X if you agree"
- A/B posts: Post opposite takes, see which gets more replies

### 2. Maximize Dwell Time

Users spending time on your post = signal of quality.

**Tactics:**
- Longer-form content (threads, images that require reading)
- Hooks that make people stop scrolling
- Content that requires thought/processing

### 3. Verification Matters

Author verification status is hydrated into scoring.

**Tactic:** Get Twitter Blue/Premium for algorithmic boost.

### 4. Don't Spam - Space Your Posts

Author Diversity Scorer attenuates repeated author scores.

**Tactics:**
- Space posts 2-4 hours apart minimum
- Quality > quantity
- Each additional post from same author gets decaying multiplier

### 5. Recency Counts

Old posts get filtered. Post timing matters.

**Tactics:**
- Post when your audience is online
- Reshare/quote your best content after time has passed
- Delete underperforming posts (they won't recover)

### 6. Avoid Muted Keywords

Posts with muted keywords get filtered for users who muted them.

**Tactics:**
- Avoid controversial political keywords unless that's your niche
- Be aware of commonly muted terms in your space
- Test different phrasings

### 7. Drive Profile Clicks

Profile clicks = strong interest signal.

**Tactics:**
- Tease more content in bio
- End posts with "Follow for more X"
- Make your profile compelling (link in bio, good header)

---

## The CJ Zafir Method

@cjzafir built an "X Verifier Suite" using:
1. Downloaded his 6.7GB X data export
2. Attached the X algorithm GitHub repo
3. Attached his tweets.js (post history)
4. Asked Claude Code to analyze and create verification skills
5. Ran ralph-loop for 6 hours ($6.78)

**Results:**
- Deep insights on writing style (what worked, what didn't)
- Topics analysis (what to talk about, what to avoid)
- Viral post ingredients for his specific account

### How to Replicate

1. **Download your X data:**
   - Settings → Your Account → Download Archive
   - Takes 24-48 hours to prepare
   - Contains tweets.js with all your posts

2. **Clone the algorithm repo:**
   ```bash
   git clone https://github.com/xai-org/x-algorithm
   ```

3. **Create Claude Code skill:**
   - Analyze your post history against algorithm
   - Identify your best-performing content patterns
   - Generate posting recommendations

4. **Build verification workflow:**
   - Before posting, run draft through verifier
   - Check: reply potential, dwell time potential, keyword issues
   - Optimize before posting

---

## Quick Reference: Post Checklist

Before posting, verify:

- [ ] Does it invite replies? (Question, controversy, debate)
- [ ] Will people dwell on it? (Interesting, requires thought)
- [ ] No muted keywords? (Check common mutes in niche)
- [ ] Not too soon after last post? (2-4 hour spacing)
- [ ] Has media? (Images/video get special handling)
- [ ] Drives profile interest? (Teases more content)
- [ ] Verified account? (Premium boost)

---

## Resources

- [X Algorithm GitHub](https://github.com/xai-org/x-algorithm)
- [@cjzafir's Verifier Suite Tweet](https://x.com/cjzafir/status/2014365898061299923)
- [@weswinder's Strategy Analysis](https://x.com/weswinder/status/2013492281433542918)

---

## Next Steps for PRINTMAXX Accounts

1. **Download X data** for each niche account (when created)
2. **Build account-specific verifier** using CJ method
3. **Create pre-post checking skill** in Claude Code
4. **Track engagement patterns** to validate algorithm insights
5. **Iterate on tactics** based on actual performance
