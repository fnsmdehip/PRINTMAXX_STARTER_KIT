# Complete cold email deliverability checklist

Everything from domain purchase to first send. Skip nothing. One wrong step and you land in spam forever.

---

## Phase 1: Domain purchase and setup

### Where to buy domains

| Registrar | Why | Price |
|-----------|-----|-------|
| Porkbun | Cheapest, clean UI | $8-12/yr |
| Namecheap | Good for bulk | $9-13/yr |
| Cloudflare | Free DNS, fast propagation | $8-10/yr |
| Google Domains (now Squarespace) | Easy Google Workspace integration | $12-14/yr |

### How many domains to buy

| Daily send target | Domains needed | Inboxes per domain | Total inboxes |
|-------------------|----------------|--------------------|----|
| 100/day | 3 | 2 | 6 |
| 250/day | 5 | 2-3 | 10-15 |
| 500/day | 10 | 2 | 20 |
| 1,000/day | 15-20 | 2-3 | 30-60 |

### Domain naming conventions

**Rules:**
- Similar to your main domain but NOT identical
- Use variations: get[brand].com, try[brand].com, [brand]hq.com, [brand]team.com
- Avoid exact match of main domain (protects main domain reputation)
- Use .com only (other TLDs have higher spam scores)
- Buy domains that are at least pronounceable

**Examples for "printmaxx.com":**
- getprintmaxx.com
- printmaxxhq.com
- printmaxxteam.com
- tryprintmaxx.com
- printmaxxgroup.com
- helloprintmaxx.com

**Bad examples (avoid):**
- pr1ntmaxx.com (looks spammy)
- printmaxx-offers.com (spam trigger word)
- printmaxx123.com (looks fake)

### Domain age requirement

- New domains need 2-4 weeks before sending cold email
- Buy domains ASAP, even if you won't send for a month
- Older domains = better reputation baseline
- Check domain history: web.archive.org (avoid previously spammed domains)

---

## Phase 2: DNS records (SPF, DKIM, DMARC)

### SPF record

**Record type:** TXT
**Host:** @
**Value:**
```
v=spf1 include:_spf.google.com ~all
```

If also using Instantly:
```
v=spf1 include:_spf.google.com include:spf.instantly.ai ~all
```

If also using Smartlead:
```
v=spf1 include:_spf.google.com include:_spf.smartlead.ai ~all
```

**Rules:**
- Only ONE SPF record per domain
- Use `~all` (soft fail), NOT `-all` (hard fail)
- Maximum 10 DNS lookups in SPF record
- If hitting limit, use SPF flattening (dmarcian.com)

### DKIM record

**Get from Google Workspace:**
1. Admin console > Apps > Google Workspace > Gmail
2. Click "Authenticate email"
3. Click "Generate new record"
4. Select 2048-bit key
5. Copy the TXT record value

**Record type:** TXT
**Host:** google._domainkey
**Value:** (long string starting with `v=DKIM1; k=rsa; p=...`)

**After adding DNS record:** Go back to Google Workspace and click "Start authentication"

### DMARC record

**Start with monitoring (first 30 days):**

**Record type:** TXT
**Host:** _dmarc
**Value:**
```
v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```

**After 30 days, upgrade to quarantine:**
```
v=DMARC1; p=quarantine; pct=100; rua=mailto:dmarc@yourdomain.com
```

### MX records (Google Workspace)

| Priority | Value |
|----------|-------|
| 1 | ASPMX.L.GOOGLE.COM |
| 5 | ALT1.ASPMX.L.GOOGLE.COM |
| 5 | ALT2.ASPMX.L.GOOGLE.COM |
| 10 | ALT3.ASPMX.L.GOOGLE.COM |
| 10 | ALT4.ASPMX.L.GOOGLE.COM |

### Custom tracking domain

If using Instantly/Smartlead tracking:

**Record type:** CNAME
**Host:** track (or custom subdomain)
**Value:** (provided by your email tool)

**Why:** Custom tracking domain prevents Google from flagging shared tracking URLs

