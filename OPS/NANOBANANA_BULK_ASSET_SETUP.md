# NanoBanana + Claude Code: Bulk Asset Generation Setup

**Created:** 2026-02-27
**Status:** READY TO SET UP (needs Gemini API key with billing)

---

## What Is NanoBanana?

NanoBanana is Google's code name for Gemini's native image generation. NanoBanana 2 launched Feb 26, 2026 — literally yesterday. It's the current state-of-the-art for speed + quality + cost.

| Version | Model | Cost | Speed | Quality |
|---------|-------|------|-------|---------|
| NanoBanana 2 | Gemini 3.1 Flash Image | ~$0.034/image (batch) | Fast | High |
| NanoBanana Pro | Gemini 3 Pro Image | ~$0.134/image | Medium | Highest |

Key features: accurate text rendering, style consistency across batches, 512px to 4K resolution.

---

## Setup: MCP Server for Claude Code

### Step 1: Get Gemini API Key
1. Go to https://aistudio.google.com
2. Create an API key
3. Enable billing on your Google Cloud project (image gen requires paid tier)

### Step 2: Install MCP Server

Option A — ConechoAI MCP (recommended):
```bash
claude mcp add nano-banana --scope user -- npx nano-banana-mcp
```

Then add the API key to `~/.claude/mcp_settings.json`:
```json
{
  "mcpServers": {
    "nano-banana": {
      "command": "npx",
      "args": ["nano-banana-mcp"],
      "env": {
        "GEMINI_API_KEY": "AIza_your_key_here"
      }
    }
  }
}
```

Option B — TamerinTECH (auto-integrates with UI coding):
```bash
git clone https://github.com/TamerinTECH/claude-code-generate-images-mcp
cd claude-code-generate-images-mcp
./install.sh
```

### Step 3: Verify
Type `/mcp` in Claude Code — confirm `nano-banana` appears in the server list.

---

## Use Cases for PRINTMAXX

### 1. App Icons and Screenshots (for 6+ PWA apps)
```
"Generate an app icon for PrayerLock: 1024x1024, dark gradient background,
golden lock icon with subtle cross motif, modern minimal style"
```

### 2. Social Media Graphics (for 13 niche accounts)
- Twitter headers (1500x500)
- Profile pictures (400x400)
- Post images (1200x675)
- Thread preview cards

### 3. Product Mockups (for Gumroad/Etsy listings)
- Digital product cover images
- Course thumbnails
- Template preview images

### 4. Landing Page Hero Images
- For the 16 surge.sh sites
- For printmaxx.io when deployed

### 5. YouTube Thumbnails (for youtube_factory.py pipeline)
- Bold text + visual + emotion
- Consistent brand per channel

---

## Bulk Asset Slash Command

Create `.claude/commands/generate-assets.md`:
```markdown
Generate a complete set of assets for the specified app or account.

Use the nano-banana MCP tool for each asset. Save to the appropriate directory.

For apps: save to builds/{app-name}/assets/
For social: save to CONTENT/social/{account}/assets/
For products: save to PRODUCTS/assets/

Asset sets available:
1. "app" — icon (1024, 512, 192, 144), splash screens, feature graphic, screenshots
2. "social" — profile pic, header, 5 post templates
3. "product" — cover image, preview mockup, OG card
4. "youtube" — thumbnail template, channel art, end screen

Usage: /generate-assets app prayerlock
       /generate-assets social printmaxxer
       /generate-assets product "funnel-teardown-guide"
```

---

## Alternative: Replicate for Model Variety

Add alongside NanoBanana:
```bash
claude mcp add replicate https://mcp.replicate.com/sse --transport sse --scope user
```

Authenticate: `/mcp auth replicate`

This gives access to FLUX.1 Pro, SDXL, and 1000+ other models. Use Replicate for artistic/abstract styles, NanoBanana for anything needing text rendering or photorealism.

---

## Cost Estimate

| Task | Images | Cost (NanoBanana 2 batch) |
|------|--------|--------------------------|
| 6 apps × 8 assets each | 48 | $1.63 |
| 13 accounts × 7 assets | 91 | $3.09 |
| 16 products × 3 assets | 48 | $1.63 |
| YouTube thumbnails (30) | 30 | $1.02 |
| Total | 217 | ~$7.37 |

At ~$0.034/image with batch API, the entire asset library costs less than $10.
