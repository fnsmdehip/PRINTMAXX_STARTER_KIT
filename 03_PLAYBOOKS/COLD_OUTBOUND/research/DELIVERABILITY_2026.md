# Cold Email Deliverability Guide 2026

**Updated:** 2026-01-20
**Purpose:** Current best practices for inbox placement and avoiding spam filters

---

## The Deliverability Landscape 2026

### What Changed

**Google/Yahoo February 2024 Requirements (Still Active):**
- SPF, DKIM, DMARC now required for bulk senders
- One-click unsubscribe mandatory
- Spam complaint rate must stay under 0.3%
- These are enforced, not suggestions

**2025-2026 Updates:**
- AI-powered spam detection more sophisticated
- Engagement signals weighted more heavily
- Domain reputation more important than ever
- Cold email platforms under more scrutiny

### The New Reality

**What Works:**
- Highly personalized, relevant outreach
- Low volume, high quality
- Strong domain/IP reputation
- Proper authentication (SPF/DKIM/DMARC)
- Clean lists (verified emails)

**What Doesn't Work:**
- Mass blast campaigns
- Generic templates
- Purchased/scraped lists without verification
- New domains without warmup
- Spammy subject lines

---

## Email Authentication Setup

### Required: SPF Record

**What it does:** Tells email servers which IPs can send on your domain's behalf

**Setup:**
1. Go to your domain DNS settings
2. Add TXT record
3. Value format:
```
v=spf1 include:_spf.google.com include:sendgrid.net ~all
```

**Check:** Use mxtoolbox.com/spf.aspx

### Required: DKIM Record

**What it does:** Digital signature proving email wasn't modified

**Setup:**
1. Generate DKIM key in your email provider
2. Add TXT record to DNS
3. Selector + key specific to provider

**Format:**
```
Name: selector._domainkey
Value: v=DKIM1; k=rsa; p=[your-public-key]
```

**Check:** Use mxtoolbox.com/dkim.aspx

### Required: DMARC Record

**What it does:** Tells servers what to do with failed SPF/DKIM and sends reports

**Setup:**
1. Add TXT record to DNS
2. Start with monitoring mode
3. Gradually increase enforcement

**Progression:**
```
# Week 1-2: Monitor only
v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com

# Week 3-4: Quarantine 25%
v=DMARC1; p=quarantine; pct=25; rua=mailto:dmarc@yourdomain.com

# Month 2+: Full enforcement
v=DMARC1; p=reject; rua=mailto:dmarc@yourdomain.com
```

**Check:** Use dmarcian.com/dmarc-inspector

### Authentication Checklist

- [ ] SPF record added and valid
- [ ] DKIM key generated and DNS record added
- [ ] DMARC record starting in monitor mode
- [ ] All three passing (use mail-tester.com to verify)
- [ ] Regular monitoring of DMARC reports

---

## Domain Setup Strategy

### The Multi-Domain Approach

**Never use your main domain for cold email.**

**Structure:**
```
Main domain: yourbrand.com (website, transactional)
Cold email 1: yourbrand.io
Cold email 2: yourbrand.co
Cold email 3: getyourbrand.com
Cold email 4: tryyourbrand.com
```

**Why multiple domains:**
- If one gets flagged, others keep working
- A/B test domain reputation impact
- Spread volume across domains
- Redundancy against platform changes

### Domain Selection Rules

**Good patterns:**
- yourname + industry.com
- get + yourproduct.com
- try + yourproduct.com
- yourproduct + hq.com

**Avoid:**
- Exact match of main domain
- Domains with "mail" in them
- Numeric domains
- Very long domains
- Recently expired/purchased domains (check history)

### Domain Age Matters

**New domain timeline:**
- Week 1-2: Don't send anything
- Week 2-4: Warmup only
- Week 4-8: Light sending (10-20/day)
- Week 8+: Gradual scale

**Best practice:** Buy domains 4-6 weeks before you need them

---

## Email Infrastructure Tiers

### Tier 1: Google Workspace (Recommended Start)

