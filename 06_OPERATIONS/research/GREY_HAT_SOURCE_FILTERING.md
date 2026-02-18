# Grey Hat Source Filtering Guide

**Purpose:** How to extract legal, actionable tactics from mixed-quality sources like BHW and Twitter communities.

---

## The Filter: What to Keep vs Skip

### KEEP (Legal Grey Hat)
- Email warmup protocols
- Account warming patterns (manual behavior)
- Deliverability optimization
- Platform algorithm changes
- "This stopped working" warnings
- Proxy/IP rotation best practices
- DNS configuration tips
- Automation timing patterns
- What got accounts banned (learn to avoid)

### SKIP (Illegal or Scammy)
- Fake engagement services
- Bot networks for followers/likes
- Account selling/buying at scale
- Credential stuffing
- Phishing templates
- Fake review services
- Click fraud schemes
- Anything with "undetectable" in the pitch
- Mass account creation tools
- Verification bypass exploits

---

## Source-Specific Filters

### BlackHatWorld

**Best Sections:**
- Email Marketing (warmup, deliverability)
- Social Media (platform changes, ban patterns)
- SEO (programmatic SEO, not link schemes)

**Red Flags to Skip:**
- Posts selling "aged accounts"
- "Guaranteed followers/views"
- Anything promising "undetectable"
- Posts from users with <100 posts and no reputation
- "DM me for method" with no preview

**Green Flags to Keep:**
- Posts with specific numbers and dates
- Screenshots of results
- Users with iTrader scores >5
- "Warning: this got patched" posts
- Technical deep-dives on platform APIs
- Discussions about policy changes

**How to Scan:**
1. Sort by "Last 7 days" or "This month"
2. Look for threads with 20+ replies (community validated)
3. Check if OP has updated with results
4. Skip anything selling something
5. Extract: What stopped working? What's new? What's risky?

**CRITICAL: Analyze Replies/Comments**
- Often the REAL alpha is in the replies, not the OP
- Look for: "I tried this and..." / "Update: this got patched" / "Actually what works is..."
- Users with high post counts correcting OP = high signal
- Check for disagreements - the nuance is in the debate
- OP edits/updates often contain refined tactics

---

### Twitter Communities

**Best Communities:**
- Cold Email / Outbound focused
- Indie Hackers / Solopreneurs
- Automation / AI tools

**Red Flags:**
- Promo-heavy accounts (check ratio of value to pitch)
- "DM me for secret" without preview
- Vague claims without numbers
- Accounts <3 months old pushing tactics

**Green Flags:**
- Accounts with real product/business
- Specific numbers in posts
- Screenshots of dashboards/results
- "Here's what went wrong" posts
- Active in replies (not just posting)

---

## Extraction Template

When finding a potential tactic, log to ALPHA_STAGING.csv with:

```
alpha_id: ALPHA[NNN]
source: BHW/[section] OR X Community/[name]
source_url: Direct link
category: WARMUP | DELIVERABILITY | PLATFORM_CHANGE | BAN_WARNING | AUTOMATION
tactic: One-line summary
status: PENDING_REVIEW
is_grey_hat: TRUE
legal_status: LEGAL | GREY_LEGAL | AVOID
evidence: What proof exists (screenshots, metrics, community validation)
date_found: YYYY-MM-DD
```

---

## Weekly Scan Routine

**Time:** 30 min/week

**BHW Scan (15 min):**
1. Email Marketing → Sort by "Last 7 days" → Scan top 10 threads
2. Social Media → Sort by "Last 7 days" → Scan top 10 threads
3. Look for: Platform changes, ban warnings, new warmup methods
4. Log anything useful to ALPHA_STAGING.csv

**Twitter Community Scan (15 min):**
1. Check 2-3 communities
2. Look for: Tool recommendations, what stopped working, new tactics
3. Cross-reference with known high-signal accounts
4. Log to ALPHA_STAGING.csv

---

## Current Working Tactics (Update Monthly)

### Email Warmup (Jan 2026)
- Auto-warmup networks still work (Instantly, Smartlead)
- Manual warmup + auto hybrid = best results
- DKIM/DMARC enforcement stricter than ever
- Google Postmaster Tools essential for monitoring

### Social Account Warming (Jan 2026)
- 7-14 day manual activity before any automation
- Same IP/device fingerprint consistency critical
- TikTok strictest (no VPN, location services required)
- Instagram requires feature usage variety (Stories, Reels, Posts)
- X/Twitter most lenient but watching for bot patterns

### What Recently Stopped Working
- (Add entries as discovered from BHW/Twitter scans)

### What Recently Started Working
- (Add entries as discovered)

---

## FTC/Legal Guardrails

Even "grey hat" must stay legal:

✅ **Legal Grey Hat:**
- Warming up accounts with real activity patterns
- Using proxies for geographic consistency
- A/B testing messaging at scale
- Automation that mimics human behavior
- Scraping public data

❌ **Illegal (Never Do):**
- Fake testimonials
- Misleading affiliate disclosures
- Spam (CAN-SPAM violations)
- Platform TOS violations that could result in legal action
- Impersonation
- Purchased engagement (violates FTC if used for marketing claims)

---

## Integration with Daily Research

When running `/daily-research`:
1. Include BHW and Twitter communities in source rotation
2. Apply filters above
3. Mark grey hat entries with `is_grey_hat: TRUE`
4. Human reviews grey hat entries with extra scrutiny in `/review-alpha`

---

*Last Updated: 2026-01-24*
