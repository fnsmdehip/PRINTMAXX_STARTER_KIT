# Roblox devs: what would you actually want from an AI code generator?

**Category:** Development Discussion
**Tags:** #discussion #development-discussion

---

## Context

I built RobloxMaxx, an AI tool that generates complete Roblox games from plain English. Tycoons, obbies, simulators, RPGs. Full script architecture, not just code snippets.

It works. People use it. But I want to make it actually useful for serious devs, not just a novelty.

## What I want to know

**1. What's the most tedious part of your workflow?**

For me it was always:
- Setting up RemoteEvents and the corresponding handler boilerplate
- DataStore save/load with proper error handling
- Gamepass/dev product integration
- UI scaffolding (shop screens, HUD, settings)

Is it the same for you? Or is something else eating your time?

**2. What would make you NOT use an AI tool?**

Honest answers. If the code quality isn't good enough, tell me specifically what's wrong. If you don't trust it, tell me why. If the pricing is wrong, say so.

**3. What game genre or feature is hardest to code?**

I want to add more templates. Currently have: tycoon, obby, simulator, RPG, horror, racing, tower defense, fighting.

What's missing? What genre do you always struggle with?

**4. Do you care about Roblox Studio integration?**

Currently RobloxMaxx has a Studio plugin that lets you generate, modify, and ask questions without leaving Studio. Is that important? Or do you prefer a web dashboard?

**5. Would you use AI to modify existing games?**

The "Code" mode reads your existing scripts and makes targeted changes. Like "add a rebirth system" or "fix the bug where players can buy upgrades they can't afford."

Is that useful? Or do you just want fresh generation?

## Current limitations (being honest)

- No 3D asset generation. Code only.
- Complex physics systems (vehicles, ragdoll) are basic. Need hand-tuning.
- Generated UI is functional but not polished. You'll want to redesign.
- Works best with clear, specific prompts. Vague = vague output.
- Free tier: 300 actions/month. Enough for ~6 complete games.

## What's working well

- Code quality: modern Luau, typed, proper patterns
- Speed: most games generate in under 90 seconds
- Monetization: every template includes gamepass + dev product hooks
- DataStore: uses UpdateAsync, proper error handling, session locking

## Try it and roast it

robloxmaxx.com - free tier, no credit card.

Generate a game. Look at the code. Tell me everything that's wrong with it. I'd rather hear criticism now than after I've built features nobody wants.

Serious feedback only. "it's cool" doesn't help me. "the DataStore implementation doesn't handle edge case X" does.
