# Section 3: Code & Building — 40 Production Prompts

## App Scaffolding Prompts (81-95)

### Prompt 81: PWA Scaffold
```
Build a Progressive Web App called [APP NAME].

Purpose: [ONE SENTENCE DESCRIPTION]

Tech stack:
- Vanilla JS (no frameworks)
- CSS Grid + Flexbox for layout
- localStorage for data persistence
- Service worker for offline support

File structure:
- index.html
- css/style.css
- js/app.js
- js/storage.js (localStorage wrapper with get/set/delete/getAll methods)
- manifest.json (standalone display, [THEME COLOR] accent)
- sw.js (cache-first strategy, versioned cache name)

Design:
- Mobile-first (320px base, max-width 480px centered on desktop)
- Dark mode default: #0A0A0A background, [ACCENT COLOR] highlights, #F5F5F5 text
- System font stack (no Google Fonts, faster load)
- Touch targets minimum 44x44px

Start with the data model, then build the UI, then add PWA features.
```

### Prompt 82: Landing Page Generator
```
Build a single-page landing page for [PRODUCT/SERVICE].

Sections (top to bottom):
1. Hero: Headline + subheadline + CTA button + hero image placeholder
2. Problem: 3 pain points with icons
3. Solution: What the product does (3 features with descriptions)
4. Social proof: Testimonial cards (3 slots with placeholder text)
5. Pricing: [PRICING TIERS — describe them]
6. FAQ: 5 expandable questions
7. Footer CTA: Final call to action + email capture

Technical requirements:
- Single HTML file with inline CSS (under 500 lines total)
- No JavaScript except for FAQ accordion and smooth scroll
- Fully responsive (320px to 1440px)
- Load time under 1 second on 3G
- Color scheme: [COLORS]
- Font: Inter via system fonts fallback stack

CTA button should link to: [URL or "Stripe payment link placeholder"]
```

### Prompt 83: REST API Scaffold (Node.js)
```
Build a REST API with these endpoints:

Resource: [RESOURCE NAME — e.g., "tasks", "users", "products"]

Endpoints:
- GET /api/[resource] — list all (with pagination: ?page=1&limit=20)
- GET /api/[resource]/:id — get one by ID
- POST /api/[resource] — create new
- PUT /api/[resource]/:id — update by ID
- DELETE /api/[resource]/:id — delete by ID

Tech:
- Node.js + Express
- SQLite via better-sqlite3 (no ORM, raw SQL)
- Input validation on POST/PUT
- Error handling middleware (consistent error format)
- CORS enabled
- Rate limiting (100 requests/15 minutes per IP)

Data model:
[DESCRIBE YOUR FIELDS — e.g., "title (string, required), description (string, optional), status (enum: todo/doing/done), created_at (auto)"]

Include a seed script that populates 20 sample records.
```

### Prompt 84: Chrome Extension Scaffold
```
Build a Chrome extension called [NAME].

What it does: [ONE SENTENCE]

Manifest V3 structure:
- manifest.json (permissions: [LIST NEEDED PERMISSIONS])
- popup.html + popup.js (the UI when you click the extension icon)
- content.js (runs on [WHICH PAGES — e.g., "all pages", "only twitter.com"])
- background.js (service worker for event handling)
- styles.css

Functionality:
[DESCRIBE WHAT THE EXTENSION DOES IN 3-5 BULLET POINTS]

Storage: Use chrome.storage.local for settings/data
Design: Match Chrome's design language (clean, minimal, 300px wide popup)
```

### Prompt 85: Dashboard UI
```
Build a dashboard page with these components:

1. Top bar: App name (left), user avatar + dropdown (right)
2. Sidebar: Navigation with icons — [LIST 5-7 NAV ITEMS]
3. Main content area with:
   - Stats row: 4 metric cards (icon + number + label + trend arrow)
   - Chart placeholder: 600x300px area labeled "[CHART TYPE] goes here"
   - Data table: [COLUMNS] with sortable headers, 10 rows, pagination
4. Responsive: Sidebar collapses to hamburger menu below 768px

Use CSS Grid for the layout. No charting library — just the placeholder.
Stats to display: [LIST YOUR 4 KEY METRICS]
Color scheme: [COLORS]
```

