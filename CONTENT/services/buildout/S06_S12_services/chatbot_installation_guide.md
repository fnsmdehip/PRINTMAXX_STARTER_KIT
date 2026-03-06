# Chatbot Installation Service — Complete Guide

## The Opportunity

Every website with a contact form is leaving money on the table. A chatbot captures leads 24/7,
qualifies them automatically, books meetings without human involvement, and handles 60-80% of
support tickets. Companies paying $0 for a basic contact form should be paying $100-300/mo for
an AI chatbot. You bridge that gap as the installer + configurator.

**Your offer:** Install, configure, train, and hand off AI chatbot for $500-1,500 flat fee.
Add a $99-199/mo maintenance retainer for updates, retraining, and analytics review.

---

## Service Packages

| Package | Price | What's Included |
|---------|-------|----------------|
| Basic Install | $497 | Tidio install, 5 flows, 30-day setup support |
| Growth | $997 | Intercom or Drift + 10 flows + 3 integrations (CRM, Calendly, email) |
| Enterprise | $1,497 | Custom-trained GPT-4 bot + full CRM sync + ongoing training + priority support |
| Monthly retainer add-on | $99/mo | Monthly review, 2 new flows/mo, performance report |

**Volume math:** 8 clients × $1,000 avg install = $8,000 one-time/month + 20 retainer clients × $149/mo = $2,980/mo recurring. Month 6 target: $11,000/mo gross.

---

## Tool Selection Guide

### Tidio (Recommended for most clients)
- **Price:** Free plan (basic), $29/mo Communicator, $59/mo Chatbots, $399/mo Tidio+
- **Best for:** eCommerce (Shopify/WooCommerce native integration), SMB, under $5M ARR
- **Install time:** 20-30 minutes
- **AI capability:** Lyro AI (built-in), GPT-3.5 base, learns from past conversations
- **Integrations:** Shopify, WooCommerce, Magento, WordPress, Wix, Squarespace, HubSpot, Klaviyo
- **Your cost to deliver:** $0 if client pays for their own Tidio account (you just configure it)

### Intercom (Mid-market)
- **Price:** $74/mo Starter (1 seat), $190/mo Pro
- **Best for:** SaaS, $2M-50M ARR, needs CRM sync + product tours
- **Install time:** 45-90 minutes
- **AI capability:** Fin (GPT-4 powered), can resolve 60%+ tickets with training
- **Integrations:** Salesforce, HubSpot, Stripe, Mixpanel, Segment, Slack, Jira
- **Your cost to deliver:** $0 — client pays Intercom, you configure

### Drift (Sales-heavy companies)
- **Price:** $2,500/mo+ (premium product, enterprise only)
- **Best for:** B2B SaaS with high ACV (>$10K deals), SDR-bot replacement
- **Install time:** 2-4 hours
- **AI capability:** Real-time account intelligence, Salesforce sync, meeting booking
- **Target client:** $10M+ ARR B2B with sales team

### Crisp (Budget option)
- **Price:** Free forever (2 agents), $25/mo Pro, $95/mo Unlimited
- **Best for:** Startups, early-stage, budget-conscious
- **AI capability:** Limited, mostly canned responses + escalation
- **Your pitch:** "Start free, upgrade as you grow"

