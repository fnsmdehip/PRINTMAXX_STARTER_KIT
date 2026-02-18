---
title: "Cold email deliverability: SPF, DKIM, DMARC setup guide 2026 | PrintMaxx"
description: "90% of cold emails land in spam because of wrong DNS setup. Fix SPF, DKIM, DMARC in 30 minutes."
keywords: ["cold email deliverability", "SPF DKIM DMARC", "email authentication", "cold email setup"]
author: "PrintMaxx Team"
date: "2026-02-02"
published: true
canonical: "/longtail/cold-email-deliverability-setup-spf-dkim-dmarc-guide-2026"
schema: "HowTo"
---

# Cold email deliverability: SPF, DKIM, DMARC setup guide 2026

## Quick answer

If your cold emails land in spam, it is almost certainly a DNS authentication problem. You need three DNS records: SPF (who can send), DKIM (email is authentic), and DMARC (what to do with failures). Setup takes 30 minutes. Without these, Gmail and Outlook reject 90%+ of your emails.

## The three records

| Record | What it does | Without it |
|--------|-------------|-----------|
| SPF | Tells servers which IPs can send from your domain | Emails marked as spoofed |
| DKIM | Cryptographic signature proving authenticity | Emails marked as tampered |
| DMARC | Tells servers what to do on failure | No enforcement or reporting |

All three required. Missing any one = spam folder.

## Step-by-step setup

### Step 1: Buy a separate domain (5 min)

Never send cold emails from your main domain. If main is `printmaxx.com`, buy `printmaxx.io` for outreach. Domains cost $10-15/year.

### Step 2: Set up SPF (5 min)

TXT record: `v=spf1 include:_spf.google.com ~all`

Rules: max 10 DNS lookups, use `~all` soft fail, one SPF record per domain.

### Step 3: Set up DKIM (10 min)

Google Workspace: Admin console, Apps, Gmail, Authenticate email. Generate 2048-bit key. Add TXT record.

### Step 4: Set up DMARC (5 min)

TXT record: `v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com; pct=100`

Start with p=none (monitor). After 2-4 weeks, upgrade to p=quarantine, then p=reject.

### Step 5: Verify (5 min)

Use MXToolbox and mail-tester.com. Target 9/10 or 10/10 score.

## Domain warmup schedule

| Day | Emails/day | Who to email |
|-----|-----------|-------------|
| 1-3 | 5 | Your own accounts |
| 4-7 | 10 | Friends who will reply |
| 8-14 | 20 | Mix warm + first cold |
| 15-21 | 30 | Mostly cold |
| 22-30 | 50 | Full cold volume |
| 30+ | 100 max | Monitor weekly |

Never exceed 100 cold emails per domain per day. Use multiple domains for volume.

## Volume scaling

| Domains | Emails/day | Monthly | Cost/year |
|---------|-----------|---------|-----------|
| 1 | 50-100 | 1,500-3,000 | $12 |
| 3 | 150-300 | 4,500-9,000 | $36 |
| 5 | 250-500 | 7,500-15,000 | $60 |
| 10 | 500-1,000 | 15,000-30,000 | $120 |

## Common deliverability killers

- Sending from your main domain
- No warmup period
- Too many emails too fast
- High bounce rate (aim under 3%)
- No reply handling
- Generic subject lines
- Links in first email

## FAQ

### How long do DNS records take to propagate?

1-4 hours usually. Up to 48 hours for some providers. Check with MXToolbox.

### Can I use Gmail for cold email?

Google Workspace yes ($7.20/mo). Free Gmail no, gets flagged quickly.

### What is a good open rate?

50-70% for properly authenticated cold email. Under 30% means spam problem.

### Should I use Instantly or Smartlead?

After warmup, yes. They handle rotation, warmup automation, and deliverability monitoring. Worth it at 100+ emails/day.

## Schema (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "Cold email deliverability setup",
  "totalTime": "PT30M",
  "step": [
    {"@type": "HowToStep", "name": "Buy separate domain", "text": "Purchase domain for cold outreach."},
    {"@type": "HowToStep", "name": "Set up SPF", "text": "Add TXT record for authorized senders."},
    {"@type": "HowToStep", "name": "Set up DKIM", "text": "Generate and add DKIM key."},
    {"@type": "HowToStep", "name": "Set up DMARC", "text": "Add DMARC record with p=none."},
    {"@type": "HowToStep", "name": "Verify", "text": "Test with MXToolbox. Target 9+/10."}
  ]
}
```

## Related

- [How to write cold emails that don't sound like spam](/longtail/how-to-write-cold-emails-that-dont-sound-like-spam)
- [Best email automation stack for solopreneurs 2026](/longtail/best-email-automation-stack-for-solopreneurs-2026)
- [Cold email sequence template for lead generation](/longtail/cold-email-sequence-template-lead-generation)

## Next steps

1. Buy a separate domain ($12/year)
2. Set up SPF, DKIM, DMARC (30 min)
3. Verify with mail-tester.com (target 9+/10)
4. Warm up 14 days before cold emails
5. Start at 20 emails/day, scale to 100/day