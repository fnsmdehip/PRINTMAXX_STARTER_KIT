# Twitter thread: vibecoding a Roblox game with AI

**Post as:** @PRINTMAXXER
**Format:** 7-tweet thread
**Hashtags (last tweet only):** #roblox #gamedev #vibecoding #buildinpublic

---

## Tweet 1 (Hook)

built a full roblox tycoon game in one session with AI. 8 scripts, 5 gamepasses, 4 dev products, pet system, rebirth system, full monetization. zero game dev experience before this. here's exactly how:

## Tweet 2 (The game)

the game: Pet Factory Tycoon

- 7 tiers of droppers (basic to mythic)
- 4 upgrader levels with multipliers up to 5x
- 3 egg types with 16 pets across 5 rarities
- rebirth system (50 max, 25% permanent bonus each)
- DataStore saves everything

all from prompts. no manual Luau writing.

## Tweet 3 (The tool stack)

tool stack:

- Claude Code (Opus) for generating all Luau scripts
- Roblox Open Cloud API for creating gamepasses + dev products programmatically
- GameInstaller.lua pattern: one script you paste into Studio command bar, sets up the entire game

the installer pattern is the real unlock. copy, paste, play.

## Tweet 4 (Monetization)

monetization was the easiest part. AI generated all of it:

- 2x Earnings: $1.99
- Auto-Collect: $1.49
- VIP Area: $2.99
- Extra Pet Slot: $0.99
- Instant Rebirth: $3.99
- 4 coin packs: $0.49 to $19.99

gamepasses + dev products created via API. not even in Studio.

## Tweet 5 (What surprised me)

what surprised me:

1. AI writes better Luau than most devforum tutorials
2. the economy balancing was solid first try (exponential cost curves, rebirth multipliers)
3. pet rarity weights actually make sense (1% mythic, 40% common)
4. DataStore save/load worked without debugging

what didn't: physical world building. AI can't place parts in 3D space yet. that's still manual.

## Tweet 6 (The numbers)

the math on roblox vibecoding:

- time to generate all 8 scripts: ~45 min
- time to set up in Studio: ~30 min manual
- total: under 2 hours for a playable monetized game
- revenue estimate at 500 DAU: $140-$544/mo
- roblox has 80M+ DAU. even 500 is tiny

now multiply by game count. that's the play.

## Tweet 7 (CTA)

i'm building a kit with all 8 scripts as templates, the GameInstaller pattern, monetization setup guide, and the exact prompts i used.

drop a follow if you want it when it's ready. building more game genres next (obby, simulator, RPG, horror).

the roblox game factory is just getting started.
