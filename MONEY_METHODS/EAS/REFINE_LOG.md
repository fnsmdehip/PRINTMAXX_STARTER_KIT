# EAS Refine Log

## 2026-03-16 -- Website hardening pass

### Changes made

**1. Tool name purge (all pages)**
- index.html: Removed "Claude, GPT" from Content Engine description. Replaced with "any major AI model or open-source alternative."
- results.html: Removed "Vapi voice agent" from dental case study. Replaced with "conversational voice AI."
- packages.html: Removed "n8n, Supabase" from open-source section and FAQ bundling answer. Replaced with capability descriptions ("open-source workflow engines and databases", "same workflow engine, same database backend").
- packages.html: Removed "MCP" acronym from Tier 3. Spelled out "Model Context Protocol."
- playbooks.html: Stripped ALL tool names -- Vapi, Bland AI, Retell, Playwright, n8n, Pinecone, Claude, GPT, Llama, Mistral, LangChain, CrewAI, Supabase, Firebase. Replaced every instance with capability descriptions (voice AI platform, headless browser, workflow engine, vector database, etc.).

**Why:** Naming specific tools publicly signals which stack we use, gives competitors free intel, creates vendor dependency perception, and limits positioning. Capability descriptions position us as tool-agnostic experts who pick whatever works best for each client.

**2. Added "90% fail" differentiator to homepage**
- New section between trust bar and "Why we're different" section.
- Headline: "90% of AI agents fail within 30 days of deployment. Ours don't."
- Supporting copy about self-healing systems, circuit breakers, retry logic.

**Why:** Primary differentiator from competitive research. Most AI agencies sell the install but have no answer for post-deployment failure. This positions us on the durability gap.

**3. Added Mark Cuban quotes section to homepage**
- Two quotes in a side-by-side grid before the FAQ section.
- Quote 1: "Go to businesses, particularly small- to medium-sized businesses that don't understand AI yet."
- Quote 2: "Companies can either be great at AI or risk being put out of business."
- Supporting copy connecting the quotes to our positioning.

**Why:** Social proof from a recognized name. Both quotes directly validate our target market (SMBs) and urgency thesis. Not endorsement -- just market validation from a credible voice.

**4. Added recurring retainer tiers to packages.html**
- Restructured page into two sections: "One-time installs" (Tiers 1-3) and "Monthly retainers."
- New "Agent Care" retainer: $997-$2,997/mo -- monitoring, prompt tuning, integration maintenance, 10 hrs improvement work, monthly performance report.
- Existing "Managed Autonomy" ($3,000-$10,000/mo) kept, reformatted to show it includes everything in Agent Care plus additional scope.

**Why:** Competitive research identified $997-$4,997/mo retainers as underserved gap. Most agencies only sell projects. Recurring revenue is the compounding play. Agent Care fills the gap between "we installed it, good luck" and full managed operations.

**5. Fixed contact form action**
- Changed from `mailto:hello@enterpriseautomationsolutions.com` (opens email client, terrible UX) to `https://formspree.io/f/placeholder` (actual form submission).
- Formspree endpoint is placeholder -- needs real endpoint created at formspree.io.

**Why:** mailto forms don't actually submit data. They open the user's email client, which on most machines either fails or creates friction. Formspree gives real form submission with email forwarding.

### Deployment
- Deployed to `eas-preview.surge.sh` via surge CLI. Live and accessible.
- Preview URL: https://eas-preview.surge.sh

### Still needs human action
- Create Formspree account and replace `placeholder` in contact.html with real form ID (5 min)
- Set up Cal.com embed in book.html (the calendar placeholder is still a static div)
- Point real domain (enterpriseautomation.solutions) to surge or move to Cloudflare Pages