### Prompt 86: Authentication Flow
```
Build a complete auth flow using Supabase:

Pages:
1. Sign up (email + password)
2. Log in (email + password)
3. Password reset (email input → reset link)
4. Protected dashboard (redirects to login if not authenticated)

Requirements:
- Supabase JS client v2
- Session persistence (stays logged in on refresh)
- Loading states on all buttons
- Error messages displayed inline (not alerts)
- Redirect after login to /dashboard
- Redirect after logout to /login
- Password requirements shown in real-time (8+ chars, 1 number, 1 uppercase)

Supabase project URL: [PLACEHOLDER]
Supabase anon key: [PLACEHOLDER]

Include the SQL to create the users table in Supabase.
```

### Prompt 87: Email Template (HTML)
```
Build a responsive HTML email template for [PURPOSE — welcome email, receipt, newsletter, etc.].

Requirements:
- Table-based layout (for email client compatibility)
- Inline CSS only (no <style> tags — Gmail strips them in some cases)
- Works in: Gmail, Outlook 365, Apple Mail, Yahoo Mail
- Max width: 600px, centered
- Mobile responsive (stacks to single column below 480px)

Sections:
- Logo header ([BRAND NAME] text + accent bar)
- [DESCRIBE CONTENT SECTIONS]
- CTA button ([BUTTON TEXT], [BUTTON COLOR], centered, 44px height minimum)
- Footer: Unsubscribe link, company address, social links

Colors: [BRAND COLORS]
Test by sending to yourself via a tool like Mailchimp or Postmark.
```

### Prompt 88: CLI Tool
```
Build a command-line tool in [LANGUAGE — Node.js/Python/Bash] that [WHAT IT DOES].

Commands:
- [COMMAND 1]: [DESCRIPTION]
- [COMMAND 2]: [DESCRIPTION]
- [COMMAND 3]: [DESCRIPTION]

Requirements:
- --help flag shows usage for all commands
- Colored output (green for success, red for errors, yellow for warnings)
- Configuration file support (~/.toolnamerc or .toolnamerc in project root)
- Input validation with clear error messages
- Exit codes (0 for success, 1 for user error, 2 for system error)

Include a README with installation and usage examples.
```

### Prompt 89: Form with Validation
```
Build a multi-step form with these fields:

Step 1: [FIELDS — e.g., "Name (required), Email (required, valid format), Phone (optional)"]
Step 2: [FIELDS]
Step 3: [FIELDS]
Review step: Show all entered data, allow editing any step

Requirements:
- Client-side validation (real-time, not just on submit)
- Error messages appear below each field
- Progress bar showing current step
- Back button on each step
- Data persists in sessionStorage (survives page refresh)
- Submit sends data to [ENDPOINT or "console.log for now"]
- Accessible: proper labels, ARIA attributes, keyboard navigation
- Mobile-friendly: fields stack vertically, 16px+ font (prevents iOS zoom)
```

### Prompt 90: Stripe Checkout Integration
```
Integrate Stripe Checkout into my existing app.

Setup:
- Netlify/Vercel serverless function for the backend
- Stripe.js on the frontend (no sensitive keys in client code)

I need:
1. A "Buy Now" button that creates a Checkout session
2. A success page that verifies payment
3. A cancel page
4. A webhook handler for checkout.session.completed

Product details:
- Name: [PRODUCT NAME]
- Price: [AMOUNT] [CURRENCY]
- Type: [ONE-TIME or SUBSCRIPTION with INTERVAL]

Include:
- Environment variable setup instructions
- Test mode card numbers for testing
- The webhook secret verification code
- Error handling for failed payments
```

