#!/bin/bash
# SEO Platform Migration: Surge.sh -> Cloudflare Pages
# Surge.sh free tier blocks ALL search engines at CDN level (Disallow: /)
# This script prepares and deploys top SEO-value pages to Cloudflare Pages
#
# Prerequisites:
#   npm install -g wrangler
#   wrangler login
#
# Usage:
#   bash AUTOMATIONS/seo_platform_migration.sh --prepare   # Prepare all pages
#   bash AUTOMATIONS/seo_platform_migration.sh --deploy     # Deploy to Cloudflare Pages
#   bash AUTOMATIONS/seo_platform_migration.sh --status     # Check deployment status

set -e
BASE_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
STAGING_DIR="$BASE_DIR/AUTOMATIONS/.seo_migration_staging"

# Top 6 pages by keyword search volume (total: 65.5K/mo)
# These represent the highest organic traffic potential
declare_pages() {
    # Format: source_path|deploy_name|keyword|monthly_volume
    PAGES=(
        "DIGITAL_PRODUCTS/lead_magnets/ai-slop-detector.html|ai-slop-detector|ai content detector free|22000"
        "DIGITAL_PRODUCTS/lead_magnets/vibe-coding-cheat-sheet.html|vibe-coding-cheat-sheet|vibe coding|12000"
        "LANDING/app-marketing-pages/cursor-vs-claude-code/|cursor-vs-claude-code|cursor vs claude code|9100"
        "DIGITAL_PRODUCTS/lead_magnets/freelance-rate-calculator.html|freelance-rate-calc|freelance rate calculator|8100"
        "LANDING/affiliate-pages/semrush-vs-ahrefs/|semrush-vs-ahrefs|semrush vs ahrefs 2026|6500"
        "DIGITAL_PRODUCTS/lead_magnets/subject-line-grader.html|subject-line-grader|cold email subject line|5400"
    )
}

ROBOTS_CONTENT='User-agent: *
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Applebot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: cohere-ai
Allow: /'

prepare_page() {
    local source="$1"
    local name="$2"
    local dest="$STAGING_DIR/$name"

    mkdir -p "$dest"

    if [ -d "$BASE_DIR/$source" ]; then
        cp -r "$BASE_DIR/$source"* "$dest/" 2>/dev/null || true
    else
        cp "$BASE_DIR/$source" "$dest/index.html"
        # Copy sibling assets
        local srcdir
        srcdir=$(dirname "$BASE_DIR/$source")
        for asset in manifest.json sw.js service-worker.js lead-capture-universal.js; do
            if [ -f "$srcdir/$asset" ]; then
                cp "$srcdir/$asset" "$dest/"
            fi
        done
    fi

    # Add robots.txt
    echo "$ROBOTS_CONTENT" > "$dest/robots.txt"

    # Add sitemap
    if [ ! -f "$dest/sitemap.xml" ]; then
        cat > "$dest/sitemap.xml" << SITEMAP
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://$name.pages.dev/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
    <lastmod>$(date +%Y-%m-%d)</lastmod>
  </url>
</urlset>
SITEMAP
    fi

    echo "Prepared: $name ($(ls "$dest" | wc -l | tr -d ' ') files)"
}

case "${1:-}" in
    --prepare)
        echo "=== Preparing SEO Migration Staging ==="
        rm -rf "$STAGING_DIR"
        mkdir -p "$STAGING_DIR"
        declare_pages
        for entry in "${PAGES[@]}"; do
            IFS='|' read -r source name keyword volume <<< "$entry"
            echo "Staging $name ($keyword, ${volume}/mo)..."
            prepare_page "$source" "$name"
        done
        echo ""
        echo "=== Staging complete ==="
        echo "Total pages: ${#PAGES[@]}"
        echo "Staging dir: $STAGING_DIR"
        echo ""
        echo "Next: bash $0 --deploy"
        ;;

    --deploy)
        if ! command -v wrangler &> /dev/null; then
            echo "ERROR: wrangler CLI not found."
            echo "Install: npm install -g wrangler"
            echo "Login: wrangler login"
            exit 1
        fi
        echo "=== Deploying to Cloudflare Pages ==="
        declare_pages
        for entry in "${PAGES[@]}"; do
            IFS='|' read -r source name keyword volume <<< "$entry"
            local_dir="$STAGING_DIR/$name"
            if [ -d "$local_dir" ]; then
                echo "Deploying $name..."
                wrangler pages deploy "$local_dir" --project-name="$name" 2>&1 || echo "FAILED: $name (may need project creation first)"
            else
                echo "SKIP: $name not staged. Run --prepare first."
            fi
        done
        echo ""
        echo "=== Deploy complete ==="
        echo "Verify robots.txt: curl https://<name>.pages.dev/robots.txt"
        ;;

    --status)
        echo "=== Migration Status ==="
        declare_pages
        for entry in "${PAGES[@]}"; do
            IFS='|' read -r source name keyword volume <<< "$entry"
            echo -n "$name ($keyword, ${volume}/mo): "
            status=$(curl -s -o /dev/null -w "%{http_code}" "https://$name.pages.dev/" 2>/dev/null || echo "---")
            robots=$(curl -s "https://$name.pages.dev/robots.txt" 2>/dev/null | head -2 | tr '\n' ' ' || echo "UNREACHABLE")
            if [ "$status" = "200" ]; then
                echo "LIVE (HTTP $status) | robots: $robots"
            else
                echo "NOT DEPLOYED (HTTP $status) | Still on surge.sh"
            fi
        done
        ;;

    --netlify)
        echo "=== Alternative: Deploy to Netlify ==="
        if ! command -v netlify &> /dev/null; then
            echo "Install: npm install -g netlify-cli"
            echo "Login: netlify login"
            exit 1
        fi
        declare_pages
        for entry in "${PAGES[@]}"; do
            IFS='|' read -r source name keyword volume <<< "$entry"
            local_dir="$STAGING_DIR/$name"
            if [ -d "$local_dir" ]; then
                echo "Deploying $name to Netlify..."
                netlify deploy --dir="$local_dir" --prod --site="$name" 2>&1 || echo "FAILED: $name"
            fi
        done
        ;;

    *)
        echo "SEO Platform Migration Script"
        echo ""
        echo "Surge.sh free tier blocks ALL search engines at CDN level."
        echo "This script migrates top SEO pages to indexable platforms."
        echo ""
        echo "Usage:"
        echo "  bash $0 --prepare   Prepare migration staging directory"
        echo "  bash $0 --deploy    Deploy to Cloudflare Pages (needs wrangler)"
        echo "  bash $0 --netlify   Deploy to Netlify (alternative)"
        echo "  bash $0 --status    Check deployment status"
        echo ""
        echo "Top 6 pages by keyword volume (65.5K total monthly searches):"
        declare_pages
        for entry in "${PAGES[@]}"; do
            IFS='|' read -r source name keyword volume <<< "$entry"
            echo "  $name: $keyword (${volume}/mo)"
        done
        ;;
esac
