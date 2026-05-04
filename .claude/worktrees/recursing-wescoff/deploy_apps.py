#!/usr/bin/env python3
"""
PRINTMAXX PWA Deployer
Deploys all 6 PWA apps to production using the first available method.

Methods tried in order:
1. Vercel (with --token if VERCEL_TOKEN env var set)
2. Surge.sh (with SURGE_LOGIN + SURGE_TOKEN env vars)
3. Netlify (with NETLIFY_AUTH_TOKEN env var)

Usage:
  # Method 1: Set env vars first, then run
  export VERCEL_TOKEN="your_token_here"
  python3 deploy_apps.py

  # Method 2: Vercel login first, then run
  vercel login
  python3 deploy_apps.py

  # Method 3: Surge login first
  surge login
  python3 deploy_apps.py

  # Method 4: Netlify login first
  netlify login
  python3 deploy_apps.py

Quick Vercel Token:
  1. Go to https://vercel.com/account/tokens
  2. Create a new token
  3. export VERCEL_TOKEN="your_token"
  4. python3 deploy_apps.py
"""

import os
import subprocess
import sys
from datetime import datetime

BASE_DIR = "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/loops/app_factory/output"
OUTPUT_FILE = "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/OPS/DEPLOYMENT_URLS.md"

# Priority order (Ramadan tracker first!)
APPS = [
    "ramadan-tracker",
    "focuslock-web",
    "habitforge-web",
    "mealmaxx-web",
    "sleepmaxx-web",
    "walktounlock-web",
]

results = {}

def run(cmd, cwd=None, timeout=120):
    """Run a command and return (success, output)"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            cwd=cwd, timeout=timeout
        )
        output = result.stdout.strip() + "\n" + result.stderr.strip()
        return result.returncode == 0, output.strip()
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except Exception as e:
        return False, str(e)

def deploy_vercel(app_name, app_dir):
    """Deploy via Vercel CLI"""
    token = os.environ.get("VERCEL_TOKEN", "")
    token_flag = f"--token {token}" if token else ""

    # Check auth
    ok, out = run(f"vercel whoami {token_flag}")
    if not ok and not token:
        print(f"  Vercel: Not authenticated (set VERCEL_TOKEN or run 'vercel login')")
        return None

    cmd = f"vercel deploy --prod --yes {token_flag}"
    print(f"  Deploying {app_name} via Vercel...")
    ok, out = run(cmd, cwd=app_dir, timeout=180)

    if ok:
        # Extract URL from output
        lines = out.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("http"):
                return line

    print(f"  Vercel deploy failed: {out[:200]}")
    return None

def deploy_surge(app_name, app_dir):
    """Deploy via Surge.sh"""
    token = os.environ.get("SURGE_TOKEN", "")
    login = os.environ.get("SURGE_LOGIN", "")

    if not token:
        # Check if logged in
        ok, out = run("surge whoami")
        if "Not Authenticated" in out:
            print(f"  Surge: Not authenticated (set SURGE_LOGIN + SURGE_TOKEN or run 'surge login')")
            return None

    domain = f"{app_name}.surge.sh"

    if token and login:
        cmd = f"surge --project {app_dir} --domain {domain}"
        env = os.environ.copy()
        env["SURGE_LOGIN"] = login
        env["SURGE_TOKEN"] = token
    else:
        cmd = f"surge {app_dir} {domain}"

    print(f"  Deploying {app_name} via Surge to {domain}...")
    ok, out = run(cmd, timeout=120)

    if ok:
        return f"https://{domain}"

    print(f"  Surge deploy failed: {out[:200]}")
    return None

def deploy_netlify(app_name, app_dir):
    """Deploy via Netlify CLI"""
    token = os.environ.get("NETLIFY_AUTH_TOKEN", "")
    token_flag = f"--auth {token}" if token else ""

    if not token:
        ok, out = run("netlify status")
        if "Not logged in" in out:
            print(f"  Netlify: Not authenticated (set NETLIFY_AUTH_TOKEN or run 'netlify login')")
            return None

    cmd = f"netlify deploy --prod --dir {app_dir} {token_flag}"
    print(f"  Deploying {app_name} via Netlify...")
    ok, out = run(cmd, timeout=180)

    if ok:
        for line in out.split("\n"):
            if "Website URL:" in line or "https://" in line:
                url = line.split("https://")[-1].strip()
                if url:
                    return f"https://{url}"

    print(f"  Netlify deploy failed: {out[:200]}")
    return None

def main():
    print("=" * 60)
    print("  PRINTMAXX PWA DEPLOYER")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    # Try each deployment method
    deployers = [
        ("Vercel", deploy_vercel),
        ("Surge", deploy_surge),
        ("Netlify", deploy_netlify),
    ]

    success_count = 0

    for app_name in APPS:
        app_dir = os.path.join(BASE_DIR, app_name)

        if not os.path.exists(os.path.join(app_dir, "index.html")):
            print(f"\n[SKIP] {app_name} - no index.html found")
            results[app_name] = ("SKIP", "No index.html")
            continue

        print(f"\n{'='*40}")
        print(f"[DEPLOY] {app_name}")
        print(f"{'='*40}")

        deployed = False
        for method_name, deployer in deployers:
            url = deployer(app_name, app_dir)
            if url:
                print(f"  SUCCESS: {url}")
                results[app_name] = ("LIVE", url)
                success_count += 1
                deployed = True
                break

        if not deployed:
            results[app_name] = ("FAILED", "All methods failed - need auth")
            print(f"  FAILED: No deployment method available")

    # Write results
    write_results(success_count)

    print(f"\n{'='*60}")
    print(f"  RESULTS: {success_count}/{len(APPS)} deployed")
    print(f"  URLs saved to: {OUTPUT_FILE}")
    print(f"{'='*60}")

    if success_count == 0:
        print("""
