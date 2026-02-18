# Troubleshooting: App crashing

**Symptoms:** App closes immediately on launch, crashes during use, freezes then closes, black screen then exit.

---

## Quick diagnosis

Ask the customer:
1. When does it crash? (Launch, specific action, random)
2. Device model and OS version
3. How much free storage do you have?
4. Did it start after an update?

---

## Crash on launch

### Step 1: Basic restart
1. Force quit the app completely
   - iOS: Swipe up from bottom, swipe app away
   - Android: Recent apps, swipe away or tap X
2. Restart the device
3. Try opening app again

### Step 2: Reinstall
If restart doesn't work:
1. Delete the app
2. Restart device
3. Reinstall from App Store / Play Store
4. Log in fresh

Data syncs from cloud. Nothing lost.

### Step 3: Check OS compatibility
- Minimum iOS: [VERSION]
- Minimum Android: [VERSION]

If customer is on older OS:
- Suggest updating if possible
- If device can't update, we may not be able to help

### Step 4: Storage check
App needs ~200MB free to run properly.

Low storage causes random crashes:
- iOS: Settings > General > iPhone Storage
- Android: Settings > Storage

---

## Crash during specific action

### Identify the trigger
"What were you doing right before it crashed?"

Common triggers:
- Opening large files
- Loading many items at once
- Using camera/photo features
- Switching between apps

### Action-specific fixes

**Crash when opening files:**
- File might be corrupted
- Try with different file
- Check file format is supported

**Crash when loading content:**
- Too many items in one view
- Archive old content
- Use filters to reduce what's displayed

**Crash when using camera:**
- Camera permissions revoked
- Check Settings > [App] > Camera > ON
- Other app using camera

**Crash when switching apps:**
- Memory issue on device
- Close other apps
- Restart device

---

## Random crashes

### Check for patterns
Ask customer to note:
- Time of day crashes happen
- What they were doing
- Any error messages (even brief)

### Common causes

**Memory leak:**
- App uses more memory over time
- Fix: Force quit and restart app daily until we fix it
- Escalate to engineering with user ID

**Network instability:**
- Poor wifi/cellular causes timeouts
- Timeouts sometimes cause crashes
- Test on different network

**Background refresh conflicts:**
- iOS: Settings > General > Background App Refresh
- Try toggling off for our app
- See if crashes continue

---

## Collecting crash data

When basic fixes don't work, need crash logs.

### iOS
1. Settings > Privacy & Security > Analytics & Improvements > Analytics Data
2. Look for entries starting with [APP NAME]
3. Share via email

### Android
1. Settings > About > Build number (tap 7 times to enable Developer Options)
2. Developer Options > Bug report
3. Share via email

### Ask customer to enable
"Can you turn on 'Share with App Developers' in your device settings? This sends us crash reports automatically."

- iOS: Settings > Privacy > Analytics > Share with App Developers
- Android: Play Store > Settings > General > Help improve Play Store

---

## Escalation criteria

Escalate to engineering when:
- 3+ users report same crash scenario
- Crash happens on supported devices after basic troubleshooting
- Crash logs show pattern

Include:
- Device model and OS
- Steps to reproduce (if known)
- Crash logs or error messages
- How many users affected

---

## Quick reference: What to try

| Crash timing | First try | Then try |
|--------------|-----------|----------|
| On launch | Restart > Reinstall | Check OS/storage |
| Specific action | Identify trigger | Permission check |
| Random | Restart device | Clear cache, check memory |
| After update | Reinstall | Wait for hotfix |
