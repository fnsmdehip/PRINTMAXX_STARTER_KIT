# OPP-016: B2B Webinar-to-Clips SaaS

**Score:** 8.3/10 (Fit: 9, Effort: 6, ROI: 8)
**Startup Cost:** $0 (we already built the pipeline)
**Time to First Revenue:** 1 week (productize existing tools)
**Monthly Potential:** $2,000-10,000
**Competition:** Medium (OpusClip, Vidyo exist but expensive and not B2B-focused)

## What

Automatically extract high-engagement clips from B2B webinars and format them for LinkedIn, TikTok, and YouTube Shorts. Marketing managers spend 4-8 hours manually finding and editing clips from each webinar. We automate it to under 10 minutes.

## Why Now

- Identified as "one of the most popular micro SaaS ideas 2026" (Lovable research)
- Solves a direct labor-cost problem for marketing managers
- We ALREADY built the auto-clip pipeline: yt-dlp -> whisper -> Claude -> ffmpeg
- Existing pipeline just needs a frontend and payment layer
- B2B companies run 2-4 webinars/month and need clips for social
- OpusClip charges $19-99/mo but targets creators, not B2B marketing teams
- B2B willingness to pay is 3-5x higher than creator market

## How

1. Wrap existing auto-clip pipeline in a simple Next.js frontend
2. Add Stripe payment: $99/mo (10 webinars) or $249/mo (unlimited)
3. User uploads webinar recording or pastes YouTube URL
4. Pipeline: transcribe -> AI identifies top 5-8 moments -> auto-crop to vertical -> add captions
5. Output: formatted clips with captions for LinkedIn, TikTok, Shorts
6. Launch on ProductHunt + cold email B2B marketing managers

## Expected ROI

- Dev time: 3-5 days (frontend + Stripe, pipeline exists)
- 20 clients at $149/mo avg = $2,980/mo
- 50 clients at $149/mo avg = $7,450/mo
- Zero marginal cost per clip (runs on our infrastructure)
- Upsell: done-for-you clip editing service at $500/webinar

## First 3 Steps

1. Create landing page with demo video showing before (1hr webinar) -> after (5 clips in 10 min)
2. Wrap auto-clip pipeline in Next.js API route with upload form
3. Cold email 30 B2B marketing managers with "we'll clip your last webinar for free" offer

## Stack Fit

Pipeline already built and tested (yt-dlp + whisper + Claude + ffmpeg). Next.js is our primary web stack. Stripe integration is standard. This is literally productizing something we already built for ourselves.
