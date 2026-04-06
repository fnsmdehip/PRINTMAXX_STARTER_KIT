# Automation Guide

> What can be automated, what tools to use, and how to set up batch workflows.

---

## Automation Summary

| Task | Automatable? | Tool | Time Saved |
|------|-------------|------|-----------|
| Image generation | Yes (batch) | Midjourney / Flux / Pollinations | 80% (batch vs daily) |
| Caption writing | Yes | Claude / GPT + templates | 90% |
| Post scheduling | Yes | Buffer / Publer / platform native | 95% |
| DM responses | Partially | Templates + AI assist | 60% |
| Analytics tracking | Yes | Spreadsheet + platform dashboards | 70% |
| Watermarking | Yes | Python script / batch processing | 100% |
| Voice messages | Yes (batch) | ElevenLabs API | 80% |
| Cross-posting | Yes | Manual or Publer | 50% |
| Content organization | Yes | Folder structure + naming convention | 90% |
| Audience engagement | No (human needed) | Manual comments and replies | 0% |

---

## Image Generation Batching

### Monthly Batch Workflow (Day 1-2 of each month)

**Step 1: Generate all images for the month**

Time estimate: 4-6 hours for 150 images (50 per character)

1. Open Midjourney or preferred tool
2. Load character reference images (--cref in Midjourney)
3. Work through IMAGE_PROMPTS.md sequentially
4. Generate 3-4 variations per prompt, select the best
5. Upscale all selected images to maximum resolution
6. Download and organize into folder structure

**Step 2: Quality check and organize**

Folder structure:
```
content/
  nova/
    2026-04/
      gym/
        nova_gym_01.png
        nova_gym_02.png
      beach/
        nova_beach_01.png
      lifestyle/
        nova_lifestyle_01.png
      ppv/
        nova_ppv_sunset_set/
          01.png through 10.png
  elara/
    2026-04/
      studio/
      urban/
      lifestyle/
      ppv/
  kai/
    2026-04/
      lifestyle/
      fashion/
      hair/
      ppv/
```

**Step 3: Apply watermarks**

Python script to batch-watermark all images:

```python
#!/usr/bin/env python3
"""
Batch watermark script for AI content.
Adds 'AI Generated' watermark to bottom-right corner.
"""
import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Install Pillow: pip3 install Pillow")
    exit(1)


def add_watermark(input_path, output_path, text="AI Generated"):
    """Add semi-transparent watermark to image."""
    img = Image.open(input_path).convert("RGBA")
    watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)

    # Font size relative to image width
    font_size = max(int(img.width * 0.025), 16)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except (OSError, IOError):
        font = ImageFont.load_default()

    # Position: bottom-right with padding
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    padding = int(img.width * 0.02)
    position = (img.width - text_width - padding, img.height - text_height - padding)

    # Semi-transparent white text
    draw.text(position, text, fill=(255, 255, 255, 120), font=font)

    # Composite and save
    result = Image.alpha_composite(img, watermark)
    result = result.convert("RGB")
    result.save(output_path, quality=95)


def batch_watermark(input_dir, output_dir):
    """Watermark all images in a directory recursively."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    for img_file in input_path.rglob("*.png"):
        relative = img_file.relative_to(input_path)
        out_file = output_path / relative
        out_file.parent.mkdir(parents=True, exist_ok=True)
        add_watermark(str(img_file), str(out_file))
        print(f"Watermarked: {relative}")

    for img_file in input_path.rglob("*.jpg"):
        relative = img_file.relative_to(input_path)
        out_file = output_path / relative
        out_file.parent.mkdir(parents=True, exist_ok=True)
        add_watermark(str(img_file), str(out_file))
        print(f"Watermarked: {relative}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 watermark.py <input_dir> <output_dir>")
        exit(1)
    batch_watermark(sys.argv[1], sys.argv[2])
    print("Done. All images watermarked.")
```

Save this script as `watermark.py` in the NSFW_AI_CONTENT directory.

Usage:
```bash
python3 watermark.py content/raw/ content/watermarked/
```

---

## Caption Generation

### Method 1: Template-Based (Fastest)

Pre-written caption templates per character, per content type. VA picks the matching template and customizes 1-2 details.

**Nova Caption Templates:**

| Content Type | Template |
|-------------|---------|
| Gym | "New week, new goals. [Exercise name] is my current obsession. What are you training today? [AI Generated]" |
| Beach | "Recovery day done right. The ocean fixes everything. [AI Generated]" |
| Lifestyle | "[Morning/Evening] vibes. Sometimes the simplest moments hit different. [AI Generated]" |
| Motivational | "Show up even when you don't want to. That's where growth lives. [AI Generated]" |
| Engagement | "[This or that question about fitness]? Drop your answer below. [AI Generated]" |

**Elara Caption Templates:**

