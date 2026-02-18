---
name: warmup-sop
description: Generate platform-specific warmup Standard Operating Procedures.
model: sonnet
---

# Warmup SOP Generator

Generate detailed warmup SOPs for social accounts.

## Platforms Supported

- X (Twitter)
- TikTok
- Instagram
- YouTube

## SOP Contents

Each SOP includes:

### Day 1-3: Passive Phase
- Follow count targets
- Like count targets
- Profile optimization checklist
- Bio templates

### Day 4-7: Engagement Phase
- Reply count targets
- Comment templates (non-spammy)
- Story/status viewing
- Community engagement

### Day 8-14: Content Phase
- First post timing
- Content mix ratios
- Hashtag strategies
- Posting schedule

### Red Lines (Never Do)
- Actions that trigger flags
- Volume limits per day
- Automation detection signals

## Arguments

- `--platform [x|tiktok|instagram|youtube|all]`
- `--niche [ai|faith|fitness]`

Output: OPS/sops/warmup_[platform]_[niche].md

Example: `/warmup-sop --platform x --niche ai`
