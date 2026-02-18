# StepUnlock Asset Requirements

Before publishing, create the following assets:

## App Icon (icon.png)
- Size: 1024x1024 pixels
- Format: PNG (no alpha/transparency for iOS)
- Design: Walking figure or footsteps with green accent (#4CAF50)
- Use a tool like Figma, Canva, or AI image generators

## Splash Screen (splash.png)
- Size: 1284x2778 pixels (or use resizeMode: "contain")
- Format: PNG
- Background color matches app.json: #4CAF50
- Simple centered logo/icon

## Android Adaptive Icon (adaptive-icon.png)
- Size: 1024x1024 pixels
- Format: PNG with transparency
- Foreground only (background color set in app.json)

## Web Favicon (favicon.png)
- Size: 48x48 pixels
- Format: PNG

## Quick Generation Options

### Option 1: AI Image Generator
Use Midjourney, DALL-E, or similar with prompt:
"App icon for a fitness step tracking app, walking figure silhouette, minimal design, green accent color, rounded corners, iOS app icon style"

### Option 2: Figma Template
1. Use a free app icon template from Figma Community
2. Customize with walking/step theme
3. Export at required sizes

### Option 3: Online Tools
- https://appicon.co - Generate all icon sizes from one image
- https://www.canva.com - Create icons with templates
- https://makeappicon.com - Generate icon sets

## Placeholder Testing
For development/testing in Expo Go, you can create simple colored squares:

```bash
# Using ImageMagick (if installed)
convert -size 1024x1024 xc:#4CAF50 icon.png
convert -size 1284x2778 xc:#4CAF50 splash.png
convert -size 1024x1024 xc:#4CAF50 adaptive-icon.png
convert -size 48x48 xc:#4CAF50 favicon.png
```

Or use this online tool: https://placeholder.com
