# Domain setup for cold email

Your main domain is your brand. Never send cold email from it. Buy separate domains.

## How many domains to buy

- 1 inbox = 20-30 emails per day max
- 1 domain = 2-3 inboxes safe limit
- Want to send 500/day? You need 8-10 domains

**Budget:** $10-15/domain/year on Namecheap, Porkbun, or Cloudflare

## Domain naming strategy

Use variations of your main brand:

Main: acmeagency.com

Buy:
- getacme.io
- acmehq.co
- tryacme.com
- acmegroup.co
- withacme.io

**Rules:**
- Same root word or brand
- Different TLDs (.io, .co, .com, .agency)
- Easy to spell
- Professional sounding

## Where to buy

| Registrar | Price | WHOIS Privacy | Notes |
|-----------|-------|---------------|-------|
| Porkbun | $9-12 | Free | Cheapest, good UI |
| Cloudflare | $9-10 | Free | At-cost pricing |
| Namecheap | $10-13 | Free | Most features |
| Google Domains | $12 | Free | Now moved to Squarespace |

## Step-by-step setup

### 1. Buy the domain
- Go to Porkbun
- Search for your variation
- Buy 1 year (test first, then renew winners)
- Total: 8-10 domains = $80-120

### 2. Set up Google Workspace
- Go to workspace.google.com
- $7.20/user/month (Starter plan works)
- Add your domain during signup
- Create 2-3 inboxes per domain:
  - john@getacme.io
  - sarah@getacme.io
  - mike@getacme.io

### 3. Configure DNS (see DNS_RECORDS.md)

### 4. Create professional email signatures

```
John Smith
Account Executive | Acme Agency
Direct: (555) 123-4567
getacme.io
```

Keep it simple. No images, no social links, no quotes.

## Domain age matters

Fresh domains have lower trust. Options:

1. **Wait method:** Buy domains, let them sit 2-4 weeks before sending
2. **Aged domain method:** Buy domains that were registered 1+ years ago on aftermarket (Namecheap marketplace, Sedo)
3. **Warmup method:** Start slow (5 emails/day) and ramp up over 30 days

Aged domains cost more ($50-200) but skip the waiting period.

## Tracking domain health

After 30 days of sending, check:

- mail-tester.com (send test email, get score)
- mxtoolbox.com (blacklist check)
- Google Postmaster Tools (if sending to Gmail)

**Healthy domain:** 9+/10 mail-tester, zero blacklists

**Sick domain:** Under 5/10, multiple blacklists = burn it, start fresh

## How long domains last

With good practices (warm sending, good lists, no spam):
- 6-12 months per domain

With aggressive sending or bad lists:
- 1-3 months before reputation tanks

**Budget for replacement:** Add 2-3 new domains every quarter.

## Domain rotation strategy

If you have 10 domains:
- Use 6-8 actively
- Keep 2-4 warming up or resting
- Rotate sick domains out
- Rotate fresh domains in

Never send from all domains simultaneously. Spread risk.

## Cost summary for 500 emails/day capacity

| Item | Cost | Notes |
|------|------|-------|
| 10 domains | $100/year | $10 each |
| 25 Google Workspace inboxes | $2,160/year | $7.20 x 25 x 12 |
| Email tool (Instantly/Smartlead) | $600-1,200/year | $50-100/month |
| **Total** | ~$3,000/year | |

That's $250/month for infrastructure to send 10,000+ cold emails/month.

## Next steps

1. Buy 3-5 domains to start
2. Set up Google Workspace
3. Configure DNS records (DNS_RECORDS.md)
4. Start warmup (INBOX_WARMUP.md)
5. After 30 days, start sending
