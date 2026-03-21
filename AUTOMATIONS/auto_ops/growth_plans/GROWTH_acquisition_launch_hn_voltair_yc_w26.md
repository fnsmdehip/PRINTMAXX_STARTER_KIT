# Growth Plan: [ACQUISITION] Launch HN: Voltair (YC W26) – Drone and chargi

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $200-600/mo indirect (tech content audience compound growth + 1-2 EAS/automation clients from YC founder outbound per quarter)

---

## Tactics

1. Post weekly 'YC W26 launches worth watching' roundup — high engagement in indie hacker/tech Twitter communities
2. Cold outreach to YC founders 2-4 weeks post-launch (honeymoon budget window, team still scrappy, need services)
3. Early comment on HN Launch HN threads (first 30 min) for visibility and backlink signal
4. Use Voltair/drone-energy as content hook: 'The $XB infrastructure problem drones are solving' — business-angle content performs well on LinkedIn

## Budget Tier Strategies

### FREE
HN Algolia API (no auth, free) daily scrape → auto-generate content via engagement_bait_converter.py → route to CONTENT/social/posting_queue/ → early HN comment for visibility

### LOW
$0-50/mo: Apollo.io free tier enrichment on YC founder domains → personalized cold email via custom SMTP scripts targeting EAS/automation pitch

### MID
$50-200/mo: LinkedIn Sales Navigator for warm-path intros to YC W26 founders → Instantly sequences for founder outreach at scale

## Daily Actions

- [ ] Create hn_yc_launch_tracker.py: hit HN Algolia API for 'Launch HN' + 'YC' posts created in last 24h
- [ ] Parse JSON response: extract title, url, author, points, created_at, objectID
- [ ] Regex-extract company name and YC batch from title pattern 'Launch HN: COMPANY (YC W26)'
- [ ] Classify sector from title keywords (drone=infra, energy, SaaS, fintech, etc.)
- [ ] Call engagement_bait_converter.py with sector + company context to generate 2-3 content hooks
- [ ] Append content to CONTENT/social/posting_queue/yc_launches_{date}.txt
- [ ] Append company domain to LEDGER/COMPETITIVE_INTEL.csv with sector tag
- [ ] Append founder domain to AUTOMATIONS/leads/yc_batch_leads.csv for chain_cold_outbound pickup
- [ ] Add cron: 0 7 * * * python3 AUTOMATIONS/hn_yc_launch_tracker.py
- [ ] Test run immediately: python3 AUTOMATIONS/hn_yc_launch_tracker.py --test

## Tooling

```json
{
  "browser": "none (HN Algolia API is plain JSON, no browser needed)",
  "email": "custom cold email scripts (existing)",
  "content": "engagement_bait_converter.py"
}
```