### Prompt 91: Database Schema Design
```
Design a database schema for [APP TYPE — e.g., "a project management tool", "an e-commerce store"].

Requirements:
[LIST 5-10 FEATURES THE APP NEEDS TO SUPPORT]

Provide:
1. Entity-relationship description (which tables, how they relate)
2. SQL CREATE TABLE statements (PostgreSQL syntax)
3. Indexes for common queries
4. Sample INSERT statements (5 rows per table)
5. 3 example queries that the app would frequently run

Constraints:
- Use UUIDs for primary keys (not auto-increment)
- Include created_at and updated_at timestamps on every table
- Use soft deletes (deleted_at column) instead of hard deletes
- Foreign key constraints with appropriate ON DELETE behavior
```

### Prompt 92: WebSocket Real-Time Feature
```
Add real-time functionality to my app using WebSockets.

Feature: [WHAT SHOULD UPDATE IN REAL-TIME — e.g., "live chat", "collaborative editing", "live notifications"]

Server (Node.js):
- Use the 'ws' package (not Socket.io — smaller, no fallback needed in 2024+)
- Handle: connection, message, close, error events
- Broadcast to all connected clients or send to specific client
- Heartbeat every 30 seconds to detect dead connections
- Reconnection logic on client side

Client:
- Connect on page load
- Auto-reconnect with exponential backoff (1s, 2s, 4s, 8s, max 30s)
- Queue messages while disconnected, send on reconnect
- Visual indicator showing connection status (green dot = connected, red = disconnected)
```

### Prompt 93: Cron Job / Scheduled Task
```
Build a scheduled task that [WHAT IT DOES] every [FREQUENCY].

Runtime: [Node.js / Python]
Trigger: [CRON EXPRESSION — or describe the schedule and I'll set the cron]

The task should:
1. [STEP 1]
2. [STEP 2]
3. [STEP 3]

Requirements:
- Logging: Write start time, end time, and result to a log file
- Error handling: If the task fails, log the error and send a notification to [SLACK WEBHOOK URL or "console.error for now"]
- Idempotency: Running the task twice should not create duplicate data
- Lock file: Prevent two instances from running simultaneously

Include the crontab entry and instructions for setting it up on macOS (launchd) and Linux (cron).
```

### Prompt 94: API Integration Wrapper
```
Build a wrapper/SDK for the [API NAME] API.

Base URL: [API BASE URL]
Auth method: [API KEY / OAUTH / BEARER TOKEN]
Rate limit: [REQUESTS PER MINUTE/HOUR]

Endpoints I need:
1. [ENDPOINT 1]: [METHOD] [PATH] — [DESCRIPTION]
2. [ENDPOINT 2]: [METHOD] [PATH] — [DESCRIPTION]
3. [ENDPOINT 3]: [METHOD] [PATH] — [DESCRIPTION]

The wrapper should:
- Handle authentication automatically
- Retry on 429 (rate limit) with exponential backoff
- Retry on 500/502/503 once
- Type-check inputs before sending requests
- Return parsed JSON, not raw responses
- Throw descriptive errors with the API's error message included

Language: [JavaScript / Python / TypeScript]
```

### Prompt 95: Scraper / Data Extractor
```
Build a web scraper that extracts [DATA TYPE] from [WEBSITE/URL PATTERN].

Data to extract per page:
- [FIELD 1]: [WHERE TO FIND IT — CSS selector, XPath, or describe location]
- [FIELD 2]: [WHERE TO FIND IT]
- [FIELD 3]: [WHERE TO FIND IT]

Requirements:
- Use [cheerio for Node.js / BeautifulSoup for Python / Playwright for JS-rendered pages]
- Handle pagination: [DESCRIBE HOW PAGINATION WORKS ON THE SITE]
- Rate limiting: Max [NUMBER] requests per minute
- Output: Save to [CSV / JSON / SQLite]
- Error handling: Skip failed pages, log errors, continue scraping
- User-agent rotation (provide 5 common user agents)
- Respect robots.txt

Expected output: [NUMBER] records from [NUMBER] pages.
```

