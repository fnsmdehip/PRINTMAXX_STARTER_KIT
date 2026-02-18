# AI Factory Tycoon - Complete Setup Guide

From zero to published Roblox game in 4-6 hours.

---

## Prerequisites

**1. Roblox Account**
- Create account at roblox.com (free)
- Email verification required
- Age 13+ (for DevEx, need 18+ or parental consent)

**2. Roblox Studio**
- Download from roblox.com/create
- Windows or Mac (free)
- Launches from browser or standalone

**3. Basic Roblox Studio Knowledge**
- 30-minute tutorial: youtube.com/watch?v=APbhF5VbJ-k (official Roblox tutorial)
- Learn: Explorer window, Properties, Play testing (F5)

---

## Phase 1: Import Scripts (15 minutes)

### Step 1: Create New Place

1. Open Roblox Studio
2. File → New → Baseplate
3. Save as "AI Factory Tycoon"

### Step 2: Create Folder Structure

In Explorer window, create these folders:

**ServerScriptService:**
- (already exists)

**StarterGui:**
- (already exists)

**ReplicatedStorage:**
- Right-click Workspace → Insert Object → Folder
- Rename to "ReplicatedStorage" (if doesn't exist)
- Create subfolder: "UpgradeModels"

**Workspace:**
- Create folder: "Tycoons"

### Step 3: Import Scripts

**In ServerScriptService:**
1. Right-click ServerScriptService → Insert Object → Script
2. Rename to "TycoonManager"
3. Delete default code, paste contents of `src/ServerScriptService/TycoonManager.lua`
4. Repeat for "GamepassManager"

**In StarterGui:**
1. Right-click StarterGui → Insert Object → LocalScript
2. Rename to "ShopGui"
3. Paste contents of `src/StarterGui/ShopGui.lua`

**In ReplicatedStorage:**
1. Right-click ReplicatedStorage → Insert Object → ModuleScript
2. Rename to "TycoonConfig"
3. Paste contents of `src/ReplicatedStorage/TycoonConfig.lua`

### Step 4: Verify Structure

Explorer should look like:
```
Workspace
├── Tycoons (Folder - empty for now)
ServerScriptService
├── TycoonManager (Script)
├── GamepassManager (Script)
StarterGui
├── ShopGui (LocalScript)
ReplicatedStorage
├── TycoonConfig (ModuleScript)
├── UpgradeModels (Folder)
```

---

## Phase 2: Build Tycoon Structure (30 minutes)

### Step 1: Create Tycoon Template

**In Workspace → Tycoons folder:**

1. Insert → Model, rename to "Tycoon1"

**Inside Tycoon1, create these parts:**

**Base (floor):**
- Insert → Part
- Rename to "Base"
- Size: 50, 1, 50 (studs)
- Position: 0, 0, 0
- Anchored: true
- BrickColor: Dark grey

**SpawnPoint (where player spawns):**
- Insert → SpawnLocation
- Rename to "SpawnPoint"
- Position: 0, 3, -20 (front of base)
- Anchored: true

**Collector (where money spawns):**
- Insert → Part
- Rename to "Collector"
- Size: 5, 5, 5
- Position: 0, 3, 20 (back of base)
- Anchored: true
- BrickColor: Bright yellow
- Material: Neon

**Owner ObjectValue:**
- Select Tycoon1 model
- Insert Object → ObjectValue
- Rename to "Owner"
- Value: leave empty (nil)

**Buttons Folder:**
- Select Tycoon1
- Insert Object → Folder
- Rename to "Buttons"

### Step 2: Create Upgrade Buttons

**Inside Buttons folder, create 10 buttons:**

For each button (Button1 through Button10):

1. Insert → Part
2. Rename to "Button1" (Button2, Button3, etc)
3. Size: 4, 1, 4
4. Position: Arrange in a line or grid in front of base
   - Suggested: X positions -20, -15, -10, -5, 0, 5, 10, 15, 20, 25
   - Y: 3 (above ground)
   - Z: -15 (in front of base)
5. Anchored: true
6. BrickColor: Bright green
7. Material: Neon

**Visual tip:** Space buttons 5 studs apart in a line for clean layout.

### Step 3: Duplicate Tycoon for Multiple Players

1. Select Tycoon1 model
2. Ctrl+D to duplicate
3. Rename to "Tycoon2"
4. Move to different position (e.g., X: 100, Z: 0)
5. Repeat for 4-8 tycoons total (supports 4-8 simultaneous players)

**Positioning tip:** Space tycoons 100-150 studs apart so they don't overlap.

---

## Phase 3: Create Upgrade Models (30 minutes)

In ReplicatedStorage → UpgradeModels folder, create placeholder models for each upgrade.

**For each upgrade (BasicServer, GPURack, etc):**

1. Insert → Part
2. Customize appearance:
   - BasicServer: Grey brick, size 5x5x3
   - GPURack: Black neon, size 5x8x3
   - DataCenter: Dark grey, size 10x10x5
   - QuantumComputer: Blue neon sphere, size 6x6x6
   - AICore: Cyan neon, size 4x10x4
   - SuperCluster: Red neon, size 12x8x6
   - NeuralNetwork: Purple neon web (union multiple parts)
   - AGILab: Rainbow parts (multiple colors)
   - SingularityHub: Black hole effect (sphere with transparency)
   - MatrioshkaBrain: Massive glowing sphere, size 20x20x20
3. Group parts if multiple → Right-click → Group
4. Rename to match config (e.g., "BasicServer")
5. Set PrimaryPart (select main part, right-click model → Set PrimaryPart)

**Quick version:** Use simple colored bricks. Polish later with better models/meshes.

---

## Phase 4: Test Locally (10 minutes)

### Step 1: Test in Studio

1. Press F5 to play test
2. Check Output window for errors (View → Output)
3. Expected behavior:
   - Player spawns at Tycoon1 SpawnPoint
   - Money (yellow parts) spawns from Collector every 2 seconds
   - Walk through money to collect (leaderboard Cash increases)
   - Touch Button1 when you have $100 (should purchase and spawn BasicServer)
   - Continue buying upgrades sequentially

### Step 2: Debug Common Issues

**"attempt to index nil" errors:**
- Check folder structure matches exactly
- Verify ObjectValue named "Owner" exists in each tycoon
- Check TycoonConfig is in ReplicatedStorage

**Money doesn't spawn:**
- Check Collector part exists in each tycoon
- Check TycoonManager script is in ServerScriptService

**Can't purchase upgrades:**
- Check Buttons folder exists
- Check upgrade models exist in ReplicatedStorage.UpgradeModels
- Check button names match config (Button1, Button2, etc)

**Multiple players test:**
- File → Publish to Roblox (save to cloud)
- Home tab → Test → Start Server (opens multiple windows)
- Test with 2-4 player windows

---

## Phase 5: Publish to Roblox (10 minutes)

### Step 1: Initial Publish

1. File → Publish to Roblox As...
2. Name: "AI Factory Tycoon"
3. Description: "Build your AI empire. Start with a server rack, upgrade to quantum computers."
4. Genre: Building
5. Max players: 10
6. Public access: On (or Friends for testing)
7. Click "Create"

### Step 2: Game Settings

In Roblox Studio, Home tab → Game Settings:

**Basic Info:**
- Title: AI Factory Tycoon
- Description: Build and manage your AI company. Collect compute credits, upgrade your infrastructure, compete on the leaderboard.
- Genre: Building

**Monetization:**
- Enable: Paid Access: Off (free to play)
- Enable: In-Experience Purchases: On

**Avatar:**
- Avatar Type: R15 (recommended)
- Animation: Standard

**Security:**
- Enable Studio Access to API Services: On (for DataStore)

Save and publish.

---

## Phase 6: Create Gamepasses & Products (20 minutes)

### Step 1: Access Creator Dashboard

1. Go to roblox.com/develop
2. Click your game: "AI Factory Tycoon"
3. Left sidebar: Monetization → Passes

### Step 2: Create Gamepasses

**Create 4 gamepasses:**

**Gamepass 1: VIP Pass**
- Name: VIP Pass
- Description: Get 2x money speed forever! Accelerate your progress and dominate the leaderboard.
- Price: 400 Robux
- Icon: Upload 512x512 image (green VIP badge, create in Canva/Photoshop)
- Click "Create Pass"
- Copy the Gamepass ID (shown in URL or page)
- Paste ID into TycoonConfig.lua → GAMEPASSES.VIP = [ID]

**Gamepass 2: Auto-Collect**
- Name: Auto-Collect
- Description: Money automatically collects - no need to walk through droppers!
- Price: 250 Robux
- Icon: 512x512 magnet or automation icon
- Copy ID → TycoonConfig.lua → GAMEPASSES.AutoCollect = [ID]

**Gamepass 3: Premium Skin**
- Name: Premium Skin
- Description: Unlock the neon blue tycoon theme. Stand out from the competition.
- Price: 150 Robux
- Icon: 512x512 neon tycoon screenshot
- Copy ID → TycoonConfig.lua → GAMEPASSES.PremiumSkin = [ID]

**Gamepass 4: Cash Boost**
- Name: Cash Boost
- Description: Start with $10,000 bonus cash. Skip the early grind.
- Price: 80 Robux
- Icon: 512x512 cash stack image
- Copy ID → TycoonConfig.lua → GAMEPASSES.CashBoost = [ID]

### Step 3: Create Developer Products

Go to Monetization → Developer Products

**Product 1: $50K Cash Pack**
- Name: $50K Cash Pack
- Description: Instant $50,000 cash injection
- Price: 150 Robux
- Icon: 512x512 cash image
- Copy Product ID → TycoonConfig.lua → DEVELOPER_PRODUCTS.Cash50K.id = [ID]

**Product 2: $200K Cash Pack**
- Name: $200K Cash Pack
- Description: Instant $200,000 cash injection
- Price: 400 Robux
- Icon: 512x512 large cash stack
- Copy ID → TycoonConfig.lua → DEVELOPER_PRODUCTS.Cash200K.id = [ID]

**Product 3: Skip Timer**
- Name: Skip Timer
- Description: Instant upgrade completion (placeholder for future feature)
- Price: 80 Robux
- Icon: 512x512 fast-forward icon
- Copy ID → TycoonConfig.lua → DEVELOPER_PRODUCTS.SkipTimer.id = [ID]

### Step 4: Update TycoonConfig

1. In Roblox Studio, open ReplicatedStorage → TycoonConfig
2. Replace all `0` values in GAMEPASSES and DEVELOPER_PRODUCTS with real IDs
3. File → Publish to Roblox (save changes)

---

## Phase 7: Test Monetization (15 minutes)

### Step 1: Test Gamepass Purchases

1. Play game in Roblox (not Studio) at roblox.com/games/[your-game-id]
2. Click SHOP button (top right)
3. Try purchasing a gamepass (you'll need Robux or use alt account)
4. Verify benefits work:
   - VIP: money spawns 2x faster
   - Auto-Collect: money collects without touching
   - Premium Skin: tycoon turns neon blue
   - Cash Boost: leaderboard shows +$10K on join

### Step 2: Test Developer Products

1. Purchase $50K Cash Pack
2. Verify cash increases by $50,000 immediately
3. Purchase again (should work - products are repeatable)

### Step 3: Check Analytics

Creator Dashboard → Analytics → Economy

- View Robux earned
- Track conversion rates (purchases / visits)
- Identify top-selling items

---

## Phase 8: Set Up DevEx (Optional - For Payouts)

**Requirements:**
- Age 13+ (18+ for direct payout, or parental consent)
- 30,000+ earned Robux (not purchased)
- Verified email
- Good account standing (no bans)

**Steps:**
1. Go to roblox.com/developexchange
2. Click "Cash Out"
3. Provide tax info (W-9 for US, W-8BEN for international)
4. Link Tipalti account (payment processor)
5. Request payout (minimum $100 USD / 30K Robux)

**DevEx Rate:** ~$0.0035 per Robux (285 Robux = $1 USD)

**Timeline:** Payouts take 5-14 days after request.

---

## Phase 9: Polish & Iterate (2-4 hours)

### Improvements to Add

**Visual Polish:**
- Better upgrade models (use free models from Roblox library or Blender)
- Particle effects (sparks, glows on machines)
- Sound effects (purchase sound, money collect sound)
- Background music (looping ambient track)
- Lighting improvements (ColorCorrection, Bloom effects)

**Gameplay Features:**
- Rebirth system (prestige for permanent multipliers)
- Daily rewards (come back each day for bonus)
- Quests/achievements (purchase X upgrades, collect X money)
- Codes (redeem for free cash - share on social media)
- VIP area (only accessible with VIP gamepass)

**Monetization Tweaks:**
- Limited-time sale gamepasses (50% off for 24 hours)
- Bundles (buy VIP + Auto-Collect for discount)
- Private servers ($150 Robux/month for playing with friends)

### Balancing

**Track these metrics in Analytics:**
- Average session time (target: 15+ minutes)
- D1 retention (% who come back next day - target: 30%+)
- Conversion rate (% who purchase - target: 2-5%)
- ARPPU (average revenue per paying user - target: $2+)

**If retention low (<20% D1):**
- Make progression faster (lower upgrade prices)
- Add more upgrades (more content = more playtime)
- Add social features (visit friends' tycoons)

**If conversion low (<1%):**
- Improve gamepass value perception (better icons, descriptions)
- Add limited-time sales (urgency)
- Show what VIP players are doing (social proof)

---

## Phase 10: Launch (Covered in MARKETING_PLAN.md)

See MARKETING_PLAN.md for:
- Roblox SEO optimization
- Thumbnail/icon design
- Advertising campaigns ($10-50 budget)
- Social media promotion (TikTok, YouTube)
- Community building

---

## Troubleshooting Common Issues

### Scripts not running
- Check Output window for errors
- Verify scripts are in correct folders (Server vs Client)
- Enable API services (Game Settings → Security → Studio Access to API Services)

### DataStore errors
- Game must be published to Roblox (can't test DataStore in unpublished place)
- Enable API services
- Check you're not hitting rate limits (60 requests/minute)

### Gamepasses not working
- Verify IDs are correct in TycoonConfig.lua
- Check MarketplaceService has permissions
- Test in published game, not Studio

### Money not spawning
- Check Collector part exists in each tycoon
- Check TycoonManager is running (print statements in Output)
- Verify tycoon ownership is set (Owner ObjectValue.Value = player)

### Players can't join
- Check max players setting (Home → Game Settings → Basic Info)
- Verify tycoons exist in Workspace.Tycoons folder
- Check spawn points are not obstructed

---

## Next Steps

1. Polish game (better models, sounds, effects)
2. Add more content (20+ upgrades, rebirth system, quests)
3. Follow MARKETING_PLAN.md to get players
4. Monitor Analytics daily
5. Iterate based on player feedback and data
6. Scale ads once retention is good (30%+ D1)

**Goal:** Get to 1K DAU = $500-1K/month revenue. Then scale to 10K+ DAU.

---

## Resources

**Roblox Dev Hub:**
- developer.roblox.com/en-us/learn-roblox (official tutorials)

**Scripting Reference:**
- developer.roblox.com/en-us/api-reference (API docs)

**Free Models & Assets:**
- roblox.com/develop/library (search "tycoon", "server rack", etc)
- Free sound effects: roblox.com/develop/library (audio)

**Community:**
- devforum.roblox.com (official dev forum)
- r/robloxgamedev (Reddit)
- Roblox OSS Discord

**YouTube Tutorials:**
- AlvinBlox (beginner scripting)
- TheDevKing (tycoon tutorials)
- Gnomenclature (UI design)

---

## Time Estimate Summary

| Phase | Time | Task |
|-------|------|------|
| 1 | 15 min | Import scripts |
| 2 | 30 min | Build tycoon structure |
| 3 | 30 min | Create upgrade models |
| 4 | 10 min | Test locally |
| 5 | 10 min | Publish to Roblox |
| 6 | 20 min | Create gamepasses & products |
| 7 | 15 min | Test monetization |
| 8 | 10 min | Set up DevEx (optional) |
| 9 | 2-4 hrs | Polish & iterate |
| **TOTAL** | **4-6 hrs** | **Basic version launched** |

Add 2-4 hours for polish (better models, sounds, effects, more upgrades).

Ship the basic version first. Iterate based on player data. Perfect is the enemy of shipped.
