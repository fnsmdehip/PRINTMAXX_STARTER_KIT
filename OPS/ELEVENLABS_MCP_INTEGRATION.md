# ElevenLabs MCP Integration Guide

**Purpose:** Integrate ElevenLabs voice synthesis with Claude Code via MCP for Remotion video voiceovers, AI influencer content, and audio production.

**Reference:** @Shpigford workflow - ElevenLabs API via MCP to add voiceover to Remotion videos.

**Last Updated:** January 2026

---

## What Is ElevenLabs?

ElevenLabs is an AI voice synthesis platform that provides:
- Text-to-speech with natural-sounding voices
- Voice cloning from audio samples
- Emotional range and voice control
- API access for programmatic generation
- Multi-language support (29+ languages)

**Quality:** Industry-leading for natural-sounding AI voices. Used by 90%+ of AI influencers.

---

## Pricing Analysis (January 2026)

| Plan | Cost | Characters | Audio Hours | Best For |
|------|------|------------|-------------|----------|
| **Free** | $0/mo | 10k | ~10 min | Testing |
| **Starter** | $5/mo | 30k | ~30 min | Light use |
| **Creator** | $22/mo | 100k | ~2 hours | Regular posting (RECOMMENDED) |
| **Pro** | $99/mo | 500k | ~10 hours | Scale operations |
| **Scale** | $330/mo | 2M | ~40 hours | Agency/production |

### Cost Per Content Type

| Content Type | Characters | Audio Length | Cost (Creator Plan) |
|--------------|------------|--------------|---------------------|
| TikTok (200 words) | ~1,000 | 30-60 sec | $0.22 |
| YouTube Short | ~1,500 | 45-90 sec | $0.33 |
| Podcast intro | ~500 | 15-30 sec | $0.11 |
| App tutorial | ~3,000 | 2-3 min | $0.66 |
| Full video voiceover | ~10,000 | 8-12 min | $2.20 |

**Monthly Capacity (Creator $22):**
- ~100 TikTok voiceovers
- ~66 YouTube Shorts
- ~10 full-length tutorials
- ~33 mixed content pieces

---

## MCP Integration Setup

### Option 1: Official ElevenLabs MCP Server (Recommended)

ElevenLabs provides an official MCP server for Claude integration.

**Installation:**

```bash
# Install via npm
npm install -g @elevenlabs/mcp-server

# Or via pip
pip install elevenlabs-mcp
```

**Configuration (claude_desktop_config.json):**

```json
{
  "mcpServers": {
    "elevenlabs": {
      "command": "npx",
      "args": ["@elevenlabs/mcp-server"],
      "env": {
        "ELEVENLABS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Option 2: Generic HTTP MCP Server

If official MCP is unavailable, use a generic HTTP MCP that wraps the ElevenLabs REST API.

**Configuration:**

```json
{
  "mcpServers": {
    "elevenlabs-http": {
      "command": "node",
      "args": ["/path/to/http-mcp-server.js"],
      "env": {
        "API_BASE_URL": "https://api.elevenlabs.io/v1",
        "API_KEY": "your_elevenlabs_api_key"
      }
    }
  }
}
```

### Option 3: Direct API Calls via Bash

For simpler integration, use Bash scripts that call the ElevenLabs API directly.

**Add to .env:**

```bash
ELEVENLABS_API_KEY=your_api_key_here
```

**Example Script (scripts/generate_voice.sh):**

```bash
#!/bin/bash
# Generate voiceover using ElevenLabs API

TEXT="$1"
VOICE_ID="${2:-21m00Tcm4TlvDq8ikWAM}"  # Default: Rachel
OUTPUT_FILE="${3:-output.mp3}"

curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}" \
  -H "Accept: audio/mpeg" \
  -H "Content-Type: application/json" \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}" \
  -d "{
    \"text\": \"${TEXT}\",
    \"model_id\": \"eleven_multilingual_v2\",
    \"voice_settings\": {
      \"stability\": 0.5,
      \"similarity_boost\": 0.5
    }
  }" \
  --output "${OUTPUT_FILE}"

