# RobloxMaxx - Anthropic ToS compliance

## The rule

Anthropic prohibits using Claude Pro/Max subscription tokens through third-party tools or automated pipelines. The API (pay-per-token) is the correct way to build products on top of Claude.

## How RobloxMaxx is compliant

### SaaS mode (BYOK - what we sell to customers)

RobloxMaxx is a BYOK (Bring Your Own Key) product. We never hold, store, or pay for any AI API key. The user provides their own API key in every request, and we pass it through to the AI provider.

**Flow:**

```
Plugin (Roblox Studio)
  -> POST robloxmaxx.com/api/generate (our Next.js backend)
    -> Authenticate user (JWT token, optional)
    -> Receive user's API key from request body
    -> POST api.anthropic.com/v1/messages (user's own API key)
    -> Track usage for analytics (no limits enforced)
    -> Return generated code to plugin
```

**What this means:**
- We never have our own ANTHROPIC_API_KEY on the server
- The user's API key is used per-request, never stored
- The user pays their own API bill directly to Anthropic/OpenAI/Google
- Zero ToS risk since we're just a tool that formats prompts and applies code changes
- This is the same model as Cursor, Windsurf, etc. when in BYOK mode

### Direct BYOK mode (plugin calls provider directly)

Users who select "Claude", "OpenAI", or "Gemini" in the plugin provider dropdown enter their own API key. The plugin calls the provider API directly from within Roblox Studio's HttpService. Our servers are not involved at all.

**Flow:**

```
Plugin (Roblox Studio)
  -> POST api.anthropic.com/v1/messages (user's own API key)
  -> Return generated code to plugin
```

No usage tracking on our end. No proxy. The user pays their own API bill.

### RobloxMaxx Pro mode (through our API proxy)

Pro subscribers ($9.99/mo) get access to premium features (meta advisor, revenue estimator, game scanner, premium templates). These requests go through our backend which adds premium context to prompts, but still uses the user's own API key.

**Flow:**

```
Plugin (Roblox Studio)
  -> POST robloxmaxx.com/api/generate (our backend)
    -> Authenticate Pro subscription
    -> Inject premium context (meta data, genre intelligence)
    -> POST api.anthropic.com/v1/messages (user's own API key)
    -> Return enhanced response
```

The Pro subscription pays for our intelligence layer, not AI compute.

### Local mode (personal use with Claude Code + MCP)

For personal game development, use Claude Code (first-party Anthropic tool) with a custom MCP server that provides Roblox-specific tools. This is:

- A first-party tool made by Anthropic
- Used interactively by a human (not automated)
- Used with a personal Claude Pro/Max subscription
- Fully allowed per Anthropic ToS

This mode is NOT part of the SaaS product. It's a separate local development workflow.

## What we do NOT do

- We do NOT hold or store any Anthropic API key on our servers
- We do NOT route subscription tokens through our backend
- We do NOT use `claude` CLI or Claude Code as a backend for the SaaS
- We do NOT use MCP servers to proxy subscription access to third parties
- We do NOT automate Claude Pro/Max sessions for batch generation
- We do NOT charge for AI compute (user pays their own provider directly)

## Summary

| Mode | How AI is called | Who pays for AI | ToS status |
|------|-----------------|-----------------|------------|
| SaaS (BYOK via proxy) | Our backend -> Anthropic API (user's key) | User pays their own API bill | Compliant |
| SaaS (BYOK direct) | Plugin -> Provider API directly | User pays their own API bill | Compliant |
| SaaS (Pro features) | Our backend + premium context -> Anthropic API (user's key) | User pays their own API bill | Compliant |
| Local (Claude Code + MCP) | Claude Code (first-party tool) | Personal subscription | Compliant |
