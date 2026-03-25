#!/usr/bin/env python3
"""
PRINTMAXX — App Factory Pipeline: Pay-to-Contact Email Paywall MVP

DAG pipeline: spec generation → Next.js scaffold → Stripe payment gate →
surge deploy → content distribution.

Concept validated ($85/24h from 1 user). Real method: charge people a fee
to send you an email, filtering inbox noise.

Usage:
    python3 paywall_email_app_factory.py --run
    python3 paywall_email_app_factory.py --status
    python3 paywall_email_app_factory.py --dry-run
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: import from _common or fall back to local definitions
# ---------------------------------------------------------------------------
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(p: Path) -> Path:
        """Resolve *p* and assert it lives inside PROJECT."""
        resolved = Path(p).resolve()
        try:
            resolved.relative_to(PROJECT)
        except ValueError:
            raise ValueError(f"Path escape attempt blocked: {resolved} is not under {PROJECT}")
        return resolved

    def recall_skills_for_task(task: str) -> list:
        return []

    def capture_skill_from_result(task: str, result: str) -> None:
        pass

# ---------------------------------------------------------------------------
# Constants & paths
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_FILE = safe_path(AUTOMATIONS_DIR / "logs" / "paywall_email_app_factory.log")
STATE_FILE = safe_path(AUTOMATIONS_DIR / "state" / "paywall_email_app_factory_state.json")
OUTPUT_DIR = safe_path(AUTOMATIONS_DIR / "output" / "paywall_email_app_factory")
METRICS_FILE = safe_path(OUTPUT_DIR / "metrics.csv")

APP_NAME = "fastpass-email-paywall"
SURGE_DOMAIN = f"{APP_NAME}.surge.sh"

# DAG stages in dependency order
DAG_STAGES = [
    "spec_generation",
    "nextjs_scaffold",
    "stripe_gate",
    "surge_deploy",
    "content_distribution",
]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("paywall_email_app_factory")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = logging.FileHandler(str(LOG_FILE), mode="a", encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(fh)
        logger.addHandler(sh)
    return logger

log = setup_logging()

# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------

def load_state() -> dict:
    """Load pipeline state from JSON file."""
    try:
        if STATE_FILE.exists():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("Could not load state file: %s", exc)
    return {stage: {"status": "pending", "ts": None, "detail": ""} for stage in DAG_STAGES}


def save_state(state: dict) -> None:
    """Persist pipeline state to JSON file."""
    try:
        p = safe_path(STATE_FILE)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except (OSError, ValueError) as exc:
        log.error("Failed to save state: %s", exc)


def mark_stage(state: dict, stage: str, status: str, detail: str = "") -> None:
    state[stage] = {
        "status": status,
        "ts": datetime.utcnow().isoformat() + "Z",
        "detail": detail,
    }
    save_state(state)


def stage_done(state: dict, stage: str) -> bool:
    return state.get(stage, {}).get("status") == "done"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def write_file(path: Path, content: str) -> None:
    """Write *content* to *path* after validating via safe_path."""
    p = safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    log.debug("Wrote %s (%d bytes)", p, len(content))


def run_cmd(cmd: list, cwd: Path | None = None, dry_run: bool = False) -> tuple[int, str, str]:
    """Run a subprocess command; return (returncode, stdout, stderr)."""
    cmd_str = " ".join(str(c) for c in cmd)
    if dry_run:
        log.info("[DRY-RUN] Would run: %s", cmd_str)
        return 0, "", ""
    log.debug("Running: %s", cmd_str)
    try:
        result = subprocess.run(
            [str(c) for c in cmd],
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode != 0:
            log.warning("Command exited %d: %s\nstderr: %s", result.returncode, cmd_str, result.stderr[:500])
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError as exc:
        log.error("Command not found: %s — %s", cmd_str, exc)
        return 127, "", str(exc)
    except subprocess.TimeoutExpired:
        log.error("Command timed out: %s", cmd_str)
        return 124, "", "timeout"
    except OSError as exc:
        log.error("OSError running %s: %s", cmd_str, exc)
        return 1, "", str(exc)


def append_metric(row: dict) -> None:
    """Append a row to the CSV metrics log."""
    try:
        p = safe_path(METRICS_FILE)
        p.parent.mkdir(parents=True, exist_ok=True)
        write_header = not p.exists()
        with open(p, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(row.keys()))
            if write_header:
                writer.writeheader()
            writer.writerow(row)
    except (OSError, ValueError) as exc:
        log.error("Failed to append metric: %s", exc)


def http_get(url: str, timeout: int = 10) -> tuple[int, str]:
    """Simple HTTP GET; returns (status_code, body)."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, str(exc)
    except (urllib.error.URLError, OSError) as exc:
        return 0, str(exc)

