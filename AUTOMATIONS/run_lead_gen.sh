#!/usr/bin/env bash
#
# run_lead_gen.sh - Batch lead generation across top US cities and industries
#
# Runs the savvy_lead_scraper.py for:
#   - 10 US cities (Austin, Miami, Dallas, Houston, Phoenix, Denver, Nashville, Atlanta, Charlotte, Tampa)
#   - 5 high-margin industries (dental, legal, HVAC, real estate, remodeling)
#   = 50 discovery runs, ~500+ scored leads
#
# Usage:
#   ./run_lead_gen.sh                    # Full blast (50 runs, ~2-3 hours)
#   ./run_lead_gen.sh --quick            # Quick mode (3 cities x 3 industries = 9 runs, ~20 min)
#   ./run_lead_gen.sh --city "Austin TX" # Single city, all top industries
#   ./run_lead_gen.sh --urls prospects.csv # Score existing URLs only
#
# Output: AUTOMATIONS/output/savvy_leads/leads_<timestamp>.csv
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRAPER="$SCRIPT_DIR/savvy_lead_scraper.py"
OUTPUT_DIR="$SCRIPT_DIR/output/savvy_leads"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${BOLD}${CYAN}================================================================${NC}"
echo -e "${BOLD}${CYAN}  SAVVY LEAD SCRAPER - Batch Lead Generation${NC}"
echo -e "${BOLD}${CYAN}  $(date)${NC}"
echo -e "${BOLD}${CYAN}================================================================${NC}"
echo ""

# Check Python dependencies
if ! python3 -c "import requests, bs4, tqdm" 2>/dev/null; then
    echo -e "${RED}Missing Python dependencies. Installing...${NC}"
    pip install requests beautifulsoup4 tqdm
fi

# Check scraper exists
if [ ! -f "$SCRAPER" ]; then
    echo -e "${RED}Scraper not found at: $SCRAPER${NC}"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Parse arguments
MODE="full"
SINGLE_CITY=""
URLS_FILE=""
COUNT=10
MIN_SCORE=30

while [[ $# -gt 0 ]]; do
    case $1 in
        --quick)
            MODE="quick"
            shift
            ;;
        --city)
            MODE="single"
            SINGLE_CITY="$2"
            shift 2
            ;;
        --urls)
            MODE="urls"
            URLS_FILE="$2"
            shift 2
            ;;
        --count)
            COUNT="$2"
            shift 2
            ;;
        --min-score)
            MIN_SCORE="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --quick              Quick mode: 3 cities x 3 industries (9 runs)"
            echo "  --city \"City ST\"     Single city, all top 5 industries"
            echo "  --urls file.csv      Score existing URLs only"
            echo "  --count N            Leads per city/industry (default: 10)"
            echo "  --min-score N        Minimum score threshold (default: 30)"
            echo "  --help               Show this help"
            echo ""
            echo "Default: Full blast (10 cities x 5 industries = 50 runs)"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

OUTPUT_FILE="$OUTPUT_DIR/leads_batch_${TIMESTAMP}.csv"

case $MODE in
    full)
        echo -e "${BOLD}Mode: FULL BLAST${NC}"
        echo -e "  10 cities x 5 industries = 50 runs"
        echo -e "  ~${COUNT} leads per run = ~$((COUNT * 50)) potential leads"
        echo -e "  Estimated time: 2-3 hours (with 2s rate limit)"
        echo -e "  Min score: $MIN_SCORE"
        echo -e "  Output: $OUTPUT_FILE"
        echo ""

        python3 "$SCRAPER" \
            --full-blast \
            --count "$COUNT" \
            --min-score "$MIN_SCORE" \
            --output "$OUTPUT_FILE"
        ;;

    quick)
        echo -e "${BOLD}Mode: QUICK (3 cities x 3 industries = 9 runs)${NC}"
        echo ""

        # Quick mode: 3 high-value cities x 3 highest-margin industries
        CITIES=("Austin TX" "Miami FL" "Dallas TX")
        INDUSTRIES=("dental" "legal" "hvac")

        FIRST=true
        for city in "${CITIES[@]}"; do
            for ind in "${INDUSTRIES[@]}"; do
                TEMP_FILE="$OUTPUT_DIR/temp_${ind}_$(echo "$city" | tr ' ' '_').csv"

                echo -e "${CYAN}Running: $ind in $city${NC}"
                python3 "$SCRAPER" \
                    --city "$city" \
                    --industry "$ind" \
                    --count "$COUNT" \
                    --min-score "$MIN_SCORE" \
                    --output "$TEMP_FILE" 2>&1 | tail -5

                # Merge CSVs (keep header only from first file)
                if [ -f "$TEMP_FILE" ]; then
                    if $FIRST; then
                        cp "$TEMP_FILE" "$OUTPUT_FILE"
                        FIRST=false
                    else
                        tail -n +2 "$TEMP_FILE" >> "$OUTPUT_FILE"
                    fi
                    rm -f "$TEMP_FILE"
                fi
            done
        done
        ;;

    single)
        echo -e "${BOLD}Mode: Single City - $SINGLE_CITY${NC}"
        echo -e "  5 industries, ~${COUNT} leads each"
        echo ""

        python3 "$SCRAPER" \
            --city "$SINGLE_CITY" \
            --industry all \
            --count "$COUNT" \
            --min-score "$MIN_SCORE" \
            --output "$OUTPUT_FILE"
        ;;

    urls)
        echo -e "${BOLD}Mode: Score existing URLs${NC}"
        echo -e "  Input: $URLS_FILE"
        echo ""

        python3 "$SCRAPER" \
            --urls-file "$URLS_FILE" \
            --min-score "$MIN_SCORE" \
            --output "$OUTPUT_FILE"
        ;;
esac

# Final summary
echo ""
echo -e "${BOLD}${GREEN}================================================================${NC}"
echo -e "${BOLD}${GREEN}  BATCH COMPLETE${NC}"
echo -e "${BOLD}${GREEN}================================================================${NC}"

if [ -f "$OUTPUT_FILE" ]; then
    TOTAL_LEADS=$(($(wc -l < "$OUTPUT_FILE") - 1))
    HOT_LEADS=$(grep -c ",HOT," "$OUTPUT_FILE" 2>/dev/null || echo 0)
    WARM_LEADS=$(grep -c ",WARM," "$OUTPUT_FILE" 2>/dev/null || echo 0)

    echo -e "  Output:     $OUTPUT_FILE"
    echo -e "  Total leads: $TOTAL_LEADS"
    echo -e "  ${RED}HOT leads:   $HOT_LEADS${NC}"
    echo -e "  ${YELLOW}WARM leads:  $WARM_LEADS${NC}"
    echo ""
    echo -e "${BOLD}Next steps:${NC}"
    echo "  1. Review HOT leads:"
    echo "     head -20 $OUTPUT_FILE"
    echo ""
    echo "  2. Generate demo pages + cold emails:"
    echo "     python3 $SCRIPT_DIR/local_biz_pipeline.py --urls-file $OUTPUT_FILE"
    echo ""
    echo "  3. Or filter HOT leads only:"
    echo "     head -1 $OUTPUT_FILE > hot_leads.csv"
    echo "     grep ',HOT,' $OUTPUT_FILE >> hot_leads.csv"
    echo ""
else
    echo -e "${RED}  No output file generated. Check logs in $OUTPUT_DIR/logs/${NC}"
fi

echo ""
