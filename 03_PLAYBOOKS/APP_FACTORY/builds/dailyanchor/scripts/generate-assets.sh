#!/bin/bash
# Generate placeholder assets for DailyAnchor

cd "$(dirname "$0")/../assets"

# Create a simple 1024x1024 purple PNG for icon
# Using ImageMagick if available, otherwise create empty placeholder
if command -v convert &> /dev/null; then
    convert -size 1024x1024 xc:'#6366F1' icon.png
    convert -size 1024x1024 xc:'#6366F1' adaptive-icon.png
    convert -size 1284x2778 xc:'#F8FAFC' splash.png
    convert -size 32x32 xc:'#6366F1' favicon.png
    echo "Assets generated with ImageMagick"
else
    # Create minimal PNG files using printf and base64
    # These are valid but minimal PNG files
    printf '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\x00\x00\x00\x04\x00\x08\x02\x00\x00\x00\xe8\xe7\xedW\x00\x00\x00\x12IDATx\x9c\xed\xc1\x01\x01\x00\x00\x00\x82 \xff\xafn\xc8@\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x03\x00\xca\xc0\x00\x01\xdaq\x8e7\x00\x00\x00\x00IEND\xaeB`\x82' > icon.png
    cp icon.png adaptive-icon.png
    cp icon.png splash.png
    cp icon.png favicon.png
    echo "Placeholder assets created. Replace with actual images later."
fi

echo "Done! Assets created in $(pwd)"
