---
title: "What's the cheapest way to get sales follow-ups done reliably | PRINTMAXX"
description: "Automate sales follow-ups without breaking budget. Tools and tactics that actually work for solopreneurs."
keywords: ["sales automation", "follow-ups", "cost", "solopreneur"]
author: "PrintMaxx Team"
date: "2026-01-20"
published: true
canonical: "/longtail/cost-sales-follow-ups-cheapest-way"
---

# What's the cheapest way to get sales follow-ups done reliably

Sales follow-ups kill conversions. Most deals close on the 5th touch. Most solopreneurs quit after the 2nd.

Automation fixes this. But most tools cost $100+/month.

Here's the $0-30/month route that works.

## The stack

**Email platform:** Mailgun or SendGrid. $0 for up to 10k emails/month. That's 200+ follow-ups weekly.

**Scheduling:** Cron jobs (built into any Linux server). Free.

**Trigger logic:** Simple CSV + Python script. Write it once, runs forever.

**Tracking:** Sheets or Airtable free tier. Manual status updates take 5 minutes weekly.

Total cost: $0-10/month for hosting.

## The workflow

1. Add prospect to CSV with email + date of first touch
2. Script checks if 48 hours have passed
3. Script sends follow-up #1
4. Next script run (3 days later) sends follow-up #2
5. Repeat until reply or max follow-ups hit

Takes 4 hours to build. Runs forever.

## Real numbers

You close $500 deals. Your close rate is 20% normally. With 5-touch automation, it's 35%.

50 prospects per month:
- Without automation: 10 deals × $500 = $5,000
- With automation: 17.5 deals × $500 = $8,750

You gain $3,750 monthly. The script cost: $0.

## The code (Python)

```python
import csv
from datetime import datetime, timedelta
import sendgrid
from sendgrid.helpers.mail import Mail

# Read prospect list
with open('prospects.csv') as f:
    for row in csv.DictReader(f):
        last_touch = datetime.fromisoformat(row['last_touch'])
        if datetime.now() - last_touch > timedelta(days=3):
            # Send follow-up
            send_email(row['email'], row['name'])
            # Update timestamp
```

That's the core. Expand as needed.

## Tools you already have

- Gmail SMTP: works with SendGrid
- Google Sheets: track follow-ups
- GitHub: version your script (free)
- Your laptop: runs cron jobs

No new subscriptions needed.

## Common failures

**Failure 1: Script breaks.** Email provider changes API. Script stops silently. Fix: add error logging. Email yourself when it fails.

**Failure 2: Follow-ups feel robotic.** Generic "checking in" emails convert at 2%. Personalized follow-ups convert at 8%. Spend time on personalization templates, not platforms.

**Failure 3: No tracking.** You send 5 follow-ups. You don't know which one converted. Add one column to your CSV: "converted_at". Check it weekly.

## When to upgrade

Switch to Pipedrive or Close ($50+/month) when:
- You're managing 3+ SDRs (coordination overhead)
- You need CRM features (deal stages, forecasting)
- Manual tracking becomes 5+ hours/week

Until then, code + Mailgun wins.

## Timeline to results

**Week 1:** Build the script, test on 5 prospects
**Week 2:** Scale to 30 prospects, track results
**Week 3:** Modify templates based on what converts
**Week 4:** Run at full capacity, measure revenue impact

Most see 20% conversion lift by week 4.

## Action this week

1. Export your current prospect list
2. Add columns: last_touch, follow_up_count, status
3. Pick 10 prospects for manual follow-ups
4. Track open rates and replies
5. After week 1, start building the script

Cheap sales automation works. It just requires one day of your time upfront.
