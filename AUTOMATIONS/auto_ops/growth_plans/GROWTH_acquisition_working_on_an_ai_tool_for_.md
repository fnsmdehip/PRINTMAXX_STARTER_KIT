# Growth Plan: [ACQUISITION] Working on an AI tool for Make.com automation.

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo indirect (content → SEO → service leads for automation builds)

---

## Tactics

1. Reply to r/SideProject, r/nocode, r/automation posts asking about Make.com with n8n comparison — link to our comparison content
2. Twitter content: 'I replaced Make.com with n8n and saved $X/mo — here are 5 AI workflows I rebuilt' thread format
3. Scrape r/SideProject for 'Make.com' and 'Zapier' mentions weekly → auto-generate reply drafts via engagement_bait_converter.py
4. Position as cheap alternative: 'Make.com charges per operation, n8n is free self-hosted' — frugal founder angle

## Budget Tier Strategies

### FREE
Reddit reply engagement on Make.com automation posts. Twitter threads via content_repurposer.py. n8n workflow screenshot content (visual, high shareability). Cross-post to r/nocode, r/automation, r/sideproject.

### LOW
$0-20/mo: Boost top-performing n8n comparison tweet. Sponsor 1 automation-focused newsletter issue.

### MID
$50-100/mo: Paid Reddit posts in r/entrepreneur targeting automation buyers. Retarget Make.com search traffic with comparison landing page.

## Daily Actions

- [ ] Route to chain_i_built_31_n8n_workflows_this_month_that — already covers n8n workflow content
- [ ] Run engagement_bait_converter.py on this entry to generate 3 tweets: Make.com vs n8n angle
- [ ] Add weekly cron to scrape r/SideProject + r/nocode for 'Make.com' mentions → queue reply drafts
- [ ] Add KPI entry to track weekly reply engagement on automation threads

## Tooling

```json
{
  "browser": "none",
  "email": "custom cold email scripts",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
