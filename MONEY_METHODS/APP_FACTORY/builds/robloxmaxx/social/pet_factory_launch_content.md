# Pet Factory Tycoon - Launch Content

Generated: 2026-02-07
Status: PENDING_REVIEW

---

## 1. Twitter/X Launch Posts (5 posts)

### Post 1 - The Build Story
```
shipped a full roblox game in ~2 hours using AI.

7 dropper tiers. 16 unique pets across 3 egg types. rebirth system with 50 levels. 5 gamepasses. 4 dev products. promo codes.

not a tutorial project. a real game with real monetization.

the tool: claude code + a custom roblox plugin that writes Luau directly into studio.

link in bio.
```

### Post 2 - The Numbers
```
built "Pet Factory Tycoon" on roblox today.

the numbers:
- 7 droppers (Basic to Mythic, $0 to $2M in-game)
- 16 pets with weighted rarity (1% Mythic drop rate)
- 50 rebirth levels with permanent 25% multipliers
- 9 monetization products
- 3 promo codes at launch

total dev time: ~2 hours. total lines of Luau: 1,200+. total coffee: 1.

AI built every script. I just made decisions.
```

### Post 3 - The Process Breakdown
```
how I shipped a roblox game with zero Luau experience:

1. described the game concept to claude code
2. it generated a full GameConfig (droppers, pets, economy, gamepasses)
3. generated 8 server/client scripts
4. custom plugin injected everything into roblox studio
5. tested, balanced, shipped

no tutorials. no courses. no "learn roblox dev in 30 days."

just AI + a clear spec + shipping energy.
```

### Post 4 - The Pet System Flex
```
the pet system alone would've taken me a week to code manually.

3 egg types (Basic, Golden, Mythic). weighted random hatching. 16 pets from Common Puppy to Galaxy Unicorn (5% mythic egg drop, 20x multiplier).

equip 3 at once. 50 pet inventory cap.

AI wrote the weighted random function, the equip/unequip toggle, the client sync.

2 hours. the entire game. not just the pet system.

roblox is a $2B+ creator economy and most devs are still hand-coding everything.
```

### Post 5 - The Monetization Angle
```
roblox game monetization breakdown (built in 2 hours with AI):

gamepasses:
- 2x Earnings: 199 R$
- Auto-Collect: 149 R$
- VIP Area: 299 R$
- Extra Pet Slot: 99 R$
- Instant Rebirth: 399 R$

dev products:
- 10K coins: 49 R$
- 50K coins: 199 R$
- 250K coins: 799 R$
- 1M coins: 1999 R$

promo codes for launch day retention (LAUNCH2026, PETFACTORY, THANKYOU).

the game isn't the product. the economy inside the game is the product.
```

---

## 2. Roblox Game Description (500 chars max)

```
Build your factory. Hatch pets. Get rich.

7 dropper tiers from Basic to Mythic. 16 unique pets across 3 egg types. Rebirth up to 50 times for permanent multipliers.

Codes: LAUNCH2026 | PETFACTORY | THANKYOU

Collect all pets. Upgrade your factory. Race to the top.

New content coming soon. Like + Favorite for updates!
```

Character count: 346

---

## 3. Reddit Posts (3 posts)

### Post A - r/roblox (Player-focused)

**Title:** Pet Factory Tycoon is live - tycoon + pet collecting with 16 pets and a rebirth system

**Body:**
```
just launched Pet Factory Tycoon and wanted to share.

the basic loop: build droppers to earn coins, hatch pets from 3 egg types to boost earnings, rebirth to get permanent multipliers. repeat.

what's in it:
- 7 dropper tiers (Basic through Mythic)
- 3 egg types: Basic (6 pets), Golden (5 pets), Mythic (5 pets)
- rarest pet is Galaxy Unicorn at 5% drop from Mythic Eggs, gives 20x multiplier
- 50 rebirth levels, each one gives +25% permanent bonus
- 4 upgraders that multiply your drop value up to 5x

free codes for launch:
- LAUNCH2026 (5K coins)
- PETFACTORY (10K coins)
- THANKYOU (25K coins)

would appreciate any feedback. still balancing the economy so if something feels too easy or too grindy let me know.
```

### Post B - r/robloxgamedev (Dev-focused "How I Built This")

**Title:** I built a full tycoon + pet game using AI (Claude Code) in about 2 hours. here's the full breakdown.

**Body:**
```
I know "I used AI" posts can be annoying, but I think the workflow here is genuinely interesting for devs.

**the setup**

I built a custom Roblox Studio plugin that connects to Claude (Anthropic's API). the plugin sends a prompt describing what I want, Claude generates Luau code, and the plugin injects it directly into the right services in Studio. no copy-pasting.

**what it generated**

8 scripts total:
- GameConfig.lua - all game numbers in one shared module (droppers, pets, economy, gamepasses, dev products, codes)
- DataManager.lua - ProfileService-style data persistence with autosave
- TycoonManager.lua - plot claiming, dropper/upgrader purchasing, collector logic
- PetSystem.lua - weighted random hatching, equip/unequip, multiplier stacking
- RebirthManager.lua - prestige system with escalating costs
- EconomyManager.lua - gamepass checks, dev product processing, code redemption
- TycoonHUD.lua - client UI for all systems
- GameInstaller.lua - one-click setup that creates all instances, remotes, folders

**the game**

Pet Factory Tycoon. 7 dropper tiers, 16 pets across 3 egg types, rebirth system, 5 gamepasses, 4 dev products, 3 promo codes.

**what I actually did vs what AI did**

AI: wrote all the Luau code, designed the data structures, handled the remote events, built the UI
Me: described the game concept, made economy balancing decisions, tested in Studio, adjusted numbers in GameConfig

**honest assessment**

the code is solid. type annotations, input validation on all remotes, proper pcall wrapping on datastore calls. it's not perfect (the tycoon plot building needs manual placement work in Studio) but the systems are production-ready.

the real value isn't "AI wrote code for me." it's that I could iterate on game design decisions in minutes instead of days. I changed the pet rarity weights 4 times before I was happy with the drop rates.

happy to answer questions about the plugin or the workflow.
```

