# OPP-005: Content Repurposing Micro-SaaS

**Score:** 8.0/10 (Fit: 9, Effort: 7, ROI: 7)
**Startup Cost:** $0
**Time to First Revenue:** 2 weeks
**Monthly Potential:** $1,500-$5,000
**Competition:** Medium (tools exist but most are expensive or enterprise)

## What

Build a tool that takes one piece of long-form content (blog post, YouTube transcript, podcast) and auto-generates platform-specific versions for Twitter/X, LinkedIn, Instagram, TikTok script, newsletter, and Reddit. 1-to-20 repurposing.

## Why Now

- Hub-and-spoke 1-to-20 repurposing model validated (ALPHA271)
- Creators manually reformatting = hours wasted
- Existing tools (Repurpose.io, Castmagic) charge $30-100/mo but miss platform nuance
- We already do this internally (130 tweets generated, content pipelines built)
- Claude API can handle tone/format transformation at pennies per call
- Digital products market: $124B+ in 2026

## How

1. Simple web app: paste URL or text, select platforms, get formatted output
2. Claude API for intelligent reformatting (not just truncation)
3. Platform-specific templates: Twitter threads, LinkedIn carousels, IG captions, TikTok scripts
4. Export as formatted text or schedule directly via Buffer/Typefully API
5. Price: $19/mo (50 repurposes) or $39/mo (unlimited)

## Expected ROI

- API costs: ~$5-15/mo at 500 repurposes
- 100 users at $29/mo avg = $2,900/mo
- Content marketing drives organic (we create content about content creation)
- Low churn: creators use daily

## First 3 Steps

1. Build MVP: text input -> 6-platform output using Claude API + Next.js frontend
2. Test internally with our own content pipeline for 1 week
3. Launch on Product Hunt + post in creator communities (r/content_marketing, Indie Hackers)

## Stack Fit

Next.js + Claude API + existing content generation infrastructure. We literally built the content pipeline this tool productizes.
