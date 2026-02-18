#!/usr/bin/env bash
# ============================================================
# PRINTMAXX Worker Mega Installer
# One script to set up a fresh macOS machine as a PRINTMAXX worker
# Idempotent — safe to run multiple times
# Usage: bash scripts/worker_mega_installer.sh [--dry-run] [--verify] [--skip-brew] [--skip-ollama]
# ============================================================

set -euo pipefail

# --- Config ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_FILE="$PROJECT_ROOT/AUTOMATIONS/logs/worker_install_$(date +%Y%m%d_%H%M%S).log"
DRY_RUN=false
VERIFY_ONLY=false
SKIP_BREW=false
SKIP_OLLAMA=false

for arg in "$@"; do
  case $arg in
    --dry-run) DRY_RUN=true ;;
    --verify) VERIFY_ONLY=true ;;
    --skip-brew) SKIP_BREW=true ;;
    --skip-ollama) SKIP_OLLAMA=true ;;
    --help|-h)
      echo "Usage: bash scripts/worker_mega_installer.sh [--dry-run] [--verify] [--skip-brew] [--skip-ollama]"
      exit 0 ;;
  esac
done

mkdir -p "$PROJECT_ROOT/AUTOMATIONS/logs"

# --- Logging ---
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"; }
ok()  { log "  ✓ $1"; }
skip() { log "  → SKIP: $1"; }
fail() { log "  ✗ FAIL: $1"; }
section() { log ""; log "========== $1 =========="; }
run() {
  if $DRY_RUN; then
    log "  [DRY RUN] $*"
  else
    "$@" 2>&1 | tee -a "$LOG_FILE"
  fi
}

log "PRINTMAXX Worker Mega Installer"
log "Project root: $PROJECT_ROOT"
log "Dry run: $DRY_RUN"
log "Verify only: $VERIFY_ONLY"
log ""

# ============================================================
section "1. SYSTEM INFO"
# ============================================================
log "macOS: $(sw_vers -productVersion 2>/dev/null || echo 'unknown')"
log "Arch: $(uname -m)"
log "User: $(whoami)"
log "Shell: $SHELL"

# ============================================================
section "2. HOMEBREW"
# ============================================================
if $SKIP_BREW; then
  skip "Homebrew (--skip-brew)"
elif command -v brew &>/dev/null; then
  ok "Homebrew already installed ($(brew --version | head -1))"
elif ! $VERIFY_ONLY; then
  log "Installing Homebrew..."
  run /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  fail "Homebrew not installed"
fi

# --- Brew packages ---
BREW_PACKAGES=(git curl wget jq ffmpeg tree watch htop)
if ! $SKIP_BREW && command -v brew &>/dev/null; then
  for pkg in "${BREW_PACKAGES[@]}"; do
    if brew list "$pkg" &>/dev/null; then
      ok "$pkg installed"
    elif ! $VERIFY_ONLY; then
      log "  Installing $pkg..."
      run brew install "$pkg"
    else
      fail "$pkg not installed"
    fi
  done
fi

