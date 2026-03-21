# Meta Ads Autonomous System

Zero cost autonomous Meta (Facebook/Instagram) ad management via OpenClaw + social-cli.

## Stack

- **OpenClaw** (free tier): AI agent platform, runs the 5 skills below
- **social-cli** (@vishalojha_me): Wraps Meta Marketing API. Handles token refresh, pagination, rate limits.
- **Meta Marketing API**: Read/write access to ad account

## 5 OpenClaw Skills

### 1. meta-ads (Daily Health Check + Auto-Pause)
- Runs daily: "Am I on track? What's running? Who's winning? Who's bleeding? Any fatigue?"
- Same 5 questions you'd ask Ads Manager every morning
- Auto-pauses any campaign with CPA > 2.5x target for 48+ hours

### 2. ad-creative-monitor (Fatigue Detection)
- Pulls daily frequency by ad
- Frequency > 3.5 = audience is cooked, CTR about to drop
- This single signal saves more than any dashboard

### 3. budget-optimizer (Efficiency Scoring + Shift Recs)
- Ranks every campaign by efficiency (ROAS, CPA, CTR composite)
- Recommends shifting spend from bottom performers to top
- Example: paused an $87 CPA campaign at 3am, scaled best performer 30%

### 4. ad-copy-generator (Variations from Winners)
- Analyzes what's working: hooks, angles, CTAs
- Generates variations modeled on patterns in YOUR top performers
- Copy based on what already converts in your account, not generic templates

### 5. ad-upload (Publishes Creative Directly)
- New creative + copy uploaded live to Meta Ads Manager
- No downloading, formatting, clicking through upload flow
- Agent handles the entire publish cycle

## Flow

```
Daily cron
  -> meta-ads skill: health check, pull metrics
  -> ad-creative-monitor: flag frequency > 3.5
  -> budget-optimizer: rank campaigns, auto-pause bleeders (CPA > 2.5x for 48hrs)
  -> budget-optimizer: shift budget to winners
  -> ad-copy-generator: write variations from winning patterns
  -> ad-upload: publish new creative directly to account
  -> morning brief: deliver summary to Telegram/Slack
```

Input: your ad account + your target CPA
Output: an AI that monitors, kills, scales, writes, AND uploads your ads

## Cost

$0/mo. OpenClaw free tier. social-cli is open source.

## Setup

1. Create Meta Business account, get Marketing API access token
2. Install social-cli: `npm install -g social-cli`
3. Configure OpenClaw with the 5 skills (meta-ads, ad-creative-monitor, budget-optimizer, ad-copy-generator, ad-upload)
4. Set target CPA per campaign
5. Set notification channel (Telegram, Slack, etc.)
6. Run daily via cron or OpenClaw scheduler

## PRINTMAXX Integration

Use this for ALL ventures that run paid Meta traffic:
- Before You (ancestry product)
- App Factory apps (FocusLock, PrayerLock, ColdMaxx)
- Digital products (Claude Code guides, playbooks)
- Content farm accounts driving to affiliate

Cross-pollination: ad-copy-generator learns from ALL ventures simultaneously. A winning hook in one vertical can inspire variations in another.

## Kill / Scale Triggers

- Kill: ROAS < 1.0 after 7 days with $50+ spend
- Scale: ROAS > 3.0 sustained 7+ days -> increase daily budget 30%
- Pause: Any single ad with frequency > 4.0
- Alert: Any campaign spending > 2x daily budget
