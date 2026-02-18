# Account creation checklist

Step-by-step setup for each revenue platform. Do these in priority order: Stripe first (blocks all payments), then Gumroad (9 products ready), then Twitter/X (distribution), then the rest in parallel.

Track progress: `python3 scripts/account_tracker.py status`
See blockers: `python3 scripts/account_tracker.py blockers`

---

## 1. Stripe (DO FIRST - blocks all payments)

**Email:** Use your primary business email
**Time:** 15 min setup, 2-3 days for verification

- [ ] Go to stripe.com, click "Start now"
- [ ] Use business email (not a throwaway - this is your payment backbone)
- [ ] Select "Individual / Sole proprietor"
- [ ] Enter legal name, DOB, SSN (required for payouts)
- [ ] Add bank account for payouts
- [ ] Set payout schedule to "daily" (fastest cash flow)
- [ ] Enable test mode and run a $1 test charge
- [ ] Verify identity (upload ID if prompted)
- [ ] Wait for verification (usually 24-48 hours)

**After verified:**
```bash
python3 scripts/account_tracker.py add --platform Stripe --username primary --email <your-email> --status ACTIVE
```

---

## 2. Gumroad (9 products ready to list)

**Email:** printmaxxer@protonmail.com (or primary business email)
**Profile pic:** Logo or professional headshot
**Bio:** "I build tools and systems for [niche]. Free and paid resources."
**Time:** 30 min setup + 20 min per product listing

### Account setup

- [ ] Go to gumroad.com, click "Start selling"
- [ ] Sign up with business email
- [ ] Go to Settings > Profile
  - [ ] Display name: PRINTMAXXER (or niche-specific name)
  - [ ] Bio: 1-2 sentences about what you sell. No fluff.
  - [ ] Profile pic: 400x400px, clean logo or headshot
  - [ ] Cover image: 1500x500px banner with value prop
- [ ] Go to Settings > Payments
  - [ ] Connect Stripe account (from step 1)
  - [ ] Verify payout method
- [ ] Go to Settings > Profile > Custom URL
  - [ ] Set to gumroad.com/printmaxxer (or niche name)

### First product listing

- [ ] Click "New Product"
- [ ] Product name: Clear, benefit-oriented (e.g., "Solopreneur Revenue Tracker - Notion Template")
- [ ] Price: Start at $0+ (pay what you want) for first product to get reviews, or $4.99-$19.99 for premium
- [ ] Description: Problem > Solution > What's included > Social proof
- [ ] Upload product file (PDF, Notion link, zip)
- [ ] Add 3-5 product images / mockups
- [ ] Add tags (Gumroad uses these for discovery)
- [ ] Set "Offer code" for launch discount (e.g., LAUNCH50 for 50% off)
- [ ] Publish

### Warmup (Days 2-5)

- [ ] Day 2: Upload 2 more products
- [ ] Day 3: Share links on Twitter, relevant subreddits, Discord servers
- [ ] Day 4: Share on second platform (LinkedIn, Facebook groups)
- [ ] Day 5: Ask early buyers for reviews. Offer free product for honest review.

**Track:**
```bash
python3 scripts/account_tracker.py add --platform Gumroad --username printmaxxer --email <email> --status CREATED
```

---

## 3. Twitter/X (primary distribution)

**Email:** printmaxxer@protonmail.com (main brand) or niche-specific emails
**Profile pic:** Logo (512x512px minimum) or AI-generated professional headshot
**Bio format:** "[What you do] | [Proof/numbers] | [CTA - link to product/newsletter]"
**Time:** 15 min setup + 30 min/day engagement

### Account setup

- [ ] Create account at x.com
- [ ] Verify email
- [ ] Profile pic: Crisp, recognizable at small size. Logo or face.
- [ ] Banner: 1500x500px. Include value prop or product showcase.
- [ ] Bio: Max 160 chars. Example: "building in public. shipping apps, content systems, and digital products. $0 to $10K/mo arc. free resources below"
- [ ] Location: Optional. "Internet" or real city.
- [ ] Website: Link to Gumroad, newsletter, or landing page
- [ ] Pinned tweet: Best performing tweet OR product launch thread
- [ ] Switch to Professional account (free, gives analytics)

### Initial content (before engaging)