### Verification after DNS setup

- [ ] SPF: `dig TXT yourdomain.com` shows SPF record
- [ ] DKIM: `dig TXT google._domainkey.yourdomain.com` shows DKIM
- [ ] DMARC: `dig TXT _dmarc.yourdomain.com` shows DMARC
- [ ] MX: `dig MX yourdomain.com` shows Google MX records
- [ ] mail-tester.com score: 9/10 or higher
- [ ] mxtoolbox.com/emailhealth: all green

---

## Phase 3: Google Workspace setup

### Per-inbox setup

For each sending inbox:
1. Create Google Workspace account ($6/mo per user)
2. Set up professional email: name@domain.com
3. Add profile photo (real person photo, not logo)
4. Set display name to real-sounding name
5. Create email signature (plain text only):

```
{{firstName}} {{lastName}}
{{title}} | {{company}}
{{phone}}
```

**No images, no social icons, no marketing slogans in signature.**

### Inbox naming conventions

Use real-sounding names. Vary first names:
- sarah@getprintmaxx.com
- mike@printmaxxhq.com
- jessica@printmaxxteam.com
- david@tryprintmaxx.com

**Avoid:**
- info@, sales@, team@, hello@ (role-based = spam filter trigger)
- Same name across all domains (looks like automation)

---

## Phase 4: Warmup protocol

### Pre-warmed inbox option (faster path)

**DeliverOn / EmailBison / InboxAlly:**
- Buy pre-warmed inboxes (already have reputation)
- Cost: $35-50/inbox/month
- Skip to sending in 3-5 days instead of 14-30
- Best for: fast launch, testing new offers

### Self-warmup protocol (cheaper, slower)

| Day | Warmup emails/day | Cold emails/day | Notes |
|-----|-------------------|-----------------|-------|
| 1-7 | 10-15 | 0 | Warmup only |
| 8-14 | 20-30 | 5-10 | Start slow |
| 15-21 | 30-40 | 15-20 | Monitor deliverability |
| 22-30 | 40-50 | 20-30 | Ramp up |
| 31+ | 20-30 (maintenance) | 30-50 | Full volume |

### Warmup tool settings (Instantly)

```
Daily warmup limit: Start 10, increase by 5 every 3 days
Reply rate: 30-40%
Read emulation: ON
Mark important: ON
Custom warmup tag: [domain]-warmup
```

### Warmup monitoring

Check daily during warmup:
- [ ] Warmup emails landing in inbox (not spam)
- [ ] No Google security alerts
- [ ] mail-tester.com score stable at 9+
- [ ] No bounces from warmup network

**Red flags (pause immediately):**
- Warmup emails going to spam folder
- Google "suspicious activity" warning
- mail-tester score dropped below 8
- Any bounce rate over 3%

---

## Phase 5: Sending tool configuration

### Instantly setup

1. Connect Google Workspace accounts (OAuth)
2. Enable warmup per inbox
3. Set up inbox rotation (spread sends across all inboxes)
4. Configure sending schedule:
   - Send window: 8am-5pm recipient timezone
   - Days: Monday through Thursday (Friday optional)
   - Delay between emails: 90-180 seconds
   - Max sends per inbox per day: 30-40 (leave headroom for warmup)

5. Set up custom tracking domain
6. Enable reply detection (auto-pause sequence on reply)
7. Set up auto-labels for replies

### Smartlead setup

Same as above. Key differences:
- Better analytics dashboard
- Built-in lead scoring
- More granular A/B testing
- Slightly more expensive ($39/mo base)

### Campaign settings checklist

- [ ] Inbox rotation enabled
- [ ] Sending schedule set to business hours
- [ ] Timezone detection enabled
- [ ] Reply stop enabled (stops sequence when lead replies)
- [ ] Bounce handling configured (auto-remove bounced emails)
- [ ] Unsubscribe handling set up
- [ ] Custom tracking domain active
- [ ] Test email sent to personal Gmail and Outlook

---

