# Customer Support Automation Guide

Comprehensive guide for automating customer support across apps, email, and app store reviews.

**Related Docs:**
- Crisis response: `OPS/CRISIS_RESPONSE_PLAYBOOK.md`
- Existing playbook: `OPS/SUPPORT/SUPPORT_PLAYBOOK.md`
- Response templates: `OPS/SUPPORT/canned_responses/`
- Escalation rules: `OPS/SUPPORT/escalation_matrix.md`

---

## Quick Start: Solo Founder Setup

**Week 1 - Foundation:**
1. Set up Crisp (free tier) for in-app chat
2. Create support@[domain].com forwarded to Gmail
3. Save canned responses in Gmail templates
4. Respond to all reviews within 24 hours

**Week 2 - Automation:**
1. Enable Crisp chatbot for FAQs
2. Set up auto-responder for common emails
3. Create review monitoring alerts
4. Add FAQ section to app settings

**Cost at this stage:** $0/month

---

## Support Tool Comparison

### Tier 1: Free/Budget (0-500 users)

| Tool | Price | Best For | Limitations |
|------|-------|----------|-------------|
| **Crisp** | Free to $25/mo | In-app chat, small teams | Limited automation on free |
| **Tawk.to** | Free | Live chat widget | No email integration |
| **Gmail + Canned Responses** | Free | Email support | Manual, no tracking |
| **Notion** | Free | Knowledge base | Not customer-facing |

**Recommended:** Crisp (free) + Gmail templates + manual review tracking

### Tier 2: Growth ($25-100/month, 500-5000 users)

| Tool | Price | Best For | Key Features |
|------|-------|----------|--------------|
| **Crisp Pro** | $25/mo | Chat + email unified | Chatbot, canned responses |
| **Help Scout** | $25/user/mo | Email-focused support | Shared inbox, docs |
| **Freshdesk** | $18/agent/mo | Full helpdesk | Ticketing, automation |

**Recommended:** Crisp Pro or Help Scout for single-founder with growing volume

### Tier 3: Scale ($100-500/month, 5000+ users)

| Tool | Price | Best For | AI Features |
|------|-------|----------|-------------|
| **Intercom** | $74+/mo | In-app messaging | Fin AI bot ($0.99/resolution) |
| **Zendesk** | $55/agent/mo | Enterprise support | Advanced AI, Answer Bot |
| **Freshdesk** | $79/agent/mo | Full automation | Freddy AI |

**Recommended:** Intercom if heavy in-app use, Zendesk if high email volume

### AI-First Options (New Category)

| Tool | Price | Capability |
|------|-------|------------|
| **Intercom Fin** | $0.99/resolved | GPT-powered, learns from docs |
| **AskAI** | $19/mo starter | Train on your content |
| **Chatbase** | $19/mo starter | Custom ChatGPT for support |
| **Dante AI** | $24/mo starter | Multilingual, voice support |

---

## In-App Support Setup

### Option 1: Crisp (Recommended for Apps)

**Why Crisp:**
- Free tier is generous
- Native iOS/Android SDKs
- Chatbot included
- Integrates with Slack

**iOS Integration (React Native):**

```javascript
// Install
npm install react-native-crisp-chat-sdk

// App.js or support screen
import CrispChat from 'react-native-crisp-chat-sdk';

// Initialize in useEffect
useEffect(() => {
  CrispChat.configure('YOUR_WEBSITE_ID');

  // Optional: Set user info
  CrispChat.setUserEmail(user.email);
  CrispChat.setUserNickname(user.name);

  // Optional: Add user context
  CrispChat.setSessionData({
    plan: user.plan,
    app_version: '1.0.0',
    user_id: user.id
  });
}, []);

// Open chat
const openSupport = () => {
  CrispChat.show();
};
```

**Expo Integration:**

```javascript
// For Expo, use web-based approach
import { WebView } from 'react-native-webview';

const SupportScreen = () => {
  const crispHTML = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <script type="text/javascript">
        window.$crisp=[];
        window.CRISP_WEBSITE_ID="YOUR_WEBSITE_ID";
        (function(){
          d=document;
          s=d.createElement("script");
          s.src="https://client.crisp.chat/l.js";
          s.async=1;
          d.getElementsByTagName("head")[0].appendChild(s);
        })();
        // Auto-open chat
        window.$crisp.push(['do', 'chat:open']);
      </script>
    </head>
    <body style="margin:0;padding:0;"></body>
    </html>
  `;

  return (
    <WebView
      source={{ html: crispHTML }}
      style={{ flex: 1 }}
    />
  );
};
```

### Option 2: Native Help Center

For simpler needs, build a native FAQ/help section:

```javascript
// HelpScreen.js
import { ScrollView, TouchableOpacity, Text, View } from 'react-native';
import { Linking } from 'react-native';