## Debugging Prompts (96-105)

### Prompt 96: Bug Diagnosis
```
I have a bug in my [LANGUAGE] code.

What should happen: [EXPECTED BEHAVIOR]
What actually happens: [ACTUAL BEHAVIOR]
When it happens: [STEPS TO REPRODUCE]

Here's the relevant code:

[PASTE CODE]

Error message (if any): [PASTE ERROR]

Diagnose the bug. Explain:
1. What's causing it (root cause, not just symptoms)
2. Why the code behaves this way
3. The fix (with corrected code)
4. How to prevent this type of bug in the future
```

### Prompt 97: Error Message Decoder
```
I'm getting this error and I don't understand what it means:

[PASTE FULL ERROR MESSAGE / STACK TRACE]

Context:
- Language/framework: [LANGUAGE]
- What I was doing when it occurred: [ACTION]
- Has this worked before? [YES/NO]
- Recent changes: [WHAT I CHANGED BEFORE THE ERROR STARTED]

Explain:
1. What this error means in plain English
2. The most likely cause (given my context)
3. The fix
4. How to debug similar errors in the future
```

### Prompt 98: Performance Optimization
```
This code is slow. It takes [TIME] to run when it should take [TARGET TIME].

[PASTE CODE]

Context:
- Data size: [HOW MUCH DATA IT PROCESSES]
- Where it runs: [BROWSER / NODE / PYTHON]
- Called how often: [ONCE / PER REQUEST / IN A LOOP]

Analyze:
1. Identify the performance bottleneck(s)
2. Explain WHY each bottleneck is slow (algorithmic complexity, I/O, memory, etc.)
3. Provide the optimized version with comments explaining each change
4. Estimate the speedup factor
```

### Prompt 99: Memory Leak Detective
```
My [LANGUAGE] application's memory usage grows over time.

Symptoms:
- Memory at start: [SIZE]
- Memory after [TIMEFRAME]: [SIZE]
- When it's worst: [CONTEXT]

Here's the code I suspect is leaking:

[PASTE CODE]

Identify:
1. Where memory is being allocated but not freed
2. Common patterns that cause this type of leak
3. The fix
4. How to monitor memory usage to verify the fix worked (specific tools/commands)
```

### Prompt 100: Code Review
```
Review this code for bugs, security issues, and improvements:

[PASTE CODE]

Focus on:
1. Bugs: Anything that will break in production
2. Security: SQL injection, XSS, exposed secrets, missing auth checks
3. Edge cases: What inputs will cause unexpected behavior?
4. Readability: Is this maintainable by someone else?
5. Performance: Any obvious inefficiencies?

For each issue, provide:
- Severity (CRITICAL / HIGH / MEDIUM / LOW)
- What's wrong
- The fix (show corrected code)
```

### Prompt 101: Regex Builder
```
I need a regex that matches: [DESCRIBE WHAT YOU WANT TO MATCH]

Examples of strings that SHOULD match:
- [EXAMPLE 1]
- [EXAMPLE 2]
- [EXAMPLE 3]

Examples of strings that should NOT match:
- [EXAMPLE 1]
- [EXAMPLE 2]

Language: [JavaScript / Python / Go / etc.]

Provide:
1. The regex pattern
2. A breakdown of what each part does
3. Test code that validates all the examples above
4. Edge cases I should test for
```

### Prompt 102: Refactor Legacy Code
```
Refactor this code to be cleaner and more maintainable:

[PASTE CODE]

Constraints:
- Don't change the external behavior (inputs and outputs stay the same)
- Keep the same language and framework
- Prioritize readability over cleverness
- [ANY SPECIFIC CONSTRAINTS — e.g., "keep the function signatures the same"]

Show:
1. The refactored code
2. A summary of what changed and why
3. Before/after comparison of key metrics (lines of code, cyclomatic complexity, number of functions)
```

