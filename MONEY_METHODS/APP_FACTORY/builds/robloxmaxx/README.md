# RobloxMaxx - AI Game Builder for Roblox

## What this is

A ropilot.ai clone/improvement. Roblox Studio plugin + SaaS backend that generates complete Roblox games from natural language using Claude AI.

## Two modes of operation

### 1. SaaS plugin mode (BYOK - for selling to others)

The hosted version at robloxmaxx.com. Users bring their own AI API key (Claude, OpenAI, or Gemini). We never hold or pay for any API key. Zero API cost risk.

- **BYOK (Bring Your Own Key):** User's API key is passed through per-request, never stored
- **Free tier:** Plugin + basic code gen + all genres + community templates (unlimited, BYOK)
- **Pro tier ($9.99/mo):** Meta advisor, revenue estimator, game scanner, premium templates
- No managed credits. No action limits. User controls their own AI costs.
- See `api/COMPLIANCE.md` for full ToS details
- See `api/UNIT_ECONOMICS.md` for cost/margin analysis (~94% margin)

### 2. Local mode (for personal use with Claude Code + MCP)

Use Claude Code with the RobloxMaxx MCP server for your own game development. This is fully allowed under Anthropic ToS since you're using your own Claude Pro/Max subscription for personal, interactive use through a first-party tool.

- See `LOCAL_SETUP.md` for the full guide
- MCP server provides Roblox-specific tools to Claude Code
- No SaaS backend needed, runs entirely on your machine
- No API key needed (uses your Claude Max subscription)

## Architecture

```
robloxmaxx/
├── plugin/
│   └── RobloxMaxxPlugin.lua     # Roblox Studio plugin (~600 lines)
├── api/                          # Next.js app (landing page + API)
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx          # Landing page
│   │   │   ├── layout.tsx        # Root layout
│   │   │   ├── globals.css       # Styles
│   │   │   └── api/
│   │   │       ├── generate/     # AI code generation endpoint
│   │   │       ├── auth/         # Register + login
│   │   │       ├── templates/    # Game template library
│   │   │       ├── usage/        # Usage tracking
│   │   │       └── stripe/       # Billing webhooks
│   │   ├── services/
│   │   │   ├── claude.ts         # Claude API integration (BYOK - user's key)
│   │   │   ├── db.ts             # SQLite database
│   │   │   └── auth.ts           # JWT + API key auth
│   │   ├── prompts/
│   │   │   └── system.ts         # Genre-specific AI prompts
│   │   └── templates/
│   │       └── tycoon.ts         # Pre-built game templates
│   ├── COMPLIANCE.md             # Anthropic ToS compliance documentation
│   ├── UNIT_ECONOMICS.md         # Cost per generation, margin analysis
│   ├── .env.example
│   └── package.json
└── README.md
```

## Improvements over ropilot.ai

| Feature | Ropilot | RobloxMaxx |
|---------|---------|------------|
| Genre-specific prompts | No | Tycoon, obby, simulator, RPG, horror |
| Full game scaffold | No | One prompt → 10-20 scripts, playable game |
| Pre-built templates | No | One-click tycoon/obby/simulator starters |
| Monetization built-in | No | Gamepasses + dev products in every template |
| Self-hosted option | No | SQLite backend, deploy anywhere |
| SaaS billing | Uses user API keys only | BYOK + optional Pro subscription ($9.99/mo) |
| Multi-turn context | No | Conversation memory within session |
| Luau-first | Lua 5.1 patterns | Modern Luau (type annotations, task library) |

## Quick start

### 1. Backend (API + Landing Page)

```bash
cd api
cp .env.example .env.local
# Edit .env.local with your JWT_SECRET (no API key needed on server - BYOK model)
npm install
mkdir -p data
npm run dev
# Runs on http://localhost:3000
```

### 2. Plugin (Roblox Studio)

1. Open Roblox Studio
2. Go to Plugins tab → Manage Plugins
3. Copy `plugin/RobloxMaxxPlugin.lua` content
4. Create new plugin: File → Save as Plugin
5. Paste the code, save
6. Plugin appears in toolbar

### 3. Connect plugin to backend

In the plugin:
- Select "Claude", "OpenAI", or "Gemini" as provider
- Enter your own API key from the provider's console
- Or select "RobloxMaxx Pro" for premium features (requires Pro subscription + your API key)

## Modes

- **Code**: Modify existing game. Plugin reads all scripts, sends to AI, applies changes.
- **Ask**: Ask questions about your codebase. Get explanations, bug fixes, suggestions.
- **Scaffold**: Generate a complete game from scratch. One prompt → full playable game.

## Monetization

### As a SaaS (BYOK model - zero API cost)
- Free: Plugin + basic code gen + all genres (unlimited, BYOK)
- Pro: $9.99/mo for premium intelligence features (meta advisor, revenue estimator, game scanner, premium templates)
- All users bring their own API key. We never hold or pay for AI compute.
- ~94% gross margin after Stripe fees. Zero marginal cost per user.
- See `api/UNIT_ECONOMICS.md` for full cost breakdown

### Internal use (pump out Roblox games)
- Use local mode with Claude Code + MCP server
- Scaffold mode generates complete games in minutes
- Monetize via Roblox gamepasses and developer products
- Each template includes monetization hooks out of the box

## Deploy

```bash
# Vercel (recommended)
cd api && vercel deploy

# Or any Node.js host
cd api && npm run build && npm start
```

## Claude Agent Teams (for development)

Agent teams are now enabled in your Claude settings. To use for developing this further:

```
# In any Claude Code session, you can now say:
"Create an agent team to build out the RobloxMaxx RPG template.
One teammate for combat system, one for quest system, one for inventory."
```

The agents work in parallel, each with their own context, coordinating via shared task list.

## ToS compliance

RobloxMaxx is BYOK-only. We never hold, store, or pay for any AI API key. The user's key is passed through per-request and never persisted. This is fully compliant with all AI provider Terms of Service.

- BYOK via plugin: The plugin calls the AI provider directly with the user's own API key. Our servers are not involved.
- BYOK via proxy (Pro): Our backend injects premium context, then calls the Anthropic API with the user's key. We never store the key.
- Local mode: Uses Claude Code + MCP, which is a first-party Anthropic tool. Fully allowed for personal use.

See `api/COMPLIANCE.md` for the full compliance breakdown.

## Next steps

1. Deploy landing page to Vercel
2. Set up Stripe products (3 tiers)
3. Publish plugin to Roblox Creator Store
4. Add more game templates (RPG, horror, racing, fighting)
5. Add self-testing (generate test scripts that validate game logic)
6. Add project save/load in dashboard
7. Marketing: post on Roblox DevForum, r/robloxgamedev, TikTok
