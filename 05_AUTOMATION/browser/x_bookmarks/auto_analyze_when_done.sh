#!/bin/bash

echo "⏳ Waiting for scraper to finish..."

# Wait for scraper process to finish
while pgrep -f "deep_scrape_bookmarks.py" > /dev/null; do
    # Check latest progress
    LATEST=$(ls -t deep_scrape_output/progress_*.json 2>/dev/null | head -1)
    if [ -n "$LATEST" ]; then
        COUNT=$(echo "$LATEST" | grep -o '[0-9]*_bookmarks' | grep -o '[0-9]*')
        echo "📊 Progress: $COUNT/238 bookmarks..."
    fi
    sleep 30
done

echo "✅ Scraper finished! Running analysis..."

# Run analysis
python3 analyze_deep_results.py

echo "🎉 Analysis complete! Check deep_scrape_output/extracted_alpha.json"
