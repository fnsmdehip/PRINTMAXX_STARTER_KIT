#!/bin/bash

# Sleep Video Production Script
# Creates YouTube-ready sleep videos with looped audio and optional alarm sounds
#
# Usage: ./video_production_script.sh "Video Title" audio_file.mp3 8 [with_alarms]
#
# Arguments:
#   $1 - Video title (used for output filename and thumbnail)
#   $2 - Input audio file path (mp3, wav, ogg, etc.)
#   $3 - Duration in hours (e.g., 8 for 8 hours)
#   $4 - "alarms" to add gentle alarms at 6, 7, 8 hours (optional)
#
# Requirements:
#   - ffmpeg (install: brew install ffmpeg on macOS)
#   - ImageMagick (install: brew install imagemagick on macOS)
#
# Output:
#   - {title_slug}_video.mp4 (YouTube-ready video)
#   - {title_slug}_thumbnail.png (1280x720 thumbnail)

set -e  # Exit on error

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${RED}Error: ffmpeg is not installed${NC}"
    echo "Install with: brew install ffmpeg"
    exit 1
fi

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo -e "${RED}Error: ImageMagick is not installed${NC}"
    echo "Install with: brew install imagemagick"
    exit 1
fi

# Parse arguments
if [ $# -lt 3 ]; then
    echo -e "${RED}Error: Missing required arguments${NC}"
    echo "Usage: $0 \"Video Title\" audio_file.mp3 duration_hours [alarms]"
    echo "Example: $0 \"Rain Sounds for Sleep\" rain.mp3 8 alarms"
    exit 1
fi

TITLE="$1"
AUDIO_FILE="$2"
DURATION_HOURS="$3"
ADD_ALARMS="${4:-no}"

# Check if audio file exists
if [ ! -f "$AUDIO_FILE" ]; then
    echo -e "${RED}Error: Audio file not found: $AUDIO_FILE${NC}"
    exit 1
fi

# Create slug from title (lowercase, spaces to underscores, remove special chars)
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | sed 's/[^a-z0-9_]//g')

# Calculate duration in seconds
DURATION_SECONDS=$((DURATION_HOURS * 3600))

# Output filenames
OUTPUT_VIDEO="${SLUG}_video.mp4"
OUTPUT_THUMBNAIL="${SLUG}_thumbnail.png"
TEMP_LOOPED_AUDIO="${SLUG}_looped_audio.mp3"
TEMP_VIDEO="${SLUG}_temp_video.mp4"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Sleep Video Production Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Title: $TITLE"
echo "Audio File: $AUDIO_FILE"
echo "Duration: $DURATION_HOURS hours ($DURATION_SECONDS seconds)"
echo "Add Alarms: $ADD_ALARMS"
echo "Output Video: $OUTPUT_VIDEO"
echo "Output Thumbnail: $OUTPUT_THUMBNAIL"
echo ""

# Step 1: Get audio duration
echo -e "${YELLOW}[1/5] Analyzing audio file...${NC}"
AUDIO_DURATION=$(ffprobe -i "$AUDIO_FILE" -show_entries format=duration -v quiet -of csv="p=0")
AUDIO_DURATION_INT=${AUDIO_DURATION%.*}
echo "Audio duration: $AUDIO_DURATION seconds"

# Step 2: Loop audio to match video duration
echo -e "${YELLOW}[2/5] Looping audio to $DURATION_HOURS hours...${NC}"

# Calculate how many times to loop
LOOP_COUNT=$((DURATION_SECONDS / AUDIO_DURATION_INT + 1))

# Create looped audio
ffmpeg -stream_loop $LOOP_COUNT -i "$AUDIO_FILE" -t $DURATION_SECONDS -c:a aac -b:a 128k -ac 2 -y "$TEMP_LOOPED_AUDIO" -loglevel warning -stats

echo "Audio looped successfully"