**Setup:**
- Google Workspace account ($6-12/user/mo)
- 1-3 inboxes per domain
- Alias strategy for variants

**Sending limits:**
- 500/day (new accounts)
- 2000/day (established accounts)
- Recommend: Stay under 50/inbox/day for cold

**Pros:**
- Highest deliverability to Gmail users
- Most trusted sender reputation
- Easy setup

**Cons:**
- Expensive at scale
- Account suspensions possible
- Manual setup per inbox

### Tier 2: Microsoft 365

**Setup:**
- Microsoft 365 Business ($6-12/user/mo)
- Similar inbox strategy to Google

**Sending limits:**
- 10,000/day (account level)
- Recommend: 50-100/inbox/day for cold

**Pros:**
- Good deliverability to Outlook/corporate
- More lenient than Google
- Cheaper at scale

**Cons:**
- Slightly lower deliverability to Gmail
- More complex setup

### Tier 3: Cold Email Platforms

**Options:**
| Platform | Cost | Inboxes | Features |
|----------|------|---------|----------|
| Instantly | $30-97/mo | Unlimited | Warmup, sequences, analytics |
| Smartlead | $39-79/mo | Unlimited | AI warmup, lead management |
| Lemlist | $59-99/mo | Per-inbox | Personalization, multichannel |
| Apollo | $49-99/mo | Limited | Built-in leads database |

**Pros:**
- Built-in warmup
- Sequence automation
- Analytics dashboard
- Easier management

**Cons:**
- Shared IP reputation risk
- Platform can change policies
- Learning curve

### Tier 4: Inbox-as-a-Service

**Options:**
| Service | Cost | What You Get |
|---------|------|--------------|
| Mailforge | $3/inbox/mo | Pre-warmed inboxes |
| DeliverOn | $49/mo | Managed infrastructure |
| Mailscale | $5/inbox/mo | Bulk inbox setup |

**Pros:**
- Skip warmup period
- Scale quickly
- Managed infrastructure

**Cons:**
- Less control
- Reputation depends on provider
- Can be shut down

### Recommended Stack (2026)

**Starting out:**
1. 2 Google Workspace accounts (2 inboxes each)
2. 2 secondary domains
3. Instantly for sequences and warmup
4. Budget: $100-150/mo

**Scaling:**
1. Add Microsoft 365 for corporate targets
2. Add Mailforge inboxes for volume
3. Multiple platforms for redundancy
4. Budget: $300-500/mo

---

## Warmup Protocol

### What Is Warmup?

Warmup = gradually increasing sending volume while maintaining positive engagement signals

**Purpose:**
- Build domain reputation
- Establish sender history
- Train spam filters you're legitimate
- Get inbox placement vs spam folder

### Manual Warmup (Free)

**Week 1:**
- Send 5-10 emails/day
- Only to people who will reply
- Friends, colleagues, existing contacts
- Reply to responses

**Week 2:**
- Send 10-20 emails/day
- Same principle - get replies
- Start calendar invites
- Subscribe to newsletters (shows engagement)

**Week 3-4:**
- Send 20-30 emails/day
- Mix personal and light prospecting
- Maintain 30%+ reply rate
- No bulk yet

### Automated Warmup Tools

| Tool | Cost | How It Works |
|------|------|--------------|
| Instantly warmup | Included | Network of real inboxes exchange |
| Warmbox | $15/mo | Similar network approach |
| Lemwarm | $29/mo | Part of Lemlist suite |
| Mailwarm | $79/mo | Standalone service |

**How automated warmup works:**
1. Tool sends emails between users' inboxes
2. Emails auto-opened and replied to
3. Moved from spam to inbox
4. Positive engagement signals built

### Warmup Timeline

| Week | Volume | Reply Rate Target | Notes |
|------|--------|-------------------|-------|
| 1-2 | 5-10/day | 50%+ | Manual only |
| 3-4 | 15-25/day | 40%+ | Start automation |
| 5-6 | 30-40/day | 30%+ | Light cold outreach |
| 7-8 | 40-50/day | 25%+ | Scale carefully |
| 9+ | 50-100/day max | 20%+ | Maintain reputation |

