# AI Art Venture Playbook
Created: 2026-04-24
Revenue Target: $1-5K/mo within 60 days
Capital Required: $0 (local gen on 64GB Mac)

---

## Overview

AI-generated digital characters monetized through social media and subscription platforms. All content clearly disclosed as AI-generated. Zero fraud. Maximum legal protection.

## Legal Framework (NON-NEGOTIABLE)

1. Every account bio includes: "All characters are AI-generated digital art. Not real people."
2. Every post watermarked with small text: "AI Generated"
3. No real person likenesses used, ever
4. All characters depicted as clearly adult (proportions, context, setting)
5. No minors depicted under any circumstances
6. Platform TOS compliance checked per platform before posting
7. Keep records of generation prompts and parameters for all published content
8. US law: AI-generated images of fictional adults are legal. Stay fictional, stay adult, stay disclosed.
9. FTC: If promoting products through character accounts, disclose paid partnerships
10. DMCA: You own outputs from locally-run models (Stable Diffusion). Cloud services may have different terms.

## Monetization Stack

| Platform | Purpose | Cut | Setup Time |
|----------|---------|-----|-----------|
| Twitter/X | Free traffic engine, sensitive media flag ON | Free | 10 min |
| Fansly | Primary subscription ($5/$15/$50 tiers) | 20% | 30 min |
| Patreon | Alt subscription, broader audience | 8-12% | 30 min |
| Throne | Wishlist/gifts (no payment processing needed) | Free | 5 min |
| Cash App | Tips in bio | Free | Already have |
| Ko-fi | One-time support | 0% (free tier) | 5 min |
| Gumroad | Sell art packs, bundles, custom sets | 10% | Already have (once account created) |

Total setup: ~90 minutes for all platforms.

## Content Pipeline

### Local Generation Stack (64GB RAM Mac)

ComfyUI + SDXL (or Pony Diffusion for anime style):
- Base model: PonyDiffusionXL or AnimagineXL (best for this niche)
- LoRAs: Train 1-3 consistent character LoRAs for recognizable "models"
- Resolution: 1024x1024 base, upscale to 2048x2048 for paid content
- Batch size: 10-20 images per generation session (~30 min)
- Video: AnimateDiff for short loops, SVD for higher quality

### Character Strategy

Create 3-5 distinct "characters" with consistent appearances:
- Each character gets their own LoRA or fixed seed+prompt combo
- Name them. Give them personalities in bios.
- Fans follow characters, not accounts. Consistency = retention.
- Rotate characters to keep feed fresh

### Posting Schedule

Twitter (main traffic driver):
- 3-5 posts/day minimum
- Mix: 70% free teasers, 30% "full set on Fansly/Patreon" CTAs
- Engage with similar accounts (like, reply, quote tweet)
- Use trending hashtags in the niche
- Pin best-performing post with link tree

Peak posting times (US audience):
- 8-10 AM EST (morning scroll)
- 12-2 PM EST (lunch)
- 8-11 PM EST (evening, highest engagement for this niche)

### Content Tiers

Free (Twitter): Cropped/watermarked previews, character introductions, behind-the-scenes prompts
$5/mo: Full resolution images, weekly drops (10-15 images)
$15/mo: Exclusive characters, NSFW variants, early access, polls to choose next content
$50/mo: Custom character requests (1 per month), access to prompt/workflow files

## ComfyUI Setup (run on Mac)

```bash
# Step 1: Clone ComfyUI
cd ~/Documents
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Step 2: Install dependencies (Apple Silicon MPS)
pip3 install torch torchvision torchaudio --break-system-packages
pip3 install -r requirements.txt --break-system-packages

# Step 3: Download model (PonyDiffusionXL recommended for this niche)
# Option A: Direct download
cd models/checkpoints
curl -L -o ponyDiffusionV6XL.safetensors "https://civitai.com/api/download/models/290640"
# OR download manually from civitai.com and place in models/checkpoints/

# Step 4: Launch
cd ~/Documents/ComfyUI
python3 main.py --force-fp16

# Opens at http://127.0.0.1:8188
# With 64GB RAM, you can run SDXL at full quality with large batch sizes
```

### Recommended ComfyUI Custom Nodes
```bash
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git  # Node manager (install everything else from UI)
# Then from ComfyUI Manager, install:
# - ComfyUI Impact Pack (face detection, upscale)
# - ComfyUI AnimateDiff Evolved (video generation)
# - ComfyUI Reactor (face swap for consistency)
# - ComfyUI Ultimate SD Upscale (high-res)
```