# Step 3: Add alarm sounds if requested
if [ "$ADD_ALARMS" = "alarms" ]; then
    echo -e "${YELLOW}[3/5] Adding gentle alarm sounds at 6, 7, 8 hours...${NC}"

    # Generate alarm sound (sine wave fade-in, 10 seconds)
    ALARM_FILE="${SLUG}_alarm.mp3"
    ffmpeg -f lavfi -i "sine=frequency=440:duration=10" -af "afade=t=in:st=0:d=8,volume=0.3" -y "$ALARM_FILE" -loglevel warning

    # Add alarms at specified times using filter_complex
    ALARM_AUDIO="${SLUG}_with_alarms.mp3"

    # Determine which alarms to add based on duration
    if [ $DURATION_HOURS -ge 8 ]; then
        # Add alarms at 6, 7, and 8 hours
        ffmpeg -i "$TEMP_LOOPED_AUDIO" -i "$ALARM_FILE" -i "$ALARM_FILE" -i "$ALARM_FILE" \
            -filter_complex "[0:a][1:a]adelay=21600000|21600000[a1];[a1][2:a]adelay=25200000|25200000[a2];[a2][3:a]adelay=28800000|28800000[out]" \
            -map "[out]" -c:a aac -b:a 128k -y "$ALARM_AUDIO" -loglevel warning -stats
    elif [ $DURATION_HOURS -ge 7 ]; then
        # Add alarms at 6 and 7 hours
        ffmpeg -i "$TEMP_LOOPED_AUDIO" -i "$ALARM_FILE" -i "$ALARM_FILE" \
            -filter_complex "[0:a][1:a]adelay=21600000|21600000[a1];[a1][2:a]adelay=25200000|25200000[out]" \
            -map "[out]" -c:a aac -b:a 128k -y "$ALARM_AUDIO" -loglevel warning -stats
    elif [ $DURATION_HOURS -ge 6 ]; then
        # Add alarm at 6 hours only
        ffmpeg -i "$TEMP_LOOPED_AUDIO" -i "$ALARM_FILE" \
            -filter_complex "[0:a][1:a]adelay=21600000|21600000[out]" \
            -map "[out]" -c:a aac -b:a 128k -y "$ALARM_AUDIO" -loglevel warning -stats
    else
        # Duration too short for alarms, just copy
        cp "$TEMP_LOOPED_AUDIO" "$ALARM_AUDIO"
    fi

    rm "$ALARM_FILE"
    FINAL_AUDIO="$ALARM_AUDIO"
else
    echo -e "${YELLOW}[3/5] Skipping alarm sounds${NC}"
    FINAL_AUDIO="$TEMP_LOOPED_AUDIO"
fi

# Step 4: Create video with black screen (or dark gradient)
echo -e "${YELLOW}[4/5] Generating video with black screen...${NC}"

# Option A: Pure black screen (most battery efficient)
# ffmpeg -f lavfi -i color=c=black:s=1920x1080:d=$DURATION_SECONDS -i "$FINAL_AUDIO" \
#     -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p -c:a copy -shortest -y "$OUTPUT_VIDEO" -loglevel warning -stats

# Option B: Dark gradient (more interesting, still battery friendly)
ffmpeg -f lavfi -i color=c=0x0a0e27:s=1920x1080:d=$DURATION_SECONDS -i "$FINAL_AUDIO" \
    -vf "format=yuv420p" -c:v libx264 -preset fast -crf 23 -c:a copy -shortest -y "$OUTPUT_VIDEO" -loglevel warning -stats

echo "Video created successfully"

# Step 5: Generate thumbnail
echo -e "${YELLOW}[5/5] Generating thumbnail...${NC}"

# Create 1280x720 thumbnail with dark background and white text
convert -size 1280x720 xc:"#0a0e27" \
    -gravity center \
    -font Arial -pointsize 72 -fill white -annotate +0-50 "$TITLE" \
    -font Arial -pointsize 36 -fill "#aaaaaa" -annotate +0+50 "${DURATION_HOURS} Hours • Black Screen" \
    "$OUTPUT_THUMBNAIL"

echo "Thumbnail created successfully"

# Cleanup temporary files
echo ""
echo -e "${YELLOW}Cleaning up temporary files...${NC}"
rm -f "$TEMP_LOOPED_AUDIO"
[ -f "$ALARM_AUDIO" ] && rm -f "$ALARM_AUDIO"

# Display file sizes
VIDEO_SIZE=$(du -h "$OUTPUT_VIDEO" | cut -f1)
THUMB_SIZE=$(du -h "$OUTPUT_THUMBNAIL" | cut -f1)

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Production Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Output Files:"
echo "  Video: $OUTPUT_VIDEO ($VIDEO_SIZE)"
echo "  Thumbnail: $OUTPUT_THUMBNAIL ($THUMB_SIZE)"
echo ""
echo "Next Steps:"
echo "  1. Upload $OUTPUT_VIDEO to YouTube"
echo "  2. Use $OUTPUT_THUMBNAIL as custom thumbnail"
echo "  3. Add description from video_descriptions.md"
echo "  4. Set visibility to Public (or schedule)"
echo ""
echo -e "${GREEN}Ready for upload!${NC}"