### Prompt 103: Test Suite Generator
```
Write tests for this code:

[PASTE CODE]

Testing framework: [JEST / PYTEST / MOCHA / GO TEST / etc.]

Cover:
1. Happy path (normal usage, expected inputs)
2. Edge cases (empty inputs, null/undefined, boundary values)
3. Error cases (invalid inputs, network failures, missing data)
4. Integration (if the code interacts with external services, mock them)

Each test should have a descriptive name that explains what it's testing.
Generate at least [NUMBER] tests.
```

### Prompt 104: Dependency Audit
```
Here's my package.json (or requirements.txt / Cargo.toml / go.mod):

[PASTE DEPENDENCY FILE]

Analyze:
1. Are any dependencies deprecated or unmaintained? (check last publish date)
2. Are there known security vulnerabilities?
3. Which dependencies can be removed (not needed or replaceable with built-in features)?
4. Which have lighter alternatives?
5. What's the total install size impact?

For each issue found, recommend a specific action (update, replace, remove).
```

### Prompt 105: Git Mess Recovery
```
I'm in a bad git state. Here's what happened:

[DESCRIBE THE SITUATION — e.g., "I accidentally committed to main instead of a feature branch", "I need to undo the last 3 commits but keep the code changes", "I have merge conflicts in 15 files"]

Current state:
- `git status` output: [PASTE]
- `git log --oneline -10` output: [PASTE]
- Branch I'm on: [BRANCH]
- Branch I should be on: [BRANCH]

Give me the exact git commands to fix this, in order. Explain each command before I run it. Flag any command that's destructive (can't be undone).
```

## API & Integration Prompts (106-120)

### Prompt 106: API Error Handling
```
Add comprehensive error handling to this API call:

[PASTE CODE WITH API CALL]

Handle these scenarios:
1. Network error (no internet)
2. Timeout (request takes too long — set timeout to [SECONDS])
3. 400 Bad Request (show the validation error from the API)
4. 401 Unauthorized (redirect to login / refresh token)
5. 403 Forbidden (show "insufficient permissions" message)
6. 404 Not Found (show "resource not found" message)
7. 429 Too Many Requests (retry after the specified delay)
8. 500 Internal Server Error (retry once, then show error message)

Each error should:
- Log the full error for debugging
- Show a user-friendly message (not the raw error)
- Not crash the application
```

### Prompt 107: Environment Variable Setup
```
Set up environment variables for my [PROJECT TYPE] project.

I need these variables:
[LIST VARIABLES — e.g., "STRIPE_SECRET_KEY, DATABASE_URL, SENDGRID_API_KEY"]

Provide:
1. A .env.example file with placeholder values
2. A .gitignore entry to exclude .env
3. The code to load env vars in [LANGUAGE/FRAMEWORK]
4. Validation that all required vars are set at startup (fail fast if missing)
5. Instructions for setting these in [PRODUCTION ENVIRONMENT — Netlify, Vercel, Railway, etc.]
```

### Prompt 108: Webhook Handler
```
Build a webhook handler for [SERVICE — Stripe, GitHub, SendGrid, etc.] events.

Events I need to handle:
1. [EVENT 1]: [WHAT TO DO WHEN THIS FIRES]
2. [EVENT 2]: [WHAT TO DO WHEN THIS FIRES]
3. [EVENT 3]: [WHAT TO DO WHEN THIS FIRES]

Requirements:
- Verify webhook signature (prevent spoofed requests)
- Respond with 200 within 5 seconds (process async if needed)
- Idempotent handling (same event delivered twice = same result)
- Log every event received (timestamp, event type, relevant data)
- Error handling that doesn't expose internals to the caller

Runtime: [Node.js / Python / Go]
Framework: [Express / Netlify Functions / Vercel / Flask / etc.]
```

