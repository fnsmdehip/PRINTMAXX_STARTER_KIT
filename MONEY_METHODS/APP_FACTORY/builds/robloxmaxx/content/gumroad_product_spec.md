# Gumroad product spec: AI Roblox Game Builder Kit

## Product details

**Name:** AI Roblox Game Builder Kit
**Slug:** roblox-game-builder-kit
**Price:** $0+ (free with email capture, suggested $19)
**Premium upsell:** $49 (5-genre mega pack)
**Platform:** Gumroad (or Whop)
**Category:** Game Development / Templates / AI Tools

---

## Landing page copy

### Headline

i built a complete Roblox game in 2 hours with AI. here are the exact scripts and prompts.

### Subheadline

8 production-ready Luau scripts. 5 gamepasses. 4 dev products. pet system. rebirth system. full DataStore persistence. paste into Studio and play.

### Body

most Roblox tutorials teach you one script at a time. you spend weeks learning how to make a basic tycoon.

i skipped all that.

i used Claude AI to generate 8 complete game scripts in one session. Pet Factory Tycoon: droppers, upgraders, pet hatching, rebirth prestige, gamepasses, developer products, client UI, and a one-paste installer that sets up the entire game in Studio.

this kit gives you everything:

**the 8 scripts (ready to paste)**
- GameConfig.lua: every number in one file. change theme in 5 minutes.
- DataManager.lua: save/load with DataStoreService. retry logic. session locking.
- TycoonManager.lua: plot claiming, purchases, dropper loops.
- PetSystem.lua: egg hatching, equipping, passive multipliers.
- RebirthManager.lua: prestige system with permanent bonuses.
- EconomyManager.lua: currency, gamepasses, dev product processing.
- TycoonHUD.lua: client-side UI for currency, shop, pet display.
- GameInstaller.lua: one paste into command bar. entire game deploys.

**the customization guide**
- how to reskin for any theme (pizza tycoon, mining tycoon, anime tycoon)
- economy balancing principles (cost curves, multiplier stacking)
- how to add new droppers, pets, eggs, gamepasses in GameConfig
- monetization pricing guide based on actual Roblox player spending data

**the AI prompts**
- the exact prompts used to generate each script
- genre-specific prompt templates (tycoon, obby, simulator)
- how to iterate: what to ask AI when something breaks
- prompt patterns that produce modern Luau (not legacy Lua 5.1)

**the monetization setup**
- how to create gamepasses and dev products via Roblox Open Cloud API
- pricing psychology for Roblox audience (mostly 8-16 year olds)
- gamepass tier strategy (99 to 399 Robux sweet spot)
- developer product repeat-purchase design

### Social proof section

"built a playable tycoon in under 2 hours. 7 dropper tiers, 16 pets, 5 gamepasses. all from AI-generated scripts."

"the GameInstaller pattern is genius. paste once, everything sets up. iterate in your editor, re-paste, test. 10x faster than dragging scripts around Studio."

"economy balancing was better than most games i've played. exponential curves, weighted rarity, rebirth multipliers. AI understood tycoon psychology."

(Note: use real testimonials from beta testers once available. these are placeholder descriptions of actual outcomes.)

### Pricing section

**Free tier ($0 with email)**
- all 8 Luau scripts
- basic customization guide
- GameInstaller pattern

**Starter ($19)**
- everything in Free
- AI prompt templates for tycoon genre
- monetization setup guide
- economy balancing spreadsheet
- discord access for support

**Mega Pack ($49)**
- everything in Starter
- 5 genre templates (tycoon, obby, simulator, RPG, horror)
- 40+ AI prompts across all genres
- GameConfig variants for 10 themes per genre
- MCP integration guide (Claude Code to Studio bridge)
- lifetime updates as new genres are added
- priority discord support

### CTA

get the kit. paste the installer. playtest in 5 minutes.

---

## Product contents (file structure)

