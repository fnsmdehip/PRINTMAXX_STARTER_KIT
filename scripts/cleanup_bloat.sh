#!/bin/bash
# PRINTMAXX Bloat Cleanup Script
# Default: Dry-run mode (shows what would be deleted)
# Use --execute flag to actually delete

set -e

PROJECT_ROOT="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
DRY_RUN=true

# Parse arguments
if [ "$1" = "--execute" ]; then
    DRY_RUN=false
    echo "⚠️  EXECUTE MODE - Will actually delete files"
    echo "Press Ctrl+C within 5 seconds to cancel..."
    sleep 5
else
    echo "🔍 DRY-RUN MODE - Showing what would be deleted"
    echo "Use --execute flag to actually delete"
    echo ""
fi

echo "=============================================="
echo "PRINTMAXX DISK BLOAT CLEANUP REPORT"
echo "=============================================="
echo ""

# Function to format bytes to human readable
format_size() {
    numfmt --to=iec-i --suffix=B "$1" 2>/dev/null || echo "$1 bytes"
}

# Track total space to be freed
TOTAL_FREED=0

echo "📦 FINDING ALL node_modules DIRECTORIES..."
echo ""

# Find all node_modules and calculate total size
NODE_MODULES_DIRS=$(find "$PROJECT_ROOT" -name "node_modules" -type d 2>/dev/null)
NODE_MODULES_COUNT=$(echo "$NODE_MODULES_DIRS" | grep -c "node_modules" || echo "0")

echo "Found $NODE_MODULES_COUNT node_modules directories"
echo ""

if [ "$NODE_MODULES_COUNT" -gt 0 ]; then
    echo "Top 10 largest node_modules directories:"
    echo "----------------------------------------"

    while IFS= read -r dir; do
        if [ -d "$dir" ]; then
            SIZE=$(du -sb "$dir" 2>/dev/null | cut -f1)
            TOTAL_FREED=$((TOTAL_FREED + SIZE))
            echo "$(du -sh "$dir" 2>/dev/null | cut -f1) - $dir"
        fi
    done < <(find "$PROJECT_ROOT" -name "node_modules" -type d 2>/dev/null | while read d; do du -sb "$d" 2>/dev/null; done | sort -rn | head -10 | cut -f2)

    echo ""
fi

echo "=============================================="
echo "SUMMARY"
echo "=============================================="
echo "Total node_modules directories: $NODE_MODULES_COUNT"
echo "Total space to free: $(format_size $TOTAL_FREED)"
echo ""

# Legacy app factory check
LEGACY_DIR="$PROJECT_ROOT/app factory"
if [ -d "$LEGACY_DIR" ]; then
    LEGACY_SIZE=$(du -sb "$LEGACY_DIR" 2>/dev/null | cut -f1)
    echo "⚠️  LEGACY DIRECTORY FOUND:"
    echo "   Location: app factory/"
    echo "   Size: $(du -sh "$LEGACY_DIR" 2>/dev/null | cut -f1)"
    echo "   Note: This is the OLD app factory (use MONEY_METHODS/APP_FACTORY/ instead)"
    echo "   Recommendation: Archive or delete after confirming no unique assets"
    echo ""
fi

# Current project size
PROJECT_SIZE=$(du -sh "$PROJECT_ROOT" 2>/dev/null | cut -f1)
echo "Current project size: $PROJECT_SIZE"
echo ""

# Execute cleanup if requested
if [ "$DRY_RUN" = false ]; then
    echo "=============================================="
    echo "EXECUTING CLEANUP"
    echo "=============================================="
    echo ""

    DELETED_COUNT=0

    echo "Deleting node_modules directories..."
    while IFS= read -r dir; do
        if [ -d "$dir" ]; then
            echo "Deleting: $dir"
            rm -rf "$dir"
            DELETED_COUNT=$((DELETED_COUNT + 1))
        fi
    done < <(find "$PROJECT_ROOT" -name "node_modules" -type d 2>/dev/null)

    echo ""
    echo "✅ Cleanup complete!"
    echo "   Deleted: $DELETED_COUNT node_modules directories"
    echo "   Freed: $(format_size $TOTAL_FREED) (approximately)"
    echo ""
    echo "To reinstall dependencies when needed:"
    echo "   cd <project-directory> && npm install"
    echo ""
else
    echo "=============================================="
    echo "TO EXECUTE CLEANUP:"
    echo "=============================================="
    echo ""
    echo "Review the report above, then run:"
    echo "   bash $0 --execute"
    echo ""
    echo "⚠️  IMPORTANT: This will delete ALL node_modules directories"
    echo "   You can reinstall with 'npm install' in each project when needed"
    echo ""
fi