## Phase 6: Pre-send content checklist

### Subject line rules

- [ ] Under 50 characters
- [ ] No ALL CAPS words
- [ ] No spam trigger words (free, guarantee, act now, limited time, urgent)
- [ ] No excessive punctuation (!!!, ???)
- [ ] Personalization token works correctly
- [ ] Looks like one human emailing another human

### Body rules

- [ ] Under 100 words (ideal: 50-80)
- [ ] Plain text only (NO HTML formatting)
- [ ] No images
- [ ] No attachments
- [ ] Maximum 1 link (calendar link or website)
- [ ] No link shorteners (bit.ly triggers spam filters)
- [ ] No colored text or custom fonts
- [ ] No marketing slogans or taglines
- [ ] Personalization variables populate correctly (not showing {{firstName}})
- [ ] Reads like a real person wrote it
- [ ] One clear CTA per email

### Spam trigger words to NEVER use

**Hard triggers (almost guaranteed spam):**
free, guarantee, act now, limited time, winner, congratulations, selected, click here, click below, urgent, no obligation, risk-free, discount, save, offer expires, order now, buy now, lowest price, one time offer

**Soft triggers (use sparingly or avoid):**
deal, opportunity, exclusive, special, promotion, incredible, amazing, unsubscribe (yes, counterintuitive for cold email)

### Signature rules

- [ ] Plain text only (no images)
- [ ] Real name and title
- [ ] Company name
- [ ] Phone number (optional but adds legitimacy)
- [ ] No social media icon images
- [ ] No marketing taglines
- [ ] No HTML formatting

---

## Phase 7: List quality pre-checks

### Before loading any list

- [ ] Emails verified through ZeroBounce or NeverBounce
- [ ] Bounce rate estimate under 3%
- [ ] Removed all catch-all email addresses
- [ ] Removed all role-based addresses (info@, sales@, support@, team@)
- [ ] Removed personal Gmail/Yahoo addresses (B2B only)
- [ ] Data is fresh (less than 90 days old)
- [ ] Removed duplicates
- [ ] Removed competitors
- [ ] Removed current customers
- [ ] Removed previous bounces from other campaigns
- [ ] Removed previous unsubscribes
- [ ] ICP criteria validated (right company size, industry, title)

---

## Phase 8: Volume ramp schedule

### First campaign launch

| Day | Volume | What to watch |
|-----|--------|---------------|
| 1-3 | 20% of target (e.g., 10/inbox) | Bounce rate, open rate |
| 4-7 | 50% of target (e.g., 20/inbox) | Reply rate, spam complaints |
| 8-14 | 75% of target (e.g., 30/inbox) | Sustained deliverability |
| 15+ | Full volume (e.g., 40/inbox) | All metrics stable |

### Daily monitoring during ramp

- [ ] Bounce rate under 3%
- [ ] Open rate above 40% (below 20% = deliverability problem)
- [ ] No spam complaints
- [ ] No inbox lockouts or Google warnings
- [ ] Warmup emails still landing in inbox
- [ ] Reply inbox checked and responded to within 4 hours

### Red flags: STOP SENDING IMMEDIATELY if

- Bounce rate over 5%
- Open rate under 20%
- Multiple spam complaints in one day
- Any inbox locked or suspended
- Warmup emails suddenly going to spam
- mail-tester score dropped below 7

---

## Phase 9: A/B testing framework

### What to test (in priority order)

1. **Subject lines** (biggest impact on open rate)
   - Test: company name vs question vs observation
   - Sample: 200 emails per variant minimum
   - Winner: highest open rate after 48 hours

2. **First line** (biggest impact on reply rate)
   - Test: specific observation vs generic opener
   - Sample: 200 per variant
   - Winner: highest reply rate after 7 days

3. **CTA** (impacts meeting booking rate)
   - Test: "15 min call?" vs "want me to send?" vs "interested?"
   - Sample: 200 per variant
   - Winner: highest positive reply rate

