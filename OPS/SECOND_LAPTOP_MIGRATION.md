# PRINTMAXX: Second Laptop Migration & Autonomous Ops

## Target Machine
- MacBook Pro M2, 16GB RAM, 1TB storage
- Role: WORKER node (autonomous execution, long agent runs)
- Main laptop remains CONTROL node (human approval, sensitive keys, personal files)

## Why Quarantine
- PRINTMAXX is 27GB with 595K files. Isolating it protects main laptop.
- Long autonomous agent runs can consume CPU/RAM for hours. Offload to dedicated machine.
- Worker node can run with `--dangerously-skip-permissions` safely since it only contains PRINTMAXX.
- If an agent goes rogue, blast radius is limited to the worker laptop.

---

## STEP 1: Migrate PRINTMAXX to Second Laptop

### On Main Laptop (one-time)

```bash
# 1. Create a transfer archive (exclude node_modules, .git objects, caches)
cd /Users/macbookpro/Documents/p/
tar czf /tmp/PRINTMAXX_TRANSFER.tar.gz \
  --exclude='node_modules' \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='.venv' \
  --exclude='*.pyc' \
  --exclude='.DS_Store' \
  PRINTMAXX_STARTER_KITttttt/

# Check size (should be ~2-5GB without node_modules/.git)
ls -lh /tmp/PRINTMAXX_TRANSFER.tar.gz

# 2. Transfer to second laptop via AirDrop, USB drive, or network
# Option A: AirDrop (easiest)
# Option B: scp (if SSH is set up)
scp /tmp/PRINTMAXX_TRANSFER.tar.gz user@second-laptop:/tmp/
# Option C: USB drive
cp /tmp/PRINTMAXX_TRANSFER.tar.gz /Volumes/USB_DRIVE/
```

### On Second Laptop (one-time setup)

```bash
# 1. Extract PRINTMAXX
mkdir -p ~/Documents/p/
cd ~/Documents/p/
tar xzf /tmp/PRINTMAXX_TRANSFER.tar.gz

# 2. Initialize git repo (fresh, not carrying main laptop history)
cd PRINTMAXX_STARTER_KITttttt
git init
git add -A
git commit -m "PRINTMAXX worker node: initial state from main laptop transfer"

# 3. Install system dependencies
brew install python3 node

# 4. Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# 5. Authenticate Claude Code
claude login
# OR set API key directly:
export ANTHROPIC_API_KEY="your-key-here"

# 6. Install Python dependencies for PRINTMAXX automations
cd AUTOMATIONS
pip3 install -r requirements.txt 2>/dev/null || true
# Most scripts use stdlib only. Install as needed.

# 7. Install Node dependencies for Before You
cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/BEFORE_YOU/
# Symlink or copy the before-you codebase
# (it lives inside ancestry-research on main laptop, copy it here)
```

### Also Transfer: Before You Codebase

```bash
# On main laptop
cd /Users/macbookpro/Documents/ancestry-research/
tar czf /tmp/BEFORE_YOU_TRANSFER.tar.gz \
  --exclude='node_modules' \
  --exclude='.git' \
  --exclude='dist' \
  before-you/

# Transfer same way as above, then on second laptop:
cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/BEFORE_YOU/
tar xzf /tmp/BEFORE_YOU_TRANSFER.tar.gz
cd before-you/generator && npm install
cd ../landing && npm install
cd ../template && npm install
```

---

## STEP 2: Configure Worker Node

### Set Environment Variables

Create `~/.zshrc` additions on second laptop:

```bash
# PRINTMAXX Worker Node
export PRINTMAXX_NODE_ROLE="worker"
export PRINTMAXX_ROOT="$HOME/Documents/p/PRINTMAXX_STARTER_KITttttt"

# LLM Keys
export GROQ_API_KEY="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"
export LLM_API_KEY="$GROQ_API_KEY"
export LLM_API_URL="https://api.groq.com/openai/v1"
export LLM_MODEL="llama-3.3-70b-versatile"

# Stripe (live)
export STRIPE_SECRET_KEY="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"

# Surge (for deploys)
export SURGE_TOKEN="your-surge-token"

# Claude Code autonomous mode
export CLAUDE_CODE_ALLOW_SKIP_PERMISSIONS=1
```

