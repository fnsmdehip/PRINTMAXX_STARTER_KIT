# Troubleshooting: Subscription not working

**Symptoms:** Customer paid but app shows free tier, features locked, or "upgrade" buttons still visible.

---

## Quick diagnosis

Ask the customer:
1. What email did you use to purchase?
2. What email are you logged in with?
3. Where did you purchase? (Website, iOS App Store, Google Play)

Most common cause: **Email mismatch between purchase and login.**

---

## Step 1: Verify purchase exists

### Website/Stripe purchases
1. Open Stripe Dashboard > Customers
2. Search by email
3. Check for active subscription

### iOS App Store purchases
1. Ask customer to check: Settings > [Their Name] > Subscriptions
2. Verify our app shows as active
3. Note: We can't see App Store purchases directly

### Google Play purchases
1. Ask customer to check: Play Store > Account > Payments & subscriptions
2. Verify our app shows as active
3. Check Play Console if we have access

---

## Step 2: Common fixes

### Email mismatch (most common)
Customer bought with email A, logged in with email B.

**Fix:**
- Have them log out and log in with the correct email
- Or: Manually merge accounts in admin (if you have access)

### Sync delay
Payment processed but app hasn't synced yet.

**Fix:**
- Force refresh: Pull down on main screen or Cmd+R
- Log out and back in
- Wait 5 minutes and try again

### Cache issue
Old subscription status cached locally.

**Fix:**
- Clear app cache: Settings > Advanced > Clear Cache
- Delete and reinstall app
- Clear browser cache and cookies if web

### Restore purchase (iOS/Android)
Purchase linked to device but not syncing.

**Fix:**
- iOS: Settings > [App] > Restore Purchases
- Android: Menu > Settings > Restore Purchases
- Make sure logged into same Apple ID/Google account used for purchase

---

## Step 3: Manual fix (admin tools)

If customer is stuck and you've verified they paid:

1. Find user in admin dashboard
2. Check their subscription_status field
3. If null or "free" but payment confirmed:
   - Set subscription_status = "premium"
   - Set subscription_source = "[stripe/ios/android]"
   - Set subscription_started = [purchase date]
4. Have customer log out and back in

---

## Step 4: Escalate if needed

Escalate to engineering when:
- Payment confirmed but manual fix doesn't work
- Multiple users reporting same issue (possible bug)
- Apple/Google webhook might be failing

Include in escalation:
- User ID
- Transaction ID / receipt
- Steps already tried
- Timestamps of purchase and issue report

---

## Prevention notes

Common reasons this happens:
- User forgot which email they used
- Sign-in with Apple created a private relay email
- Family sharing complications (iOS)
- Multiple Google accounts on device (Android)

For repeat issues, suggest customer creates a dedicated email for app purchases.
