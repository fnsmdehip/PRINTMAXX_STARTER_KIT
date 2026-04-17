# PRINTMAXX Mobile Control Playbook
Last updated: 2026-04-17

System: MacBook at 192.168.1.172 | Computer name: HAELO_1.00 | Project: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/

---

## Quick Decision Matrix

| Option | Setup Time | Best Use Case | Reliability | Cost |
|--------|-----------|---------------|-------------|------|
| Tailscale + Web Dashboard | 10 min | Browse full control panel on iPhone | High | Free |
| Tailscale SSH (Termius) | 15 min | Run any command, full shell access | High | Free |
| Telegram Bot | 30 min | One-tap commands, receive alerts proactively | High | Free |
| RustDesk Remote Desktop | 5 min | Visual QA, see what Mac screen looks like | Medium | Free |
| iPhone Shortcuts + SSH | 20 min | Siri shortcuts, iOS home screen widgets | Medium | Free |
| Ntfy Push Notifications | 20 min | Receive alerts from automation (one-way) | High | Free |
| GitHub Actions Mobile Trigger | 45 min | Trigger long jobs when away from Mac | Medium | Free |

**Recommended stack for this weekend (in order):**
1. Fix Tailscale login (10 min) then immediately get web dashboard access
2. Enable SSH Remote Login (2 min in System Settings)
3. Set up Telegram bot (30 min) for proactive alerts + commands
4. Add caffeinate/sleep prevention so Mac stays on

---

## CRITICAL: Keep the Mac On

The laptop went offline for a week. Fix this first.

### Step 1: Prevent Sleep Right Now
```bash
# Prevent sleep indefinitely (kill when done with caffeinate -k $(pgrep caffeinate))
caffeinate -dims &

# Or permanent via launchd:
cat > ~/Library/LaunchAgents/com.printmaxx.nosleep.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.printmaxx.nosleep</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/caffeinate</string>
    <string>-dims</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
</dict>
</plist>
EOF
launchctl load ~/Library/LaunchAgents/com.printmaxx.nosleep.plist
launchctl start com.printmaxx.nosleep
```

### Step 2: Verify Sleep is Prevented
```bash
pmset -g | grep sleep
# Should show: sleep 0 (or "sleep prevented by caffeinate")
```

### Step 3: Power Adapter
Make sure the MacBook stays plugged in. macOS will honor caffeinate on AC power but may override on battery if critically low.

---

## Option 1: Tailscale + Web Dashboard (EASIEST - 10 min)

### What it does
Tailscale creates an encrypted VPN mesh. Your iPhone gets a private IP on the same virtual network as your Mac. You can then open `http://<tailscale-ip>:9999` in Safari on your iPhone and get the full PRINTMAXX control panel.

### Current State
Tailscale 1.94.2 is installed at `/opt/homebrew/bin/tailscale`. It is NOT logged in. The Tailscale daemon socket exists but is not authenticated.

### Setup Steps

**On the Mac:**
```bash
# Step 1: Log in to Tailscale (opens browser)
/opt/homebrew/bin/tailscale login

# Step 2: Verify it connected
/opt/homebrew/bin/tailscale status
# Should show your Mac with a 100.x.x.x IP

# Step 3: Get your Tailscale IP
/opt/homebrew/bin/tailscale ip --4
# Example: 100.101.102.103 - save this number
```