- [ ] Write 5 tweets ready to post (use content from AUTOMATIONS/content_posting/)
- [ ] Write 1 thread (5-7 tweets) about what you're building
- [ ] Schedule first week of content using Buffer or TweetDeck

### Warmup (Days 2-7)

- [ ] Day 2-3: Follow 50 relevant accounts in your niche. Like and RT 20+ tweets. Post 2 tweets.
- [ ] Day 4-5: Post 3-5 tweets/day. Reply to 15 accounts with real value (not "great post").
- [ ] Day 6-7: Post 5 tweets. Run first thread. Quote tweet 2-3 posts with added insight.
- [ ] Day 8+: ACTIVE. 5+ tweets/day, daily engagement, weekly threads.

**Engagement rules:**
- Never post generic replies ("Great post!", "So true!")
- Add value in every reply (data, personal experience, follow-up question)
- Reply to accounts slightly larger than yours (10x your size, not 1000x)
- Quote tweet > retweet (more visibility)

**Track:**
```bash
python3 scripts/account_tracker.py add --platform "Twitter/X" --username @PRINTMAXXER --email printmaxxer@protonmail.com --status CREATED --niche Meta
```

---

## 4. Fiverr (freelance arbitrage - 30 services ready)

**Email:** Business email (separate from personal)
**Profile pic:** Professional headshot (AI-generated is fine, use consistent identity)
**Bio:** Focus on results and speed. "I deliver [service] in [timeframe]. [X] clients served."
**Time:** 45 min setup + 15 min per gig

### Account setup

- [ ] Go to fiverr.com, click "Become a Seller"
- [ ] Sign up with business email
- [ ] Complete profile:
  - [ ] Professional photo (clear face, neutral background, good lighting)
  - [ ] Display name: Professional, not meme-y
  - [ ] Description: 2-3 short paragraphs. Lead with results, not credentials.
  - [ ] Languages: English (Native/Fluent)
  - [ ] Skills: Add all relevant skills (Fiverr uses these for search)
  - [ ] Education: Optional but helps trust
  - [ ] Certifications: Add any relevant ones

### First 3 gigs (create all on Day 1)

For each gig:
- [ ] Title: "[I will] + [specific deliverable] + [for whom]" (e.g., "I will design a professional Notion dashboard for your business")
- [ ] Category: Pick the most specific subcategory
- [ ] Tags: Use all 5 tag slots. Research what buyers search for.
- [ ] Pricing: 3 tiers
  - Basic: Low price entry ($5-15). Minimal deliverable.
  - Standard: Main offer ($25-50). Full deliverable.
  - Premium: Upsell ($75-150). Full deliverable + extras.
- [ ] Description: Problem > Solution > What's included > Delivery time
- [ ] Requirements: What you need from the buyer (be specific to reduce revisions)
- [ ] Gallery: 3 images minimum. Show example deliverables. Before/after if applicable.
- [ ] FAQ: 3-5 common questions
- [ ] Publish

### Warmup (Days 2-7)

- [ ] Day 2-3: Create 4 more gigs (total 7)
- [ ] Day 4-5: Check Buyer Requests daily. Apply to 5+ with personalized proposals.
- [ ] Day 6-7: Share gig links on social. Post on r/forhire. Offer first order at discount for review.
- [ ] Day 8+: ACTIVE. Daily buyer request applications.

**Track:**
```bash
python3 scripts/account_tracker.py add --platform Fiverr --username <handle> --email <email> --status CREATED
```

---

## 5. Upwork (higher-ticket freelance)

**Email:** Business email
**Profile pic:** Same as Fiverr (professional headshot)
**Bio:** Results-oriented. Include specific numbers. "Helped X clients achieve Y."
**Time:** 1 hour setup (profile is more detailed than Fiverr)

### Account setup

- [ ] Go to upwork.com, click "Sign Up" as freelancer
- [ ] Sign up with business email
- [ ] Complete profile:
  - [ ] Professional title: Specific, not generic. "AI Automation Specialist" not "Freelancer"
  - [ ] Profile overview: 3-4 paragraphs.
    - Para 1: What you do and who you help (lead with value)
    - Para 2: Specific results or experience
    - Para 3: Your process (makes client feel safe)
    - Para 4: CTA ("Message me about your project")
  - [ ] Hourly rate: Start $25-40/hr (raise after first 5 reviews)
  - [ ] Skills: Add 10+ relevant skills
  - [ ] Portfolio: Upload 3-5 work samples (create samples if needed)
  - [ ] Employment history: Optional but helps
  - [ ] Education: Add if relevant

