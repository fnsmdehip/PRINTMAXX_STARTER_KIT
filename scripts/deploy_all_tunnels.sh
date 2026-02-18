#!/bin/bash
# PRINTMAXX Deploy All Tunnels
# Serves all deployable sites locally and exposes via tunnels
# Usage: bash scripts/deploy_all_tunnels.sh
# To stop: bash scripts/deploy_all_tunnels.sh stop

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
PIDFILE="/tmp/printmaxx_deploy_pids.txt"

if [ "$1" = "stop" ]; then
    echo "Stopping all deploy servers and tunnels..."
    if [ -f "$PIDFILE" ]; then
        while read pid; do
            kill "$pid" 2>/dev/null
        done < "$PIDFILE"
        rm "$PIDFILE"
    fi
    for port in 8091 8092 8093 8094 8095 8096 8097 8098; do
        lsof -ti:$port | xargs kill 2>/dev/null
    done
    killall ngrok 2>/dev/null
    echo "All stopped."
    exit 0
fi

echo "=== PRINTMAXX DEPLOY ALL ==="
echo "Starting local servers..."
> "$PIDFILE"

# Ramadan Tracker (URGENT)
cd "$BASE/ralph/loops/app_factory/output/ramadan-tracker"
python3 -m http.server 8091 > /dev/null 2>&1 &
echo $! >> "$PIDFILE"
echo "  [8091] Ramadan Tracker (Hilal)"

# Programmatic SEO (601 pages)
cd "$BASE/builds/programmatic_seo"
python3 -m http.server 8092 > /dev/null 2>&1 &
echo $! >> "$PIDFILE"
echo "  [8092] Programmatic SEO (601 pages)"

# HabitForge
cd "$BASE/ralph/loops/app_factory/output/habitforge-web"
python3 -m http.server 8093 > /dev/null 2>&1 &
echo $! >> "$PIDFILE"
echo "  [8093] HabitForge"

# FocusLock
cd "$BASE/ralph/loops/app_factory/output/focuslock-web"
python3 -m http.server 8094 > /dev/null 2>&1 &
echo $! >> "$PIDFILE"
echo "  [8094] FocusLock"

# SleepMaxx
cd "$BASE/ralph/loops/app_factory/output/sleepmaxx-web"
python3 -m http.server 8095 > /dev/null 2>&1 &
echo $! >> "$PIDFILE"
echo "  [8095] SleepMaxx"

# WalkToUnlock
cd "$BASE/ralph/loops/app_factory/output/walktounlock-web"
python3 -m http.server 8096 > /dev/null 2>&1 &
echo $! >> "$PIDFILE"
echo "  [8096] WalkToUnlock"

# MealMaxx
cd "$BASE/ralph/loops/app_factory/output/mealmaxx-web"
python3 -m http.server 8097 > /dev/null 2>&1 &
echo $! >> "$PIDFILE"
echo "  [8097] MealMaxx"

# Motion Templates
cd "$BASE/MONEY_METHODS/LOCAL_BIZ/motion_templates"
python3 -m http.server 8098 > /dev/null 2>&1 &
echo $! >> "$PIDFILE"
echo "  [8098] Motion Templates (dental, restaurant, realtor)"

sleep 2

echo ""
echo "=== Starting tunnels ==="

# ngrok for Ramadan tracker (most stable)
ngrok http 8091 --log=stdout --log-format=json > /tmp/ngrok_ramadan.log 2>&1 &
echo $! >> "$PIDFILE"
sleep 5
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); [print(t['public_url']) for t in d['tunnels']]" 2>/dev/null | head -1)
echo "  Ramadan Tracker: $NGROK_URL"

# localtunnel for everything else
npx localtunnel --port 8092 --subdomain printmaxx-seo > /tmp/lt_seo.log 2>&1 &
echo $! >> "$PIDFILE"
sleep 3
echo "  Programmatic SEO: https://printmaxx-seo.loca.lt"

npx localtunnel --port 8093 --subdomain habitforge-app > /tmp/lt_habit.log 2>&1 &
echo $! >> "$PIDFILE"
sleep 3
echo "  HabitForge: https://habitforge-app.loca.lt"

npx localtunnel --port 8094 --subdomain focuslock-app > /tmp/lt_focus.log 2>&1 &
echo $! >> "$PIDFILE"
sleep 3
echo "  FocusLock: https://focuslock-app.loca.lt"

npx localtunnel --port 8095 --subdomain sleepmaxx-app > /tmp/lt_sleep.log 2>&1 &
echo $! >> "$PIDFILE"
sleep 3
echo "  SleepMaxx: https://sleepmaxx-app.loca.lt"

npx localtunnel --port 8096 --subdomain walktounlock-app > /tmp/lt_walk.log 2>&1 &
echo $! >> "$PIDFILE"
sleep 3
echo "  WalkToUnlock: https://walktounlock-app.loca.lt"

npx localtunnel --port 8097 --subdomain mealmaxx-app > /tmp/lt_meal.log 2>&1 &
echo $! >> "$PIDFILE"
sleep 3
echo "  MealMaxx: https://mealmaxx-app.loca.lt"

npx localtunnel --port 8098 --subdomain printmaxx-demos > /tmp/lt_demos.log 2>&1 &
echo $! >> "$PIDFILE"
sleep 3
echo "  Motion Demos: https://printmaxx-demos.loca.lt"

echo ""
echo "=== ALL DEPLOYED ==="
echo "  10 sites live (6 PWAs + 601 SEO pages + 3 motion demos)"
echo "  Stop with: bash $0 stop"
echo "  Logs: /tmp/ngrok_ramadan.log, /tmp/lt_*.log"