| Content Type | Template |
|-------------|---------|
| Studio | "[One cryptic line about light, shadow, or beauty]. [AI Generated]" |
| Urban | "The city holds its breath at [time of day]. [AI Generated]" |
| Artistic | "Creating is the only honest thing I know how to do. [AI Generated]" |
| Personal | "Some days the work speaks. Other days I just listen. [AI Generated]" |
| Engagement | "What does [art/beauty/silence] mean to you? [AI Generated]" |

**Kai Caption Templates:**

| Content Type | Template |
|-------------|---------|
| Lifestyle | "Living my best life and it looks like [describe the scene]. Who's with me?? [AI Generated]" |
| Fashion | "Today's fit check: [describe outfit]. Rate it 1-10!! [AI Generated]" |
| Studio | "New beat coming soon and it goes CRAZY. Stay tuned. [AI Generated]" |
| Fun | "POV: you [funny relatable situation]. [AI Generated]" |
| Engagement | "Okay real talk -- [fun question]?? I need answers!! [AI Generated]" |

### Method 2: AI-Assisted (Higher Quality)

Use Claude or GPT to generate captions in character voice.

**Prompt template for caption generation:**
```
You are writing social media captions for [Character Name], an AI-generated
digital character. Here is her personality: [paste personality from CHARACTER_PROFILES.md]

Generate 30 captions for the following content types:
- 10 fitness/gym captions (Nova) / studio/art captions (Elara) / lifestyle captions (Kai)
- 10 engagement/question captions
- 5 personal/reflective captions
- 5 promotional captions (driving to subscription)

Every caption must end with "[AI Generated]" tag.
Write in the character's voice as described above.
Keep captions under 200 characters for optimal engagement.
```

Run this once per month per character. Saves 30 minutes of manual writing.

---

## Voice Message Generation

### ElevenLabs Setup

1. Create an account at elevenlabs.io
2. Use Voice Design or Voice Cloning to create unique voices for each character
3. Save voice IDs for each character

**Voice profiles to create:**
- Nova: Warm, energetic, slight Miami inflection
- Elara: Soft, measured, British received pronunciation
- Kai: Bright, expressive, California casual

### Batch Voice Generation

Monthly batch: 12-20 voice messages per character (3-5 per week)

**Message types to pre-generate:**

| Type | Count/Month | Length | Example |
|------|------------|--------|---------|
| Morning greeting | 4 | 15-30 sec | "Good morning! Hope you're starting this day with good energy..." |
| Thank you | 4 | 15-30 sec | "Just wanted to say thank you for being here..." |
| Personal update | 4 | 30-60 sec | "So today I [character-specific activity]..." |
| Subscriber milestone | 2 | 30-45 sec | "We just hit [number] subscribers and I'm so grateful..." |
| Seasonal/special | 2 | 30-60 sec | Holiday, birthday, or event-specific messages |

### ElevenLabs API Script (for batch generation)

```python
#!/usr/bin/env python3
"""
Batch voice message generator using ElevenLabs API.
Generates pre-written messages for each character.
"""
import os
import json
import requests
from pathlib import Path

API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
BASE_URL = "https://api.elevenlabs.io/v1"

# Voice IDs (replace with actual IDs after creating voices)
VOICES = {
    "nova": "VOICE_ID_NOVA",
    "elara": "VOICE_ID_ELARA",
    "kai": "VOICE_ID_KAI",
}

# Voice settings per character
SETTINGS = {
    "nova": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.4},
    "elara": {"stability": 0.7, "similarity_boost": 0.8, "style": 0.3},
    "kai": {"stability": 0.4, "similarity_boost": 0.7, "style": 0.6},
}


def generate_voice(character, text, output_path):
    """Generate a voice message and save to file."""
    if not API_KEY:
        print("Set ELEVENLABS_API_KEY environment variable")
        return False

    voice_id = VOICES.get(character)
    if not voice_id or voice_id.startswith("VOICE_ID_"):
        print(f"Replace placeholder voice ID for {character}")
        return False

    settings = SETTINGS.get(character, {})

    response = requests.post(
        f"{BASE_URL}/text-to-speech/{voice_id}",
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": settings,
        },
    )

    if response.status_code == 200:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Generated: {output_path}")
        return True
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return False


def batch_generate(messages_file, output_dir):
    """
    Generate all messages from a JSON file.

    JSON format:
    [
        {"character": "nova", "type": "greeting", "text": "Hey! Good morning..."},
        {"character": "elara", "type": "update", "text": "I've been thinking about..."},
    ]
    """
    with open(messages_file) as f:
        messages = json.load(f)

    for i, msg in enumerate(messages):
        character = msg["character"]
        msg_type = msg["type"]
        filename = f"{character}_{msg_type}_{i:03d}.mp3"
        output_path = os.path.join(output_dir, character, filename)
        generate_voice(character, msg["text"], output_path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 voice_generator.py <messages.json> <output_dir>")
        exit(1)
    batch_generate(sys.argv[1], sys.argv[2])
```

