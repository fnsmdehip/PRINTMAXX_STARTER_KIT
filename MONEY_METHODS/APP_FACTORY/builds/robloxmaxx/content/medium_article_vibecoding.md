# I vibecoded a complete Roblox game with AI in one session

**Subtitle:** 8 scripts, 5 gamepasses, 16 pets, full monetization. no game dev experience required.
**Publication:** Better Programming / self-publish
**Tags:** roblox, game-development, artificial-intelligence, vibecoding, indie-game
**Reading time:** ~8 min

---

i had zero Roblox development experience 48 hours ago. now i have a fully playable Pet Factory Tycoon with 8 Luau scripts, 5 gamepasses, 4 developer products, a pet hatching system with 16 pets across 5 rarity tiers, a rebirth prestige system, and persistent data saves.

i didn't write a single line of Luau by hand.

here's exactly what i built, how i built it, and what i learned about using AI as a game engine.

## what i built

Pet Factory Tycoon. standard Roblox tycoon loop:

1. player claims a plot
2. droppers generate resource orbs every 0.8 to 2.0 seconds depending on tier
3. orbs travel along conveyors to upgraders (1.5x to 5x multipliers)
4. upgraded orbs hit the collector and convert to coins
5. coins buy more droppers, upgraders, and pet eggs
6. pets give passive earnings multipliers (1.1x for a Common Puppy up to 20x for a Mythic Galaxy Unicorn)
7. rebirth resets everything for a permanent 25% bonus (stacks up to 50 times)
8. repeat

the full game has:

- 7 dropper tiers (Basic through Mythic, cost 0 to 2,000,000 coins)
- 4 upgrader levels (1.5x to 5x multiplier)
- 3 egg types (Basic at 5,000, Golden at 50,000, Mythic at 500,000)
- 16 unique pets with weighted rarity (40% Common down to 1% Mythic in Basic Egg)
- 50 rebirth levels at 25% permanent bonus each
- 3 promo codes built in (LAUNCH2026, PETFACTORY, THANKYOU)
- full DataStore persistence (currency, purchases, pets, rebirths all save)

## the tools

**Claude Code with Opus model.** this was the only AI tool needed for code generation. i described the game mechanics in natural language and got back production-quality Luau.

**Roblox Open Cloud API.** gamepasses and developer products were created programmatically via HTTP requests. never opened the Creator Dashboard for monetization setup.

the key scripts:

| Script | Purpose | Lines (approx) |
|--------|---------|----------------|
| GameConfig.lua | All game numbers in one place | 120 |
| DataManager.lua | DataStoreService save/load | ~200 |
| TycoonManager.lua | Plot claiming, purchases, dropper loops | ~350 |
| PetSystem.lua | Egg hatching, equipping, multipliers | ~250 |
| RebirthManager.lua | Prestige system logic | ~150 |
| EconomyManager.lua | Currency, gamepasses, dev products | ~250 |
| TycoonHUD.lua | Client-side UI | ~300 |
| GameInstaller.lua | One-paste Studio setup | ~400 |

8 scripts. roughly 2,000 lines of Luau total.

## the process

### step 1: game design via prompt

i started with a single prompt describing the game loop, economy structure, and monetization. no PRD. no design doc. just "build a pet factory tycoon with these mechanics."

AI generated GameConfig.lua first. this is the pattern that made everything else work: every number in the game lives in one file. dropper costs, pet rarities, gamepass prices, rebirth multipliers. change one number, the whole game rebalances.

### step 2: systems one at a time

each subsequent script was generated with context from GameConfig. the AI read the config, understood the economy, and built systems that referenced it correctly.

the order mattered:

1. GameConfig (data layer)
2. DataManager (persistence)
3. TycoonManager (core gameplay)
4. PetSystem (collection mechanic)
5. RebirthManager (prestige loop)
6. EconomyManager (monetization hooks)
7. TycoonHUD (client UI)
8. GameInstaller (deployment)

each script took about 5 minutes of prompting and reviewing. some needed one revision. most worked first try.

### step 3: monetization via API

this was the part i expected to be manual. it wasn't.

5 gamepasses created programmatically:

| Gamepass | Price (Robux) | USD equivalent |
|----------|---------------|----------------|
| 2x Earnings | 199 | $1.99 |
| Auto-Collect | 149 | $1.49 |
| VIP Area | 299 | $2.99 |
| Extra Pet Slot | 99 | $0.99 |
| Instant Rebirth | 399 | $3.99 |

4 developer products (repeatable purchases):

| Product | Price (Robux) | USD equivalent |
|---------|---------------|----------------|
| 10K Coins | 49 | $0.49 |
| 50K Coins | 199 | $1.99 |
| 250K Coins | 799 | $7.99 |
| 1M Coins | 1999 | $19.99 |

