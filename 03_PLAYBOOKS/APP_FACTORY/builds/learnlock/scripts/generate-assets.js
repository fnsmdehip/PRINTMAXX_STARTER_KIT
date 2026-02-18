#!/usr/bin/env node
/**
 * Generate placeholder assets for LearnLock app
 * Run: node scripts/generate-assets.js
 */

const fs = require('fs');
const path = require('path');

const assetsDir = path.join(__dirname, '..', 'assets');

// Ensure assets directory exists
if (!fs.existsSync(assetsDir)) {
  fs.mkdirSync(assetsDir, { recursive: true });
}

// Create a simple 1x1 PNG with the primary color (#4F46E5)
// This is a minimal valid PNG file
const createPlaceholderPng = (width, height, filename) => {
  // For simplicity, create a small PNG header that represents a colored pixel
  // In production, you would use a proper image library like sharp or jimp

  const filePath = path.join(assetsDir, filename);

  // Minimal PNG for placeholder (will need to be replaced with actual assets)
  console.log(`Placeholder needed: ${filePath} (${width}x${height})`);
  console.log(`  → Download from: https://via.placeholder.com/${width}x${height}/4F46E5/FFFFFF?text=LL`);
};

// Required assets
const assets = [
  { width: 1024, height: 1024, filename: 'icon.png' },
  { width: 1284, height: 2778, filename: 'splash.png' },
  { width: 1024, height: 1024, filename: 'adaptive-icon.png' },
  { width: 48, height: 48, filename: 'favicon.png' },
  { width: 96, height: 96, filename: 'notification-icon.png' },
];

console.log('\\n=== LearnLock Asset Generation ===\\n');
console.log('Required placeholder assets for development:\\n');

assets.forEach(asset => {
  createPlaceholderPng(asset.width, asset.height, asset.filename);
});

console.log('\\n=== Quick Setup ===\\n');
console.log('For development, you can use these commands to download placeholders:\\n');
console.log('curl -o assets/icon.png "https://via.placeholder.com/1024x1024/4F46E5/FFFFFF?text=LL"');
console.log('curl -o assets/splash.png "https://via.placeholder.com/1284x2778/4F46E5/FFFFFF?text=LearnLock"');
console.log('curl -o assets/adaptive-icon.png "https://via.placeholder.com/1024x1024/4F46E5/FFFFFF?text=LL"');
console.log('curl -o assets/favicon.png "https://via.placeholder.com/48x48/4F46E5/FFFFFF?text=LL"');
console.log('curl -o assets/notification-icon.png "https://via.placeholder.com/96x96/4F46E5/FFFFFF?text=LL"');
console.log('\\nOr generate proper assets using: npx @expo/image-utils create-icons\\n');