echo "Generated: ${OUTPUT_FILE}"
```

---

## Available MCP Tools

When ElevenLabs MCP is configured, these tools become available:

### Core Voice Generation

| Tool | Purpose | Parameters |
|------|---------|------------|
| `generate_speech` | Convert text to audio | text, voice_id, model_id, output_format |
| `list_voices` | Get available voices | category, search |
| `get_voice` | Get voice details | voice_id |
| `add_voice` | Clone new voice | name, files, description |
| `edit_voice` | Update voice settings | voice_id, settings |
| `delete_voice` | Remove cloned voice | voice_id |

### Audio Processing

| Tool | Purpose | Parameters |
|------|---------|------------|
| `get_audio_from_sample` | Extract voice from sample | audio_file |
| `convert_text_to_speech_stream` | Stream audio generation | text, voice_id |

### History & Management

| Tool | Purpose | Parameters |
|------|---------|------------|
| `get_history` | Get generation history | page_size, start_after |
| `get_history_item` | Get specific generation | history_id |
| `get_subscription_info` | Check usage/limits | none |

---

## Voice Selection Strategy

### Pre-built Voices (No Setup Required)

| Voice Name | Voice ID | Style | Best For |
|------------|----------|-------|----------|
| Rachel | 21m00Tcm4TlvDq8ikWAM | American female, warm | General narration |
| Domi | AZnzlk1XvdvUeBnXmlld | American female, assertive | Marketing |
| Bella | EXAVITQu4vr4xnSDxMaL | American female, soft | ASMR, wellness |
| Antoni | ErXwobaYiN019PkySvjV | American male, calm | Tutorials |
| Josh | TxGEqnHWrfWFTfGW9XjX | American male, deep | Authority content |
| Arnold | VR6AewLTigWG4xSOukaG | American male, confident | Fitness, motivation |
| Adam | pNInz6obpgDQGcFmaJgB | American male, deep | Documentary |
| Sam | yoZ06aMxZJJ28mfd3POQ | American male, raspy | Edgy content |

### Voice-to-Niche Matching

| Niche | Recommended Voice | Alternative | Style Settings |
|-------|-------------------|-------------|----------------|
| **Faith/Prayer** | Bella (soft female) | Antoni (calm male) | Stability: 70%, Clarity: 60% |
| **Fitness/Gym** | Arnold (confident) | Josh (deep) | Stability: 50%, Clarity: 70% |
| **Women's Wellness** | Rachel (warm) | Bella (soft) | Stability: 65%, Clarity: 65% |
| **Tech/Productivity** | Antoni (calm) | Rachel (warm) | Stability: 60%, Clarity: 75% |
| **ASMR** | Bella (soft) | Custom whisper | Stability: 70%, Clarity: 50% |
| **Biohacking** | Josh (deep) | Adam (documentary) | Stability: 55%, Clarity: 70% |
| **Finance/Crypto** | Adam (deep) | Arnold (confident) | Stability: 50%, Clarity: 75% |

### Custom Voice Cloning

For unique brand voice, clone from audio samples:

**Requirements:**
- 3-10 minutes of clean audio
- No background noise
- Consistent speaking style
- Single speaker only

**Setup Process:**
1. Record or source clean audio samples
2. Upload via ElevenLabs dashboard or API
3. Wait for processing (5-15 minutes)
4. Test with sample text
5. Adjust settings for consistency
6. Lock settings for all future use

**Voice Clone API Call:**

```bash
curl -X POST "https://api.elevenlabs.io/v1/voices/add" \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}" \
  -F "name=MyBrandVoice" \
  -F "files=@sample1.mp3" \
  -F "files=@sample2.mp3" \
  -F "description=Brand voice for PRINTMAXX content"
```

---

## PRINTMAXX Use Cases

### 1. Remotion Video Voiceovers

**Workflow:**
1. Write video script
2. Generate voiceover via ElevenLabs
3. Import MP3 to Remotion project
4. Sync audio with visuals
5. Export final video

**Integration with Remotion:**

```typescript
// In Remotion composition
import { Audio, staticFile } from 'remotion';

export const MyVideo: React.FC = () => {
  return (
    <>
      {/* Other video content */}
      <Audio
        src={staticFile('voiceover.mp3')}
        startFrom={0}
        volume={1}
      />
    </>
  );
};
```

**Script for Batch Generation:**

```bash
#!/bin/bash
# Generate voiceovers for all video scripts

