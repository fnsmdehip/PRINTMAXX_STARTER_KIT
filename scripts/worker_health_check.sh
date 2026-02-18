#!/usr/bin/env bash
# ============================================================
# PRINTMAXX Worker Health Check
# Quick verify that the worker is ready to run
# Usage: bash scripts/worker_health_check.sh
# ============================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PASS=0
FAIL=0
WARN=0

ok()   { echo "  ✓ $1"; ((PASS++)); }
fail() { echo "  ✗ $1"; ((FAIL++)); }
warn() { echo "  ⚠ $1"; ((WARN++)); }

check_cmd() {
  if command -v "$1" &>/dev/null; then
    ok "$1 $(command -v "$1")"
  else
    fail "$1 not found"
  fi
}

check_python_pkg() {
  if python3 -c "import $1" 2>/dev/null; then
    ok "python: $1"
  else
    fail "python: $1 missing"
  fi
}

echo "PRINTMAXX Worker Health Check"
echo "Project: $PROJECT_ROOT"
echo ""

# --- System tools ---
echo "=== System Tools ==="
check_cmd brew
check_cmd git
check_cmd curl
check_cmd jq
check_cmd ffmpeg
check_cmd tree

# --- Runtimes ---
echo ""
echo "=== Runtimes ==="
check_cmd python3
if command -v python3 &>/dev/null; then
  VER=$(python3 --version 2>&1)
  MINOR=$(echo "$VER" | grep -oE '[0-9]+\.[0-9]+' | cut -d. -f2)
  if [ "$MINOR" -ge 12 ]; then ok "Python version: $VER"; else warn "Python version: $VER (want 3.12+)"; fi
fi

check_cmd node
if command -v node &>/dev/null; then
  NVER=$(node --version | grep -oE '[0-9]+' | head -1)
  if [ "$NVER" -ge 22 ]; then ok "Node version: $(node --version)"; else warn "Node version: $(node --version) (want 22+)"; fi
fi

check_cmd npm
check_cmd npx

# --- Python packages ---
echo ""
echo "=== Python Packages ==="
check_python_pkg requests
check_python_pkg bs4
check_python_pkg playwright
check_python_pkg selenium
check_python_pkg openpyxl
check_python_pkg numpy
check_python_pkg rich
check_python_pkg pandas
check_python_pkg yaml
check_python_pkg dotenv
check_python_pkg aiohttp

# --- NPM globals ---
echo ""
echo "=== NPM Globals ==="
if npm list -g openclaw &>/dev/null 2>&1; then ok "openclaw"; else fail "openclaw not installed"; fi

# --- Ollama ---
echo ""
echo "=== Local AI ==="
if command -v ollama &>/dev/null; then
  ok "ollama installed"
  if pgrep -x ollama &>/dev/null; then ok "ollama running"; else warn "ollama not running (start with: ollama serve)"; fi
else
  warn "ollama not installed (optional)"
fi

# --- Project structure ---
echo ""
echo "=== Project Structure ==="
for dir in AUTOMATIONS AUTOMATIONS/logs LEDGER OPS OPS/openclaw output ralph; do
  if [ -d "$PROJECT_ROOT/$dir" ]; then ok "dir: $dir"; else fail "dir: $dir missing"; fi
done

for f in CODEX.md .claude/CLAUDE.md AUTOMATIONS/ship_captain.py ship.sh; do
  if [ -f "$PROJECT_ROOT/$f" ]; then ok "file: $f"; else fail "file: $f missing"; fi
done

# --- Node role ---
echo ""
echo "=== Worker Config ==="
ROLE_FILE="$PROJECT_ROOT/OPS/NODE_ROLE.json"
if [ -f "$ROLE_FILE" ]; then
  ROLE=$(python3 -c "import json; print(json.load(open('$ROLE_FILE')).get('role','unknown'))" 2>/dev/null || echo "unknown")
  if [ "$ROLE" = "worker" ]; then ok "Node role: worker"; else warn "Node role: $ROLE (expected worker)"; fi
else
  fail "NODE_ROLE.json missing"
fi

# --- Env vars ---
echo ""
echo "=== Environment Variables ==="
if [ -n "${OPENROUTER_API_KEY:-}" ]; then ok "OPENROUTER_API_KEY set"; else warn "OPENROUTER_API_KEY not set"; fi
if [ -n "${OPENCLAW_GATEWAY_TOKEN:-}" ]; then ok "OPENCLAW_GATEWAY_TOKEN set"; else warn "OPENCLAW_GATEWAY_TOKEN not set"; fi

# --- OpenClaw config ---
if [ -f "$HOME/.openclaw/openclaw.json" ]; then ok "OpenClaw config exists"; else warn "OpenClaw config missing (~/.openclaw/openclaw.json)"; fi

# --- Cron ---
echo ""
echo "=== Cron ==="
CRON_COUNT=$(crontab -l 2>/dev/null | grep -c "^[^#]" || echo 0)
if [ "$CRON_COUNT" -gt 0 ]; then ok "Cron active: $CRON_COUNT entries"; else warn "No cron entries installed"; fi

# --- SSH ---
echo ""
echo "=== SSH ==="
if [ -f "$HOME/.ssh/authorized_keys" ]; then
  KEY_COUNT=$(wc -l < "$HOME/.ssh/authorized_keys" | tr -d ' ')
  ok "authorized_keys: $KEY_COUNT keys"
else
  warn "No authorized_keys (control node can't SSH in)"
fi

# --- Summary ---
echo ""
echo "================================"
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "  WARN: $WARN"
echo "================================"

if [ "$FAIL" -eq 0 ]; then
  echo ""
  echo "Worker is READY."
  echo "Start with: ./ship.sh"
  exit 0
else
  echo ""
  echo "Worker has $FAIL failures. Fix and rerun."
  echo "Quick fix: bash scripts/worker_mega_installer.sh"
  exit 1
fi
