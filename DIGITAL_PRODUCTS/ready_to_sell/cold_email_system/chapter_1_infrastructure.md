# Chapter 1: Free Email Infrastructure That Doesn't Land in Spam

## What You'll Have After This Chapter

Three email accounts on custom domains with proper DNS authentication, warmed up and ready to send cold emails without landing in spam. Total cost: $10/year per domain. Total tool cost: $0.

## Why Infrastructure Matters More Than Copy

You could write the best cold email in history. If your domain has no reputation and your DNS records are wrong, it's going to spam. 76% of cold emails never reach the inbox. Not because the content is bad — because the sender's infrastructure is broken.

Fix the infrastructure first. Then worry about what you're writing.

## Step 1: Buy 3 Domains (15 minutes)

Don't send cold emails from your primary domain. If your main domain gets flagged, your entire business email goes to spam. That's a recovery process that takes 4-6 weeks and sometimes never fully recovers.

Buy 3 secondary domains. They should look related to your main brand but different enough that if one gets burned, the others survive.

Example: If your business is `acmedesign.com`:
- `acmedesign.co`
- `acmedigital.com`
- `getacme.com`

Where to buy:
- **Porkbun**: $9-11/year for a .com, free WHOIS privacy
- **Namecheap**: $8-12/year, $2.88 first year promotions regularly
- **Cloudflare Registrar**: At-cost pricing, usually $9-10/year

Don't use GoDaddy. Their markup is 30-50% higher and their upselling is relentless.

You're spending $27-33/year on 3 domains. This is your only cost.

## Step 2: Set Up Free Email Accounts (20 minutes per domain)

You need actual email accounts on each domain. Three free options:

### Option A: Zoho Mail (Free Plan)

Zoho's free plan gives you 5 email accounts per domain with 5GB storage each. This is the best free option.

1. Go to `mail.zoho.com` and sign up
2. Click "Add Domain" and enter your domain
3. Zoho gives you DNS records to add. Go to your domain registrar and add:
   - MX records (these tell the internet where your email lives)
   - TXT record for domain verification
4. Create your email: `yourname@yourdomain.com`
5. Repeat for all 3 domains

### Option B: ImprovMX + Gmail (Free)

ImprovMX forwards emails from your custom domain to your Gmail. Free plan allows 25 forwarding addresses.

1. Go to `improvmx.com` and add your domain
2. Add the MX records they provide to your DNS
3. In Gmail, go to Settings > Accounts > "Send mail as" and add your custom domain email
4. Gmail will send a verification email — confirm it
5. Now you can send AND receive from your custom domain using Gmail's interface

### Option C: Cloudflare Email Routing + Gmail (Free)

If your domain is on Cloudflare:

1. Dashboard > Email > Email Routing
2. Add a forwarding rule: `yourname@yourdomain.com` forwards to your Gmail
3. In Gmail, add it as a "Send mail as" address (same process as Option B)

Whichever option you choose, create one email account per domain. Use professional names:
- `alex@acmedesign.co` (good)
- `contact@acmedesign.co` (too generic for cold email)
- `alex.smith@acmedesign.co` (good if your name is common)

## Step 3: DNS Configuration (30 minutes total)

This is the part most people skip, and it's why their emails go to spam. You need three DNS records per domain: SPF, DKIM, and DMARC.

### SPF (Sender Policy Framework)

SPF tells receiving servers which mail servers are authorized to send email from your domain.

Add a TXT record to your DNS:

```
Type: TXT
Host: @
Value: v=spf1 include:zoho.com ~all
```

If using Gmail/ImprovMX:
```
Value: v=spf1 include:_spf.google.com include:improvmx.com ~all
```

**Important:** You can only have ONE SPF record per domain. If you need multiple services, combine them into one record with multiple `include:` statements.

### DKIM (DomainKeys Identified Mail)

DKIM adds a cryptographic signature to your emails, proving they came from you and weren't tampered with.

- **Zoho:** Go to Mail Admin Console > Email Authentication > DKIM. Zoho generates the record. Add it to your DNS as a TXT record.
- **Gmail:** Google Workspace has DKIM built in. For free Gmail with ImprovMX, DKIM is handled by Google's servers.

The record looks something like:
```
Type: TXT
Host: zoho._domainkey
Value: v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4...(long key)
```

### DMARC (Domain-based Message Authentication)

DMARC tells receiving servers what to do if SPF or DKIM fails.

