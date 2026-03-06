# Email Deliverability Guide

Goal: Land in Primary inbox, not Promotions or Spam
Target: 95%+ delivery rate, 90%+ inbox placement

---

## THE DELIVERABILITY STACK (In Priority Order)

1. DNS records (SPF, DKIM, DMARC) — non-negotiable
2. Domain warming — critical for new sending domains
3. List hygiene — ongoing
4. Content signals — ongoing
5. Engagement optimization — ongoing

Skip step 1 and nothing else matters. Your emails go to spam regardless.

---

## STEP 1: DNS RECORDS (SET THESE UP FIRST)

### SPF Record
**What it does:** Tells email providers which servers are allowed to send email from your domain.

**Add to DNS (TXT record):**
```
Type: TXT
Host: @ (or your domain)
Value: v=spf1 include:sendgrid.net include:beehiiv.com ~all
```

Adjust based on your ESP. Replace `sendgrid.net` with your ESP's include.

Common ESP includes:
- Beehiiv: `include:beehiiv.com`
- ConvertKit: `include:emailoctopus.com` or ConvertKit's specific include
- Mailchimp: `include:servers.mcsv.net`
- Instantly: `include:sparkpostmail.com`

**Verify:** Use MXToolbox.com → SPF Lookup

### DKIM Record
**What it does:** Cryptographically signs outgoing emails. Verifies the email wasn't tampered with in transit.

**Setup:** Your ESP generates the DKIM keys. Get them from your ESP dashboard under "Sending Domain" or "Authentication."

They'll give you something like:
```
Type: TXT
Host: smtp._domainkey.yourdomain.com
Value: v=DKIM1; k=rsa; p=MIGfMA0GCS...
```

Copy and paste exactly. Do not modify the key.

**Verify:** MXToolbox.com → DKIM Lookup → Enter domain + selector (usually "smtp" or "mail")

### DMARC Record
**What it does:** Tells email providers what to do when SPF or DKIM fails. Also gives you reports on who is sending email from your domain.

**Start with monitoring mode (p=none):**
```
Type: TXT
Host: _dmarc.yourdomain.com
Value: v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```

After 30 days with no issues, upgrade to quarantine:
```
Value: v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com
```

After 60 days, upgrade to reject (maximum protection):
```
Value: v=DMARC1; p=reject; rua=mailto:dmarc@yourdomain.com
```

**DMARC reports go to:** the `rua` email address. Use DMARC Analyzer (free tier) to read them.

### DNS Check Checklist
- [ ] SPF record exists and validates
- [ ] DKIM record exists and validates
- [ ] DMARC record exists (start with p=none)
- [ ] No conflicting SPF records (only one SPF record per domain)
- [ ] Verified with MXToolbox.com

---

## STEP 2: DOMAIN WARMING SCHEDULE

**Why this matters:** Fresh domains have no sending reputation. Email providers are suspicious. Warming builds trust over 4-6 weeks.

**Use a subdomain for bulk email:**
- Marketing email domain: `mail.yourdomain.com` or `news.yourdomain.com`
- Keep your main domain (`yourdomain.com`) clean for transactional emails
- If main domain gets flagged, your other email still works

### Week-by-Week Warming Schedule

**Week 1: 50-100 emails/day**
- Send to your highest-engagement subscribers first
- These are people who have opened your emails before
- If you're brand new: send to people who opted in most recently
- Content: your best content, real value, no offers

**Week 2: 200-500 emails/day**
- Add slightly less engaged subscribers
- Monitor: bounce rate (keep under 2%), spam rate (keep under 0.1%)
- If metrics are clean: proceed to week 3
- If spam rate is 0.1%+: pause and diagnose

**Week 3: 1,000-2,000 emails/day**
- Continue expanding to full list
- Start sending offers (if engagement is good)
- Target: 30%+ open rate in this phase

**Week 4: 5,000-10,000 emails/day**
- Full volume capability
- Normal sending patterns established

**Week 5-6: Full volume**
- Maintain consistent sending cadence
- Never go from 0 to full volume (even on a warmed domain)

### Automated Warming (Instantly.ai)
If you're doing cold email outreach (not newsletter), use Instantly's warmup feature:
- Free with paid plan ($37/mo)
- Automatically sends emails between your accounts + other Instantly users
- They reply to each other, boosting reputation
- Run for 30 days before sending cold outreach campaigns

---

## STEP 3: LIST HYGIENE (Ongoing)

**Problem:** Every unvalidated email on your list is a liability.

**Monthly hygiene checklist:**
1. Remove hard bounces immediately (any bounce over the last 30 days)
2. Remove soft bounce addresses after 3 bounces
3. Remove unsubscribers (should happen automatically)
4. Review and suppress cold segments (60+ days no open)
5. Validate new list additions if imported from external sources

**Bounce rate targets:**
- Hard bounce rate: under 0.5% (domain blocking territory above 2%)
- Soft bounce rate: under 2%

**Tools for list validation (before importing old lists):**
- ZeroBounce: $18 for 2,000 validations
- NeverBounce: $8 per 1,000 credits
- Kickbox: $0.008 per email
- Verify before importing any list you didn't build yourself

**Spam trap detection:**
List cleaning services also flag known spam traps — fake addresses that ISPs use to catch senders with poor hygiene. Sending to even one spam trap tanks deliverability.

---

## STEP 4: CONTENT SIGNALS

