# Campaign tracking setup

How to track cold outbound campaigns for optimization and ROI measurement.

## What to track

### Email metrics (per campaign)

**Volume metrics:**
- Emails sent
- Emails delivered (sent - bounces)
- Delivery rate (delivered / sent)

**Engagement metrics:**
- Opens (unique)
- Open rate (opens / delivered)
- Clicks (if using links)
- Click rate (clicks / delivered)

**Response metrics:**
- Total replies
- Reply rate (replies / delivered)
- Positive replies
- Positive reply rate
- Negative replies / objections
- Unsubscribes

**Conversion metrics:**
- Meetings booked
- Meeting rate (meetings / delivered)
- Opportunities created
- Deals closed
- Revenue generated

### LinkedIn metrics

**Connection metrics:**
- Connection requests sent
- Connections accepted
- Acceptance rate (accepted / sent)

**Message metrics:**
- Messages sent
- Messages replied
- Reply rate (replied / sent)
- Conversations started

**Conversion metrics:**
- Meetings from LinkedIn
- Opportunities from LinkedIn

### Overall funnel metrics

- Total prospects contacted (all channels)
- Total responses
- Total meetings
- Opportunities created
- Deals closed
- Revenue generated
- Cost per meeting
- Cost per customer acquired
- ROI (revenue / costs)

## Tracking tools

### Built-in email tool tracking

**Instantly, Smartlead, etc. provide:**
- Open tracking (pixel-based)
- Click tracking
- Reply detection
- Campaign dashboards

**Limitations:**
- Apple Mail Privacy Protection blocks open tracking
- Some email clients block tracking pixels
- True open rates may be 10-20% higher than reported

### CRM integration

**HubSpot, Pipedrive, Salesforce:**
- Track full funnel from email to close
- Associate revenue with campaigns
- Multi-touch attribution

**Setup:**
- Sync email tool with CRM
- Create deal stages for outbound leads
- Tag leads by campaign source

### Spreadsheet tracking (manual but works)

If you don't have CRM, track in Google Sheets:

**Campaign tracker template:**

| Campaign | Sent | Delivered | Opens | Open Rate | Replies | Reply Rate | Meetings | Revenue |
|----------|------|-----------|-------|-----------|---------|------------|----------|---------|
| Campaign A | 500 | 485 | 265 | 54.6% | 28 | 5.8% | 4 | $15K |
| Campaign B | 500 | 490 | 210 | 42.9% | 15 | 3.1% | 2 | $8K |

**Lead tracker template:**

| Name | Company | Email | Campaign | Sent Date | Opens | Replied | Reply Date | Status | Notes |
|------|---------|-------|----------|-----------|-------|---------|------------|--------|-------|
| John | Acme | john@acme.com | Campaign A | 1/15 | 3 | Yes | 1/17 | Meeting booked | |

## Setting up tracking

### Step 1: Define your funnel stages

**Standard outbound funnel:**
1. Prospect (in list, not yet contacted)
2. Contacted (email/LinkedIn sent)
3. Engaged (opened, clicked, viewed profile)
4. Replied (any response)
5. Interested (positive response)
6. Meeting Scheduled
7. Meeting Completed
8. Opportunity (qualified, proposal sent)
9. Negotiation
10. Closed Won / Closed Lost

### Step 2: Set up tracking in email tool

**Instantly setup:**
1. Enable open tracking
2. Enable link tracking (if using links)
3. Set up tags for different campaigns
4. Configure reply detection
5. Set up webhook for CRM sync (optional)

**Smartlead setup:**
1. Same as above
2. Use built-in analytics dashboards
3. Export data regularly for analysis

### Step 3: Set up tracking in CRM (optional)

**If using CRM:**
1. Create custom field for "Source" = Cold Outbound
2. Create field for "Campaign Name"
3. Set up deal pipeline for outbound leads
4. Create dashboard for outbound metrics

### Step 4: Create reporting cadence

**Daily:**
- Check replies
- Review bounce rates
- Monitor for deliverability issues

**Weekly:**
- Campaign performance review
- Update tracking spreadsheet
- A/B test analysis

**Monthly:**
- Full funnel analysis
- ROI calculation
- Optimization planning

## Attribution tracking

### Single-touch attribution (simple)