SCRIPTS_DIR="LANDING/printmaxx-site/scripts"
OUTPUT_DIR="LANDING/printmaxx-site/public/voiceovers"

for script in "$SCRIPTS_DIR"/*.txt; do
  filename=$(basename "$script" .txt)
  text=$(cat "$script")

  curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" \
    -H "Accept: audio/mpeg" \
    -H "xi-api-key: ${ELEVENLABS_API_KEY}" \
    -d "{\"text\": \"${text}\", \"model_id\": \"eleven_multilingual_v2\"}" \
    --output "${OUTPUT_DIR}/${filename}.mp3"

  echo "Generated: ${filename}.mp3"
done
```

### 2. AI Influencer Content (AI004 - ASMR)

**ASMR Voice Settings:**
```json
{
  "voice_id": "EXAVITQu4vr4xnSDxMaL",  // Bella
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.7,
    "similarity_boost": 0.5,
    "style": 0.0,
    "use_speaker_boost": false
  }
}
```

**Whisper Effect:**
- Lower stability (60-70%)
- Lower clarity (50-60%)
- Post-process: reduce volume, add reverb
- Layer with ambient sounds

### 3. App Tutorial Narration

Generate voiceovers for app demos and tutorials:

```bash
# Example: PrayerLock tutorial
generate_speech \
  --text "Welcome to PrayerLock. Set your daily prayer time, and your phone will lock until you complete your devotional." \
  --voice_id "21m00Tcm4TlvDq8ikWAM" \
  --output "builds/prayerlock/marketing/tutorial_voiceover.mp3"
```

### 4. Podcast/Audio Content

Generate full podcast episodes:

```python
# Python script for podcast generation
import requests
import os

def generate_podcast_segment(text, segment_name, voice_id="21m00Tcm4TlvDq8ikWAM"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.environ["ELEVENLABS_API_KEY"]
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)

    with open(f"podcast_{segment_name}.mp3", "wb") as f:
        f.write(response.content)

    return f"podcast_{segment_name}.mp3"
```

### 5. Cold Outbound Voice Notes

Generate personalized voice notes for LinkedIn outreach:

```bash
# Generate voice note for prospect
TEXT="Hey [Name], saw your post about [topic]. Quick thought on how [solution] could help. Would love to connect."

curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/VR6AewLTigWG4xSOukaG" \
  -H "Accept: audio/mpeg" \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}" \
  -d "{\"text\": \"${TEXT}\", \"model_id\": \"eleven_multilingual_v2\"}" \
  --output "voice_note_prospect.mp3"
```

---

## Integration with Existing Skills

### /remotion-video + ElevenLabs

Modify the Remotion skill to automatically generate voiceovers:

**Updated Workflow:**
1. `/remotion-video` generates video composition
2. Script extracted and sent to ElevenLabs
3. Voiceover generated and saved to `public/voiceovers/`
4. Remotion composition includes `<Audio>` component
5. Final video rendered with synchronized audio

### Ralph Loop Integration

Add to ralph loop for batch content generation:

```bash
# ralph/loops/content_social/prompt.md addition

For video content generation:
1. Generate video script
2. Call ElevenLabs API for voiceover
3. Save audio to output/voiceovers/
4. Update Remotion composition with audio
5. Render final video
```

---

## Technical Setup Steps

### 1. Create ElevenLabs Account

1. Go to https://elevenlabs.io
2. Sign up (email or Google)
3. Verify email
4. Select plan (Creator $22/mo recommended)

### 2. Get API Key

1. Log into ElevenLabs
2. Go to Profile > API Keys
3. Copy API key
4. Store securely (never commit to git)

### 3. Add to Environment

```bash
# Add to .env
echo "ELEVENLABS_API_KEY=your_key_here" >> .env

# Add to .gitignore if not already
echo ".env" >> .gitignore
```

### 4. Configure MCP (Option A - NPM Server)

```bash
# Install server
npm install -g @elevenlabs/mcp-server

# Add to Claude config
# Edit ~/Library/Application Support/Claude/claude_desktop_config.json
```

### 5. Test Integration

```bash
# Test API directly
curl -X GET "https://api.elevenlabs.io/v1/voices" \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}"
```

### 6. Create Voice Presets

Save voice settings for consistency:

```json
// voice_presets.json
{
  "printmaxx_faith": {
    "voice_id": "EXAVITQu4vr4xnSDxMaL",
    "stability": 0.7,
    "similarity_boost": 0.6,
    "style": 0.0
  },
  "printmaxx_fitness": {
    "voice_id": "VR6AewLTigWG4xSOukaG",
    "stability": 0.5,
    "similarity_boost": 0.7,
    "style": 0.3
  },
  "printmaxx_tech": {
    "voice_id": "ErXwobaYiN019PkySvjV",
    "stability": 0.6,
    "similarity_boost": 0.75,
    "style": 0.0
  }
}
```

---

## Budget Optimization

### Character Counting Tips

- Remove unnecessary words
- Use contractions ("it's" vs "it is")
- Avoid repetition
- Batch similar content

### Cost Reduction Strategies

1. **Batch Generation:** Generate multiple videos at once
2. **Template Reuse:** Create intro/outro once, reuse across videos
3. **Tiered Quality:** Use free tier for testing, Creator for production
4. **Cache Common Phrases:** Generate standard phrases once, reuse

### Monthly Budget Allocation (Creator Plan - $22)

| Content Type | Allocation | Character Budget |
|--------------|------------|------------------|
| App Promos | 40% | 40,000 chars |
| Social Content | 30% | 30,000 chars |
| Tutorials | 20% | 20,000 chars |
| Testing | 10% | 10,000 chars |

---

## Quality Checklist

Before using generated audio:

- [ ] Listen through completely
- [ ] Check pronunciation of brand names
- [ ] Verify pacing matches visual
- [ ] No awkward pauses or cuts
- [ ] Consistent volume levels
- [ ] No digital artifacts
- [ ] Matches target emotion/tone

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Robotic sound | Low stability | Increase stability to 60-70% |
| Inconsistent voice | Settings changed | Lock voice settings, document values |
| Audio clipping | Text too long | Break into shorter segments |
| Wrong pronunciation | Unusual words | Use phonetic spelling or SSML |
| API rate limit | Too many requests | Add delay between calls |

### SSML for Pronunciation

```xml
<speak>
  Welcome to <phoneme alphabet="ipa" ph="preɪ.ər.lɑk">PrayerLock</phoneme>.
  Take a <break time="500ms"/> deep breath.
</speak>
```

---

## Related Files

- **Sound Design Guide:** `OPS/prompts/remotion/SOUND_DESIGN_GUIDE.md`
- **Remotion Prompts:** `OPS/prompts/remotion/REMOTION_MASTER_PROMPT.md`
- **ASMR PRD:** `MONEY_METHODS/AI_INFLUENCER/ASMR/prd.json`
- **AI Influencer Platforms:** `MONEY_METHODS/AI_INFLUENCER/AI_INFLUENCER_PLATFORMS_MEGA_GUIDE.md`
- **Tools Master List:** `LEDGER/TOOLS_SERVICES_MASTER.csv`

---

## Human Setup Required

**TIER 1 (Required for Integration):**
- [ ] Create ElevenLabs account
- [ ] Subscribe to Creator plan ($22/mo)
- [ ] Get API key from dashboard
- [ ] Add API key to .env file
- [ ] Test API connection

**TIER 2 (Optional Enhancements):**
- [ ] Clone custom brand voice
- [ ] Configure MCP server
- [ ] Set up voice presets per niche
- [ ] Create batch generation scripts

---

## Quick Start Commands

```bash
# Test connection
curl -s "https://api.elevenlabs.io/v1/voices" \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}" | jq '.voices[0].name'

# Generate simple voiceover
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" \
  -H "Accept: audio/mpeg" \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}" \
  -d '{"text": "Hello, welcome to PRINTMAXX.", "model_id": "eleven_multilingual_v2"}' \
  --output test_voiceover.mp3

# Check usage
curl -s "https://api.elevenlabs.io/v1/user/subscription" \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}" | jq '.character_count, .character_limit'
```

---

*Note: API pricing and features may change. Check https://elevenlabs.io for current information.*