# ============================================================
section "3. PYTHON 3.12+"
# ============================================================
PYTHON=""
for p in python3.12 python3.13 python3; do
  if command -v "$p" &>/dev/null; then
    ver=$("$p" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
    major=$(echo "$ver" | cut -d. -f1)
    minor=$(echo "$ver" | cut -d. -f2)
    if [ "$major" -ge 3 ] && [ "$minor" -ge 12 ]; then
      PYTHON="$p"
      break
    fi
  fi
done

if [ -n "$PYTHON" ]; then
  ok "Python: $($PYTHON --version)"
else
  if ! $VERIFY_ONLY && command -v brew &>/dev/null; then
    log "Installing Python 3.12..."
    run brew install python@3.12
    PYTHON="python3.12"
  else
    fail "Python 3.12+ not found"
    PYTHON="python3"
  fi
fi

# ============================================================
section "4. PYTHON PACKAGES (pip)"
# ============================================================
PIP_PACKAGES=(
  # Core HTTP/scraping
  requests
  beautifulsoup4
  lxml
  # Browser automation
  playwright
  selenium
  webdriver-manager
  # Data processing
  numpy
  pandas
  openpyxl
  # TUI/terminal
  rich
  textual
  # Discord bot
  "discord.py"
  # ML/AI (optional but used)
  torch
  soundfile
  # Google Trends
  pytrends
  # Misc
  schedule
  python-dotenv
  aiohttp
  aiofiles
  pyyaml
  Pillow
)

if ! $VERIFY_ONLY; then
  log "Installing Python packages..."
  for pkg in "${PIP_PACKAGES[@]}"; do
    if $DRY_RUN; then
      log "  [DRY RUN] pip install $pkg"
    else
      $PYTHON -m pip install --quiet "$pkg" 2>&1 | tail -1 | tee -a "$LOG_FILE" || fail "pip install $pkg"
    fi
  done
  ok "Python packages installed"

  # Playwright browsers
  log "Installing Playwright browsers (headless)..."
  if $DRY_RUN; then
    log "  [DRY RUN] playwright install chromium"
  else
    $PYTHON -m playwright install chromium 2>&1 | tee -a "$LOG_FILE" || fail "Playwright chromium install"
    ok "Playwright chromium installed"
  fi
else
  for pkg in requests beautifulsoup4 playwright selenium openpyxl rich numpy; do
    if $PYTHON -c "import ${pkg//-/_}" 2>/dev/null; then
      ok "Python: $pkg"
    else
      fail "Python: $pkg not installed"
    fi
  done
fi

# ============================================================
section "5. NODE.JS >= 22"
# ============================================================
NODE_OK=false
if command -v node &>/dev/null; then
  NODE_VER=$(node --version | grep -oE '[0-9]+' | head -1)
  if [ "$NODE_VER" -ge 22 ]; then
    ok "Node.js $(node --version)"
    NODE_OK=true
  else
    log "  Node.js $(node --version) is too old (need >= 22)"
  fi
fi

if ! $NODE_OK; then
  if ! $VERIFY_ONLY && command -v brew &>/dev/null; then
    log "Installing Node.js 22..."
    run brew install node@22
    ok "Node.js installed"
  else
    fail "Node.js >= 22 not found"
  fi
fi

# --- NPM global packages ---
NPM_GLOBALS=(openclaw)
if command -v npm &>/dev/null; then
  for pkg in "${NPM_GLOBALS[@]}"; do
    if npm list -g "$pkg" &>/dev/null 2>&1; then
      ok "npm global: $pkg"
    elif ! $VERIFY_ONLY; then
      log "  Installing $pkg globally..."
      run npm install -g "$pkg@latest"
    else
      fail "npm global: $pkg not installed"
    fi
  done
fi

# ============================================================
section "6. OLLAMA (local models)"
# ============================================================
if $SKIP_OLLAMA; then
  skip "Ollama (--skip-ollama)"
elif command -v ollama &>/dev/null; then
  ok "Ollama installed ($(ollama --version 2>/dev/null || echo 'unknown'))"
elif ! $VERIFY_ONLY && command -v brew &>/dev/null; then
  log "Installing Ollama..."
  run brew install ollama
else
  fail "Ollama not installed"
fi

# ============================================================
section "7. PROJECT DIRECTORIES"
# ============================================================
REQUIRED_DIRS=(
  AUTOMATIONS/logs
  AUTOMATIONS/_archive
  AUTOMATIONS/content_posting
  AUDIT
  LEDGER
  OPS
  OPS/playbooks
  OPS/openclaw
  output
  output/dashboard
  output/cron_fleet
  output/openrouter_budget_guard
  output/clawwork_sidecar
  output/qwen_tts
  ralph/loops
)

for dir in "${REQUIRED_DIRS[@]}"; do
  full="$PROJECT_ROOT/$dir"
  if [ -d "$full" ]; then
    ok "Dir: $dir"
  elif ! $VERIFY_ONLY; then
    run mkdir -p "$full"
    ok "Created: $dir"
  else
    fail "Dir missing: $dir"
  fi
done

# ============================================================
section "8. NODE ROLE"
# ============================================================
ROLE_FILE="$PROJECT_ROOT/OPS/NODE_ROLE.json"
if [ -f "$ROLE_FILE" ]; then
  ok "NODE_ROLE.json exists: $(cat "$ROLE_FILE")"
else
  if ! $VERIFY_ONLY; then
    echo '{"role":"worker","machine":"m2","set_at":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"}' > "$ROLE_FILE"
    ok "Created NODE_ROLE.json (worker)"
  else
    fail "NODE_ROLE.json missing"
  fi
fi

# ============================================================
section "9. ENVIRONMENT TEMPLATE"
# ============================================================
ENV_FILE="$PROJECT_ROOT/.env.worker.template"
if [ -f "$ENV_FILE" ]; then
  ok ".env.worker.template exists"
else
  if ! $VERIFY_ONLY; then
    cat > "$ENV_FILE" << 'ENVEOF'
# PRINTMAXX Worker Environment Variables
# Copy this to .env and fill in values

# OpenRouter (required for agent loops)
OPENROUTER_API_KEY=sk-or-REPLACE_ME
OPENROUTER_ADMIN_API_KEY=sk-or-admin-REPLACE_ME

# OpenClaw gateway
OPENCLAW_GATEWAY_TOKEN=REPLACE_ME_LONG_RANDOM_STRING

# Email infrastructure (for cold email automation)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=

# Social accounts (for posting automation)
TWITTER_AUTH_TOKEN=
TWITTER_CT0=

# App Store
APPLE_DEVELOPER_TEAM_ID=
GOOGLE_PLAY_SERVICE_ACCOUNT_JSON=

# Analytics
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX

# Brave browser path (for cookie extraction)
BRAVE_COOKIE_DB=~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Cookies

# Firecrawl (if using MCP)
FIRECRAWL_API_KEY=

# Discord (if using bot)
DISCORD_BOT_TOKEN=
ENVEOF
    ok "Created .env.worker.template"
  else
    fail ".env.worker.template missing"
  fi
fi

# ============================================================
section "10. CRON SETUP"
# ============================================================
CRON_FILE="$PROJECT_ROOT/AUTOMATIONS/crontab_secure_minimal.txt"
if [ -f "$CRON_FILE" ]; then
  ok "Secure cron file exists"
  CRON_LINES=$(grep -c "^[^#]" "$CRON_FILE" 2>/dev/null || echo 0)
  log "  Active cron entries: $CRON_LINES"
  if ! $VERIFY_ONLY && ! $DRY_RUN; then
    log "  To install: crontab $CRON_FILE"
  fi
else
  skip "No secure cron file found"
fi

# ============================================================
section "11. SSH AUTHORIZED KEYS"
# ============================================================
AUTH_KEYS="$HOME/.ssh/authorized_keys"
if [ -f "$AUTH_KEYS" ]; then
  KEY_COUNT=$(wc -l < "$AUTH_KEYS" | tr -d ' ')
  ok "authorized_keys exists ($KEY_COUNT keys)"
else
  log "  No authorized_keys file. Run setup_control_to_worker_ssh.sh from control node."
fi

# ============================================================
section "12. OPENCLAW CONFIG"
# ============================================================
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"
OPENCLAW_TEMPLATE="$PROJECT_ROOT/OPS/openclaw/openclaw_worker_template.json5"
if [ -f "$OPENCLAW_CONFIG" ]; then
  ok "OpenClaw config exists"
elif [ -f "$OPENCLAW_TEMPLATE" ]; then
  if ! $VERIFY_ONLY; then
    mkdir -p "$HOME/.openclaw"
    # Strip json5 comments for json compatibility
    sed 's|//.*||g' "$OPENCLAW_TEMPLATE" | grep -v '^\s*$' > "$OPENCLAW_CONFIG" 2>/dev/null || cp "$OPENCLAW_TEMPLATE" "$OPENCLAW_CONFIG"
    ok "Seeded OpenClaw config from template"
  else
    fail "OpenClaw config missing (template available)"
  fi
else
  skip "No OpenClaw template found"
fi

# ============================================================
section "13. HEALTH CHECK"
# ============================================================
CHECKS_PASSED=0
CHECKS_FAILED=0

check() {
  if "$@" &>/dev/null; then
    ok "$1"
    ((CHECKS_PASSED++))
  else
    fail "$1"
    ((CHECKS_FAILED++))
  fi
}

check command -v brew
check command -v git
check command -v $PYTHON
check command -v node
check command -v npm
check command -v curl
check command -v jq
check command -v ffmpeg
check test -d "$PROJECT_ROOT/AUTOMATIONS"
check test -d "$PROJECT_ROOT/LEDGER"
check test -d "$PROJECT_ROOT/OPS"
check test -f "$PROJECT_ROOT/CODEX.md"
check test -f "$PROJECT_ROOT/.claude/CLAUDE.md"

log ""
log "========== SUMMARY =========="
log "Checks passed: $CHECKS_PASSED"
log "Checks failed: $CHECKS_FAILED"
log "Log file: $LOG_FILE"

if [ "$CHECKS_FAILED" -eq 0 ]; then
  log ""
  log "Worker is READY. Next steps:"
  log "  1. Copy .env.worker.template to .env and fill in secrets"
  log "  2. Run: bash scripts/setup_openclaw_worker_stack.sh"
  log "  3. Install cron: crontab AUTOMATIONS/crontab_secure_minimal.txt"
  log "  4. Start Ship Captain: ./ship.sh"
else
  log ""
  log "Worker has $CHECKS_FAILED issues. Fix them and rerun with --verify."
fi