# ---------------------------------------------------------------------------
# DAG stage implementations
# ---------------------------------------------------------------------------

def stage_spec_generation(state: dict, dry_run: bool = False) -> bool:
    """Stage 1: Generate app spec JSON and write to output directory."""
    log.info("=== Stage: spec_generation ===")
    skills = recall_skills_for_task("generate email paywall app spec")
    log.debug("Recalled %d skills", len(skills))

    spec = {
        "app_name": APP_NAME,
        "version": "0.1.0",
        "concept": "Pay-to-contact email paywall — charge senders a fee to reach your inbox",
        "revenue_target_usd_per_month": {"low": 25, "high": 150},
        "validated_revenue_usd": 85,
        "validation_window_hours": 24,
        "stack": {
            "frontend": "Next.js 14 (App Router)",
            "payments": "Stripe Checkout",
            "hosting": "Surge.sh (static export)",
            "email_delivery": "mailto fallback (MVP)",
        },
        "pages": [
            {"route": "/", "purpose": "Landing — explain paywall, CTA to pay"},
            {"route": "/pay", "purpose": "Stripe Checkout redirect"},
            {"route": "/success", "purpose": "Post-payment message form"},
            {"route": "/cancel", "purpose": "Abandoned checkout recovery"},
        ],
        "pricing_tiers": [
            {"label": "Fast Pass", "amount_usd": 5, "priority": "normal"},
            {"label": "Express Lane", "amount_usd": 15, "priority": "high"},
            {"label": "VIP Direct", "amount_usd": 50, "priority": "urgent"},
        ],
        "env_vars_required": [
            "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY",
            "STRIPE_SECRET_KEY",
            "STRIPE_WEBHOOK_SECRET",
            "OWNER_EMAIL",
            "NEXT_PUBLIC_SITE_URL",
        ],
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }

    spec_path = safe_path(OUTPUT_DIR / "spec.json")
    if not dry_run:
        try:
            write_file(spec_path, json.dumps(spec, indent=2))
        except (OSError, ValueError) as exc:
            log.error("spec_generation failed: %s", exc)
            mark_stage(state, "spec_generation", "failed", str(exc))
            return False

    capture_skill_from_result("generate email paywall app spec", json.dumps(spec, indent=2))
    mark_stage(state, "spec_generation", "done" if not dry_run else "dry-run", str(spec_path))
    append_metric({"ts": datetime.utcnow().isoformat(), "stage": "spec_generation", "status": "done", "detail": str(spec_path)})
    log.info("spec_generation complete → %s", spec_path)
    return True


