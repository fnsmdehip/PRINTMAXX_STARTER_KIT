#!/bin/bash
# Deploy all SEO-updated landing pages from the 2026-05-05 SEO audit cycle.
# Run after: surge login (re-authenticate with fnsmdehip@proton.me)

set -euo pipefail
BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
cd "$BASE"

log() { echo "[$(date '+%H:%M:%S')] $1"; }

# ── Priority 1: Sites with new og.png files ──────────────────────────────────
log "Deploying sites with new og.png..."
surge LANDING/cnsnt cnsnt.surge.sh && log "OK: cnsnt.surge.sh"
surge LANDING/cnsnt-downloads cnsnt-downloads.surge.sh && log "OK: cnsnt-downloads.surge.sh"
surge LANDING/research-blog fnsmdehip-research.surge.sh && log "OK: fnsmdehip-research.surge.sh"
surge LANDING/builders-ledger builders-ledger.surge.sh && log "OK: builders-ledger.surge.sh"
surge LANDING/truthscope truthscope.surge.sh && log "OK: truthscope.surge.sh"
surge LANDING/androx androx-trt.surge.sh && log "OK: androx-trt.surge.sh"

# ── Priority 2: Affiliate pages (OG image + JSON-LD fixes) ──────────────────
log "Deploying affiliate pages..."
deploy_affiliate() {
    local dir="$1"
    local domain="${2:-}"
    if [ -z "$domain" ]; then
        domain="$(basename "$dir").surge.sh"
    fi
    if surge "$dir" "$domain" 2>&1 | grep -q "Success"; then
        log "OK: $domain"
    else
        log "WARN: $domain"
    fi
}

for dir in LANDING/affiliate-pages/*/; do
    deploy_affiliate "$dir"
done

for dir in LANDING/affiliate-pages/seo-articles/*/; do
    deploy_affiliate "$dir"
done

log "All SEO-updated sites deployed."
