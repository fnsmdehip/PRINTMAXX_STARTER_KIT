#!/usr/bin/env bash
set -euo pipefail

# RobloxMaxx Local Creation Station - Launch Script
# Checks MCP servers, creates project from template, starts Claude Code

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$SCRIPT_DIR/templates"
PROJECTS_DIR="${ROBLOX_PROJECTS_DIR:-$HOME/Documents/RobloxProjects}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  ____       _     _           __  __                "
echo " |  _ \\ ___ | |__ | | _____  _|  \\/  | __ ___  ___  "
echo " | |_) / _ \\| '_ \\| |/ _ \\ \\/ / |\\/| |/ _\` \\ \\/ / "
echo " |  _ < (_) | |_) | | (_) >  <| |  | | (_| |>  <   "
echo " |_| \\_\\___/|_.__/|_|\\___/_/\\_\\_|  |_|\\__,_/_/\\_\\  "
echo "                                                     "
echo "  Local Creation Station                             "
echo -e "${NC}"

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check Claude Code
if ! command -v claude &> /dev/null; then
    echo -e "${RED}ERROR: Claude Code CLI not found. Install from https://claude.ai/code${NC}"
    exit 1
fi
echo -e "${GREEN}  Claude Code CLI: OK${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}ERROR: Node.js not found. Install from https://nodejs.org${NC}"
    exit 1
fi
NODE_VERSION=$(node --version | sed 's/v//' | cut -d. -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo -e "${RED}ERROR: Node.js 18+ required. Current: $(node --version)${NC}"
    exit 1
fi
echo -e "${GREEN}  Node.js $(node --version): OK${NC}"

# Check if robloxstudio MCP is configured
MCP_CHECK=$(claude mcp list 2>/dev/null || echo "")
if echo "$MCP_CHECK" | grep -qi "robloxstudio"; then
    echo -e "${GREEN}  RobloxStudio MCP: configured${NC}"
else
    echo -e "${YELLOW}  RobloxStudio MCP: not configured${NC}"
    echo -e "${YELLOW}  Adding robloxstudio MCP server...${NC}"
    claude mcp add robloxstudio -- npx robloxstudio-mcp
    echo -e "${GREEN}  RobloxStudio MCP: added${NC}"
fi

# Check Roblox Studio running (informational only)
if pgrep -x "RobloxStudio" > /dev/null 2>&1; then
    echo -e "${GREEN}  Roblox Studio: running${NC}"
else
    echo -e "${YELLOW}  Roblox Studio: not running (start it and open a place before using MCP tools)${NC}"
fi

echo ""

# Genre selection
echo -e "${CYAN}Select game genre:${NC}"
echo "  1) Tycoon (dropper-rebirth, currency, upgrades)"
echo "  2) Obby (obstacle course, checkpoints, speedrun)"
echo "  3) Simulator (click-earn, pets, rebirths, zones)"
echo "  4) RPG (quests, combat, loot, dungeons)"
echo "  5) Horror (monster AI, atmosphere, puzzles)"
echo "  6) General (blank project with master CLAUDE.md)"
echo ""
read -p "Genre [1-6]: " GENRE_CHOICE

case "$GENRE_CHOICE" in
    1) GENRE="tycoon" ;;
    2) GENRE="obby" ;;
    3) GENRE="simulator" ;;
    4) GENRE="rpg" ;;
    5) GENRE="horror" ;;
    6) GENRE="general" ;;
    *) GENRE="general" ;;
esac

# Project name
echo ""
read -p "Project name (e.g., my-tycoon-game): " PROJECT_NAME
if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME="roblox-${GENRE}-$(date +%Y%m%d)"
fi

# Create project directory
PROJECT_DIR="$PROJECTS_DIR/$PROJECT_NAME"
mkdir -p "$PROJECT_DIR"

# Copy template CLAUDE.md
if [ "$GENRE" != "general" ] && [ -f "$TEMPLATES_DIR/$GENRE/CLAUDE.md" ]; then
    cp "$TEMPLATES_DIR/$GENRE/CLAUDE.md" "$PROJECT_DIR/CLAUDE.md"
    echo -e "${GREEN}Copied ${GENRE} template to $PROJECT_DIR/CLAUDE.md${NC}"
else
    # Copy master CLAUDE.md for general projects
    cp "$SCRIPT_DIR/CLAUDE.md" "$PROJECT_DIR/CLAUDE.md"
    echo -e "${GREEN}Copied master CLAUDE.md to $PROJECT_DIR/CLAUDE.md${NC}"
fi

# Create basic project structure
mkdir -p "$PROJECT_DIR/src"
mkdir -p "$PROJECT_DIR/docs"
mkdir -p "$PROJECT_DIR/assets"

echo ""
echo -e "${GREEN}Project created at: $PROJECT_DIR${NC}"
echo ""
echo -e "${CYAN}Launching Claude Code...${NC}"
echo -e "${YELLOW}Tip: Make sure Roblox Studio is open with a place loaded before using MCP tools.${NC}"
echo ""

# Launch Claude Code in the project directory
cd "$PROJECT_DIR"
exec claude
