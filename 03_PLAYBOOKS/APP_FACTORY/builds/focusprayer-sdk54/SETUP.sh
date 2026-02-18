#!/bin/bash

# Setup script for focusprayer-sdk54
# This script copies remaining directories from the original focusprayer app

SRC_DIR="/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/builds/focusprayer"
DEST_DIR="/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/builds/focusprayer-sdk54"

echo "Setting up focusprayer-sdk54..."
echo ""

# Copy app directory
echo "Copying app directory..."
cp -r "$SRC_DIR/app" "$DEST_DIR/app"
if [ $? -eq 0 ]; then
    echo "✓ app directory copied"
else
    echo "✗ Failed to copy app directory"
    exit 1
fi

# Copy src directory
echo "Copying src directory..."
cp -r "$SRC_DIR/src" "$DEST_DIR/src"
if [ $? -eq 0 ]; then
    echo "✓ src directory copied"
else
    echo "✗ Failed to copy src directory"
    exit 1
fi

# Copy assets directory
echo "Copying assets directory..."
cp -r "$SRC_DIR/assets" "$DEST_DIR/assets"
if [ $? -eq 0 ]; then
    echo "✓ assets directory copied"
else
    echo "✗ Failed to copy assets directory"
    exit 1
fi

# Copy __tests__ directory
echo "Copying __tests__ directory..."
cp -r "$SRC_DIR/__tests__" "$DEST_DIR/__tests__"
if [ $? -eq 0 ]; then
    echo "✓ __tests__ directory copied"
else
    echo "✗ Failed to copy __tests__ directory"
    exit 1
fi

echo ""
echo "✓ All directories copied successfully!"
echo ""
echo "Next steps:"
echo "1. cd focusprayer-sdk54"
echo "2. npm install"
echo "3. npx expo start --ios"