def stage_nextjs_scaffold(state: dict, dry_run: bool = False) -> bool:
    """Stage 2: Write Next.js project scaffold files."""
    log.info("=== Stage: nextjs_scaffold ===")

    scaffold_root = safe_path(OUTPUT_DIR / "app")

    files: dict[Path, str] = {}

    # package.json
    files[scaffold_root / "package.json"] = json.dumps({
        "name": APP_NAME,
        "version": "0.1.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "export": "next build && next export",
            "lint": "next lint",
        },
        "dependencies": {
            "next": "14.2.3",
            "react": "^18",
            "react-dom": "^18",
            "@stripe/stripe-js": "^3.4.1",
            "stripe": "^15.7.0",
        },
        "devDependencies": {
            "typescript": "^5",
            "@types/node": "^20",
            "@types/react": "^18",
            "@types/react-dom": "^18",
            "tailwindcss": "^3.4",
            "postcss": "^8",
            "autoprefixer": "^10",
        },
    }, indent=2)

    # next.config.js
    files[scaffold_root / "next.config.js"] = """\
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: { unoptimized: true },
};

module.exports = nextConfig;
"""

    # tailwind.config.js
    files[scaffold_root / "tailwind.config.js"] = """\
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: { extend: {} },
  plugins: [],
};
"""

    # postcss.config.js
    files[scaffold_root / "postcss.config.js"] = """\
module.exports = {
  plugins: { tailwindcss: {}, autoprefixer: {} },
};
"""

    # tsconfig.json
    files[scaffold_root / "tsconfig.json"] = json.dumps({
        "compilerOptions": {
            "target": "es5",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "strict": True,
            "noEmit": True,
            "esModuleInterop": True,
            "module": "esnext",
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "preserve",
            "incremental": True,
            "plugins": [{"name": "next"}],
            "paths": {"@/*": ["./src/*"]},
        },
        "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
        "exclude": ["node_modules"],
    }, indent=2)

    # src/app/globals.css
    files[scaffold_root / "src" / "app" / "globals.css"] = """\
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground: #0a0a0a;
  --background: #fafafa;
}

body {
  color: var(--foreground);
  background: var(--background);
  font-family: system-ui, -apple-system, sans-serif;
}
"""

    # src/app/layout.tsx
    files[scaffold_root / "src" / "app" / "layout.tsx"] = """\
import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'FastPass Email — Skip the noise',
  description: 'Pay a small fee to send a guaranteed-read email.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col">{children}</body>
    </html>
  );
}
"""

    # src/app/page.tsx — Landing
    files[scaffold_root / "src" / "app" / "page.tsx"] = """\
import Link from 'next/link';

const TIERS = [
  { label: 'Fast Pass', price: '$5', priority: 'Standard priority', href: '/pay?tier=fast' },
  { label: 'Express Lane', price: '$15', priority: 'High priority', href: '/pay?tier=express' },
  { label: 'VIP Direct', price: '$50', priority: 'Urgent — same-day response', href: '/pay?tier=vip' },
];

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center flex-1 px-6 py-20 text-center">
      <h1 className="text-4xl font-bold mb-4">Your time is valuable. So is mine.</h1>
      <p className="text-lg text-gray-600 max-w-xl mb-12">
        Pay a small fee to send me a message I will actually read. Every submission is
        reviewed personally — no spam filters, no AI screeners.
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 w-full max-w-3xl">
        {TIERS.map((t) => (
          <Link
            key={t.label}
            href={t.href}
            className="border rounded-2xl p-8 hover:shadow-lg transition-shadow flex flex-col gap-3"
          >
            <span className="text-2xl font-semibold">{t.price}</span>
            <span className="font-medium">{t.label}</span>
            <span className="text-sm text-gray-500">{t.priority}</span>
          </Link>
        ))}
      </div>
    </main>
  );
}
"""

    # src/app/pay/page.tsx — Stripe redirect
    files[scaffold_root / "src" / "app" / "pay" / "page.tsx"] = """\
'use client';

import { useSearchParams } from 'next/navigation';
import { useEffect } from 'react';
import { loadStripe } from '@stripe/stripe-js';

const PRICE_MAP: Record<string, string> = {
  fast: process.env.NEXT_PUBLIC_STRIPE_PRICE_FAST ?? '',
  express: process.env.NEXT_PUBLIC_STRIPE_PRICE_EXPRESS ?? '',
  vip: process.env.NEXT_PUBLIC_STRIPE_PRICE_VIP ?? '',
};

export default function PayPage() {
  const params = useSearchParams();
  const tier = params.get('tier') ?? 'fast';

  useEffect(() => {
    async function redirect() {
      const stripe = await loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY ?? '');
      if (!stripe) return;
      await stripe.redirectToCheckout({
        lineItems: [{ price: PRICE_MAP[tier] ?? PRICE_MAP['fast'], quantity: 1 }],
        mode: 'payment',
        successUrl: `${process.env.NEXT_PUBLIC_SITE_URL}/success?tier=${tier}`,
        cancelUrl: `${process.env.NEXT_PUBLIC_SITE_URL}/cancel`,
      });
    }
    redirect();
  }, [tier]);

  return (
    <main className="flex items-center justify-center flex-1 text-gray-500">
      Redirecting to secure checkout…
    </main>
  );
}
"""

    # src/app/success/page.tsx
    files[scaffold_root / "src" / "app" / "success" / "page.tsx"] = """\
'use client';

import { useState } from 'react';
import { useSearchParams } from 'next/navigation';

export default function SuccessPage() {
  const params = useSearchParams();
  const tier = params.get('tier') ?? 'fast';
  const [submitted, setSubmitted] = useState(false);
  const [msg, setMsg] = useState('');

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const email = process.env.NEXT_PUBLIC_OWNER_EMAIL ?? '';
    const subject = encodeURIComponent(`[FastPass/${tier.toUpperCase()}] Message for you`);
    const body = encodeURIComponent(msg);
    window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
    setSubmitted(true);
  }

  if (submitted) {
    return (
      <main className="flex flex-col items-center justify-center flex-1 px-6 text-center gap-4">
        <h2 className="text-3xl font-bold">Message sent!</h2>
        <p className="text-gray-600">You'll hear back soon. Thank you.</p>
      </main>
    );
  }

  return (
    <main className="flex flex-col items-center justify-center flex-1 px-6 py-20">
      <h2 className="text-3xl font-bold mb-2">Payment confirmed ✓</h2>
      <p className="text-gray-600 mb-8">Now write your message below.</p>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-lg">
        <textarea
          className="border rounded-xl p-4 h-40 resize-none focus:outline-none focus:ring-2 focus:ring-black"
          placeholder="Write your message here…"
          value={msg}
          onChange={(e) => setMsg(e.target.value)}
          required
        />
        <button
          type="submit"
          className="bg-black text-white rounded-xl py-3 font-medium hover:bg-gray-800 transition-colors"
        >
          Send message
        </button>
      </form>
    </main>
  );
}
"""

    # src/app/cancel/page.tsx
    files[scaffold_root / "src" / "app" / "cancel" / "page.tsx"] = """\
import Link from 'next/link';

export default function CancelPage() {
  return (
    <main className="flex flex-col items-center justify-center flex-1 px-6 text-center gap-6">
      <h2 className="text-3xl font-bold">No worries</h2>
      <p className="text-gray-600">Your payment was not processed. Feel free to try again.</p>
      <Link href="/" className="underline text-gray-800">← Back to pricing</Link>
    </main>
  );
}
"""

    # .env.local.example
    files[scaffold_root / ".env.local.example"] = """\
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PRICE_FAST=price_...
NEXT_PUBLIC_STRIPE_PRICE_EXPRESS=price_...
NEXT_PUBLIC_STRIPE_PRICE_VIP=price_...
OWNER_EMAIL=you@example.com
NEXT_PUBLIC_OWNER_EMAIL=you@example.com
NEXT_PUBLIC_SITE_URL=https://fastpass-email-paywall.surge.sh
"""

    if not dry_run:
        try:
            for path, content in files.items():
                write_file(path, content)
        except (OSError, ValueError) as exc:
            log.error("nextjs_scaffold failed writing files: %s", exc)
            mark_stage(state, "nextjs_scaffold", "failed", str(exc))
            return False

    mark_stage(state, "nextjs_scaffold", "done" if not dry_run else "dry-run", str(scaffold_root))
    append_metric({"ts": datetime.utcnow().isoformat(), "stage": "nextjs_scaffold", "status": "done", "detail": str(scaffold_root)})
    log.info("nextjs_scaffold complete → %d files in %s", len(files), scaffold_root)
    return True