Gmail, Outlook, and other providers scan content. These patterns trigger spam filters.

### Spam Trigger Words (Avoid in Subject Lines)
High-risk words:
- "FREE" (caps)
- "winner", "won", "prize"
- "click here", "click below"
- "limited time offer"
- "earn money", "make money fast"
- "100% free"
- "no cost", "no risk"
- "guaranteed"
- "act now"

Lower risk but use sparingly:
- "discount", "sale", "offer"
- "promotion", "deal"
- "buy now", "order now"

### Content Best Practices for Inbox Placement

**Plain-text or minimal HTML:**
- Plain-text emails have the highest inbox placement rate
- If using HTML: keep it simple (1 column, minimal images, <3 colors)
- Heavy HTML with complex layouts → Promotions tab

**Image-to-text ratio:**
- Keep images under 30% of email content
- Never send an email that's mostly one image (spam filter bait)
- Alt text on all images

**Link practices:**
- 1-3 links maximum per email
- No link shorteners (bit.ly, tinyurl) — flag deliverability
- Use your own domain for tracking links
- Never link to domains with poor reputation

**One clear CTA:**
Multiple competing CTAs = spam signals and lower click rate

---

## STEP 5: ENGAGEMENT OPTIMIZATION

Deliverability is engagement-dependent. Low engagement → lower inbox placement → lower engagement (death spiral).

### Engagement Signals Google Tracks

**Positive signals:**
- Open rate (Gmail uses proxy clicks now, not pixel tracking)
- Reply to email
- Click links
- Move to Primary from Promotions
- Add sender to contacts
- Star the email

**Negative signals:**
- Mark as spam
- Delete without opening
- Move to Promotions
- Report as phishing

### Getting the First Email Right
The first email has the highest open rate. Use it to:
1. Set expectations (what they'll get, how often)
2. Deliver immediate value
3. Ask a micro-engagement question ("reply with X")
4. Get them to click something

If they engage with email 1, Gmail learns that your emails are wanted → higher placement going forward.

### The "Reply to This Email" Pattern
Add a question that invites replies in your first 3 emails:
- "reply with your biggest challenge around [TOPIC] and I'll answer it"
- "reply with a number (1, 2, 3) to tell me which direction to take next"
- "any questions? reply and I answer personally"

Replies are the strongest engagement signal Gmail reads.

### Sunset Policy
Subscribers who haven't engaged in 90+ days hurt your sender score.

**Protocol:**
1. 60 days: re-engagement sequence (Seq 6 in email_sequences_10.md)
2. 90 days: one final email, then suppress
3. 120 days: remove from active list
4. 180 days: delete if GDPR-compliant

---

## MONITORING DASHBOARD

**Weekly metrics to track:**

| Metric | Target | Warning | Red Flag |
|---|---|---|---|
| Delivery rate | 98%+ | 96-98% | Under 96% |
| Open rate | 35%+ | 25-35% | Under 25% |
| Click rate | 3%+ | 1-3% | Under 1% |
| Spam complaint rate | Under 0.05% | 0.05-0.1% | Over 0.1% |
| Hard bounce rate | Under 0.3% | 0.3-0.5% | Over 0.5% |
| Unsubscribe rate | Under 0.5% | 0.5-1% | Over 1% |

**Tools to monitor inbox placement:**
- GlockApps: $9/mo — sends test emails, shows inbox vs spam placement per provider
- Mail-Tester.com: free, one-time checks
- MXToolbox: free, DNS and blacklist checks

**Blacklist check (run monthly):**
MXToolbox.com → Blacklist Check → Enter your sending IP
If you're on a shared IP (most ESPs), your ESP manages this.

---

## EMERGENCY DELIVERABILITY FIXES

**Symptoms and causes:**

| Symptom | Likely Cause | Fix |
|---|---|---|
| Sudden drop in open rate | IP blacklisted or reputation hit | Check blacklists, pause sending, diagnose |
| High spam complaints | Wrong audience, too many sends, spam content | Segment list, reduce frequency, review content |
| Emails going to Promotions | HTML-heavy template, multiple links | Switch to plain text, reduce links |
| High bounce rate | Old list, cold list, no validation | List hygiene, ZeroBounce validation |
| Delivery rate drop | SPF/DKIM misconfigured | DNS check, re-verify with MXToolbox |

**If spam complaint rate exceeds 0.1%:**
1. Stop all sends immediately
2. Identify the segment that complained (source tag)
3. Check: did they explicitly opt in? are you sending what they expected?
4. Fix the cause
5. Resume at lower volume

**Google Postmaster Tools:**
Free tool from Google. Shows your domain's spam rate, IP reputation, and authentication status from Gmail's perspective.
Setup: postmaster.google.com → Add your sending domain → Verify ownership via DNS

---

## COMPLETE DNS SETUP CHECKLIST

Before sending ANY email from a new domain:
- [ ] SPF record created and validated
- [ ] DKIM record created and validated
- [ ] DMARC record created (p=none to start)
- [ ] Subdomain configured for bulk sends (mail.yourdomain.com)
- [ ] Google Postmaster Tools set up
- [ ] Warming schedule in place (start Day 1)
- [ ] Test email sent and checked in GlockApps or Mail-Tester.com
- [ ] Unsubscribe link verified (CAN-SPAM requirement)
- [ ] Physical address in email footer (CAN-SPAM requirement)
- [ ] List validation completed if importing any external list
