# Code Style Rules

## General Principles

- **Clarity over cleverness** - Code should be obvious
- **Consistency** - Follow existing patterns
- **Simplicity** - Prefer simple solutions
- **DRY** - But don't abstract too early

## File Organization

```
LANDING/printmaxx-site/
├── app/
│   ├── (routes)/
│   │   ├── page.tsx          # Homepage
│   │   ├── truth/
│   │   │   ├── page.tsx      # Truth index
│   │   │   └── [slug]/
│   │   │       └── page.tsx  # Dynamic truth page
│   │   └── magnet/
│   │       └── stack-generator/
│   │           └── page.tsx
│   ├── layout.tsx            # Root layout
│   └── globals.css
├── components/
│   ├── ui/                   # Shadcn components
│   ├── forms/                # Form components
│   ├── layouts/              # Layout components
│   └── content/              # Content-specific
├── lib/
│   ├── utils.ts              # Utilities
│   ├── data.ts               # Data fetching
│   └── validation.ts         # Validation schemas
└── public/
    ├── images/
    └── content/
```

## Naming Conventions

**Files:**
- Components: `PascalCase.tsx`
- Utilities: `camelCase.ts`
- Constants: `SCREAMING_SNAKE_CASE.ts`
- Tests: `*.test.ts` or `*.spec.ts`

**Variables:**
```typescript
// ✅ Good
const userName = 'John';
const MAX_RETRIES = 3;
const isLoading = false;

// ❌ Bad
const user_name = 'John';
const maxretries = 3;
const loading = false; // unclear boolean
```

**Functions:**
```typescript
// ✅ Good - Clear, verb-first
function getUserById(id: string) {}
function calculateTotal(items: Item[]) {}
const handleSubmit = () => {};

// ❌ Bad
function user(id: string) {} // unclear
function total(items: Item[]) {} // not a verb
const submit = () => {}; // missing 'handle' convention
```

**Components:**
```typescript
// ✅ Good
function TruthPageCard({ title, excerpt }: Props) {}
const LeadCaptureForm = () => {};

// ❌ Bad
function Card({ title, excerpt }: Props) {} // too generic
const form = () => {}; // lowercase component
```

## TypeScript Guidelines

**Always:**
- Define prop interfaces
- Use type inference where obvious
- Avoid `any` (use `unknown` if needed)
- Use strict mode

```typescript
// ✅ Good
interface TruthPage {
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  publishedAt: Date;
}

function TruthPageCard({ title, excerpt }: Pick<TruthPage, 'title' | 'excerpt'>) {
  return <div>{title}</div>;
}

// ❌ Bad
function TruthPageCard(props: any) {
  return <div>{props.title}</div>;
}
```

## React Patterns

**Component structure:**
```typescript
// 1. Imports
import { useState } from 'react';
import { Button } from '@/components/ui/button';

// 2. Types
interface Props {
  title: string;
  onSubmit: (data: FormData) => void;
}

// 3. Component
export function LeadCaptureForm({ title, onSubmit }: Props) {
  // 3a. Hooks
  const [email, setEmail] = useState('');

  // 3b. Handlers
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ email });
  };

  // 3c. Render
  return (
    <form onSubmit={handleSubmit}>
      <h2>{title}</h2>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <Button type="submit">Submit</Button>
    </form>
  );
}
```

**Prefer:**
- Functional components over class components
- Named exports for components
- Default exports for pages
- Controlled components
- Server components by default (mark 'use client' when needed)

## Data Fetching

```typescript
// ✅ Good - Server component
async function TruthPage({ params }: { params: { slug: string } }) {
  const page = await getTruthPageBySlug(params.slug);
  return <TruthPageContent page={page} />;
}

// ✅ Good - Client component with SWR
'use client';
function TruthPageList() {
  const { data, error } = useSWR('/api/truth-pages', fetcher);
  if (error) return <Error />;
  if (!data) return <Loading />;
  return <List pages={data} />;
}
```

## Error Handling

```typescript
// ✅ Good - Specific errors
try {
  const page = await getTruthPage(slug);
  if (!page) {
    throw new NotFoundError(`Truth page not found: ${slug}`);
  }
  return page;
} catch (error) {
  if (error instanceof NotFoundError) {
    return notFound();
  }
  throw error;
}

// ❌ Bad - Silent failures
try {
  const page = await getTruthPage(slug);
  return page;
} catch {
  return null; // Lost error context
}
```

## Comments

**When to comment:**
- Complex algorithms (explain the why, not the what)
- Workarounds or hacks (explain why it's necessary)
- Public API functions (JSDoc)
- Non-obvious business logic

```typescript
// ✅ Good - Explains why
// Using setTimeout to avoid race condition with CSV file lock
setTimeout(() => saveToCsv(lead), 100);

// ❌ Bad - Restates code
// Set email to event target value
setEmail(e.target.value);
```

**Avoid:**
- Commented-out code (use git history)
- Obvious comments
- TODO comments without issue links

## Formatting

**Use Prettier with these settings:**
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

**Run on save:**
- Enable format-on-save in editor
- Use pre-commit hook for consistency

## Import Organization

```typescript
// 1. External packages
import { useState } from 'react';
import { cn } from 'clsx';

// 2. Internal absolute imports
import { Button } from '@/components/ui/button';
import { getTruthPages } from '@/lib/data';

// 3. Relative imports
import { TruthPageCard } from './TruthPageCard';
import { formatDate } from '../utils';

// 4. Types
import type { TruthPage } from '@/types';
```

## Testing

**File structure:**
```
components/
├── LeadCaptureForm.tsx
└── LeadCaptureForm.test.tsx
```

**Test organization:**
```typescript
describe('LeadCaptureForm', () => {
  it('renders title', () => {});
  it('validates email input', () => {});
  it('calls onSubmit with form data', () => {});
  it('shows error on invalid email', () => {});
});
```

## Before Committing

- [ ] Run `npm run lint`
- [ ] Run `npm run type-check`
- [ ] Run `npm test`
- [ ] Format code with Prettier
- [ ] Remove console.log statements
- [ ] Update types if needed