### Monthly Voice Messages JSON Template

Create `messages_april.json`:
```json
[
    {
        "character": "nova",
        "type": "morning_01",
        "text": "Hey! Good morning. I just finished my workout and I'm feeling so good. I hope you're starting this day with good energy. Remember, showing up is half the battle. You got this."
    },
    {
        "character": "nova",
        "type": "thankyou_01",
        "text": "I just wanted to take a second to say thank you. You being here, supporting this, it means the world. Every time I see a new subscriber I smile. So thank you for that."
    },
    {
        "character": "elara",
        "type": "diary_01",
        "text": "I've been sitting in the studio all afternoon. There's something about the light in late April that makes everything feel like it's dissolving. I started a new series today. I'm not sure what it is yet. But I trust the process."
    },
    {
        "character": "elara",
        "type": "thankyou_01",
        "text": "Thank you. For being here. For seeing this work. It matters more than I can express. This project exists because of people like you."
    },
    {
        "character": "kai",
        "type": "morning_01",
        "text": "Good MORNING! Okay so I literally just woke up like five minutes ago and I already have three song ideas in my head. This is gonna be a good day. I can feel it. What are you up to today?"
    },
    {
        "character": "kai",
        "type": "thankyou_01",
        "text": "Oh my god you guys. Thank you SO much for subscribing. Like, I can't even believe this is real. You all are literally the best. I'm about to make so much content for you, get ready."
    }
]
```

---

## Post Scheduling

### Option 1: Buffer (Recommended for Starting)

- Free tier: 3 accounts, 10 scheduled posts per account
- Paid ($6/mo per channel): unlimited scheduling
- Supports Twitter, Reddit (limited), and general scheduling

**Setup:**
1. Create Buffer account
2. Connect Twitter accounts for each character
3. Upload content batch and schedule for the month
4. Reddit posts must be done manually (Buffer Reddit support is limited)

### Option 2: Publer (More Features)

- Free tier: 3 accounts, 10 posts
- Paid ($12/mo): unlimited scheduling, auto-scheduling, recurring posts
- Better Reddit support than Buffer
- Bulk upload and schedule

**Setup:**
1. Create Publer account
2. Connect all platform accounts
3. Use CSV upload for bulk scheduling
4. Set optimal posting times per platform

### Option 3: Platform Native Scheduling

- **Fanvue:** Queue system for scheduled posts
- **Fansly:** Scheduled posts built in
- **Twitter:** Schedule tweets natively

**Recommended approach:** Use platform native scheduling for Fanvue/Fansly (most control), Buffer for Twitter.

### Optimal Posting Times (adjust based on your analytics)

| Platform | Best Time (EST) | Why |
|----------|----------------|-----|
| Fanvue/Fansly | 8-10 PM | Peak engagement for creator platforms |
| Reddit | 9 AM, 12 PM, 6 PM | Morning, lunch, evening browsing peaks |
| Twitter | 12 PM, 5 PM, 9 PM | Lunch break, commute, evening scroll |

---

## DM Response Automation

### Template-Based DM System

DMs are partially automatable using templates. The VA selects the appropriate template and personalizes 1-2 words.

**Welcome Message (auto-send on subscribe):**
Most platforms support auto-welcome messages. Set these up once per character.

**Response Templates by Category:**

```
CATEGORY: Compliment
NOVA: "Aww thank you so much! That honestly made my day. What kind of content do you love seeing most?"
ELARA: "Thank you. That means a lot. I appreciate you seeing the work."
KAI: "STOPPP you're so sweet!! Thank you!! What should I do next??"

CATEGORY: Content request
NOVA: "Ooh I love that idea! I'll add it to my list. Stay tuned!"
ELARA: "That's an interesting concept. Let me think about how to bring that to life."
KAI: "OKAY BET. Adding that to the queue right now. You're gonna love it."

CATEGORY: General chat
NOVA: "Hey! How's your day going? I've been [activity related to recent post]."
ELARA: "Hello. [Brief reflection related to recent content]. How are you?"
KAI: "Heyyy! What's up? I've been [activity]. Tell me about YOUR day!"

CATEGORY: Tip thank you
NOVA: "You're amazing, thank you! That energy keeps me going. Seriously."
ELARA: "This means more than you know. Thank you for supporting the work."
KAI: "OMG thank you!! You literally just made me SO happy. ILY!"

CATEGORY: Subscription thank you
NOVA: "Welcome! I'm so glad you're here. Quick reminder: I'm an AI-generated character and all content is made with AI. Now let's get to the good stuff!"
ELARA: "Welcome. I appreciate your presence here. As a note, I'm an AI-generated digital character. Every image is created with AI. I find beauty in that truth."
KAI: "WELCOME!! So excited you're here! Quick heads up: I'm AI-generated -- all my pics are made with AI, no real person! Which is honestly sick. ANYWAY let's go!!"
```