### Profile optimization tips

- [ ] Profile 100% complete (Upwork ranks complete profiles higher)
- [ ] Add a 30-second intro video (optional but boosts applications by 2x)
- [ ] Specialized profiles: Create 2-3 for different service categories
- [ ] Availability badge: Set to "Available now"
- [ ] Response time: Reply to messages within 1 hour during business hours

### Warmup (Days 2-7)

- [ ] Day 2: Apply to 5 jobs. Personalize every proposal. Reference specific details from the job post.
- [ ] Day 3: Apply to 5 more. Adjust based on responses.
- [ ] Day 4-5: Apply to 5/day. Consider lower rate for first 2 jobs to build reviews.
- [ ] Day 6-7: Apply to 5/day. Check for invitations. Refine profile.
- [ ] Day 8+: ACTIVE. Daily applications, raise rates after 3+ reviews.

**Proposal template:**
```
Hi [name],

[1 sentence showing you read the job post and understand the problem]

I can [specific deliverable] by [date]. Here's what I'd do:
1. [Step 1]
2. [Step 2]
3. [Step 3]

[1 sentence about relevant experience or similar project]

Happy to discuss details.
[Name]
```

**Track:**
```bash
python3 scripts/account_tracker.py add --platform Upwork --username <handle> --email <email> --status CREATED
```

---

## 6. Fanvue (AI influencer - primary platform)

**Email:** Dedicated email for this brand (not your personal)
**Profile pic:** AI-generated persona image (consistent character, use LoRA-trained model)
**Bio:** Persona-specific. Seductive but not explicit in bio. Tease, don't reveal.
**Time:** 30 min setup + 1 hour content upload

### Account setup

- [ ] Go to fanvue.com, click "Become a Creator"
- [ ] Sign up with dedicated email
- [ ] Verify identity (Fanvue requires ID verification)
- [ ] Complete profile:
  - [ ] Display name: Persona name
  - [ ] Profile pic: Best AI-generated image (face, high quality, consistent character)
  - [ ] Banner: 1920x480px. Lifestyle/aesthetic image matching persona.
  - [ ] Bio: 2-3 sentences. Personality + what subscribers get. Include "AI-generated" disclosure (FTC compliance).
  - [ ] Location: Optional (can be fictional for AI personas if disclosed)

### Tier setup (do on Day 1)

- [ ] Tier 1 - "Peek" ($9.99/mo):
  - Access to feed
  - Weekly posts
  - Basic chat
- [ ] Tier 2 - "VIP" ($24.99/mo):
  - Everything in Peek
  - Exclusive content
  - Priority DMs
  - Weekly drops
- [ ] Tier 3 - "Elite" ($49.99/mo):
  - Everything in VIP
  - Custom content requests
  - Direct chat access
  - Early access to new content
- [ ] Set up tip menu ($5, $10, $25, $50, $100 increments)
- [ ] Enable PPV messaging

### Content upload (Day 1-2)

- [ ] Upload 10 teaser posts:
  - 5 free posts (visible to non-subscribers, drives signups)
  - 5 locked posts (visible preview, full content behind paywall)
- [ ] Each post: Compelling caption, relevant hashtags, consistent character
- [ ] Pin your best free post (this is what new visitors see first)

### Warmup (Days 3-5)

- [ ] Day 3: Cross-promote on Twitter/X. Post teaser images with Fanvue link in bio.
- [ ] Day 4: Post 3-5 new pieces. Engage with any subscribers via DM.
- [ ] Day 5: Cross-promote on Reddit (relevant subs). Run limited promo pricing.
- [ ] Day 6+: ACTIVE. Daily posts, DM engagement, weekly PPV drops.

**Compliance reminder:**
- [ ] "AI-generated content" clearly disclosed in bio
- [ ] FTC disclosure on any sponsored/affiliate content
- [ ] Age-gated content properly marked
- [ ] No impersonation of real people

**Track:**
```bash
python3 scripts/account_tracker.py add --platform Fanvue --username <persona-name> --email <email> --status CREATED --niche AI
```

---

## 7. Fansly (AI influencer - backup/secondary platform)