**On the iPhone:**
1. Install Tailscale from the App Store (free)
2. Sign in with the SAME account you used on the Mac
3. Toggle the VPN on
4. Open Safari and go to: `http://100.x.x.x:9999` (using your Mac's Tailscale IP)

### Make sure the control panel is running
```bash
# Check if it's running
pgrep -f control_panel.py && echo "UP" || echo "DOWN"

# Start it (and keep it running)
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
nohup python3 AUTOMATIONS/control_panel.py > AUTOMATIONS/logs/control_panel.log 2>&1 &

# Add to cron so it auto-restarts:
(crontab -l 2>/dev/null; echo "*/5 * * * * pgrep -f control_panel.py || cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && nohup python3 AUTOMATIONS/control_panel.py >> AUTOMATIONS/logs/control_panel.log 2>&1 &") | crontab -
```

### What you get on iPhone
Full web dashboard at `http://100.x.x.x:9999` with:
- Agent status and toggle controls
- Revenue pipeline view
- KPI dashboard
- Run any action button (from `/api/actions`)
- Cron scheduler
- Real-time system metrics
- Venture status
- Pipeline funnel view
- n8n workflow status
- Daily intel feed

### Bookmark it
In Safari, tap Share > Add to Home Screen. You now have a PRINTMAXX app icon on your iPhone.

---

## Option 2: Tailscale SSH via Termius (15 min)

### What it does
Full terminal access to the Mac from your iPhone. Run any Python script, check logs, fix broken crons. Requires SSH Remote Login to be enabled on macOS.

### Step 1: Enable SSH on Mac
```
System Settings > General > Sharing > Remote Login = ON
```
Or via terminal (requires sudo):
```bash
sudo launchctl load -w /System/Library/LaunchDaemons/ssh.plist
```

Verify:
```bash
launchctl list com.openssh.sshd 2>/dev/null && echo "SSH ON" || echo "SSH OFF"
```

### Step 2: Set up SSH key auth (so you don't type a password on phone)
```bash
# On Mac - check your existing public key
cat ~/.ssh/id_rsa.pub
# Copy this output - you'll need it from phone

# The key is already at ~/.ssh/id_rsa.pub (key exists)
# Add it to authorized_keys (allows passwordless login from the same machine)
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### Step 3: iPhone App
**Termius** (recommended) - free tier supports one host
- App Store: search "Termius SSH client"
- Create new host:
  - Hostname: `100.x.x.x` (your Tailscale IP)
  - Username: `macbookpro`
  - Port: `22`
  - Authentication: Password first (use Mac login password), then import key

**a-Shell** (free alternative, no server needed) - actually runs local shell commands via SSH via `ssh` command built in.

### SSH Connection String
```
ssh macbookpro@100.x.x.x
```

On LAN (same wifi), you can also use:
```
ssh macbookpro@192.168.1.172
# or
ssh macbookpro@HAELO-100.local
```

### Key Commands to Run from Mobile Terminal
```bash
# Navigate to project
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

# Quick health check
python3 AUTOMATIONS/system_health_monitor.py --quick

# Decision engine
python3 AUTOMATIONS/decision_engine.py --cycle

# Loop status
python3 AUTOMATIONS/loop_closer.py --status

# Check crons
crontab -l | grep PRINTMAXX | wc -l

# Check control panel
pgrep -f control_panel.py && echo "UP" || echo "DOWN"

# Tail logs
tail -f AUTOMATIONS/logs/$(ls -t AUTOMATIONS/logs/*.log | head -1 | xargs basename)

# Alpha count
wc -l LEDGER/ALPHA_STAGING.csv

# Run morning DAG
python3 AUTOMATIONS/morning_dag.py --run

# Check ventures
python3 AUTOMATIONS/venture_autonomy.py --status
```

---

## Option 3: Telegram Bot (30 min - most powerful for daily use)

### What it does
A Python bot you control by texting commands to a Telegram chat. It runs on your Mac 24/7. From your iPhone, you tap a command like `/status` and get a full system report back within seconds. No VPN needed - Telegram is internet-accessible.

This is the best option for quick daily checks and proactive alerts (the bot can push notifications to you without you asking).

### Bot Creation Steps (5 min)

1. Open Telegram on your iPhone
2. Search for `@BotFather` and start a chat
3. Send: `/newbot`
4. Follow prompts: pick a name (e.g., "PRINTMAXX Control") and username (e.g., `printmaxx_control_bot`)
5. BotFather gives you a token like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
6. Send any message to your new bot (this creates the chat)
7. Get your chat ID:
   ```
   Open in browser: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   Find "chat":{"id":123456789} - that number is your chat_id
   ```

### Add credentials to .env
```bash
echo 'TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz' >> /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/.env
echo 'TELEGRAM_CHAT_ID=123456789' >> /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/.env
```

### Test the connection
```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
python3 AUTOMATIONS/telegram_control_bot.py --test
# Should send a test message to your Telegram
```

### Start the bot
```bash
# Foreground (to test):
python3 AUTOMATIONS/telegram_control_bot.py

# Background (persistent):
nohup python3 AUTOMATIONS/telegram_control_bot.py > AUTOMATIONS/logs/telegram_bot.log 2>&1 &

# Check it's running:
python3 AUTOMATIONS/telegram_control_bot.py --status
```

### Add keepalive to cron
```bash
# Auto-restart if bot crashes
(crontab -l 2>/dev/null; echo "*/5 * * * * pgrep -f telegram_control_bot.py || nohup python3 /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/telegram_control_bot.py >> /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/logs/telegram_bot.log 2>&1 &") | crontab -
```

### Bot Commands Available
```
/start      - Welcome + command list
/status     - Full system overview (crons, health score, alpha count, control panel status)
/health     - Quick 16-point health check
/cron       - List all active cron jobs
/revenue    - Revenue pipeline state
/queue      - Top actionable queue items
/loops      - Loop closer status (OK/DEAD/STALE)
/sites      - Count of live surge.sh deployments
/alpha      - Alpha staging count + last 3 entries
/logs       - Last 20 lines of most recent log
/morning    - Trigger morning DAG manually
/decision   - Run decision engine cycle
/run health        - Quick health check
/run health_full   - Full 16-point check
/run decision      - Decision engine cycle
/run morning       - Morning DAG
/run loops         - Loop closer status
/run scrape_twitter  - Twitter alpha scraper
/run scrape_reddit   - Reddit scraper
/run alpha_process   - Process new alpha
/run capital_rank    - Capital genesis top 5
/run venture_status  - All venture status
/run swarm_status    - Agent swarm status
/help       - Show all commands
```

### Add proactive alerts to existing automations
The `AUTOMATIONS/autonomous_alerts.py` already has a `send_telegram()` function. Wire it into key scripts:

```python
# Add to any automation script after key events:
from autonomous_alerts import send_telegram

send_telegram("Morning DAG completed. 3 new alpha entries.", "success")
send_telegram("ALERT: Loop closer shows DEAD loops!", "critical")
send_telegram("Revenue milestone: first Stripe payment received!", "success")
```

### The bot script
The full bot is at: `AUTOMATIONS/telegram_control_bot.py` (created this session)
It uses only stdlib (urllib, json, subprocess) - no additional pip install needed.

---

## Option 4: RustDesk Full Remote Desktop (5 min - already installed)

### What it does
Full visual remote control of your Mac screen from your iPhone. See exactly what's on screen, click, type, run scripts visually.

### Current State
RustDesk is installed at `/Applications/RustDesk.app`. Not configured (no Screen Recording permission).

### Setup on Mac (2 min)
1. Open RustDesk on Mac (Spotlight > RustDesk)
2. macOS will prompt for Accessibility + Screen Recording permissions
3. Go to: **System Settings > Privacy & Security > Screen Recording** > enable RustDesk
4. Go to: **System Settings > Privacy & Security > Accessibility** > enable RustDesk
5. Note your RustDesk ID (shown in the app, looks like: `123 456 789`)
6. Set a password in RustDesk: Settings > Security > set a permanent password

### iPhone App
1. Install "RustDesk - Remote Desktop" from App Store (free)
2. Enter your Mac's RustDesk ID
3. Enter your password
4. Connect

### When to Use RustDesk vs SSH
- RustDesk: visual QA, seeing simulator output, watching logs scroll, checking browser
- SSH: running scripts, editing files, checking crons, anything text-based (10x faster)

### Note on Relay Servers
RustDesk default uses relay servers for connections outside LAN. For LAN-only (same wifi) it's peer-to-peer. For remote access from anywhere, keep default relay. For privacy, self-host: `hbbs` + `hbbr` on a $6/mo VPS.

---

## Option 5: iPhone Shortcuts + SSH (20 min)

### What it does
Create iOS Home Screen shortcuts that run PRINTMAXX commands in one tap. "Check Status" shortcut opens Termius and runs health check. "Run Morning DAG" shortcut SSHes in and fires the DAG.

### Prerequisites
- Tailscale connected (for remote)
- SSH Remote Login enabled (Option 2 step 1)
- Termius installed on iPhone

### Create a Shortcut: "PRINTMAXX Status"
1. Open Shortcuts app on iPhone
2. New Shortcut > Add Action
3. Search "SSH" - use the built-in SSH action (iOS 15+)
4. Configure:
   - Host: `100.x.x.x` (Tailscale IP)
   - User: `macbookpro`
   - Authentication: Password
   - Command: `cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/system_health_monitor.py --quick 2>&1 | tail -20`
5. Add "Show Result" action after SSH
6. Name it "PRINTMAXX Status"

### Useful Shortcuts to Build

**"Morning DAG"**
```
SSH Command: cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/morning_dag.py --run > AUTOMATIONS/logs/morning_dag_$(date +%Y%m%d).log 2>&1 && echo "Started in background"
```

**"Check System Status"**
```
SSH Command: cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/system_health_monitor.py --quick
```

**"Process Alpha"**
```
SSH Command: cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/alpha_auto_processor.py --process-new 2>&1 | tail -10
```

**"Check Crons"**
```
SSH Command: crontab -l | grep -v "^#" | wc -l && echo "active cron jobs"
```

**"Loop Status"**
```
SSH Command: cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/loop_closer.py --status 2>&1 | tail -15
```

### Add to Home Screen
In Shortcuts: long press shortcut > Add to Home Screen. Creates a tappable icon.

### Ask Siri
"Hey Siri, PRINTMAXX Status" will run the shortcut hands-free.

---

## Option 6: Ntfy Push Notifications (20 min - receive alerts without asking)

### What it does
ntfy.sh is a free push notification service. Your Mac sends HTTP POST requests to a topic URL, and the ntfy iPhone app receives them instantly. Zero infrastructure needed.

### Setup on iPhone
1. Install "ntfy" from App Store (free)
2. Subscribe to a topic: tap + and enter a unique topic name
   Example: `printmaxx-alerts-[random-suffix]` (make it unique to avoid others subscribing)
   Your topic URL: `https://ntfy.sh/printmaxx-alerts-abc123`

### Send notifications from Mac
```bash
# One-liner to send a notification (no libraries needed, just curl)
curl -s -X POST https://ntfy.sh/printmaxx-alerts-abc123 \
  -H "Title: PRINTMAXX Alert" \
  -H "Priority: urgent" \
  -H "Tags: warning" \
  -d "Decision engine completed. 3 new P0 methods found."
```

### Python helper (add to automation scripts)
```python
import urllib.request
import urllib.parse

def ntfy(message: str, title: str = "PRINTMAXX", priority: str = "default"):
    """Send push notification to iPhone via ntfy.sh"""
    topic = "printmaxx-alerts-abc123"  # Your topic here
    url = f"https://ntfy.sh/{topic}"
    headers = {
        "Title": title,
        "Priority": priority,  # min/low/default/high/urgent
        "Tags": "robot"
    }
    data = message.encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception:
        return False
```

### Wire into existing automation (AUTOMATIONS/autonomous_alerts.py already exists)
Add ntfy support alongside Telegram in `autonomous_alerts.py`:
```python
# Add to AUTOMATIONS/autonomous_alerts.py
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "")  # Add NTFY_TOPIC=your-topic to .env

def send_ntfy(message: str, title: str = "PRINTMAXX", priority: str = "default") -> bool:
    if not NTFY_TOPIC:
        return False
    import urllib.request
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    req = urllib.request.Request(
        url,
        data=message.encode(),
        headers={"Title": title, "Priority": priority, "Tags": "robot"},
        method="POST"
    )
    try:
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception:
        return False
```

### Key Events to Alert On
Wire notifications into these scripts:
```bash
# After morning_dag.py completes
# After decision_engine.py --cycle
# When loop_closer detects DEAD loops
# When alpha count crosses milestones
# When cron jobs get wiped (cron_watchdog.py already checks this)
# When control panel goes down
```

### Add .env variable
```bash
echo 'NTFY_TOPIC=printmaxx-alerts-abc123' >> /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/.env
```

---

## Option 7: Control Panel via Tailscale (5 min once Tailscale works)

### What it does
Once Tailscale is connected (Option 1), you get the full web dashboard on iPhone without any additional setup.

### Access
```
http://100.x.x.x:9999
```

### Available Dashboard Endpoints
These are the live API endpoints in `AUTOMATIONS/control_panel.py`:

| Endpoint | What it shows |
|----------|---------------|
| `/` | Main dashboard (full UI) |
| `/api/status` | System health summary |
| `/api/agents` | All agent statuses |
| `/api/ventures` | Venture status |
| `/api/pipeline` | Pipeline funnel |
| `/api/kpi` | KPI dashboard |
| `/api/daily-feed` | Today's intelligence feed |
| `/api/intel-feed` | Alpha/intel entries |
| `/api/sites` | Deployed site list |
| `/api/blockers` | Human blockers surfaced |
| `/api/scheduler/crons` | All cron jobs |
| `/api/realtime` | Live metrics |
| `/api/daily-output` | Today's output |
| `/api/commands/all` | Available commands |
| `/api/commands/run` (POST) | Run a command |
| `/api/sovrun/skills` | Skill/memory DB |
| `/api/n8n/workflows` | n8n workflow status |

### Quick API calls from iPhone browser
Navigate to these in Safari for quick text-only views:
- `http://100.x.x.x:9999/api/status` - JSON status
- `http://100.x.x.x:9999/api/blockers` - What needs human action

---

## Option 8: GitHub Actions Triggered from Phone (advanced)

### What it does
Trigger long-running automation jobs by dispatching a GitHub Actions workflow from the GitHub mobile app or a webhook URL. Useful when you're not at your Mac and want to queue a heavy task.

### Use Case
"I want to kick off the full alpha pipeline while I'm out" - tap a button in GitHub mobile, the action queues, Mac picks it up via polling.

### Setup
This requires your PRINTMAXX repo to be on GitHub (private is fine).

**1. Create workflow file** (`.github/workflows/mobile-trigger.yml`):
```yaml
name: Mobile Trigger
on:
  workflow_dispatch:
    inputs:
      command:
        description: 'Command to run'
        required: true
        default: 'status'
        type: choice
        options:
        - status
        - morning_dag
        - decision_cycle
        - process_alpha

jobs:
  run:
    runs-on: self-hosted  # Requires GitHub Actions self-hosted runner on Mac
    steps:
      - name: Run command
        run: |
          cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
          python3 AUTOMATIONS/system_health_monitor.py --quick
```

**2. On iPhone**: GitHub mobile app > Actions tab > Run workflow

### Alternative: Simpler polling approach
Create a cron job that polls a GitHub issue or Gist for commands:
```bash
# Mac polls a GitHub Gist every 5 min for a command file
# iPhone edits the Gist to queue a command
# No self-hosted runner needed
```

This is the most complex option and only worth it for jobs that take >10 min to run.

---

## Recommended Setup Order (This Weekend)

### Priority 1 - Right Now (20 min total)
1. **Prevent sleep**: Run `caffeinate -dims &` + add the launchd plist above
2. **Log in to Tailscale**: `/opt/homebrew/bin/tailscale login` then install iPhone app
3. **Start control panel**: `nohup python3 AUTOMATIONS/control_panel.py > AUTOMATIONS/logs/control_panel.log 2>&1 &`
4. **Open iPhone Safari**: `http://<tailscale-ip>:9999` - you now have full dashboard

### Priority 2 - Today (30 min total)
5. **Enable SSH Remote Login**: System Settings > General > Sharing > Remote Login = ON
6. **Install Termius on iPhone**: Set up SSH connection via Tailscale IP
7. **Set up Telegram bot**: Create via BotFather, add token to .env, start bot

### Priority 3 - This Week (1 hr total)
8. **Grant RustDesk Screen Recording permission**: For visual remote access
9. **Create 3 iPhone Shortcuts**: Status, Morning DAG, Loop Check
10. **Wire ntfy into autonomous_alerts.py**: For proactive push notifications
11. **Add all keepalive crons**: Control panel, Telegram bot, caffeinate watchdog

---

## Quick Reference - Common Mobile Commands

### Via Telegram (type to your bot):
```
/status         - Full system overview
/health         - Health score + key metrics
/loops          - Are loops OK or DEAD?
/queue          - What should run next?
/morning        - Trigger morning DAG
/run decision   - Decision engine cycle
/cron           - How many crons running?
/alpha          - Alpha entry count
```

### Via SSH (from Termius):
```bash
# Always start here:
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

# Health
python3 AUTOMATIONS/system_health_monitor.py --quick

# Decision engine
python3 AUTOMATIONS/decision_engine.py --cycle

# Loops
python3 AUTOMATIONS/loop_closer.py --status

# Cron count
crontab -l | grep -v "^#" | grep -v "^$" | wc -l

# Control panel up?
pgrep -f control_panel.py && echo "UP" || echo "DOWN"

# Telegram bot up?
pgrep -f telegram_control_bot.py && echo "UP" || echo "DOWN"

# Today's activity
ls -lt AUTOMATIONS/logs/ | head -10

# Alpha since yesterday
python3 AUTOMATIONS/alpha_auto_processor.py --process-new

# Ventures
python3 AUTOMATIONS/venture_autonomy.py --status

# Capital genesis top 5
python3 AUTOMATIONS/capital_genesis_ranker.py --rank --top 5

# Tail any log
tail -f AUTOMATIONS/logs/control_panel.log
tail -f AUTOMATIONS/logs/telegram_bot.log
tail -f AUTOMATIONS/logs/decision_engine.log
```

### Via Control Panel (Safari at Tailscale IP:9999):
- Open dashboard > click agent toggles
- Actions panel > run any quick action
- KPI calendar > advance day, mark tasks complete
- Cron scheduler > enable/disable cron jobs
- Ventures > check status of all 8 venture types

---

## Keeping the Mac Always-On

### Software (do all three)
```bash
# 1. Immediate caffeinate
caffeinate -dims &

# 2. launchd plist (survives reboots) - see CRITICAL section above

# 3. Disable display sleep separately (doesn't affect system sleep):
sudo pmset -a displaysleep 0

# 4. Disable disk sleep:
sudo pmset -a disksleep 0

# 5. Check current power state:
pmset -g | grep sleep
```

### macOS Energy Settings
System Settings > Battery (or Energy Saver):
- "Prevent computer from sleeping automatically when the display is off" = ON
- "Wake for network access" = ON
- "Start up automatically after a power failure" = ON

### Hardware
If the Mac might lose power, a UPS (uninterruptible power supply) is the only solution for extended outages. A $60-80 APC Back-UPS 600VA gives ~15 min of runtime to cleanly shut down.

### Network
If on wifi: consider ethernet cable for reliability. Also pin a static local IP via DHCP reservation in your router settings:
- Go to router admin (usually 192.168.1.1)
- Find DHCP > Static leases or Address reservation
- Add MAC address of your MacBook -> reserve 192.168.1.172

---

## ADVANCED: Creative Mobile Control (Added Apr 17)

### Option 9: Scriptable Home Screen Widget (20 min - live stats on lock screen)

**What it does:** A JavaScript widget on your iPhone Home Screen that fetches live data from the control panel API every 15 minutes. Shows revenue, health %, alpha count, and loop status at a glance without opening any app.

**Setup:**
1. Install "Scriptable" from App Store (free)
2. Create new script with this code:

```javascript
// PRINTMAXX Status Widget
const TAILSCALE_IP = "100.x.x.x" // Replace with your Tailscale IP
const BASE = `http://${TAILSCALE_IP}:9999`

let widget = new ListWidget()
widget.backgroundColor = new Color("#0a0a0a")

try {
  let req = new Request(`${BASE}/api/status`)
  req.timeoutInterval = 5
  let data = await req.loadJSON()
  
  let title = widget.addText("PRINTMAXX")
  title.font = Font.boldSystemFont(12)
  title.textColor = new Color("#ffd700")
  
  widget.addSpacer(4)
  
  let rev = widget.addText(`$${data.revenue || 0} revenue`)
  rev.font = Font.systemFont(14)
  rev.textColor = data.revenue > 0 ? Color.green() : Color.red()
  
  let alpha = widget.addText(`${data.alpha_total || "?"} alpha entries`)
  alpha.font = Font.systemFont(11)
  alpha.textColor = Color.white()
  
  let crons = widget.addText(`${data.cron_jobs || "?"} cron jobs active`)
  crons.font = Font.systemFont(11)
  crons.textColor = Color.gray()
  
} catch(e) {
  let err = widget.addText("Mac offline")
  err.font = Font.boldSystemFont(14)
  err.textColor = Color.red()
}

Script.setWidget(widget)
widget.presentSmall()
```

3. Long-press Home Screen > tap + > Scriptable > select your script
4. Widget refreshes every 15 minutes showing live stats

### Option 10: NFC Command Tags ($5 total - tap to trigger)

**What it does:** Physical NFC stickers that trigger iOS Shortcuts when you tap your phone on them. Tap the desk tag = run full pipeline. Tap the nightstand tag = morning briefing.

**Setup:**
1. Buy NFC tags ($5 for 10 on Amazon - search "NFC stickers NTAG215")
2. Open Shortcuts app > Automation > Create Personal Automation
3. Choose "NFC" trigger > Scan tag > name it (e.g., "DESK-PIPELINE")
4. Add actions:
   - "Run SSH Command" over Tailscale
   - OR "Open URL" to `http://100.x.x.x:9999/api/commands/run` with POST body
5. Stick the NFC tag wherever you want

**Suggested tag layout:**
| Location | Tag Name | Action |
|----------|----------|--------|
| Desk | PIPELINE | Full morning DAG + decision engine + show status |
| Nightstand | BRIEFING | Read SESSION_BRIEFING.md aloud via Siri TTS |
| Kitchen | HEALTH | Quick health check + read loop status aloud |
| Wallet | REVENUE | Check Stripe balance + show pipeline value |

### Option 11: PWA Dashboard (10 min - app-like experience)

**What it does:** Makes the Flask dashboard behave like a native app on iPhone. Full screen, no Safari chrome, offline caching, push notifications via service worker.

**To enable:** Add a manifest and service worker to the control panel HTML:

Add to `AUTOMATIONS/control_panel.html` `<head>`:
```html
<link rel="manifest" href="/manifest.json">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="PRINTMAXX">
<link rel="apple-touch-icon" href="/api/icon">
```

Add a `/manifest.json` route to control_panel.py:
```python
@app.route("/manifest.json")
def manifest():
    return jsonify({
        "name": "PRINTMAXX Control",
        "short_name": "PRTMX",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0a0a0a",
        "theme_color": "#ffd700"
    })
```

Then on iPhone Safari: Share > Add to Home Screen. Opens full-screen like a native app.

### Option 12: Pushover + Apple Watch via Watchsmith (15-25 min - wrist status)

**Watchsmith ($3.99 iOS app)** supports "Web" complications that fetch JSON from a URL. Point it at `http://control-node.tailnet:9999/api/watch` over Tailscale and it displays extracted values as gauge/text complications. No coding needed. Update every 15-60 min.

A `/api/watch` endpoint has been added to control_panel.py (this session) returning exactly 4 glanceable values: revenue, alpha count, loop health, agents active.

### Option 12b: Pushover for Emergency Escalation ($5 one-time)

**What it does:** Pushover ($5 one-time purchase) delivers push notifications with custom sounds, priority levels, and an Apple Watch complication showing the last alert.

**Why Pushover over Telegram for notifications:**
- Apple Watch complication (shows last alert on watch face)
- Custom notification sounds per priority level
- Quiet Hours with emergency override for critical alerts
- Delivery receipts (know if the notification was actually seen)
- 10,000 messages/month on free tier after $5 app purchase

**Setup:**
1. Buy Pushover app ($5, one-time) on iPhone
2. Create account at pushover.net, get User Key
3. Create Application, get API Token
4. Add to .env: `PUSHOVER_USER_KEY=xxx` and `PUSHOVER_API_TOKEN=xxx`

**Python (add to autonomous_alerts.py):**
```python
def send_pushover(message, title="PRINTMAXX", priority=0):
    import urllib.request, urllib.parse
    data = urllib.parse.urlencode({
        "token": os.environ.get("PUSHOVER_API_TOKEN", ""),
        "user": os.environ.get("PUSHOVER_USER_KEY", ""),
        "message": message,
        "title": title,
        "priority": priority,  # -2=silent, -1=quiet, 0=normal, 1=high, 2=emergency
    }).encode()
    urllib.request.urlopen("https://api.pushover.net/1/messages.json", data, timeout=5)
```

**Apple Watch:** Once Pushover is installed and sending notifications, the Watch complication auto-shows the latest alert. Glance at your wrist to see "Pipeline complete: 54 alpha approved" without touching your phone.

### Option 13: Voice Control ("Hey Siri, run the pipeline")

**What it does:** Chain Siri Shortcuts so you can voice-command the system.

**Setup:**
1. Create Shortcuts as in Option 5 (SSH-based)
2. Name them with voice-friendly names:
   - "Run the Pipeline" -> morning DAG + decision engine
   - "Check PRINTMAXX" -> system health + loop status
   - "Morning Brief" -> read SESSION_BRIEFING.md via TTS
   - "How's Revenue" -> check Stripe balance + speak result

**The voice chain:**
"Hey Siri, run the pipeline" ->
Shortcut "Run the Pipeline" ->
SSH to Mac via Tailscale ->
`python3 morning_intelligence_dag.py && python3 decision_engine.py --cycle` ->
Parse output ->
Speak "Pipeline complete. 54 alpha approved. 17 freelance leads found."

### Option 14: Cloudflare Tunnel (Alternative to Tailscale)

**What it does:** Exposes the Flask dashboard at a public URL (e.g., `printmaxx.yourdomain.com`) without VPN. Cloudflare handles TLS, DDoS protection, and access control.

**Pros over Tailscale:** No VPN app needed on iPhone. Works in any browser. Can share with others (with Cloudflare Access auth).
**Cons:** Requires a domain on Cloudflare. Public URL (secured by Cloudflare Access, but still exposed).

**Setup (10 min if you have a Cloudflare domain):**
```bash
brew install cloudflared
cloudflared tunnel login
cloudflared tunnel create printmaxx
cloudflared tunnel route dns printmaxx control.yourdomain.com
cloudflared tunnel run --url http://localhost:9999 printmaxx
```

**Add Cloudflare Access (zero-trust auth):**
Cloudflare dashboard > Access > Applications > Add > Self-hosted
- URL: control.yourdomain.com
- Policy: Allow email = your@email.com (sends a one-time code)
- Now the dashboard requires email auth before showing

---

## THE POWER STACK (recommended combination)

For a solo operator running a 24/7 autonomous system, here's the optimal combo:

| Layer | Tool | Purpose | Cost |
|-------|------|---------|------|
| Network | Tailscale | Encrypted mesh VPN | Free |
| Dashboard | Flask PWA via Tailscale | Full control panel on Home Screen | Free |
| Commands | Telegram bot | Type commands, get responses | Free |
| Alerts | Pushover | Priority notifications + Apple Watch | $5 one-time |
| Widgets | Scriptable | Live stats on Home Screen | Free |
| Quick triggers | NFC tags | Tap to run pipelines | $5 one-time |
| Voice | Siri Shortcuts | Hands-free commands | Free |
| Backup access | RustDesk | Full remote desktop when needed | Free |

**Total cost: $10 one-time.**
**Setup time: ~2 hours (do it once, works forever).**

This gives you:
- Glance at Home Screen widget = see system health
- Glance at Apple Watch = see last alert
- "Hey Siri, check PRINTMAXX" = voice status
- Tap NFC on desk = run full pipeline
- Open Telegram = full command interface
- Open Safari bookmark = full dashboard
- Any alert = instant Pushover notification with priority levels
- Need full desktop? = RustDesk in 5 seconds

---

## Files Created This Session

- `AUTOMATIONS/telegram_control_bot.py` - Full Telegram control bot (540 lines, no pip install needed)

## Existing Infrastructure Found

- `AUTOMATIONS/autonomous_alerts.py` - Telegram send_telegram() function already exists
- `AUTOMATIONS/telegram_community_monitor.py` - Telegram channel monitoring (separate from control)
- `AUTOMATIONS/remote_access_status.py` - Remote access inspector script
- `AUTOMATIONS/coderelay_tailscale_sync.py` - Tailscale/CodeRelay integration
- Control panel: 40+ API endpoints at localhost:9999
- Tailscale 1.94.2 installed but NOT logged in
- RustDesk installed at /Applications/RustDesk.app but no Screen Recording permission
- SSH keys exist at ~/.ssh/id_rsa but Remote Login is disabled
- Mac IP: 192.168.1.172 (local), hostname: HAELO-100.local

## What's Blocking You Right Now

1. **Tailscale not logged in** - run `tailscale login` to fix (2 min)
2. **SSH Remote Login disabled** - System Settings > Sharing > enable (30 sec)
3. **RustDesk no Screen Recording** - System Settings > Privacy > Screen Recording (30 sec)
4. **caffeinate not running** - Mac will sleep without it
5. **Telegram bot not configured** - need TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID in .env