const FAQs = [
  {
    question: "How do I cancel my subscription?",
    answer: "Go to Settings > Subscription > Cancel. Your access continues until the end of your billing period."
  },
  {
    question: "How do I get a refund?",
    answer: "Email support@[domain].com within 7 days of purchase. Include your receipt."
  },
  {
    question: "Why isn't my premium feature working?",
    answer: "Try: 1) Sign out and back in, 2) Restore purchases in Settings, 3) Check your subscription is active in App Store."
  }
];

const HelpScreen = () => {
  const [expanded, setExpanded] = useState({});

  return (
    <ScrollView style={{ padding: 16 }}>
      <Text style={styles.title}>Help Center</Text>

      {FAQs.map((faq, index) => (
        <TouchableOpacity
          key={index}
          onPress={() => setExpanded(prev => ({...prev, [index]: !prev[index]}))}
        >
          <View style={styles.faqItem}>
            <Text style={styles.question}>{faq.question}</Text>
            {expanded[index] && (
              <Text style={styles.answer}>{faq.answer}</Text>
            )}
          </View>
        </TouchableOpacity>
      ))}

      <TouchableOpacity
        style={styles.contactButton}
        onPress={() => Linking.openURL('mailto:support@[domain].com')}
      >
        <Text>Still need help? Contact us</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};
```

### Option 3: Intercom (Premium)

**When to use Intercom:**
- 5000+ users
- Need AI resolution
- Budget for $74+/mo + $0.99/AI resolution

```javascript
// React Native Intercom
npm install @intercom/intercom-react-native

// Initialize
import Intercom from '@intercom/intercom-react-native';

Intercom.setApiKey('YOUR_API_KEY', 'YOUR_APP_ID');

// Identify user
Intercom.registerIdentifiedUser({ userId: user.id });
Intercom.updateUser({
  email: user.email,
  name: user.name,
  customAttributes: {
    plan: user.plan,
    subscription_status: user.subscriptionStatus
  }
});

// Open messenger
Intercom.present();
```

---

## Email Support Automation

### Gmail Setup (Budget)

**1. Create Email Address:**
- support@[domain].com
- Route to Gmail or Google Workspace

**2. Set Up Filters:**
```
Filter 1: "refund" OR "money back" → Label: URGENT, Star
Filter 2: "can't log in" OR "password" → Label: Account
Filter 3: "bug" OR "crash" OR "error" → Label: Technical
Filter 4: "feature" OR "suggestion" → Label: Feedback
```

**3. Create Canned Responses:**
Settings > Advanced > Enable Templates

**4. Auto-Responder (Vacation Responder):**
```
Subject: We got your message

Thanks for reaching out. We typically respond within 24 hours (business days).

While you wait, check our FAQ: [link]

Common fixes:
- Subscription issues: Sign out/in or restore purchases
- Crashes: Update to latest version
- Billing: Check App Store subscriptions

We'll be in touch soon.
```

### Help Scout Setup (Growth)

**Why Help Scout:**
- Clean shared inbox
- Built-in knowledge base
- $25/user/month
- Great for email-heavy support

**Automation Workflows:**

```yaml
# Auto-assign subscription issues
Workflow: Subscription Priority
Trigger: Contains "subscription" OR "premium" OR "pro"
Action:
  - Assign to: [You]
  - Tag: subscription
  - Priority: High

# Auto-reply to feature requests
Workflow: Feature Request Auto-Reply
Trigger: Contains "feature" OR "please add" OR "would be great if"
Action:
  - Tag: feature-request
  - Auto-reply: feature_request_template
  - Priority: Low
```

**Saved Replies to Create:**

1. **Subscription Active** - "Your subscription is active. Try signing out..."
2. **Refund Approved** - "Refund processed. 3-5 business days..."
3. **Bug Acknowledged** - "Thanks for reporting. We're investigating..."
4. **Feature Noted** - "Thanks for the suggestion. Added to our list..."
5. **More Info Needed** - "To help you faster, please share..."

### Freshdesk Setup (Scale)

**Automation Rules:**

```
Rule: Auto-close stale tickets
Trigger: No customer reply for 7 days
Condition: Status = "Awaiting Customer"
Action: Change status to "Resolved"

Rule: SLA breach alert
Trigger: Ticket approaching SLA breach (2 hours before)
Action: Send Slack notification, escalate priority

Rule: VIP routing
Trigger: Customer has "lifetime" OR "pro-annual" tag
Action: Priority = High, Assign to senior support
```

---

## AI Chatbot Setup

### Option 1: Crisp Chatbot (Free)

**Bot Builder Setup:**

```yaml
# Welcome message
Trigger: Chat opened
Bot: "Hey! How can I help?

      Quick options:
      [Subscription help] [Report a bug] [Talk to human]"

# Subscription flow
Trigger: Button clicked "Subscription help"
Bot: "What's happening with your subscription?

      [Can't access premium] [Want to cancel] [Billing question]"

# Can't access premium
Trigger: Button clicked "Can't access premium"
Bot: "Try these steps:
      1. Sign out of the app
      2. Go to App Store > Account > Subscriptions
      3. Verify your subscription is active
      4. Sign back in

      Still not working? [Talk to human]"
```

### Option 2: Custom Claude/GPT Bot

**Build your own with Chatbase or Dante AI:**

1. **Upload your content:**
   - FAQ document
   - Product documentation
   - Previous support conversations (anonymized)
   - App store listing

2. **Configure behavior:**
```
System prompt:
You are a support agent for [APP NAME], a [description] app.

Rules:
- Be concise (2-3 sentences max)
- Always offer to connect with human support
- For refunds, direct to support@[domain].com
- For crashes, ask for device and OS version
- Never promise features or timelines
- If unsure, say "Let me connect you with our team"

Knowledge:
- Subscription: $X/month or $Y/year
- Refund policy: Within 7 days
- Support hours: 9am-6pm PST weekdays
```

3. **Train on specific scenarios:**
```
Q: My subscription isn't working
A: Let's fix that. First, try signing out and back in. If that doesn't work, go to App Store > Account > Subscriptions to verify it's active. Still having trouble? I'll connect you with our team.

Q: How do I cancel?
A: Settings > Account > Cancel Subscription. You'll keep access until your billing period ends. Want me to connect you with support instead?

Q: I want a refund
A: I can help with that. Email support@[domain].com with your purchase receipt. We process refunds within 24 hours for requests made within 7 days.
```

### Option 3: Intercom Fin (Premium AI)

**Cost:** $0.99 per successful resolution

**Setup:**
1. Add all help articles to Intercom
2. Enable Fin in Settings > AI
3. Set fallback to human agent
4. Monitor resolution quality weekly

**Fin behavior customization:**
```
Custom instructions:
- Only answer from documented knowledge
- Escalate billing disputes immediately
- Offer 10% discount code for frustrated users (code: SORRY10)
- Collect bug reports with device/OS/steps before escalating
```

---

## App Store Review Management

### Monitoring Tools

**Free:**
- App Store Connect (iOS) - Daily email digest
- Google Play Console (Android) - Built-in alerts
- RSS feeds from app store pages

**Paid:**
- **AppFollow** ($79/mo) - Multi-platform, auto-translate, respond from dashboard
- **Appbot** ($49/mo) - Sentiment analysis, keyword tracking
- **ReviewBot** ($9/mo) - Slack notifications only

### Response Strategy

**Response Time Targets:**
- 1-2 star reviews: <12 hours
- 3 star reviews: <24 hours
- 4-5 star reviews: <48 hours (optional)

**Review Response Templates:**

See `OPS/SUPPORT/canned_responses/app_store_review_responses.md` for full templates.

**Quick Reference:**

| Scenario | Response Approach |
|----------|-------------------|
| Bug report | Apologize, mention fix, offer email support |
| Feature request | Thank, note it's logged, no promises |
| Subscription anger | Direct to Settings > Subscriptions, offer email help |
| Vague negative | Invite them to email with details |
| Pricing complaint | Mention free tier, don't argue price |

**Negative Review Recovery Flow:**

```
1. Respond publicly within 12 hours (empathetic, brief)
2. If they email, resolve issue with priority
3. After resolution, wait 3 days
4. Send follow-up: "Hope the fix worked. If so, would you consider updating your review?"
5. Track conversion rate (aim for 30% review updates)
```

### Review Request Strategy

**When to ask for reviews:**
- After completing a positive action (finished workout, saved money, hit goal)
- After 3+ sessions with the app
- After successfully using a paid feature
- Never after an error or frustration

**In-App Review Prompt (iOS):**

```swift
import StoreKit

func requestReview() {
    guard let scene = UIApplication.shared.connectedScenes.first as? UIWindowScene else { return }
    SKStoreReviewController.requestReview(in: scene)
}

// Trigger conditions
let sessionsCompleted = UserDefaults.standard.integer(forKey: "sessions")
let lastPrompt = UserDefaults.standard.object(forKey: "lastReviewPrompt") as? Date

if sessionsCompleted >= 5 && (lastPrompt == nil || daysSince(lastPrompt!) > 90) {
    requestReview()
    UserDefaults.standard.set(Date(), forKey: "lastReviewPrompt")
}
```

**React Native:**

```javascript
import * as StoreReview from 'expo-store-review';

async function requestReview() {
  if (await StoreReview.isAvailableAsync()) {
    const sessions = await AsyncStorage.getItem('sessions');
    const lastPrompt = await AsyncStorage.getItem('lastReviewPrompt');

    const daysSincePrompt = lastPrompt
      ? (Date.now() - new Date(lastPrompt)) / (1000 * 60 * 60 * 24)
      : 999;

    if (parseInt(sessions) >= 5 && daysSincePrompt > 90) {
      await StoreReview.requestReview();
      await AsyncStorage.setItem('lastReviewPrompt', new Date().toISOString());
    }
  }
}
```

---

## Workflow Automation

### Support Workflow Overview

```
Customer contacts →
  |
  ├─ Chat widget → Chatbot handles or escalates
  |
  ├─ Email → Auto-categorized, template suggested
  |
  ├─ App review → Alert + template sent
  |
  └─ All channels →
       |
       ├─ AI resolves common issues (60%+)
       |
       └─ Human handles complex (40% or less)
```

### Automation with Zapier

**Zap 1: New Review Alert**
```
Trigger: New app review (via AppFollow webhook)
Filter: Rating < 4 stars
Action:
  1. Post to Slack #reviews
  2. Create Notion task
  3. Send email notification
```

**Zap 2: Support Email to Slack**
```
Trigger: New email to support@
Filter: Subject contains "urgent" OR body contains "refund"
Action: Post to Slack #support-urgent
```

**Zap 3: CSAT Survey After Resolution**
```
Trigger: Ticket status changed to "Resolved" (Help Scout/Zendesk)
Delay: Wait 1 hour
Action: Send email with satisfaction survey
```

**Zap 4: Escalation Alert**
```
Trigger: Ticket tagged "escalation"
Action:
  1. Send SMS to founder
  2. Post to Slack with @channel
  3. Change priority to Critical
```

### n8n Automation (Self-Hosted Alternative)

**Benefit:** Free, self-hosted, more complex flows

**Example: AI-Powered Email Triage**

```json
{
  "nodes": [
    {
      "name": "Email Trigger",
      "type": "IMAP",
      "params": { "mailbox": "support@domain.com" }
    },
    {
      "name": "Claude Classification",
      "type": "HTTP Request",
      "params": {
        "url": "https://api.anthropic.com/v1/messages",
        "body": {
          "model": "claude-3-haiku-20240307",
          "messages": [
            {
              "role": "user",
              "content": "Classify this support email into one category: BILLING, TECHNICAL, ACCOUNT, FEATURE_REQUEST, SPAM. Email: {{$node.EmailTrigger.json.text}}"
            }
          ]
        }
      }
    },
    {
      "name": "Route by Category",
      "type": "Switch",
      "params": {
        "conditions": [
          { "value": "BILLING", "output": 0 },
          { "value": "TECHNICAL", "output": 1 },
          { "value": "ACCOUNT", "output": 2 }
        ]
      }
    }
  ]
}
```

---

## PRINTMAXX App Support Setup

### Per-App Configuration

**PrayerLock:**
- Common issues: Timer sync, notification delivery, subscription access
- FAQ topics: "How timing works," "Family sharing," "Offline mode"
- Affiliate support: Link to faith-based apps/books

**WalkToUnlock:**
- Common issues: Step counting accuracy, health permissions, GPS battery
- FAQ topics: "Calibrating steps," "Battery optimization," "Lockout recovery"
- Technical note: Health API requires careful permission handling

**StudyLock:**
- Common issues: App blocking conflicts, timer accuracy, subscription restore
- FAQ topics: "Which apps blocked," "Emergency unlock," "Screen time vs StudyLock"

### Support Email Templates

**Subscription Not Working (Most Common):**
```
Subject: Re: Subscription issue

Got it. Let's fix this.

Try these steps:
1. Open the App Store
2. Tap your profile (top right)
3. Tap Subscriptions
4. Find [APP NAME] and verify it shows "Active"
5. Open [APP NAME] and sign out/back in

If it shows active but still not working, reply with a screenshot of your Subscriptions page. I'll manually sync it.

- [Name]
```

**Refund Request:**
```
Subject: Re: Refund request

Done. Refund processed for $X.

You'll see it in 3-5 business days depending on your bank.

Sorry it didn't work out. If you want to try again later, the door's always open.

- [Name]
```

**Bug Report Response:**
```
Subject: Re: Bug report

Thanks for the details. That shouldn't happen.

I've logged this with our dev team. A few questions to help them fix it faster:

1. What device and iOS/Android version are you using?
2. Does it happen every time or randomly?
3. Any error messages?

We'll keep you posted on the fix.

- [Name]
```

**Feature Request:**
```
Subject: Re: Feature suggestion

Cool idea. Logged it.

We prioritize based on how many people ask for things. Can't promise timelines, but it's on the list.

Thanks for caring enough to suggest improvements.

- [Name]
```

---

## Metrics & Measurement

### Key Metrics to Track

See `OPS/SUPPORT/support_metrics.md` for full details.

**Solo Founder Essentials (Track Weekly):**
1. Response time (target: <24h)
2. Tickets opened vs closed
3. Repeat contacts (same person, same issue)
4. Review rating trend

**Growth Stage (Track Daily):**
1. First response time by channel
2. Resolution time
3. CSAT score
4. Chatbot resolution rate
5. Escalation rate

### Spreadsheet Tracking (Free)

**Google Sheets Template:**

| Date | Channel | Category | Response Time | Resolution Time | CSAT | Notes |
|------|---------|----------|---------------|-----------------|------|-------|
| 1/25 | Email | Billing | 2h | 4h | Positive | Refund processed |
| 1/25 | Chat | Technical | 5m | 30m | Positive | Bot resolved |
| 1/25 | Review | Negative | 6h | 24h | N/A | Updated review to 4* |

**Weekly Summary Row:**
```
=AVERAGE(C2:C8)  // Avg response time
=COUNTIF(F2:F8, "Positive")/COUNT(F2:F8)  // CSAT rate
```

---

## Cost Calculator

### Monthly Support Cost Estimation

**0-500 users (Pre-revenue):**
| Item | Cost |
|------|------|
| Crisp Free | $0 |
| Gmail | $0 |
| Your time (5h/week) | ~$75 if valued at $15/h |
| **Total** | ~$75/mo |

**500-2000 users (Early traction):**
| Item | Cost |
|------|------|
| Crisp Pro | $25 |
| Your time (10h/week) | ~$150 |
| **Total** | ~$175/mo |

**2000-10000 users (Growing):**
| Item | Cost |
|------|------|
| Intercom Starter | $74 |
| Fin AI (100 resolutions) | $99 |
| Part-time VA (20h/week) | $400 |
| AppFollow | $79 |
| **Total** | ~$650/mo |

**Rule of thumb:** Support cost should be <5% of revenue. If higher, invest in self-service.

---

## Implementation Checklist

### Week 1: Foundation
- [ ] Create support@[domain].com email
- [ ] Set up Crisp free account
- [ ] Add Crisp widget to app (or native help screen)
- [ ] Create 5 basic canned responses
- [ ] Set up review monitoring alerts

### Week 2: Automation
- [ ] Build Crisp chatbot for top 5 FAQs
- [ ] Create email filters and labels
- [ ] Set up auto-responder
- [ ] Create review response templates
- [ ] Add FAQ/Help section to app

### Week 3: Measurement
- [ ] Start tracking response times
- [ ] Set up weekly metrics review
- [ ] Create feedback loop (support issues → product fixes)
- [ ] Document recurring issues

### Month 2+: Optimization
- [ ] Analyze top ticket categories
- [ ] Create self-service content for top issues
- [ ] Test AI chatbot (Chatbase, Dante AI)
- [ ] Implement review request prompts
- [ ] Consider upgrading tools based on volume

---

## Resources

### Tools Mentioned
- Crisp: crisp.chat
- Help Scout: helpscout.com
- Freshdesk: freshdesk.com
- Intercom: intercom.com
- Zendesk: zendesk.com
- AppFollow: appfollow.io
- Chatbase: chatbase.co
- Dante AI: dante-ai.com

### Related Internal Docs
- Response templates: `OPS/SUPPORT/canned_responses/`
- Escalation rules: `OPS/SUPPORT/escalation_matrix.md`
- FAQ content: `OPS/SUPPORT/FAQ_MASTER.md`
- Crisis handling: `OPS/CRISIS_RESPONSE_PLAYBOOK.md`
- Support metrics: `OPS/SUPPORT/support_metrics.md`

---

Last updated: 2026-01-25