### Prompt 109: OAuth Integration
```
Implement OAuth 2.0 login with [PROVIDER — Google, GitHub, Twitter, etc.].

Flow:
1. User clicks "Sign in with [PROVIDER]"
2. Redirect to provider's auth page
3. Provider redirects back with auth code
4. Exchange code for access token
5. Fetch user profile
6. Create or update user in my database
7. Set session/JWT and redirect to dashboard

Stack: [YOUR STACK]
Callback URL: [YOUR CALLBACK URL]

Include:
- Required scopes and why each is needed
- Where to get client ID and secret (link to provider's developer console)
- Token refresh logic
- What to store in the database (user ID, email, avatar, access token, refresh token)
```

### Prompt 110: Data Migration Script
```
Write a migration script that transforms data from [FORMAT A] to [FORMAT B].

Source: [DESCRIBE SOURCE — CSV file, old database table, API response, etc.]
Destination: [DESCRIBE DESTINATION — new database table, JSON file, API endpoint, etc.]

Example source record:
[PASTE EXAMPLE]

Expected destination record:
[PASTE EXPECTED OUTPUT]

Transformations needed:
1. [TRANSFORMATION 1 — e.g., "split full_name into first_name and last_name"]
2. [TRANSFORMATION 2]
3. [TRANSFORMATION 3]

Requirements:
- Process in batches of [NUMBER] (don't load everything into memory)
- Log progress (every [NUMBER] records)
- Handle malformed records (skip + log, don't crash)
- Dry run mode (--dry-run flag that shows what would change without doing it)
- Rollback plan (how to undo if something goes wrong)
```

### Prompt 111: Caching Layer
```
Add caching to this code to reduce [API CALLS / DATABASE QUERIES / COMPUTATION TIME]:

[PASTE CODE]

Cache strategy:
- Cache duration: [TIME — e.g., "5 minutes", "1 hour", "until manually invalidated"]
- Cache key: [HOW TO GENERATE THE KEY — e.g., "based on the request URL", "based on user ID + query"]
- Storage: [IN-MEMORY / REDIS / FILESYSTEM]
- Invalidation: [WHEN TO CLEAR THE CACHE]

Include:
- Cache hit/miss logging
- Fallback to source if cache is unavailable
- Cache warming (pre-populate on startup if applicable)
```

### Prompt 112: File Upload Handler
```
Build a file upload feature for my [WEB APP / API].

Requirements:
- Accept: [FILE TYPES — e.g., "images only (jpg, png, webp)", "PDFs up to 10MB"]
- Max file size: [SIZE]
- Storage: [LOCAL FILESYSTEM / S3 / CLOUDFLARE R2]
- Generate unique filename (prevent overwrites)
- Return the file URL after upload

Security:
- Validate file type by magic bytes (not just extension)
- Scan filename for path traversal
- Set appropriate Content-Type headers
- Resize images to max [WIDTH]x[HEIGHT] if applicable

Frontend: Drag-and-drop zone + file picker + progress bar
Backend: [YOUR STACK]
```

### Prompt 113: Search Implementation
```
Add search functionality to my app.

What users search for: [DESCRIBE THE DATA — e.g., "product names and descriptions", "blog post titles and content"]
Data size: [NUMBER OF RECORDS]
Search requirements:
- Fuzzy matching (typo tolerance)
- Results ranked by relevance
- Highlighted matching text in results
- Search-as-you-type (debounced, 300ms delay)

Implementation:
- If under 10K records: Client-side with Fuse.js
- If 10K-100K records: SQLite FTS5
- If 100K+ records: Meilisearch or Typesense (self-hosted, free)

Build the [APPROPRIATE OPTION] version. Include the search UI component with results dropdown.
```

### Prompt 114: Email Sending Function
```
Build a function that sends emails from my app.

Service: [SENDGRID / RESEND / POSTMARK / SES]
API key location: Environment variable [VAR_NAME]

Email types I need:
1. [TYPE 1 — e.g., "Welcome email after signup"]
2. [TYPE 2 — e.g., "Password reset with link"]
3. [TYPE 3 — e.g., "Order confirmation with details"]

For each type, create:
- HTML template (inline CSS, responsive, matches [BRAND COLORS])
- Plain text fallback
- Function with proper parameters
- Error handling and retry logic

Include a test function that sends a sample email to verify setup.
```

