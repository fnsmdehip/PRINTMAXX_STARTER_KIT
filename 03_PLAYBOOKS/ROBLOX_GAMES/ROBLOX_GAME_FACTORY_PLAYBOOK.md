# Roblox Game Factory Playbook

**Last Updated:** 2026-01-24
**Status:** Deep research complete, ready for implementation
**Revenue Potential:** $1k-$100k+/month

---

## The Opportunity

**Platform Stats (Q4 2025):**
- 151.5M daily active users (70% growth YoY)
- 381.8M monthly active users
- $3.6B platform revenue (2024)
- $1B+ paid to creators (9 months of 2025)
- 44M+ games/experiences
- DevEx Rate: $3.80 per 100K Robux (increased from $3.50)

**Developer Earnings:**
| Tier | Annual Earnings |
|------|-----------------|
| Top 10 | $33.9M average |
| Top 100 | $6M-7M average |
| Top 500 | $200k+ each |
| Top 1000 | $820k-980k average |
| Median | $1,440/year |

**Your edge:** Claude Code Max + Roblox Studio MCP = Build games via prompts overnight.

---

## Section 1: CURRENT META (Jan 2026)

### What's Actually Hot RIGHT NOW

**Record Breakers:**

| Game | Peak CCU | Key Mechanic | Why It Works |
|------|----------|--------------|--------------|
| **Steal a Brainrot** | 25.8M (all-time record) | AFK + PvP theft | Meme virality + controversy + simple loop |
| **Grow A Garden** | 21.6M | AFK farming | True AFK-friendly, weekly events |
| **The Forge [BETA]** | 623K active, 96% approval | Crafting/building | High quality, deep mechanics |

**Rising Fast (Watch These):**
- **Basketball Showdown** - 16M+ visits, 98% rating, launched Dec 2024
- **Strongest Battlegrounds** - 10.29B visits, entered top 10 recently
- **Plants vs. Brainrots** - Riding the brainrot wave

### The Steal a Brainrot Formula (Deep Analysis)

This game broke every record. Here's exactly how it works:

**Core Loop:** Acquire → Grow → Defend → Steal
1. Players start with base + small currency
2. Buy brainrots from conveyor (price rises as others buy)
3. Brainrots generate passive income every few seconds
4. Can steal from other players' UNLOCKED bases
5. When stolen, thief is slowed + vulnerable to attacks
6. Attack a thief = brainrot returns to original owner
7. Shield button provides temporary defense
8. Rebirth system = reset for better stats (lock time increases 10s per rebirth)

**Why 25M CCU:**
- Meme-based (brainrot meme = viral content)
- Latin America dominance (huge Spanish/Portuguese audience)
- Developer beef attracted media coverage
- Simple enough for kids, deep enough for grind
- Social clips went viral on TikTok
- Pay-to-win elements drive revenue (controversial but profitable)

**Monetization Stack:**
- Robux to drop enemy lasers
- Lucky Boxes with random drops (gambling mechanics)
- Server Luck gamepass (increase rare spawn rate, 2200+ Robux)
- Cosmetics and mutations (1.25x to 10x income multipliers)

**Won:** Best Creative Direction at 2025 Roblox Innovation Awards

### Genre Performance Data

| Genre | Daily Visits | Trend |
|-------|--------------|-------|
| Simulation | 110M | Growing |
| Roleplay & Avatar Sim | 116M | Stable/Growing |
| Platformers | 70M | Saturated |
| Survival | 70M | Stable |
| Action | 59M | Stable |

**Key Insight:** Simulation games win because monetization + LiveOps loops drive higher LTV. Pure platformers struggle with monetization.

---

## Section 2: DYING META (What to Avoid)

### Oversaturated/Declining

**Generic Simulators**
- "X Simulator" format is played out
- Need unique angle or you're invisible
- Exception: Niche targeting (faith, fitness) still works

**Legacy Anime Battlers**
- Crowded market
- New entrants struggle without IP or competitive edge
- Exception: Basketball Showdown succeeded with anime IP (Kuroko No Basuke)

**Pure Obby/Parkour**
- 70M daily visits but fragmented across thousands of games
- Low monetization compared to tycoons
- Hard to stand out

**Open-World RPGs**
- Too expensive to build
- High technical bar
- Casual players quit (20+ hours to "get good")

### Why Games Die

1. **No updates** - 2+ week gap = 20% player drop-off
2. **High barrier** - Need massive content to compete with established games
3. **Wrong monetization** - Too aggressive (kills retention) or too passive (no revenue)
4. **Build in isolation** - No marketing until launch

