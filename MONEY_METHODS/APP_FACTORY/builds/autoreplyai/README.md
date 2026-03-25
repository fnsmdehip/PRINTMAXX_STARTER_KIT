# AutoReplyAI

AI-powered customer support widget. Embed a chat widget on any website that answers customer questions using your knowledge base, powered by Google Gemini AI.

## Architecture

```
autoreplyai/
  backend/       Express + Prisma + SQLite API (port 3001)
  frontend/      Next.js dashboard for website owners (port 3000)
  backend/widget/  Embeddable chat widget (served from backend)
```

## Quick Start

### 1. Backend

```bash
cd backend
npm install
npx prisma generate
npx prisma migrate dev --name init
npm run dev
```

The backend starts on `http://localhost:3001`. Verify with `curl http://localhost:3001/health`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

The dashboard runs on `http://localhost:3000`.

### 3. Usage Flow

1. Go to `http://localhost:3000/signup` to register your website
2. Save the API key shown after registration
3. Log in at `http://localhost:3000/login` with your API key
4. Add knowledge base items in the dashboard (FAQs, page content, custom responses)
5. Copy the embed code from Widget Settings
6. Paste the embed code on your website

### 4. Widget Embed Code

```html
<script src="http://localhost:3001/widget/widget.js" data-key="YOUR_API_KEY"></script>
```

Optional data attributes:
- `data-color` - Override primary color (hex)
- `data-position` - `bottom-right` or `bottom-left`
- `data-greeting` - Custom greeting message

## API Endpoints

### Auth
- `POST /api/auth/register` - Register website, get API key
- `POST /api/auth/login` - Login with API key
- `GET /api/auth/me` - Get website info (requires x-api-key header)
- `PUT /api/auth/settings` - Update widget settings

### Widget (used by the embedded widget)
- `POST /api/widget/init` - Initialize chat session
- `POST /api/widget/chat` - Send message, get AI response
- `POST /api/widget/rate` - Rate a conversation

### Knowledge Base
- `GET /api/knowledge` - List all items
- `POST /api/knowledge` - Create item
- `POST /api/knowledge/bulk` - Bulk create items
- `PUT /api/knowledge/:id` - Update item
- `DELETE /api/knowledge/:id` - Delete item

### Analytics
- `GET /api/analytics/overview` - Dashboard stats
- `GET /api/analytics/messages-per-day` - Chart data
- `GET /api/analytics/conversations` - List conversations (with search)
- `GET /api/analytics/conversations/:id` - Single conversation

### Billing
- `GET /api/billing/plans` - List plans
- `POST /api/billing/checkout` - Start Stripe checkout
- `POST /api/billing/portal` - Stripe customer portal
- `GET /api/billing/status` - Current billing status
- `POST /api/billing/webhook` - Stripe webhook handler

## Plans

| Plan       | Price    | Messages/Month |
|------------|----------|----------------|
| Free       | $0       | 100            |
| Pro        | $29/mo   | 5,000          |
| Enterprise | $99/mo   | Unlimited      |

## Tech Stack

- **Backend**: Node.js, Express, Prisma, SQLite
- **AI**: Google Gemini API (primary), HuggingFace Inference (fallback)
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Payments**: Stripe Checkout + Customer Portal
- **Widget**: Vanilla JS, zero dependencies, works on any website

## Environment Variables

Backend `.env`:
```
DATABASE_URL="file:./dev.db"
GEMINI_API_KEY=your-gemini-key
STRIPE_SECRET_KEY=your-stripe-key
STRIPE_WEBHOOK_SECRET=optional-webhook-secret
PORT=3001
NODE_ENV=development
CORS_ORIGIN=http://localhost:3000
```

Frontend `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_APP_URL=http://localhost:3000
```
