# Pre-send deliverability checklist

Run through this before every campaign. Skip steps and you land in spam.

## Before writing a single email

### DNS and infrastructure
- [ ] SPF record configured correctly
- [ ] DKIM enabled and authenticated
- [ ] DMARC set up (at least p=none)
- [ ] mail-tester.com score 9/10 or higher
- [ ] No blacklists (check mxtoolbox.com)
- [ ] Domain age at least 2 weeks (ideally 4+)

### Warmup status
- [ ] Inbox warmed for minimum 14 days (21+ preferred)
- [ ] Warmup still running (maintenance mode)
- [ ] Warmup tool shows good engagement (30%+ reply rate)
- [ ] No recent Google/Outlook security warnings

### Sending limits
- [ ] Under 50 cold emails per inbox per day
- [ ] Using inbox rotation across multiple inboxes
- [ ] Delay between emails set (60-180 seconds)
- [ ] Daily volume ramps gradually (not 0 to 500 overnight)

## Email content checks

### Subject line
- [ ] Under 50 characters
- [ ] No ALL CAPS
- [ ] No spam trigger words (free, guarantee, act now, limited time)
- [ ] No excessive punctuation (!!!, ???)
- [ ] Looks like a human wrote it
- [ ] Personalization variable works ({{firstName}} not broken)

### Body copy
- [ ] Under 150 words (ideal: 50-100)
- [ ] No images (images hurt deliverability)
- [ ] No attachments (attachments hurt deliverability)
- [ ] Maximum 1 link (your calendar or website)
- [ ] No link shorteners (bit.ly, tinyurl flag spam filters)
- [ ] No HTML formatting (plain text only)
- [ ] No colored text or fonts
- [ ] Personalization makes sense (not "Hi {{firstName}}")

### Spam trigger words to avoid
- Free, discount, save, limited time
- Act now, urgent, don't miss
- Guaranteed, no obligation, risk-free
- Winner, congratulations, selected
- Click here, click below, click now
- Unsubscribe (yes, counterintuitive but true for cold email)

### Signature
- [ ] Simple text signature (no images)
- [ ] Real name and title
- [ ] Company name
- [ ] Phone number (optional but helps legitimacy)
- [ ] No social media icons
- [ ] No marketing slogans

## List quality checks

### Before importing
- [ ] List is verified (ZeroBounce, NeverBounce, etc.)
- [ ] Bounce rate under 3%
- [ ] No catch-all or role-based emails (info@, sales@, support@)
- [ ] No personal Gmail/Yahoo addresses (B2B only)
- [ ] List is fresh (data less than 90 days old)

### List hygiene
- [ ] Removed duplicates
- [ ] Removed competitors
- [ ] Removed current customers
- [ ] Removed previous bounces
- [ ] Removed unsubscribes from past campaigns

### Targeting quality
- [ ] ICP (ideal customer profile) clearly defined
- [ ] Leads match ICP criteria
- [ ] Company size appropriate for your offer
- [ ] Industry/vertical makes sense
- [ ] Decision-maker level appropriate (not too junior, not CEO of Fortune 500)

## Technical checks before launch

### In your email tool
- [ ] Correct inbox selected
- [ ] Inbox rotation enabled
- [ ] Schedule set (business hours, Mon-Thu optimal)
- [ ] Timezone set correctly
- [ ] Send limit per day configured
- [ ] Tracking enabled (opens/clicks)
- [ ] Custom tracking domain set up (if available)

### Sequence settings
- [ ] Follow-up delays make sense (2-4 days between emails)
- [ ] Total sequence length reasonable (3-5 emails)
- [ ] Reply detection enabled (stops sequence on reply)
- [ ] Auto-labels for replies set up
- [ ] Unsubscribe handling configured

### Test sends
- [ ] Sent test to personal Gmail
- [ ] Sent test to personal Outlook
- [ ] Email renders correctly
- [ ] Personalization variables populate
- [ ] Links work
- [ ] Landed in inbox (not spam/promotions)

## Launch day checks

### Volume ramp
Day 1-3: 20% of target volume
Day 4-7: 50% of target volume
Day 8+: Full volume (if metrics look good)

### Metrics to watch first 48 hours
- [ ] Bounce rate under 3%
- [ ] Open rate above 40%
- [ ] No sudden spike in spam reports
- [ ] No Google/Outlook warnings on inboxes

### Red flags that mean STOP immediately
- Bounce rate over 5%
- Open rate under 20% (deliverability issue)
- Multiple spam complaints
- Inbox locked or suspended
- Warmup emails suddenly going to spam

## Ongoing monitoring

### Daily checks
- [ ] Check reply inbox
- [ ] Respond to interested leads within 4 hours
- [ ] Monitor bounce rate
- [ ] Check for spam complaints

### Weekly checks
- [ ] Run mail-tester.com
- [ ] Check Google Postmaster Tools
- [ ] Review open/reply rates by inbox
- [ ] Rotate out underperforming inboxes
- [ ] Add fresh leads to campaigns

### Monthly checks
- [ ] Full deliverability audit
- [ ] Blacklist check on all domains
- [ ] Inbox health review
- [ ] Domain rotation (rest tired domains)
- [ ] Update ICP based on who's responding

## Emergency procedures

### If deliverability tanks

**Immediate:**
1. Pause all campaigns
2. Check blacklists
3. Check mail-tester score
4. Review bounce reasons

**Recovery:**
1. Stop cold sending for 2 weeks
2. Keep warmup running at high volume
3. Investigate root cause (bad list? spam content?)
4. Fix issue
5. Restart with small volume

### If inbox gets suspended

**Google Workspace:**
1. Don't panic (usually temporary)
2. Follow Google's recovery steps
3. Wait 24-48 hours
4. If permanent, that inbox is burned
5. Remove from tool, don't send from it again

**Burn rate:** Budget for losing 1-2 inboxes per quarter. It happens.

## Quick reference card

**Perfect email checklist:**
- Under 100 words
- Plain text only
- 1 personalization
- 1 link maximum
- No images
- No attachments
- Clear CTA

**Perfect list checklist:**
- Verified emails
- Under 3% bounce rate
- B2B only
- Fresh data
- Matches ICP

**Perfect send checklist:**
- Warmed inbox (14+ days)
- Under 50/day/inbox
- Rotation enabled
- Business hours
- Mon-Thu
