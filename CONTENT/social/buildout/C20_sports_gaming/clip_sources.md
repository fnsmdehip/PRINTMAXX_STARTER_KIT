# C20 Sports/Gaming Clips Channel — Legal Clip Usage Guide

## The Core Legal Framework

### Fair Use (US) — 4-Factor Test

| Factor | What It Means | How to Pass |
|--------|--------------|-------------|
| Purpose | Transformative > commercial | Add commentary, analysis, or criticism. Never repost raw clips. |
| Nature | Factual > creative | Sports game footage is partially factual (real events). |
| Amount | Less is better | 30-90 second clips only. Never full broadcast. |
| Market effect | Don't substitute | Your commentary video doesn't replace ESPN. |

**Safe harbor:** Every clip in this channel has commentary over it. No silent highlight reels. This is the line.

**Not a lawyer disclaimer:** This is operational guidance. Get actual legal advice before monetizing with >100K views.

---

## TIER 1: ZERO-RISK SOURCES

### Own Gameplay Footage
- **What:** Record your own game sessions
- **Tools:** OBS Studio (free), NVIDIA ShadowPlay (free with GPU), Xbox Game Bar (Windows built-in)
- **Best for:** Gaming concepts #11-20, comparison videos
- **Risk:** None

### Screen Recordings of Public Data/Tools
- **What:** Record your browser while showing pro-football-reference.com, basketball-reference.com, etc.
- **Tools:** OBS or Loom
- **Best for:** Stats-heavy sports videos #1, #2, #6
- **Risk:** None — recording public information

### Chess.com / Lichess Board Analysis
- **What:** Replay any public game on lichess.org or chess.com analysis board
- **Tools:** Screen record the analysis board
- **Best for:** Chess concepts #4, #16
- **Risk:** None — both platforms explicitly allow this

### Official MLB YouTube Channel
- **URL:** youtube.com/mlb (21M subscribers)
- **Policy:** MLB embeds clips with YouTube's standard embed policy — embedding is allowed
- **Best for:** Baseball concepts #3, #7
- **How:** Use YouTube's embed feature or link out in description. Do NOT download and re-upload.
- **Risk:** Low — embedding vs. downloading distinction

### Official NBA YouTube Channel
- **URL:** youtube.com/nba
- **Policy:** Same as MLB
- **Best for:** Basketball concepts #2
- **Risk:** Low for embedded, Medium for re-uploaded clips

---

## TIER 2: LOW-RISK SOURCES (Transformative Commentary)

### News Broadcast Clips
- **What:** News organizations (ESPN, Fox Sports) reporting ON events — press conferences, post-game interviews, referee explanations
- **Legal basis:** News commentary is explicitly protected under fair use factor 1 (transformative purpose)
- **Best for:** Referee analysis #5, analytical breakdowns
- **How to source:** ESPN YouTube channel clips of press conferences and analysis segments
- **Time limit:** Keep clips under 60 seconds
- **Risk:** Low — news clips under commentary protection

### Press Conference Footage
- **What:** Official team/league press conferences
- **Legal basis:** Generally public record, low copyright protection
- **Best for:** Sports concepts, player analysis
- **Where to find:** Team official YouTube channels, league official channels
- **Risk:** Very low

