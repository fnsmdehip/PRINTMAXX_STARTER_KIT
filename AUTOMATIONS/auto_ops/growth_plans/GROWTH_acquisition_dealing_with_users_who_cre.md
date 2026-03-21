# Growth Plan: [ACQUISITION] Dealing with users who creates a new account e

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $100-400/mo

---

## Tactics

1. Post 3 indiehacker-voice tweets: 'free trial abusers cost me $X/mo until I blocked disposable emails — here is the 20-line Python check I use'
2. Cross-post detection heuristics as a Reddit thread on r/indiehackers + r/SaaS framed as 'What we learned after 500 fake signups'
3. Package detection script as a free Gumroad lead magnet (Python snippet + guide PDF) — email capture for upsell to $29 advanced version

## Budget Tier Strategies

### FREE
3 posts with specific heuristics (disposable email domain blocklist, IP abuse lookup via free AbuseIPDB tier, device fingerprint guidance) — authority signal for SaaS founders, drives inbound DMs and list signups

### LOW
$0-50/mo: Promote Gumroad lead magnet via targeted Twitter ads to SaaS/indiehacker audience; schedule via Buffer CSV import

### MID
$50-200/mo: Sponsor indiehackers newsletter slot with detection tool as the hook; affiliate angle bundled with email verification services like NeverBounce

## Daily Actions

- [ ] Run engagement_bait_converter.py on this pain point → 3 posts to CONTENT/social/posting_queue/
- [ ] Write free_trial_abuse_detector.py: check email against open disposable-domain lists (github.com/disposable-email-domains), query AbuseIPDB free tier for IP score, output detection_report.json
- [ ] Package as Gumroad lead magnet: PDF guide + Python snippet, free tier captures email, $29 upsell for extended blocklist + Stripe webhook integration
- [ ] Deploy a single surge.sh landing page for the tool with Stripe payment link

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
