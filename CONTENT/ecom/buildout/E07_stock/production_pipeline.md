# E07 AI Stock Footage — Production Pipeline

## FULL STACK: $0 to 500 Clips in 90 Days

### Tool Stack (Minimum Viable)
| Tool | Monthly Cost | Purpose | Output Rate |
|------|-------------|---------|-------------|
| Kling AI (free tier) | $0 | 5s clips, 5 per day free | 25 clips/week |
| Pika Labs (free tier) | $0 | 3s clips, 5 per day | 15 clips/week |
| CapCut (free) | $0 | Loop extension + color grade | 40 clips/week |
| Canva (free) | $0 | Thumbnail/preview | - |
| ExifTool | $0 | Metadata batch embed | - |
| **Total free tier** | **$0** | | **40 clips/week** |

### Upgraded Stack (Month 2 if revenue hitting)
| Tool | Monthly Cost | Upgrade |
|------|-------------|---------|
| Runway Gen-2 Standard | $15 | 125 credits/mo, better quality |
| Kling AI Standard | $10 | 300 credits/mo, 5-10s clips |
| Adobe Creative Cloud (Bridge) | $55 | Batch metadata + Premiere |
| **Total upgraded** | **$80/mo** | 200+ clips/week potential |

---

## STEP-BY-STEP PRODUCTION WORKFLOW

### Phase 1: Concept Selection (15 min)
1. Open `footage_concepts_30.md`
2. Pick 10 concepts from highest-demand batch (Batch D Abstract first)
3. Note template multiplier variants to generate (4-6 per concept)

### Phase 2: AI Generation (60-90 min for 10 clips)

**Kling AI workflow:**
1. Go to klingai.com → Video Generation
2. Set: 5 seconds, 720p (free) or 1080p (paid), no negative prompts needed for abstract
3. Paste prompt from concepts file
4. Queue 5 at a time (free limit)
5. Download as MP4

**Pika Labs workflow:**
1. Go to pika.art → Generate
2. Text-to-video
3. Paste prompt, select 3 seconds, 1080p
4. Generate 5 simultaneously
5. Download

**Runway Gen-2 workflow (paid):**
1. runwayml.com → Gen-2
2. Text to Video
3. Set: 4 seconds, HD
4. Use 10 credits per clip (125 credits/mo Standard = 12 clips/mo)
5. Download

### Phase 3: Post-Production (30-45 min per 10 clips)

**Loop Extension in CapCut (Free):**
1. Import raw clip (3-5 seconds)
2. Duplicate clip 3-4 times to reach 10-15 seconds
3. Add fade crossblend between clips for seamless loop
4. Export: MP4, H.264, 1080p, 30fps, ~50 Mbps bitrate

**Seamless Loop Trick:**
- For abstract/particle clips: reverse duplicate works well
  - Clip A → Clip A reversed → Clip A → creates perfect palindrome loop
- For nature clips: crossfade at 0.5s overlap

**Color Grading (optional but increases sales):**
- LUTs: download free cinematic LUTs from LUTRobot.com
- Apply in CapCut: Effects → LUT → apply subtle grade
- Don't over-process — natural = more versatile for buyers

**Vertical Variant (1080x1920):**
- In CapCut: change canvas to 9:16
- Center reframe the clip (most abstracts work fine)
- Export as separate file with "_vertical" suffix

### Phase 4: Metadata Writing (30 min per 10 clips)

**Fill this template for each clip:**

```
CLIP: [Concept number + variant name]
FILE: concept_XX_[color/variant].mp4
TITLE: [60-70 chars, most specific keyword first]
DESCRIPTION: [150-200 chars, describe what you see + loop/duration]
CATEGORY: [Shutterstock category]
KEYWORDS: [50 keywords, comma-separated, most specific first]
```

**Keyword expansion formula:**
1. Start with concept-specific (5 keywords)
2. Add visual descriptors (10 keywords)
3. Add use-case/where-used keywords (10 keywords)
4. Add style/mood keywords (10 keywords)
5. Add broad catch-all keywords (15 keywords)

