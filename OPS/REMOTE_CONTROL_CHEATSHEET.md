# PRINTMAXX Remote Control Cheat Sheet

Quick reference for controlling the worker laptop from your main machine.

## Prerequisites
- SSH enabled on worker: System Settings > General > Sharing > Remote Login
- Worker hostname/IP saved: `export WORKER=user@192.168.x.x` in your main laptop .zshrc

---

## Common Commands (run from main laptop)

### Start an Autonomous Agent Run
```bash
ssh $WORKER "tmux new-session -d -s agent && tmux send-keys -t agent 'cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt && claude -p \"\$(cat OPS/AUTONOMOUS_DAILY_PROMPT.md)\" --allowedTools Bash,Read,Edit,Write,Glob,Grep --max-turns 30 --max-budget-usd 10.00 2>&1 | tee /tmp/printmaxx-run-\$(date +%Y%m%d-%H%M).log' Enter"
```

### Check What the Agent Is Doing
```bash
ssh $WORKER "tmux capture-pane -t agent -p | tail -30"
```

### Get a Status Report
```bash
ssh $WORKER "cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt && claude -p 'Read output/worker_session_log.md and OPS/KPI_DASHBOARD.md. Give me a 5-line status: revenue, what ran, errors, top priority, blockers.' --allowedTools Read,Glob,Grep --max-turns 5 --output-format json"
```

### Run a Specific Venture Task
```bash
# Before You: test generation
ssh $WORKER "cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/BEFORE_YOU/before-you/generator && node index.js --intake test-intake.json"

# Capital Genesis ranker
ssh $WORKER "cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/capital_genesis_ranker.py"

# Venture map executor
ssh $WORKER "cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/venture_map_executor.py --apply"
```

### Kill a Runaway Agent
```bash
ssh $WORKER "pkill -f 'claude -p'; echo 'killed'"
```

### Kill Everything
```bash
ssh $WORKER "tmux kill-server; pkill -f claude; pkill -f node; echo 'all killed'"
```

### Read the Latest Session Log
```bash
ssh $WORKER "cat ~/Documents/p/PRINTMAXX_STARTER_KITttttt/output/worker_session_log.md"
```

### Read Latest Run Log
```bash
ssh $WORKER "ls -t /tmp/printmaxx-run-*.log | head -1 | xargs tail -50"
```

### Check Worker Health
```bash
ssh $WORKER "echo '--- UPTIME ---'; uptime; echo '--- DISK ---'; df -h /; echo '--- MEMORY ---'; vm_stat | head -5; echo '--- CLAUDE PROCS ---'; ps aux | grep claude | grep -v grep; echo '--- TMUX ---'; tmux ls 2>/dev/null || echo 'no tmux sessions'"
```

---

## Claude Desktop SSH (Interactive Control)

For interactive sessions where you want to see diffs and approve changes:

1. Open Claude Desktop on main laptop
2. Environment dropdown > Add SSH connection
3. Enter: `user@worker-ip`, port 22, SSH key path
4. Select `~/Documents/p/PRINTMAXX_STARTER_KITttttt`
5. Start session. You get full Claude Code UI but execution happens on worker.

---

## Dispatch Patterns

### Pattern 1: Fire and Forget
Start a long run, check results later.
```bash
ssh $WORKER "nohup bash -c 'cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt && claude -p \"Execute Capital Genesis top 5 priorities\" --allowedTools Bash,Read,Edit,Write,Glob,Grep --max-turns 30 --output-format json > /tmp/printmaxx-dispatch-\$(date +%s).log 2>&1' &"
```

### Pattern 2: Supervised Autonomous
Start a tmux run, check in periodically.
```bash
# Start
ssh $WORKER "tmux new-session -d -s supervised && tmux send-keys -t supervised 'cd ~/Documents/p/PRINTMAXX_STARTER_KITttttt && claude --allowedTools Bash,Read,Edit,Write,Glob,Grep' Enter"

# Send instructions
ssh $WORKER "tmux send-keys -t supervised 'Run the daily tactical engine and execute top 3 tasks' Enter"

# Check progress
ssh $WORKER "tmux capture-pane -t supervised -p | tail -20"
```

### Pattern 3: Cron Autonomous
Set it and forget it. Worker runs on schedule.
```bash
# Already configured via launchd in SECOND_LAPTOP_MIGRATION.md
# Check if it's running:
ssh $WORKER "launchctl list | grep printmaxx"
```

---

## Sync Changes Back to Main Laptop

If the worker produces artifacts you want on the main laptop:

```bash
# Pull specific outputs
scp $WORKER:~/Documents/p/PRINTMAXX_STARTER_KITttttt/output/worker_session_log.md /tmp/

# Pull all outputs
rsync -avz $WORKER:~/Documents/p/PRINTMAXX_STARTER_KITttttt/output/ /tmp/printmaxx-output/

# Pull updated OPS docs
rsync -avz $WORKER:~/Documents/p/PRINTMAXX_STARTER_KITttttt/OPS/ /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/OPS/
```
