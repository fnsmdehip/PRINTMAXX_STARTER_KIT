---
title: "Playwright Instagram automation complete guide 2026 | PrintMaxx"
description: "Mobile proxies required. Session management critical. Follow/unfollow still works. Here's the setup that avoids bans."
keywords: ["Playwright Instagram", "Instagram automation", "Instagram bot", "Playwright social media", "Instagram growth"]
author: "PrintMaxx Team"
date: "2026-01-22"
published: true
canonical: "/longtail/playwright-instagram-automation-complete-guide-2026"
---

# Playwright Instagram automation complete guide 2026

## Quick Answer

Use Playwright with mobile proxies (4G/5G). Warm account for 2 weeks before automation. Limit actions to 150/day split across 12 hours. Follow/unfollow, DM automation, and story viewing still work. Comment/like automation is riskier. Cost: $75/mo (Soax mobile proxies $65 + Playwright free).

Don't use datacenter proxies. Don't automate from home IP. Don't exceed 200 actions/day. Instagram detects these and bans accounts.

## Why Instagram Automation is Harder in 2026

Instagram's detection improved:
- Session fingerprinting (detects headless browsers)
- Action pattern analysis (detects bot-like timing)
- IP reputation tracking (datacenter IPs flagged)
- Device consistency checks (same device = safer)

**What still works:**
- Follow/unfollow strategy (with limits)
- Story viewing automation
- DM sequences (with personalization)
- Profile visiting (builds presence)

**What's risky:**
- Mass liking (>100/day triggers review)
- Mass commenting (detected as spam)
- Story replies (high ban rate)

## The Safe Automation Stack

### Layer 1: Proxies

**Soax Mobile Proxies - $65/mo for 2GB**

4G/5G mobile IPs rotate from real devices. Instagram sees normal mobile traffic.

Why mobile proxies specifically:
- Instagram expects mobile traffic (80% of users are mobile)
- IP reputation is clean
- Rotation looks like user switching towers
- Harder for Instagram to detect

**Setup:**

1. Buy Soax mobile proxies (USA recommended)
2. Choose "rotating" mode (IP changes every 5 minutes)
3. Whitelist your server IP
4. Get proxy credentials

**Configuration in Playwright:**

```javascript
const browser = await playwright.chromium.launch({
  proxy: {
    server: 'http://gate.soax.com:80',
    username: 'your_soax_username',
    password: 'your_soax_password'
  }
});
```

**Don't use:**
- Datacenter proxies (banned in hours)
- Free proxies (all blacklisted)
- Home IP (risks main account)
- VPN (Instagram detects VPN IPs)

**Cost comparison:**

| Proxy Type | Cost | Detection Rate | Recommendation |
|------------|------|----------------|----------------|
| Soax Mobile | $65/mo | Low (5%) | Use this |
| Datacenter | $5/mo | High (80%) | Avoid |
| Residential | $25/mo | Medium (30%) | OK for testing |
| Free | $0 | Very High (95%) | Never use |

### Layer 2: Session Management

**Instagram tracks device fingerprint.** Breaking this triggers bans.

**Critical settings:**

```javascript
const context = await browser.newContext({
  userAgent: 'Instagram 275.0.0.27.98 Android (28/9; 420dpi; 1080x2260; OnePlus; ONEPLUS A6010; OnePlus6T; qcom; en_US; 422626547)',
  viewport: { width: 393, height: 851 }, // iPhone 14 Pro
  deviceScaleFactor: 3,
  isMobile: true,
  hasTouch: true,
  locale: 'en-US',
  timezoneId: 'America/New_York'
});
```

**Save session cookies:**

```javascript
// After login, save cookies
const cookies = await context.cookies();
await fs.writeFile('instagram_session.json', JSON.stringify(cookies));

// Next run, load cookies (skip login)
const savedCookies = JSON.parse(await fs.readFile('instagram_session.json'));
await context.addCookies(savedCookies);
```

**Why this matters:**

Instagram flags frequent logins. Reusing session = 1 login per month instead of daily logins.

### Layer 3: Human-Like Delays

**Random delays between actions:**