**Email:** Same dedicated email as Fanvue or separate
**Profile pic:** Same AI persona (cross-platform consistency)
**Bio:** Same as Fanvue with platform-specific link
**Time:** 20 min setup (copy structure from Fanvue)

### Account setup

- [ ] Go to fansly.com, click "Become a Creator"
- [ ] Sign up with dedicated email
- [ ] Verify identity
- [ ] Complete profile (mirror Fanvue setup):
  - [ ] Display name: Same persona name
  - [ ] Profile pic: Same as Fanvue
  - [ ] Banner: Same or variation
  - [ ] Bio: Same + "AI-generated" disclosure

### Tier setup (mirror Fanvue)

- [ ] Tier 1 - "Peek" ($9.99/mo)
- [ ] Tier 2 - "VIP" ($24.99/mo)
- [ ] Tier 3 - "Elite" ($49.99/mo)
- [ ] Tip menu enabled
- [ ] PPV messaging enabled

### Content upload

- [ ] Upload same 10 teaser posts as Fanvue (or slight variations)
- [ ] Pin best free post
- [ ] Cross-link: Mention Fanvue in Fansly bio and vice versa

### Warmup (Days 3-5)

- [ ] Same warmup as Fanvue
- [ ] Stagger posting times (don't duplicate exact same content at exact same time)
- [ ] Day 6+: ACTIVE

**Track:**
```bash
python3 scripts/account_tracker.py add --platform Fansly --username <persona-name> --email <email> --status CREATED --niche AI
```

---

## 8. TikTok (content farm - 3 niches)

**Email:** Niche-specific emails
**Profile pic:** Niche-specific (logo for brand accounts, face for personal accounts)
**Bio:** "[What the account is about] | [CTA] | Link in bio"
**Time:** 15 min setup + 30 min/day content creation

### Account setup

- [ ] Download TikTok or go to tiktok.com
- [ ] Create account with niche email
- [ ] Switch to Business Account (free, gives analytics)
- [ ] Complete profile:
  - [ ] Username: Niche-specific, memorable, same across platforms
  - [ ] Display name: Clean, recognizable
  - [ ] Profile pic: 200x200px, clear at small size
  - [ ] Bio: 80 chars max. What + For whom + CTA.
  - [ ] Link: Linktree or direct to product/newsletter

### Content strategy (before posting)

- [ ] Research 10 trending sounds in your niche
- [ ] Save 20 videos to "inspiration" collection
- [ ] Plan first 7 videos (1 per day minimum)
- [ ] Video format: Hook (first 1 sec) > Value (5-15 sec) > CTA (last 2 sec)
- [ ] Keep videos under 30 seconds initially (higher completion rate)

### Warmup (Days 1-14)

- [ ] Day 1: Set up account. Watch 50+ videos in niche (trains algorithm).
- [ ] Day 2-3: Watch, like, comment on 30+ videos. Follow 20 creators.
- [ ] Day 4-7: Post 1-2 videos/day. Use trending sounds. Engage with comments.
- [ ] Day 8-14: Post 2-3 videos/day. Test different hooks. Duet/stitch trending videos.
- [ ] Day 15+: ACTIVE. 3x/day posting. Analyze what works, double down.

**Repeat for each niche account (faith, fitness, AI).**

**Track:**
```bash
python3 scripts/account_tracker.py add --platform TikTok --username @<handle> --email <email> --status CREATED --niche <niche>
```

---

## Priority order summary

| Priority | Platform | Why | Time to active |
|----------|----------|-----|----------------|
| 1 | Stripe | Blocks ALL payments | 2-3 days (verification) |
| 2 | Gumroad | 9 products ready, fastest to revenue | 5-6 days |
| 3 | Twitter/X | Primary distribution, blocks content ops | 7-8 days |
| 4 | Fiverr | 30 services ready, passive income | 7-8 days |
| 5 | Upwork | Higher ticket freelance | 7-8 days |
| 6 | Fanvue | AI findom (10 personas ready) | 5-6 days |
| 7 | Fansly | Backup to Fanvue | 5-6 days |
| 8 | TikTok | Content farm (longer warmup) | 14-15 days |

**Do 1-3 on Day 1.** Start 4-8 on Day 2 (run in parallel). Track everything:

```bash
python3 scripts/account_tracker.py status
python3 scripts/account_tracker.py warmup
python3 scripts/account_tracker.py blockers
```