all created via Roblox Open Cloud API. the IDs were returned and plugged straight into GameConfig.lua. no manual dashboard clicking.

### step 4: the GameInstaller pattern

this is the trick that makes vibecoded Roblox games actually shippable.

GameInstaller.lua is a single script you paste into Roblox Studio's command bar. it creates:

- all server scripts in ServerScriptService
- all client scripts in StarterPlayerScripts
- shared modules in ReplicatedStorage
- the physical game world (plots, parts, UI)
- remote events for client-server communication

one paste. one enter key. game is ready to play.

this pattern means you can iterate on game logic entirely in your code editor, regenerate the installer, and deploy a fresh version in seconds.

## what worked

**economy balancing was surprisingly good.** exponential cost curves (500 to 2,000,000 for droppers, 1,000 to 1,000,000 for upgraders) create the right progression feel without manual tuning. the rebirth cost at 2.5x multiplier per level means early rebirths are cheap and late ones require real grinding. standard tycoon psychology and the AI got it right.

**pet rarity weights were realistic.** 1% chance for a Mythic Phoenix in Basic Egg means roughly 1 in 100 hatches. at 5,000 coins per egg, you need 500,000 coins on average for the best pet. that's a meaningful grind that maps to real Roblox player behavior.

**DataStore implementation worked first try.** save/load with retry logic, session locking, and proper error handling. this usually takes experienced devs multiple iterations. the AI pattern-matched from thousands of DataStore implementations and produced a solid one.

**Luau type annotations.** the generated code uses modern Luau conventions (type annotations, task library, Promises). not legacy Lua 5.1 patterns that most tutorials still teach.

## what didn't work

**physical world building.** AI cannot place 3D parts in Roblox Studio. the GameInstaller creates basic geometry (plots, droppers as colored parts, conveyors) but it looks like a prototype. visual polish still requires a human in Studio or pre-made asset packs.

**MCP bridge was finicky.** we built a robloxstudio-mcp plugin to let Claude Code communicate directly with Roblox Studio. the concept works but Studio's plugin security sandbox makes real-time code injection unreliable. the GameInstaller pattern ended up being more robust.

**testing required manual play.** there's no automated test framework for Roblox games. you have to click Play in Studio and walk around. AI generated the code but couldn't verify it worked. every script needed a manual playtest.

## the revenue math

Roblox has 80M+ daily active users. the platform pays creators through engagement-based payouts and direct purchases (gamepasses/dev products).

at 500 DAU (a tiny game by Roblox standards):

- estimated monthly Robux: 50,625 to 202,500
- estimated monthly USD: $140 to $544
- this includes gamepass sales (59%), dev product purchases (29%), and engagement-based creator rewards (12%)

that's one game. the play is volume.

if you can vibecode a game template in 2 hours and publish 5 genre variants in a week, you're running a portfolio. some will get zero traction. some will catch an algorithm wave. the ones that stick get iterated on. the ones that don't cost you nothing but time.

Roblox also has the youngest demographics of any platform. kids discover games through the Roblox search and algorithm, not external marketing. your discovery cost is zero if the game shows up in search results.

## what this means for indie game dev

Roblox vibecoding isn't going to produce AAA quality games. but it doesn't need to.

the top Roblox games are almost comically simple in concept. Adopt Me is a pet trading game. Brookhaven is a roleplaying game with basic houses. Pet Simulator X is clicking a button and watching numbers go up.

the bar for "good enough to get players" on Roblox is lower than any other platform. and the discovery mechanism is built in.

the people who will win here are the ones who:

1. treat it like a portfolio (many games, not one game)
2. use AI for the 90% that's mechanical (scripts, economy balancing, data persistence)
3. spend their human time on the 10% that matters (visual polish, playtesting, game feel)
4. iterate based on player data, not assumptions

i'm building out templates for obby, simulator, RPG, and horror genres next. same pattern: GameConfig drives everything, AI generates the systems, GameInstaller deploys it.

## the kit

i'm packaging everything from this build into a starter kit:

- all 8 Luau scripts as customizable templates
- GameConfig guide (how to reskin for any theme)
- monetization setup walkthrough
- the exact prompts i used
- genre-specific prompt templates (tycoon, obby, simulator, RPG, horror)

if you want to vibecode Roblox games, the templates save you the first 80% of the work. customize GameConfig, regenerate with AI, paste the installer, playtest, publish.

the game factory pattern. build once, reskin infinitely.

---

*i write about vibecoding, AI-assisted game dev, and building internet businesses from zero. follow @PRINTMAXXER on X for more.*