### Custom ChatGPT API Bot (Premium offer)
- **Price:** $1,497+ setup
- **Tech:** OpenAI Assistants API + custom knowledge base (your client's docs, FAQs, product catalog)
- **Hosting:** Vercel (free tier for serverless functions)
- **Best for:** Clients who want total control + custom persona
- **Build time:** 4-8 hours

---

## Installation SOPs

### Tidio Installation (WordPress/Shopify)

**WordPress:**
```
1. Client gives you WP admin access (or install plugin themselves)
2. Plugins → Add New → search "Tidio"
3. Install + Activate
4. Plugin Settings → Tidio Settings → Connect Account (client creates Tidio account if none)
5. Tidio Dashboard → configure in web UI
6. No code needed for basic install
```

**Shopify:**
```
1. Shopify App Store → search "Tidio"
2. Install app → Authorize
3. Tidio app opens → configure
4. Flows can be built without code
```

**Custom HTML embed (any site):**
```html
<!-- Add this before </body> on every page -->
<script>
  (function() {
    var tidioScript = document.createElement('script');
    tidioScript.src = '//code.tidio.co/[CLIENT_TIDIO_ID].js';
    tidioScript.async = true;
    document.body.appendChild(tidioScript);
  })();
</script>
```

---

### Intercom Installation (SaaS / Web App)

**JavaScript snippet (goes in <head>):**
```html
<script>
  window.intercomSettings = {
    api_base: "https://api-iam.intercom.io",
    app_id: "[CLIENT_APP_ID]",
    // Optional: pre-fill for logged-in users
    user_id: "{{user.id}}",
    email: "{{user.email}}",
    name: "{{user.name}}",
    created_at: {{user.created_at}}
  };
</script>
<script>
  (function(){var w=window;var ic=w.Intercom;if(typeof ic==="function"){ic('reattach_activator');ic('update',w.intercomSettings);}else{var d=document;var i=function(){i.c(arguments);};i.q=[];i.c=function(args){i.q.push(args);};w.Intercom=i;var l=function(){var s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://widget.intercom.io/widget/[CLIENT_APP_ID]';var x=d.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);};if(document.readyState==='complete'){l();}else if(w.attachEvent){w.attachEvent('onload',l);}else{w.addEventListener('load',l,false);}}})();
</script>
```

---

### Custom GPT Chatbot (OpenAI Assistants API)

**Backend (Node.js / Vercel serverless):**
```javascript
// api/chat.js — Vercel serverless function
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Create assistant once, save assistant_id to env
// const assistant = await openai.beta.assistants.create({
//   name: "Client Company Assistant",
//   instructions: "You are a helpful assistant for [Client]. Answer questions about...",
//   model: "gpt-4o",
//   tools: [{ type: "file_search" }],
// });

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  const { message, threadId } = req.body;

  // Create or retrieve thread
  const thread = threadId
    ? { id: threadId }
    : await openai.beta.threads.create();

  // Add user message
  await openai.beta.threads.messages.create(thread.id, {
    role: 'user',
    content: message
  });

  // Run assistant
  const run = await openai.beta.threads.runs.createAndPoll(thread.id, {
    assistant_id: process.env.ASSISTANT_ID
  });

  if (run.status === 'completed') {
    const messages = await openai.beta.threads.messages.list(thread.id);
    const reply = messages.data[0].content[0].text.value;
    return res.json({ reply, threadId: thread.id });
  }

  return res.status(500).json({ error: 'Assistant failed' });
}
```

**Frontend widget (embed on any site):**
```html
<!-- Floating chatbot widget -->
<div id="chatbot-container">
  <button id="chat-toggle" onclick="toggleChat()">Chat</button>
  <div id="chat-window" style="display:none">
    <div id="chat-messages"></div>
    <input id="chat-input" type="text" placeholder="Ask anything..." />
    <button onclick="sendMessage()">Send</button>
  </div>
</div>

<script>
let threadId = null;

async function sendMessage() {
  const input = document.getElementById('chat-input');
  const msg = input.value.trim();
  if (!msg) return;
  input.value = '';

  appendMessage('user', msg);

  const resp = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: msg, threadId })
  });
  const data = await resp.json();
  threadId = data.threadId;
  appendMessage('assistant', data.reply);
}

function appendMessage(role, text) {
  const el = document.getElementById('chat-messages');
  el.innerHTML += `<div class="msg ${role}">${text}</div>`;
  el.scrollTop = el.scrollHeight;
}

function toggleChat() {
  const win = document.getElementById('chat-window');
  win.style.display = win.style.display === 'none' ? 'block' : 'none';
}

document.getElementById('chat-input').addEventListener('keypress', e => {
  if (e.key === 'Enter') sendMessage();
});
</script>
```

**Cost to run:** GPT-4o input $2.50/1M tokens + output $10/1M tokens. A typical chatbot conversation = ~500 tokens total. At 100 conversations/day: 50K tokens/day = ~$0.25/day = $7.50/mo. Sell the client a $99/mo hosting plan = 93% margin.

---

## Flow Templates (Tidio / Intercom)

### Flow 1: Lead Qualification (Universal)

```
Trigger: First visit OR after 30 seconds on site

Step 1: "Hey! What brings you here today?"
  Option A → "Looking for pricing/info" → go to Flow 2
  Option B → "Need support with something" → go to Flow 3
  Option C → "Just browsing" → tag as [cold], end chat

Step 2: "What's your biggest challenge with [product category]?"
  [open text] → capture as lead note, tag as qualified

Step 3: "Want me to connect you with someone who can help?"
  Option A → "Yes" → trigger Calendly embed or collect email → notify sales
  Option B → "Not yet" → "No problem! Here's our [pricing page / free resource]"
```

### Flow 2: Meeting Booking

```
Trigger: "Book a call" or "Talk to sales" button click

Step 1: "Great! A few quick questions to make sure it's the right call:"
Step 2: "What's your company's approximate size?" [dropdown: 1-10, 11-50, 50-200, 200+]
Step 3: "What's your current budget range?" [dropdown: <$1K/mo, $1-5K/mo, $5K+/mo]
Step 4: If size ≥ 11 AND budget ≥ $1K/mo → show Calendly iframe
         Else → "Here's a resource that might help first: [link]" → collect email
```

### Flow 3: Support Deflection

```
Trigger: "Support" or "Help" click

Step 1: Bot searches knowledge base (Intercom Fin or Tidio Lyro)
Step 2: Shows top 3 relevant articles
Step 3: "Did that answer your question?"
  Option A → "Yes" → end chat, mark resolved
  Option B → "No" → assign to human agent (or collect email + ticket)
```

---

## Client Handoff Checklist

After installation is complete:
- [ ] All flows tested in incognito window (simulate new visitor)
- [ ] Lead capture tested: confirmed email arrives in client's inbox + CRM
- [ ] Meeting booking tested: slot appears in client's calendar
- [ ] Mobile view tested (chatbot renders correctly on iPhone + Android)
- [ ] Analytics connected: Google Analytics 4 custom events for chat_open, lead_captured
- [ ] Knowledge base uploaded: FAQs, pricing, product docs uploaded to bot
- [ ] Escalation path defined: after X failed attempts → route to human + email client
- [ ] Notification setup: client alerted via email or Slack when new lead captured
- [ ] Recorded Loom walkthrough delivered: 15-min tutorial for client to manage bot themselves
- [ ] Access transferred: client has admin access to their bot account

---

## Upsell Path

After basic install:
- Month 1: Review bot conversations → identify top 3 unanswered questions → add 3 new flows ($299)
- Month 2: Integrate with CRM (HubSpot/Salesforce sync setup) → $497
- Month 3: A/B test proactive messages (trigger timing, greeting text) → $199
- Month 6: Full retraining + add new product line to knowledge base → $399

Client lifetime value (LTV): $1,500 install + $99/mo × 12 mo + $200/mo upsells × 6 mo = $3,900 first year.
