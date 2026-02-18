# App Factory Automation Setup

## Overview
This document outlines how to automate app development using Cursor, browser automation, and parallel development workflows.

---

## 1. Parallel Cursor Development

### Running Multiple Cursor Windows
```bash
# Open multiple Cursor windows for different apps
open -na "Cursor" --args "/Users/macbookpro/Documents/app factory/scripture-streak"
open -na "Cursor" --args "/Users/macbookpro/Documents/app factory/looksmax-tracker"
open -na "Cursor" --args "/Users/macbookpro/Documents/app factory/anxiety-relief"
```

### Using Cursor's Agent Mode
Each Cursor window can run an independent AI agent. Key tips:
- Use **Plan Mode** first to scope the work
- Switch to **Agent Mode** for execution
- Keep each agent focused on ONE app at a time

### Automating Cursor with AppleScript (macOS)
```applescript
-- Open Cursor and send a prompt
tell application "Cursor"
    activate
    delay 1
end tell

tell application "System Events"
    keystroke "k" using {command down} -- Open command palette
    delay 0.5
    keystroke "Build the app from scratch following APP-BUILD-SPECS.md"
    keystroke return
end tell
```

---

## 2. Browser Automation with Playwright

### Setup
```bash
npm install -D @playwright/test
npx playwright install chromium
```

### Supabase Automation Script
```javascript
// scripts/setup-supabase.js
const { chromium } = require('playwright');

async function setupSupabase(projectName) {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  // Navigate to Supabase
  await page.goto('https://supabase.com/dashboard');
  
  // Wait for login (manual step)
  console.log('Please log in to Supabase...');
  await page.waitForURL('**/dashboard/projects**', { timeout: 120000 });
  
  // Create new project
  await page.click('text=New Project');
  await page.fill('[name="name"]', projectName);
  await page.fill('[name="dbPassword"]', generatePassword());
  await page.click('text=Create new project');
  
  // Wait for project creation
  await page.waitForSelector('text=API Settings', { timeout: 120000 });
  
  // Get API keys
  await page.click('text=Settings');
  await page.click('text=API');
  
  const url = await page.locator('input[aria-label="Project URL"]').inputValue();
  const anonKey = await page.locator('input[aria-label="anon key"]').inputValue();
  
  console.log(`\nSupabase URL: ${url}`);
  console.log(`Anon Key: ${anonKey}`);
  
  // Copy SQL and run it
  const sqlContent = require('fs').readFileSync('./supabase-setup.sql', 'utf8');
  await page.click('text=SQL Editor');
  await page.click('text=New query');
  await page.locator('.monaco-editor textarea').fill(sqlContent);
  await page.click('text=Run');
  
  await browser.close();
  return { url, anonKey };
}

function generatePassword() {
  return 'Sup4b4s3_' + Math.random().toString(36).slice(2, 10) + '!';
}

setupSupabase('scripture-streak').then(console.log);
```

### RevenueCat Automation Script
```javascript
// scripts/setup-revenuecat.js
const { chromium } = require('playwright');

async function setupRevenueCat(appName) {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://app.revenuecat.com/');
  
  console.log('Please log in to RevenueCat...');
  await page.waitForURL('**/projects**', { timeout: 120000 });
  
  // Create new project
  await page.click('text=New Project');
  await page.fill('[name="name"]', appName);
  await page.click('text=Create Project');
  
  // Create iOS app
  await page.click('text=+ New App');
  await page.click('text=App Store');
  await page.fill('[name="name"]', appName + ' iOS');
  await page.fill('[name="bundleId"]', `com.yourcompany.${appName.toLowerCase().replace(/\s/g, '')}`);
  
  // Get API keys
  await page.click('text=API Keys');
  const iosKey = await page.locator('input[aria-label="iOS API Key"]').inputValue();
  
  console.log(`\nRevenueCat iOS Key: ${iosKey}`);
  
  await browser.close();
  return { iosKey };
}

setupRevenueCat('Scripture Streak').then(console.log);
```

---

## 3. Master Build Script

