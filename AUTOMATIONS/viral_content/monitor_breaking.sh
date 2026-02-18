#!/bin/bash
# Breaking viral content monitor
# Run every 30-60 minutes to catch high-velocity viral content

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_DIR"

echo "🚨 Checking for breaking viral content (last 2 hours)..."
echo ""

python3 AUTOMATIONS/viral_content_scanner.py --breaking

# Check if breaking alerts file exists and has content
ALERTS_FILE="AUTOMATIONS/viral_content/breaking_alerts.json"

if [ -f "$ALERTS_FILE" ]; then
    # Count number of alerts
    ALERT_COUNT=$(jq '. | length' "$ALERTS_FILE" 2>/dev/null || echo "0")

    if [ "$ALERT_COUNT" -gt 0 ]; then
        echo ""
        echo "⚠️  BREAKING VIRAL CONTENT DETECTED"
        echo "   $ALERT_COUNT high-velocity tweets found"
        echo ""
        echo "Action required:"
        echo "1. Review: $ALERTS_FILE"
        echo "2. Download media immediately"
        echo "3. Post ASAP (don't wait for schedule)"
        echo "4. Capitalize on viral velocity"
        echo ""

        # Show top 3 by viral velocity
        echo "Top breaking tweets:"
        jq -r '.[:3] | .[] | "  @\(.handle): \(.viral_velocity | floor) likes/hour - \(.text[:60])..."' "$ALERTS_FILE" 2>/dev/null || true
        echo ""
    else
        echo "✅ No breaking viral content detected"
        echo "   All clear - check again in 30-60 minutes"
        echo ""
    fi
else
    echo "✅ No breaking viral content detected"
    echo ""
fi