### Twitch Clips (For Commentary)
- **What:** Publicly clipped Twitch moments
- **URL:** clips.twitch.tv
- **Legal basis:** Transformative criticism (Twitch Gambling video #19)
- **Terms note:** Twitch clips are user-generated, creator owns copyright. Commentary = fair use defense.
- **Best for:** Gaming/streaming culture concepts
- **Risk:** Low-medium — add your commentary voice over clip

### Speedrun Footage
- **What:** Speedruns posted publicly to YouTube/Twitch
- **Sources:** speedrun.com, GDQ YouTube channel, individual runner channels
- **Legal basis:** Educational/transformative — breaking down technique
- **Best for:** Speedrun concept #11
- **Risk:** Low — reach out to runners first; most love the attention

---

## TIER 3: MEDIUM-RISK SOURCES (Handle With Care)

### NFL Game Footage
- **Owner:** NFL holds strict copyright on game footage
- **Policy:** NFL aggressively DMCA claims highlight reels
- **Safe approach:** Use ONLY official NFL YouTube embeds, or clips under 15 seconds with commentary
- **Safer alternative:** Use press conference clips instead of game footage
- **If you must:** Keep under 10 seconds, add clear transformative commentary, accept potential DMCA
- **Risk:** Medium — NFL is aggressive

### NBA Game Footage
- **Owner:** NBA / Turner Broadcasting
- **Policy:** More lenient than NFL but still active
- **Safe approach:** Official NBA clips under 30 seconds, with commentary
- **Safer alternative:** Use stat visualizations instead of game footage
- **Risk:** Medium

### Video Game Cutscenes/Story Content
- **Owner:** Game publishers (Nintendo is most aggressive, then Sony)
- **Policy:** Nintendo DMCA claims anything over 60 seconds of cutscenes
- **Safe approach:** Gameplay footage (generally protected) vs. story cinematics (higher risk)
- **Nintendo specifically:** Avoid any monetized video using more than 30 seconds of Nintendo cutscene footage
- **Risk:** Medium for Nintendo, Low for most other publishers

### Esports Tournament Footage
- **Owner:** Tournament organizers (Riot, Valve, ESL)
- **Policy:** Varies significantly by organizer
- **Riot/League:** Has a content creator policy — review riot's policies page before using
- **Valve/Dota:** More lenient, no structured policy
- **CS:GO/CS2:** ESL clips available under press license
- **Safe approach:** Keep clips under 60 seconds with commentary, link to official VOD
- **Risk:** Low-medium depending on publisher

---

## TIER 4: HIGH-RISK — AVOID

### Full Game Broadcasts
- Full ESPN/Fox Sports broadcasts — NEVER use
- Pay-per-view event footage — NEVER use
- NFL RedZone clips — NEVER use

### Music in Sports Arenas
- Goal celebrations with arena music playing — copyright for the MUSIC, not just the event
- Any clip with recognizable copyrighted songs in background — mute or avoid

### Pay-Per-View Sports
- Boxing/UFC PPV footage — extremely aggressive legal teams
- WWE content — copyrighted and actively monitored

---

## The Clip Workflow (Safe Operations)

### Step 1: Source Identification
```
Before downloading any clip, classify it:
- Tier 1? → Use freely
- Tier 2? → Add commentary before uploading
- Tier 3? → Keep short, add commentary, accept risk
- Tier 4? → Find alternative
```

### Step 2: Download Tools
```bash
# YouTube clips (fair use segments only)
yt-dlp --download-sections "*00:01:30-00:02:15" "https://youtube.com/watch?v=..." -o "clip.mp4"

# Twitch VOD clips
yt-dlp "https://clips.twitch.tv/ClipName" -o "clip_name.mp4"

# Speedrun videos
yt-dlp --download-sections "*HH:MM:SS-HH:MM:SS" "URL" -o "speedrun_segment.mp4"
```

### Step 3: Commentary Coverage
- Every clip MUST have your voice commentary playing over it
- Add on-screen text analysis
- No silent clips of any duration — this is what makes it transformative

### Step 4: YouTube Upload Settings
- In YouTube description: "Clips used under fair use for educational/commentary purposes"
- Add timestamps showing which portions are your content vs. referenced clips
- Keep clips under 60 seconds total per 10-minute video

---

## DMCA Response Protocol

**If you receive a Content ID claim (most common):**
1. Review the claim — most are automatic, not manual
2. If your video is clearly transformative: file a dispute with your fair use reasoning
3. If unsure: accept the claim (they get ad revenue, not you — video stays up)
4. Never delete disputed videos — this forfeits your defense

**If you receive a manual DMCA takedown:**
1. Review if the claim is valid
2. If fair use applies: file a counter-notification (you accept legal liability)
3. If unsure: re-edit the video to remove the specific clip and re-upload

**Track record:** Gaming commentary channels (MoistCr1tikal, penguinz0) operate for years on transformative commentary. Sports data channels (Ben Falk, The Ringer) rarely get taken down. Follow their clip usage patterns.

---

## Recommended Starting Sources (Zero to Low Risk)

For your first 20 videos, use ONLY:
1. Own gameplay recordings
2. Screen recordings of public stats sites
3. Chess.com/lichess analysis boards
4. Official league YouTube embeds (embed, don't download)
5. Data visualizations you create yourself (Canva, Python matplotlib)

This covers all 10 gaming concepts and 6 of 10 sports concepts cleanly. Add Tier 2 sources once channel is established and you understand what content ID hits on.
