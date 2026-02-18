# Roblox Games Deep Dive

**Method ID:** MM011
**Last Updated:** 2026-01-25
**Status:** Research complete, ready for implementation
**Monthly Potential:** $100 - $100k+ (portfolio approach)
**Phase:** 4 (requires validation first)

---

## Executive Summary

Roblox is a $3.6B platform with 151M+ daily active users. Top games earn $20M+/month. The barrier to entry dropped dramatically with AI-assisted development: Claude Code + Roblox Studio MCP Server enables building games via prompts overnight.

**The opportunity:** Build a portfolio of 5-10 niche-targeted games using vibe coding. Target underserved audiences (faith, fitness, education). Launch fast, iterate based on data, double down on winners.

**Your edge:**
- Official Roblox Studio MCP Server (Claude manipulates Studio directly)
- Claude Max context window for overnight builds
- PRINTMAXX niche positioning (faith, fitness, education)
- Existing content farm infrastructure for marketing

---

## Table of Contents

1. [Platform Economics](#1-platform-economics)
2. [DevEx (Developer Exchange)](#2-devex-developer-exchange)
3. [Game Types That Earn](#3-game-types-that-earn)
4. [Monetization Models](#4-monetization-models)
5. [AI-Assisted Development](#5-ai-assisted-development)
6. [Development Timeline](#6-development-timeline)
7. [Marketing Approaches](#7-marketing-approaches)
8. [Case Studies](#8-case-studies)
9. [Implementation Roadmap](#9-implementation-roadmap)

---

## 1. Platform Economics

### Key Stats (Q4 2025 - Q1 2026)

| Metric | Value | Growth |
|--------|-------|--------|
| Daily Active Users | 151.5M | +70% YoY |
| Monthly Active Users | 381.8M | - |
| Platform Revenue (2024) | $3.6B | - |
| Paid to Creators (9mo 2025) | $1B+ | - |
| Total Games/Experiences | 44M+ | - |

### Audience Demographics

- 70% are ages 9-16
- Global reach (Latin America growing fastest)
- High engagement: average 2.5 hours/day for active players
- 60% of players engage with Robux economy
- Parents increasingly trust educational/faith games

### Revenue Split

| Party | % of Gross |
|-------|-----------|
| Developer | 25-30% |
| Roblox Platform | 30% |
| App Store (mobile) | 30% |
| Payment Processing | 5-10% |

**Net to developer:** After all fees, expect ~25-28% of gross player spend.

---

## 2. DevEx (Developer Exchange)

### What is DevEx?

DevEx converts earned Robux to real USD. Only legitimate revenue qualifies.

### Current Rates (2026)

| Tier | Robux to USD |
|------|--------------|
| Standard | $3.80 per 100,000 Robux |
| Previous Rate (2024) | $3.50 per 100,000 Robux |

**Example:** 1M Robux earned = $38 USD payout

### DevEx Requirements

1. **Account age:** 13+ and verified
2. **Premium membership:** Required (continuous subscription)
3. **Minimum balance:** 30,000 Robux (was 100,000)
4. **Earnings source:** Must be from verified games/experiences
5. **Good standing:** No ToS violations
6. **Tax info:** W-9 or W-8BEN required
7. **Tipalti account:** Payment processor verification

### DevEx Timeline

- Processing: 3-5 business days after request
- Payment: Via Tipalti (bank transfer, PayPal, etc.)
- Frequency: Can request monthly after minimum met

### Robux Conversion Math

| Player Spends | Robux Purchased | Developer Receives | USD After DevEx |
|---------------|-----------------|-------------------|-----------------|
| $1 | ~80 Robux | ~56 Robux (70%) | ~$0.02 |
| $10 | ~800 Robux | ~560 Robux | ~$0.21 |
| $100 | ~10,000 Robux | ~7,000 Robux | ~$2.66 |
| $1,000 | ~100,000 Robux | ~70,000 Robux | ~$26.60 |

**Reality:** You keep ~2.5-2.8 cents per dollar spent by players.

### Why Volume Matters

The low net margin means you need VOLUME:
- 1,000 DAU with $0.01 ARPDAU = $10/day = $300/month
- 10,000 DAU with $0.05 ARPDAU = $500/day = $15,000/month
- 100,000 DAU with $0.10 ARPDAU = $10,000/day = $300,000/month

**Target:** Build games that reach 10k+ DAU and optimize ARPDAU through better monetization.

---

## 3. Game Types That Earn

### Revenue by Genre (2025-2026 Data)

| Genre | Daily Visits | Revenue Potential | Complexity |
|-------|--------------|-------------------|------------|
| Simulation/Tycoon | 110M | Highest | Low-Medium |
| Roleplay/Avatar Sim | 116M | High | Medium |
| Platformers/Obby | 70M | Low-Medium | Low |
| Survival | 70M | Medium | Medium |
| Action/Fighting | 59M | Medium | Medium-High |
| Horror | 30M | Medium | Medium |

### High-Earning Game Archetypes

**1. AFK Tycoons (Highest ROI for Solo Devs)**
- Core Loop: Spawn, collect, upgrade, rebirth
- Why: Low skill requirement, high engagement
- Monetization: VIP passes, currency packs, auto-collectors
- Example: Grow A Garden (21.6M CCU peak)

**2. Pet Collectors/Simulators**
- Core Loop: Hatch eggs, collect pets, trade
- Why: Completionist psychology, trading creates stickiness
- Monetization: Rare eggs, VIP hatching, pet storage
- Example: Pet Simulator X (billions of visits)

**3. PvP + Collection Hybrids**
- Core Loop: Collect, grow, defend/attack others
- Why: Social competition drives engagement
- Monetization: Power-ups, cosmetics, luck boosters
- Example: Steal a Brainrot (25.8M CCU all-time record)

**4. Niche-Targeted Simulators**
- Core Loop: Standard tycoon/sim with niche theme
- Why: Less competition, loyal audience, parent approval
- Monetization: Same as tycoons but with themed content
- Example: Faith/fitness/education adaptations

### What to Avoid

| Type | Why It Fails |
|------|--------------|
| Generic "X Simulator" | Too crowded, invisible |
| Complex RPGs | Too expensive, high technical bar |
| Story Games | Low replay value, poor monetization |
| Pure Obbies | Low monetization ceiling |
| Open-World without LiveOps | Players exhaust content |

---

## 4. Monetization Models

### Revenue Streams Breakdown

| Stream | % of Typical Revenue | Description |
|--------|---------------------|-------------|
| Game Passes | 60% | One-time purchases |
| Dev Products | 25% | Consumables |
| Premium Payouts | 15% | Time from Premium users |

### Game Passes (One-Time)

Best-performing pass types:

| Pass Type | Price Range | Conversion |
|-----------|-------------|------------|
| VIP/2x Coins | 99-199 Robux | 2-5% |
| Auto-Collector | 149-249 Robux | 1-3% |
| Exclusive Area | 199-499 Robux | 0.5-2% |
| Lucky/Luck Boost | 299-999 Robux | 0.5-1% |
| Premium Bundle | 999-2499 Robux | 0.1-0.5% |

**Pricing Strategy:**
- Entry pass: 99 Robux (~$1.25)
- Mid-tier: 199-299 Robux (~$2.50-3.75)
- Premium: 499-999 Robux (~$6-12)
- Whale tier: 2000+ Robux (~$25+)

### Developer Products (Consumables)

| Product Type | Price Range | Use Case |
|--------------|-------------|----------|
| Currency packs | 49-999 Robux | Speed up progression |
| Rebirth tokens | 99-249 Robux | Instant prestige |
| Rare eggs/boxes | 149-499 Robux | Gambling psychology |
| Event tickets | 49-199 Robux | Time-limited access |

### Premium Payouts

How it works:
1. Roblox Premium users spend time in your game
2. You get paid based on engagement time
3. No action required from developer
4. Roughly $0.003-0.005 per Premium minute played

**Optimization:** Give Premium users exclusive benefits to increase their time spent.

### Regional Pricing (NEW 2025)

Roblox now supports regional pricing:
- Same pass = lower price in Brazil/India
- Higher price in US/Europe
- Increases global conversion
- Set via Developer Hub

### Rewarded Video Ads

- "Watch 30s ad for 50 Robux boost"
- 40-50% watch rate typical
- Good for F2P retention
- Additional revenue stream without P2W

### Monetization Anti-Patterns

| DON'T | Why |
|-------|-----|
| Paywall main content | Kills retention, bad reviews |
| Aggressive P2W | Younger audience = parents block |
| Too many SKUs | Decision paralysis |
| Expensive entry pass | Low conversion |

---

## 5. AI-Assisted Development

### The Breakthrough: Roblox Studio MCP Server

**Source:** Official Roblox staff release (DevForum, Jan 2026)

**What it does:**
- Claude directly manipulates Roblox Studio
- Insert models, run Luau code, build games via prompts
- Works with Claude Desktop and Claude Max
- Free, open-source

**How to use:**

1. Install Roblox Studio (free)
2. Download MCP plugin from DevForum
3. Configure Claude Desktop/Code with MCP
4. Restart both applications
5. Prompt Claude to build games

**Example workflow:**
```
"Create a pet simulator with:
1. Click to earn coins
2. Egg hatching system
3. 5 pet rarities
4. Trading between players
5. VIP gamepass with 2x coins"
```

Claude generates the game in Roblox Studio.

### What AI Can Build Well

- Simple physics and AFK loops
- Avatar customization
- Passive generation systems
- Basic UI (buttons, menus, HUDs)
- Real-time multiplayer (100+ players)
- Cross-platform compatibility
- Data stores (saving progress)
- Leaderboards

### What AI Struggles With

| Task | Why AI Struggles | Workaround |
|------|------------------|------------|
| Custom 3D models | No 3D generation | Use Creator Store assets |
| Complex animations | Rigging is hard | Use default Roblox animations |
| 20k+ line codebases | Context limits | Modular architecture (<300 lines/file) |
| Security/exploits | Doesn't understand attack vectors | Manual security audit |
| Advanced graphics | Mobile performance limits | Accept platform constraints |
| Terrain generation | Perlin noise not optimized | Use terrain editor manually |

### Vibe Coding Best Practices

1. **Keep modules under 300 lines** - AI loses context above this
2. **Use Creator Store assets** - Don't build 3D from scratch
3. **Backup before AI rewrites** - Hallucinations happen
4. **Start simple** - Tycoon or idle game, not RPG
5. **Test frequently** - Catch issues early
6. **Manual security audit** - AI can't protect you from exploiters

### Alternative AI Tools

| Tool | Use Case | Source |
|------|----------|--------|
| Roblox Studio MCP | Direct Studio manipulation | ALPHA197 |
| Claude Code | General Luau scripting | Existing |
| Roblox AI Creator Tools | Procedural objects | Native to Studio (2025) |
| GitHub Copilot | Code completion | Alternative |

---

## 6. Development Timeline

### MVP Build (5 Days with AI)

**Day 1: Core Loop**
```
Prompt: "Create a basic [GAME_TYPE] game with:
1. Player spawns in starting area
2. Core mechanic: [MECHANIC]
3. Basic UI showing [STAT]
4. One way to earn currency"
```

**Day 2: Progression**
```
Prompt: "Add progression system:
1. XP/level system
2. Unlock tiers
3. Rebirth/prestige mechanic
4. Save player data"
```

**Day 3: Monetization**
```
Prompt: "Add monetization:
1. VIP gamepass with [PERKS]
2. Currency pack dev products
3. Premium payout tracking
4. Shop UI"
```

**Day 4: Polish**
```
Prompt: "Polish the game:
1. Sound effects
2. Particle effects
3. Better UI
4. Tutorial/onboarding"
```

**Day 5: Social + Moments**
```
Prompt: "Add social features:
1. Leaderboards
2. Trading system
3. Friend bonuses
4. Chat commands
5. Screenshot-worthy moments for clips"
```

### Portfolio Timeline

| Month | Games | Expected Monthly Revenue |
|-------|-------|--------------------------|
| 1 | 2 games launched | $0-100 |
| 2 | 4 games total | $100-500 |
| 3 | 6 games total | $500-2k |
| 6 | 10 games total | $2k-5k |
| 12 | 15 games, 2 hits | $5k-15k |

### Cost Analysis

| Item | Cost |
|------|------|
| Roblox Studio | Free |
| Claude Max | $100/mo (already have) |
| Roblox Premium (DevEx) | $13/mo |
| Sponsored Ads | $100-500/mo |
| Assets (optional) | $50-200/mo |
| **Total Monthly** | **$163-813/mo** |

**Breakeven:** ~$200-800/mo revenue to cover costs.

---

## 7. Marketing Approaches

### Channel Effectiveness (Ranked)

**1. TikTok Organic (Highest ROI if viral)**
- 1 in 5 gaming videos mention Roblox
- Build games designed for clips
- Post 3-5 clips/week from your own account
- Controversial/unique games get more coverage

**2. Roblox Home Page Discovery (90% of new traffic)**
- Algorithm favors:
  - Frequent updates
  - High retention
  - Positive ratings
  - Moments clips
- Update weekly minimum

**3. Roblox Moments (TikTok Clone) - NEW**
- 30-second vertical clips
- Tap-to-join from clips
- Build "clip-worthy" moments into gameplay
- Could become biggest discovery channel by Q2 2026

**4. YouTube (Long-Tail)**
- 105+ Roblox creators with 100K+ subs
- Higher LTV audience (older, spends more)
- Developer channels outperform generic gaming

**5. Influencer/Creator Seeding**
- Micro (10K-100K followers): $50-500 per collab
- Mid-tier (100K-1M): $500-2,000
- Top creators: revenue share deals

**6. Roblox Ads Platform**
- $0.01-$0.10 per click
- Whales outspend small devs
- Use for testing, not scaling

### Content Strategy

**Build for Moments:**
Design gameplay that creates clip-worthy moments:
- Rare pet hatches
- PvP wins
- Funny bugs (intentional)
- Flex moments

**Developer Content:**
Post 3-5 clips/week:
- Behind-the-scenes
- Update previews
- Player reactions
- "I got the rarest X" compilations

### Community Building

**Discord (Required):**
- Post patch notes every 1-2 days
- Exclusive cosmetics for members
- Community voting on features
- Streamer program with revenue share

**Update Cadence (Critical):**

| Frequency | Content |
|-----------|---------|
| Daily/Every-other-day | Status updates, small fixes |
| Weekly | Content update (new items, areas) |
| Bi-weekly | Cosmetic drops |
| Monthly | Major balance patches, new mechanics |

**Warning:** Games with 2+ week gaps see ~20% player drop-off.

---

## 8. Case Studies

### Case Study 1: Steal a Brainrot ($20M+/month)

**Stats:**
- 25.8M concurrent players (all-time Roblox record)
- 22M CCU at peak
- $20M/month AFTER Roblox fees
- For context: Fortnite has 1.13M concurrent (20x smaller)

**Core Loop:**
1. Acquire brainrots from conveyor (price rises as others buy)
2. Brainrots generate passive income
3. Can steal from other players' unlocked bases
4. Attack thieves to recover stolen items
5. Shield button provides temporary defense
6. Rebirth for better stats

**Why It Works:**
- Meme-based (brainrot meme = viral content)
- Latin America dominance
- Developer beef attracted media coverage
- Simple enough for kids, deep enough for grind
- Social clips went viral on TikTok

**Monetization:**
- Lucky Boxes with random drops
- Server Luck gamepass (2200+ Robux)
- Cosmetics and mutations (1.25x to 10x multipliers)

**Lesson:** Meme themes + PvP + viral controversy = record-breaking numbers.

### Case Study 2: Grow A Garden (21.6M CCU)

**Stats:**
- 21.6M concurrent players
- Consistent top 5 game
- True AFK-friendly

**Core Loop:**
- Plant seeds
- Plants grow over time
- Harvest for currency
- Buy better seeds
- Weekly events

**Why It Works:**
- No punishment for offline time
- Pet interactions (cosmetic layer)
- Casual farming appeal
- Weekly events timed to cultural moments

**Lesson:** AFK-friendly + casual theme + consistent events = sustainable hit.

### Case Study 3: Top 1000 Developer Average

**Stats:**
- Average earnings: $820k-980k/year
- About 1,000 developers at this level
- Requires multiple games or one major hit

**Path:**
- Portfolio of 10+ games
- 1-2 games with 50k+ DAU
- Consistent updates
- Community engagement

### Case Study 4: Median Developer

**Stats:**
- $1,440/year
- 44M+ games competing
- Most games earn near-zero

**Reality Check:**
- Majority of games fail
- Discovery is extremely competitive
- Need differentiation to stand out
- Portfolio approach reduces risk

---

## 9. Implementation Roadmap

### Phase 1: Setup (Week 1)

**Day 1-2:**
- [ ] Download and install Roblox Studio
- [ ] Complete basic Roblox Studio tutorials (2-3 hours)
- [ ] Set up Roblox Creator Hub account
- [ ] Configure Claude + MCP Server integration

**Day 3-4:**
- [ ] Research top 10 games in target niche
- [ ] Document successful patterns
- [ ] Choose first game concept (niche-targeted)
- [ ] Outline core loop and monetization

**Day 5-7:**
- [ ] Build MVP using AI-assisted workflow
- [ ] Implement basic monetization (1-2 passes)
- [ ] Test thoroughly
- [ ] Create assets (thumbnail, icon, description)

### Phase 2: Launch (Week 2)

**Day 8-10:**
- [ ] Publish game to Roblox
- [ ] Set up analytics tracking
- [ ] Create Discord server
- [ ] Start Roblox Ads campaign ($20-50 initial)

**Day 11-14:**
- [ ] Monitor metrics daily
- [ ] Create 3-5 TikTok clips
- [ ] Engage in r/robloxgamedev
- [ ] Respond to player feedback
- [ ] Push first update

### Phase 3: Scale (Month 2-3)

**Weekly:**
- [ ] Content update (new items/areas)
- [ ] 5-10 social media posts
- [ ] Community engagement

**Bi-weekly:**
- [ ] Launch new game (portfolio approach)
- [ ] Cosmetic drops for existing games

**Monthly:**
- [ ] Major update for top performer
- [ ] Review analytics, double down on winners
- [ ] A/B test monetization

### PRINTMAXX Niche Adaptations

| Popular Game | PRINTMAXX Version | Target Audience |
|--------------|-------------------|-----------------|
| Steal a Brainrot | Steal a Virtue | Faith kids (collect virtues, defend from sins) |
| Grow A Garden | Grow A Prayer Garden | Faith families (Bible verses as rewards) |
| Pet Simulator | Fitness Pet | Fitness kids (pet evolves with activity) |
| Generic Obby | Study Obby | Parents/Education (quiz gates) |
| Roleplay | Church Community RP | Faith teens (clean social) |
| Tycoon | Startup Tycoon | Ambitious teens (business education) |

### Success Metrics

**Month 1:**
- 2 games launched
- 500+ total visits
- $0-100 revenue

**Month 3:**
- 6 games launched
- 5,000+ total visits
- $500-2k revenue
- 1 game with 1k+ DAU

**Month 6:**
- 10 games launched
- 50,000+ total visits
- $2k-5k revenue
- 2 games with 5k+ DAU

**Month 12:**
- 15 games portfolio
- 500,000+ total visits
- $5k-15k revenue
- 1-2 breakout hits (10k+ DAU)

---

## Quick Reference: The Winning Formula

1. **Game Type:** AFK-friendly tycoon or simulator with optional PvP element
2. **Theme:** Meme-based OR niche-targeted (faith, fitness, education)
3. **Core Loop:** Simple (acquire -> grow -> optional PvP)
4. **Monetization:** 3-tier passes + cosmetics + optional ads
5. **Updates:** Weekly minimum, bi-weekly cosmetics, monthly major
6. **Marketing:** Own TikTok (3-5 clips/week) + Discord + micro-influencer seed
7. **Build for Moments:** Design clip-worthy gameplay moments

---

## Cross-Pollination Opportunities

From LEDGER/CROSS_POLLINATION_MATRIX.csv:

| Method | Synergy | How |
|--------|---------|-----|
| CF004 MEME_CHANNELS | 80 | Meme content promotes Roblox games |
| AI007 GAMING_PERSONAS | 85 | AI gaming persona plays/promotes games |
| MM002 INFO_PRODUCTS | 70 | Sell Roblox dev courses |
| SWARM001 | 95 | Coordinated accounts funnel to game |

**Stack Example:**
1. Build Roblox game (MM011)
2. Create AI gaming persona (AI007) to play/stream
3. Post memes from game (CF004)
4. Coordinate across 10-20 accounts (SWARM001)
5. Sell "How I Built a $10k/mo Roblox Game" course (MM002)

---

## Sources & References

**Official:**
- Roblox Developer Hub: developer.roblox.com
- Roblox DevForum: devforum.roblox.com
- Roblox Charts: roblox.com/charts

**Alpha Sources:**
- ALPHA126: Grow A Garden $20M/month data (@kai_xbt)
- ALPHA197: Roblox Studio MCP Server (Official Roblox DevForum)
- ALPHA205: Swarm cross-pollination strategy

**Analytics:**
- RoMonitor Stats: romonitorstats.com
- Blox Metric: bloxmetric.com

---

## Related Documents

- `ROBLOX_GAME_FACTORY_PLAYBOOK.md` - Detailed playbook
- `README.md` - Quick overview
- `research/` - Competitor analysis
- `game_templates/` - Starter templates
- `marketing/` - Launch playbooks
- `analytics/` - Tracking setup

---

Last Updated: 2026-01-25