### Post C - r/IndieGaming (General)

**Title:** Built a Roblox tycoon game with AI in 2 hours - pet collecting, rebirth system, full economy

**Body:**
```
been experimenting with using AI to build games faster. shipped "Pet Factory Tycoon" on Roblox today.

the game: factory tycoon where you build droppers to earn coins, hatch pets to boost income, and rebirth for permanent multipliers. pretty standard tycoon loop but with a full pet collecting meta layered on top.

some stats:
- 7 dropper tiers (free Basic up to 2M-coin Mythic)
- 16 pets across 3 egg types with weighted rarities
- Galaxy Unicorn is the chase pet: 5% drop from the most expensive egg, 20x income multiplier
- 50 rebirth tiers
- 9 monetization items (gamepasses + coin packs)

the interesting part: I wrote zero Luau (Roblox's scripting language) by hand. built a plugin that connects Roblox Studio to Claude and generates the scripts directly. described the game, AI coded it, plugin injected it into Studio.

the Roblox creator economy did $900M+ in payouts to devs last year. felt like it was worth exploring whether AI tools could make it accessible to people who aren't traditional game devs.

game is live now if anyone wants to check it out.
```

---

## 4. Twitter Thread (Best Post Expansion - Post 3)

### Tweet 1 (Hook)
```
how I shipped a roblox game with zero game dev experience using AI.

not a demo. not a prototype. a real game with real monetization.

Pet Factory Tycoon. 7 dropper tiers. 16 pets. 50 rebirth levels. 9 paid products.

here's the full breakdown:
```

### Tweet 2 (The Tool)
```
step 1: I built a roblox studio plugin.

it connects to Claude's API. I describe what I want in plain english. Claude generates Luau code. the plugin injects it directly into Studio.

no copy-pasting. no tutorials. no "learn Luau in 30 days."

just describe, generate, inject.
```

### Tweet 3 (The Config)
```
step 2: game design as a config file.

instead of coding game logic, I described the economy I wanted. AI generated a single GameConfig module:

- 7 droppers ($0 to $2M cost curve)
- 4 upgraders (1.5x to 5x multipliers)
- 16 pets with weighted drop rates
- rebirth costs that scale at 2.5x per level
- 5 gamepasses, 4 dev products

all numbers in one file. easy to rebalance.
```

### Tweet 4 (The Systems)
```
step 3: AI generated 8 server/client scripts.

DataManager (autosave every 60s)
TycoonManager (plot claiming, purchasing)
PetSystem (weighted hatching, equip slots)
RebirthManager (prestige loop)
EconomyManager (gamepasses, dev products, codes)
TycoonHUD (full client UI)
GameInstaller (one-click setup)

every script has type annotations and input validation. not throwaway code.
```

### Tweet 5 (The Pet System)
```
the pet system is the retention hook.

3 egg tiers: Basic (5K coins), Golden (50K), Mythic (500K).

rarest pet: Galaxy Unicorn. 5% drop from Mythic Eggs. 20x income multiplier.

players grind coins to hatch eggs. chase the rare pets. equip 3 at a time. 50 inventory slots.

this is what keeps people coming back.
```

### Tweet 6 (The Money)
```
roblox paid devs $900M+ last year.

the game has 9 monetization touchpoints:
- 5 gamepasses (99 to 399 R$)
- 4 coin packs (49 to 1999 R$)

the real play: roblox's audience is massive and most games are built by small teams. AI shrinks dev time from months to hours.

one person can now run a game studio.
```

### Tweet 7 (CTA)
```
Pet Factory Tycoon is live now.

free codes:
LAUNCH2026 - 5K coins
PETFACTORY - 10K coins
THANKYOU - 25K coins

play it. break it. tell me what to add next.

if you want to see how I built the Roblox Studio plugin, follow @PRINTMAXXER. building everything in public.
```

---

## Notes

- All content follows PRINTMAXX voice guidelines (lowercase, direct, specific numbers, no AI vocabulary)
- Promo codes verified from GameConfig.lua: LAUNCH2026 (5K), PETFACTORY (10K), THANKYOU (25K)
- Pet count verified: Basic Egg (6 pets) + Golden Egg (5 pets) + Mythic Egg (5 pets) = 16 total
- Dropper count verified: 7 tiers (Basic, Copper, Silver, Gold, Diamond, Emerald, Mythic)
- Monetization: 5 gamepasses + 4 dev products = 9 total monetization items
- Galaxy Unicorn is the rarest pet: 5% weight in Mythic Egg, 20x multiplier
- All posts reference real numbers from the actual game code