NO DEPLOYMENTS SUCCEEDED - Authentication needed.

Fastest fix (pick one):

OPTION 1 - Vercel (recommended):
  1. Go to https://vercel.com/account/tokens
  2. Create a token
  3. Run: export VERCEL_TOKEN="your_token_here"
  4. Run: python3 deploy_apps.py

OPTION 2 - Vercel login:
  1. Run: vercel login
  2. Follow browser auth flow
  3. Run: python3 deploy_apps.py

OPTION 3 - Surge.sh:
  1. Run: surge login
  2. Enter email + password
  3. Run: python3 deploy_apps.py

OPTION 4 - Manual one-liner per app:
  cd /path/to/app && vercel deploy --prod --yes
""")

def write_results(success_count):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Ensure OPS directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, 'w') as f:
        f.write("# PRINTMAXX PWA Deployment URLs\n\n")
        f.write(f"**Last updated:** {timestamp}\n\n")
        f.write("---\n\n")
        f.write("## Production URLs\n\n")
        f.write("| App | URL | Status |\n")
        f.write("|-----|-----|--------|\n")

        for app_name in APPS:
            status, url_or_msg = results.get(app_name, ("UNKNOWN", ""))
            if status == "LIVE":
                f.write(f"| {app_name} | {url_or_msg} | LIVE |\n")
            else:
                f.write(f"| {app_name} | {url_or_msg} | {status} |\n")

        f.write(f"\n---\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- **Deployed:** {success_count}/{len(APPS)}\n")
        f.write(f"- **Timestamp:** {timestamp}\n\n")

        f.write("## App Details\n\n")
        f.write("| App | Brand Name | Description |\n")
        f.write("|-----|-----------|-------------|\n")
        f.write("| ramadan-tracker | Hilal | Ramadan companion - fasting, prayer times, Quran tracking |\n")
        f.write("| focuslock-web | Vault | Pomodoro timer with task tracking and stats |\n")
        f.write("| habitforge-web | HabitForge | Habit tracking and streak building |\n")
        f.write("| mealmaxx-web | MealMaxx | Meal planning and nutrition tracking |\n")
        f.write("| sleepmaxx-web | Dusk | Sleep tracking and optimization |\n")
        f.write("| walktounlock-web | WalkToUnlock | Walking incentive and step tracking |\n")

        f.write("\n## Notes\n\n")
        f.write("- All apps are single-file PWAs (index.html + manifest.json + sw.js)\n")
        f.write("- All apps work offline after first visit\n")
        f.write("- No backend required - all data in browser localStorage\n")
        f.write("- **Ramadan Tracker is HIGHEST PRIORITY** - Ramadan starts Feb 28, 2026\n")

        if success_count == 0:
            f.write("\n## Authentication Required\n\n")
            f.write("Deployment failed because no hosting platform is authenticated.\n\n")
            f.write("**Quick fix:** Run one of these:\n")
            f.write("```bash\n")
            f.write("# Option 1: Vercel\n")
            f.write("vercel login\n")
            f.write("python3 deploy_apps.py\n\n")
            f.write("# Option 2: Vercel with token\n")
            f.write("export VERCEL_TOKEN='your_token_from_vercel.com/account/tokens'\n")
            f.write("python3 deploy_apps.py\n\n")
            f.write("# Option 3: Surge.sh\n")
            f.write("surge login\n")
            f.write("python3 deploy_apps.py\n")
            f.write("```\n")

if __name__ == "__main__":
    main()