### Create the Worker CLAUDE.md

See `CLAUDE_WORKER.md` (created separately) for the full autonomous operating instructions that go in `~/Documents/p/PRINTMAXX_STARTER_KITttttt/.claude/CLAUDE.md` on the worker node.

---

## STEP 3: Running Autonomous Agent Sessions

### Method 1: tmux + CLI (recommended for long runs)

```bash
# Start a named tmux session
tmux new-session -s printmaxx

# Run a long autonomous task
cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt
claude -p "Run the daily tactical engine, execute top 5 priority tasks from Capital Genesis stack, and report results" \
  --allowedTools "Bash,Read,Edit,Write,Glob,Grep" \
  --max-turns 50 \
  --output-format stream-json \
  2>&1 | tee /tmp/printmaxx-run-$(date +%Y%m%d-%H%M).log

# Detach from tmux: Ctrl+B then D
# Reattach later: tmux attach -t printmaxx
```

### Method 2: Scheduled Autonomous Runs (launchd)

```bash
# Create a launchd plist for recurring runs
cat > ~/Library/LaunchAgents/com.printmaxx.autonomous.plist << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.printmaxx.autonomous</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt && claude -p "$(cat OPS/AUTONOMOUS_DAILY_PROMPT.md)" --allowedTools "Bash,Read,Edit,Write,Glob,Grep" --max-turns 30 --output-format json >> /tmp/printmaxx-auto.log 2>&1</string>
    </array>
    <key>StartInterval</key>
    <integer>21600</integer>
    <key>StandardOutPath</key>
    <string>/tmp/printmaxx-auto-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/printmaxx-auto-stderr.log</string>
</dict>
</plist>
PLIST

# Load it
launchctl load ~/Library/LaunchAgents/com.printmaxx.autonomous.plist
```

### Method 3: Remote Control from Main Laptop via SSH

```bash
# On second laptop: enable SSH
# System Settings > General > Sharing > Remote Login > ON

# On main laptop: run commands on worker
ssh user@second-laptop "cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt && claude -p 'status report: what ran, what revenue, what errors' --output-format json"

# Or start a long run remotely
ssh user@second-laptop "tmux new-session -d -s agent && tmux send-keys -t agent 'cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt && claude -p \"Execute top priority from Capital Genesis stack\" --allowedTools Bash,Read,Edit,Write,Glob,Grep --max-turns 30' Enter"

# Check on it
ssh user@second-laptop "tmux capture-pane -t agent -p | tail -20"
```

### Method 4: Claude Desktop SSH Session

1. Open Claude Desktop on main laptop
2. Click environment dropdown > Add SSH connection
3. Enter: `user@second-laptop-ip`
4. Select the PRINTMAXX directory
5. Start a session. Claude runs on the worker laptop, you control from main.

---

## STEP 4: Monitoring & Safety

### Budget Guards
```bash
# Always set spending limits
claude -p "task" --max-budget-usd 10.00 --max-turns 30
```

### Log Rotation
```bash
# Add to crontab on worker
0 0 * * * find /tmp/printmaxx-*.log -mtime +7 -delete
```

### Health Check (run from main laptop)
```bash
ssh user@second-laptop "ps aux | grep claude; df -h; uptime"
```

### Emergency Kill
```bash
ssh user@second-laptop "pkill -f 'claude -p'; tmux kill-server"
```

---

## NODE ROLE SUMMARY

| | Main Laptop (CONTROL) | Second Laptop (WORKER) |
|---|---|---|
| Role | Human approval, sensitive ops | Autonomous execution |
| PRINTMAXX | Read-only reference / not needed | Full copy, primary workspace |
| Claude Mode | Interactive (default permissions) | `--allowedTools` or `--dangerously-skip-permissions` |
| Long runs | No (need laptop for other work) | Yes (dedicated to PRINTMAXX) |
| API keys | Stored, used for manual ops | Stored in .zshrc for automation |
| Blast radius | Personal files, other projects | PRINTMAXX only |
| Before You | Landing page dev, manual testing | Generator server, batch generation |
