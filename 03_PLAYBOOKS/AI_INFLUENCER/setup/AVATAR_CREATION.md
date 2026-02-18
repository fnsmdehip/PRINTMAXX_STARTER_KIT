# Avatar Creation for AI Influencers

Tools and workflows for creating consistent AI character visuals and media.

---

## The avatar stack

| Type | Tool | Cost | Use case |
|------|------|------|----------|
| Static images | Midjourney | $10-30/mo | Photos, thumbnails |
| Static images | Leonardo.ai | $12-48/mo | Photos, consistent characters |
| Video | HeyGen | $24-180/mo | Talking head videos |
| Video | D-ID | $5.99-300/mo | Quick video clips |
| Voice | ElevenLabs | $5-99/mo | Voice consistency |
| Voice | PlayHT | $31-99/mo | Voice variety |

---

## Static avatar creation

### Option 1: Midjourney

Best for: Stylized, artistic avatars

**Process:**
1. Generate base character with detailed prompt
2. Use --seed to maintain consistency
3. Create reference sheet with multiple angles
4. Use that reference for all future generations

**Prompt template:**
```
portrait of [gender] [age range] [ethnicity] [style],
[hair color/style], [eye color], [expression],
[outfit description], [setting],
professional photo, 8k, consistent lighting
--ar 1:1 --seed [number]
```

**Consistency tips:**
- Save the seed number for every good generation
- Create a character reference sheet
- Use /describe on your best outputs
- Build a prompt library for your character

### Option 2: Leonardo.ai

Best for: Photorealistic, highly consistent characters

**Advantage:** Character consistency feature built in

**Process:**
1. Train a character model on 10-20 images
2. Generate new content using that model
3. Maintain same character across poses, settings

**Workflow:**
1. Generate initial character
2. Use image-to-image for variations
3. Build expression library
4. Create pose library
5. Generate content using libraries

---

## Video avatar creation

### Option 1: HeyGen (recommended)

Best for: Professional talking head videos

**Pricing:**
- Creator: $24/mo (36 credits)
- Business: $180/mo (unlimited)

**Process:**
1. Use their AI avatars or create custom
2. Input script
3. Select voice (or use your trained voice)
4. Generate video
5. Download and edit if needed

**Quality tips:**
- Keep videos under 2 minutes
- Use natural-sounding scripts
- Match lip sync to voice speed
- Add captions (improves engagement 30%+)

**Custom avatar option:**
- Record 2-5 minute video of yourself/actor
- Upload to train custom avatar
- Use that avatar for all content
- Requires consent documentation

### Option 2: D-ID

Best for: Quick, short-form clips

**Pricing:**
- Lite: $5.99/mo (5 min video)
- Pro: $49/mo (50 min video)

**Best use cases:**
- Short replies/engagement content
- Stories
- Quick tips (under 60 seconds)

### Comparison

| Feature | HeyGen | D-ID |
|---------|--------|------|
| Quality | Higher | Good |
| Speed | Slower | Faster |
| Custom avatars | Yes | Yes |
| Price/minute | Higher | Lower |
| Best for | Main content | Quick clips |

---

## Voice creation

### ElevenLabs (recommended)

**Pricing:**
- Starter: $5/mo (30k characters)
- Creator: $22/mo (100k characters)
- Pro: $99/mo (500k characters)

**Voice cloning options:**
1. Instant voice clone (quick, less accurate)
2. Professional voice clone (higher quality)
3. Choose from library voices

**Process for original voice:**
1. Select base voice from library
2. Adjust settings (stability, clarity, style)
3. Test with sample scripts
4. Lock settings for consistency

**Consistency rules:**
- Save voice settings exactly
- Use same voice for all content
- Keep speech rate consistent
- Match emotion to content type

### PlayHT

**Good for:** More variety in voices, different accents

**When to use:** If ElevenLabs doesn't have the voice profile you need

---

## Workflow: Creating a content piece

### For a talking head video:

1. **Write script** (use SCRIPT_TEMPLATES/)
2. **Generate audio** with ElevenLabs
3. **Preview for natural sound** (adjust if robotic)
4. **Generate video** with HeyGen using that audio
5. **Add captions** (CapCut, Opus Clip)
6. **Add disclosure watermark** if not in bio/description

### For a static image post:

1. **Define concept** (what's the visual message?)
2. **Reference your character sheet**
3. **Generate with consistent prompt structure**
4. **Check against reference** (same person?)
5. **Add text/overlays** in Canva/editing tool
6. **Verify disclosure visible**

---

## Building your asset library

Create folders for:
```
/avatar_assets/
  /reference/
    character_sheet.png
    expression_guide.png
    style_reference.png
  /images/
    /headshots/
    /full_body/
    /expressions/
  /video/
    /intros/
    /outros/
    /b_roll/
  /audio/
    voice_settings.json
    sample_clips/
  /templates/
    caption_templates/
    thumbnail_templates/
```

---

## Consistency checklist

Before publishing any visual content:

- [ ] Face matches reference character
- [ ] Outfit aligns with character style
- [ ] Lighting consistent with other content
- [ ] Expression appropriate for message
- [ ] Voice matches established voice
- [ ] Disclosure visible or mentioned
- [ ] No conflicting visual elements

---

## Cost optimization

**Starter budget ($50/mo):**
- Leonardo.ai: $12
- ElevenLabs: $22
- D-ID: $6
- Total: $40

**Growth budget ($200/mo):**
- Midjourney: $30
- HeyGen: $24
- ElevenLabs: $22
- Extra generation credits: $124

**Scale budget ($500+/mo):**
- HeyGen Business: $180
- ElevenLabs Pro: $99
- Leonardo Pro: $48
- Midjourney Pro: $60
- Buffer for extras: $113

---

## Common mistakes

**Inconsistent character**
Each generation looks slightly different. Solve by training custom models or using strict seed/reference control.

**Uncanny valley**
Video looks almost human but wrong. Solve by embracing stylization or using higher quality tiers.

**Voice mismatch**
Video voice doesn't match usual voice. Solve by always using same ElevenLabs voice settings.

**Over-producing**
Spending hours on single piece. Solve by creating templates and batch processing.

---

## Disclosure in visuals

Options:
1. Watermark in corner: "AI-Generated Content"
2. Intro slate: "I'm [Name], your AI [role]"
3. Caption: "[AI avatar]" visible throughout
4. End slate: "Created with AI tools"

At minimum: One visual disclosure per video
Best practice: Multiple disclosure touchpoints
