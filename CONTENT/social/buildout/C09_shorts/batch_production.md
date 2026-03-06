# Batch Production SOP — 10 Shorts in 1 Hour

**Goal:** Go from 0 to 10 published Shorts in 60 minutes or less
**Requires:** Claude Pro, ElevenLabs, CapCut (mobile or desktop), YouTube app
**Cost per session:** ~$0.80 in ElevenLabs credits

---

## THE ASSEMBLY LINE APPROACH

The mistake most creators make: produce one Short end-to-end before starting the next.
The correct approach: run all 10 Shorts through each stage together.
Stage 1 for all 10 → Stage 2 for all 10 → etc.
This is how factories work. Apply it to content.

---

## PHASE 1: SCRIPT GENERATION (10 minutes for 10 scripts)

**Tool:** Claude Pro
**Prompt template (copy-paste ready):**

```
I need 10 YouTube Shorts scripts for a solopreneur/money methods channel.

Format for each:
- Hook (0-3 seconds): One sentence. Consequence-first. Specific number if possible.
- Body (4-42 seconds): The actual content. Real steps or real data. No fluff.
- CTA (43-48 seconds): One line. Not "like and subscribe." Give a reason.

Topics for today's batch:
[paste 10 topics from your idea bank]

Rules:
- No em dashes
- No AI vocabulary (leverage, utilize, comprehensive, robust)
- Short sentences. Punchy. Lowercase energy.
- Use specific numbers always.
- Each script must stand alone as complete value.

Output: 10 numbered scripts in the exact format above.
```

**Time:** 2 minutes for the prompt + 3 minutes for Claude to generate + 5 minutes to quick-edit the best ones
**Output:** 10 scripts ready for voiceover

---

## PHASE 2: VOICEOVER GENERATION (15 minutes for 10 clips)

**Tool:** ElevenLabs
**Voice recommendation:** Adam (casual, authoritative) or Josh (energetic, younger)
**Settings:** Stability 0.5, Similarity 0.75, Style 0.4

**Workflow:**
1. Open ElevenLabs Speech Synthesis
2. Paste Script 1 body text (hook + body only, no CTA — add CTA as text on screen)
3. Generate. Download as MP3.
4. Paste Script 2. Generate. Download.
5. Continue until all 10 done.

**Speed tip:** Have the next script text ready to paste before the current generation finishes.
**Average generation time per clip:** 30-45 seconds
**Total time for 10 clips:** ~8 minutes generation + 7 minutes downloading/naming

**File naming convention:** `short_[date]_[number]_[2-word-topic].mp3`
Example: `short_20260305_01_cold-email.mp3`

**ElevenLabs character budget:**
- Average Short script: 300-400 characters
- 10 scripts: ~3,500 characters
- ElevenLabs Starter plan: 30,000 characters/month
- This batch: ~12% of monthly budget

---

## PHASE 3: VISUAL CREATION (20 minutes for 10 videos)

**Tool:** CapCut (desktop preferred for speed, mobile works)
**Template approach:** Use one base template and swap content

**CapCut setup for batching:**
1. Create a "Shorts Template" project
2. Set dimensions to 1080×1920
3. Background: solid black or dark gradient (loads fast, no rendering lag)
4. Font: Inter Bold or Montserrat Black, white text, 60-70pt
5. Save this as your base template

**For each Short:**
1. Import audio file (MP3 from ElevenLabs)
2. Add hook text as subtitle (first 3 seconds, large white text)
3. Add body captions (auto-generate from audio using CapCut auto-caption feature)
4. Add CTA text at end (last 5 seconds)
5. Optional: add one relevant B-roll clip (use Pexels free video search)
6. Export: 1080×1920, H.264, max quality

**Time per Short in CapCut:** 2 minutes once you have the template
**Total for 10 Shorts:** 20 minutes

**Auto-caption setup (do once):**
- CapCut → Text → Auto Captions → Language: English
- Style: Large, center-bottom, white with black outline
- Font: Montserrat Bold

---

## PHASE 4: UPLOAD & METADATA (15 minutes for 10 videos)

**Tool:** YouTube Studio (desktop)

**Upload all 10 videos first (bulk upload):**
1. YouTube Studio → Create → Upload
2. Select all 10 files at once
3. YouTube queues them all

**Metadata template for each (fill in the [brackets]):**

**Title:** [Hook line from script, max 60 characters]
Good example: "I made $300 this week with no inventory"
Bad example: "How I Make Passive Income Online 2026 (YouTube Shorts)"

**Description:**
```
[2-3 sentence summary of what the Short covers]

Tools mentioned:
- [Tool 1]: [URL or "link in bio"]
- [Tool 2]: [URL]

Follow for more [niche] breakdowns: [channel handle]

#YouTubeShorts #[niche] #[specific topic] #solopreneur
```

**Tags:** 5-8 tags max. Mix broad and specific.
Example: "youtube shorts", "make money online", "passive income 2026", "cold email", "solopreneur"

**Category:** Education (not "People & Blogs" — Education gets better placement)
**Made for Kids:** No
**Visibility:** Schedule (optimal times below)

---

## OPTIMAL SCHEDULING (10 Videos over 3-4 Days)

Don't upload 10 in one day. Spread them out for sustained algorithm push.

| Day | Time (EST) | Videos |
|-----|-----------|--------|
| Day 1 | 9:00 AM | #1, #2, #3 |
| Day 2 | 9:00 AM | #4, #5 |
| Day 2 | 7:00 PM | #6 |
| Day 3 | 9:00 AM | #7, #8 |
| Day 3 | 7:00 PM | #9 |
| Day 4 | 9:00 AM | #10 |

**Rationale:** YouTube Shorts gets a 48-hour "evaluation window" per video.
Posting too many simultaneously splits the algorithm attention.
3 per day max for new channels. 5 per day max for established channels.

---

## FULL SESSION TIMELINE

| Phase | Activity | Time |
|-------|----------|------|
| Prep | Open all tools, load template | 2 min |
| Phase 1 | Script generation (Claude) | 10 min |
| Phase 2 | Voiceover generation (ElevenLabs) | 15 min |
| Phase 3 | Video creation (CapCut batch) | 20 min |
| Phase 4 | Upload + metadata (YouTube Studio) | 15 min |
| **Total** | **10 Shorts ready** | **62 min** |

---

## COMMON BOTTLENECKS & FIXES

**Bottleneck: CapCut captions are wrong**
Fix: Use CapCut's manual caption editor. Spot-check first 5 seconds only. Let the rest auto-generate. Most viewers don't notice minor caption errors in the body.

**Bottleneck: ElevenLabs sounds robotic**
Fix: Add commas after natural pause points in the script. Commas = pauses = more natural cadence. Also try reducing Stability to 0.35 for more expressive delivery.

**Bottleneck: Videos take forever to export from CapCut**
Fix: Export one at a time. Don't queue multiple CapCut exports — it throttles. While one exports, work on YouTube metadata for previously exported videos.

**Bottleneck: Can't think of 10 topics**
Fix: Open reddit_deep_scraper.py output. Look at what questions people are asking in your niche this week. Every question = a Short. 10 topics in 5 minutes.

---

## FACELESS VERSION (No Camera Required)

This entire SOP works with zero on-camera presence:
- **Visual:** Screen recording of tools working OR text-on-screen with relevant B-roll
- **Audio:** ElevenLabs AI voice (Adam voice is indistinguishable from human in casual settings)
- **Face:** Never appears. Branding through style, not identity.

The 30 scripts in shorts_scripts_30.md are all designed for faceless production.