4. **Send time** (impacts open rate)
   - Test: 8am vs 11am vs 2pm recipient timezone
   - Sample: 500+ per time slot
   - Winner: highest open rate

5. **Sequence length** (impacts total conversion)
   - Test: 3-email vs 5-email sequence
   - Sample: 500+ per variant
   - Winner: highest meeting rate per 100 prospects

### A/B test rules

- Only test ONE variable at a time
- Minimum 200 sends per variant before declaring winner
- Wait full 7 days before judging reply rates
- Judge open rate after 48 hours
- Document every test result in `MONEY_METHODS/COLD_OUTBOUND/metrics/AB_TEST_LOG.md`

---

## Phase 10: Ongoing maintenance

### Daily checks (5 minutes)

- [ ] Check reply inbox
- [ ] Respond to interested leads within 4 hours
- [ ] Check for bounces
- [ ] Check for spam complaints
- [ ] Verify warmup still running

### Weekly checks (15 minutes)

- [ ] Run mail-tester.com on each sending domain
- [ ] Check Google Postmaster Tools for domain reputation
- [ ] Review open/reply rates by inbox (rotate out underperformers)
- [ ] Add fresh leads to campaigns
- [ ] Check mxtoolbox.com blacklist status

### Monthly checks (30 minutes)

- [ ] Full deliverability audit on all domains
- [ ] Blacklist check on all domains
- [ ] Review inbox health across all accounts
- [ ] Rest tired domains (rotate in fresh ones)
- [ ] Update ICP based on who's responding best
- [ ] Review and optimize sequences based on performance data
- [ ] Budget check: domain renewals, workspace costs, tool subscriptions

---

## Emergency procedures

### Deliverability tanked

1. **Pause all cold sending immediately**
2. Keep warmup running at 2x volume
3. Check mail-tester.com score
4. Check mxtoolbox.com for blacklists
5. Review last 48 hours: what changed? (new list? new copy? volume spike?)
6. Fix root cause
7. Wait 2 weeks with warmup only
8. Restart at 20% volume

### Inbox suspended

1. Don't panic (often temporary)
2. Follow Google's recovery steps
3. Wait 24-48 hours
4. If permanent: that inbox is burned. Remove from tool. Don't send from it.
5. Set up replacement inbox on different domain

### Blacklisted

1. Check which blacklist: mxtoolbox.com
2. Submit removal request to blacklist
3. Fix the issue that caused blacklisting (usually bad list or volume spike)
4. Wait for removal (24 hours to 2 weeks depending on blacklist)
5. Monitor closely after removal

### Budget for failure

- Plan to lose 1-2 inboxes per quarter. It happens.
- Keep 2-3 backup domains aged and warm
- Never put all sending on one domain

---

## Cost summary

| Item | Monthly cost | Notes |
|------|-------------|-------|
| Domains (10) | ~$10/mo ($100/yr) | Buy on Porkbun |
| Google Workspace (20 inboxes) | $120/mo ($6/user) | 2 inboxes per domain |
| Instantly (Growth) | $97/mo | Up to 25 email accounts |
| Email verification | $16-40/mo | ZeroBounce, depends on volume |
| Apollo (Professional) | $99/mo | Lead sourcing |
| LinkedIn Sales Nav | $99/mo | Optional but recommended |
| **Total** | **~$440-$470/mo** | For 500 cold emails/day capacity |

### ROI math

At 500 emails/day x 20 business days = 10,000 emails/month
- 50% open rate = 5,000 opens
- 5% reply rate = 500 replies
- 20% positive = 100 interested leads
- 30% meeting rate = 30 meetings
- 20% close rate = 6 new clients

At $1,500/mo average client value:
- Revenue: $9,000/mo
- Cost: $470/mo
- **ROI: 19x**

Even at half these rates, ROI is 9.5x. The math works.

---

Created: 2026-01-28
Last updated: 2026-01-28
References: DELIVERABILITY_CHECKLIST.md, DNS_RECORDS.md, INBOX_WARMUP.md, EMAIL_TOOLS_COMPARISON.md