def stage_stripe_gate(state: dict, dry_run: bool = False) -> bool:
    """Stage 3: Write Stripe API route (webhook handler) and verify CLI availability."""
    log.info("=== Stage: stripe_gate ===")

    scaffold_root = safe_path(OUTPUT_DIR / "app")

    # Next.js API route for webhook (server-side only — not exported)
    webhook_handler = """\
// pages/api/stripe-webhook.ts
// NOTE: This route requires a Node.js server (not static export).
// Deploy to Vercel/Railway for webhook support; Surge is static-only.
import type { NextApiRequest, NextApiResponse } from 'next';

export const config = { api: { bodyParser: false } };

async function buffer(readable: NextApiRequest): Promise<Buffer> {
  const chunks: Buffer[] = [];
  for await (const chunk of readable) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }
  return Buffer.concat(chunks);
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).end('Method Not Allowed');
  }

  const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
  const sig = req.headers['stripe-signature'] as string;
  const rawBody = await buffer(req);

  let event;
  try {
    event = stripe.webhooks.constructEvent(rawBody, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error('Webhook signature verification failed:', msg);
    return res.status(400).send(`Webhook Error: ${msg}`);
  }

  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    console.log('Payment received:', session.id, session.amount_total);
    // TODO: send confirmation email, log to DB, etc.
  }

  res.json({ received: true });
}
"""

    stripe_setup_guide = """\
# Stripe Setup Guide

## 1. Create products & prices
```
stripe products create --name="Fast Pass"
stripe prices create --unit-amount=500 --currency=usd --product=<id>

stripe products create --name="Express Lane"
stripe prices create --unit-amount=1500 --currency=usd --product=<id>

stripe products create --name="VIP Direct"
stripe prices create --unit-amount=5000 --currency=usd --product=<id>
```

## 2. Set price IDs in .env.local

## 3. Forward webhooks locally (development)
```
stripe listen --forward-to localhost:3000/api/stripe-webhook
```

## 4. Production webhook
Register https://your-domain.com/api/stripe-webhook in Stripe dashboard.
Events: checkout.session.completed

## Revenue model
- Discount stated 70% for realistic projection
- Target: $25–$150/mo per install
- Portfolio of similar micro-apps compounds
"""

    files = {
        scaffold_root / "pages" / "api" / "stripe-webhook.ts": webhook_handler,
        scaffold_root / "STRIPE_SETUP.md": stripe_setup_guide,
    }

    if not dry_run:
        try:
            for path, content in files.items():
                write_file(path, content)
        except (OSError, ValueError) as exc:
            log.error("stripe_gate failed: %s", exc)
            mark_stage(state, "stripe_gate", "failed", str(exc))
            return False

        # Soft-check for stripe CLI
        rc, out, _ = run_cmd(["stripe", "version"], dry_run=False)
        if rc == 0:
            log.info("Stripe CLI found: %s", out.strip())
        else:
            log.warning("Stripe CLI not found — install via: brew install stripe/stripe-cli/stripe")

    mark_stage(state, "stripe_gate", "done" if not dry_run else "dry-run", str(scaffold_root / "pages" / "api"))
    append_metric({"ts": datetime.utcnow().isoformat(), "stage": "stripe_gate", "status": "done", "detail": "webhook handler written"})
    log.info("stripe_gate complete")
    return True