**Example — Concept 24 (Bokeh Lights):**
```
TITLE: soft gold bokeh lights abstract background, seamless loop 4K
DESCRIPTION: Soft circular gold and white bokeh lights gently moving against dark background. Seamless loop. Perfect for presentations, social media, and wedding video backgrounds. 4K.
CATEGORY: Abstract / Backgrounds
KEYWORDS: bokeh lights, abstract background, gold bokeh, light bokeh, bokeh background, blurry lights, defocused lights, seamless loop, video background, motion background, wedding background, christmas lights background, party background, celebration background, holiday background, soft lights, circular lights, glowing lights, warm bokeh, golden bokeh, abstract motion, background footage, loop background, video loop, animated background, stock footage loop, background video, blur bokeh, lens bokeh, out of focus lights, sparkle background, twinkle lights, fairy lights blur, romantic background, luxury background, presentation background, slide background, social media background, instagram background, youtube background, vlog background, video template, bokeh effect, bokeh overlay, light overlay, atmosphere background, cozy background, warm atmosphere, warm tones background, golden hour bokeh, soft focus
```

### Phase 5: Batch Upload (45 min per 40 clips)

**Shutterstock Batch Upload:**
1. Portal.shutterstock.com → Submit Content → Video
2. Upload all clips simultaneously (drag and drop)
3. SS auto-reads embedded IPTC metadata (use ExifTool beforehand)
4. Review queue: typically approved within 1-3 business days
5. Rejected? Check: resolution, bitrate, content restrictions

**ExifTool IPTC embed command (batch):**
```bash
# Single file
exiftool -IPTC:ObjectName="soft gold bokeh lights abstract background" \
         -IPTC:Caption-Abstract="Soft circular gold bokeh..." \
         -IPTC:Keywords="bokeh lights,abstract background,gold bokeh" \
         video.mp4

# Batch (all MP4 in folder)
exiftool -IPTC:Keywords="keyword1,keyword2,keyword3" *.mp4
```

**Adobe Stock Batch Upload (via Bridge):**
1. Open Adobe Bridge
2. Select all video files
3. Tools → Adobe Stock Contributor → Upload and Submit
4. Fill metadata in Bridge info panel before upload
5. Approved within 1-5 business days

---

## 90-DAY PRODUCTION CALENDAR

### Month 1: Foundation (Target: 120 clips live)
| Week | Task | Clips Generated | Clips Uploaded |
|------|------|----------------|----------------|
| 1 | Learn tools, generate batch D (abstract) | 30 | 30 |
| 2 | Batch D variants (color/vertical) | 40 | 40 |
| 3 | Batch A (business/tech) | 30 | 30 |
| 4 | Batch A variants | 20 | 20 |
| **Month 1 Total** | | **120** | **120** |

Revenue month 1: $0 (clips in review, starting to go live)

### Month 2: Scale (Target: +200 clips = 320 total)
| Week | Task | Clips |
|------|------|-------|
| 5 | Batch B (nature) | 30 |
| 6 | Batch B variants | 40 |
| 7 | Batch C (lifestyle - AI illustrated) | 30 |
| 8 | Batch C variants | 40 |
| **Month 2 Total** | | **+140** |

Revenue month 2: $200-400/mo (month 1 clips earning)

### Month 3: Compound (Target: +200 clips = 520 total)
| Week | Task |
|------|------|
| 9-12 | New concepts outside the 30 (trending searches: AI, Ramadan, summer) |
| Research trending: Shutterstock trending search data from SS Blog |

Revenue month 3: $600-1,000/mo

---

## TRENDING SEARCH INTELLIGENCE

