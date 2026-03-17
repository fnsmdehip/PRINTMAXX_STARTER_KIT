#!/bin/bash
# SEO-aware surge.sh deployment wrapper
# Ensures every deployment includes robots.txt (Allow: /) and sitemap reference
# Usage: bash seo_deploy_wrapper.sh <html_file_or_directory> <subdomain>.surge.sh

set -e

SOURCE="$1"
DOMAIN="$2"

# Handle --batch before arg validation (batch only needs $1)
if [ "$SOURCE" = "--batch" ]; then
    DOMAIN="batch"
fi

if [ -z "$SOURCE" ] || [ -z "$DOMAIN" ]; then
    echo "Usage: bash seo_deploy_wrapper.sh <html_file_or_directory> <subdomain>.surge.sh"
    echo ""
    echo "Examples:"
    echo "  bash seo_deploy_wrapper.sh path/to/index.html myapp.surge.sh"
    echo "  bash seo_deploy_wrapper.sh path/to/directory/ myapp.surge.sh"
    echo "  bash seo_deploy_wrapper.sh --batch  # Deploy all lead magnets"
    exit 1
fi

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

# Batch mode: deploy all lead magnets
if [ "$SOURCE" = "--batch" ]; then
    echo "=== Batch SEO Deploy: Lead Magnets ==="
    LEAD_DIR="DIGITAL_PRODUCTS/lead_magnets"

    # bash 3 compatible (no associative arrays on macOS default bash)
    LEAD_FILES="freelance-rate-calculator.html:freelance-rate-calc.surge.sh
cold-email-roi-calculator.html:cold-email-roi-calculator.surge.sh
ai-slop-detector.html:ai-slop-detector.surge.sh
subject-line-grader.html:subject-line-grader.surge.sh
vibe-coding-cheat-sheet.html:vibe-coding-cheat-sheet.surge.sh
vibe-coding-profit-calculator.html:vibe-coding-profit-calc.surge.sh
side-project-revenue-estimator.html:side-project-revenue-est.surge.sh
saas-stack-audit.html:saas-stack-audit.surge.sh
revenue-leak-audit.html:revenue-leak-audit.surge.sh
solopreneur-launch-checklist.html:solopreneur-launch-checklist.surge.sh
ramadan-daily-planner.html:ramadan-daily-planner.surge.sh
productivity-stack-quiz.html:productivity-stack-quiz.surge.sh
200.html:200-day-calculator.surge.sh
app-hub-crosslinks.html:app-hub-crosslinks.surge.sh"

    echo "$LEAD_FILES" | while IFS=: read -r file domain; do
        src="$LEAD_DIR/$file"
        if [ -f "$src" ]; then
            echo "Deploying $file -> $domain"
            bash "$0" "$src" "$domain"
        else
            echo "SKIP: $src not found"
        fi
    done

    echo "=== Batch deploy complete ==="
    exit 0
fi

# Create temp directory for deployment
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

if [ -d "$SOURCE" ]; then
    # Source is a directory - copy contents
    cp -r "$SOURCE"/* "$TMPDIR/" 2>/dev/null || true
    cp -r "$SOURCE"/.* "$TMPDIR/" 2>/dev/null || true
else
    # Source is a single HTML file - copy as index.html
    cp "$SOURCE" "$TMPDIR/index.html"

    # Also copy any sibling assets (manifest.json, sw.js, etc.)
    SRCDIR=$(dirname "$SOURCE")
    for asset in manifest.json sw.js service-worker.js lead-capture-universal.js; do
        if [ -f "$SRCDIR/$asset" ]; then
            cp "$SRCDIR/$asset" "$TMPDIR/"
        fi
    done
fi

# Always add/override robots.txt with Allow
echo "$ROBOTS_CONTENT" > "$TMPDIR/robots.txt"

# Add a basic sitemap if missing
if [ ! -f "$TMPDIR/sitemap.xml" ]; then
    cat > "$TMPDIR/sitemap.xml" << SITEMAP
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://${DOMAIN}/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
    <lastmod>$(date +%Y-%m-%d)</lastmod>
  </url>
</urlset>
SITEMAP
fi

# Deploy
echo "Deploying to $DOMAIN..."
echo "Files in deploy directory:"
ls -la "$TMPDIR/"
echo ""

# Check if surge is available
if command -v surge &> /dev/null; then
    surge "$TMPDIR" "$DOMAIN"
    echo "Deployed successfully: https://$DOMAIN"
else
    echo "ERROR: surge CLI not found. Install with: npm install -g surge"
    echo "Deploy directory ready at: $TMPDIR"
    echo "Manual deploy: surge $TMPDIR $DOMAIN"
    # Keep temp dir alive if surge not found
    trap "" EXIT
fi