### Full App Factory Pipeline
```bash
#!/bin/bash
# build-app.sh - One-shot app builder

APP_NAME=$1
APP_DIR="/Users/macbookpro/Documents/app factory/${APP_NAME}"

# 1. Create project
echo "🚀 Creating ${APP_NAME}..."
npx create-expo-app@latest "${APP_DIR}" --template blank-typescript

# 2. Install dependencies
cd "${APP_DIR}"
npm install @supabase/supabase-js zustand expo-secure-store expo-haptics expo-linear-gradient react-native-gesture-handler

# 3. Copy boilerplate structure
cp -r "../scripture-streak/app" .
cp -r "../scripture-streak/src" .

# 4. Run Supabase setup (interactive)
node ../scripts/setup-supabase.js "${APP_NAME}"

# 5. Run RevenueCat setup (interactive)
node ../scripts/setup-revenuecat.js "${APP_NAME}"

# 6. Start development
npx expo start --ios
```

---

## 4. Cursor Prompt Templates

### New App Prompt
```
Build [APP_NAME] following the specifications in APP-BUILD-SPECS.md.

Requirements:
1. Use Expo Router for navigation
2. Use Supabase for auth and database
3. Use Zustand for state management
4. Implement hard paywall after onboarding
5. Follow the psychological onboarding pattern (guilt -> hope -> action)

Start by creating the project structure, then implement each screen.
```

### Debug Prompt
```
The [FEATURE] is not working. Check the console logs, review the code flow, and fix any issues.
Focus on:
1. State management updates
2. Navigation guards
3. AsyncStorage/SecureStore operations
4. API calls and error handling
```

### Security Audit Prompt
```
Perform a security audit on this React Native app:
1. Check for exposed API keys
2. Review authentication flow
3. Check for SQL injection in Supabase queries
4. Review RLS policies
5. Check for sensitive data in logs
```

---

## 5. Google Sheets Integration

### Apps Script for Data Pipeline
```javascript
// In Google Sheets > Extensions > Apps Script

function fetchAppIdeas() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const ideas = [
    // Populate from research
    ['Scripture Streak', 'Christian', 'High', '3 days', '$500/mo'],
    ['LooksMax Tracker', 'Self-improvement', 'High', '4 days', '$1000/mo'],
  ];
  
  sheet.getRange(2, 1, ideas.length, ideas[0].length).setValues(ideas);
}

function exportToBuildSpec() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const data = sheet.getDataRange().getValues();
  
  // Convert to markdown format
  let markdown = '# App Build Specs\n\n';
  data.forEach((row, i) => {
    if (i === 0) return; // Skip header
    markdown += `## ${row[0]}\n- Niche: ${row[1]}\n- Priority: ${row[2]}\n- Build Time: ${row[3]}\n\n`;
  });
  
  // Save to Drive
  DriveApp.createFile('APP-BUILD-SPECS.md', markdown, MimeType.PLAIN_TEXT);
}
```

---

## 6. Quick Commands Reference

### Development
```bash
# Start iOS simulator
npx expo start --ios --clear

# Reset everything and start fresh
rm -rf node_modules .expo && npm install && npx expo start --ios --clear

# Check for type errors
npx tsc --noEmit

# Lint code
npx eslint app/ src/ --fix
```

### Deployment
```bash
# Build for App Store
npx eas build --platform ios --profile production

# Submit to App Store
npx eas submit --platform ios

# Check build status
npx eas build:list
```

### Testing
```bash
# Run tests
npm test

# E2E tests with Detox
npx detox test --configuration ios.sim.release
```

---

## 7. Daily Workflow

### Morning (Research & Plan)
1. Check Google Sheets for app queue
2. Review competitor apps
3. Update APP-BUILD-SPECS.md

### Afternoon (Build)
1. Open 2-3 Cursor windows
2. Start building apps in parallel
3. Use prompts from CURSOR-CHEATSHEET.md

### Evening (Test & Submit)
1. Test apps on simulator
2. Fix any bugs
3. Submit to App Store via EAS

---

## 8. Monitoring

### App Store Connect
- Check review status daily
- Respond to rejections within 24h

### Revenue Tracking
- RevenueCat dashboard for subscriptions
- App Store Connect for downloads

### Analytics (Add Later)
- Mixpanel or Amplitude for user behavior
- Firebase Crashlytics for crash reports