Add a TXT record:
```
Type: TXT
Host: _dmarc
Value: v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```

Start with `p=none` (monitor mode). This tells receivers to deliver emails even if checks fail, but send you reports. After 2 weeks of successful sending, change to `p=quarantine`.

### Verify Your Setup

Go to `mxtoolbox.com/SuperTool.aspx` and run these checks:
- MX Lookup: Confirms your mail server is configured
- SPF Record Lookup: Confirms SPF is valid
- DKIM Test: Send an email to `check-auth@verifier.port25.com` — you'll get a report back
- DMARC Lookup: Confirms your DMARC policy

All three should show green checks. If any fail, fix them before sending a single cold email.

## Step 4: Domain Warming (14 days)

A brand-new domain sending 50 emails on day one gets flagged instantly. You need to warm it up — establish sending reputation gradually.

### Free Warming Method (Manual)

Days 1-3: Send 3-5 personal emails per day to friends, colleagues, and yourself. Have them reply to every email. Open, read, and reply to all responses.

Days 4-7: Send 10-15 emails per day. Mix personal emails with emails to yourself at different providers (Gmail, Outlook, Yahoo). Have conversations — reply threads build reputation faster than one-off sends.

Days 8-14: Send 15-25 emails per day. Start subscribing to newsletters and replying to mailing list emails from this address. The goal is diverse, two-way email activity.

### Semi-Automated Warming

**InboxAlly** has a free tier (limited). Sign up at `inboxally.com`. It sends seed emails to your address and engages with them (opens, clicks, replies, moves from spam to inbox). This trains Gmail and Outlook to trust your domain.

**Warmup Inbox** (warmupinbox.com) — free tier available. Similar concept.

### What "Warmed" Looks Like

After 14 days:
- You can send 50-75 emails/day per domain without spam issues
- Your emails land in Primary (Gmail) or Inbox (Outlook), not Promotions or Spam
- Your domain has a neutral-to-positive reputation

Test by sending an email to `mail-tester.com`. They score you 1-10. You want 7+ before starting outreach.

## Step 5: Sending Infrastructure

Don't send cold emails from your email client (Gmail, Zoho webmail). You need a sending tool that handles scheduling, follow-ups, and tracking.

### Free Sending Tools

**GMass** (free tier): 50 emails/day for free. Works inside Gmail. Handles sequences, follow-ups, and basic tracking. This is the best free option if you're using Gmail.

To set up:
1. Install the GMass Chrome extension
2. Connect your Gmail account
3. Create a Google Sheet with your prospect list (Name, Email, Company columns)
4. Compose your email in Gmail
5. GMass personalizes and schedules sends from the Sheet

**Mailmeteor** (free tier): 50 emails/day. Also works inside Gmail/Google Sheets. Simpler than GMass but limited to single sends (no sequences on free plan).

**Yet Another Mail Merge (YAMM)**: 50 emails/day free tier. Google Sheets integration.

### Sending Rules

- **Never send more than 50 emails per domain per day.** Across 3 domains, that's 150 emails/day — more than enough.
- **Space sends 60-120 seconds apart.** Bulk blasts at the same timestamp scream spam.
- **Send between 8 AM - 11 AM in your prospect's timezone.** Tuesday, Wednesday, Thursday are highest open rate days.
- **Don't use tracking pixels** on cold emails. Google's AI detects tracking pixels and deprioritizes those emails. Use reply rate as your metric instead of open rate.
- **Plain text only.** No HTML templates, no images, no logos. Plain text emails get 2-3x higher deliverability in cold outreach.

## Infrastructure Checklist

Before moving to Chapter 2, confirm:

- [ ] 3 domains purchased and DNS pointed correctly
- [ ] Email accounts created on each domain
- [ ] SPF record added and verified on all 3 domains
- [ ] DKIM record added and verified on all 3 domains
- [ ] DMARC record added on all 3 domains
- [ ] mail-tester.com score of 7+ on all 3 accounts
- [ ] 14 days of warming completed (or warming tool running)
- [ ] GMass or alternative sending tool installed and configured
- [ ] Test email sent to yourself and landing in Primary inbox

If any of these are incomplete, stop here and fix them. Sending cold emails on broken infrastructure is worse than not sending at all — you'll burn domains that take 2 weeks to set up.

Next chapter: Finding 500+ qualified prospects using only free tools.