```javascript
function randomDelay(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

// Between actions
await page.waitForTimeout(randomDelay(2000, 5000));

// Between page navigations
await page.waitForTimeout(randomDelay(3000, 8000));

// After following someone
await page.waitForTimeout(randomDelay(10000, 20000));
```

**Why random delays:**

Bots use fixed delays (exactly 3 seconds between actions). Humans vary (2-7 seconds randomly).

Instagram detects fixed-interval patterns.

### Layer 4: Action Limits

**Safe daily limits:**

| Action | Daily Limit | Hourly Limit | Notes |
|--------|-------------|--------------|-------|
| Follows | 150 | 15 | New accounts: 50/day |
| Unfollows | 150 | 15 | Same as follows |
| Likes | 100 | 12 | Riskier than follows |
| Comments | 20 | 3 | High detection rate |
| DMs | 50 | 8 | Personalize or get flagged |
| Story views | 200 | 25 | Safest action |

**Implementation:**

```javascript
const actions = {
  follows: 0,
  unfollows: 0,
  likes: 0
};

const limits = {
  follows: 150,
  unfollows: 150,
  likes: 100
};

async function followUser(username) {
  if (actions.follows >= limits.follows) {
    console.log('Daily follow limit reached');
    return;
  }

  // Follow logic here
  actions.follows++;
}
```

## Complete Follow/Unfollow Bot Script

```javascript
const { chromium } = require('playwright');
const fs = require('fs').promises;

const config = {
  username: 'your_username',
  password: 'your_password',
  targetHashtag: 'solopreneur', // Target audience
  followsPerDay: 120,
  unfollowsPerDay: 100
};

async function instagramBot() {
  // Launch with proxy
  const browser = await chromium.launch({
    headless: true,
    proxy: {
      server: 'http://gate.soax.com:80',
      username: 'your_soax_username',
      password: 'your_soax_password'
    }
  });

  // Mobile context
  const context = await browser.newContext({
    userAgent: 'Instagram 275.0.0.27.98 Android',
    viewport: { width: 393, height: 851 },
    isMobile: true,
    hasTouch: true
  });

  const page = await context.newPage();

  // Load saved session or login
  try {
    const cookies = JSON.parse(await fs.readFile('session.json', 'utf-8'));
    await context.addCookies(cookies);
    await page.goto('https://www.instagram.com/');

    // Check if still logged in
    await page.waitForSelector('[aria-label="Home"]', { timeout: 5000 });
    console.log('Session restored');
  } catch {
    // Need to login
    await login(page);
    const cookies = await context.cookies();
    await fs.writeFile('session.json', JSON.stringify(cookies));
  }

  // Main automation loop
  await followUsersFromHashtag(page, config.targetHashtag);
  await unfollowOldFollows(page);

  await browser.close();
}

async function login(page) {
  await page.goto('https://www.instagram.com/accounts/login/');
  await page.waitForTimeout(randomDelay(2000, 4000));

  await page.fill('input[name="username"]', config.username);
  await page.waitForTimeout(randomDelay(500, 1500));

  await page.fill('input[name="password"]', config.password);
  await page.waitForTimeout(randomDelay(500, 1500));

  await page.click('button[type="submit"]');
  await page.waitForTimeout(randomDelay(3000, 6000));

  // Handle "Save Login Info" popup
  try {
    await page.click('button:has-text("Not Now")', { timeout: 5000 });
  } catch {}

  // Handle "Turn on Notifications" popup
  try {
    await page.click('button:has-text("Not Now")', { timeout: 5000 });
  } catch {}
}

async function followUsersFromHashtag(page, hashtag) {
  await page.goto(`https://www.instagram.com/explore/tags/${hashtag}/`);
  await page.waitForTimeout(randomDelay(3000, 5000));

  // Get top posts
  const posts = await page.$$('article a[href^="/p/"]');

  let followed = 0;

  for (let i = 0; i < posts.length && followed < config.followsPerDay; i++) {
    await posts[i].click();
    await page.waitForTimeout(randomDelay(2000, 4000));

    // Get username
    const username = await page.$eval(
      'article header a',
      el => el.textContent
    );

    // Check if already following
    const followButton = await page.$('button:has-text("Follow")');

    if (followButton) {
      await followButton.click();
      console.log(`Followed: ${username}`);

      // Save to follow list (for later unfollow)
      await saveFollow(username);

      followed++;
      await page.waitForTimeout(randomDelay(10000, 20000)); // Long delay after follow
    }

    // Close post modal
    await page.click('svg[aria-label="Close"]');
    await page.waitForTimeout(randomDelay(2000, 4000));

    // Random actions between follows
    if (Math.random() > 0.7) {
      await viewStories(page, 2); // View 2 random stories
    }
  }

  return followed;
}