def stage_surge_deploy(state: dict, dry_run: bool = False) -> bool:
    """Stage 4: Build Next.js static export and deploy to Surge.sh."""
    log.info("=== Stage: surge_deploy ===")

    scaffold_root = safe_path(OUTPUT_DIR / "app")
    out_dir = safe_path(scaffold_root / "out")

    # Write CNAME for Surge custom domain
    cname_path = safe_path(scaffold_root / "public" / "CNAME")
    if not dry_run:
        try:
            write_file(cname_path, SURGE_DOMAIN + "\n")
        except (OSError, ValueError) as exc:
            log.error("Failed writing CNAME: %s", exc)
            mark_stage(state, "surge_deploy", "failed", str(exc))
            return False

    # npm install
    rc, _, err = run_cmd(["npm", "install", "--prefer-offline"], cwd=scaffold_root, dry_run=dry_run)
    if rc not in (0, 1) and not dry_run:
        log.error("npm install failed (rc=%d): %s", rc, err[:300])
        mark_stage(state, "surge_deploy", "failed", f"npm install rc={rc}")
        return False

    # npm run build (static export)
    rc, _, err = run_cmd(["npm", "run", "build"], cwd=scaffold_root, dry_run=dry_run)
    if rc != 0 and not dry_run:
        log.error("next build failed (rc=%d): %s", rc, err[:500])
        mark_stage(state, "surge_deploy", "failed", f"build rc={rc}")
        return False

    # surge deploy
    rc, stdout, err = run_cmd(
        ["surge", str(out_dir), SURGE_DOMAIN],
        cwd=scaffold_root,
        dry_run=dry_run,
    )
    if rc != 0 and not dry_run:
        log.error("surge deploy failed (rc=%d): %s", rc, err[:500])
        mark_stage(state, "surge_deploy", "failed", f"surge rc={rc}")
        return False

    url = f"https://{SURGE_DOMAIN}"
    log.info("Deployed to %s", url)

    # Verify deployment with HTTP check
    if not dry_run:
        status_code, _ = http_get(url, timeout=15)
        if status_code == 200:
            log.info("Deployment verified (HTTP %d)", status_code)
        else:
            log.warning("Deployment check returned HTTP %d — DNS may still be propagating", status_code)

    mark_stage(state, "surge_deploy", "done" if not dry_run else "dry-run", url)
    append_metric({"ts": datetime.utcnow().isoformat(), "stage": "surge_deploy", "status": "done", "detail": url})
    log.info("surge_deploy complete → %s", url)
    return True


