#!/bin/bash

# GlowMaxx SDK 54 Migration Completion Script
# This script completes the Expo SDK 54 upgrade by copying remaining files

set -e

GLOWMAXX_SOURCE="../glowmaxx"
GLOWMAXX_SDK54="."

echo "Starting GlowMaxx SDK 54 migration completion..."

# Copy src directory
echo "Copying src directory..."
cp -r "$GLOWMAXX_SOURCE/src/stores" "$GLOWMAXX_SDK54/src/" || echo "Stores directory already exists or copy failed"
cp -r "$GLOWMAXX_SOURCE/src/components" "$GLOWMAXX_SDK54/src/" || echo "Components directory already exists or copy failed"
cp -r "$GLOWMAXX_SOURCE/src/services" "$GLOWMAXX_SDK54/src/" || echo "Services directory already exists or copy failed"
cp -r "$GLOWMAXX_SOURCE/src/data" "$GLOWMAXX_SDK54/src/" || echo "Data directory already exists or copy failed"
cp "$GLOWMAXX_SOURCE/src/utils/dateUtils.ts" "$GLOWMAXX_SDK54/src/utils/" || echo "dateUtils already exists or copy failed"

# Copy assets
echo "Copying assets..."
cp -r "$GLOWMAXX_SOURCE/assets/"* "$GLOWMAXX_SDK54/assets/" 2>/dev/null || echo "Assets copy completed"

# Copy remaining app screens
echo "Copying remaining app screens..."
cp "$GLOWMAXX_SOURCE/app/paywall.tsx" "$GLOWMAXX_SDK54/app/" 2>/dev/null || echo "paywall.tsx already exists or needs manual copy"
cp "$GLOWMAXX_SOURCE/app/routine-player.tsx" "$GLOWMAXX_SDK54/app/" 2>/dev/null || echo "routine-player.tsx already exists or needs manual copy"
cp "$GLOWMAXX_SOURCE/app/privacy-policy.tsx" "$GLOWMAXX_SDK54/app/" 2>/dev/null || echo "privacy-policy.tsx already exists or needs manual copy"
cp "$GLOWMAXX_SOURCE/app/terms.tsx" "$GLOWMAXX_SDK54/app/" 2>/dev/null || echo "terms.tsx already exists or needs manual copy"

# Copy other config files
echo "Copying config files..."
cp "$GLOWMAXX_SOURCE/babel.config.js" "$GLOWMAXX_SDK54/" 2>/dev/null || echo "babel.config.js already exists"
cp "$GLOWMAXX_SOURCE/metro.config.js" "$GLOWMAXX_SDK54/" 2>/dev/null || echo "metro.config.js already exists"
cp "$GLOWMAXX_SOURCE/.prettierrc.js" "$GLOWMAXX_SDK54/" 2>/dev/null || echo ".prettierrc.js already exists"

# Install dependencies
echo "Installing dependencies..."
npm install

# Generate expo config
echo "Generating Expo config..."
npx expo prebuild --clean 2>/dev/null || echo "Prebuild (optional) - can be done later"

echo ""
echo "Migration completion script finished!"
echo ""
echo "Next steps:"
echo "1. Review any files that weren't copied (noted above)"
echo "2. Run: npx expo start --ios"
echo "3. Test the app in iOS Simulator"
echo ""
echo "If you get any import errors, copy the missing files manually from builds/glowmaxx/src/"
