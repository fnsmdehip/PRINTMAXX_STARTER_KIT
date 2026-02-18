# Tutorial: Build a complete tycoon game with AI in 5 minutes

**Category:** Community Resources > Tutorials
**Tags:** #resources #tutorials #community-resources

---

## What we're building

A fully playable pizza tycoon with:
- 8 cooking stations (unlock progressively)
- Currency system with auto-collection
- Upgrade system (speed, capacity, value)
- Gamepasses (2x earnings, auto-collect, VIP room)
- Dev products (100 coins, skip timer)
- DataStore persistence (saves between sessions)
- Leaderboard

Total time: about 5 minutes from prompt to playtest.

## Step 1: Open RobloxMaxx (30 seconds)

Option A: Use the Roblox Studio plugin
- Plugins tab > RobloxMaxx
- Click the toolbar button
- Select "Scaffold" mode

Option B: Use the web dashboard
- Go to robloxmaxx.com
- Log in (or create free account)
- Click "New Game"

## Step 2: Write your prompt (30 seconds)

Type this (or your own version):

```
Build a pizza tycoon game. 8 cooking stations that unlock progressively as the player earns money.
Each station has: dough prep, sauce, toppings, oven, packaging.
Currency: PizzaBucks. Players collect from completed pizzas.
Upgrades: cooking speed (5 levels), oven capacity (3 levels), pizza value (5 levels).
Gamepasses: 2x PizzaBucks ($99 Robux), Auto-Collect ($149 Robux), VIP Kitchen ($249 Robux).
Dev products: 500 PizzaBucks ($49 Robux), Skip Timer ($29 Robux).
DataStore: save player progress, currency, unlocked stations, purchased upgrades.
Leaderboard: top earners by total PizzaBucks earned.
```

Hit generate.

## Step 3: Wait for generation (45-90 seconds)

RobloxMaxx generates the full game architecture. For this tycoon, expect 15-20 scripts:

**ServerScriptService:**
- TycoonManager.server.lua (core game loop)
- DataManager.server.lua (save/load with UpdateAsync)
- MonetizationManager.server.lua (gamepass + dev product handlers)
- LeaderboardManager.server.lua

**ReplicatedStorage:**
- TycoonConfig.lua (all station/upgrade/price data)
- Types.lua (type definitions)

**StarterGui:**
- ShopUI.client.lua
- HUDController.client.lua
- UpgradeUI.client.lua

**StarterPlayerScripts:**
- ClientController.client.lua (input handling, UI updates)

## Step 4: Copy into Roblox Studio (2 minutes)

1. Open Roblox Studio with a Baseplate template
2. For each generated script:
   - Create the script in the correct service (ServerScriptService, ReplicatedStorage, etc.)
   - Paste the code
   - Rename to match

The plugin does this automatically if you're using the Studio plugin. One click.

## Step 5: Playtest (1 minute)

Hit Play in Studio. You should see:
- Your character spawns
- HUD shows PizzaBucks: 0
- First station is unlocked
- Walk to station, pizza starts cooking
- Collect completed pizza for PizzaBucks
- Open shop to buy upgrades
- Gamepass prompts work

## What to customize

The generated code is clean Luau with comments. Common tweaks:

**Change prices:**
Open TycoonConfig.lua. All prices are in one table. Change numbers, not code.

**Add more stations:**
Add entries to the stations table in TycoonConfig. The TycoonManager reads from config, so new stations just work.

**Change the theme:**
The code doesn't care if it's pizza or mining or farming. Rename the assets and strings. Logic stays the same.

**Add a rebirth system:**
Use the "Code" mode. Select your game, type "add a rebirth system that resets progress but gives a permanent 1.5x multiplier per rebirth." AI adds it to your existing code.

## Tips for better prompts

1. **Be specific about numbers.** "8 stations" is better than "multiple stations."
2. **Name your currency.** "PizzaBucks" gives the AI context for naming everything else.
3. **Specify Robux prices.** The AI sets up the gamepass/dev product handler with your prices.
4. **Mention DataStore explicitly.** If you want saves, say so. The AI won't assume.
5. **One game per prompt.** Don't try to combine genres. Generate separately, then merge.

## The code is yours

Everything RobloxMaxx generates is your code. No attribution required. No watermarks. No licensing restrictions. Publish, sell, modify, whatever you want.

## Questions?

Reply here or DM me. Happy to help troubleshoot any issues with the generated code.

If you build something cool with this, post it in Cool Creations and tag me. I'd love to see what people make with 5 minutes and a good prompt.
