# RobloxMaxx Local Creation Station - Setup Guide

Complete setup for building Roblox games with Claude Code + MCP servers on your local machine.

---

## Prerequisites

- macOS (tested on macOS 15+)
- Roblox Studio installed and launched at least once
- Claude Code CLI installed (`claude` command available)
- Node.js 18+ installed
- Rust toolchain (for the official Roblox MCP server)

---

## MCP Server Comparison

We evaluated 4 MCP servers. Here's the verdict:

| Server | Tools | Best For | Maturity |
|--------|-------|----------|----------|
| **Roblox Official** (studio-rust-mcp-server) | 2 (run_code, insert_model) | Stable core operations | HIGH - official Roblox repo |
| **boshyxd/robloxstudio-mcp** | 37+ | Full Studio manipulation | HIGH - actively maintained, npm package |
| **ZubeidHendricks/roblox-studio-mcp-claude-code** | ~4 | Claude Code specific integration | MEDIUM - wrapper around official |
| **cynisca/roblox-mcp** | 8+ (play, screenshot, state) | Test automation, QA | MEDIUM - macOS focused, test-oriented |

**Recommendation: Install boshyxd/robloxstudio-mcp as primary (37+ tools, npm install, works with Claude Code directly) and cynisca/roblox-mcp as secondary for test automation.**

The official Roblox server only has 2 tools (run_code, insert_model). boshyxd wraps these plus 35 more: reading game hierarchy, editing scripts, bulk operations, property manipulation. It's the clear winner for development.

cynisca/roblox-mcp adds play testing, screenshot capture, and game state inspection, which fills the QA gap.

---

## Step 1: Install the Primary MCP Server (boshyxd/robloxstudio-mcp)

### 1a. Install the Roblox Studio Plugin

Download the plugin from the releases page:

```bash
# Option A: Download from GitHub releases
open "https://github.com/boshyxd/robloxstudio-mcp/releases"
# Download the .rbxmx file and place it in your Plugins folder

# Option B: The plugin auto-installs via the npm package in some configurations
# Check after running npx robloxstudio-mcp once
```

Place the plugin file in:
```
~/Documents/Roblox/Plugins/
```

### 1b. Enable HTTP Requests in Roblox Studio

1. Open Roblox Studio
2. Open any place (or create a new one)
3. Go to Game Settings > Security
4. Enable "Allow HTTP Requests"
5. The plugin should show "Connected" in the output panel

### 1c. Add to Claude Code

```bash
claude mcp add robloxstudio -- npx robloxstudio-mcp
```

That's it. Claude Code now has access to 37+ Roblox Studio tools.

To verify:
```bash
claude
# Then type: /mcp
# You should see "robloxstudio" listed with its tools
```

---

## Step 2: Install the Test Automation MCP Server (cynisca/roblox-mcp)

### 2a. Clone and Build

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/robloxmaxx/local
git clone https://github.com/cynisca/roblox-mcp.git roblox-test-mcp
cd roblox-test-mcp/roblox-test-mcp
npm install && npm run build
```

### 2b. Install its Roblox Studio Plugin

```bash
./roblox-plugin/install.sh
```

This copies the test plugin to `~/Documents/Roblox/Plugins/`.

### 2c. Grant Accessibility Permissions

On macOS, the test MCP needs accessibility permissions for your terminal app (Terminal.app, iTerm2, Warp, etc.):

System Settings > Privacy & Security > Accessibility > Add your terminal app

### 2d. Configure in Claude Code

Add to `~/.claude/settings.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "roblox-test": {
      "command": "node",
      "args": ["/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/robloxmaxx/local/roblox-test-mcp/roblox-test-mcp/dist/index.js"]
    }
  }
}
```

Or use the CLI:
```bash
claude mcp add roblox-test -- node /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/robloxmaxx/local/roblox-test-mcp/roblox-test-mcp/dist/index.js
```

### 2e. Configure Roblox Studio for Testing

1. In Roblox Studio, enable "Allow HTTP Requests" (Game Settings > Security)
2. In ServerScriptService properties, check "LoadStringEnabled"
3. Restart Claude Code to pick up new MCP servers

### 2f. Verify

```bash
cd roblox-test-mcp/roblox-test-mcp
npm run setup:verify
```

---

## Step 3: (Optional) Install Official Roblox MCP Server

If you want the official server as a fallback (only 2 tools but maximum stability):

### 3a. Install Rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

### 3b. Build from Source

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/robloxmaxx/local
git clone https://github.com/Roblox/studio-rust-mcp-server.git roblox-official-mcp
cd roblox-official-mcp
cargo build --release
```

