#!/usr/bin/env python3
"""
App Batch Fix - Apply common fixes across all SDK54 apps.

Copies missing templates (eas.json, subscriptionService, notificationService, MoreApps)
to all SDK54 app builds that are missing them.

Usage:
    python3 app_batch_fix.py audit          # Show what's missing per app
    python3 app_batch_fix.py fix-eas        # Copy eas.json to missing apps
    python3 app_batch_fix.py fix-all        # Apply all fixes
    python3 app_batch_fix.py status         # Show completion status per app
"""

import json
import shutil
import argparse
from pathlib import Path

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
BUILDS_DIR = PROJECT_DIR / "MONEY_METHODS" / "APP_FACTORY" / "builds"
TEMPLATES_DIR = PROJECT_DIR / "MONEY_METHODS" / "APP_FACTORY" / "templates"


def get_sdk54_apps() -> list[Path]:
    """Get all SDK54 app directories."""
    return sorted([
        d for d in BUILDS_DIR.iterdir()
        if d.is_dir() and d.name.endswith('-sdk54')
    ])


def audit_app(app_dir: Path) -> dict:
    """Audit a single app for missing components."""
    result = {
        'name': app_dir.name,
        'has_package_json': (app_dir / 'package.json').exists(),
        'has_app_json': (app_dir / 'app.json').exists(),
        'has_eas_json': (app_dir / 'eas.json').exists(),
        'has_tsconfig': (app_dir / 'tsconfig.json').exists(),
        'has_node_modules': (app_dir / 'node_modules').exists(),
        'has_subscription_service': False,
        'has_notification_service': False,
        'has_more_apps': False,
    }

    # Search for service files
    for path in app_dir.rglob('*.ts'):
        name = path.name.lower()
        if 'subscription' in name and 'service' in name:
            result['has_subscription_service'] = True
        if 'notification' in name and 'service' in name:
            result['has_notification_service'] = True

    for path in app_dir.rglob('*.tsx'):
        name = path.name.lower()
        if 'moreapps' in name or 'more_apps' in name or 'more-apps' in name:
            result['has_more_apps'] = True

    return result


def cmd_audit(args):
    """Audit all SDK54 apps."""
    apps = get_sdk54_apps()

    print(f"\n{'App':<25} {'pkg':<5} {'app':<5} {'eas':<5} {'sub':<5} {'notif':<5} {'xpromo':<5} {'deps':<5}")
    print("-" * 70)

    for app_dir in apps:
        r = audit_app(app_dir)
        def yn(val): return 'Y' if val else '-'
        print(
            f"{r['name']:<25} "
            f"{yn(r['has_package_json']):<5} "
            f"{yn(r['has_app_json']):<5} "
            f"{yn(r['has_eas_json']):<5} "
            f"{yn(r['has_subscription_service']):<5} "
            f"{yn(r['has_notification_service']):<5} "
            f"{yn(r['has_more_apps']):<5} "
            f"{yn(r['has_node_modules']):<5}"
        )

    print(f"\nLegend: pkg=package.json, app=app.json, eas=eas.json, sub=subscriptionService, notif=notificationService, xpromo=MoreApps, deps=node_modules")


def cmd_fix_eas(args):
    """Copy eas.json template to apps missing it."""
    template = TEMPLATES_DIR / "eas.json"
    if not template.exists():
        print(f"Template not found: {template}")
        return

    apps = get_sdk54_apps()
    fixed = 0

    for app_dir in apps:
        eas_path = app_dir / "eas.json"
        if not eas_path.exists():
            shutil.copy2(template, eas_path)
            print(f"  Created: {app_dir.name}/eas.json")
            fixed += 1

    print(f"\nFixed {fixed} apps")


def cmd_fix_all(args):
    """Apply all missing templates."""
    apps = get_sdk54_apps()
    total_fixes = 0

    for app_dir in apps:
        audit = audit_app(app_dir)
        fixes = []

        # eas.json
        if not audit['has_eas_json']:
            src = TEMPLATES_DIR / "eas.json"
            if src.exists():
                shutil.copy2(src, app_dir / "eas.json")
                fixes.append("eas.json")

        # subscriptionService.ts
        if not audit['has_subscription_service']:
            src = TEMPLATES_DIR / "subscriptionService.ts"
            if src.exists():
                services_dir = app_dir / "src" / "services"
                services_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, services_dir / "subscriptionService.ts")
                fixes.append("subscriptionService.ts")

        # notificationService.ts
        if not audit['has_notification_service']:
            src = TEMPLATES_DIR / "notificationService.ts"
            if src.exists():
                services_dir = app_dir / "src" / "services"
                services_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, services_dir / "notificationService.ts")
                fixes.append("notificationService.ts")

        # MoreApps.tsx
        if not audit['has_more_apps']:
            src = TEMPLATES_DIR / "MoreApps.tsx"
            if src.exists():
                components_dir = app_dir / "src" / "components"
                components_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, components_dir / "MoreApps.tsx")
                fixes.append("MoreApps.tsx")

        if fixes:
            print(f"  {app_dir.name}: Added {', '.join(fixes)}")
            total_fixes += len(fixes)

    print(f"\nTotal fixes applied: {total_fixes}")


def cmd_status(args):
    """Show completion status per app."""
    apps = get_sdk54_apps()

    print(f"\n{'App':<25} {'Completion':>12} {'Missing'}")
    print("-" * 70)

    for app_dir in apps:
        audit = audit_app(app_dir)

        checks = [
            audit['has_package_json'],
            audit['has_app_json'],
            audit['has_eas_json'],
            audit['has_subscription_service'],
            audit['has_notification_service'],
            audit['has_more_apps'],
            audit['has_node_modules'],
        ]

        total = len(checks)
        passing = sum(checks)
        pct = passing / total * 100

        missing = []
        if not audit['has_eas_json']:
            missing.append('eas')
        if not audit['has_subscription_service']:
            missing.append('sub')
        if not audit['has_notification_service']:
            missing.append('notif')
        if not audit['has_more_apps']:
            missing.append('xpromo')

        missing_str = ', '.join(missing) if missing else 'None'
        print(f"{app_dir.name:<25} {passing}/{total} ({pct:.0f}%)    {missing_str}")


def main():
    parser = argparse.ArgumentParser(description='App Batch Fix Tool')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('audit', help='Audit all SDK54 apps')
    subparsers.add_parser('fix-eas', help='Copy eas.json to missing apps')
    subparsers.add_parser('fix-all', help='Apply all fixes')
    subparsers.add_parser('status', help='Show completion status')

    args = parser.parse_args()

    commands = {
        'audit': cmd_audit,
        'fix-eas': cmd_fix_eas,
        'fix-all': cmd_fix_all,
        'status': cmd_status,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
