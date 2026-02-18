#!/bin/bash
# Daily viral content scan workflow
# Run this once per day (morning recommended)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_DIR"

echo "==========================================="
echo "VIRAL CONTENT DAILY SCAN"
echo "==========================================="
echo ""

# 1. Scan all meme accounts
echo "📡 Step 1: Scanning meme accounts for viral content..."
python3 AUTOMATIONS/viral_content_scanner.py --scan
echo ""

# 2. Download media
echo "📥 Step 2: Downloading media from viral tweets..."
python3 AUTOMATIONS/viral_content_scanner.py --download
echo ""

# 3. Generate scheduled queue
echo "📅 Step 3: Generating scheduled posting queue..."
python3 AUTOMATIONS/viral_content_scanner.py --schedule
echo ""

# 4. Show stats
echo "📊 Step 4: Statistics..."
python3 AUTOMATIONS/viral_content_scanner.py --stats
echo ""

# 5. Summary
echo "==========================================="
echo "DAILY SCAN COMPLETE"
echo "==========================================="
echo ""
echo "Next steps:"
echo "1. Review: AUTOMATIONS/viral_content/repurpose_queue.csv"
echo "2. Curate: Mark APPROVED for content you want to post"
echo "3. Edit: Adjust captions/times if needed"
echo "4. Post: Upload to Buffer or post manually"
echo ""
echo "Files created:"
echo "- repurpose_queue.csv (main queue)"
echo "- media/ (downloaded images/videos)"
echo "- scan_history/ (historical data)"
echo ""