The binary is at `target/release/rbx-studio-mcp`. Running `cargo run` also auto-configures Claude Desktop and installs the Studio plugin.

### 3c. Add to Claude Code

```bash
claude mcp add roblox-official -- /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/robloxmaxx/local/roblox-official-mcp/target/release/rbx-studio-mcp --stdio
```

---

## Step 4: Verify Full Setup

Open Roblox Studio with a place, then:

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/robloxmaxx/local
claude

# Inside Claude Code, check MCP:
# /mcp
# Should see: robloxstudio (37+ tools), roblox-test (8+ tools)

# Test basic operation:
# "Use the robloxstudio MCP to list all instances in the game"
```

---

## Using the Creation Station

### Start a New Game Project

```bash
# Copy a genre template
cp -r templates/tycoon ~/Documents/RobloxProjects/my-tycoon-game/

# Start Claude Code in that directory (it picks up the CLAUDE.md automatically)
cd ~/Documents/RobloxProjects/my-tycoon-game/
claude
```

The CLAUDE.md in each template directory loads genre-specific context, monetization strategies, and Roblox meta intelligence into Claude Code automatically.

### Quick Launch (Use start.sh)

```bash
./start.sh
# Interactive: picks genre, creates project dir, launches Claude Code
```

### What You Can Ask Claude Code to Do

With the MCP servers connected:

- "Scaffold a complete tycoon game with dropper-rebirth mechanics"
- "Read the current game hierarchy and suggest improvements"
- "Add a pet system with egg hatching and weighted rarities"
- "Create a gamepass for 2x earnings and wire up MarketplaceService"
- "Find all scripts using deprecated wait() and update to task.wait()"
- "Run this Lua code in Studio to test the combat system"
- "Take a screenshot of the current game state"
- "Start playtesting and check if the player spawns correctly"

### Parallel Game Development with Agent Teams

Claude Code supports agent teams. You can build multiple games simultaneously:

```bash
# Terminal 1: Tycoon game
cd ~/Documents/RobloxProjects/my-tycoon/
claude

# Terminal 2: Obby game
cd ~/Documents/RobloxProjects/my-obby/
claude

# Terminal 3: Simulator game
cd ~/Documents/RobloxProjects/my-simulator/
claude
```

Each instance connects to the same Roblox Studio (open different places in tabs) or you can alternate between Studio sessions.

---

## Troubleshooting

**"Plugin not connected"**
- Make sure Roblox Studio is open with a place loaded
- Check Game Settings > Security > "Allow HTTP Requests" is ON
- Check the Output panel in Studio for connection messages
- Try restarting the MCP server: `claude mcp remove robloxstudio && claude mcp add robloxstudio -- npx robloxstudio-mcp`

**"MCP server not found"**
- Run `claude /mcp` to list active servers
- Ensure Node.js 18+ is installed: `node --version`
- Try running `npx robloxstudio-mcp` directly to check for errors

**"Permission denied" (test MCP)**
- Grant accessibility permissions to your terminal app
- System Settings > Privacy & Security > Accessibility

**"LoadString is not allowed"**
- Enable LoadStringEnabled in ServerScriptService properties
- Required for the test automation MCP to execute scripts

**Slow performance**
- Close unnecessary Studio tabs
- The MCP communicates via HTTP on localhost, so network isn't a bottleneck
- If Claude Code is slow, check your context window usage with /compact

---

## File Structure

```
local/
├── SETUP_GUIDE.md          # This file
├── CLAUDE.md               # Master context (loaded by Claude Code)
├── start.sh                # Launch script
├── templates/
│   ├── tycoon/
│   │   └── CLAUDE.md       # Tycoon-specific context
│   ├── obby/
│   │   └── CLAUDE.md       # Obby-specific context
│   └── simulator/
│       └── CLAUDE.md       # Simulator-specific context
├── roblox-test-mcp/        # Test automation MCP (after cloning)
└── roblox-official-mcp/    # Official MCP (optional, after cloning)
```