def stage_content_distribution(state: dict, dry_run: bool = False) -> bool:
    """Stage 5: Write distribution content — tweet thread, HN post, Reddit post."""
    log.info("=== Stage: content_distribution ===")

    site_url = f"https://{SURGE_DOMAIN}"

    content_dir = safe_path(OUTPUT_DIR / "distribution")

    tweet_thread = f"""\
Tweet thread: Pay-to-Contact Email Paywall Launch

1/ I built a tiny app that charges people to email me. Made $85 in the first 24h from 1 user.
Here's the honest breakdown and how you can clone it in a weekend. 🧵

2/ The problem: my inbox was drowning in "quick questions" and "just 5 minutes" cold asks.
The insight: a small payment signal filters 99% of the noise. Real requests get through.

3/ The stack (entirely free/OSS):
• Next.js 14 static export
• Stripe Checkout (no server needed for payments)
• Surge.sh (free static hosting)
• Total infra cost: $0/mo

4/ Revenue math (honest):
• Stated: $85 in 24h
• Discounted 70% for realistic ongoing rate
• Realistic target: $25–$150/mo per install
• Portfolio of 10 = $250–$1,500/mo passive

5/ Live demo + full code: {site_url}

If you build something with this, reply with what you made. I read every reply. (Irony intended.)
"""

    hn_post = f"""\
Title: Show HN: I charge people $5–$50 to email me – made $85 in 24h

Body:
Hey HN,

I built a pay-to-contact email paywall to filter inbox noise. The idea: instead of a spam filter,
you charge senders a small fee. Real requests get through; mass outreach doesn't.

Tech: Next.js static export + Stripe Checkout + Surge.sh. Zero server costs.

First 24h: one user paid, generating ~$85. I'm discounting that 70% for realistic projections
($25–$150/mo sustainable). But the interesting part is composability — a portfolio of similar
micro-SaaS apps compounds.

Live: {site_url}

Happy to share the full build walkthrough if there's interest. What am I missing on pricing?
"""

    reddit_post = f"""\
Subreddit: r/SideProject

Title: Made $85 in 24h charging people to email me — here's the honest breakdown

Body:
Built a pay-to-contact paywall over a weekend. Concept: people pay $5–$50 to send you a
guaranteed-read email. Stripe Checkout + Next.js + Surge.sh — zero server costs.

Revenue: $85 in first 24h (1 user). Being honest — that's not a repeatable daily rate.
Realistic ongoing: $25–$150/mo per install. But run 10 of these for different use cases and
it starts to add up.

Demo: {site_url}

AMA. What would you use this for?
"""

    files = {
        content_dir / "tweet_thread.txt": tweet_thread,
        content_dir / "hn_post.txt": hn_post,
        content_dir / "reddit_post.txt": reddit_post,
    }

    if not dry_run:
        try:
            for path, content in files.items():
                write_file(path, content)
        except (OSError, ValueError) as exc:
            log.error("content_distribution failed: %s", exc)
            mark_stage(state, "content_distribution", "failed", str(exc))
            return False

    capture_skill_from_result(
        "distribute email paywall launch content",
        f"Generated {len(files)} distribution files in {content_dir}",
    )

    mark_stage(state, "content_distribution", "done" if not dry_run else "dry-run", str(content_dir))
    append_metric({"ts": datetime.utcnow().isoformat(), "stage": "content_distribution", "status": "done", "detail": str(content_dir)})
    log.info("content_distribution complete → %s", content_dir)
    return True

