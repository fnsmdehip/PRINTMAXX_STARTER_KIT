#!/bin/bash
# Weekly site deploy - runs via launchd (catches up if laptop was sleeping)
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
LOGDIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/logs"
mkdir -p "$LOGDIR"

log() { echo "[$(date '+%Y-%m-%d %H:%M')] $1" >> "$LOGDIR/weekly_deploy.log"; }
log "=== WEEKLY DEPLOY START ==="

# Archive previous builders-ledger before updating
ARCHIVE_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/LANDING/builders-ledger/archive"
mkdir -p "$ARCHIVE_DIR"
WEEK=$(date '+%Y-W%V')
cp /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/LANDING/builders-ledger/index.html "$ARCHIVE_DIR/index_${WEEK}.html" 2>/dev/null
log "Archived builders-ledger to ${WEEK}"

# Deploy all sites
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/LANDING/builders-ledger && npx surge . builders-ledger.surge.sh 2>&1 && log "builders-ledger: OK" || log "builders-ledger: FAILED"

cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/OPEN_SOURCE/agent-soul/site && npx surge . sovrun-agent-os.surge.sh 2>&1 && log "sovrun: OK" || log "sovrun: FAILED"

cd /Users/macbookpro/Documents/devprint/portfolio_site/build && npx surge . devprint-portfolio.surge.sh 2>&1 && log "devprint: OK" || log "devprint: FAILED" 

# Open in browser after deploy
open "https://builders-ledger.surge.sh" 2>/dev/null
open "https://sovrun-agent-os.surge.sh" 2>/dev/null
open "https://devprint-portfolio.surge.sh" 2>/dev/null

log "=== WEEKLY DEPLOY COMPLETE ==="
