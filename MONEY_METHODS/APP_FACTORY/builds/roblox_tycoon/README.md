# AI Factory Tycoon - Roblox Game Starter Kit

## Game Concept

Build and manage your own AI company empire. Start with a basic server rack, collect compute credits, upgrade your infrastructure, and become the biggest AI mogul in the game.

**Core Loop:**
1. Money (compute credits) spawns from your servers
2. Collect money by walking through droppers
3. Buy upgrades (faster servers, bigger racks, automation)
4. Unlock new machines (GPU clusters, quantum computers)
5. Compete on global leaderboard

**Theme:** AI/tech aesthetic with neon colors, server racks, glowing circuits. Appeals to tech-savvy kids who watch YouTube tech content.

---

## Monetization Model

### Revenue Streams

**Gamepasses (permanent purchases):**
- VIP Pass ($4.99 / 400 Robux) - 2x money speed
- Auto-Collect ($2.99 / 250 Robux) - money auto-collects
- Premium Skin ($1.99 / 150 Robux) - neon tycoon theme
- Cash Boost ($0.99 / 80 Robux) - start with $10K

**Developer Products (repeatable purchases):**
- $50K cash injection ($1.99 / 150 Robux)
- $200K cash injection ($4.99 / 400 Robux)
- Skip upgrade timer ($0.99 / 80 Robux)

**Private Servers:**
- Monthly subscription ($1.99 / 150 Robux/month)
- Play with friends only, faster progression

### Revenue Math

Roblox economics:
- Developer gets 70% of Robux after platform cut
- DevEx rate: ~$0.0035 per Robux (285 Robux = $1 USD)
- Example: $4.99 gamepass = 400 Robux = $1.40 to developer

**Projections by Daily Active Users (DAU):**

| DAU | Avg Spend/User | Monthly Revenue | Notes |
|-----|----------------|-----------------|-------|
| 100 | $0.50-1.00 | $50-100 | Proof of concept |
| 1K | $0.50-1.00 | $500-1K | Sustainable income |
| 10K | $0.50-1.00 | $5K-10K | Full-time viable |
| 100K | $0.40-0.80 | $40K-80K | Life-changing |

**Conversion benchmarks:**
- 2-5% of players buy something
- VIP pass = highest volume (25-35% of purchases)
- Whales spend $20-100+ total

---

## Target Audience

**Primary:** 8-16 year old Roblox players (core demo)
- Love tycoon games (proven format)
- Tech/AI theme = trendy right now
- Progression loops = dopamine hits
- Social comparison (leaderboard)

**Secondary:** 17-25 Roblox players
- Nostalgia for classic tycoons
- Appreciate tech aesthetic
- More likely to spend on gamepasses

**Parent-friendliness:**
- Non-violent, educational theme (AI/tech)
- No gambling mechanics (just progression)
- Clear value for purchases (not lootboxes)

---

## Tech Stack

**Language:** Luau (Roblox's Lua variant)
- Fully typed
- Performance optimized for Roblox servers
- Client-server architecture

**Roblox Services Used:**
- DataStoreService (save player progress)
- MarketplaceService (handle purchases)
- TeleportService (server hopping)
- ReplicatedStorage (shared configs)
- StarterGui (UI)

**Development Tools:**
- Roblox Studio (free IDE)
- Moon Animator (for cutscenes/trailers)
- Photoshop/Figma (for thumbnails/icons)

---

## Competitive Analysis

**Top Roblox tycoons (for reference):**
1. **Lumber Tycoon 2** - 2.5B+ visits, $5M+ revenue
2. **Retail Tycoon 2** - 800M+ visits, $2M+ revenue
3. **Restaurant Tycoon 2** - 500M+ visits, $1M+ revenue

**What makes tycoons work:**
- Clear progression (unlock linear path)
- Satisfying feedback loops (money drops, upgrade sounds)
- Social comparison (visit friends' tycoons)
- Monetization feels fair (convenience, not pay-to-win)

**Our edge:**
- AI theme = trendy right now (everyone talks about AI)
- Cleaner code (modern Luau best practices)
- Faster iteration (starter kit = ship in days, not months)

---

## File Structure

```
roblox_tycoon/
├── README.md (this file)
├── SETUP_GUIDE.md (step-by-step instructions)
├── MARKETING_PLAN.md (SEO, ads, growth tactics)
├── src/
│   ├── ServerScriptService/
│   │   ├── TycoonManager.lua (core game logic)
│   │   └── GamepassManager.lua (monetization)
│   ├── StarterGui/
│   │   └── ShopGui.lua (shop UI client-side)
│   └── ReplicatedStorage/
│       └── TycoonConfig.lua (balance/config module)
```

---

## Quick Start

1. Install Roblox Studio (free at roblox.com/create)
2. Follow SETUP_GUIDE.md to import scripts
3. Configure gamepass IDs in Creator Dashboard
4. Test in Studio (F5 to play)
5. Publish to Roblox (File → Publish to Roblox)
6. Follow MARKETING_PLAN.md to get players

**Time to launch:** 4-6 hours for basic version, 1-2 weeks for polished.

---

## Revenue Timeline

**Week 1:** Publish game, run $10-20 Roblox ad test
- Expected: 50-200 visits, 10-50 DAU
- Revenue: $5-20

**Week 2-4:** Iterate based on analytics, post TikTok clips
- Expected: 200-1K visits/day, 100-500 DAU
- Revenue: $50-300/week

**Month 2-3:** If retention good (30%+ D1), scale ads
- Expected: 1K-5K DAU
- Revenue: $500-2K/month

**Month 4+:** Organic growth from Roblox algorithm
- Expected: 5K-50K DAU (if game quality high)
- Revenue: $2K-20K/month

---

## Why Tycoon Games Work

1. **Proven format** - Players know what to expect
2. **Low skill floor** - Anyone can play (collect money, click buttons)
3. **High retention** - Progression keeps players coming back
4. **Monetization-friendly** - Speed-ups and convenience = natural purchases
5. **Social** - Players visit friends' tycoons, compete on leaderboards

Tycoon games are the "idle clicker" genre of Roblox. Simple, addictive, monetizable.

---

## Next Steps

1. Read SETUP_GUIDE.md to build the game
2. Customize theme (AI factory can become anything: restaurant, tech startup, space station)
3. Add unique mechanics (mini-games, quests, rebirth system)
4. Read MARKETING_PLAN.md to get players
5. Track metrics in Roblox Analytics
6. Iterate based on player feedback

**Philosophy:** Ship fast, iterate based on data. This starter kit gets you to launch in days, not months. Focus on retention metrics (D1, D7, D30). If retention good, scale ads. If retention bad, improve game loop before spending on ads.