### AI-Assisted DM Responses (Scale Phase)

At 500+ subscribers, template DMs won't scale. Use Claude or GPT to generate personalized responses:

**Prompt for DM response generation:**
```
You are [Character Name]. Here is your personality: [paste from CHARACTER_PROFILES.md]

A subscriber sent this DM: "[subscriber message]"

Write a response in character. Keep it under 3 sentences. Be warm but maintain boundaries.
Never claim to be a real person. If asked directly, confirm you're an AI character.
Never agree to meet in person. Never share personal information beyond the character bio.
```

---

## Analytics Tracking Automation

### Weekly Tracking Spreadsheet

Create a Google Sheet with these tabs:

**Tab 1: Subscriber Tracking**
```
Week | Nova_Fanvue | Nova_Fansly | Elara_Fanvue | Elara_Fansly | Kai_Fanvue | Kai_Fansly | Total
```

**Tab 2: Revenue Tracking**
```
Week | Subs_Revenue | PPV_Revenue | Tips | Custom | Affiliate | Total_Gross | Fees | Net
```

**Tab 3: Content Performance**
```
Date | Character | Platform | Content_Type | Engagement_Rate | Notes
```

**Tab 4: Churn Tracking**
```
Month | Character | Starting_Subs | New_Subs | Churned | Ending_Subs | Churn_Rate
```

### Automated Data Collection

Most platform dashboards export CSV. Monthly workflow:
1. Export data from each platform dashboard
2. Import into tracking spreadsheet
3. Calculate key metrics
4. Flag any concerning trends (churn above 20%, revenue decline)

---

## Full Monthly Automation Workflow

### Day 1-2: Content Generation (4-6 hours)
```
1. Generate 50 images per character using IMAGE_PROMPTS.md (150 total)
2. Select best outputs, upscale, organize into folders
3. Run watermark.py on all images
4. Generate 30 captions per character using templates or AI
5. Generate 12-20 voice messages per character using voice_generator.py
```

### Day 3: Scheduling (2-3 hours)
```
1. Upload content to Fanvue/Fansly and schedule for the month
2. Schedule Twitter posts via Buffer
3. Prepare Reddit posts (save drafts, schedule manually)
4. Set up PPV content drops for weeks 2 and 4
5. Schedule cross-promotion posts for week 3
```

### Daily: Engagement (1-2 hours total, 20-40 min per character)
```
1. Check DMs and respond using templates (morning)
2. Respond to comments on posts (afternoon)
3. Post any reactive/trending content (if applicable)
4. Quick check platform analytics
```

### Weekly: Review (30 min)
```
1. Update tracking spreadsheet
2. Note top-performing content
3. Adjust next week's schedule if needed
4. Check for any platform policy updates
```

### Monthly: Optimization (1-2 hours)
```
1. Full analytics review
2. Calculate churn rates
3. Update pricing if needed
4. Plan next month's content themes
5. Generate next month's content batch
```

---

## Tools Cost Summary

| Tool | Plan | Monthly Cost | Purpose |
|------|------|-------------|---------|
| Midjourney | Standard | $30 | Image generation |
| ElevenLabs | Starter | $5 | Voice messages |
| Buffer | Free or Pro | $0-18 | Tweet scheduling |
| Publer (optional) | Free or Pro | $0-12 | Multi-platform scheduling |
| Pillow (Python) | Free | $0 | Image watermarking |
| Google Sheets | Free | $0 | Analytics tracking |
| Claude API (optional) | Pay-per-use | $5-10 | Caption and DM generation |
| **Total** | | **$35-75/mo** | |

---

## Scaling Automation (Phase 3+)

When revenue exceeds $5K/mo, consider:

1. **VA hire:** $500-800/mo for a part-time VA to handle daily engagement and scheduling
2. **Custom posting tool:** Build a simple script that posts to all platforms via API
3. **Automated analytics dashboard:** Pull platform data via API into a real-time dashboard
4. **Content recycling:** After 6 months, older content can be re-posted to new subscribers who haven't seen it
5. **Character expansion:** Add characters 4 and 5 using the same batch workflow

### What NOT to Automate

- **Genuine engagement.** Real comments and replies build parasocial connection. Template DMs are fine for scale, but some human touch is needed.
- **Content quality decisions.** AI generates multiple variations. A human must pick the best ones.
- **Platform policy compliance.** A human must review policy changes and adjust.
- **Custom content fulfillment.** Each custom request needs a human to review and generate to spec.
- **Crisis management.** If an account gets flagged or content is removed, a human decides the response.
