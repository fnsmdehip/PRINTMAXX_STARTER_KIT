---
title: "What's the cheapest way to get sales follow-ups done reliably? | PrintMaxx"
description: "Google Sheets + cron + EmailBison. $27/month. 95% deliverability. No monthly subscription bloat."
keywords: ["sales automation", "email follow-up", "budget", "cheap tools", "solopreneur"]
author: "PrintMaxx Team"
date: "2026-01-22"
published: true
canonical: "/longtail/what-s-the-cheapest-way-to-get-sales-follow-ups-done-reliably"
---

# What's the cheapest way to get sales follow-ups done reliably?

## Quick Answer

Google Sheets (free) + EmailBison ($27/month) + Python cron (free) = complete automation.

Or Airtable ($20/mo) + EmailBison ($27/mo) = $47/month with more features.

Start with Google Sheets version. Upgrade only if it breaks.

## The $27/Month Stack

**Tools:**
- Google Sheets (free) - CRM database
- EmailBison ($27/month) - SMTP with warmup
- Python + cron (free) - Automation script
- Your server or Heroku free tier (free)

**What it does:**
- Track leads in Sheet
- Auto-send follow-ups on schedule
- Track opens/clicks
- 95% deliverability (Yahoo/Gmail respect EmailBison)

## Stack Comparison

| Stack | Cost/Mo | Setup | Reliability | Best For |
|-------|---------|-------|-------------|----------|
| Manual | $0 | None | Low (you forget) | <10/week |
| Google Sheets + EmailBison | $27 | 2 hours | High (95%+) | 50-200/week |
| Airtable + EmailBison | $47 | 3 hours | High (95%+) | 200+/week |
| Zapier + Mailchimp | $50+ | 1 hour | Medium | 100-500/week |

Google Sheets wins on cost. Airtable wins on ease-of-use.

## The $27 Setup: Step by Step

### Step 1: Create Google Sheet (10 min)

```
Columns:
- Name
- Email
- Date added
- Follow-up 1 sent (Y/N)
- Follow-up 2 sent (Y/N)
- Notes
```

### Step 2: Set up EmailBison ($27/month)

Create account at emailbison.com. Get your API key.

Why EmailBison over alternatives:
- Cheap ($27/mo for 10k emails)
- Built-in warmup (avoid spam folder)
- Easy API
- Works with Gmail/Yahoo/Outlook

### Step 3: Write Python script (20 min)

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

# Google Sheets auth
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)
sheet = gc.open('Sales Leads').worksheet(0)

# Get all rows
rows = sheet.get_all_records()

for row in rows:
    if row['Follow-up 1 sent'] == 'N':
        email = row['Email']
        name = row['Name']

        # Send via EmailBison
        requests.post('https://api.emailbison.com/send', json={
            'to': email,
            'subject': f'Quick follow-up, {name}',
            'html': f'<p>Hi {name},<br>Following up on our earlier conversation...</p>'
        }, headers={'Authorization': f'Bearer {API_KEY}'})

        # Mark sent
        sheet.update_cell(row_index, col_index, 'Y')

