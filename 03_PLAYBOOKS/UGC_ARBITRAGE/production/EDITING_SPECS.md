# UGC editing and delivery specs

Technical specifications for final deliverables.

---

## Video specifications

### Platform-specific specs

| Platform | Aspect ratio | Resolution | Max length | File size |
|----------|--------------|------------|------------|-----------|
| TikTok | 9:16 | 1080x1920 | 10 min | 287MB |
| Instagram Reels | 9:16 | 1080x1920 | 90 sec | 250MB |
| Instagram Feed | 1:1 or 4:5 | 1080x1080 or 1080x1350 | 60 sec | 250MB |
| YouTube Shorts | 9:16 | 1080x1920 | 60 sec | - |
| Facebook | 9:16 or 1:1 | 1080x1920 | 240 min | 4GB |
| Paid Ads (Meta) | 9:16, 1:1, 4:5 | 1080+ | 15-60s typical | - |

### Universal delivery specs

```
PRIMARY DELIVERY:

Format: MP4 (H.264 codec)
Resolution: 1080x1920 (vertical) minimum
Frame rate: 30fps (24-60fps acceptable)
Bitrate: 10-20 Mbps
Audio: AAC, 128kbps minimum, stereo

ALTERNATIVE (if needed):

Format: MOV (ProRes for high quality)
Resolution: 4K (3840x2160) if available
```

---

## Audio specifications

### Quality requirements

| Spec | Requirement |
|------|-------------|
| Format | AAC or WAV |
| Sample rate | 44.1kHz or 48kHz |
| Bit depth | 16-bit minimum |
| Channels | Stereo |
| Levels | -6dB to -3dB peak |
| Noise floor | Below -60dB |

### Audio checklist

- [ ] Voice clearly audible
- [ ] No background noise
- [ ] No clipping/distortion
- [ ] Consistent volume throughout
- [ ] No echo/reverb (unless intentional)
- [ ] Music doesn't overpower voice (if applicable)

---

## File delivery requirements

### What to request from creators

**Always include:**
1. Final edited video (ready to use)
2. Raw footage files
3. Alternate takes (if available)
4. B-roll footage (if shot)

**Optional extras:**
- Separated audio track
- Project file (if they edited)
- Behind-the-scenes content

### File organization

Request this structure:
```
[Brand]_[Creator]_[Date]/
├── FINAL/
│   ├── [Name]_Hook1_Final.mp4
│   ├── [Name]_Hook2_Final.mp4
│   └── [Name]_Hook3_Final.mp4
├── RAW/
│   ├── Take1.mov
│   ├── Take2.mov
│   └── ...
├── BROLL/
│   ├── Product_closeup.mov
│   └── Lifestyle_shot.mov
└── NOTES.txt (optional)
```

### File naming convention

```
[Brand]_[Creator]_[ContentType]_[Hook#]_[Version]_[Date]

Examples:
GlowSerum_JaneDoe_Testimonial_Hook1_v1_20240115.mp4
TechApp_JohnSmith_Tutorial_v2_FINAL_20240115.mp4
```

---

## Delivery methods

### Google Drive (recommended)

**Pros:** Free, easy sharing, folder organization
**Setup:** Create shared folder, send link to creator
**Tip:** Request they upload to your folder vs. sharing theirs

### Dropbox

**Pros:** Professional, reliable
**Cons:** Storage limits on free plan
**Best for:** Ongoing relationships

### WeTransfer

**Pros:** No account needed, easy for one-offs
**Cons:** Links expire (7 days free)
**Best for:** Single deliveries

### Frame.io (premium)

**Pros:** Built for video review
**Cons:** Paid service
**Best for:** High volume, agency operations

---

## Quality control checklist

### Before accepting delivery

**Technical:**
- [ ] Correct resolution (1080p minimum)
- [ ] Correct aspect ratio
- [ ] Acceptable file size
- [ ] No compression artifacts
- [ ] Audio synced to video

**Visual:**
- [ ] Subject in focus
- [ ] Adequate lighting
- [ ] Clean background
- [ ] Product visible and readable
- [ ] No unwanted items in frame

**Audio:**
- [ ] Voice clear and audible
- [ ] No background noise
- [ ] No echo or distortion
- [ ] Consistent levels

**Content:**
- [ ] All talking points covered
- [ ] Hooks as requested
- [ ] CTA included
- [ ] Brand name correct
- [ ] No compliance issues

---

## Common technical issues

### Problem: Video too compressed

**Symptom:** Blurry, pixelated
**Cause:** Creator exported at low quality or uploaded through messaging app
**Fix:** Request original file, have them send via proper delivery method

### Problem: Wrong aspect ratio

**Symptom:** Black bars, cropped content
**Cause:** Shot or exported in wrong format
**Fix:** Re-export at correct ratio or reshoot

### Problem: Audio out of sync

**Symptom:** Lips don't match words
**Cause:** Variable frame rate, editing error
**Fix:** Re-export with constant frame rate

### Problem: Lighting changes mid-video

**Symptom:** Brightness/color shifts
**Cause:** Auto-exposure or auto white balance
**Fix:** Lock exposure/WB settings, or reshoot

### Problem: File too large

**Symptom:** Can't upload to platforms
**Cause:** High bitrate or 4K when not needed
**Fix:** Re-export at lower bitrate, 1080p

---

## Post-delivery processing

### What you might do after receiving content

**Basic adjustments:**
- Trim heads/tails
- Adjust audio levels
- Add captions/subtitles
- Add brand intro/outro
- Color correction

**Platform optimization:**
- Export for different ratios
- Adjust length for platform
- Add platform-specific elements

**Performance optimization:**
- Create multiple cuts
- Test different hooks
- A/B test variations

---

## Tools for post-processing

### Free/Low cost
- CapCut (mobile and desktop)
- DaVinci Resolve (professional, free tier)
- Canva (basic video editing)

### Professional
- Adobe Premiere Pro
- Final Cut Pro
- After Effects (motion graphics)

### Captioning
- CapCut (auto-captions)
- Descript (AI transcription)
- Rev.com (human transcription)

### Batch processing
- HandBrake (format conversion)
- FFmpeg (command line)

---

## Archiving and storage

### Organization system

```
/UGC_ARCHIVE/
├── 2024/
│   ├── Q1/
│   │   ├── Client1/
│   │   │   ├── Campaign_Jan/
│   │   │   │   ├── FINAL/
│   │   │   │   └── RAW/
│   │   │   └── Campaign_Feb/
│   │   └── Client2/
│   └── Q2/
```

### Retention policy

- **Final files:** Keep indefinitely
- **Raw footage:** Keep 12 months minimum
- **Rejected takes:** Delete after final approval
- **Project files:** Keep 6 months

### Backup strategy

- Primary: Cloud storage (Google Drive, Dropbox)
- Secondary: External hard drive
- Critical: Both locations

---

## Spec sheet for creators

Send this to new creators:

```
TECHNICAL REQUIREMENTS

Video:
- Format: MP4 (H.264)
- Resolution: 1080x1920 minimum (vertical)
- Frame rate: 30fps
- No filters that alter natural appearance

Audio:
- Clear voice, no background noise
- Record in quiet environment
- Test audio before full recording

Delivery:
- Upload to: [Your Google Drive link]
- Include: Final video + raw footage
- Naming: [Brand]_[YourName]_[Date]

Quality check before sending:
- Watch full video with sound
- Check audio is clear
- Verify product name visible
- Confirm all talking points covered
```
