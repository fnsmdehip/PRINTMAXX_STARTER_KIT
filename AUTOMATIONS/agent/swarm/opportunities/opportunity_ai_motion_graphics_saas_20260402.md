# AI Motion Graphics / Video Template SaaS

## What
A web app that generates animated motion graphics (logo reveals, social media intros, data visualizations, product showcases) from text prompts using Remotion + Claude API. Users describe what they want, AI generates the Remotion code, renders the video.

## Why Now
- FrameNet (AI motion graphics maker) hit $6K revenue in 3 months per r/microsaas post this week (282 upvotes). Proof that this exact category converts.
- In-house video production post on r/SAAS showed companies saving $5K-15K/quarter by bringing video production in-house. AI-generated motion graphics is the next step.
- r/slavelabour shows demand for "basic video editing/content creation -- $150-200/mo" and "TikTok slideshows -- $4/post". These buyers would switch to $29/mo self-serve tool.
- Three.js 3x growth in one year (421 upvotes on r/webdev) indicates exploding demand for web-based visual/animation tools.
- We already have Remotion (React video) in our media pipeline. This is extending existing capability into a product.
- The "building apps is the new starting a podcast" post (144 upvotes r/Entrepreneur) signals that TOOLS for creators are the meta-play, not building yet another app.

## How to Execute
1. Build a Next.js frontend where users describe their video (e.g., "logo reveal for a dental clinic, blue and white, professional, 5 seconds")
2. Claude API generates Remotion component code from the description
3. Remotion renders the video server-side (Lambda or local)
4. User downloads MP4 or gets embed code
5. Freemium: 3 free renders/month, $29/mo for unlimited

## Stack
Next.js (frontend), Claude API (code generation), Remotion (video rendering), Vercel (hosting), AWS Lambda or Render (video processing), Stripe ($29/mo subscription)

## Startup Cost
$20-50 (Render for video processing, everything else on free tiers)

## Time to First Revenue
10-14 days. The core loop (prompt -> Claude generates Remotion code -> render -> MP4) can be built in a weekend. Polish the UI and add billing in week 2.

## Monthly Potential
$2,000-8,000. FrameNet hit $2K/mo in month 3 at a similar price point. At $29/mo with 69-276 subscribers. The $4/post TikTok slideshow market alone represents hundreds of potential customers who would prefer self-serve at $29/mo.

## Competition
LOW-MEDIUM. FrameNet exists but is early-stage. Canva has motion graphics but not AI-generated custom code. Pika/Runway do AI video but not structured motion graphics (logo reveals, data viz). The niche is "structured, branded motion graphics from text" -- not general AI video generation.

## First 3 Steps
1. TODAY: Build proof of concept -- Claude API prompt that takes a text description and outputs valid Remotion component code. Test with 5 different motion graphic types (logo reveal, text animation, data chart, product showcase, social media intro).
2. DAYS 2-5: Build Next.js app with prompt input, Claude code generation, Remotion server-side render, video download. Use Remotion Lambda for rendering (pay-per-render, ~$0.01-0.05 per video).
3. DAYS 6-10: Add Stripe billing ($29/mo), deploy to Vercel, create 10 example videos as marketing material, launch on Product Hunt and post to r/SideProject with "I built an AI that generates professional motion graphics in 30 seconds."

## Score: 8.0/10
- Market Size: 8 (every business needs video content)
- Speed to Revenue: 7 (needs 10-14 days of building)
- Automation Potential: 9 (fully automated generation pipeline)
- Stack Fit: 9 (Remotion already in our stack, Claude API, Next.js)
- Low Competition: 7 (FrameNet exists but market is nascent)
