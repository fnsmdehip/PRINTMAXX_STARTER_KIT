# Icon Generation Status

## Ready to Generate

All 9 app icon prompts are competitor-informed and ready in:
- `/MONEY_METHODS/APP_FACTORY/assets/ICON_PROMPTS_V2.txt`

### Quick Commands

```bash
# Get specific app prompt (copy to Ideogram/Midjourney/DALL-E)
python3 scripts/generate_icons.py --prompt-only --app biomaxx

# List all apps
python3 scripts/generate_icons.py --list

# Try Gemini API (when quota resets at midnight Pacific)
python3 scripts/generate_icons.py --app biomaxx
```

### Free Generation Options

1. **Ideogram** (https://ideogram.ai) - 25 free images/day, excellent for icons
2. **Leonardo.ai** (https://leonardo.ai) - 150 free tokens/day
3. **Google AI Studio** (https://aistudio.google.com) - Use Gemini 2.0 Flash in web UI
4. **Midjourney** - If you have subscription
5. **Bing Image Creator** - Free with Microsoft account

### Apps Ready for Icon Generation

| App | Niche | Primary Color | Status |
|-----|-------|---------------|--------|
| BioMaxx | Biohacking | Emerald green | Pending |
| GlowMaxx | Looksmaxxing | Coral red | Pending |
| StepUnlock | Fitness/Steps | Electric green | Pending |
| DevotionFlow | Faith | Warm gold | Pending |
| PelvicPro | Women's Health | Pink/Purple | Pending |
| PromptVault | AI/Productivity | Blue/Purple | Pending |
| FocusPrayer | Faith/Focus | Gold | Pending |
| DailyAnchor | Faith/Habits | Blue/Gold | Pending |
| LearnLock | Education | Purple/Blue | Pending |

### Design System Applied

All prompts include:
- Competitor analysis (top 4-5 apps per niche)
- Differentiation strategy (what makes us stand out)
- Must include: 3D depth, glossy finish, glow effect, iOS style
- Must avoid: flat design, text/letters, cluttered symbols
- Technical: 1024x1024, recognizable at 60px

---

---

## V3 Lock Apps (HIGHEST PRIORITY - Blocking App Store Submission)

**Location:** `LOCK_APPS_ICON_PROMPTS_V3.md`

These are competitor-informed prompts for the 4 launch-ready apps:

| App | Status | Notes |
|-----|--------|-------|
| PrayerLock | NEEDS_GENERATION | Multi-faith universal design (golden lock + divine light). Old prayerlock-icon-1024.png is Christian-only flat design. |
| WalkToUnlock | NEEDS_GENERATION | Activity ring + footprint design. No existing icon. StepUnlock is different branding. |
| StudyLock | NEEDS_GENERATION | Book + Pomodoro timer ring. No existing icon. LearnLock is different branding. |
| BioMaxx | DONE (V2) | Existing biomaxx-icon-1024.png from V2 prompts. Copy to builds. |

**V3 improvements over V2:**
- Multi-faith PrayerLock (universal gold lock, no crosses/crescents)
- "Lock App Family" design system (shared visual DNA)
- Competitor analysis per app (specific differentiation strategy)
- Activity ring motif ties WalkToUnlock and StudyLock together
- Alternative prompts for each app if primary doesn't generate well

Last updated: 2026-02-03