---

## Section 3: NEW MECHANICS THAT WORK

### Platform-Level Changes (2025)

**Roblox Moments (TikTok Clone) - CRITICAL**
- 30-second vertical video clips
- Tap-to-join from clips = instant game launch
- Games optimized for clip-able moments are favored by algorithm
- **Build for Moments:** Design "screenshot moments" and highlight-worthy gameplay

**AI Creator Tools (Sept 2025)**
- Procedural object generation ("Generate a red sports car" → playable object)
- Real-time voice translation (multi-language without dev overhead)
- Reduces art bottleneck for small teams

**Server Authority Mode**
- Native anti-cheat mode
- Better physics for skill-based gameplay
- Reduces exploits in competitive games

### Winning Mechanics from Top Games

**From Steal a Brainrot:**
- Spawn-based PvP theft + persistent storage
- Dynamic pricing on central marketplace (creates scarcity pressure)
- Meme-character cosmetics (collecting variants)
- Rebirth = reset for stats (simple but addictive)

**From Grow A Garden:**
- True AFK-friendly (no punishment for offline time)
- Pet interactions (cosmetic layer drives engagement)
- Casual farming appeal (attracts non-hardcore players)
- Weekly events timed to cultural moments

### What AI/Vibe Coding CAN'T Do Well