```
AI-Roblox-Game-Builder-Kit/
├── README.md                          # Start here
├── scripts/
│   ├── GameConfig.lua                 # All game numbers
│   ├── DataManager.lua                # Save/load
│   ├── TycoonManager.lua              # Core gameplay
│   ├── PetSystem.lua                  # Pet collection
│   ├── RebirthManager.lua             # Prestige system
│   ├── EconomyManager.lua             # Monetization
│   ├── TycoonHUD.lua                  # Client UI
│   └── GameInstaller.lua              # One-paste setup
├── guides/
│   ├── CUSTOMIZATION_GUIDE.md         # Reskinning for any theme
│   ├── MONETIZATION_SETUP.md          # Gamepasses + dev products
│   ├── ECONOMY_BALANCING.md           # Cost curves + multipliers
│   └── STUDIO_SETUP.md               # Step-by-step Studio instructions
├── prompts/
│   ├── TYCOON_PROMPTS.md              # Tycoon generation prompts
│   ├── OBBY_PROMPTS.md                # (Starter+)
│   ├── SIMULATOR_PROMPTS.md           # (Starter+)
│   ├── RPG_PROMPTS.md                 # (Mega Pack)
│   ├── HORROR_PROMPTS.md              # (Mega Pack)
│   └── ITERATION_PROMPTS.md           # Fixing + extending
├── themes/                            # (Mega Pack)
│   ├── pizza_tycoon_config.lua
│   ├── mining_tycoon_config.lua
│   ├── anime_tycoon_config.lua
│   ├── space_tycoon_config.lua
│   └── ... (10 per genre)
└── tools/
    ├── create_gamepasses.py            # Open Cloud API script
    ├── create_devproducts.py           # Open Cloud API script
    └── MCP_SETUP.md                   # (Mega Pack) Claude Code bridge
```

---

## Gumroad settings

**URL:** gumroad.com/l/roblox-game-builder-kit
**Thumbnail:** screenshot of Pet Factory Tycoon in Studio with code overlay
**Tags:** roblox, game development, lua, luau, tycoon, AI, vibecoding, templates
**Ratings:** enable
**Discover:** enable (Gumroad marketplace visibility)
**Email capture:** required for free tier
**Workflow:** purchase triggers Beehiiv "roblox-builders" tag for newsletter

---

## Upsell funnel

1. Free kit ($0 + email) via Twitter/Medium/Reddit
2. Email sequence (3 emails over 5 days):
   - Day 0: "your scripts are ready" + quick start guide
   - Day 2: "how i monetized a Roblox game in one session" + Starter upsell
   - Day 5: "5 genres, 50 templates" + Mega Pack upsell
3. Mega Pack buyers get discord invite + priority support
4. Discord community becomes social proof engine for more free kit downloads
5. Repeat with new genre releases

---

## Revenue projections

**Conservative (first 30 days):**
- 500 free downloads (email capture)
- 10% convert to Starter ($19): 50 x $19 = $950
- 5% convert to Mega Pack ($49): 25 x $49 = $1,225
- Total: $2,175 + 500 email leads

**Moderate (first 90 days):**
- 2,000 free downloads
- 200 Starter sales = $3,800
- 100 Mega Pack sales = $4,900
- Total: $8,700 + 2,000 email leads

distribution channels: X/Twitter thread, Medium article, Reddit (r/robloxgamedev, r/roblox, r/gamedev), Roblox DevForum, TikTok dev content, YouTube tutorial.

---

## Competitor analysis

| Product | Price | What they offer | Our edge |
|---------|-------|-----------------|----------|
| Roblox DevForum tutorials | Free | One script at a time, outdated Lua 5.1 | Complete game in one kit, modern Luau |
| Udemy Roblox courses | $20-80 | Video courses, slow paced | Scripts you can paste and play immediately |
| Ropilot.ai | Free/$15/mo | AI code gen but no full games | Full game templates with monetization built in |
| Generic YouTube tutorials | Free | Hours of video for basic games | 5 minutes from download to playable game |

the main edge: nobody else gives you a complete, monetized, production-ready game you can paste into Studio and play in 5 minutes. everyone else teaches you one concept at a time over weeks.