async function unfollowOldFollows(page) {
  // Load follows from 7 days ago
  const followsToUnfollow = await getOldFollows(7);

  let unfollowed = 0;

  for (const username of followsToUnfollow) {
    if (unfollowed >= config.unfollowsPerDay) break;

    await page.goto(`https://www.instagram.com/${username}/`);
    await page.waitForTimeout(randomDelay(2000, 4000));

    const followingButton = await page.$('button:has-text("Following")');

    if (followingButton) {
      await followingButton.click();
      await page.waitForTimeout(randomDelay(1000, 2000));

      // Confirm unfollow
      await page.click('button:has-text("Unfollow")');
      console.log(`Unfollowed: ${username}`);

      unfollowed++;
      await page.waitForTimeout(randomDelay(8000, 15000));
    }
  }

  return unfollowed;
}

async function viewStories(page, count) {
  await page.goto('https://www.instagram.com/');
  await page.waitForTimeout(randomDelay(2000, 3000));

  const storyButtons = await page.$$('canvas[role="button"]');

  for (let i = 0; i < Math.min(count, storyButtons.length); i++) {
    await storyButtons[i].click();
    await page.waitForTimeout(randomDelay(5000, 10000)); // Watch story

    // Next story
    await page.click('button[aria-label="Next"]');
    await page.waitForTimeout(randomDelay(3000, 5000));
  }

  // Close stories
  await page.click('svg[aria-label="Close"]');
}

// Helper functions

async function saveFollow(username) {
  const follows = await loadFollows();
  follows[username] = new Date().toISOString();
  await fs.writeFile('follows.json', JSON.stringify(follows, null, 2));
}

async function loadFollows() {
  try {
    return JSON.parse(await fs.readFile('follows.json', 'utf-8'));
  } catch {
    return {};
  }
}

async function getOldFollows(daysAgo) {
  const follows = await loadFollows();
  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - daysAgo);

  return Object.entries(follows)
    .filter(([_, date]) => new Date(date) < cutoffDate)
    .map(([username, _]) => username);
}

