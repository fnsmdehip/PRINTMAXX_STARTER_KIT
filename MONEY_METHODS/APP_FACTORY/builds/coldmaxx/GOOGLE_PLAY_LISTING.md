# ColdMaxx — Google Play Listing

## App Name (50 chars max)
ColdMaxx: Cold Email Writer

## Short Description (80 chars max)
Write cold emails that get replies. AIDA, PAS & BAB frameworks in 30 seconds.

## Full Description (4000 chars max)

**Cold emails that get replies. 3 proven copywriting frameworks. 30 seconds.**

Most cold emails get ignored because they sound like templates. ColdMaxx uses battle-tested copywriting frameworks — AIDA, PAS, and BAB — to generate personalized, high-converting outreach emails that don't read like spam.

**3 FRAMEWORKS**

► AIDA (Attention → Interest → Desire → Action) — the classic framework that works across every industry
► PAS (Problem → Agitate → Solution) — highest-converting framework for pain-point-driven outreach
► BAB (Before → After → Bridge) — best for results-oriented pitches

**FEATURES**

✓ Generate 3 email variants simultaneously
✓ Subject line generator — 5 options per campaign
✓ Follow-up sequence builder (3-email chain)
✓ Spam word checker — flags terms that kill deliverability
✓ Read time + word count estimator
✓ One-tap copy to clipboard
✓ Save templates for repeat campaigns
✓ Industry subject line swipe library
✓ 100% offline — no API calls, no server

**WHO USES IT**

• Founders doing cold outreach
• Agency owners landing clients
• Sales reps crushing quota
• Freelancers pitching cold
• Anyone who wants more email replies

**PRIVATE**

No account. No data sent anywhere. Your prospect info stays on your device.

---

Pick a framework. Fill in your offer. Get your email in 30 seconds.

## Category
Business

## Content Rating
Everyone

## Price
Free

## Privacy Policy URL
https://coldmaxx.surge.sh/privacy-policy.html

## Feature Graphic (1024x500px)
Design: Dark navy background (#0f0f1a), "ColdMaxx" in large indigo text, a mock email card on the right showing AIDA framework, tagline "Cold emails that actually get replies"

## Screenshots (1080x1920px)
1. Framework selector (AIDA/PAS/BAB)
2. Email generation form
3. 3 generated email variants
4. Subject line generator
5. Spam checker view
6. Follow-up sequence

## Submission Method (TWA recommended)
```bash
# 1. Deploy to HTTPS
npx surge . coldmaxx.surge.sh

# 2. Convert SVG icon to PNG
# Use: https://svgtopng.com or Inkscape:
# inkscape icon-1024.svg -o icon-1024.png -w 1024 -h 1024

# 3. Update manifest.json to use PNG icons instead of SVG data URIs

# 4. Init TWA with Bubblewrap
npx @bubblewrap/cli init --manifest https://coldmaxx.surge.sh/manifest.json

# 5. Build APK
bubblewrap build

# 6. Upload to Play Console as Internal Test first
```

## TWA Checklist
- [ ] Deployed to HTTPS (surge.sh or custom domain)
- [ ] Icons converted to PNG (not SVG data URIs)
- [ ] assetlinks.json configured
- [ ] Play Console developer account created ($25 one-time)