**Hard/Limited:**
- Complex procedural generation (Luau not optimized for Perlin noise at scale)
- Advanced graphics (limited to mobile performance)
- Real-time collaboration tools
- In-game LLMs (need external APIs)
- Large open worlds (streaming terrains supported but performance drops)
- Custom networking (must use Roblox's built-in Remotes)

**AI Specific Problems:**
- Doesn't understand Roblox Studio quirks
- Struggles with scripts over 300 lines (loses context)
- Can't handle animation, modeling, or terrain generation well
- Security exploits = AI can't fix when you have 20k lines of Lua
- Hallucinations when rewriting modules

**Best Practices for Vibe Coding:**
- Keep individual modules under 300 lines
- Split logic aggressively
- Avoid custom 3D models and animation systems
- Keep game simple if you're new
- Always backup before AI overwrites
- Use AI as tool, not crutch

---

## Section 4: MONETIZATION (What's Working NOW)

### The 2026 Winning Stack

**Gamepass Tiers (60% of revenue):**
| Tier | Price | Perks |
|------|-------|-------|
| Entry | $4.99 | +5% daily passive income |
| Mid | $9.99 | +10% + daily Robux bonus |
| Premium | $19.99 | +20% + exclusive pets + priority queue |

**Dev Products (25% of revenue):**
- Limited cosmetics (NOT P2W)
- Currency bundles ($0.99-$9.99)
- One-time leveling boosters (not permanent edge)
- Lucky Boxes (controversial but profitable)

**Creator Fund Payouts (15% of revenue):**
- 70% to creator, 30% to Roblox
- Extra payout if game drives new DAUs

### New Revenue Opportunities

**Regional Pricing** - Same pass = lower price in Brazil/India, higher in US
**Rewarded Video Ads** - "Watch 30s ad for 50 Robux boost" (~40-50% watch rate)
**Creator Rewards Program** - Bonus for driving new users

### What's NOT Working

- Aggressive P2W paywalls (kills retention)
- Too many cosmetics (overwhelms monetization UI)
- Premium-only features (players feel gated)
- Forcing purchases to progress (younger audience = parents block spending)

---

## Section 5: COMMUNITY BUILDING (What Actually Works)

### Discord Strategy (From Successful Devs)

**Daily Operations:**
- Post patch notes/content updates every 1-2 days
- Exclusive cosmetics for Discord members (small reward = server growth)
- Community voting on features (players feel ownership)
- Streamer program with revenue share (% of viewers' purchases, not lump sum)

**Structure:**
- Clear rules (68% of successful communities attribute growth to transparent codes of conduct)
- Hybrid content: structured tutorials + freeform brainstorming
- Target 13-18 age range (60% of Roblox DevForum users)

### Update Cadence (Critical)

| Frequency | Content |
|-----------|---------|
| Daily/Every-other-day | Status updates, small fixes |
| Weekly | Content update (new items, areas, events) |
| Bi-weekly | Cosmetic drops |
| Monthly | Major balance patches, new mechanics |
| Real-time | Meta shift hotfixes |

**Warning:** Games with 2+ week gaps see ~20% player drop-off

### Social Strategy (Cross-Platform)

**TikTok/YouTube Shorts (Highest ROI):**
- Developers themselves post 3-5 clips per week
- Don't rely on influencers alone
- Short clips (15-30s) of unique moments or memes
- Build for Moments (Roblox's TikTok clone)

**Reply-Guy Strategy:**
- Engage under trending Roblox posts with game clips/gifs
- Be present where players talk

**Influencer Seeding:**
- Give 50-100 micro creators ($10-50k followers) early access
- Micro > Macro for ROI
- Cost: $50-500 per collab = $5-10K total for 50K+ impressions

**What Doesn't Work:**
- Generic Discord (no exclusive value)
- Sporadic updates
- Waiting for organic YouTube coverage
- Facebook Gaming (declining Roblox presence)

---

## Section 6: MARKETING CHANNELS (Where Players Come From)

### Ranked by Effectiveness

**1. TikTok Organic (Highest ROI if viral)**
- 1 in 5 game videos mention Roblox
- 1 trillion all-time YouTube views for Roblox content
- Key: Controversial/unique games get coverage (Steal a Brainrot beef drove media)

**2. Roblox Home Page Discovery (90% of new traffic)**
- Algorithm favors: Frequent updates, high retention, positive ratings
- Moments clips appear on Home page
- Update weekly minimum

**3. In-Game Moments (TikTok Clone) - NEW**
- Clip shared → Moments viewers can tap → instant join
- Could become biggest discovery channel by Q2 2026

**4. YouTube (Long-Tail)**
- 105+ Roblox creators with 100K+ subs
- Higher LTV (older audience, spends more)
- Developer channels outperform generic gaming channels

**5. Influencer/Creator Seeding**
- Micro-creators (10K-100K): $50-500 per collab
- Top creators: expensive lump sums or %

**6. Roblox Ads Platform**
- $0.01-$0.10 per click
- Reality: Whales have infinite budget, small devs compete poorly

**7. Reddit/Twitter**
- Good for brand building, not direct launches
- r/robloxgamedev: dev-focused, not players

---

## Section 7: NICHE DIFFERENTIATION (Your Edge)

### Why Niche Wins

- 70% of Roblox players are 9-16 years old
- Underserved segments have less competition
- Parents approve educational/faith games
- Specific communities are more loyal

### Niche Adaptation Table

| Popular Game | Niche Version | Differentiation | Target Audience |
|--------------|---------------|-----------------|-----------------|
| Steal a Brainrot | Steal a Virtue | Collect virtues, defend from sins | Faith kids |
| Grow A Garden | Grow A Prayer Garden | Faith themes, Bible verses as rewards | Faith families |
| Pet Simulator | Fitness Pet | Pet evolves based on steps/activity | Fitness kids |
| Generic Obby | Study Obby | Quiz gates between stages | Parents/Education |
| Roleplay | Church Community RP | Faith-based social | Faith teens |
| Tycoon | Startup Tycoon | Business education, real concepts | Ambitious teens |
| Basketball Showdown | Faith Sports | Christian athletes, clean content | Sports + faith |

### Portfolio Approach

Don't bet on one game:
- Build 5-10 games
- See what sticks
- Double down on winners
- Learn from losers
- First mover on trends (build meme games within 48 hours)

---

## Section 8: VIBE CODING LIMITATIONS & WORKAROUNDS

### What Claude + MCP Can Build Well

- Simple physics + AFK loops
- Avatar customization
- Passive generation systems
- Basic UI
- Real-time multiplayer (100+ players)
- Cross-platform compatibility

### What Requires Manual Work

| Task | Why AI Struggles | Workaround |
|------|------------------|------------|
| Custom 3D models | No 3D generation in Roblox | Use Creator Store assets |
| Animation systems | Complex rigging | Use default Roblox animations |
| Large codebases (20k+ lines) | Context limits | Modular architecture (<300 lines/file) |
| Terrain generation | Perlin noise not optimized | Use terrain editor manually |
| Security/exploit fixes | AI doesn't understand attack vectors | Manual security audit |
| Advanced graphics | Mobile performance limits | Accept platform constraints |

### Best Practices for Vibe Coding

1. **Start simple** - Tycoon or idle game, not RPG
2. **Modular code** - Keep files under 300 lines
3. **Backup before AI rewrites** - Hallucinations happen
4. **Use Creator Store** - Don't build assets from scratch
5. **Test frequently** - Catch issues early
6. **Manual security audit** - AI can't protect you

---

## Section 9: BUILD SEQUENCE (Claude + MCP)

### Day 1: Core Loop
```
Prompt: "Create a basic [GAME_TYPE] game with:
1. Player spawns in starting area
2. Core mechanic: [MECHANIC]
3. Basic UI showing [STAT]
4. One way to earn currency"
```

### Day 2: Progression
```
Prompt: "Add progression system:
1. XP/level system
2. Unlock tiers
3. Rebirth/prestige mechanic
4. Save player data"
```

### Day 3: Monetization
```
Prompt: "Add monetization:
1. VIP gamepass with [PERKS]
2. Currency pack dev products
3. Premium payout tracking
4. Shop UI"
```

### Day 4: Polish
```
Prompt: "Polish the game:
1. Sound effects
2. Particle effects
3. Better UI
4. Tutorial/onboarding"
```

### Day 5: Social + Moments
```
Prompt: "Add social features:
1. Leaderboards
2. Trading system
3. Friend bonuses
4. Chat commands
5. Screenshot-worthy moments for Moments clips"
```

---

## Section 10: REVENUE PROJECTIONS

### Conservative Path

| Month | Games | Monthly Revenue |
|-------|-------|-----------------|
| 1 | 2 games launched | $0-100 |
| 2 | 4 games total | $100-500 |
| 3 | 6 games total | $500-2k |
| 6 | 10 games total | $2k-5k |
| 12 | 15 games, 2 hits | $5k-15k |

### Aggressive Path (With Viral Hit)

| Milestone | Revenue |
|-----------|---------|
| 1 game gets 10k DAU | $1k-3k/mo |
| 1 game gets 100k DAU | $5k-15k/mo |
| 1 game gets 1M DAU | $20k-50k/mo |
| Steal a Brainrot level | $1M+/mo |

### Breakeven Analysis

| Cost | Amount |
|------|--------|
| Roblox Studio | Free |
| Claude Max | $100/mo (already have) |
| Sponsored Ads | $100-500/mo |
| Assets (optional) | $50-200/mo |
| **Total** | **$150-800/mo** |

---

## Section 11: AUTOMATION & COMMUNITY

### Automated Tasks (Ralph-able)

- Content generation prompts
- Basic game building via MCP
- TikTok clip scheduling (via Buffer)
- Discord bot responses
- Analytics collection

### Manual Tasks (Human Required)

- Publishing to Roblox
- Responding to player feedback
- Security audits
- Major game design decisions
- Community management tone
- Influencer negotiations

### Community Building Automation

**Discord:**
- Welcome bot with role assignment
- Auto-post update announcements
- Scheduled giveaways
- XP/level system for active members

**Social:**
- Schedule TikTok posts via Buffer
- Auto-cross-post to YouTube Shorts
- Engagement tracking dashboard

---

## Quick Reference: The Winning Formula

1. **Game Type:** AFK-friendly tycoon or simulator with PvP element
2. **Theme:** Meme-based OR niche-targeted (faith, fitness, education)
3. **Core Loop:** Simple (acquire → grow → optional PvP)
4. **Monetization:** 3-tier passes + cosmetics + optional ads
5. **Updates:** Weekly minimum, bi-weekly cosmetics, monthly major
6. **Marketing:** Own TikTok (3-5 clips/week) + Discord + micro-influencer seed
7. **Build for Moments:** Design clip-worthy gameplay moments

---

## Sources

- [Roblox Official Charts](https://www.roblox.com/charts/top-trending)
- [Steal a Brainrot Wikipedia](https://en.wikipedia.org/wiki/Steal_a_Brainrot)
- [Roblox 2025 Year in Review - DevForum](https://devforum.roblox.com/t/2025-year-in-review/4164479)
- [Roblox Studio MCP Server](https://devforum.roblox.com/t/introducing-the-open-source-studio-mcp-server/3649365)
- [Vibe Coding in Roblox - Medium](https://medium.com/@hromov.s/i-tried-vibecoding-an-rpg-in-roblox-heres-what-i-learned-4481b079d6b2)
- [Roblox Monetization Guide 2025](https://boostroom.com/blog/monetization-for-creators-gamepasses-dev-products)
- [TechCrunch: Roblox Moments & AI Tools](https://techcrunch.com/2025/09/05/roblox-announces-short-form-video-feed-for-gameplay-clips-new-ai-tools-for-creators-and-more/)
- [Pocket Gamer: Steal a Brainrot 25M CCU](https://www.pocketgamer.biz/robloxs-steal-a-brainrot-becomes-first-game-to-surpass-25m-concurrent-players/)
- [RoMonitor Stats](https://romonitorstats.com/)

---

Last Updated: 2026-01-24