function randomDelay(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

// Run bot
instagramBot();
```

## Account Warming Protocol

**Never automate a fresh account immediately.** Instagram flags new accounts that automate.

**2-week warmup schedule:**

**Days 1-3:**
- Manual use only (phone app)
- Follow 10 accounts
- Like 20 posts
- Comment on 3 posts
- Post 1 photo

**Days 4-7:**
- Follow 20 accounts/day (manual or semi-automated)
- Like 30 posts/day
- View 30 stories/day
- Post 1-2 times

**Days 8-14:**
- Follow 50 accounts/day
- Like 50 posts/day
- View 50 stories/day
- Post 2-3 times

**Day 15+:**
- Start full automation
- Ramp to 150 follows/day over 7 days

## DM Automation (Advanced)

**Automated DMs work if personalized.**

Bad DM (gets flagged):
"Hey! Check out my page!"

Good DM (passes filters):
"Hey [name], saw your post about [specific topic]. I'm working on something similar - [brief personal detail]. Would love to connect!"

**Playwright DM script:**

```javascript
async function sendDM(page, username, message) {
  await page.goto(`https://www.instagram.com/${username}/`);
  await page.waitForTimeout(randomDelay(2000, 4000));

  // Click "Message" button
  await page.click('button:has-text("Message")');
  await page.waitForTimeout(randomDelay(2000, 3000));

  // Type message (with human-like typing speed)
  const messageBox = await page.$('textarea[placeholder="Message..."]');

  for (const char of message) {
    await messageBox.type(char);
    await page.waitForTimeout(randomDelay(50, 150)); // Type like human
  }

  await page.waitForTimeout(randomDelay(1000, 2000));

  // Send
  await page.click('button:has-text("Send")');
  await page.waitForTimeout(randomDelay(3000, 6000));
}

// Personalize DMs
async function sendPersonalizedDM(page, username) {
  // Get recent post info for personalization
  await page.goto(`https://www.instagram.com/${username}/`);
  const recentPost = await page.$eval(
    'article a[href^="/p/"] img',
    el => el.getAttribute('alt')
  );

  const message = `Hey ${username}, just saw your post about "${recentPost.slice(0, 30)}". Really resonated with me because I'm working on something similar. Would love to hear more about your journey!`;

  await sendDM(page, username, message);
}
```

**DM limits:**

New accounts: 20 DMs/day
Warmed accounts: 50 DMs/day

Exceed this = temporary DM ban (24-48 hours).

## Story Viewing Strategy

**Safest automation tactic.** Low detection rate, builds presence.

**Why it works:**
- Viewing story shows interest
- Account sees you in viewer list
- Often leads to follow-back or engagement
- Instagram doesn't flag story viewing heavily

**Automated story viewer:**

```javascript
async function viewStoriesFromHashtag(page, hashtag, count) {
  await page.goto(`https://www.instagram.com/explore/tags/${hashtag}/`);
  await page.waitForTimeout(randomDelay(3000, 5000));

  // Find accounts with active stories
  const storyRings = await page.$$('canvas[role="button"]');

  let viewed = 0;

  for (const ring of storyRings) {
    if (viewed >= count) break;

    await ring.click();
    await page.waitForTimeout(randomDelay(5000, 8000)); // Watch story

    // Skip to next account's story
    await page.click('button[aria-label="Next"]');
    await page.waitForTimeout(randomDelay(2000, 3000));

    viewed++;
  }

  console.log(`Viewed ${viewed} stories`);
}
```

**Daily limit:** 200 story views (safe)

## Common Detection Triggers to Avoid

### Trigger 1: Consistent Timing

**Don't run automation at same time every day.**

Bad: Every day at 9am sharp
Good: Random time between 8am-11am, different each day

```javascript
function getRandomStartTime() {
  const hour = randomDelay(8, 23); // 8am to 11pm
  const minute = randomDelay(0, 59);

  const now = new Date();
  const start = new Date(now);
  start.setHours(hour, minute, 0, 0);

  return start - now; // Milliseconds until start
}

// Schedule random start
setTimeout(() => {
  instagramBot();
}, getRandomStartTime());
```

### Trigger 2: Perfect Intervals

**Don't follow every 10 seconds exactly.**

Bad: Follow at :00, :10, :20, :30...
Good: Follow at :03, :17, :29, :48...

Use `randomDelay()` function shown earlier.

### Trigger 3: Zero Engagement Beyond Actions

**Bots only follow. Humans browse, search, view profiles.**

Add random actions:
- View 3-5 explore page posts (don't like, just view)
- Search for random hashtags
- Visit your own profile occasionally
- Check DMs and notifications

```javascript
async function randomHumanActivity(page) {
  const activities = [
    async () => {
      await page.goto('https://www.instagram.com/explore/');
      await page.waitForTimeout(randomDelay(5000, 10000));
    },
    async () => {
      await page.goto(`https://www.instagram.com/${config.username}/`);
      await page.waitForTimeout(randomDelay(3000, 6000));
    },
    async () => {
      await page.click('svg[aria-label="Search"]');
      await page.fill('input[placeholder="Search"]', 'fitness');
      await page.waitForTimeout(randomDelay(2000, 4000));
    }
  ];

  const randomActivity = activities[Math.floor(Math.random() * activities.length)];
  await randomActivity();
}

// Run between automation tasks
await followUsers(page);
await randomHumanActivity(page);
await unfollowUsers(page);
await randomHumanActivity(page);
```

### Trigger 4: Headless Browser Fingerprint

**Instagram detects headless Chrome.**

Add stealth plugin:

```bash
npm install playwright-extra puppeteer-extra-plugin-stealth
```

```javascript
const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();

chromium.use(stealth);

const browser = await chromium.launch();
```

This masks headless signatures.

## Handling Bans and Blocks

### Action Block (Temporary)

**Symptoms:** "Try again later" message when following/liking

**Duration:** 24 hours to 14 days

**Recovery:**
- Stop all automation immediately
- Use account manually (phone only) for 3-5 days
- Don't login from bot IP
- Restart automation at 50% limits after block lifts

### Permanent Ban

**Symptoms:** Account disabled, can't log in

**Prevention:**
- Never exceed 200 actions/day
- Always use mobile proxies
- Warm new accounts properly
- Don't automate multiple accounts from same IP

**Recovery:**
- Appeal (rarely works)
- Create new account with different email/phone
- Warm for 3 weeks before automating

## Cost Breakdown

| Item | Monthly Cost | Purpose |
|------|--------------|---------|
| Soax mobile proxies (2GB) | $65 | Clean IPs |
| Playwright | Free | Automation |
| Server (DigitalOcean) | $6 | Run 24/7 |
| Phone verification (if needed) | $2 | SMS verification |
| **Total** | **$73/mo** | Per account |

**ROI calculation:**

150 follows/day = 4,500/month
10% follow-back rate = 450 new followers/month

If 1% convert to customer at $100 value = $450/month revenue

Break-even at 1 conversion every 6 months.

## Scaling to Multiple Accounts

**Run separate browser contexts per account:**

```javascript
async function runMultipleAccounts(accounts) {
  for (const account of accounts) {
    const browser = await chromium.launch({
      proxy: account.proxy // Different proxy per account
    });

    // Run bot for this account
    await instagramBot(browser, account);

    await browser.close();

    // Long delay between accounts
    await sleep(randomDelay(300000, 600000)); // 5-10 minutes
  }
}
```

**Critical rules for multiple accounts:**
- Different proxy per account (don't share IPs)
- Different phone number per account
- Different email per account
- Stagger automation times (don't run all at once)
- Keep accounts in separate niches (don't link them)

**Recommended scale:**
- Beginner: 1 account
- Intermediate: 3 accounts
- Advanced: 5-10 accounts max

More than 10 accounts = high management overhead.

## Monitoring and Logging

**Track metrics to optimize:**

```javascript
const metrics = {
  follows: 0,
  unfollows: 0,
  followBacks: 0,
  blocks: 0,
  startTime: Date.now()
};

async function logMetrics() {
  await fs.appendFile('metrics.log', JSON.stringify({
    date: new Date().toISOString(),
    ...metrics
  }) + '\n');
}

// Call at end of each run
await logMetrics();
```

**Watch for warning signs:**
- Follow-back rate drops below 5% → Change targeting
- Action blocks increase → Reduce limits
- Engagement decreases → Improve content

## Legal and Ethical Considerations

**Instagram Terms of Service:**

Automation violates TOS. You can be banned.

**Risk acceptance:**

Use throwaway accounts for testing. Don't automate your main account.

**Ethical use:**

Don't:
- Send spam DMs
- Comment spam
- Mass unfollow without engagement

Do:
- Target relevant audiences
- Provide value in DMs
- Follow accounts you actually find interesting

## Alternatives to Full Automation

**Manual + Tools (safer):**

Use Instagram app + spreadsheet tracking:
- Manually follow 50/day
- Track in Google Sheets
- Unfollow after 7 days if no follow-back

Takes 20 minutes/day vs full automation but zero risk.

**Paid services (expensive but hands-off):**

- Kicksta: $49/mo (they automate for you)
- Growthoid: $39/mo (managed service)
- Inflact: $29/mo (browser extension)

More expensive but they handle IP/proxy/limits.

## The Bottom Line

Instagram automation still works in 2026 with mobile proxies and human-like behavior.

Follow/unfollow strategy: 4,500 actions/month = ~400 new followers at 10% follow-back rate.

Cost: $73/mo per account. Returns depend on your niche and conversion rate.

Use for lead generation or audience building. Don't rely solely on automation (content quality still matters most).

Start with one account. Test for 30 days. Scale if profitable.
