# DNS records for email deliverability

Three records protect your domain: SPF, DKIM, DMARC. Miss any one and you land in spam.

## Quick setup checklist

- [ ] SPF record added
- [ ] DKIM record added (from Google Workspace)
- [ ] DMARC record added
- [ ] MX records pointing to Google
- [ ] Test with mail-tester.com (score 9+/10)

## SPF (Sender Policy Framework)

Tells receiving servers which IPs can send email from your domain.

**Record type:** TXT
**Host:** @ (or leave blank)
**Value:**
```
v=spf1 include:_spf.google.com ~all
```

If using Instantly or Smartlead, add their SPF too:
```
v=spf1 include:_spf.google.com include:spf.instantly.ai ~all
```

**Common mistakes:**
- Multiple SPF records (only 1 allowed)
- Using `-all` instead of `~all` (too strict, causes bounces)
- Forgetting to add your email tool's SPF

## DKIM (DomainKeys Identified Mail)

Cryptographic signature that proves the email wasn't tampered with.

**Get your DKIM from Google Workspace:**
1. Admin console > Apps > Google Workspace > Gmail
2. Authenticate email
3. Generate new record
4. Copy the TXT record

**Record type:** TXT
**Host:** google._domainkey (Google tells you the exact host)
**Value:** Long string starting with `v=DKIM1; k=rsa; p=...`

**Important:** After adding the record, go back to Google Workspace and click "Start authentication"

## DMARC (Domain-based Message Authentication)

Tells receiving servers what to do when SPF/DKIM fail.

**Start with monitoring mode (first 30 days):**

**Record type:** TXT
**Host:** _dmarc
**Value:**
```
v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```

**After 30 days, switch to quarantine:**
```
v=DMARC1; p=quarantine; pct=100; rua=mailto:dmarc@yourdomain.com
```

**Aggressive mode (only if deliverability is solid):**
```
v=DMARC1; p=reject; pct=100; rua=mailto:dmarc@yourdomain.com
```

## MX Records (Mail Exchange)

Tell the world where to deliver email to your domain.

**For Google Workspace:**

| Priority | Host | Value |
|----------|------|-------|
| 1 | @ | ASPMX.L.GOOGLE.COM |
| 5 | @ | ALT1.ASPMX.L.GOOGLE.COM |
| 5 | @ | ALT2.ASPMX.L.GOOGLE.COM |
| 10 | @ | ALT3.ASPMX.L.GOOGLE.COM |
| 10 | @ | ALT4.ASPMX.L.GOOGLE.COM |

## Complete DNS example

For domain: getacme.io

| Type | Host | Value | TTL |
|------|------|-------|-----|
| MX | @ | ASPMX.L.GOOGLE.COM (Priority 1) | 3600 |
| MX | @ | ALT1.ASPMX.L.GOOGLE.COM (Priority 5) | 3600 |
| TXT | @ | v=spf1 include:_spf.google.com ~all | 3600 |
| TXT | google._domainkey | v=DKIM1; k=rsa; p=MIIBIj... | 3600 |
| TXT | _dmarc | v=DMARC1; p=none; rua=mailto:dmarc@getacme.io | 3600 |

## Verification tools

### Before sending (required)

**mail-tester.com**
1. Get your unique test address
2. Send an email from your inbox
3. Check score
4. Target: 9/10 or higher

**mxtoolbox.com/emailhealth**
- Checks SPF, DKIM, DMARC
- Shows any configuration errors

### After sending starts

**Google Postmaster Tools** (postmaster.google.com)
- Shows your domain reputation at Gmail
- Tracks spam rate
- Free, but takes a few days to show data

## DNS propagation

Changes take 15 minutes to 48 hours to propagate globally.

**Speed it up:**
- Set TTL to 300 (5 minutes) when making changes
- Use DNS checker: dnschecker.org
- Most changes work within 1 hour

## Troubleshooting

### SPF "permerror" or "too many lookups"
SPF allows max 10 DNS lookups. If you have many services:
- Use SPF flattening (dmarcian.com has free tool)
- Remove unused includes

### DKIM not validating
- Wait 24 hours after adding record
- Make sure you clicked "Start authentication" in Google
- Check for typos in the long DKIM string

### Emails going to spam despite perfect DNS
DNS is necessary but not sufficient. Also check:
- Email content (spam trigger words)
- Warmup status (see INBOX_WARMUP.md)
- List quality (bounces kill reputation)

## Per-registrar guides

### Cloudflare
1. DNS > Add record
2. Type: TXT
3. Name: @ or _dmarc or google._domainkey
4. Content: your value
5. Proxy status: DNS only (gray cloud)

### Namecheap
1. Domain List > Manage > Advanced DNS
2. Add New Record
3. Same fields as above

### Porkbun
1. Domain Management > DNS
2. Edit > Add record
3. Same fields

## Time investment

Setting up DNS for one domain: 15-20 minutes
Setting up 10 domains: 2-3 hours (gets faster with practice)

Do it right the first time. Bad DNS = all your emails go to spam.
