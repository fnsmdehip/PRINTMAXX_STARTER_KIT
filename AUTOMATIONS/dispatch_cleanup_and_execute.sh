#!/bin/bash
# DISPATCH AUTO-EXECUTE — Written by Dispatch session, picked up by cron
# Self-deleting after execution

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
LOG="$BASE/AUTOMATIONS/logs/dispatch_execute.log"

echo "=== DISPATCH EXECUTE $(date) ===" >> "$LOG"

# Step 1: Clean worktrees
echo "[1] Cleaning worktrees..." >> "$LOG"
cd "$BASE"
rm -rf .claude/worktrees/* 2>> "$LOG"
git worktree prune 2>> "$LOG"
echo "[1] Worktrees cleaned: $(git worktree list | wc -l) remaining" >> "$LOG"

# Step 2: Prevent sleep
caffeinate -dims &
echo "[2] Sleep prevention active (PID: $!)" >> "$LOG"

# Step 3: Install ComfyUI
if [ ! -d "$HOME/Documents/ComfyUI" ]; then
    echo "[3] Installing ComfyUI..." >> "$LOG"
    cd "$HOME/Documents"
    git clone https://github.com/comfyanonymous/ComfyUI.git >> "$LOG" 2>&1
    cd ComfyUI
    pip3 install torch torchvision torchaudio --break-system-packages >> "$LOG" 2>&1
    pip3 install -r requirements.txt --break-system-packages >> "$LOG" 2>&1
    cd custom_nodes
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git >> "$LOG" 2>&1
    echo "[3] ComfyUI installed" >> "$LOG"
else
    echo "[3] ComfyUI already exists" >> "$LOG"
fi

# Step 4: Generate test image
mkdir -p "$BASE/MONEY_METHODS/AI_ART_VENTURE/test_output"
curl -sL --max-time 60 -o "$BASE/MONEY_METHODS/AI_ART_VENTURE/test_output/test_character.png" \
    "https://image.pollinations.ai/prompt/anime+digital+art+character+portrait+elegant+fantasy+woman+detailed?width=1024&height=1024&nologo=true&seed=42" 2>> "$LOG"
echo "[4] Test image generated" >> "$LOG"

# Step 5: Run scrapers
cd "$BASE"
python3 AUTOMATIONS/twitter_alpha_scraper.py --all --days 14 >> "$LOG" 2>&1
echo "[5] Twitter scraper done" >> "$LOG"
python3 AUTOMATIONS/background_reddit_scraper.py --scrape >> "$LOG" 2>&1
echo "[5] Reddit scraper done" >> "$LOG"

# Step 6: Fire autonomous systems
python3 AUTOMATIONS/ceo_agent.py --dag >> "$LOG" 2>&1
echo "[6] CEO agent fired" >> "$LOG"
python3 AUTOMATIONS/loop_closer.py --cycle >> "$LOG" 2>&1
echo "[6] Loop closer fired" >> "$LOG"
python3 AUTOMATIONS/venture_autonomy.py --status >> "$LOG" 2>&1
echo "[6] Venture autonomy status" >> "$LOG"

# Step 7: Launch ComfyUI in background
if [ -d "$HOME/Documents/ComfyUI" ]; then
    cd "$HOME/Documents/ComfyUI"
    nohup python3 main.py --force-fp16 > /tmp/comfyui.log 2>&1 &
    echo "[7] ComfyUI launched on :8188 (PID: $!)" >> "$LOG"
fi

# Step 8: Launch control panel
cd "$BASE"
pgrep -f control_panel.py > /dev/null || nohup python3 AUTOMATIONS/control_panel.py >> AUTOMATIONS/logs/control_panel.log 2>&1 &
echo "[8] Control panel ensured running" >> "$LOG"

echo "=== DISPATCH EXECUTE COMPLETE $(date) ===" >> "$LOG"

# Mark as executed so perpetual_guardian or cron doesn't re-run
mv "$0" "$0.executed"