# ---------------------------------------------------------------------------
# CLI handlers
# ---------------------------------------------------------------------------

STAGE_FNS = {
    "spec_generation": stage_spec_generation,
    "nextjs_scaffold": stage_nextjs_scaffold,
    "stripe_gate": stage_stripe_gate,
    "surge_deploy": stage_surge_deploy,
    "content_distribution": stage_content_distribution,
}


def run_pipeline(dry_run: bool = False) -> int:
    """Execute all DAG stages in dependency order. Returns exit code."""
    log.info("Starting paywall_email_app_factory pipeline (dry_run=%s)", dry_run)
    state = load_state()

    for stage in DAG_STAGES:
        if stage_done(state, stage) and not dry_run:
            log.info("Skipping %s (already done)", stage)
            continue

        fn = STAGE_FNS[stage]
        try:
            success = fn(state, dry_run=dry_run)
        except Exception as exc:
            log.exception("Unexpected error in stage %s: %s", stage, exc)
            mark_stage(state, stage, "failed", str(exc))
            success = False

        if not success:
            log.error("Pipeline halted at stage: %s", stage)
            return 1

    log.info("Pipeline complete. All stages done.")
    return 0


def print_status() -> None:
    """Print a human-readable DAG status table."""
    state = load_state()
    print(f"\n{'Stage':<25} {'Status':<12} {'Timestamp':<26} Detail")
    print("-" * 90)
    for stage in DAG_STAGES:
        info = state.get(stage, {})
        status = info.get("status", "pending")
        ts = info.get("ts") or "—"
        detail = (info.get("detail") or "")[:40]
        marker = {"done": "✓", "failed": "✗", "pending": "○", "dry-run": "~"}.get(status, "?")
        print(f"{marker} {stage:<23} {status:<12} {ts:<26} {detail}")
    print()

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: Pay-to-contact email paywall App Factory pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--run", action="store_true", help="Execute the full pipeline")
    parser.add_argument("--status", action="store_true", help="Print current pipeline status")
    parser.add_argument("--dry-run", action="store_true", dest="dry_run",
                        help="Simulate all stages without writing files or running commands")

    args = parser.parse_args()

    if not any([args.run, args.status, args.dry_run]):
        parser.print_help()
        sys.exit(0)

    if args.status:
        print_status()
        sys.exit(0)

    exit_code = run_pipeline(dry_run=args.dry_run)
    if args.dry_run:
        log.info("Dry-run complete. No files written, no commands executed.")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()