print('Done')
```

### Step 4: Schedule with cron (10 min)

Run daily at 9am:
```
0 9 * * * /usr/bin/python3 /path/to/follow_up.py
```

Or upload to Heroku free tier, run daily.

**Total setup time: 40 minutes**

## Why Each Tool

**Google Sheets:** Free. Everyone knows it. Good enough for CSVs.

**EmailBison:** Cheap + reliable. Gmail/Yahoo warmup included. Avoids spam folder.

**Python + cron:** Free. No monthly subscription. You own the script.

## When to Upgrade

Upgrade to Airtable ($20/mo) when:
- You need 500+ leads per week
- You want automation triggers (if lead tagged "hot" then auto-reply faster)
- You want better UI than Sheets

Upgrade to Zapier ($50/mo) when:
- You need Zapier integrations (Stripe, Slack, etc)
- You want no-code solution
- You have budget

But start with $27. Seriously.

## Real Example: Follow-Up Sequence

**Day 0:** Lead signs up (added to Sheet)
**Day 1:** First email: "Thanks for signing up"
**Day 3:** Second email: "Here's what I recommend"
**Day 7:** Third email: "Last chance offer"

Script checks Sheet daily. Sends if not sent yet. Marks as sent.

Total active leads at any time: 100
Emails per week: 300
EmailBison cost: $27/month (covers 10k/month)

## Reliability Check

Will it work?

- Google Sheets: 99.9% uptime
- EmailBison: 99.5% uptime + SMTP redundancy
- Cron: 99% if using Heroku or own server

Expected deliverability: 90-95% (some bounces are normal)

## Troubleshooting

**Problem: Emails going to spam**

Solution: EmailBison has built-in warmup. But also:
- Use real sender name (not "Sales Bot")
- Include unsubscribe link
- Keep emails personal (short, conversational)

**Problem: Script stops running**

Solution:
- Check cron logs: `log stream --predicate 'process == "cron"'`
- Use Heroku scheduler instead (more reliable)
- Add error email alerts

**Problem: API quota hit**

Solution: EmailBison limits are generous ($27/mo = 10k emails). You're safe until 10k/month.

## Cost Scaling

| Volume | Stack | Cost |
|--------|-------|------|
| 100/month | Sheets + EmailBison | $27 |
| 1k/month | Sheets + EmailBison | $27 |
| 10k/month | Sheets + EmailBison | $27 |
| 50k/month | Upgrade to EmailBison tier | $99 |

You can handle 10k emails/month on the cheap stack.

## Alternatives if Stuck

**Free:** Just use Gmail + BCC yourself on follow-ups. Manually check spreadsheet. Works but slow.

**$10/mo:** Mailgun SMTP service. More complex setup.

**$50/mo:** ActiveCampaign. Best-in-class. Overkill for MVP.

## Related

- [Best sales follow-ups automation stack in 2026](/longtail/best-sales-follow-ups-automation-stack-in-2026)
- [How to disclose affiliates without killing conversions for sales follow-ups](/longtail/how-to-disclose-affiliates-without-killing-conversions-for-sales-follow-ups)

## Next Steps

1. Create Google Sheet with lead data
2. Sign up for EmailBison ($27/mo)
3. Copy Python script above
4. Test sending 1 email manually
5. Set up cron job
6. Monitor for 1 week
7. Adjust email copy based on open rates
| Notion + n8n | $0-20 | Medium | Tinkerers |
| Airtable + EmailBison | $47 | High | Most solopreneurs |
| Instantly | $97 | High | Scale mode |

## The $27/Month Stack

### Components

1. **Notion (Free)** - Your CRM
2. **n8n (Self-hosted)** - Automation engine
3. **EmailBison ($27/mo)** - Sending

### Setup Steps

**Step 1: Create Notion CRM**
- Name, Email, Company, Status, Last Contact, Next Follow-up

**Step 2: Set Up n8n Workflow**
```
Schedule (daily) -> Query Notion -> Generate Email -> Send -> Update Notion
```

**Step 3: Configure EmailBison**
- Connect domain, warmup 2 weeks, start 20/day

## Follow-Up Sequence Template

### Day 0: Initial Outreach
```
Subject: Quick question about [company]

Saw [specific thing]. Thought [product] might help.

Worth a quick chat?
```

### Day 3: Follow-Up 1
```
Following up. [One sentence value prop].

Open to a 15-min call?
```

### Day 7: Follow-Up 2
```
Last note. If [problem] isn't priority, no worries.

If it is, happy to share how [customer] solved it.
```

### Day 14: Break-Up
```
Haven't heard back. Assuming timing isn't right.

If things change, inbox is open.
```

## FAQ

**Q: Is free Notion reliable for CRM?**
A: Yes for <500 leads.

**Q: Why EmailBison over Instantly?**
A: $70/mo cheaper. API-first.

**Q: How many follow-ups?**
A: 3-4 over 2 weeks. More risks spam complaints.

## When to Upgrade

Move to paid CRM when:
- >500 active leads
- Need team collaboration
- Manual tracking >2 hours/week

## Related Resources

- [Truth Page: Lead Generation](/truth/lead-generation-systems-validation-before-paid-ads)