Credit the first touch:
- Lead came from Campaign A → Campaign A gets credit

### Multi-touch attribution (more accurate)

For multi-channel outreach:

**First touch:** Which campaign introduced them?
**Last touch:** What converted them to meeting?
**Multi-touch:** Weight all touchpoints

**Example:**
- Day 1: Email #1 (first touch)
- Day 3: Email #2
- Day 5: LinkedIn connection (converted to reply)
- Day 7: Email #3
- Day 10: Meeting booked from LinkedIn message (last touch)

**Attribution options:**
- First touch: Email Campaign X
- Last touch: LinkedIn Campaign Y
- Even split: 50% email, 50% LinkedIn
- Time decay: More weight on touches closer to conversion

### Practical approach

For most solopreneurs:
- Track both email and LinkedIn separately
- Credit the channel that got the reply/meeting
- Don't overthink attribution

## UTM tracking for links

If you include links in cold emails (not recommended for deliverability, but sometimes needed):

### UTM parameter structure:
```
https://yoursite.com?utm_source=cold_email&utm_medium=email&utm_campaign=saas_demo_jan25
```

**Parameters:**
- utm_source: cold_email
- utm_medium: email
- utm_campaign: [campaign name]
- utm_content: [optional - for A/B testing]

### View in Google Analytics:
1. Go to Acquisition > Campaigns
2. Filter by source = cold_email
3. See traffic and conversions by campaign

## Cost tracking

### What to track:

**Fixed costs:**
- Email tool (Instantly, etc.): $/month
- Sales Navigator: $/month
- Verification tools: $/month
- Domains/inboxes: $/month

**Variable costs:**
- Lead data (Apollo credits, etc.)
- Verification per email
- VA time (if applicable)

### ROI calculation:

```
Monthly costs:
- Instantly: $97
- Sales Navigator: $99
- Apollo: $79
- Domains/Workspace: $100
- Verification: $20
Total: $395/month

Monthly results:
- Meetings booked: 15
- Customers closed: 3
- Revenue: $15,000

ROI: $15,000 / $395 = 38x return
Cost per meeting: $395 / 15 = $26.33
Cost per customer: $395 / 3 = $131.67
```

## Dashboards

### Essential dashboard view

**Daily snapshot:**
- Emails sent yesterday
- Opens yesterday
- Replies received
- Meetings booked
- Any warnings/issues

**Weekly rollup:**
- Total sent
- Open rate
- Reply rate
- Positive reply rate
- Meetings booked
- Pipeline value created

**Monthly summary:**
- Full funnel metrics
- Campaign comparison
- ROI calculation
- Trend vs previous month

### Building in Google Sheets

Create tabs for:
1. **Raw Data:** All campaign data
2. **Campaign Comparison:** Side-by-side metrics
3. **Weekly Dashboard:** Automated calculations
4. **Monthly Summary:** Higher-level view

### Using Looker Studio (free)

1. Connect to Google Sheets
2. Build visual dashboard
3. Auto-refreshes with data updates
4. Share with team if needed

## Common tracking mistakes

1. **Not tracking at all** - Can't improve what you don't measure
2. **Tracking vanity metrics only** - Opens don't pay bills
3. **Not connecting to revenue** - Need full funnel view
4. **Inconsistent tracking** - Gaps make analysis impossible
5. **Overcomplicating** - Simple tracking > no tracking
6. **Not reviewing data** - Tracking is useless without action

## Quick start tracking setup

### Minimum viable tracking (30 min setup):

1. **Create Google Sheet** with columns:
   - Campaign name
   - Date range
   - Emails sent
   - Opens
   - Replies
   - Meetings
   - Notes

2. **Update weekly** from email tool dashboards

3. **Calculate rates:**
   - Open rate = Opens / Sent
   - Reply rate = Replies / Sent
   - Meeting rate = Meetings / Sent

4. **Review monthly** for patterns and optimization opportunities

### Level 2 (CRM integration):

1. Add HubSpot or Pipedrive (free tiers available)
2. Sync email tool to CRM
3. Track deals through pipeline
4. Connect revenue to campaigns

### Level 3 (full stack):

1. CRM with full pipeline
2. Multiple attribution models
3. Automated dashboards
4. Revenue forecasting from outbound metrics
