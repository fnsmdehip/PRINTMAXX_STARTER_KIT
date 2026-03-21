# Growth Plan: Launched DistillNote - knowledge vault that turns videos/pod

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. Use structured video summaries as Twitter thread content
2. Post 'I summarized X hours of podcasts so you don't have to' engagement bait

## Budget Tier Strategies

### FREE
Process competitor SaaS podcasts through existing auto-clip pipeline, post structured summaries as threads on Twitter/LinkedIn

### LOW
N/A at this tier

### MID
N/A at this tier

## Daily Actions

- [ ] Route video/podcast processing through existing auto-clip pipeline (yt-dlp → whisper → claude -p → structured output)
- [ ] Add KPI task to process 2 competitor videos/week for alpha extraction
- [ ] Feed structured summaries to engagement_bait_converter.py for social content

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "existing auto-clip pipeline + content_repurposer.py"
}
```
