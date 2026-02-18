# STREAMER_CLIPS

Clip trending streamers, repurpose on viral pages.

---

## Overview

Find top trending streamers. Pull their YouTube VOD uploads. Use AI to analyze transcripts and identify clippable moments. Auto-generate clips with captions. Post across accounts. Get paid by creator fund, sponsorships, and directly by streamers.

---

## Revenue Streams

| Stream | How It Works | Potential |
|--------|--------------|-----------|
| Creator Fund | TikTok, YouTube Shorts payouts | $500-5k/mo at scale |
| Streamer Payments | Get paid to promote their content | $100-500/clip deal |
| Sponsorships | Gaming gear, energy drinks, apps | $200-2k/post |
| Affiliate | Streaming gear, games | 5-15% commission |

---

## Automation Pipeline

```
1. IDENTIFY: Find top trending streamers (Twitch tracker, YouTube gaming)
2. SOURCE: Pull YouTube re-uploads of streams (already uploaded by others)
3. TRANSCRIBE: Extract transcript via YouTube API or Whisper
4. ANALYZE: AI identifies clippable moments:
   - High chat activity moments
   - Emotional peaks (laugh, rage, shock)
   - Skill plays
   - Drama/controversy
   - Quotable lines
5. CLIP: Extract 30-60 second segments
6. EDIT: Add captions, format for platform (9:16 for TikTok/Reels/Shorts)
7. QUEUE: Schedule across accounts
8. TRACK: Monitor performance, iterate on clip selection criteria
```

---

## Account Strategy

### Per Streamer Accounts
- @[StreamerName]Clips
- @[StreamerName]Moments
- Focus on one streamer per account for targeted audience

### Genre Accounts
- @BestTwitchClips
- @GamingMoments
- @StreamerRage
- Aggregates across multiple streamers

### Platform Spread
- TikTok (highest creator fund potential)
- YouTube Shorts (longest tail)
- Instagram Reels (brand-safe sponsors)

---

## Clip Selection Criteria

### High-Performing Clip Types

| Type | Why It Works | Example |
|------|--------------|---------|
| Rage/Fail | Schadenfreude | Streamer dies and loses it |
| Skill Play | Aspiration | Insane clutch moment |
| Funny Moment | Entertainment | Unexpected joke lands |
| Drama | Tea culture | Beef with another streamer |
| Wholesome | Feel-good | Fan interaction, donation reaction |

### Technical Criteria
- Clear audio (no music copyright issues)
- Good visual quality
- Self-contained (no context needed)
- Under 60 seconds (platform preference)

---

## Tools

### Finding Streamers
- TwitchTracker (top channels)
- SullyGnome (analytics)
- YouTube Trending Gaming

### Transcript Analysis
- YouTube transcript API
- Whisper (local transcription)
- Claude/GPT for moment identification

### Clipping
- FFmpeg (command line)
- CapCut (manual if needed)
- Custom Python script (automation/)

### Posting
- Buffer/Hypefury (scheduling)
- Playwright scripts (automation)

---

## Streamer Outreach

Some streamers will pay for clips. Others will send cease and desist.

### Good Targets
- Growing streamers (1k-50k followers) who want exposure
- Streamers without clip channels
- Streamers who engage with fan content

### Pitch Template

```
Hey [Name],

I run @[AccountName] - we clip and share the best moments from streamers we love.

Your [specific clip] got [X views] on our channel. Figured you'd want to know your content is resonating.

If you're interested, we'd love to do more clips or even work together on a promotion deal.

Let me know!
```

### Red Flags (Avoid)
- Streamers with existing clip channels they control
- Streamers who have DMCA'd clip channels before
- Major streamers with aggressive management

---

## Monetization Setup

### Creator Fund
1. TikTok: 10k followers + 100k views to qualify
2. YouTube: 1k subs + 10M Shorts views (90 days)
3. Focus on volume to hit thresholds fast

### Sponsorships
- Once at 50k+ followers, DM gaming brands
- Common sponsors: GFuel, gaming chairs, VPNs, mobile games
- Rate: $10-50 per 1k followers

### Affiliate
- Amazon Associates (streaming gear)
- Game keys (G2A, CDKeys)
- Streaming software (Streamlabs)

---

## Ralph Tasks

### Daily
- Scan for new viral streamer moments
- Process clips through pipeline
- Queue posts

### Weekly
- Analyze top performing clips
- Adjust selection criteria
- Outreach to new streamers

---

## Compliance Notes

- Don't claim you created the content
- Credit streamers in captions
- Remove if DMCA'd (don't fight)
- Keep originals archived (proof of fair use)

---

## Getting Started

1. Pick 5 streamers to focus on
2. Set up 1 account per platform
3. Run transcript analysis on recent VODs
4. Create 10 clips to test
5. Post and measure
6. Scale what works

---

## Related Docs

- `research/TOP_STREAMERS.csv` - Target streamers list
- `research/CLIP_CRITERIA.md` - Detailed selection guidelines
- `automation/transcript_analyzer.py` - AI analysis script
- `outreach/STREAMER_PITCH_TEMPLATES.md` - Outreach templates

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| `STREAMER_CLIPS_DEEP_DIVE.md` | Comprehensive research on all business models, revenue data, platforms, legal considerations |
| `CLIPPING_BUSINESS_PLAYBOOK.md` | Step-by-step playbook from clipper to network operator |
| `CLIPPER_INFO_PRODUCT_SPEC.md` | Full info product ladder specification ($67 to $1,997) |
| `NETWORK_OPERATOR_RESEARCH.md` | 500 clipper model case study and network economics |

---

## Quick Start

1. Read `STREAMER_CLIPS_DEEP_DIVE.md` for full business model overview
2. Pick your starting point (clipper, channel owner, or network)
3. Follow `CLIPPING_BUSINESS_PLAYBOOK.md` for execution steps
4. Scale to info products using `CLIPPER_INFO_PRODUCT_SPEC.md`

---

Last updated: 2026-01-25