### Prompt 115: PDF Generator
```
Build a function that generates PDFs from data.

Use case: [WHAT THE PDF IS — invoice, report, certificate, resume, etc.]

Data inputs:
[LIST THE DATA FIELDS THAT GO INTO THE PDF]

Library: [Puppeteer for HTML-to-PDF / jsPDF for client-side / ReportLab for Python]

Requirements:
- Professional layout (header, body, footer with page numbers)
- Company logo placeholder
- Consistent fonts and spacing
- Table support (if applicable)
- Output: Save to file and/or return as buffer for download

Include a sample data object and the expected PDF layout description.
```

### Prompt 116: Rate Limiter
```
Implement rate limiting for my API.

Strategy: [FIXED WINDOW / SLIDING WINDOW / TOKEN BUCKET]
Limit: [NUMBER] requests per [TIME PERIOD] per [IP / API KEY / USER ID]

Requirements:
- Return 429 Too Many Requests when limit exceeded
- Include Retry-After header
- Include X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset headers
- Storage: [IN-MEMORY / REDIS]
- Exempt certain routes: [LIST ROUTES THAT SHOULDN'T BE LIMITED]
- Different limits for authenticated vs. unauthenticated users

Framework: [EXPRESS / FASTIFY / FLASK / etc.]
```

### Prompt 117: Logging System
```
Set up structured logging for my [LANGUAGE] application.

Requirements:
- Log levels: DEBUG, INFO, WARN, ERROR
- JSON format in production, pretty-printed in development
- Include: timestamp, level, message, request ID (for tracing), duration (for performance)
- Write to stdout (for container/serverless environments)
- Sensitive data masking (mask emails, API keys, passwords in logs)

Library: [winston for Node.js / structlog for Python / zerolog for Go / pino for Node.js]

Include:
- Logger initialization code
- Middleware that logs every HTTP request (method, path, status code, duration)
- Example usage for each log level
- How to search logs in production (grep patterns or dashboard recommendations)
```

### Prompt 118: Feature Flag System
```
Build a simple feature flag system for my app.

Requirements:
- Define flags in a JSON config file
- Check flags in code: if (flags.isEnabled('new_checkout')) { ... }
- Support flag types: boolean (on/off), percentage (roll out to X% of users), user list (enable for specific user IDs)
- Admin endpoint to toggle flags without redeployment
- Default to "off" if a flag doesn't exist

Storage: [JSON FILE / DATABASE / ENVIRONMENT VARIABLES]
Language: [LANGUAGE]

Include 5 example flags and the code to check them in different contexts (API route, UI component, background job).
```

### Prompt 119: CI/CD Pipeline
```
Set up a CI/CD pipeline for my project using [GITHUB ACTIONS / GITLAB CI / etc.].

On every push to a feature branch:
1. Run linter
2. Run tests
3. Build the project
4. Deploy to preview environment

On merge to main:
1. All of the above
2. Deploy to production
3. Post deployment notification to [SLACK WEBHOOK URL / "console" for now]

Project type: [LANGUAGE/FRAMEWORK]
Test command: [COMMAND]
Build command: [COMMAND]
Deploy target: [NETLIFY / VERCEL / AWS / etc.]

Include the YAML config file with comments explaining each step.
```

### Prompt 120: Docker Setup
```
Dockerize my [LANGUAGE/FRAMEWORK] application.

Application entry point: [FILE]
Dependencies: [PACKAGE MANAGER AND LOCKFILE]
Port: [PORT]
Environment variables needed: [LIST]

Provide:
1. Dockerfile (multi-stage build for smallest image size)
2. .dockerignore
3. docker-compose.yml (app + [ANY DEPENDENCIES — database, redis, etc.])
4. Commands to build, run, and stop

Optimize for:
- Image size (use alpine base images)
- Build speed (layer caching for dependencies)
- Security (non-root user, no unnecessary packages)
- Development experience (hot reload with volume mounts)
```
