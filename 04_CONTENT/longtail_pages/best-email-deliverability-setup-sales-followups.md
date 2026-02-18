---
title: "Best email deliverability setup for sales follow-ups outreach | PrintMaxx"
description: "SPF, DKIM, DMARC, warmup, tracking. Skip spam folder. Hit inbox 95% of the time."
keywords: ["email deliverability", "spam filtering", "SPF DKIM DMARC", "email warmup", "sales outreach"]
author: "PrintMaxx Team"
date: "2026-01-21"
published: true
canonical: "/longtail/best-email-deliverability-setup-sales-followups"
---

# Best email deliverability setup for sales follow-ups outreach

## Quick Answer

SPF + DKIM + DMARC + warm up your IP = 95% inbox rate.

Skip these and you're in spam folder. Takes 2 hours to set up. Saves 50% of your outreach revenue.

## Why Deliverability Matters

Send 100 cold emails:

**Without deliverability setup:**
- 30 land in spam (lost)
- 70 land in inbox
- 5% reply rate = 3-4 responses

**With proper setup:**
- 5 land in spam
- 95 land in inbox
- 5% reply rate = 4-5 responses

+25-30% more replies from deliverability alone.

## The Checklist

### 1. Domain Setup (30 min)

Buy a custom domain. Don't use Gmail/Outlook free tier (spam folder magnet).

Costs: $12/year (Namecheap).

### 2. SPF Record (15 min)

SPF = "Sender Policy Framework"

Tells email providers: "This server is authorized to send emails for my domain."

In your domain registrar (Namecheap, GoDaddy):

```
Add DNS record:
Type: TXT
Name: @
Value: v=spf1 include:sendgrid.net ~all
```

(Replace sendgrid.net with your email tool's SPF value)

Check if it's working: https://mxtoolbox.com/spf.aspx

### 3. DKIM Record (15 min)

DKIM = "DomainKeys Identified Mail"

Cryptographically signs your emails. Proves you sent them.

Your email tool (Sendgrid, Mailgun, Convertkit) generates this:

```
Add DNS record:
Type: TXT
Name: default._domainkey
Value: [long string from email tool]
```

Check if working: https://mxtoolbox.com/dkim.aspx

### 4. DMARC Record (10 min)

DMARC = "Domain-based Message Authentication and Conformance"

Policy for what happens if SPF/DKIM fail.

```
Add DNS record:
Type: TXT
Name: _dmarc
Value: v=DMARC1; p=quarantine; rua=mailto:admin@yourdomain.com
```

This tells Gmail/Outlook: "If email fails checks, quarantine it."

Check if working: https://mxtoolbox.com/dmarc.aspx

### 5. Reverse DNS (Optional, 5 min)

Ask your hosting provider to set reverse DNS (PTR record).

Proves IP ownership. Most important for SMTP.

### 6. IP Warmup (7 days)

New IP = untrusted. Warmup gradually.

**Week 1:**
- Day 1: Send 5 emails
- Day 2: Send 10 emails
- Day 3: Send 20 emails
- Day 4: Send 40 emails
- Day 5: Send 80 emails
- Day 6: Send 100 emails
- Day 7: Send 200 emails

Ramp up slowly. Providers see "new IP, low volume, probably legit."

After 7 days, send 1000/day if you want.

### 7. Email Tracking (Smart)

Add pixel tracking to see opens:

```html
<img src="https://tracking.yourdomain.com/p?id=1234" width="1" height="1">
```

But don't overdo it. Too many redirects = spam folder.

Use reputable tools (Mailgun, Sendgrid, Convertkit).

## Email Tool Comparison

| Tool | Cost | Deliverability | Best For |
|------|------|-----------------|----------|
| Sendgrid | $25/mo | 95%+ | High volume |
| Mailgun | $35/mo | 95%+ | Developers |
| Convertkit | $25/mo | 92%+ | Creators |
| Lemlist | $25/mo | 90%+ | Cold email |
| Apollo | Free | 85% | Minimal |
| Gmail | $0 (free) | 60% | Personal |

Don't use free Gmail for sales. Spam folder waiting.

## Real Setup Example

You're sending sales follow-ups for SaaS product.

**Step 1: Buy domain**
- yoursaas.com ($12/year)

**Step 2: Add SPF**
```
yoursaas.com TXT v=spf1 include:sendgrid.net ~all
```

**Step 3: Add DKIM**
```
default._domainkey.yoursaas.com TXT [sendgrid DKIM]
```

**Step 4: Add DMARC**
```
_dmarc.yoursaas.com TXT v=DMARC1; p=quarantine
```

**Step 5: Warmup**
- Day 1: Send 5 emails
- Day 2: Send 10 emails
- ...continue ramping

**Step 6: Send campaigns**
- Use Sendgrid, Lemlist, or Apollo
- After warmup, send 100+ emails safely

**Result:** 95%+ inbox rate. 5% response rate from cold emails.

## Red Flags

**Sign your email might be in spam:**
- Reply rate below 2% (normal is 5-10%)
- Unsubscribe complaints (Gmail marks as spam)
- High bounce rate (bad list)
- Gets manually marked as spam (message quality)

**If experiencing issues:**
1. Check SPF/DKIM/DMARC are set (use mxtoolbox)
2. Warm up IP more slowly
3. Reduce email volume (send 20/day instead of 100)
4. Check email content (no spam words)
5. Clean email list (remove bounces)

## Email Content Best Practices

Avoid these in subject/body:

- ALL CAPS: MAKE $50K FAST
- Excessive punctuation: !!!!!!
- Spam keywords: FREE, GUARANTEED, RISK-FREE
- Misleading subject: "Re:" when not replying
- Too many links: [5+ links] = spam folder
- Weird formatting: Strange HTML
- From name mismatch: "John Smith" but email is marketing@

Keep it personal. One link per email. Real person name in From.

## Warming Sequence (Copy This)

```
Day 1: 5 emails to warm contacts (people you know)
Day 2: 10 emails (half warm, half new)
Day 3: 20 emails (mostly new)
Day 4: 40 emails (all new, higher quality)
Day 5: 80 emails (bulk)
Day 6: 100 emails (bulk)
Day 7: 200 emails (bulk)
Day 8+: 500-1000 emails/day (keep monitoring)
```

This ramps your reputation slowly.

## Cost Breakdown

| Item | Cost |
|------|------|
| Domain | $12/year |
| Email tool | $25/mo |
| DNS setup | Free (your time) |
| IP warmup | Free (just patience) |
| **Total** | **$25/mo** |

Cheap insurance for your outreach.

## Related

- [Cold email sequence template for lead generation](/longtail/cold-email-sequence-template-lead-generation)
- [How to avoid spam folder when cold emailing for sales follow-ups](/longtail/how-to-avoid-spam-folder-cold-email-sales)

## Next Steps

1. Buy domain ($12)
2. Add SPF record (15 min)
3. Add DKIM record (15 min)
4. Add DMARC record (10 min)
5. Verify all 3 with mxtoolbox
6. Start warmup sequence (7 days)
7. Send campaigns

One-time 1-hour setup. Protects your entire outreach forever.