### Warmup Best Practices

- [ ] Never skip warmup for new domains
- [ ] Continue warmup even after starting cold sends
- [ ] Dedicate 20-30% of volume to warmup ongoing
- [ ] Monitor deliverability weekly
- [ ] Reduce volume if metrics drop

---

## Sending Best Practices

### Volume Guidelines

**Per inbox:**
- Maximum: 100 emails/day
- Recommended: 30-50 emails/day
- Conservative: 20-30 emails/day

**Per domain:**
- Maximum: 200-300 emails/day (across inboxes)
- Spread across business hours
- Don't send in bursts

### Timing Optimization

**Best days:**
- Tuesday, Wednesday, Thursday (B2B)
- Monday ok if not too early
- Friday ok if morning

**Best times:**
- 8-10 AM recipient timezone
- 2-4 PM recipient timezone
- Avoid: Before 7 AM, after 7 PM

**Spread sends:**
- 10-15 minute gaps between emails
- Randomize timing (don't send exactly on the hour)
- Mimic human sending patterns

### Subject Line Guidelines

**Do:**
- Keep under 50 characters
- Personalize when possible
- Be specific to their situation
- Use lowercase (more casual)
- Test variations

**Don't:**
- ALL CAPS anything
- Excessive punctuation!!!
- Spammy words (free, guarantee, act now)
- Misleading Re: or Fwd:
- Generic templates

**Good examples:**
- "Quick question about [Company]"
- "[Mutual connection] suggested I reach out"
- "Idea for [their specific problem]"
- "Saw your post about [topic]"

**Bad examples:**
- "AMAZING OPPORTUNITY!!!"
- "Re: Our conversation" (when there wasn't one)
- "FREE consultation inside"
- "Quick question" (too vague)

### Body Copy Guidelines

**Structure:**
```
Line 1: Personalized observation (proves you researched)
Line 2-3: Problem statement + bridge
Line 4: Your offer (specific, low commitment)
Line 5: Soft CTA
Signature: Name only (no long signature)
```

**Do:**
- Keep under 100 words
- Use short sentences
- One clear CTA
- Sound human
- Provide value

**Don't:**
- Wall of text
- Multiple links
- HTML formatting (images, colors)
- Attach files (first email)
- Multiple asks

---

## Deliverability Monitoring

### Key Metrics to Track

| Metric | Good | Warning | Bad |
|--------|------|---------|-----|
| Open rate | >50% | 30-50% | <30% |
| Reply rate | >5% | 2-5% | <2% |
| Bounce rate | <2% | 2-5% | >5% |
| Spam complaints | <0.1% | 0.1-0.3% | >0.3% |
| Unsubscribe rate | <0.5% | 0.5-1% | >1% |

### Monitoring Tools

**Free:**
- Google Postmaster Tools (Gmail deliverability)
- mail-tester.com (per-email scoring)
- mxtoolbox.com (authentication checks)

**Paid:**
- GlockApps ($59/mo) - inbox placement testing
- Mailreach ($25/mo) - deliverability monitoring
- MailerCheck ($10/mo) - email verification

### Weekly Checkup

- [ ] Review open rates by domain/inbox
- [ ] Check bounce rates
- [ ] Monitor spam complaints
- [ ] Run mail-tester.com on sample
- [ ] Check Google Postmaster Tools
- [ ] Verify warmup still running

### Recovery Protocol

**If metrics drop:**

1. **Stop sending** from affected inbox
2. **Increase warmup** ratio (50%+ of sends)
3. **Clean list** (remove bounces, unengaged)
4. **Check authentication** (SPF/DKIM/DMARC)
5. **Wait 2 weeks** before resuming
6. **Resume at 50%** of previous volume

**If inbox blacklisted:**

1. Stop using immediately
2. Check blacklist status (mxtoolbox.com/blacklists.aspx)
3. Request removal from blacklists
4. Wait 2-4 weeks
5. Start fresh warmup
6. Consider retiring if repeated

---

## List Hygiene

### Email Verification (Required)

**Verify all emails before sending.**

**Tools:**
| Service | Cost | Speed |
|---------|------|-------|
| NeverBounce | $8/1000 | Fast |
| ZeroBounce | $16/1000 | Fast |
| Hunter.io | Free tier | Medium |
| Clearout | $5/1000 | Fast |
| Emailable | $4/1000 | Fast |

**Verification results:**
- Valid: Safe to email
- Invalid: Remove immediately
- Catch-all: Use cautiously (50% risk)
- Unknown: Test small sample first

### List Maintenance

**Before sending:**
- Remove any email >6 months old without verification
- Remove role addresses (info@, sales@, support@)
- Remove free email domains if B2B only
- Check against suppression list

**After sending:**
- Remove hard bounces immediately
- Remove soft bounces after 3 attempts
- Remove unsubscribes immediately
- Suppress non-responders after 5+ touches

### Suppression List Management

**Never email again:**
- Hard bounces
- Spam complaints
- Unsubscribes
- Legal/compliance issues

**Store suppression list:**
- Separate from active lists
- Check against before any campaign
- Share across all email tools
- Keep forever

---

## Compliance Requirements

### CAN-SPAM (US)

**Required:**
- Physical mailing address in email
- Clear unsubscribe mechanism
- Honor unsubscribe within 10 days
- No misleading subject lines
- Identify as advertisement if applicable

### GDPR (EU/UK)

**Required for EU recipients:**
- Legitimate interest basis documented
- Clear identification of sender
- Easy unsubscribe
- Data processing records
- Respond to data requests within 30 days

### CASL (Canada)

**Required for Canadian recipients:**
- Implied or express consent
- Clear identification
- Unsubscribe mechanism
- Keep consent records

### Best Practice: Universal Compliance

Apply strictest rules to everyone:
- Clear sender identification
- Easy one-click unsubscribe
- Physical address included
- Respond to requests promptly
- Document everything

---

## Troubleshooting Guide

### "My emails go to spam"

**Check:**
1. Authentication (SPF/DKIM/DMARC) - mail-tester.com
2. Domain reputation - Google Postmaster
3. Content - remove spammy words, links
4. List quality - verify emails
5. Volume - reduce if too high

### "My open rates dropped"

**Check:**
1. Subject lines - test new variants
2. Send timing - adjust to recipient timezone
3. List fatigue - fresh leads needed
4. Domain reputation - may need recovery
5. Tracking pixels - some clients block

### "I'm getting bounces"

**Check:**
1. Email verification - verify before sending
2. List age - old lists decay
3. Data source - low quality source
4. Formatting - check for typos in addresses

### "My account got suspended"

**Actions:**
1. Don't panic - common, usually recoverable
2. Review terms violated
3. Appeal with explanation
4. Reduce volume on restoration
5. Consider backup platform

---

## 2026 Deliverability Checklist

### Setup (Do Once)

- [ ] Purchase 2+ secondary domains
- [ ] Wait 2 weeks before any sending
- [ ] Set up SPF, DKIM, DMARC on all domains
- [ ] Create Google Workspace or M365 accounts
- [ ] Set up cold email platform
- [ ] Configure warmup tools

### Weekly Maintenance

- [ ] Check deliverability metrics
- [ ] Review bounce rates
- [ ] Monitor spam complaints
- [ ] Verify warmup still running
- [ ] Clean lists of bounces/unsubscribes

### Monthly Audit

- [ ] Full authentication check
- [ ] Domain reputation review
- [ ] List quality assessment
- [ ] Platform performance comparison
- [ ] Update suppression lists

---

**Related docs:**
- WARM_UP_PROTOCOLS.md - Detailed warmup guide
- SCRIPT_TEMPLATES.md - Email copy templates
- LEAD_SOURCES.md - Where to find leads
- SEQUENCES.md - Multi-touch frameworks
