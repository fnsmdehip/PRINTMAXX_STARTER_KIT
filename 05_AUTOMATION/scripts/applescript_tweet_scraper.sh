#!/bin/bash
# Tweet Scraper using AppleScript for Brave Browser
# Requires: "Allow JavaScript from Apple Events" enabled in Brave

OUTPUT_DIR="/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LEDGER"
CSV_FILE="$OUTPUT_DIR/SCRAPED_TWEETS_ALPHA.csv"
JSON_FILE="$OUTPUT_DIR/SCRAPED_TWEETS_ALPHA.json"

# Tweet URLs to scrape
URLS=(
    "https://x.com/xivy0k/status/2013267462616228102"
    "https://x.com/tatealax/status/2013347648321753524"
    "https://x.com/simonecanciello/status/2013290619313992028"
    "https://x.com/lottsnomad/status/2013281137234214961"
    "https://x.com/CEOLandshark/status/2012909226641993869"
    "https://x.com/knoxtwts/status/2011358199144648836"
    "https://x.com/knoxtwts/status/2012895519832518880"
    "https://x.com/wesocialgrowth/status/2012887735879565456"
    "https://x.com/gregisenberg/status/2012960814701949281"
    "https://x.com/matteo_spada/status/2012917994364805177"
    "https://x.com/alexcooldev/status/2013002551587901555"
    "https://x.com/alexcooldev/status/2012466735862182002"
    "https://x.com/pipelineabuser/status/2012028804407980354"
    "https://x.com/pipelineabuser/status/2011864820933673114"
    "https://x.com/pipelineabuser/status/2009717466600206558"
    "https://x.com/seanb2b/status/2012977071279014342"
    "https://x.com/WorkflowWhisper/status/2012566082326868407"
    "https://x.com/joelhooks/status/2012934260265816387"
    "https://x.com/wannercashcow/status/2013182221512036821"
    "https://x.com/mattwelter/status/2013271008342659529"
    "https://x.com/Jahjiren/status/2013195696824827981"
    "https://x.com/purpdevvv/status/2013201984916980003"
    "https://x.com/purpdevvv/status/2012442944947585410"
)

# Initialize CSV with headers
echo "url,handle,author,text,timestamp,scraped_at,status" > "$CSV_FILE"

# Initialize JSON array
echo "[" > "$JSON_FILE"

TOTAL=${#URLS[@]}
COUNT=0
FIRST=true

echo "Scraping $TOTAL tweets..."

for URL in "${URLS[@]}"; do
    COUNT=$((COUNT + 1))
    HANDLE=$(echo "$URL" | cut -d'/' -f4)
    echo "[$COUNT/$TOTAL] @$HANDLE..."

    # Navigate to URL
    osascript -e "tell application \"Brave Browser\" to set URL of active tab of front window to \"$URL\""

    # Wait for page load
    sleep 3

    # Extract tweet data
    RESULT=$(osascript -e 'tell application "Brave Browser" to execute active tab of front window javascript "
(function() {
    var tweetText = document.querySelector(\"[data-testid=tweetText]\");
    var author = document.querySelector(\"[data-testid=User-Name]\");
    var time = document.querySelector(\"time\");
    return JSON.stringify({
        text: tweetText ? tweetText.innerText.replace(/\\n/g, \" \").replace(/\"/g, \"\\\\\"\") : \"\",
        author: author ? author.innerText.split(\"\\n\")[0] : \"\",
        handle: author ? author.innerText.split(\"\\n\")[1] : \"\",
        timestamp: time ? time.getAttribute(\"datetime\") : \"\"
    });
})()
"' 2>&1)

    if [[ "$RESULT" == *"error"* ]]; then
        echo "  ERROR: $RESULT"
        STATUS="ERROR"
        TEXT=""
        AUTHOR=""
        TWEET_HANDLE=""
        TIMESTAMP=""
    else
        STATUS="SUCCESS"
        # Parse JSON result
        TEXT=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('text',''))" 2>/dev/null || echo "")
        AUTHOR=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('author',''))" 2>/dev/null || echo "")
        TWEET_HANDLE=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('handle',''))" 2>/dev/null || echo "@$HANDLE")
        TIMESTAMP=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('timestamp',''))" 2>/dev/null || echo "")
        echo "  OK: ${TEXT:0:60}..."
    fi

    SCRAPED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Escape for CSV
    TEXT_CSV=$(echo "$TEXT" | sed 's/"/""/g')

    # Append to CSV
    echo "\"$URL\",\"$TWEET_HANDLE\",\"$AUTHOR\",\"$TEXT_CSV\",\"$TIMESTAMP\",\"$SCRAPED_AT\",\"$STATUS\"" >> "$CSV_FILE"

    # Append to JSON
    if [ "$FIRST" = true ]; then
        FIRST=false
    else
        echo "," >> "$JSON_FILE"
    fi

    cat >> "$JSON_FILE" << JSONEOF
  {
    "url": "$URL",
    "handle": "$TWEET_HANDLE",
    "author": "$AUTHOR",
    "text": "$TEXT",
    "timestamp": "$TIMESTAMP",
    "scraped_at": "$SCRAPED_AT",
    "status": "$STATUS"
  }
JSONEOF

    # Rate limiting
    sleep 2
done

# Close JSON array
echo "]" >> "$JSON_FILE"

echo ""
echo "Done! Scraped $COUNT tweets"
echo "CSV: $CSV_FILE"
echo "JSON: $JSON_FILE"
