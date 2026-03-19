# sovrun Connector Registry

118 MCP (Model Context Protocol) connectors for sovrun agents. Slack, Stripe, GitHub, OpenAI, Playwright, and 100+ more. One setup script, auto-generated MCP config.

## Quick Start

```bash
# See all available connectors
python connectors/setup.py --list

# Check what's configured
python connectors/setup.py --status

# Set up a specific connector
python connectors/setup.py --setup slack

# Generate MCP config for configured connectors
python connectors/setup.py --mcp-config > mcp_servers.json

# Search for connectors
python connectors/setup.py --search email

# View statistics
python connectors/setup.py --stats
```

## What this is

A curated registry of MCP server commands and their config. sovrun doesn't reimplement connectors. It points your agents to existing MCP servers (community-maintained, Composio, or Pipedream) so you don't have to find and configure them yourself.

## Registry Overview

| Category | Count | Description |
|----------|-------|-------------|
| communication | 9 | Slack, Discord, Telegram, WhatsApp, Email, Teams, Twilio |
| social | 11 | Twitter/X, LinkedIn, Reddit, YouTube, TikTok, Instagram, Bluesky |
| data | 9 | Google Sheets, Notion, Airtable, PostgreSQL, MongoDB, Supabase |
| dev | 10 | GitHub, GitLab, Linear, Jira, Vercel, Netlify |
| commerce | 7 | Stripe, Shopify, Gumroad, PayPal, Amazon |
| ai | 10 | OpenAI, Anthropic, Gemini, Replicate, HuggingFace, Pinecone |
| storage | 6 | Google Drive, S3, Cloudflare R2, Dropbox |
| crm | 4 | HubSpot, Salesforce, Pipedrive, Zoho |
| marketing | 7 | Mailchimp, SendGrid, Resend, Beehiiv, ConvertKit |
| scraping | 6 | Firecrawl, Playwright, Puppeteer, Browserbase, Apify |
| search | 6 | Brave, Tavily, Exa, Google, Perplexity |
| monitoring | 5 | Sentry, Datadog, Grafana, PagerDuty |
| productivity | 7 | Google Calendar, Zoom, Figma, Calendly |
| finance | 3 | Plaid, QuickBooks, Wise |
| analytics | 4 | PostHog, Google Analytics, Amplitude, Mixpanel |
| support | 4 | Zendesk, Intercom, Freshdesk, Crisp |
| infrastructure | 8 | Docker, Kubernetes, AWS, HTTP, Webhooks, Composio, Pipedream |
| media | 2 | Cloudinary, ImgBB |

## MCP Server Availability

About 50% of connectors have existing MCP servers you can use directly. For the rest:

1. **Composio** - meta-connector with 100+ tools and built-in auth. One MCP server covers many services.
2. **Pipedream** - 2,400+ API connectors with managed auth. Bridges any gap.
3. **Custom** - build your own using the MCP SDK (TypeScript or Python). 50-100 lines for most integrations.

## Adding a Connector

Add a new entry to `registry.json`:

```json
{
  "name": "service_name",
  "display_name": "Service Name",
  "category": "category",
  "mcp_server": "npx -y @scope/mcp-server-name",
  "mcp_available": true,
  "setup_requires": ["API_KEY_VAR"],
  "description": "What this connector does",
  "capabilities": ["action1", "action2"],
  "competitors_with_this": ["n8n", "zapier"],
  "priority": "high"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique snake_case identifier |
| `display_name` | string | Human-readable name |
| `category` | string | One of the registry categories |
| `mcp_server` | string/null | npx/uvx command to run the MCP server, or null |
| `mcp_available` | boolean | Whether an MCP server exists |
| `setup_requires` | string[] | Environment variables needed |
| `description` | string | What the connector enables |
| `capabilities` | string[] | Specific actions available |
| `competitors_with_this` | string[] | Which platforms also offer this |
| `priority` | string | "high", "medium", or "low" |

## Competitor Coverage

Built by auditing integrations from:

- **n8n** - 400+ native nodes, 600+ community nodes
- **Zapier** - 8,500+ app integrations
- **Make.com** - 3,000+ app connectors
- **Hermes Agent** - 40+ bundled skills, messaging gateway
- **OpenHands** - GitHub, GitLab, Slack native integrations

The registry includes connectors relevant to autonomous agent workflows (not simple webhook triggers). Each entry tracks whether an MCP server exists, what env vars are needed, and what the connector can actually do.

## Using with Claude Desktop / Claude Code

Run `python connectors/setup.py --mcp-config` to generate a config block, then merge it into your `claude_desktop_config.json` (or `.claude.json` for Claude Code):

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-...",
        "SLACK_TEAM_ID": "T..."
      }
    }
  }
}
```