### Where to Find What Buyers Are Searching
1. **Shutterstock trends:** shutterstock.com/trends (free, updated regularly)
2. **Adobe Stock Trends:** adobe.com/creativecloud/photography/discover/stock-trends.html
3. **Google Trends (video searches):** trends.google.com → compare terms
4. **Pond5 Editorial:** their "Collections" show trending themes

### Current High-Demand Searches (2026)
- AI and technology visualizations
- Mental health and wellness imagery
- Diverse and inclusive business settings
- Sustainable/green energy
- Ramadan and Islamic geometric patterns (seasonal, March-April peak)
- Remote work lifestyle
- Cryptocurrency and fintech
- Neuroscience / brain visualization
- Space and cosmos
- Minimalist abstract backgrounds

### Seasonal Calendar
| Month | Trending Searches | Plan Ahead |
|-------|------------------|------------|
| Jan | New Year, goals, fresh start | Upload Dec |
| Feb | Valentine's Day, love | Upload Jan |
| Mar | Spring, Ramadan (2026), Easter | Upload Feb |
| Apr | Earth Day, nature | Upload Mar |
| May | Graduation, Mother's Day | Upload Apr |
| Jun | Pride, Summer, Father's Day | Upload May |
| Jul-Aug | Summer, beach, travel | Upload Jun |
| Sep | Back to school, Fall | Upload Aug |
| Oct | Halloween, Autumn | Upload Sep |
| Nov | Thanksgiving, Black Friday | Upload Oct |
| Dec | Christmas, Hanukkah, New Year | Upload Nov |

---

## QUALITY STANDARDS CHECKLIST

Before uploading any clip:

**Technical:**
- [ ] Resolution: 1920x1080 minimum (3840x2160 preferred)
- [ ] Bitrate: 10 Mbps minimum (50+ Mbps for 4K)
- [ ] Frame rate: 23.98, 24, 25, 29.97, or 30 FPS (consistent, no mixed)
- [ ] Duration: 5-30 seconds (10-15 optimal)
- [ ] No artifacts, banding, or visible compression
- [ ] Loops seamlessly (if loop)
- [ ] No watermarks, no text overlays
- [ ] No brand logos visible
- [ ] No real people (or clear model release)
- [ ] AI disclosure checked on platform

**Metadata:**
- [ ] Title: specific, 60-70 chars, keyword-first
- [ ] 50 keywords filled
- [ ] Description: 150-200 chars, descriptive
- [ ] Category correctly assigned
- [ ] AI generated tag applied

**Content:**
- [ ] Commercially viable subject matter
- [ ] No political content
- [ ] No trademarks/logos
- [ ] No copyrighted characters
- [ ] "No people" OR illustrated/silhouette style

---

## INCOME ACCELERATION TACTICS

### 1. Series Packs
Upload 5-10 clips in same visual style as a series.
SS and Adobe surface series together, boosting organic discovery per clip.
Example: "Colorful Bokeh Lights Pack" — gold, red, blue, purple, white (5 clips in series).

### 2. Seasonal Front-Running
Upload 4 weeks BEFORE a seasonal event.
SS/Adobe need 1-2 weeks review, then you get the seasonal traffic wave.

### 3. Trending Keyword Injection
Every week, check SS Trending and incorporate 2-3 trending keywords into new uploads.
Even if clip isn't specifically that topic, adjacent keywords get you adjacent impressions.

### 4. Cross-Platform Arbitrage
Same clip earns differently per platform.
A $0.25 SS clip might earn $3.00 on Adobe Stock if the right buyer finds it.
Upload everywhere, see which platform earns more per clip, double down there.

### 5. Premium Pricing on Pond5
Pond5 lets you set price. Test $30-80 for premium abstract loops.
One Enhanced License sale ($79) = 316 Shutterstock standard DLs equivalent.

### 6. Clip Repurposing for Shorts/Reels
Use your own stock library as B-roll for YouTube/TikTok content.
Content about "I make $X from AI stock footage" = huge traffic + converts to portfolio sales.
This is the flywheel: stock footage business funds content machine, content machine drives stock sales.