## DM Agent (Locally Hosted)

### Architecture
- Python script running locally, checks DMs via Twitter API (or Nitter scrape)
- Auto-responds with pricing menu
- Hard content filter on incoming messages

### Auto-Response Template
```
Hey! Thanks for the message.

Just so you know, all my characters are AI-generated digital art.

Here's what I offer:
- Free content on my timeline daily
- $5/mo Fansly: Full resolution + weekly drops
- $15/mo Fansly: Exclusive characters + NSFW + polls
- $50/mo Fansly: Custom character requests (1/month)

Links: [linktree URL]

For custom commissions, reply with what you're looking for and I'll quote you.
```

### GUARDRAILS (CRITICAL - ZERO TOLERANCE)

```python
BLOCKED_KEYWORDS = [
    # Minors - ABSOLUTE ZERO TOLERANCE
    "child", "kid", "minor", "underage", "young", "teen", "loli", "shota",
    "preteen", "jailbait", "pedo", "cp", "school girl", "school boy",
    "little girl", "little boy", "daughter", "son", "baby",
    # Add age-specific terms
    "12", "13", "14", "15", "16", "17",  # when in sexual context

    # Non-consensual
    "force", "rape", "assault", "drugged", "unconscious", "sleeping",
    "non-con", "noncon", "reluctant",

    # Real people
    "celebrity", "looks like [name]", "deepfake",

    # Illegal activity
    "bestiality", "animal", "incest",
]

RESPONSE_ON_BLOCK = """
This request violates our content policy and has been logged.
We create fictional adult digital art only.
Repeated violations will result in a permanent block.
"""

# All blocked messages are:
# 1. Logged with timestamp and sender ID (NO message content stored for legal protection)
# 2. Sender is auto-blocked
# 3. If pattern matches child-related terms: auto-reported to platform + NCMEC CyberTipline
```

### DM Agent Script Location
`AUTOMATIONS/ai_art_dm_agent.py`

## Revenue Projections

Conservative (month 1-2): $100-500/mo
- 500-1000 Twitter followers
- 20-50 Fansly subs at $5 avg

Growth (month 3-6): $1-3K/mo
- 5K-15K Twitter followers
- 200-600 Fansly subs
- Art pack sales on Gumroad

Scale (month 6-12): $3-10K/mo
- 15K-50K followers
- Multiple characters with dedicated fanbases
- Automated pipeline: gen -> post -> monetize

## Quick Start Checklist

- [ ] Install ComfyUI (commands above)
- [ ] Download PonyDiffusionXL or AnimagineXL model
- [ ] Generate first test batch (10 SFW character portraits)
- [ ] Create Twitter account with sensitive media enabled
- [ ] Set up Fansly account with 3 subscription tiers
- [ ] Create Throne wishlist
- [ ] Add Cash App / Ko-fi links to bio
- [ ] Create Linktree with all platform links
- [ ] Write character bios for 3 distinct characters
- [ ] First post with character introduction
- [ ] Set up DM auto-responder with guardrails
- [ ] Schedule daily posting (3-5x/day)

## Pollinations Quick Test (no install needed)

For immediate test before ComfyUI is set up:
```bash
curl -sL -o test_character.png "https://image.pollinations.ai/prompt/anime+digital+art+character+portrait+elegant+fantasy+woman+detailed+studio+lighting?width=1024&height=1024&nologo=true&seed=42"
```

Run this on the Mac terminal (not from VM — network restrictions apply).

## Integration with PRINTMAXX

- Add to Capital Genesis as new venture (CONTENT type, $0 upfront, high automation potential)
- Content feeds engagement_bait_converter.py for cross-promotion
- Revenue tracked in FINANCIALS/revenue_pipeline.json
- Characters can promote other PRINTMAXX products organically
- Art packs listed on Gumroad alongside other digital products

## Scaling with Video (AnimateDiff / SVD)

Once image pipeline is proven:
1. Install AnimateDiff Evolved in ComfyUI
2. Generate 2-4 second character loops (hair moving, blinking, breathing)
3. Video content gets 3-5x engagement vs static images on Twitter
4. Short-form video for TikTok (if platform allows)
5. Longer animations for premium tier content

64GB RAM handles AnimateDiff easily. Target: 512x768 at 16 frames for loops.
